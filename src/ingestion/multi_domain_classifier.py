"""
Multi-Domain Legal Document Classifier

Enhanced classification system with:
- MultiDomainClassification structured output
- 10-factor BOOST scoring system
- Citation extraction pipeline
- Authority scoring with binding precedent logic

This module supersedes the basic DomainClassifier for production use.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class DocumentType(Enum):
    """Legal document types with classification priority."""
    CASE_LAW = "case_law"
    PRIMARY_LEGISLATION = "primary_legislation"
    SECONDARY_LEGISLATION = "secondary_legislation"
    BILL = "bill"
    EXPLANATORY_MEMO = "explanatory_memo"
    TRIBUNAL_DECISION = "tribunal_decision"
    PRACTICE_NOTE = "practice_note"
    UNKNOWN = "unknown"


class CitationType(Enum):
    """Citation format types."""
    MEDIUM_NEUTRAL = "medium_neutral"  # [2020] HCA 1
    AUTHORIZED_REPORT = "authorized_report"  # (2020) 271 CLR 657
    LEGISLATION = "legislation"  # Family Law Act 1975 (Cth)
    UNKNOWN = "unknown"


class BindingStatus(Enum):
    """Precedent binding status."""
    BINDING = "binding"
    PERSUASIVE = "persuasive"
    NOT_BINDING = "not_binding"
    UNKNOWN = "unknown"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class LegislationRef:
    """Extracted legislation reference."""
    name: str
    year: Optional[int] = None
    jurisdiction: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    is_current: bool = True
    domain_hint: Optional[str] = None


@dataclass
class CaseRef:
    """Extracted case law reference."""
    name: str
    citation: str
    year: Optional[int] = None
    court: Optional[str] = None
    is_landmark: bool = False
    domain_hint: Optional[str] = None


@dataclass
class CourtInfo:
    """Court metadata for a document."""
    code: str
    name: str
    level: str
    jurisdiction: str
    authority_score: int
    domain_hint: Optional[str] = None


@dataclass
class BoostBreakdown:
    """Detailed breakdown of BOOST scoring factors."""
    citation_match: int = 0  # BOOST 1
    jurisdiction_alignment: int = 0  # BOOST 2
    court_domain_hint: int = 0  # BOOST 3
    legislation_reference: int = 0  # BOOST 4
    case_law_reference: int = 0  # BOOST 5
    case_title_pattern: int = 0  # BOOST 6
    multi_domain_confidence: int = 0  # BOOST 7
    legislation_status: int = 0  # BOOST 8
    common_statute_distinction: int = 0  # BOOST 9
    document_type_weight: int = 0  # BOOST 10

    @property
    def total(self) -> int:
        """Calculate total BOOST score."""
        return (
            self.citation_match +
            self.jurisdiction_alignment +
            self.court_domain_hint +
            self.legislation_reference +
            self.case_law_reference +
            self.case_title_pattern +
            self.multi_domain_confidence +
            self.legislation_status +
            self.common_statute_distinction +
            self.document_type_weight
        )

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary for serialization."""
        return {
            'citation_match': self.citation_match,
            'jurisdiction_alignment': self.jurisdiction_alignment,
            'court_domain_hint': self.court_domain_hint,
            'legislation_reference': self.legislation_reference,
            'case_law_reference': self.case_law_reference,
            'case_title_pattern': self.case_title_pattern,
            'multi_domain_confidence': self.multi_domain_confidence,
            'legislation_status': self.legislation_status,
            'common_statute_distinction': self.common_statute_distinction,
            'document_type_weight': self.document_type_weight,
            'total': self.total,
        }


