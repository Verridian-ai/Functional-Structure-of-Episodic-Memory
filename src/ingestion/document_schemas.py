"""
Document Structure Schemas for Australian Legal Documents
==========================================================

This module defines Pydantic schemas for parsing and validating Australian legal documents.
These schemas align with the structures documented in docs/AUSTRALIAN_LEGAL_DOCUMENT_STRUCTURES.md

Usage:
    from src.ingestion.document_schemas import LegislationDocument, CaseLawDocument

    # Parse a judgment
    case = CaseLawDocument.from_raw_text(text)

    # Access structured components
    for para in case.judgment.paragraphs:
        print(f"[{para.number}] {para.text[:100]}")
"""

import re
from enum import Enum
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import date


# ============================================================================
# ENUMS - Document Classification
# ============================================================================

class Jurisdiction(str, Enum):
    """Australian jurisdictions."""
    COMMONWEALTH = "Cth"
    NSW = "NSW"
    VICTORIA = "VIC"
    QUEENSLAND = "QLD"
    WA = "WA"
    SA = "SA"
    TASMANIA = "TAS"
    ACT = "ACT"
    NT = "NT"


class DocumentType(str, Enum):
    """Types of legal documents."""
    LEGISLATION = "legislation"
    CASE_LAW = "case_law"
    REGULATION = "regulation"
    BILL = "bill"


class HeadingType(str, Enum):
    """Types of Part/Chapter headings."""
    PRELIMINARY = "preliminary"
    MISCELLANEOUS = "miscellaneous"
    GENERAL = "general"


class ScheduleType(str, Enum):
    """Types of schedules."""
    AMENDING = "amending"
    NON_AMENDING = "non_amending"
    FORM = "form"
    TABLE = "table"
    LIST = "list"
    TECHNICAL = "technical"
    OTHER = "other"


class JudgmentType(str, Enum):
    """Types of judicial opinions."""
    MAIN = "main"
    CONCURRING = "concurring"
    DISSENTING = "dissenting"


class SectionType(str, Enum):
    """Types of judgment sections."""
    INTRODUCTION = "introduction"
    FACTS = "facts"
    ISSUES = "issues"
    ANALYSIS = "analysis"
    CONCLUSION = "conclusion"


class CaseTreatment(str, Enum):
    """How a case was treated in judgment."""
    APPLIED = "applied"
    DISTINGUISHED = "distinguished"
    FOLLOWED = "followed"
    OVERRULED = "overruled"
    CONSIDERED = "considered"
    REFERRED_TO = "referred_to"


# ============================================================================
# COMMON COMPONENTS
# ============================================================================

class Subparagraph(BaseModel):
    """A subparagraph within a paragraph (e.g., (i), (ii))."""
    roman: str  # "(i)", "(ii)", "(iii)"
    text: str


class Paragraph(BaseModel):
    """A paragraph within a subsection (e.g., (a), (b))."""
    letter: str  # "(a)", "(b)", "(c)"
    text: str
    subparagraphs: List[Subparagraph] = Field(default_factory=list)


class Subsection(BaseModel):
    """A subsection within a section (e.g., (1), (2))."""
    number: str  # "(1)", "(2)", "(3)"
    text: str
    paragraphs: List[Paragraph] = Field(default_factory=list)


class Section(BaseModel):
    """A section in legislation or regulation."""
    number: str  # "79" or "79A"
    title: str
    text: str
    subsections: List[Subsection] = Field(default_factory=list)
    notes: Optional[str] = None
    examples: List[str] = Field(default_factory=list)


class Subdivision(BaseModel):
    """A subdivision within a division."""
    number: str
    title: str
    sections: List[Section] = Field(default_factory=list)


class Division(BaseModel):
    """A division within a part."""
    number: str
    title: str
    subdivisions: List[Subdivision] = Field(default_factory=list)
    sections: List[Section] = Field(default_factory=list)


class Part(BaseModel):
    """A part within legislation."""
    number: str
    title: str
    heading_type: Optional[HeadingType] = None
    divisions: List[Division] = Field(default_factory=list)
    sections: List[Section] = Field(default_factory=list)


class Chapter(BaseModel):
    """A chapter (highest level in large Acts)."""
    number: str
    title: str
    parts: List[Part] = Field(default_factory=list)


class Schedule(BaseModel):
    """A schedule at the end of legislation."""
    number: str  # Can be int or str (e.g., "1A")
    title: str
    short_title: Optional[str] = None
    schedule_type: ScheduleType
    contents: Dict[str, Any] = Field(default_factory=dict)


class DefinitionTerm(BaseModel):
    """A defined term."""
    term: str
    definition: str
    section: Optional[str] = None


# ============================================================================
# LEGISLATION SCHEMAS
# ============================================================================

