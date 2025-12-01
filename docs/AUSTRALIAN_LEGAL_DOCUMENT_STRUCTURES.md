# Australian Legal Document Structures
## Reference Guide for Anatomist Agent Document Parsing

This document provides comprehensive structural schemas for parsing Australian legal documents into their constituent components. These schemas enable the Anatomist Agent to identify, extract, and organize legal content hierarchically.

---

## Table of Contents

1. [Legislation (Acts)](#1-legislation-acts)
2. [Case Law (Judgments)](#2-case-law-judgments)
3. [Regulations (Subordinate Legislation)](#3-regulations-subordinate-legislation)
4. [Bills](#4-bills)
5. [Medium Neutral Citation Format](#5-medium-neutral-citation-format)
6. [Parsing Schema Structures](#6-parsing-schema-structures)

---

## 1. LEGISLATION (Acts)

### 1.1 Hierarchical Structure

Australian Acts follow a consistent hierarchical organization:

```
Act
├── Long Title
├── Short Title (Citation section)
├── Preamble (optional)
├── Chapters (optional, for larger Acts)
│   ├── Parts
│   │   ├── Divisions
│   │   │   ├── Subdivisions
│   │   │   │   ├── Sections
│   │   │   │   │   ├── Subsections
│   │   │   │   │   │   ├── Paragraphs
│   │   │   │   │   │   │   └── Subparagraphs
│   │   │   │   │   │   │       └── Items
└── Schedules
    ├── Amending Schedules
    └── Non-amending Schedules
```

### 1.2 Structural Components

#### 1.2.1 Preliminary Section
- **Location**: First Chapter/Part (typically headed "Preliminary")
- **Contents**:
  - Citation section (Short Title)
  - Commencement section
  - Definitions section
  - Objects of the Act (optional)

#### 1.2.2 Organizational Units
- **Chapters**: Highest level grouping (used in larger Acts)
  - Example: Criminal Code Act 1995 (Cth)
  - Constraint: Chapters may contain Parts that consist only of sections

- **Parts**: Major divisions of an Act
  - May exist independently or within Chapters
  - Typically headed with descriptive titles

- **Divisions**: Must occur within Parts
  - Cannot exist independently

- **Subdivisions**: Must occur within Divisions
  - Cannot exist independently

#### 1.2.3 Provision Units
- **Sections**: Primary unit of legislation
  - Numbered sequentially (1, 2, 3...)
  - May have inserted sections (5A between 5 and 6)

- **Subsections**: Subdivisions of sections
  - Referenced in parentheses: s 5(1), s 5(2)
  - No space between section and subsection number

- **Paragraphs**: Subdivisions of subsections
  - Typically lettered: (a), (b), (c)

- **Subparagraphs**: Further subdivisions
  - Typically numbered: (i), (ii), (iii)

- **Items**: Lowest level provisions
  - Used in schedules and complex provisions

#### 1.2.4 Miscellaneous Section
- **Location**: Last Chapter/Part (typically headed "Miscellaneous")
- **Contents**:
  - Regulation-making powers (Governor)
  - Other miscellaneous provisions

#### 1.2.5 Schedules
- **Location**: After main body of Act
- **Types**:
  - **Amending Schedules**: Modify other legislation
  - **Non-amending Schedules**: Supplementary material, forms, etc.
- **Short Titles**: May have specific titles for reference
  - Example: *Criminal Code Act 1995* (Cth) sch 1 ('Criminal Code')

### 1.3 Numbering System
- Sequential numbering: 1, 2, 3...
- Inserted provisions: 5A, 5B (between 5 and 6)
- Flexible system to accommodate amendments

### 1.4 Citation Format (AGLC)
```
Format: Title Year (Jurisdiction) pinpoint

Examples:
- Family Law Act 1975 (Cth)
- Family Law Act 1975 (Cth) s 79
- Family Law Act 1975 (Cth) s 79(4)(a)
- Criminal Code Act 1995 (Cth) sch 1 s 5.1(1)
```

**Pinpoint Components**:
- Space between abbreviation and number
- Subsections in parentheses (no space)
- Abbreviations: s (section), pt (part), sch (schedule), div (division)

---

## 2. CASE LAW (Judgments)

### 2.1 Hierarchical Structure

```
Judgment
├── Header Information
│   ├── Court Name
│   ├── Citation (Medium Neutral)
│   ├── Case Name
│   ├── Hearing Date(s)
│   ├── Judgment Date
│   └── Judge(s)/Judicial Officers
├── Catchwords
│   └── Keywords/Phrases (italicized/bold)
├── Headnote/Summary
│   ├── Facts Summary
│   ├── Legal Issues
│   ├── Held (Decision)
│   └── Arguments (CLR only)
├── Appearances
│   ├── Counsel for Applicant/Appellant
│   └── Counsel for Respondent
├── Legislation Cited
├── Cases Cited
├── Judgment Proper
│   ├── Introduction [1]-[n]
│   ├── Facts [n]-[m]
│   ├── Issues [m]-[p]
│   ├── Legal Analysis [p]-[q]
│   │   ├── Judge 1 Judgment
│   │   ├── Judge 2 Judgment (if applicable)
│   │   └── Dissenting Opinion (if applicable)
│   └── Conclusion [q]-[r]
└── Orders/Disposition
    └── Formal Orders Made
```

### 2.2 Structural Components

#### 2.2.1 Case Name Format
- **Individual Parties**: Surname only
  - Format: *Smith v Jones*
- **Multiple Parties**: First plaintiff and first defendant only
  - Format: *ABC Pty Ltd v XYZ Corporation*
- **Style**: Italicized, separated by 'v'

#### 2.2.2 Catchwords
- **Purpose**: Indexing and subject identification
- **Format**: Keywords/phrases separated by dashes or en-dashes
- **Content**:
  - Legal principles discussed
  - Legislation references
  - Subject matter terms
- **Multiple Sequences**: One per legal issue addressed
- **Style**: Italics or bold at beginning of case
- **Example**:
  ```
  FAMILY LAW – Property settlement – Contributions –
  Initial contributions – Homemaker contributions –
  Section 79 Family Law Act 1975

  MIGRATION – Visa cancellation – Character test –
  Discretion – Ministerial Direction No 65
  ```

#### 2.2.3 Headnote/Summary
- **Author**: Written by law reporter, NOT the judge
- **Status**: Not part of official judgment (not citable authority)
- **Content**:
  - Summary of facts
  - Legal issues raised
  - Principles of law decided
  - Outcome (Held)
  - Arguments of both sides (Commonwealth Law Reports only)
- **Marker**: End often indicated by "Curia advisari vult" or judges' names in CAPITALS

#### 2.2.4 Appearances
```
Appearances:
For the Applicant: [Barrister Name], instructed by [Solicitor Firm]
For the Respondent: [Barrister Name], instructed by [Solicitor Firm]
```

#### 2.2.5 Judgment Proper
- **Indicator**: Usually starts with judge's surname
  - Format: "STANLEY J:" or "Stanley J:"
- **Paragraph Numbering**: Sequential in square brackets
  - Format: [1], [2], [3]...[n]
  - Introduced since 2000 for medium neutral citations
- **Multiple Judges**: Each judge may write separately
  - Main judgment
  - Concurring judgments
  - Dissenting judgments

#### 2.2.6 Orders/Disposition
- **Location**: End of judgment
- **Format**: Numbered formal orders
- **Example**:
  ```
  THE COURT ORDERS THAT:
  1. The appeal be allowed.
  2. The orders of the District Court be set aside.
  3. The respondent pay the appellant's costs.
  ```

### 2.3 Citation Format (Medium Neutral)

See Section 5 for comprehensive medium neutral citation format.

---

## 3. REGULATIONS (Subordinate Legislation)

### 3.1 Hierarchical Structure

```
Regulation/Rule/By-law
├── Title
├── Enabling Act Reference
│   └── Authority Section
├── Commencement
├── Definitions
├── Regulation Provisions
│   ├── Parts
│   │   ├── Divisions
│   │   │   └── Regulations (numbered)
│   │   │       ├── Subregulations
│   │   │       │   ├── Paragraphs
│   │   │       │   │   └── Subparagraphs
└── Schedules
    ├── Forms
    ├── Tables
    └── Other Supplementary Material
```

### 3.2 Types of Subordinate Legislation

#### 3.2.1 Terminology by Jurisdiction
- **Regulations**: Most common term
- **Rules**: Court rules, procedural rules
- **By-laws**: Local government
- **Orders**: Administrative orders
- **Statutory Rules**: Some jurisdictions
- **Legislative Instruments**: Federal definition (Legislation Act 2003 s 8)

#### 3.2.2 Enabling Act Reference
- **Required**: Reference to parent Act
- **Format**: Made under authority of [Act Name]
- **Example**: "Made under the Family Law Act 1975"

### 3.3 Structural Components

#### 3.3.1 Regulation Numbering
- Similar to sections in Acts
- Numbered sequentially: reg 1, reg 2, reg 3
- Subregulations: reg 5(1), reg 5(2)
- Amendment insertions: reg 5A, reg 5B

#### 3.3.2 Schedule Formats
- **Forms**: Official forms prescribed by regulation
- **Tables**: Data tables, fee schedules, classifications
- **Technical Details**: Specifications, standards
- **Lists**: Approved items, prohibited substances

### 3.4 Citation Format (AGLC)

```
Format: Title Year (Jurisdiction) pinpoint

Examples:
- Right to Information Regulation 2009 (Qld)
- Uniform Civil Procedure Rules 1999 (Qld) r 5.4
- High Court Rules 2004 (Cth) r 21.07.1
- Family Law Rules 2004 (Cth) r 10.10(2)
```

**Style Requirements**:
- Title in italics
- Title case (maximal capitalization)
- "Regulation" or "Regulations" capitalized in title
- Same pinpoint format as Acts
- Abbreviation: r (rule), reg (regulation)

---

## 4. BILLS

### 4.1 Hierarchical Structure

```
Bill
├── Bill Metadata
│   ├── Bill Title
│   ├── Bill Number
│   ├── Parliament/Session
│   └── Introduction Date
├── Explanatory Memorandum (separate document)
│   ├── Overview
│   ├── Financial Impact Statement
│   ├── Clause-by-Clause Analysis
│   │   └── Explanation for each clause
│   ├── Anticipated Outcomes
│   └── Compatibility Statements
├── Second Reading Speech (Hansard record)
│   ├── Policy Background
│   ├── Legislative Objectives
│   ├── Expected Benefits
│   ├── Law Reform References
│   └── Anticipated Outcomes
└── Bill Text (same structure as Acts)
    └── [Follows Act structure - see Section 1]
```

### 4.2 Explanatory Memorandum (EM)

#### 4.2.1 Purpose and History
- **Introduction**: Became common from 1950s onwards
- **Mandatory**: All Commonwealth Government Bills since 1982
- **Audience**: Members of Parliament, officials, and public
- **Function**: Explains objective and operation of proposed law

#### 4.2.2 Structure
- **Overview**: High-level summary of Bill's purpose
- **Financial Impact**: Budgetary implications
- **Clause-by-Clause Explanation**:
  - Each clause analyzed separately
  - Intended effect if enacted
  - Non-legal language used
- **Policy Objectives**: Broader goals
- **Compatibility Statements**: Human rights, constitutional compliance

#### 4.2.3 Interpretive Use
- Used to interpret legislation if enacted
- Explains legislative intent
- Plain language for accessibility

#### 4.2.4 Availability
- Not all jurisdictions use EMs (South Australia exception)
- Most Bills from 1996+ available on Parliament websites
- If EM unavailable, second reading speech may substitute

### 4.3 Second Reading Speech

#### 4.3.1 Legislative Process Context
- **First Reading**: Bill presented (formal)
- **Second Reading**: Debate on Bill's purpose
- **Third Reading**: Vote on Bill

#### 4.3.2 Content
- **Background**: Policy context, law reform reports
- **Necessity**: Why law is needed
- **Positive Outcomes**: Expected benefits
- **Negative Prevention**: Problems addressed
- **Policy Objectives**: Government goals

#### 4.3.3 Speaker
- Minister or Member presenting the Bill
- Delivered before debate
- Recorded verbatim in Hansard

#### 4.3.4 Research Value
- Background to legislation
- Legislative intent
- Anticipated outcomes
- Useful when EM unavailable

### 4.4 Citation Format

```
Format: Title, Parliament, Session (Pinpoint if applicable)

Examples:
- Tax Laws Amendment Bill 2020 (Cth)
- Family Law Amendment Bill 2018 (Cth) cl 5
- EM to Tax Laws Amendment Bill 2020 (Cth) [3.5]
```

---

## 5. MEDIUM NEUTRAL CITATION FORMAT

### 5.1 Purpose and Introduction
- **Introduced**: Late 1990s by High Court of Australia
- **Purpose**: Uniform citation for online judgments
- **Independence**: Citation not dependent on publication medium
- **Advantage**: Enables citation before official reporting

### 5.2 Citation Structure

```
Format: Case Name [Year] Court Identifier Judgment Number, [Pinpoint]

Components:
1. Case Name (italicized)
2. [Year] (square brackets, mandatory)
3. Court Identifier (abbreviation, mandatory)
4. Judgment Number (court-allocated)
5. [Pinpoint] (paragraph numbers in square brackets)
```

### 5.3 Examples

```
Basic Citation:
Smith v Jones [2009] HCA 35

With Pinpoint:
Smith v Jones [2009] HCA 35, [6]

With Judge Reference:
Tropac Timbers Pty Ltd v A-One Asphalt Pty Ltd [2005] QSC 378, [19] (Muir J)

Multiple Paragraphs:
Kadir v The Queen [2020] HCA 1, [14], [18]--[21]

Multiple Judgments:
Work Health Authority v Outback Ballooning [2019] HCA 2, [3] (Kiefel CJ), [45] (Bell J)
```

### 5.4 Court Identifiers (Selected)

#### High Court
- **HCA**: High Court of Australia

#### Federal Courts
- **FCA**: Federal Court of Australia
- **FCAFC**: Federal Court (Full Court)
- **FamCA**: Family Court of Australia
- **FamCAFC**: Family Court (Full Court)
- **FCFCOA**: Federal Circuit and Family Court
- **AATA**: Administrative Appeals Tribunal

#### NSW Courts
- **NSWCA**: NSW Court of Appeal
- **NSWCCA**: NSW Court of Criminal Appeal
- **NSWSC**: NSW Supreme Court
- **NSWDC**: NSW District Court
- **NSWLC**: NSW Local Court
- **NSWLEC**: Land and Environment Court

#### NSW Tribunals
- **NSWCAT**: NSW Civil and Administrative Tribunal
- **NSWCATAD**: NCAT Administrative Division
- **NSWCATAP**: NCAT Appeal Panel
- **NSWCATCD**: NCAT Consumer Division
- **NSWCATGD**: NCAT Guardianship Division
- **NSWIRComm**: Industrial Relations Commission
- **NSWWCC**: Workers Compensation Commission

#### Other States
- **VSCA**: Victoria Court of Appeal
- **VSC**: Victoria Supreme Court
- **QCA**: Queensland Court of Appeal
- **QSC**: Queensland Supreme Court
- **WASCA**: WA Court of Appeal
- **WASC**: WA Supreme Court
- **SASCA**: SA Court of Appeal
- **SASC**: SA Supreme Court
- **TASSC**: Tasmania Supreme Court
- **ACTCA**: ACT Court of Appeal
- **ACTSC**: ACT Supreme Court

### 5.5 Paragraph Numbering
- **Format**: Sequential numbers in square brackets: [1], [2], [3]
- **Requirement**: Mandatory for decisions since 2000
- **Purpose**: Enable pinpoint references without page numbers
- **Application**: Numbers continue throughout entire judgment

### 5.6 Pinpoint Rules

#### Single Paragraph
```
[2020] HCA 1, [14]
```

#### Range of Paragraphs
```
[2020] HCA 1, [14]--[21]
(Use en-dash, not hyphen)
```

#### Multiple Non-consecutive Paragraphs
```
[2020] HCA 1, [14], [18], [23]
```

#### With Judicial Officer
```
[2020] HCA 1, [14] (Kiefel CJ)
[2020] HCA 1, [45]--[52] (Bell and Gageler JJ)
```

**Rule**: Add judicial officer in round brackets if not identified in accompanying text

---

## 6. PARSING SCHEMA STRUCTURES

### 6.1 Legislation Parser Schema

```python
{
  "document_type": "legislation",
  "metadata": {
    "long_title": str,
    "short_title": str,
    "citation": str,  # e.g., "Family Law Act 1975 (Cth)"
    "year": int,
    "jurisdiction": str,  # Cth, NSW, VIC, QLD, WA, SA, TAS, ACT, NT
    "act_number": str,
    "assent_date": str,
    "commencement_date": str
  },
  "preamble": str | None,
  "structure": {
    "chapters": [
      {
        "number": str,
        "title": str,
        "parts": [...]  # Nested structure
      }
    ],
    "parts": [
      {
        "number": str,
        "title": str,
        "heading_type": "preliminary" | "miscellaneous" | "general",
        "divisions": [
          {
            "number": str,
            "title": str,
            "subdivisions": [
              {
                "number": str,
                "title": str,
                "sections": [...]
              }
            ],
            "sections": [...]
          }
        ],
        "sections": [...]
      }
    ],
    "sections": [
      {
        "number": str,  # "79" or "79A"
        "title": str,
        "text": str,
        "subsections": [
          {
            "number": str,  # "(1)", "(2)"
            "text": str,
            "paragraphs": [
              {
                "letter": str,  # "(a)", "(b)"
                "text": str,
                "subparagraphs": [
                  {
                    "roman": str,  # "(i)", "(ii)"
                    "text": str
                  }
                ]
              }
            ]
          }
        ],
        "notes": str | None,
        "examples": [str] | None
      }
    ]
  },
  "schedules": [
    {
      "number": int | str,
      "title": str,
      "short_title": str | None,
      "schedule_type": "amending" | "non_amending",
      "contents": [...]  # May follow similar section structure
    }
  ],
  "definitions": {
    "section_reference": str,  # Where definitions are located
    "terms": [
      {
        "term": str,
        "definition": str,
        "section": str
      }
    ]
  }
}
```

### 6.2 Case Law Parser Schema

```python
{
  "document_type": "case_law",
  "metadata": {
    "case_name": str,
    "medium_neutral_citation": str,  # "[2020] HCA 35"
    "court_identifier": str,  # "HCA", "NSWSC", etc.
    "judgment_number": int,
    "year": int,
    "court_name": str,
    "jurisdiction": str,
    "hearing_dates": [str],
    "judgment_date": str,
    "judges": [
      {
        "name": str,
        "role": str,  # "CJ", "J", "JJ"
        "judgment_type": "main" | "concurring" | "dissenting"
      }
    ]
  },
  "catchwords": [
    {
      "sequence": int,
      "keywords": [str],  # List of keywords/phrases
      "separator": str  # Usually "–" or "-"
    }
  ],
  "headnote": {
    "facts_summary": str,
    "issues": [str],
    "held": str,
    "arguments": {  # CLR only
      "applicant": [str],
      "respondent": [str]
    } | None
  },
  "appearances": {
    "applicant": {
      "counsel": [str],
      "solicitors": [str]
    },
    "respondent": {
      "counsel": [str],
      "solicitors": [str]
    }
  },
  "legislation_cited": [
    {
      "citation": str,
      "sections": [str]
    }
  ],
  "cases_cited": [
    {
      "citation": str,
      "treatment": str  # "applied", "distinguished", "followed", "overruled"
    }
  ],
  "judgment": {
    "paragraphs": [
      {
        "number": int,
        "judge": str | None,  # If multi-judge decision
        "text": str,
        "heading": str | None,
        "footnotes": [str] | None
      }
    ],
    "sections": [
      {
        "heading": str,
        "paragraph_range": [int, int],  # Start, end paragraph numbers
        "type": "introduction" | "facts" | "issues" | "analysis" | "conclusion"
      }
    ]
  },
  "orders": [
    {
      "number": int,
      "text": str
    }
  ]
}
```

### 6.3 Regulation Parser Schema

```python
{
  "document_type": "regulation",
  "metadata": {
    "title": str,
    "citation": str,  # "Family Law Rules 2004 (Cth)"
    "year": int,
    "jurisdiction": str,
    "regulation_number": str | None,
    "enabling_act": {
      "title": str,
      "section": str | None  # Authority section
    },
    "commencement_date": str
  },
  "definitions": {
    "regulation_reference": str,
    "terms": [
      {
        "term": str,
        "definition": str
      }
    ]
  },
  "structure": {
    "parts": [
      {
        "number": str,
        "title": str,
        "divisions": [
          {
            "number": str,
            "title": str,
            "regulations": [...]
          }
        ],
        "regulations": [...]
      }
    ],
    "regulations": [
      {
        "number": str,  # "5", "5A"
        "title": str,
        "text": str,
        "subregulations": [
          {
            "number": str,
            "text": str,
            "paragraphs": [
              {
                "letter": str,
                "text": str
              }
            ]
          }
        ]
      }
    ]
  },
  "schedules": [
    {
      "number": int | str,
      "title": str,
      "schedule_type": "form" | "table" | "list" | "technical" | "other",
      "contents": {}  # Structure varies by type
    }
  ]
}
```

### 6.4 Bill Parser Schema

```python
{
  "document_type": "bill",
  "metadata": {
    "bill_title": str,
    "bill_number": str,
    "parliament": str,
    "session": str,
    "introduction_date": str,
    "jurisdiction": str,
    "stage": str  # "First Reading", "Second Reading", etc.
  },
  "bill_text": {
    # Same structure as legislation schema (Section 6.1)
  },
  "explanatory_memorandum": {
    "available": bool,
    "overview": str | None,
    "financial_impact": str | None,
    "clause_notes": [
      {
        "clause_number": str,
        "explanation": str,
        "intended_effect": str
      }
    ] | None,
    "policy_objectives": [str] | None,
    "compatibility_statements": {
      "human_rights": str | None,
      "constitutional": str | None
    } | None
  },
  "second_reading_speech": {
    "available": bool,
    "speaker": str | None,
    "date": str | None,
    "hansard_reference": str | None,
    "content": {
      "background": str | None,
      "objectives": [str] | None,
      "benefits": [str] | None,
      "law_reform_references": [str] | None
    } | None
  }
}
```

### 6.5 Common Extraction Patterns (Regex)

#### Section References
```python
PATTERNS = {
    "section": r"s(?:ection)?\s+(\d+[A-Z]*)",
    "subsection": r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)",
    "paragraph": r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)",
    "subparagraph": r"s(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)\(([ivx]+)\)",

    "part": r"[Pp]art\s+([IVX\d]+[A-Z]*)",
    "division": r"[Dd]ivision\s+(\d+[A-Z]*)",
    "schedule": r"[Ss]chedule\s+(\d+)",

    "regulation": r"reg(?:ulation)?\s+(\d+[A-Z]*)",
    "rule": r"r(?:ule)?\s+(\d+[A-Z]*\.\d+(?:\.\d+)?)",
}
```

#### Medium Neutral Citation
```python
MNC_PATTERN = r"\[(\d{4})\]\s+([A-Z]+(?:Comm|FC|CA|SC|DC|LC)?)\s+(\d+)"
PARAGRAPH_REF = r"\[(\d+)\]"
PARAGRAPH_RANGE = r"\[(\d+)\]--\[(\d+)\]"
```

#### Catchwords Extraction
```python
CATCHWORDS_PATTERN = r"(?:CATCHWORDS?|Catchwords?)[:\s]*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\nLEGISLATION|\nCases)"
```

#### Court Code Extraction
```python
COURT_CODE_PATTERN = r"\[?\d{4}\]?\s*([A-Z]+(?:Comm|FC|CA|SC|DC|LC|CC|MC|CT|AT|PD|AP|CD|GD|OD)?)\s*\d+"
```

---

## References

This document synthesizes information from the following authoritative sources:

**Legislation Structure:**
- [Structure of a law - Federal Register of Legislation](https://www.legislation.gov.au/help-and-resources/understanding-legislation/structure-of-a-law)
- [Structure of principal Acts - NSW legislation](https://legislation.nsw.gov.au/information/structure-of-principal-acts)
- [Legislative materials - Australian Guide to Legal Citation](https://bond.libguides.com/aglc/legislative-materials)

**Case Law Structure:**
- [GUIDE TO UNIFORM PRODUCTION OF JUDGMENTS SECOND EDITION](https://aija.org.au/wp-content/uploads/2017/10/Guide-to-Uniform-Production-of-Judgments-2nd-Ed-Olsson-1999.pdf)
- [Cases - Australian Guide to Legal Citation](https://bond.libguides.com/aglc/cases)
- [Case structure - Murdoch University](https://libguides.murdoch.edu.au/caselaw/about/structure)
- [Understanding Case Citations - UTS](https://studyguides.lib.uts.edu.au/caselaw/citations)

**Regulations:**
- [Delegated legislation - Style Manual](https://www.stylemanual.gov.au/referencing-and-attribution/legal-material/delegated-legislation)
- [Subordinate legislation - National Library of Australia](https://www.nla.gov.au/research-guides/australian-legislation/subordinate-legislation)

**Bills:**
- [Bills and explanatory memoranda - National Library of Australia](https://www.library.gov.au/research/research-guides-0/australian-legislation-research-guide/bills-and-explanatory-memoranda)
- [Explanatory Materials and Second Reading Speeches - UTS](https://studyguides.lib.uts.edu.au/legislation/explanatorymaterials)
- [Bills and explanatory material - Style Manual](https://www.stylemanual.gov.au/referencing-and-attribution/legal-material/bills-and-explanatory-material)

**Medium Neutral Citations:**
- [Cases - AGLC Referencing Style - ANU](https://libguides.anu.edu.au/c.php?g=641553&p=4493583)
- [Australian Guide to Legal Citation - UQ](https://guides.library.uq.edu.au/referencing/AGLC4/cases)

---

## Usage Notes for Anatomist Agent

### Parsing Strategy

1. **Document Type Detection**
   - Use citation format and document structure to identify type
   - Check for court codes (case law) vs section numbering (legislation)

2. **Hierarchical Extraction**
   - Parse from top-down: Chapter → Part → Division → Section
   - Maintain parent-child relationships in extracted data

3. **Component Identification**
   - Use regex patterns for numbered components
   - Identify headings by capitalization and formatting
   - Track nesting depth for correct hierarchy

4. **Metadata Extraction**
   - Extract citations early for document classification
   - Parse dates in multiple formats (ISO, Australian DD/MM/YYYY)
   - Identify jurisdiction from citation abbreviations

5. **Validation**
   - Verify hierarchical constraints (e.g., subdivisions require divisions)
   - Check numbering sequences for gaps or insertions
   - Validate citation format against AGLC standards

### Implementation Considerations

- **Text Preprocessing**: Remove page numbers, headers, footers before parsing
- **OCR Artifacts**: Handle common OCR errors in scanned documents
- **Version Control**: Track amendments, repeals, and consolidations
- **Cross-references**: Extract and link internal references between sections
- **Historical Documents**: Pre-2000 judgments lack paragraph numbering

---

**Document Version**: 1.0
**Last Updated**: 2025-11-29
**Maintained by**: Verridian AI - Functional Structure of Episodic Memory Project