@dataclass
class MultiDomainClassification:
    """
    Comprehensive classification result for a legal document.

    This is the primary output structure for the enhanced classifier,
    providing detailed multi-domain attribution with confidence scores.
    """
    document_id: str
    primary_domain: str
    primary_category: str
    primary_confidence: float
    secondary_domains: List[Tuple[str, str, float]] = field(default_factory=list)
    document_type: DocumentType = DocumentType.UNKNOWN
    citation_type: CitationType = CitationType.UNKNOWN
    legislation_refs: List[LegislationRef] = field(default_factory=list)
    case_refs: List[CaseRef] = field(default_factory=list)
    court_info: Optional[CourtInfo] = None
    authority_score: int = 0
    binding_status: BindingStatus = BindingStatus.UNKNOWN
    boost_breakdown: BoostBreakdown = field(default_factory=BoostBreakdown)

    # Classification metadata
    keyword_matches: int = 0
    classification_version: str = "2.0"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'document_id': self.document_id,
            'primary_domain': self.primary_domain,
            'primary_category': self.primary_category,
            'primary_confidence': round(self.primary_confidence, 3),
            'secondary_domains': [
                {'domain': d, 'category': c, 'confidence': round(conf, 3)}
                for d, c, conf in self.secondary_domains
            ],
            'document_type': self.document_type.value,
            'citation_type': self.citation_type.value,
            'legislation_refs': [
                {
                    'name': ref.name,
                    'year': ref.year,
                    'jurisdiction': ref.jurisdiction,
                    'section': ref.section,
                    'is_current': ref.is_current,
                    'domain_hint': ref.domain_hint,
                }
                for ref in self.legislation_refs[:10]
            ],
            'case_refs': [
                {
                    'name': ref.name,
                    'citation': ref.citation,
                    'year': ref.year,
                    'court': ref.court,
                    'is_landmark': ref.is_landmark,
                    'domain_hint': ref.domain_hint,
                }
                for ref in self.case_refs[:10]
            ],
            'court_info': {
                'code': self.court_info.code,
                'name': self.court_info.name,
                'level': self.court_info.level,
                'jurisdiction': self.court_info.jurisdiction,
                'authority_score': self.court_info.authority_score,
                'domain_hint': self.court_info.domain_hint,
            } if self.court_info else None,
            'authority_score': self.authority_score,
            'binding_status': self.binding_status.value,
            'boost_breakdown': self.boost_breakdown.to_dict(),
            'keyword_matches': self.keyword_matches,
            'classification_version': self.classification_version,
        }


# ============================================================================
# CITATION EXTRACTION
# ============================================================================

class CitationExtractor:
    """Extract and parse legal citations from text."""

    # Medium Neutral: [2020] HCA 1
    MEDIUM_NEUTRAL_PATTERN = re.compile(
        r'\[(\d{4})\]\s*([A-Za-z]{2,10})\s*(\d+)',
        re.IGNORECASE
    )

    # Authorized Report: (2020) 271 CLR 657
    AUTHORIZED_REPORT_PATTERN = re.compile(
        r'\((\d{4})\)\s+(\d+)\s+([A-Z]{2,6})\s+(\d+)',
        re.IGNORECASE
    )

    # Legislation: Family Law Act 1975 (Cth) s 79
    LEGISLATION_PATTERN = re.compile(
        r'([A-Z][a-zA-Z\s]+(?:Act|Regulation|Rules?))\s+(\d{4})\s*\(([A-Za-z]{2,4})\)(?:\s+s\s*(\d+[a-zA-Z]*(?:\([a-z0-9]+\))?))?',
        re.IGNORECASE
    )

    # Section/Subsection: s 51(xxvi), reg 4.12
    SECTION_PATTERN = re.compile(
        r'(?:s|section|reg|regulation|r|rule)\s*(\d+[a-zA-Z]*(?:\([a-z0-9]+\))?(?:\.\d+)?)',
        re.IGNORECASE
    )

    @classmethod
    def extract_medium_neutral(cls, text: str) -> List[Dict]:
        """Extract medium neutral citations."""
        results = []
        for match in cls.MEDIUM_NEUTRAL_PATTERN.finditer(text):
            year, court, number = match.groups()
            results.append({
                'citation': match.group(0),
                'year': int(year),
                'court': court.upper(),
                'number': int(number),
                'type': CitationType.MEDIUM_NEUTRAL,
            })
        return results

    @classmethod
    def extract_authorized_reports(cls, text: str) -> List[Dict]:
        """Extract authorized report citations."""
        results = []
        for match in cls.AUTHORIZED_REPORT_PATTERN.finditer(text):
            year, volume, report, page = match.groups()
            results.append({
                'citation': match.group(0),
                'year': int(year),
                'volume': int(volume),
                'report': report.upper(),
                'page': int(page),
                'type': CitationType.AUTHORIZED_REPORT,
            })
        return results

    @classmethod
    def extract_legislation(cls, text: str) -> List[LegislationRef]:
        """Extract legislation references with section numbers."""
        results = []
        for match in cls.LEGISLATION_PATTERN.finditer(text):
            name, year, jurisdiction, section = match.groups()
            results.append(LegislationRef(
                name=name.strip(),
                year=int(year) if year else None,
                jurisdiction=jurisdiction.upper() if jurisdiction else None,
                section=section,
            ))
        return results

    @classmethod
    def detect_citation_type(cls, citation: str) -> CitationType:
        """Detect the type of citation format used."""
        if cls.MEDIUM_NEUTRAL_PATTERN.search(citation):
            return CitationType.MEDIUM_NEUTRAL
        if cls.AUTHORIZED_REPORT_PATTERN.search(citation):
            return CitationType.AUTHORIZED_REPORT
        if cls.LEGISLATION_PATTERN.search(citation):
            return CitationType.LEGISLATION
        return CitationType.UNKNOWN