class LegislationMetadata(BaseModel):
    """Metadata for legislation (Acts)."""
    long_title: str
    short_title: str
    citation: str  # "Family Law Act 1975 (Cth)"
    year: int
    jurisdiction: Jurisdiction
    act_number: Optional[str] = None
    assent_date: Optional[str] = None
    commencement_date: Optional[str] = None


class LegislationStructure(BaseModel):
    """The hierarchical structure of legislation."""
    chapters: List[Chapter] = Field(default_factory=list)
    parts: List[Part] = Field(default_factory=list)
    sections: List[Section] = Field(default_factory=list)


class LegislationDocument(BaseModel):
    """Complete legislation document schema."""
    document_type: Literal[DocumentType.LEGISLATION] = DocumentType.LEGISLATION
    metadata: LegislationMetadata
    preamble: Optional[str] = None
    structure: LegislationStructure
    schedules: List[Schedule] = Field(default_factory=list)
    definitions: Dict[str, DefinitionTerm] = Field(default_factory=dict)

    def get_section(self, number: str) -> Optional[Section]:
        """Retrieve a section by number."""
        # Search in top-level sections
        for section in self.structure.sections:
            if section.number == number:
                return section

        # Search in parts
        for part in self.structure.parts:
            for section in part.sections:
                if section.number == number:
                    return section
            for division in part.divisions:
                for section in division.sections:
                    if section.number == number:
                        return section

        # Search in chapters
        for chapter in self.structure.chapters:
            for part in chapter.parts:
                for section in part.sections:
                    if section.number == number:
                        return section

        return None


# ============================================================================
# CASE LAW SCHEMAS
# ============================================================================

class Judge(BaseModel):
    """A judge/judicial officer."""
    name: str
    role: str  # "CJ", "J", "JJ"
    judgment_type: JudgmentType = JudgmentType.MAIN


class Catchwords(BaseModel):
    """A sequence of catchwords."""
    sequence: int  # For multi-issue cases
    keywords: List[str]
    separator: str = "–"


class Headnote(BaseModel):
    """Case headnote/summary."""
    facts_summary: str
    issues: List[str] = Field(default_factory=list)
    held: str
    arguments: Optional[Dict[str, List[str]]] = None  # CLR only


class Appearances(BaseModel):
    """Counsel and solicitor appearances."""
    applicant: Dict[str, List[str]] = Field(
        default_factory=lambda: {"counsel": [], "solicitors": []}
    )
    respondent: Dict[str, List[str]] = Field(
        default_factory=lambda: {"counsel": [], "solicitors": []}
    )


class LegislationCited(BaseModel):
    """Legislation cited in judgment."""
    citation: str
    sections: List[str] = Field(default_factory=list)


class CaseCited(BaseModel):
    """Case cited in judgment."""
    citation: str
    treatment: Optional[CaseTreatment] = None


class JudgmentParagraph(BaseModel):
    """A numbered paragraph in the judgment."""
    number: int
    judge: Optional[str] = None  # For multi-judge decisions
    text: str
    heading: Optional[str] = None
    footnotes: List[str] = Field(default_factory=list)


class JudgmentSection(BaseModel):
    """A logical section of the judgment."""
    heading: str
    paragraph_range: tuple[int, int]  # (start, end)
    section_type: SectionType


class Judgment(BaseModel):
    """The judgment proper."""
    paragraphs: List[JudgmentParagraph] = Field(default_factory=list)
    sections: List[JudgmentSection] = Field(default_factory=list)


class Order(BaseModel):
    """A formal court order."""
    number: int
    text: str


class CaseLawMetadata(BaseModel):
    """Metadata for case law."""
    case_name: str
    medium_neutral_citation: str  # "[2020] HCA 35"
    court_identifier: str  # "HCA", "NSWSC", etc.
    judgment_number: int
    year: int
    court_name: str
    jurisdiction: Jurisdiction
    hearing_dates: List[str] = Field(default_factory=list)
    judgment_date: str
    judges: List[Judge] = Field(default_factory=list)


class CaseLawDocument(BaseModel):
    """Complete case law document schema."""
    document_type: Literal[DocumentType.CASE_LAW] = DocumentType.CASE_LAW
    metadata: CaseLawMetadata
    catchwords: List[Catchwords] = Field(default_factory=list)
    headnote: Optional[Headnote] = None
    appearances: Optional[Appearances] = None
    legislation_cited: List[LegislationCited] = Field(default_factory=list)
    cases_cited: List[CaseCited] = Field(default_factory=list)
    judgment: Judgment
    orders: List[Order] = Field(default_factory=list)

    def get_paragraph(self, number: int) -> Optional[JudgmentParagraph]:
        """Retrieve a paragraph by number."""
        for para in self.judgment.paragraphs:
            if para.number == number:
                return para
        return None

    def get_paragraphs_by_judge(self, judge_name: str) -> List[JudgmentParagraph]:
        """Get all paragraphs authored by a specific judge."""
        return [p for p in self.judgment.paragraphs if p.judge == judge_name]


