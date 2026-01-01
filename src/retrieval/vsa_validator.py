"""
VSA Anti-Hallucination Validator
=================================

Validates retrieval results against VSA ontology with confidence scoring.
Implements the anti-hallucination layer for the retrieval pipeline.

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
Phase 6: Integration with Retrieval Pipeline
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

import torch

from src.logic.gsw_schema import GlobalWorkspace
from src.vsa.encoder import GSWVSAEncoder
from src.vsa.legal_vsa import get_vsa_service
from src.vsa.ontology import CONCEPTS, RELATIONSHIPS, ROLES

logger = logging.getLogger(__name__)


class VSAValidator:
    """
    Validates retrieval results against VSA ontology.

    This class implements the anti-hallucination layer by:
    1. Extracting factual claims from responses
    2. Encoding claims and workspace context as hypervectors
    3. Calculating similarity scores to detect hallucinations
    4. Providing calibrated confidence scores
    """

    def __init__(self, ontology_path: Path | None = None):
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

    def load_ontology(self, ontology_path: Path) -> None:
        """
        Load additional ontology rules from external JSON file.

        The ontology file should be a JSON with the following structure:
        {
            "concepts": ["CONCEPT1", "CONCEPT2", ...],
            "roles": ["ROLE1", "ROLE2", ...],
            "relationships": ["REL1", "REL2", ...],
            "logic_rules": [
                ["SUBJECT", "RELATION", "OBJECT"],
                ...
            ]
        }

        Args:
            ontology_path: Path to ontology JSON file
        """
        try:
            with open(ontology_path, encoding="utf-8") as f:
                ontology_data = json.load(f)

            # Load additional concepts into VSA vocabulary
            if "concepts" in ontology_data:
                for concept in ontology_data["concepts"]:
                    # Register concept in VSA if not already present
                    if concept.upper() not in self._get_known_concepts():
                        self.vsa.get_vector(concept.upper())
                logger.info(f"Loaded {len(ontology_data['concepts'])} additional concepts")

            # Load additional roles
            if "roles" in ontology_data:
                for role in ontology_data["roles"]:
                    self.vsa.get_vector(role.upper())
                logger.info(f"Loaded {len(ontology_data['roles'])} additional roles")

            # Load additional relationships
            if "relationships" in ontology_data:
                for rel in ontology_data["relationships"]:
                    self.vsa.get_vector(rel.upper())
                logger.info(
                    f"Loaded {len(ontology_data['relationships'])} additional relationships"
                )

            # Store logic rules for validation
            if "logic_rules" in ontology_data:
                self._external_logic_rules = [tuple(rule) for rule in ontology_data["logic_rules"]]
                logger.info(f"Loaded {len(self._external_logic_rules)} additional logic rules")

            logger.info(f"Successfully loaded ontology from {ontology_path}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ontology file {ontology_path}: {e}")
            raise ValueError(f"Invalid JSON in ontology file: {e}")
        except OSError as e:
            logger.error(f"Failed to read ontology file {ontology_path}: {e}")
            raise

    def _get_known_concepts(self) -> set[str]:
        """Get set of known concepts from base ontology."""
        return set(CONCEPTS + ROLES + RELATIONSHIPS)

    def validate_response(self, query: str, response: str, workspace: GlobalWorkspace) -> dict:
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
                "total_claims": 0,
                "valid_claims": 0,
                "overall_confidence": 0.5,
                "hallucination_detected": False,
                "severity": {"high_risk": 0, "medium_risk": 0, "low_risk": 0, "verified": 0},
                "individual_validations": [],
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

            validations.append(
                {
                    "claim": claim,
                    "similarity": similarity,
                    "valid": similarity > 0.7,
                    "confidence": self._calibrate_confidence(similarity),
                    "vsa_valid": vsa_check["valid"],
                    "vsa_confidence": vsa_check["confidence"],
                    "concepts": claim_concepts,
                }
            )

        # Aggregate results
        return self._aggregate_validations(validations)

    def _extract_claims(self, response: str) -> list[str]:
        """
        Extract factual claims from response text.

        Args:
            response: The response text to analyze

        Returns:
            List of factual claim strings
        """
        claims = []

        # Split into sentences (handle multiple punctuation marks)
        sentences = re.split(r"[.!?]+", response)

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
        if sentence.endswith("?"):
            return False

        # Skip opinions (modal verbs indicating uncertainty)
        opinion_markers = [
            "may",
            "might",
            "could",
            "possibly",
            "perhaps",
            "probably",
            "maybe",
            "seems",
            "appears",
        ]
        sentence_lower = sentence.lower()

        # Check for opinion markers at word boundaries
        if any(re.search(r"\b" + marker + r"\b", sentence_lower) for marker in opinion_markers):
            return False

        # Has factual indicators (verbs of being, temporal markers, etc.)
        factual_markers = [
            "is",
            "was",
            "has",
            "had",
            "on",
            "in",
            "held",
            "ordered",
            "filed",
            "granted",
            "denied",
            "married",
            "divorced",
            "separated",
            "born",
            "dated",
        ]

        return any(re.search(r"\b" + marker + r"\b", sentence_lower) for marker in factual_markers)

    def _extract_concepts(self, claim: str) -> list[str]:
        """
        Extract key concepts from a claim.

        Args:
            claim: The claim text

        Returns:
            List of concept strings
        """
        # Simple extraction: get meaningful words
        # Remove common stop words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "was",
            "are",
            "were",
            "been",
            "be",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "should",
            "could",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
        }

        # Extract words (alphanumeric with potential hyphens)
        words = re.findall(r"\b[a-zA-Z][\w-]*\b", claim.lower())

        # Filter stop words and short words
        concepts = [w for w in words if w not in stop_words and len(w) > 2]

        return concepts

    def _encode_claim(self, concepts: list[str]) -> torch.Tensor:
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

    def _aggregate_validations(self, validations: list[dict]) -> dict:
        """
        Aggregate individual claim validations.

        Args:
            validations: List of validation dictionaries

        Returns:
            Aggregated validation results
        """
        total_claims = len(validations)
        valid_claims = sum(1 for v in validations if v["valid"])

        # Overall confidence is average of valid claims
        # If no valid claims, use average of all claims
        confidences = [v["confidence"] for v in validations if v["valid"]]
        if not confidences:
            confidences = [v["confidence"] for v in validations]

        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Factor in VSA validation results
        vsa_confidences = [v["vsa_confidence"] for v in validations]
        avg_vsa_confidence = sum(vsa_confidences) / len(vsa_confidences) if vsa_confidences else 0.0

        # Weighted combination of similarity-based and VSA-based confidence
        # VSA confidence (from ontology) gets 40% weight
        # Similarity confidence gets 60% weight
        combined_confidence = (overall_confidence * 0.6) + (avg_vsa_confidence * 0.4)

        # Flag hallucination if any claim has very low similarity
        hallucination_detected = any(v["similarity"] < 0.3 for v in validations)

        # Also flag if VSA detects issues
        vsa_issues_detected = any(not v["vsa_valid"] for v in validations)
        hallucination_detected = hallucination_detected or vsa_issues_detected

        # Severity breakdown
        severity = {
            "high_risk": sum(1 for v in validations if v["similarity"] < 0.3),
            "medium_risk": sum(1 for v in validations if 0.3 <= v["similarity"] < 0.5),
            "low_risk": sum(1 for v in validations if 0.5 <= v["similarity"] < 0.7),
            "verified": sum(1 for v in validations if v["similarity"] >= 0.7),
        }

        return {
            "total_claims": total_claims,
            "valid_claims": valid_claims,
            "overall_confidence": combined_confidence,
            "similarity_confidence": overall_confidence,
            "vsa_confidence": avg_vsa_confidence,
            "hallucination_detected": hallucination_detected,
            "severity": severity,
            "individual_validations": validations,
        }

    def validate_claim(self, claim: str, workspace: GlobalWorkspace) -> dict:
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
            "claim": claim,
            "concepts": concepts,
            "similarity": similarity,
            "confidence": self._calibrate_confidence(similarity),
            "valid": similarity > 0.7,
            "vsa_valid": vsa_check["valid"],
            "vsa_issues": vsa_check["issues"],
            "vsa_confidence": vsa_check["confidence"],
        }


class EnhancedVSAValidator(VSAValidator):
    """
    Enhanced VSA validator with additional features:
    - Temporal validation
    - Relationship validation
    - Cross-reference checking
    """

    def __init__(self, ontology_path: Path | None = None):
        super().__init__(ontology_path)
        self.validation_cache = {}  # Cache for repeated validations

    def validate_with_context(
        self, query: str, response: str, workspace: GlobalWorkspace, context: dict | None = None
    ) -> dict:
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
            base_validation["context_checks"] = self._validate_context(response, context)

        return base_validation

    def _validate_context(self, response: str, context: dict) -> dict:
        """
        Validate response against additional context.

        Args:
            response: The response text
            context: Context dictionary with optional keys:
                - 'date': Reference date for temporal validation
                - 'date_range': Tuple of (start_date, end_date) for range checks
                - 'entities': List of known entity names
                - 'case_parties': List of party names in the case

        Returns:
            Context validation results with:
                - temporal_consistency: bool
                - entity_consistency: bool
                - issues: List of identified issues
        """
        checks = {"temporal_consistency": True, "entity_consistency": True, "issues": []}

        # Check temporal consistency
        if "date" in context or "date_range" in context:
            temporal_result = self._validate_temporal_consistency(response, context)
            checks["temporal_consistency"] = temporal_result["consistent"]
            checks["issues"].extend(temporal_result["issues"])

        # Check entity consistency
        if "entities" in context or "case_parties" in context:
            entity_result = self._validate_entity_consistency(response, context)
            checks["entity_consistency"] = entity_result["consistent"]
            checks["issues"].extend(entity_result["issues"])

        return checks

    def _extract_dates_from_text(self, text: str) -> list[tuple[str, datetime]]:
        """
        Extract dates from text with their string representation.

        Args:
            text: Text to extract dates from

        Returns:
            List of (date_string, datetime) tuples
        """
        extracted_dates = []

        # Common date patterns
        patterns = [
            # ISO format: 2024-01-15
            (r"\b(\d{4}-\d{1,2}-\d{1,2})\b", "%Y-%m-%d"),
            # Australian format: 15/01/2024 or 15-01-2024
            (r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b", None),  # Multiple formats
            # Written format: 15 January 2024
            (
                r"\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b",
                "%d %B %Y",
            ),
            # Written format: January 15, 2024
            (
                r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b",
                None,
            ),
            # Year only: 2024
            (r"\b((?:19|20)\d{2})\b(?!\s*-)", "%Y"),
        ]

        for pattern, date_format in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1)
                parsed_date = self._parse_date(date_str, date_format)
                if parsed_date:
                    extracted_dates.append((date_str, parsed_date))

        return extracted_dates

    def _parse_date(self, date_str: str, preferred_format: str | None = None) -> datetime | None:
        """
        Parse a date string into a datetime object.

        Args:
            date_str: The date string to parse
            preferred_format: Preferred strptime format

        Returns:
            Parsed datetime or None if parsing fails
        """
        formats_to_try = []

        if preferred_format:
            formats_to_try.append(preferred_format)

        # Add common formats
        formats_to_try.extend(
            [
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%m/%d/%Y",
                "%d %B %Y",
                "%B %d, %Y",
                "%B %d %Y",
                "%Y",
            ]
        )

        for fmt in formats_to_try:
            try:
                return datetime.strptime(date_str.strip().replace(",", ""), fmt)
            except ValueError:
                continue

        return None

    def _validate_temporal_consistency(self, response: str, context: dict) -> dict:
        """
        Validate temporal consistency of response against context.

        Args:
            response: The response text
            context: Context with 'date' or 'date_range'

        Returns:
            Dictionary with 'consistent' bool and 'issues' list
        """
        result = {"consistent": True, "issues": []}

        # Extract dates from response
        extracted_dates = self._extract_dates_from_text(response)

        if not extracted_dates:
            # No dates to validate
            return result

        # Get reference date(s) from context
        reference_date = None
        date_range = None

        if "date" in context:
            ref = context["date"]
            if isinstance(ref, datetime):
                reference_date = ref
            elif isinstance(ref, str):
                reference_date = self._parse_date(ref)

        if "date_range" in context:
            range_tuple = context["date_range"]
            if len(range_tuple) == 2:
                start = (
                    range_tuple[0]
                    if isinstance(range_tuple[0], datetime)
                    else self._parse_date(str(range_tuple[0]))
                )
                end = (
                    range_tuple[1]
                    if isinstance(range_tuple[1], datetime)
                    else self._parse_date(str(range_tuple[1]))
                )
                if start and end:
                    date_range = (start, end)

        # Validate extracted dates
        for date_str, extracted_date in extracted_dates:
            # Check against reference date (if provided)
            if reference_date:
                # Allow some tolerance for year-only comparisons
                if extracted_date.year > datetime.now().year + 1:
                    result["consistent"] = False
                    result["issues"].append(
                        f"Future date detected: '{date_str}' is after current year"
                    )

            # Check against date range (if provided)
            if date_range:
                start_date, end_date = date_range
                # Only check if we have a full date (not just year)
                if extracted_date.month != 1 or extracted_date.day != 1:
                    if extracted_date < start_date or extracted_date > end_date:
                        result["consistent"] = False
                        result["issues"].append(
                            f"Date '{date_str}' outside expected range "
                            f"({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
                        )

            # Check for impossible dates (before relevant legal system)
            if extracted_date.year < 1901:  # Pre-Federation Australia
                result["consistent"] = False
                result["issues"].append(
                    f"Unlikely historical date: '{date_str}' predates Australian Federation"
                )

        return result

    def _validate_entity_consistency(self, response: str, context: dict) -> dict:
        """
        Validate entity consistency - check that mentioned entities exist in context.

        Args:
            response: The response text
            context: Context with 'entities' or 'case_parties'

        Returns:
            Dictionary with 'consistent' bool and 'issues' list
        """
        result = {"consistent": True, "issues": []}

        # Gather known entities from context
        known_entities: set[str] = set()

        if "entities" in context:
            for entity in context["entities"]:
                if isinstance(entity, str):
                    known_entities.add(entity.lower())
                elif isinstance(entity, dict) and "name" in entity:
                    known_entities.add(entity["name"].lower())

        if "case_parties" in context:
            for party in context["case_parties"]:
                if isinstance(party, str):
                    known_entities.add(party.lower())

        if not known_entities:
            # No entities to cross-reference
            return result

        # Extract potential entity mentions from response
        # Look for capitalized words/phrases that might be names
        potential_entities = self._extract_entity_mentions(response)

        # Check for entities mentioned in response but not in context
        # This could indicate hallucinated entities
        unrecognized_entities = []
        for entity in potential_entities:
            entity_lower = entity.lower()
            # Check if entity matches any known entity (partial match)
            if not any(known in entity_lower or entity_lower in known for known in known_entities):
                # Additional check: skip common legal terms that look like names
                legal_terms = {
                    "court",
                    "judge",
                    "applicant",
                    "respondent",
                    "child",
                    "property",
                    "order",
                    "act",
                    "section",
                    "family",
                    "parenting",
                    "consent",
                    "hearing",
                    "trial",
                }
                if entity_lower not in legal_terms:
                    unrecognized_entities.append(entity)

        # Flag if we find potential hallucinated entities
        if unrecognized_entities:
            # Only flag if there are multiple unrecognized entities
            # or if the entity appears to be a proper name
            significant_unrecognized = [
                e for e in unrecognized_entities if len(e.split()) >= 2 or e[0].isupper()
            ]

            if len(significant_unrecognized) >= 2:
                result["consistent"] = False
                result["issues"].append(
                    f"Potentially unrecognized entities mentioned: "
                    f"{', '.join(significant_unrecognized[:5])}"
                )

        return result

    def _extract_entity_mentions(self, text: str) -> list[str]:
        """
        Extract potential entity mentions from text.

        Args:
            text: Text to extract entities from

        Returns:
            List of potential entity strings
        """
        entities = []

        # Pattern for proper nouns (capitalized words)
        # Match sequences of capitalized words
        pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b"
        matches = re.findall(pattern, text)

        # Filter out sentence starters and common terms
        for match in matches:
            # Skip if it's at the start of a sentence (preceded by . ! ? or start)
            # This is a simplified check
            if len(match) > 2:
                entities.append(match)

        return list(set(entities))
