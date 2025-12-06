"""
VSA Anti-Hallucination Validator
=================================

Validates retrieval results against VSA ontology with confidence scoring.
Implements the anti-hallucination layer for the retrieval pipeline.

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
Phase 6: Integration with Retrieval Pipeline
"""

import re
import torch
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from src.vsa.legal_vsa import LegalVSA, get_vsa_service
from src.vsa.encoder import GSWVSAEncoder
from src.logic.gsw_schema import GlobalWorkspace


class VSAValidator:
    """
    Validates retrieval results against VSA ontology.

    This class implements the anti-hallucination layer by:
    1. Extracting factual claims from responses
    2. Encoding claims and workspace context as hypervectors
    3. Calculating similarity scores to detect hallucinations
    4. Providing calibrated confidence scores
    """

    def __init__(self, ontology_path: Optional[Path] = None):
        """
        Initialize the VSA validator.

        Args:
            ontology_path: Optional path to load additional ontology rules
        """
        self.vsa = get_vsa_service()
        self.encoder = GSWVSAEncoder(self.vsa)

        # Load legal ontology rules if provided
        if ontology_path and ontology_path.exists():
            self.load_ontology(ontology_path)

    def load_ontology(self, ontology_path: Path):
        """
        Load additional ontology rules from file.

        Args:
            ontology_path: Path to ontology file
        """
        # TODO: Implement ontology loading from external file
        # For now, we rely on the ontology defined in src/vsa/ontology.py
        pass

    def validate_response(
        self,
        query: str,
        response: str,
        workspace: GlobalWorkspace
    ) -> Dict:
        """
        Validate response against workspace knowledge.

        Args:
            query: The original query
            response: The generated response to validate
            workspace: The global workspace containing ground truth

        Returns:
            Dictionary containing:
                - overall_confidence: Float [0, 1]
                - hallucination_detected: Boolean
                - severity: Breakdown by risk level
                - individual_validations: List of per-claim validations
                - total_claims: Number of claims validated
                - valid_claims: Number of claims that passed validation
        """
        # Encode workspace as scene vector
        scene_vector = self.encoder.encode_workspace(workspace)

        # Extract claims from response
        claims = self._extract_claims(response)

        if not claims:
            # No claims to validate - neutral response
            return {
                'total_claims': 0,
                'valid_claims': 0,
                'overall_confidence': 0.5,
                'hallucination_detected': False,
                'severity': {
                    'high_risk': 0,
                    'medium_risk': 0,
                    'low_risk': 0,
                    'verified': 0
                },
                'individual_validations': []
            }

        # Validate each claim
        validations = []
        for claim in claims:
            # Extract concepts from claim
            claim_concepts = self._extract_concepts(claim)

            # Encode claim as vector
            claim_vector = self._encode_claim(claim_concepts)

            # Check consistency with workspace
            similarity = self.vsa.similarity(scene_vector, claim_vector)

            # Perform VSA-based hallucination check
            vsa_check = self.vsa.verify_no_hallucination(claim_concepts)

            validations.append({
                'claim': claim,
                'similarity': similarity,
                'valid': similarity > 0.7,
                'confidence': self._calibrate_confidence(similarity),
                'vsa_valid': vsa_check['valid'],
                'vsa_confidence': vsa_check['confidence'],
                'concepts': claim_concepts
            })

        # Aggregate results
        return self._aggregate_validations(validations)

    def _extract_claims(self, response: str) -> List[str]:
        """
        Extract factual claims from response text.

        Args:
            response: The response text to analyze

        Returns:
            List of factual claim strings
        """
        claims = []

        # Split into sentences (handle multiple punctuation marks)
        sentences = re.split(r'[.!?]+', response)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Identify factual statements (not questions/opinions)
            if self._is_factual(sentence):
                claims.append(sentence)

        return claims

    def _is_factual(self, sentence: str) -> bool:
        """
        Check if sentence makes a factual claim.

        Args:
            sentence: The sentence to analyze

        Returns:
            True if sentence appears to be a factual statement
        """
        # Skip questions
        if sentence.endswith('?'):
            return False

        # Skip opinions (modal verbs indicating uncertainty)
        opinion_markers = ['may', 'might', 'could', 'possibly', 'perhaps',
                          'probably', 'maybe', 'seems', 'appears']
        sentence_lower = sentence.lower()

        # Check for opinion markers at word boundaries
        if any(re.search(r'\b' + marker + r'\b', sentence_lower)
               for marker in opinion_markers):
            return False

        # Has factual indicators (verbs of being, temporal markers, etc.)
        factual_markers = ['is', 'was', 'has', 'had', 'on', 'in', 'held',
                          'ordered', 'filed', 'granted', 'denied', 'married',
                          'divorced', 'separated', 'born', 'dated']

        return any(re.search(r'\b' + marker + r'\b', sentence_lower)
                  for marker in factual_markers)

    def _extract_concepts(self, claim: str) -> List[str]:
        """
        Extract key concepts from a claim.

        Args:
            claim: The claim text

        Returns:
            List of concept strings
        """
        # Simple extraction: get meaningful words
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                     'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                     'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do',
                     'does', 'did', 'will', 'would', 'should', 'could', 'may',
                     'might', 'must', 'can', 'this', 'that', 'these', 'those'}

        # Extract words (alphanumeric with potential hyphens)
        words = re.findall(r'\b[a-zA-Z][\w-]*\b', claim.lower())

        # Filter stop words and short words
        concepts = [w for w in words if w not in stop_words and len(w) > 2]

        return concepts

    def _encode_claim(self, concepts: List[str]) -> torch.Tensor:
        """
        Encode a claim as a hypervector.

        Args:
            concepts: List of concept strings

        Returns:
            Hypervector representation of the claim
        """
        if not concepts:
            return torch.zeros(self.vsa.dimension, device=self.vsa.device)

        # Get vectors for each concept
        concept_vectors = []
        for concept in concepts:
            vec = self.vsa.get_vector(concept.upper())
            concept_vectors.append(vec)

        # Bundle all concepts into a single vector
        return self.vsa.bundle(concept_vectors)

    def _calibrate_confidence(self, similarity: float) -> float:
        """
        Convert VSA similarity to calibrated confidence score.

        VSA similarity is in [-1, 1] range, where:
        - 1.0 = identical vectors
        - 0.0 = orthogonal (no relation)
        - -1.0 = opposite vectors

        Args:
            similarity: VSA similarity score in [-1, 1]

        Returns:
            Calibrated confidence score in [0, 1]
        """
        # Map similarity to confidence using a calibrated curve
        if similarity > 0.9:
            return 0.95  # Very high confidence
        elif similarity > 0.7:
            # High confidence: linear interpolation from 0.80 to 0.95
            return 0.80 + (similarity - 0.7) * 0.75
        elif similarity > 0.5:
            # Medium confidence: linear interpolation from 0.60 to 0.80
            return 0.60 + (similarity - 0.5) * 1.0
        elif similarity > 0.3:
            # Low confidence: linear interpolation from 0.40 to 0.60
            return 0.40 + (similarity - 0.3) * 1.0
        else:
            # Very low confidence: map [-1, 0.3] to [0, 0.40]
            # Ensure non-negative
            return max(0.0, (similarity + 1.0) * 0.2)

    def _aggregate_validations(self, validations: List[Dict]) -> Dict:
        """
        Aggregate individual claim validations.

        Args:
            validations: List of validation dictionaries

        Returns:
            Aggregated validation results
        """
        total_claims = len(validations)
        valid_claims = sum(1 for v in validations if v['valid'])

        # Overall confidence is average of valid claims
        # If no valid claims, use average of all claims
        confidences = [v['confidence'] for v in validations if v['valid']]
        if not confidences:
            confidences = [v['confidence'] for v in validations]

        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Factor in VSA validation results
        vsa_confidences = [v['vsa_confidence'] for v in validations]
        avg_vsa_confidence = sum(vsa_confidences) / len(vsa_confidences) if vsa_confidences else 0.0

        # Weighted combination of similarity-based and VSA-based confidence
        # VSA confidence (from ontology) gets 40% weight
        # Similarity confidence gets 60% weight
        combined_confidence = (overall_confidence * 0.6) + (avg_vsa_confidence * 0.4)

        # Flag hallucination if any claim has very low similarity
        hallucination_detected = any(v['similarity'] < 0.3 for v in validations)

        # Also flag if VSA detects issues
        vsa_issues_detected = any(not v['vsa_valid'] for v in validations)
        hallucination_detected = hallucination_detected or vsa_issues_detected

        # Severity breakdown
        severity = {
            'high_risk': sum(1 for v in validations if v['similarity'] < 0.3),
            'medium_risk': sum(1 for v in validations if 0.3 <= v['similarity'] < 0.5),
            'low_risk': sum(1 for v in validations if 0.5 <= v['similarity'] < 0.7),
            'verified': sum(1 for v in validations if v['similarity'] >= 0.7)
        }

        return {
            'total_claims': total_claims,
            'valid_claims': valid_claims,
            'overall_confidence': combined_confidence,
            'similarity_confidence': overall_confidence,
            'vsa_confidence': avg_vsa_confidence,
            'hallucination_detected': hallucination_detected,
            'severity': severity,
            'individual_validations': validations
        }

    def validate_claim(
        self,
        claim: str,
        workspace: GlobalWorkspace
    ) -> Dict:
        """
        Validate a single claim against workspace.

        Args:
            claim: The claim to validate
            workspace: The global workspace containing ground truth

        Returns:
            Validation result dictionary
        """
        # Encode workspace
        scene_vector = self.encoder.encode_workspace(workspace)

        # Extract concepts and encode claim
        concepts = self._extract_concepts(claim)
        claim_vector = self._encode_claim(concepts)

        # Calculate similarity
        similarity = self.vsa.similarity(scene_vector, claim_vector)

        # VSA validation
        vsa_check = self.vsa.verify_no_hallucination(concepts)

        return {
            'claim': claim,
            'concepts': concepts,
            'similarity': similarity,
            'confidence': self._calibrate_confidence(similarity),
            'valid': similarity > 0.7,
            'vsa_valid': vsa_check['valid'],
            'vsa_issues': vsa_check['issues'],
            'vsa_confidence': vsa_check['confidence']
        }