# ============================================================================
# ENHANCED CLASSIFIER
# ============================================================================

class EnhancedDomainClassifier:
    """
    Enhanced multi-domain classifier with 10-factor BOOST scoring.

    This classifier provides:
    - Multi-dimensional domain attribution
    - Confidence-scored secondary domains
    - Detailed BOOST breakdown
    - Citation extraction and validation
    - Authority scoring with binding precedent logic
    """

    def __init__(self):
        # Import configuration lazily to avoid circular imports
        from src.ingestion.classification_config import CLASSIFICATION_MAP, DOMAIN_MAPPING
        from src.ingestion.legislation_patterns import LEGISLATION_TO_DOMAIN
        from src.ingestion.case_patterns import LANDMARK_CASES
        from src.ingestion.court_hierarchy import (
            COURT_CODES, get_court_info, get_domain_hint,
            extract_court_from_citation
        )

        self.classification_map = CLASSIFICATION_MAP
        self.domain_mapping = DOMAIN_MAPPING
        self.legislation_to_domain = LEGISLATION_TO_DOMAIN
        self.landmark_cases = LANDMARK_CASES
        self.court_codes = COURT_CODES
        self.get_court_info = get_court_info
        self.get_domain_hint = get_domain_hint
        self.extract_court_from_citation = extract_court_from_citation

        # Build reverse lookup: category -> domain
        self.category_to_domain: Dict[str, str] = {}
        for broad, granular_list in self.domain_mapping.items():
            for granular in granular_list:
                self.category_to_domain[granular] = broad

        # Pre-compile keyword patterns
        self.patterns: Dict[str, re.Pattern] = {}
        for category, keywords in self.classification_map.items():
            # Clean keywords - remove markdown artifacts
            clean_keywords = [self._clean_keyword(k) for k in keywords if k.strip()]
            clean_keywords = [k for k in clean_keywords if k]  # Remove empty
            if clean_keywords:
                pattern_str = "|".join([re.escape(k) for k in clean_keywords])
                self.patterns[category] = re.compile(pattern_str, re.IGNORECASE)

        # Pre-lowercase legislation and case names for fast matching
        self.legislation_names = {k.lower(): k for k in self.legislation_to_domain.keys()}
        self.case_names = {k.lower(): k for k in self.landmark_cases.keys()}

        logger.info(f"EnhancedDomainClassifier initialized with {len(self.patterns)} categories")

    def _clean_keyword(self, keyword: str) -> str:
        """Remove markdown artifacts from keywords."""
        if not keyword:
            return ""
        # Remove markdown bold/italic
        cleaned = re.sub(r'\*+', '', keyword)
        # Remove markdown headers
        cleaned = re.sub(r'^#+\s*', '', cleaned)
        # Remove code blocks
        cleaned = re.sub(r'```[a-z]*', '', cleaned)
        # Clean up whitespace
        cleaned = cleaned.strip()
        return cleaned

    def classify(self, doc: Dict[str, Any]) -> MultiDomainClassification:
        """
        Classify a document with enhanced multi-domain attribution.

        Args:
            doc: Document dictionary with 'text', 'citation', 'type', etc.

        Returns:
            MultiDomainClassification with full attribution details
        """
        doc_id = doc.get('id', doc.get('citation', 'unknown'))
        doc_type_str = doc.get('type', '')
        citation = doc.get('citation', '') or ''
        text = doc.get('text', '') or ''
        jurisdiction = (doc.get('jurisdiction', '') or '').lower()

        # Determine document type
        doc_type = self._detect_document_type(doc_type_str)

        # Initialize BOOST breakdown
        boost = BoostBreakdown()

        # Extract court information
        court_info = self._extract_court_info(citation)
        authority_score = court_info.authority_score if court_info else 0

        # Extract citations
        citation_type = CitationExtractor.detect_citation_type(citation)
        legislation_refs = self._extract_legislation_refs(f"{citation} {text[:5000]}")
        case_refs = self._extract_case_refs(f"{citation} {text[:5000]}")

        # Calculate base scores for each category
        search_text = f"{citation} {text[:15000]}".lower()
        citation_lower = citation.lower()

        scores: Dict[str, int] = {}

        for category, pattern in self.patterns.items():
            matches = pattern.findall(search_text)
            if not matches:
                continue

            base_score = len(matches)

            # BOOST 1: Citation match
            if pattern.search(citation_lower):
                base_score += 10
                boost.citation_match = max(boost.citation_match, 10)

            # BOOST 2: Jurisdiction alignment
            boost_2 = self._calculate_jurisdiction_boost(category, jurisdiction, search_text)
            base_score += boost_2
            boost.jurisdiction_alignment = max(boost.jurisdiction_alignment, boost_2)

            # BOOST 3: Court domain hint alignment
            if court_info and court_info.domain_hint:
                category_domain = self.category_to_domain.get(category, '')
                if court_info.domain_hint == category_domain:
                    base_score += 25
                    boost.court_domain_hint = 25

            scores[category] = base_score

        # BOOST 4: Legislation-based domain boost
        for leg_ref in legislation_refs:
            if leg_ref.name in self.legislation_to_domain:
                leg_info = self.legislation_to_domain[leg_ref.name]
                for subcat in leg_info.get('subcategories', []):
                    scores[subcat] = scores.get(subcat, 0) + 15
                boost.legislation_reference = max(boost.legislation_reference, 15)

        # BOOST 5: Case law-based domain boost
        for case_ref in case_refs:
            if case_ref.name in self.landmark_cases:
                case_info = self.landmark_cases[case_ref.name]
                for subcat in case_info.get('subcategories', []):
                    scores[subcat] = scores.get(subcat, 0) + 10
                boost.case_law_reference = max(boost.case_law_reference, 10)

        # BOOST 6: Case title patterns
        boost_6 = self._calculate_title_pattern_boost(citation_lower, scores)
        boost.case_title_pattern = boost_6

        # BOOST 7: Multi-domain confidence (boost when multiple strong signals)
        strong_domains = [cat for cat, score in scores.items() if score >= 20]
        if len(strong_domains) >= 2:
            for cat in strong_domains:
                scores[cat] += 5
            boost.multi_domain_confidence = 5

        # BOOST 8: Legislation status
        if doc_type in [DocumentType.PRIMARY_LEGISLATION, DocumentType.SECONDARY_LEGISLATION]:
            for cat in scores:
                scores[cat] += 10
            boost.legislation_status = 10

        # BOOST 9: Common law vs statute distinction
        if self._is_common_law_decision(text, court_info):
            for cat in scores:
                if 'Equity' in cat or 'Tort' in cat or 'Prop_' in cat:
                    scores[cat] += 5
            boost.common_statute_distinction = 5

        # BOOST 10: Document type weighting
        boost_10 = self._calculate_document_type_boost(doc_type)
        for cat in scores:
            scores[cat] += boost_10
        boost.document_type_weight = boost_10

        # Determine primary and secondary domains
        if not scores:
            primary_domain = "Unclassified"
            primary_category = "Unclassified"
            primary_confidence = 0.0
            secondary_domains = []
        else:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            total_score = sum(score for _, score in sorted_scores)

            best_category = sorted_scores[0][0]
            best_score = sorted_scores[0][1]
            primary_domain = self.category_to_domain.get(best_category, "Unclassified")
            primary_category = best_category
            primary_confidence = best_score / total_score if total_score > 0 else 0.0

            # Get secondary domains (different from primary, confidence > 0.1)
            secondary_domains = []
            for cat, score in sorted_scores[1:6]:
                domain = self.category_to_domain.get(cat, "Unclassified")
                conf = score / total_score if total_score > 0 else 0.0
                if domain != primary_domain and conf >= 0.1:
                    secondary_domains.append((domain, cat, conf))

        # Determine binding status
        binding_status = self._determine_binding_status(court_info)

        return MultiDomainClassification(
            document_id=doc_id,
            primary_domain=primary_domain,
            primary_category=primary_category,
            primary_confidence=primary_confidence,
            secondary_domains=secondary_domains,
            document_type=doc_type,
            citation_type=citation_type,
            legislation_refs=legislation_refs[:10],
            case_refs=case_refs[:10],
            court_info=court_info,
            authority_score=authority_score,
            binding_status=binding_status,
            boost_breakdown=boost,
            keyword_matches=sum(scores.values()),
        )

    def _detect_document_type(self, type_str: str) -> DocumentType:
        """Detect document type from type string."""
        type_lower = type_str.lower()
        if 'primary_legislation' in type_lower or type_lower == 'act':
            return DocumentType.PRIMARY_LEGISLATION
        if 'secondary_legislation' in type_lower or 'regulation' in type_lower:
            return DocumentType.SECONDARY_LEGISLATION
        if 'bill' in type_lower:
            return DocumentType.BILL
        if 'explanatory' in type_lower or 'memo' in type_lower:
            return DocumentType.EXPLANATORY_MEMO
        if 'tribunal' in type_lower:
            return DocumentType.TRIBUNAL_DECISION
        if 'case' in type_lower or 'decision' in type_lower:
            return DocumentType.CASE_LAW
        return DocumentType.UNKNOWN

    def _extract_court_info(self, citation: str) -> Optional[CourtInfo]:
        """Extract court information from citation."""
        court_code = self.extract_court_from_citation(citation)
        if not court_code:
            return None

        info = self.get_court_info(court_code)
        if not info:
            return None

        return CourtInfo(
            code=court_code,
            name=info.get('name', ''),
            level=info.get('level', ''),
            jurisdiction=info.get('jurisdiction', ''),
            authority_score=info.get('authority_score', 0),
            domain_hint=info.get('domain_hint'),
        )

    def _extract_legislation_refs(self, text: str) -> List[LegislationRef]:
        """Extract legislation references from text."""
        refs = []
        text_lower = text.lower()

        # Match known legislation
        for name_lower, name_original in self.legislation_names.items():
            if name_lower in text_lower:
                leg_info = self.legislation_to_domain.get(name_original, {})
                refs.append(LegislationRef(
                    name=name_original,
                    domain_hint=leg_info.get('domain'),
                ))

        # Also extract with regex for section numbers
        refs.extend(CitationExtractor.extract_legislation(text))

        return refs[:15]

    def _extract_case_refs(self, text: str) -> List[CaseRef]:
        """Extract case law references from text."""
        refs = []
        text_lower = text.lower()

        # Match landmark cases
        for name_lower, name_original in self.case_names.items():
            if name_lower in text_lower:
                case_info = self.landmark_cases.get(name_original, {})
                refs.append(CaseRef(
                    name=name_original,
                    citation=case_info.get('citation', ''),
                    is_landmark=True,
                    domain_hint=case_info.get('domain'),
                ))

        return refs[:15]

    def _calculate_jurisdiction_boost(
        self, category: str, jurisdiction: str, search_text: str
    ) -> int:
        """Calculate BOOST 2: Jurisdiction alignment."""
        boost = 0

        if "Family" in category:
            if "family" in jurisdiction or "family court" in search_text[:1000]:
                boost = 20

        if "Migration" in category or "Admin_Migration" in category:
            if "refugee" in search_text or "visa" in search_text or "migration" in jurisdiction:
                boost = 15

        if "Criminal" in category:
            if "criminal" in jurisdiction or "crime" in jurisdiction:
                boost = 15

        if "Employment" in category or "Emp_" in category:
            if "employment" in jurisdiction or "industrial" in jurisdiction or "fair work" in search_text:
                boost = 15

        return boost

    def _calculate_title_pattern_boost(
        self, citation_lower: str, scores: Dict[str, int]
    ) -> int:
        """Calculate BOOST 6: Case title patterns."""
        boost = 0

        # Criminal indicators
        if any(pattern in citation_lower for pattern in ["r v ", "regina v ", "dpp v ", "police v "]):
            scores["Criminal_General"] = scores.get("Criminal_General", 0) + 20
            boost = max(boost, 20)

        # Administrative/Migration indicators
        if "minister " in citation_lower:
            scores["Admin_Review"] = scores.get("Admin_Review", 0) + 15
            boost = max(boost, 15)
            if "immigration" in citation_lower:
                scores["Admin_Migration"] = scores.get("Admin_Migration", 0) + 20
                boost = max(boost, 20)

        # Competition/Consumer indicators
        if "accc " in citation_lower:
            scores["Competition_Cartels"] = scores.get("Competition_Cartels", 0) + 15
            scores["Comm_Consumer"] = scores.get("Comm_Consumer", 0) + 15
            boost = max(boost, 15)

        # Corporate indicators
        if "asic " in citation_lower:
            scores["Corp_Governance"] = scores.get("Corp_Governance", 0) + 15
            scores["Securities_Licensing"] = scores.get("Securities_Licensing", 0) + 15
            boost = max(boost, 15)

        # Tax indicators
        if "commissioner of taxation" in citation_lower or "fct v" in citation_lower:
            scores["Tax_Federal"] = scores.get("Tax_Federal", 0) + 20
            boost = max(boost, 20)

        return boost

    def _calculate_document_type_boost(self, doc_type: DocumentType) -> int:
        """Calculate BOOST 10: Document type weighting."""
        weights = {
            DocumentType.PRIMARY_LEGISLATION: 15,
            DocumentType.SECONDARY_LEGISLATION: 10,
            DocumentType.CASE_LAW: 10,
            DocumentType.TRIBUNAL_DECISION: 5,
            DocumentType.BILL: 3,
            DocumentType.EXPLANATORY_MEMO: 3,
            DocumentType.PRACTICE_NOTE: 2,
            DocumentType.UNKNOWN: 0,
        }
        return weights.get(doc_type, 0)

    def _is_common_law_decision(
        self, text: str, court_info: Optional[CourtInfo]
    ) -> bool:
        """Determine if this is a common law (vs statute-based) decision."""
        if not court_info:
            return False

        # Common law indicators
        common_law_markers = [
            "common law", "precedent", "stare decisis",
            "ratio decidendi", "obiter dicta",
        ]

        text_lower = text[:5000].lower()
        return any(marker in text_lower for marker in common_law_markers)

    def _determine_binding_status(
        self, court_info: Optional[CourtInfo]
    ) -> BindingStatus:
        """Determine binding precedent status."""
        if not court_info:
            return BindingStatus.UNKNOWN

        if court_info.code == "HCA":
            return BindingStatus.BINDING

        if court_info.level in ["apex", "superior_appellate"]:
            return BindingStatus.BINDING

        if court_info.level in ["superior_trial", "intermediate_appellate"]:
            return BindingStatus.PERSUASIVE

        return BindingStatus.NOT_BINDING