# ============================================================================
# REGULATION SCHEMAS
# ============================================================================

class EnablingAct(BaseModel):
    """The Act that authorizes this regulation."""
    title: str
    section: Optional[str] = None  # Authority section


class RegulationMetadata(BaseModel):
    """Metadata for regulations."""
    title: str
    citation: str  # "Family Law Rules 2004 (Cth)"
    year: int
    jurisdiction: Jurisdiction
    regulation_number: Optional[str] = None
    enabling_act: EnablingAct
    commencement_date: Optional[str] = None


class Regulation(BaseModel):
    """A single regulation provision."""
    number: str  # "5", "5A"
    title: str
    text: str
    subregulations: List[Subsection] = Field(default_factory=list)


class RegulationPart(BaseModel):
    """A part within regulations."""
    number: str
    title: str
    divisions: List[Division] = Field(default_factory=list)
    regulations: List[Regulation] = Field(default_factory=list)


class RegulationStructure(BaseModel):
    """The structure of regulations."""
    parts: List[RegulationPart] = Field(default_factory=list)
    regulations: List[Regulation] = Field(default_factory=list)


class RegulationDocument(BaseModel):
    """Complete regulation document schema."""
    document_type: Literal[DocumentType.REGULATION] = DocumentType.REGULATION
    metadata: RegulationMetadata
    definitions: Dict[str, DefinitionTerm] = Field(default_factory=dict)
    structure: RegulationStructure
    schedules: List[Schedule] = Field(default_factory=list)


# ============================================================================
# BILL SCHEMAS
# ============================================================================

class ClauseNote(BaseModel):
    """Explanatory note for a Bill clause."""
    clause_number: str
    explanation: str
    intended_effect: str


class CompatibilityStatement(BaseModel):
    """Compatibility statements for Bill."""
    human_rights: Optional[str] = None
    constitutional: Optional[str] = None


class ExplanatoryMemorandum(BaseModel):
    """Explanatory Memorandum for a Bill."""
    available: bool
    overview: Optional[str] = None
    financial_impact: Optional[str] = None
    clause_notes: List[ClauseNote] = Field(default_factory=list)
    policy_objectives: List[str] = Field(default_factory=list)
    compatibility_statements: Optional[CompatibilityStatement] = None


class SecondReadingSpeech(BaseModel):
    """Second Reading Speech for a Bill."""
    available: bool
    speaker: Optional[str] = None
    date: Optional[str] = None
    hansard_reference: Optional[str] = None
    background: Optional[str] = None
    objectives: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    law_reform_references: List[str] = Field(default_factory=list)


class BillMetadata(BaseModel):
    """Metadata for Bills."""
    bill_title: str
    bill_number: str
    parliament: str
    session: str
    introduction_date: str
    jurisdiction: Jurisdiction
    stage: str  # "First Reading", "Second Reading", etc.


class BillDocument(BaseModel):
    """Complete Bill document schema."""
    document_type: Literal[DocumentType.BILL] = DocumentType.BILL
    metadata: BillMetadata
    bill_text: LegislationStructure  # Same as legislation
    explanatory_memorandum: Optional[ExplanatoryMemorandum] = None
    second_reading_speech: Optional[SecondReadingSpeech] = None


# ============================================================================
# REGEX PATTERNS FOR PARSING
# ============================================================================

