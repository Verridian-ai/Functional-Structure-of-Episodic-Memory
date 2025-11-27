"""
Statutory RAG Validator
========================

Validates legal extractions against statutory corpus using RAG (Retrieval-Augmented Generation).
Ensures compliance with statutory requirements and identifies potential conflicts.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import re
from pathlib import Path

from .corpus_loader import CorpusLoader


@dataclass
class StatutoryReference:
    """
    Represents a reference to a statutory provision.

    Attributes:
        act_name: Name of the act (e.g., "Family Law Act 1975")
        section: Section number (e.g., "60CC")
        subsection: Optional subsection (e.g., "2")
        content: Text content of the provision
        url: URL to the legislation
    """
    act_name: str
    section: str
    subsection: Optional[str] = None
    content: str = ""
    url: str = ""

    def __str__(self) -> str:
        """String representation of the reference."""
        ref = f"{self.act_name} s{self.section}"
        if self.subsection:
            ref += f"({self.subsection})"
        return ref


@dataclass
class ValidationResult:
    """
    Results of statutory validation.

    Attributes:
        is_valid: Whether the extraction is valid
        compliance_score: Score from 0.0 to 1.0 indicating compliance level
        supporting_citations: List of statutory references that support the extraction
        conflicts: List of identified conflicts with statutory requirements
        recommendations: List of recommendations to improve compliance
    """
    is_valid: bool
    compliance_score: float
    supporting_citations: List[StatutoryReference] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        """String representation of validation results."""
        status = "VALID" if self.is_valid else "INVALID"
        return (
            f"Validation Result: {status}\n"
            f"Compliance Score: {self.compliance_score:.2f}\n"
            f"Supporting Citations: {len(self.supporting_citations)}\n"
            f"Conflicts: {len(self.conflicts)}\n"
            f"Recommendations: {len(self.recommendations)}"
        )


class StatutoryRAGValidator:
    """
    Validates legal extractions against statutory corpus using RAG.

    This validator retrieves relevant statutory provisions and checks whether
    extractions comply with legal requirements, identifying conflicts and
    providing recommendations.
    """

    def __init__(self, corpus_path: str = "data/statutory_corpus"):
        """
        Initialize the statutory RAG validator.

        Args:
            corpus_path: Path to the directory containing statutory JSON files
        """
        self.corpus_path = corpus_path
        self.corpus_loader: Optional[CorpusLoader] = None
        self.embeddings: Optional[Any] = None

        self._load_corpus(corpus_path)
        self._build_embeddings()

    def _load_corpus(self, path: str) -> Dict:
        """
        Load the statutory corpus from the specified path.

        Args:
            path: Path to the corpus directory

        Returns:
            Dictionary containing the loaded corpus
        """
        print(f"[StatutoryRAGValidator] Loading corpus from {path}")

        try:
            self.corpus_loader = CorpusLoader(path)

            if not self.corpus_loader.acts:
                print(f"[StatutoryRAGValidator] Warning: No acts loaded from {path}")
                return {}

            print(f"[StatutoryRAGValidator] Loaded {len(self.corpus_loader.acts)} acts")
            return dict(self.corpus_loader.acts)

        except Exception as e:
            print(f"[StatutoryRAGValidator] Error loading corpus: {e}")
            return {}

    def _build_embeddings(self) -> Any:
        """
        Build embeddings for the corpus for semantic search.

        Note: This is a placeholder for actual embedding generation.
        In a production system, this would use a model like sentence-transformers
        to create embeddings for semantic similarity search.

        Returns:
            Embeddings object (currently None)
        """
        print("[StatutoryRAGValidator] Building embeddings (placeholder)")

        # Placeholder: In production, this would:
        # 1. Load a sentence transformer model
        # 2. Generate embeddings for all sections
        # 3. Store in a vector database or FAISS index
        # 4. Enable semantic similarity search

        self.embeddings = None
        return self.embeddings

    def validate_extraction(self, extraction: dict, context: str = "") -> ValidationResult:
        """
        Validate a legal extraction against the statutory corpus.

        Args:
            extraction: Dictionary containing the extraction to validate
            context: Optional additional context

        Returns:
            ValidationResult with compliance score, citations, conflicts, and recommendations
        """
        print(f"[StatutoryRAGValidator] Validating extraction")

        if not self.corpus_loader or not self.corpus_loader.acts:
            print("[StatutoryRAGValidator] Warning: No corpus loaded, returning invalid result")
            return ValidationResult(
                is_valid=False,
                compliance_score=0.0,
                conflicts=["No statutory corpus loaded for validation"],
                recommendations=["Load statutory corpus before validation"]
            )

        # Extract claims from the extraction
        claims = self._extract_claims(extraction)

        if not claims:
            print("[StatutoryRAGValidator] No claims found in extraction")
            return ValidationResult(
                is_valid=False,
                compliance_score=0.0,
                conflicts=["No extractable claims found"],
                recommendations=["Ensure extraction contains analyzable legal claims"]
            )

        # Retrieve relevant statutes
        statutes = self._retrieve_statutes(claims)

        # Check compliance
        compliance_score = self._check_compliance(claims, statutes)

        # Detect conflicts
        conflicts = self._detect_conflicts(claims, statutes)

        # Generate recommendations
        recommendations = self._generate_recommendations(conflicts)

        # Convert statutes to StatutoryReference objects
        supporting_citations = []
        for statute in statutes:
            ref = StatutoryReference(
                act_name=statute.get('act_name', 'Unknown Act'),
                section=statute.get('section', 'Unknown'),
                subsection=statute.get('subsection'),
                content=statute.get('summary', statute.get('title', '')),
                url=statute.get('act_url', '')
            )
            supporting_citations.append(ref)

        # Determine validity
        is_valid = compliance_score >= 0.6 and len(conflicts) == 0

        result = ValidationResult(
            is_valid=is_valid,
            compliance_score=compliance_score,
            supporting_citations=supporting_citations,
            conflicts=conflicts,
            recommendations=recommendations
        )

        print(f"[StatutoryRAGValidator] Validation complete: {result.compliance_score:.2f}")
        return result

    def _extract_claims(self, extraction: dict) -> List[str]:
        """
        Extract verifiable claims from the extraction.

        Args:
            extraction: The extraction dictionary

        Returns:
            List of extracted claims
        """
        claims = []

        # Extract from common fields
        if isinstance(extraction, dict):
            # Check for text-based fields
            for field in ['text', 'content', 'summary', 'conclusion', 'finding']:
                if field in extraction and extraction[field]:
                    claims.append(str(extraction[field]))

            # Check for structured legal tests
            if 'legal_test' in extraction:
                claims.append(extraction['legal_test'])

            # Check for requirements
            if 'requirements' in extraction:
                if isinstance(extraction['requirements'], list):
                    claims.extend([str(req) for req in extraction['requirements']])
                else:
                    claims.append(str(extraction['requirements']))

            # Check for elements
            if 'elements' in extraction:
                if isinstance(extraction['elements'], list):
                    claims.extend([str(elem) for elem in extraction['elements']])
                elif isinstance(extraction['elements'], dict):
                    claims.extend([str(v) for v in extraction['elements'].values()])

            # Check for findings
            if 'findings' in extraction:
                if isinstance(extraction['findings'], list):
                    claims.extend([str(f) for f in extraction['findings']])

            # Extract nested claims recursively
            for key, value in extraction.items():
                if isinstance(value, dict) and key not in ['metadata', 'source']:
                    claims.extend(self._extract_claims(value))

        elif isinstance(extraction, list):
            for item in extraction:
                if isinstance(item, (dict, list)):
                    claims.extend(self._extract_claims(item))
                else:
                    claims.append(str(item))

        # Filter out empty claims and deduplicate
        claims = [c.strip() for c in claims if c and str(c).strip()]
        claims = list(dict.fromkeys(claims))  # Deduplicate while preserving order

        print(f"[StatutoryRAGValidator] Extracted {len(claims)} claims")
        return claims

    def _retrieve_statutes(self, claims: List[str]) -> List[Dict]:
        """
        Retrieve relevant statutes for the given claims.

        Args:
            claims: List of claims to find statutes for

        Returns:
            List of relevant statutory provisions
        """
        if not self.corpus_loader:
            return []

        all_statutes = []
        seen_sections = set()

        for claim in claims:
            # Search by text
            text_results = self.corpus_loader.search_by_text(claim, top_k=3)

            for result in text_results:
                section_key = (result.get('act_name'), result.get('section'))
                if section_key not in seen_sections:
                    all_statutes.append(result)
                    seen_sections.add(section_key)

            # Extract keywords and search
            keywords = self._extract_keywords(claim)
            for keyword in keywords[:3]:  # Limit to top 3 keywords
                keyword_results = self.corpus_loader.search_by_keyword(keyword, top_k=2)

                for result in keyword_results:
                    section_key = (result.get('act_name'), result.get('section'))
                    if section_key not in seen_sections:
                        all_statutes.append(result)
                        seen_sections.add(section_key)

        print(f"[StatutoryRAGValidator] Retrieved {len(all_statutes)} relevant statutes")
        return all_statutes[:10]  # Limit total results

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text for searching.

        Args:
            text: Text to extract keywords from

        Returns:
            List of keywords
        """
        # Simple keyword extraction based on word frequency and length
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

        # Remove common legal stop words
        stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'were',
                     'their', 'which', 'when', 'where', 'there', 'would', 'could',
                     'should', 'shall', 'will', 'must', 'such', 'each', 'upon'}

        keywords = [w for w in words if w not in stop_words]

        # Return unique keywords
        return list(dict.fromkeys(keywords))[:10]

    def _check_compliance(self, claims: List[str], statutes: List[Dict]) -> float:
        """
        Check compliance of claims against statutes.

        Args:
            claims: List of claims to check
            statutes: List of relevant statutes

        Returns:
            Compliance score between 0.0 and 1.0
        """
        if not statutes:
            print("[StatutoryRAGValidator] No statutes to check compliance against")
            return 0.0

        total_score = 0.0
        checked_claims = 0

        for claim in claims:
            claim_lower = claim.lower()
            claim_terms = set(re.findall(r'\w+', claim_lower))

            best_match_score = 0.0

            for statute in statutes:
                # Build statute text
                statute_text = ' '.join([
                    statute.get('title', ''),
                    statute.get('summary', ''),
                    statute.get('legal_test', ''),
                    ' '.join(statute.get('keywords', []))
                ]).lower()

                statute_terms = set(re.findall(r'\w+', statute_text))

                # Calculate term overlap
                if claim_terms and statute_terms:
                    overlap = len(claim_terms.intersection(statute_terms))
                    match_score = overlap / len(claim_terms)

                    # Check for required elements if present
                    if 'required_elements' in statute:
                        elements = statute['required_elements']
                        element_matches = 0

                        for element in elements:
                            element_keywords = element.get('keywords', [])
                            for keyword in element_keywords:
                                if keyword.lower() in claim_lower:
                                    element_matches += 1
                                    break

                        if elements:
                            element_score = element_matches / len(elements)
                            match_score = (match_score + element_score) / 2

                    best_match_score = max(best_match_score, match_score)

            total_score += best_match_score
            checked_claims += 1

        if checked_claims == 0:
            return 0.0

        compliance_score = total_score / checked_claims
        print(f"[StatutoryRAGValidator] Compliance score: {compliance_score:.2f}")

        return compliance_score

    def _detect_conflicts(self, claims: List[str], statutes: List[Dict]) -> List[str]:
        """
        Detect conflicts between claims and statutory requirements.

        Args:
            claims: List of claims to check
            statutes: List of relevant statutes

        Returns:
            List of detected conflicts
        """
        conflicts = []

        # Check for missing required elements
        for statute in statutes:
            if 'required_elements' in statute:
                elements = statute['required_elements']
                minimum_elements = statute.get('minimum_elements', len(elements))
                threshold = statute.get('threshold', 0.5)

                # Combine all claims for checking
                all_claims_text = ' '.join(claims).lower()

                found_elements = 0
                missing_elements = []

                for element in elements:
                    element_keywords = element.get('keywords', [])
                    element_found = False

                    for keyword in element_keywords:
                        if keyword.lower() in all_claims_text:
                            element_found = True
                            break

                    if element_found:
                        found_elements += 1
                    else:
                        missing_elements.append(element.get('element', 'Unknown element'))

                if found_elements < minimum_elements:
                    section_ref = f"{statute.get('act_name', 'Unknown')} s{statute.get('section', '?')}"
                    conflict = (
                        f"Insufficient elements for {section_ref} "
                        f"({statute.get('legal_test', 'test')}): "
                        f"found {found_elements}/{len(elements)}, "
                        f"minimum required: {minimum_elements}. "
                        f"Missing: {', '.join(missing_elements)}"
                    )
                    conflicts.append(conflict)

        # Check for contradictory statements
        negative_indicators = ['not', 'no', 'never', 'cannot', 'unable', 'fails', 'lacks']
        positive_indicators = ['must', 'shall', 'required', 'necessary', 'essential', 'needs']

        for statute in statutes:
            statute_summary = statute.get('summary', '').lower()

            for claim in claims:
                claim_lower = claim.lower()

                # Check if claim negates a requirement
                has_negative = any(neg in claim_lower for neg in negative_indicators)
                statute_has_positive = any(pos in statute_summary for pos in positive_indicators)

                if has_negative and statute_has_positive:
                    # Potential conflict - check for keyword overlap
                    claim_terms = set(re.findall(r'\w+', claim_lower))
                    statute_terms = set(re.findall(r'\w+', statute_summary))
                    overlap = len(claim_terms.intersection(statute_terms))

                    if overlap > 3:  # Significant overlap
                        section_ref = f"{statute.get('act_name', 'Unknown')} s{statute.get('section', '?')}"
                        conflict = (
                            f"Potential conflict with {section_ref}: "
                            f"claim appears to negate statutory requirement"
                        )
                        conflicts.append(conflict)

        print(f"[StatutoryRAGValidator] Detected {len(conflicts)} conflicts")
        return conflicts

    def _generate_recommendations(self, conflicts: List[str]) -> List[str]:
        """
        Generate recommendations based on detected conflicts.

        Args:
            conflicts: List of detected conflicts

        Returns:
            List of recommendations
        """
        recommendations = []

        if not conflicts:
            recommendations.append("Extraction appears compliant with statutory requirements")
            return recommendations

        for conflict in conflicts:
            # Parse conflict to generate specific recommendation
            if 'Insufficient elements' in conflict:
                # Extract missing elements
                if 'Missing:' in conflict:
                    missing = conflict.split('Missing:')[1].strip()
                    recommendation = (
                        f"Consider addressing the following elements: {missing}"
                    )
                    recommendations.append(recommendation)
                else:
                    recommendations.append("Ensure all required statutory elements are addressed")

            elif 'Potential conflict' in conflict:
                recommendations.append(
                    "Review extraction for potential contradictions with statutory requirements"
                )

            elif 'section' in conflict.lower():
                # Extract section reference
                section_match = re.search(r's(\w+)', conflict)
                if section_match:
                    section = section_match.group(1)
                    recommendation = (
                        f"Review compliance with section {section} requirements"
                    )
                    recommendations.append(recommendation)

        # Add general recommendations
        if len(conflicts) > 3:
            recommendations.append(
                "Multiple compliance issues detected - recommend comprehensive review against statutory framework"
            )

        recommendations.append("Verify all statutory references and ensure complete coverage of legal tests")

        print(f"[StatutoryRAGValidator] Generated {len(recommendations)} recommendations")
        return recommendations