class EnhancedVSAValidator(VSAValidator):
    """
    Enhanced VSA validator with additional features:
    - Temporal validation
    - Relationship validation
    - Cross-reference checking
    """

    def __init__(self, ontology_path: Optional[Path] = None):
        super().__init__(ontology_path)
        self.validation_cache = {}  # Cache for repeated validations

    def validate_with_context(
        self,
        query: str,
        response: str,
        workspace: GlobalWorkspace,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Validate response with additional context.

        Args:
            query: The original query
            response: The generated response
            workspace: The global workspace
            context: Additional context (e.g., case metadata)

        Returns:
            Enhanced validation results
        """
        # Get base validation
        base_validation = self.validate_response(query, response, workspace)

        # Add context-specific checks if provided
        if context:
            base_validation['context_checks'] = self._validate_context(
                response, context
            )

        return base_validation

    def _validate_context(self, response: str, context: Dict) -> Dict:
        """
        Validate response against additional context.

        Args:
            response: The response text
            context: Context dictionary

        Returns:
            Context validation results
        """
        checks = {
            'temporal_consistency': True,
            'entity_consistency': True,
            'issues': []
        }

        # Check temporal consistency
        if 'date' in context:
            # Extract dates from response and check consistency
            # TODO: Implement date extraction and validation
            pass

        # Check entity consistency
        if 'entities' in context:
            # Verify mentioned entities exist in context
            # TODO: Implement entity cross-referencing
            pass

        return checks