class ParsingPatterns:
    """Compiled regex patterns for document parsing."""

    # Section references
    SECTION = re.compile(r"s(?:ection)?\s+(\d+[A-Z]*)")
    SUBSECTION = re.compile(r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)")
    PARAGRAPH = re.compile(r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)")
    SUBPARAGRAPH = re.compile(r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)\(([ivx]+)\)")

    # Structural references
    PART = re.compile(r"[Pp]art\s+([IVX\d]+[A-Z]*)")
    DIVISION = re.compile(r"[Dd]ivision\s+(\d+[A-Z]*)")
    SCHEDULE = re.compile(r"[Ss]chedule\s+(\d+)")
    CHAPTER = re.compile(r"[Cc]hapter\s+([IVX\d]+[A-Z]*)")

    # Regulation references
    REGULATION = re.compile(r"reg(?:ulation)?\s+(\d+[A-Z]*)")
    RULE = re.compile(r"r(?:ule)?\s+(\d+[A-Z]*\.\d+(?:\.\d+)?)")

    # Medium Neutral Citation
    MNC = re.compile(r"\[(\d{4})\]\s+([A-Z]+(?:Comm|FC|CA|SC|DC|LC)?)\s+(\d+)")
    PARAGRAPH_REF = re.compile(r"\[(\d+)\]")
    PARAGRAPH_RANGE = re.compile(r"\[(\d+)\]--\[(\d+)\]")

    # Case law components
    CATCHWORDS = re.compile(
        r"(?:CATCHWORDS?|Catchwords?)[:\s]*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\nLEGISLATION|\nCases)",
        re.IGNORECASE
    )
    COURT_CODE = re.compile(
        r"\[?\d{4}\]?\s*([A-Z]+(?:Comm|FC|CA|SC|DC|LC|CC|MC|CT|AT|PD|AP|CD|GD|OD)?)\s*\d+"
    )

    # Headings
    HEADING_ALL_CAPS = re.compile(r"^[A-Z\s]{5,}$")
    HEADING_TITLE_CASE = re.compile(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_court_code(citation: str) -> Optional[str]:
    """
    Extract court code from citation.

    Args:
        citation: Medium neutral citation

    Returns:
        Court code (e.g., "HCA", "NSWSC") or None

    Examples:
        >>> extract_court_code("[2020] HCA 35")
        'HCA'
        >>> extract_court_code("[2013] NSWSC 1668")
        'NSWSC'
    """
    match = ParsingPatterns.COURT_CODE.search(citation)
    return match.group(1) if match else None


def extract_year_from_mnc(citation: str) -> Optional[int]:
    """
    Extract year from medium neutral citation.

    Args:
        citation: Medium neutral citation

    Returns:
        Year as integer or None

    Examples:
        >>> extract_year_from_mnc("[2020] HCA 35")
        2020
    """
    match = ParsingPatterns.MNC.search(citation)
    return int(match.group(1)) if match else None


def parse_section_reference(ref: str) -> Dict[str, Optional[str]]:
    """
    Parse a section reference into components.

    Args:
        ref: Section reference string

    Returns:
        Dictionary with keys: section, subsection, paragraph, subparagraph

    Examples:
        >>> parse_section_reference("s 79(4)(a)")
        {'section': '79', 'subsection': '4', 'paragraph': 'a', 'subparagraph': None}
    """
    result = {
        "section": None,
        "subsection": None,
        "paragraph": None,
        "subparagraph": None
    }

    # Try most specific first
    match = ParsingPatterns.SUBPARAGRAPH.search(ref)
    if match:
        result["section"] = match.group(1)
        result["subsection"] = match.group(2)
        result["paragraph"] = match.group(3)
        result["subparagraph"] = match.group(4)
        return result

    match = ParsingPatterns.PARAGRAPH.search(ref)
    if match:
        result["section"] = match.group(1)
        result["subsection"] = match.group(2)
        result["paragraph"] = match.group(3)
        return result

    match = ParsingPatterns.SUBSECTION.search(ref)
    if match:
        result["section"] = match.group(1)
        result["subsection"] = match.group(2)
        return result

    match = ParsingPatterns.SECTION.search(ref)
    if match:
        result["section"] = match.group(1)
        return result

    return result


def is_heading(line: str) -> bool:
    """
    Determine if a line is likely a heading.

    Args:
        line: Text line to check

    Returns:
        True if line appears to be a heading
    """
    line = line.strip()
    if not line:
        return False

    # All caps headings (common in older documents)
    if ParsingPatterns.HEADING_ALL_CAPS.match(line):
        return True

    # Title case headings
    if ParsingPatterns.HEADING_TITLE_CASE.match(line):
        return True

    # Check for structural markers
    if any(line.startswith(marker) for marker in ["Part ", "Division ", "Chapter "]):
        return True

    return False


__all__ = [
    # Enums
    "Jurisdiction",
    "DocumentType",
    "HeadingType",
    "ScheduleType",
    "JudgmentType",
    "SectionType",
    "CaseTreatment",

    # Common components
    "Subparagraph",
    "Paragraph",
    "Subsection",
    "Section",
    "Subdivision",
    "Division",
    "Part",
    "Chapter",
    "Schedule",
    "DefinitionTerm",

    # Legislation
    "LegislationMetadata",
    "LegislationStructure",
    "LegislationDocument",

    # Case Law
    "Judge",
    "Catchwords",
    "Headnote",
    "Appearances",
    "LegislationCited",
    "CaseCited",
    "JudgmentParagraph",
    "JudgmentSection",
    "Judgment",
    "Order",
    "CaseLawMetadata",
    "CaseLawDocument",

    # Regulations
    "EnablingAct",
    "RegulationMetadata",
    "Regulation",
    "RegulationPart",
    "RegulationStructure",
    "RegulationDocument",

    # Bills
    "ClauseNote",
    "CompatibilityStatement",
    "ExplanatoryMemorandum",
    "SecondReadingSpeech",
    "BillMetadata",
    "BillDocument",

    # Utilities
    "ParsingPatterns",
    "extract_court_code",
    "extract_year_from_mnc",
    "parse_section_reference",
    "is_heading",
]
