# API Reference

## Overview

This reference documents the Python API for the Australian Legal Corpus Classification System, including dataclasses, classifiers, and utility functions.

---

## Table of Contents

- [Data Classes](#data-classes)
  - [MultiDomainClassification](#multidomainclassification)
  - [BoostBreakdown](#boostbreakdown)
  - [CourtInfo](#courtinfo)
  - [LegislationRef](#legislationref)
  - [CaseRef](#caseref)
- [Classifiers](#classifiers)
  - [EnhancedDomainClassifier](#enhanceddomainclassifier)
  - [DomainClassifier](#domainclassifier)
- [Utilities](#utilities)
  - [CitationExtractor](#citationextractor)
  - [Court Hierarchy Functions](#court-hierarchy-functions)
  - [Legislation Functions](#legislation-functions)
- [Enums](#enums)

---

## Data Classes

### MultiDomainClassification

**Module**: `src.ingestion.multi_domain_classifier`

Comprehensive classification result for a legal document with multi-domain attribution.

#### Definition

```python
@dataclass
class MultiDomainClassification:
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
    keyword_matches: int = 0
    classification_version: str = "2.0"
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | `str` | Unique identifier (usually citation) |
| `primary_domain` | `str` | Primary broad domain (e.g., "Family") |
| `primary_category` | `str` | Primary granular category (e.g., "Family_Property") |
| `primary_confidence` | `float` | Confidence score 0.0-1.0 |
| `secondary_domains` | `List[Tuple[str, str, float]]` | Secondary domains with (domain, category, confidence) |
| `document_type` | `DocumentType` | Type of document (case_law, legislation, etc.) |
| `citation_type` | `CitationType` | Citation format type |
| `legislation_refs` | `List[LegislationRef]` | Referenced legislation (max 10) |
| `case_refs` | `List[CaseRef]` | Referenced cases (max 10) |
| `court_info` | `Optional[CourtInfo]` | Court metadata if applicable |
| `authority_score` | `int` | Authority score 0-100 |
| `binding_status` | `BindingStatus` | Precedent binding status |
| `boost_breakdown` | `BoostBreakdown` | Detailed BOOST scoring |
| `keyword_matches` | `int` | Total keyword matches |
| `classification_version` | `str` | Version identifier |

#### Methods

```python
def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary for JSON serialization."""
```

#### Example

```python
classification = MultiDomainClassification(
    document_id="[2020] FamCA 123",
    primary_domain="Family",
    primary_category="Family_Property",
    primary_confidence=0.68,
    secondary_domains=[
        ("Equity", "Equity_Trusts", 0.18),
        ("Property", "Prop_Real", 0.12)
    ],
    document_type=DocumentType.CASE_LAW,
    authority_score=75,
    boost_breakdown=BoostBreakdown(
        citation_match=10,
        jurisdiction_alignment=20,
        court_domain_hint=25
    )
)

# Serialize to JSON
result_dict = classification.to_dict()
```

---

### BoostBreakdown

**Module**: `src.ingestion.multi_domain_classifier`

Detailed breakdown of the 10-factor BOOST scoring.

#### Definition

```python
@dataclass
class BoostBreakdown:
    citation_match: int = 0              # BOOST 1
    jurisdiction_alignment: int = 0      # BOOST 2
    court_domain_hint: int = 0           # BOOST 3
    legislation_reference: int = 0       # BOOST 4
    case_law_reference: int = 0          # BOOST 5
    case_title_pattern: int = 0          # BOOST 6
    multi_domain_confidence: int = 0     # BOOST 7
    legislation_status: int = 0          # BOOST 8
    common_statute_distinction: int = 0  # BOOST 9
    document_type_weight: int = 0        # BOOST 10
```

#### Properties

```python
@property
def total(self) -> int:
    """Calculate total BOOST score."""
    return sum of all boost factors
```

#### Methods

```python
def to_dict(self) -> Dict[str, int]:
    """Convert to dictionary including total."""
```

#### Example

```python
boost = BoostBreakdown(
    citation_match=10,
    jurisdiction_alignment=20,
    court_domain_hint=25,
    legislation_reference=15
)

print(boost.total)  # 70
```

---

### CourtInfo

**Module**: `src.ingestion.multi_domain_classifier`

Court metadata extracted from citation.

#### Definition

```python
@dataclass
class CourtInfo:
    code: str
    name: str
    level: str
    jurisdiction: str
    authority_score: int
    domain_hint: Optional[str] = None
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Court code (e.g., "HCA", "FamCA") |
| `name` | `str` | Full court name |
| `level` | `str` | Hierarchy level (apex, superior_appellate, etc.) |
| `jurisdiction` | `str` | Jurisdiction (Commonwealth, NSW, etc.) |
| `authority_score` | `int` | Authority score 0-100 |
| `domain_hint` | `Optional[str]` | Domain hint for specialist courts |

#### Example

```python
court_info = CourtInfo(
    code="FamCA",
    name="Family Court of Australia",
    level="superior_trial",
    jurisdiction="Commonwealth",
    authority_score=75,
    domain_hint="Family"
)
```

---

### LegislationRef

**Module**: `src.ingestion.multi_domain_classifier`

Extracted legislation reference with section information.

#### Definition

```python
@dataclass
class LegislationRef:
    name: str
    year: Optional[int] = None
    jurisdiction: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    is_current: bool = True
    domain_hint: Optional[str] = None
```

#### Example

```python
leg_ref = LegislationRef(
    name="Family Law Act",
    year=1975,
    jurisdiction="Cth",
    section="s 79",
    domain_hint="Family"
)
```

---

### CaseRef

**Module**: `src.ingestion.multi_domain_classifier`

Extracted case law reference.

#### Definition

```python
@dataclass
class CaseRef:
    name: str
    citation: str
    year: Optional[int] = None
    court: Optional[str] = None
    is_landmark: bool = False
    domain_hint: Optional[str] = None
```

#### Example

```python
case_ref = CaseRef(
    name="Mabo v Queensland (No 2)",
    citation="(1992) 175 CLR 1",
    year=1992,
    court="HCA",
    is_landmark=True,
    domain_hint="Property"
)
```

---

## Classifiers

### EnhancedDomainClassifier

**Module**: `src.ingestion.multi_domain_classifier`

Enhanced multi-domain classifier with 10-factor BOOST scoring.

#### Initialization

```python
class EnhancedDomainClassifier:
    def __init__(self):
        """
        Initialize classifier with:
        - 16,495 keyword patterns
        - 500+ legislation mappings
        - 150+ landmark cases
        - 80 court codes
        """
```

#### Main Method

```python
def classify(self, doc: Dict[str, Any]) -> MultiDomainClassification:
    """
    Classify a document with enhanced multi-domain attribution.

    Args:
        doc: Document dictionary with keys:
            - 'id' or 'citation': Document identifier
            - 'text': Full document text
            - 'citation': Document citation
            - 'type': Document type string
            - 'jurisdiction': Jurisdiction (optional)

    Returns:
        MultiDomainClassification with full attribution
    """
```

#### Example Usage

```python
from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier

classifier = EnhancedDomainClassifier()

doc = {
    "citation": "Smith v Jones [2020] FamCA 123",
    "text": "The applicant seeks property orders under s 79...",
    "type": "case_law",
    "jurisdiction": "family court"
}

result = classifier.classify(doc)

print(f"Domain: {result.primary_domain}")
print(f"Category: {result.primary_category}")
print(f"Confidence: {result.primary_confidence:.2%}")
print(f"Authority: {result.authority_score}")
```

#### Private Methods

```python
def _detect_document_type(self, type_str: str) -> DocumentType:
    """Detect document type from type string."""

def _extract_court_info(self, citation: str) -> Optional[CourtInfo]:
    """Extract court information from citation."""

def _extract_legislation_refs(self, text: str) -> List[LegislationRef]:
    """Extract legislation references from text."""

def _extract_case_refs(self, text: str) -> List[CaseRef]:
    """Extract case law references from text."""

def _calculate_jurisdiction_boost(
    self, category: str, jurisdiction: str, search_text: str
) -> int:
    """Calculate BOOST 2: Jurisdiction alignment."""

def _calculate_title_pattern_boost(
    self, citation_lower: str, scores: Dict[str, int]
) -> int:
    """Calculate BOOST 6: Case title patterns."""

def _calculate_document_type_boost(self, doc_type: DocumentType) -> int:
    """Calculate BOOST 10: Document type weighting."""

def _is_common_law_decision(
    self, text: str, court_info: Optional[CourtInfo]
) -> bool:
    """Determine if this is a common law decision."""

def _determine_binding_status(
    self, court_info: Optional[CourtInfo]
) -> BindingStatus:
    """Determine binding precedent status."""
```

---

### DomainClassifier

**Module**: `src.ingestion.corpus_domain_extractor`

Basic classifier used for streaming corpus extraction.

#### Initialization

```python
class DomainClassifier:
    def __init__(self):
        """Initialize with pre-compiled keyword patterns."""
```

#### Main Method

```python
def classify(
    self, doc: Dict[str, Any]
) -> Tuple[str, str, List[Tuple[str, int]], Dict]:
    """
    Classify a document into domains.

    Returns:
        (primary_domain, primary_category, all_matches, enhanced_metadata)

        - primary_domain: Main domain classification
        - primary_category: Specific subcategory
        - all_matches: [(category, score), ...] sorted by score
        - enhanced_metadata: {
            'legislation_refs': List[str],
            'case_refs': List[str],
            'court': str,
            'court_level': str,
            'authority_score': int,
            'domain_hint': str (if specialist court)
          }
    """
```

#### Example Usage

```python
from src.ingestion.corpus_domain_extractor import DomainClassifier

classifier = DomainClassifier()

doc = {
    "citation": "[2020] HCA 15",
    "text": "The High Court considered...",
    "type": "decision"
}

domain, category, matches, metadata = classifier.classify(doc)

print(f"Domain: {domain}")
print(f"Category: {category}")
print(f"Top 3 matches: {matches[:3]}")
print(f"Court: {metadata['court']}")
print(f"Authority: {metadata['authority_score']}")
```

---

## Utilities

### CitationExtractor

**Module**: `src.ingestion.multi_domain_classifier`

Extract and parse legal citations from text.

#### Class Methods

```python
class CitationExtractor:

    @classmethod
    def extract_medium_neutral(cls, text: str) -> List[Dict]:
        """
        Extract medium neutral citations [YYYY] COURT NUM.

        Returns:
            List of dicts with keys: citation, year, court, number, type
        """

    @classmethod
    def extract_authorized_reports(cls, text: str) -> List[Dict]:
        """
        Extract authorized report citations (YYYY) VOL REPORT PAGE.

        Returns:
            List of dicts with keys: citation, year, volume, report, page, type
        """

    @classmethod
    def extract_legislation(cls, text: str) -> List[LegislationRef]:
        """
        Extract legislation references with section numbers.

        Returns:
            List of LegislationRef objects
        """

    @classmethod
    def detect_citation_type(cls, citation: str) -> CitationType:
        """
        Detect the type of citation format used.

        Returns:
            CitationType enum value
        """
```

#### Example Usage

```python
from src.ingestion.multi_domain_classifier import CitationExtractor

text = """
The decision in Smith v Jones [2020] HCA 15; (2020) 271 CLR 657
applied s 79 of the Family Law Act 1975 (Cth).
"""

# Extract medium neutral citations
mn_cites = CitationExtractor.extract_medium_neutral(text)
# [{'citation': '[2020] HCA 15', 'year': 2020, 'court': 'HCA', 'number': 15}]

# Extract authorized reports
reports = CitationExtractor.extract_authorized_reports(text)
# [{'citation': '(2020) 271 CLR 657', 'year': 2020, 'volume': 271, ...}]

# Extract legislation
legislation = CitationExtractor.extract_legislation(text)
# [LegislationRef(name='Family Law Act', year=1975, jurisdiction='Cth', section='s 79')]

# Detect citation type
cite_type = CitationExtractor.detect_citation_type("[2020] HCA 15")
# CitationType.MEDIUM_NEUTRAL
```

---

### Court Hierarchy Functions

**Module**: `src.ingestion.court_hierarchy`

#### Functions

```python
def get_court_info(court_code: str) -> Optional[Dict]:
    """
    Get court information by code (case-insensitive).

    Args:
        court_code: Court abbreviation (e.g., "HCA", "FamCA")

    Returns:
        Dict with keys: name, level, jurisdiction, authority_score, binding, domain_hint
        or None if not found
    """

def get_hierarchy_level(court_code: str) -> int:
    """
    Get numeric hierarchy level for a court (1=highest, 10=lowest).

    Returns:
        1-10 ranking
    """

def get_authority_score(court_code: str) -> int:
    """
    Get authority score for a court (0-100).

    Returns:
        0-100 score
    """

def get_jurisdiction(court_code: str) -> Optional[str]:
    """Get jurisdiction for a court code."""

def get_domain_hint(court_code: str) -> Optional[str]:
    """
    Get domain hint for a specialist court.

    Returns:
        Domain name (e.g., "Family", "Employment") or None
    """

def extract_court_from_citation(citation: str) -> Optional[str]:
    """
    Extract court code from a medium neutral citation.

    Args:
        citation: Citation string (e.g., "[2020] HCA 15")

    Returns:
        Court code (e.g., "HCA") or None
    """

def is_binding_authority(citing_court: str, cited_court: str) -> bool:
    """
    Determine if a cited court's decision is binding on the citing court.

    Returns:
        True if cited_court binds citing_court
    """

def get_report_series_info(series_abbr: str) -> Optional[Dict]:
    """
    Get information about a report series.

    Args:
        series_abbr: Report abbreviation (e.g., "CLR", "FCR")

    Returns:
        Dict with keys: name, jurisdiction, court, authority_score
    """
```

#### Example Usage

```python
from src.ingestion.court_hierarchy import (
    get_court_info, get_authority_score, extract_court_from_citation,
    is_binding_authority
)

# Get court information
info = get_court_info("FamCA")
# {'name': 'Family Court of Australia', 'level': 'superior_trial', ...}

# Get authority score
score = get_authority_score("HCA")
# 100

# Extract court from citation
court = extract_court_from_citation("[2020] FamCA 123")
# "FamCA"

# Check binding authority
is_binding = is_binding_authority("NSWDC", "NSWCA")
# True (Court of Appeal binds District Court)
```

---

### Legislation Functions

**Module**: `src.ingestion.legislation_patterns`

#### Functions

```python
def extract_legislation_refs(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract legislation references from text.

    Returns:
        List of (act_name, section, domain) tuples
    """

def get_domain_for_legislation(act_name: str) -> Optional[str]:
    """
    Get the primary domain for a legislation name.

    Returns:
        Domain name or None
    """

def get_subcategories_for_section(act_name: str, section: str) -> List[str]:
    """
    Get subcategories for a specific section of an Act.

    Returns:
        List of subcategory names
    """
```

#### Example Usage

```python
from src.ingestion.legislation_patterns import (
    get_domain_for_legislation, get_subcategories_for_section
)

# Get domain for legislation
domain = get_domain_for_legislation("Family Law Act 1975")
# "Family"

# Get subcategories for section
subcats = get_subcategories_for_section("Family Law Act 1975", "s79")
# ["Family_Property"]
```

---

## Enums

### DocumentType

**Module**: `src.ingestion.multi_domain_classifier`

```python
class DocumentType(Enum):
    CASE_LAW = "case_law"
    PRIMARY_LEGISLATION = "primary_legislation"
    SECONDARY_LEGISLATION = "secondary_legislation"
    BILL = "bill"
    EXPLANATORY_MEMO = "explanatory_memo"
    TRIBUNAL_DECISION = "tribunal_decision"
    PRACTICE_NOTE = "practice_note"
    UNKNOWN = "unknown"
```

---

### CitationType

**Module**: `src.ingestion.multi_domain_classifier`

```python
class CitationType(Enum):
    MEDIUM_NEUTRAL = "medium_neutral"      # [2020] HCA 1
    AUTHORIZED_REPORT = "authorized_report"  # (2020) 271 CLR 657
    LEGISLATION = "legislation"            # Family Law Act 1975
    UNKNOWN = "unknown"
```

---

### BindingStatus

**Module**: `src.ingestion.multi_domain_classifier`

```python
class BindingStatus(Enum):
    BINDING = "binding"              # Binds the citing court
    PERSUASIVE = "persuasive"        # Persuasive authority
    NOT_BINDING = "not_binding"      # No binding effect
    UNKNOWN = "unknown"
```

---

## Configuration Dictionaries

### CLASSIFICATION_MAP

**Module**: `src.ingestion.classification_config`

**Type**: `Dict[str, List[str]]`

Maps 103 categories to 16,495 keywords.

```python
CLASSIFICATION_MAP = {
    'Family_Property': [
        'property settlement',
        's 79',
        'contributions',
        'future needs',
        ...
    ],
    'Criminal_Violence': [
        'murder',
        'manslaughter',
        'assault',
        ...
    ],
    ...
}
```

---

### DOMAIN_MAPPING

**Module**: `src.ingestion.classification_config`

**Type**: `Dict[str, List[str]]`

Maps 22 broad domains to granular subcategories.

```python
DOMAIN_MAPPING = {
    'Family': [
        'Family_Parenting',
        'Family_Property',
        'Family_Child_Protection',
        'Family_Violence',
        'Family_General'
    ],
    'Criminal': [
        'Criminal_Violence',
        'Criminal_Sexual',
        'Criminal_Drugs',
        ...
    ],
    ...
}
```

---

### LEGISLATION_TO_DOMAIN

**Module**: `src.ingestion.legislation_patterns`

**Type**: `Dict[str, Dict]`

Maps 500+ Acts to domains and subcategories.

```python
LEGISLATION_TO_DOMAIN = {
    'Family Law Act 1975': {
        'domain': 'Family',
        'subcategories': ['Family_General', 'Family_Children', 'Family_Property'],
        'key_sections': {
            's79': 'Family_Property',
            's60B': 'Family_Children',
        }
    },
    ...
}
```

---

### COURT_CODES

**Module**: `src.ingestion.court_hierarchy`

**Type**: `Dict[str, Dict]`

Maps 80 court codes to metadata.

```python
COURT_CODES = {
    'HCA': {
        'name': 'High Court of Australia',
        'level': 'apex',
        'jurisdiction': 'Commonwealth',
        'binding': True,
        'authority_score': 100,
    },
    'FamCA': {
        'name': 'Family Court of Australia',
        'level': 'superior_trial',
        'jurisdiction': 'Commonwealth',
        'binding': 'family_matters',
        'authority_score': 75,
        'domain_hint': 'Family',
    },
    ...
}
```

---

## Complete Example

### End-to-End Classification

```python
from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier
import json

# Initialize classifier
classifier = EnhancedDomainClassifier()

# Sample document
doc = {
    "id": "example_001",
    "citation": "Smith v Jones [2020] FamCA 123",
    "text": """
    The applicant wife seeks property orders pursuant to s 79 of the
    Family Law Act 1975 (Cth). The parties were married for 15 years
    and have two children. The asset pool totals $2.5 million,
    comprising the family home, investment properties, and superannuation.

    The wife made significant contributions as homemaker and parent.
    The husband was the primary income earner. The Court must assess
    contributions pursuant to s 79(4) and consider future needs under
    s 75(2).
    """,
    "type": "decision",
    "jurisdiction": "family court",
    "date": "2020-06-15"
}

# Classify
result = classifier.classify(doc)

# Output results
print("=" * 60)
print(f"Document: {result.document_id}")
print(f"Primary Domain: {result.primary_domain}")
print(f"Primary Category: {result.primary_category}")
print(f"Confidence: {result.primary_confidence:.1%}")
print()

print("Secondary Domains:")
for domain, category, confidence in result.secondary_domains:
    print(f"  - {domain}: {category} ({confidence:.1%})")
print()

print(f"Court: {result.court_info.name if result.court_info else 'N/A'}")
print(f"Authority Score: {result.authority_score}")
print(f"Binding Status: {result.binding_status.value}")
print()

print("Legislation References:")
for ref in result.legislation_refs[:5]:
    section = f" {ref.section}" if ref.section else ""
    print(f"  - {ref.name}{section}")
print()

print("BOOST Breakdown:")
breakdown = result.boost_breakdown.to_dict()
for factor, score in breakdown.items():
    if score > 0 and factor != 'total':
        print(f"  {factor}: +{score}")
print(f"  Total BOOST: {breakdown['total']}")

# Serialize to JSON
output = result.to_dict()
print()
print("JSON Output:")
print(json.dumps(output, indent=2))
```

---

## Related Documentation

- [CLASSIFICATION_SYSTEM.md](CLASSIFICATION_SYSTEM.md) - Classification methodology
- [COURT_HIERARCHY.md](COURT_HIERARCHY.md) - Court codes reference
- [CITATION_FORMATS.md](CITATION_FORMATS.md) - Citation patterns
- [DOMAIN_TAXONOMY.md](DOMAIN_TAXONOMY.md) - Domain structure
