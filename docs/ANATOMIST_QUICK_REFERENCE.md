# Anatomist Agent Quick Reference Guide
## Australian Legal Document Structures - Parsing Cheat Sheet

---

## Document Type Detection

### 1. Legislation (Acts)
**Indicators:**
- Citation format: `Title Year (Jurisdiction)`
- Example: `Family Law Act 1975 (Cth)`
- Contains: Sections (s), Parts, Divisions, Schedules
- Structure: Sequential section numbering (s 1, s 2, s 79)

**Quick Test:**
```python
if re.search(r'\b(?:Act|Acts)\s+\d{4}\s*\((?:Cth|NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\)', text):
    document_type = "legislation"
```

### 2. Case Law (Judgments)
**Indicators:**
- Citation format: `[Year] COURT Number`
- Example: `[2020] HCA 35`
- Contains: Catchwords, paragraphs in [1], [2] format
- Has: Case name in *italics v italics* format

**Quick Test:**
```python
if re.search(r'\[\d{4}\]\s+[A-Z]{2,6}\s+\d+', text):
    document_type = "case_law"
```

### 3. Regulations
**Indicators:**
- Citation format: `Title Year (Jurisdiction)`
- Example: `Family Law Rules 2004 (Cth)`
- Contains: "Rules", "Regulations", "By-laws" in title
- Reference to enabling Act

**Quick Test:**
```python
if re.search(r'\b(?:Rules?|Regulations?|By-laws?)\s+\d{4}\s*\((?:Cth|NSW)\)', text):
    document_type = "regulation"
```

### 4. Bills
**Indicators:**
- Title contains "Bill"
- Example: `Tax Laws Amendment Bill 2020 (Cth)`
- May have Explanatory Memorandum (EM)
- May have Second Reading Speech

**Quick Test:**
```python
if re.search(r'\bBill\s+\d{4}\s*\((?:Cth|NSW)\)', text):
    document_type = "bill"
```

---

## Hierarchical Parsing Order

### Legislation Hierarchy (Top → Bottom)
```
1. Chapter (optional, large Acts only)
2. Part (most common top level)
3. Division (must be within Part)
4. Subdivision (must be within Division)
5. Section (primary provision unit)
6. Subsection (numbered in parentheses)
7. Paragraph (lettered in parentheses)
8. Subparagraph (roman numerals)
```

**Parsing Strategy:**
1. Identify top-level structure (Chapters or Parts)
2. Parse downward: Parts → Divisions → Sections
3. Within sections: Subsections → Paragraphs → Subparagraphs
4. Extract schedules separately (at end of document)

### Case Law Hierarchy
```
1. Header (court, citation, parties)
2. Catchwords (keywords/topics)
3. Headnote (summary - NOT citable)
4. Appearances (counsel/solicitors)
5. Judgment Proper (paragraphs [1] to [n])
6. Orders (formal court orders)
```

**Parsing Strategy:**
1. Extract medium neutral citation first
2. Parse catchwords (before main judgment)
3. Identify start of judgment: Judge's name + ":"
4. Parse paragraphs sequentially by [number]
5. Extract orders at end

---

## Critical Regex Patterns

### Section References
```python
PATTERNS = {
    # Basic section: "s 79" or "section 79"
    'section': r's(?:ection)?\s+(\d+[A-Z]*)',

    # With subsection: "s 79(4)"
    'subsection': r's(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)',

    # With paragraph: "s 79(4)(a)"
    'paragraph': r's(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)',

    # Full reference: "s 79(4)(a)(i)"
    'subparagraph': r's(?:ection)?\s+(\d+[A-Z]*)\((\d+)\)\(([a-z])\)\(([ivx]+)\)',

    # Inserted sections: "s 79A", "s 79AB"
    'inserted': r's(?:ection)?\s+(\d+[A-Z]+)',
}
```

### Structural Elements
```python
STRUCTURE = {
    # Part: "Part IV" or "Part 4A"
    'part': r'[Pp]art\s+([IVX\d]+[A-Z]*)',

    # Division: "Division 2"
    'division': r'[Dd]ivision\s+(\d+[A-Z]*)',

    # Schedule: "Schedule 1"
    'schedule': r'[Ss]chedule\s+(\d+)',

    # Chapter: "Chapter 3"
    'chapter': r'[Cc]hapter\s+([IVX\d]+[A-Z]*)',
}
```

### Medium Neutral Citations
```python
MNC = {
    # Full citation: "[2020] HCA 35"
    'citation': r'\[(\d{4})\]\s+([A-Z]+(?:FC|CA|SC|DC)?)\s+(\d+)',

    # Paragraph reference: "[14]"
    'paragraph': r'\[(\d+)\]',

    # Paragraph range: "[14]--[21]"
    'range': r'\[(\d+)\]--\[(\d+)\]',

    # Court code only: "HCA", "NSWSC"
    'court': r'\[?\d{4}\]?\s*([A-Z]+(?:FC|CA|SC|DC)?)\s*\d+',
}
```

### Catchwords Extraction
```python
CATCHWORDS = r'(?:CATCHWORDS?|Catchwords?)[:\s]*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\nLEGISLATION|\nCases)'
```

---

## Common Court Codes

### Federal Courts
- **HCA** = High Court of Australia
- **FCA** = Federal Court of Australia
- **FCAFC** = Federal Court (Full Court)
- **FamCA** = Family Court of Australia
- **FamCAFC** = Family Court (Full Court)
- **FCFCOA** = Federal Circuit and Family Court

### NSW Courts
- **NSWCA** = NSW Court of Appeal
- **NSWCCA** = NSW Court of Criminal Appeal
- **NSWSC** = NSW Supreme Court
- **NSWDC** = NSW District Court
- **NSWLC** = NSW Local Court
- **NSWLEC** = Land and Environment Court

### NSW Tribunals
- **NSWCAT** = NSW Civil and Administrative Tribunal
- **NSWCATAD** = NCAT Administrative Division
- **NSWCATAP** = NCAT Appeal Panel
- **NSWIRComm** = Industrial Relations Commission
- **NSWWCC** = Workers Compensation Commission

### Other States
- **VSCA/VSC** = Victoria Court of Appeal/Supreme Court
- **QCA/QSC** = Queensland Court of Appeal/Supreme Court
- **WASCA/WASC** = WA Court of Appeal/Supreme Court
- **SASCA/SASC** = SA Court of Appeal/Supreme Court

---

## Citation Formatting Rules (AGLC)

### Legislation
```
Format: Title Year (Jurisdiction) pinpoint

Examples:
✓ Family Law Act 1975 (Cth)
✓ Family Law Act 1975 (Cth) s 79
✓ Family Law Act 1975 (Cth) s 79(4)(a)
✗ Family Law Act 1975 (Cth) s79(4)(a)  [Missing space]
✗ Family Law Act 1975 (Cth) s 79 (4)   [Extra space]
```

**Pinpoint Abbreviations:**
- s = section
- ss = sections
- pt = part
- div = division
- sch = schedule
- reg = regulation
- r = rule

### Case Law (Medium Neutral)
```
Format: Case Name [Year] Court Number, [Paragraph]

Examples:
✓ Smith v Jones [2020] HCA 35
✓ Smith v Jones [2020] HCA 35, [14]
✓ Smith v Jones [2020] HCA 35, [14]--[21]
✓ Smith v Jones [2020] HCA 35, [14] (Kiefel CJ)
✗ Smith v Jones (2020) HCA 35  [Wrong brackets on year]
✗ Smith v Jones [2020] HCA 35 [14]  [Missing comma]
```

### Regulations
```
Format: Title Year (Jurisdiction) pinpoint

Examples:
✓ Family Law Rules 2004 (Cth)
✓ Family Law Rules 2004 (Cth) r 10.10
✓ Uniform Civil Procedure Rules 1999 (Qld) r 5.4(2)
```

---

## Parsing Validation Checklist

### Legislation Validation
- [ ] Chapters only contain Parts (if Chapters exist)
- [ ] Divisions only exist within Parts
- [ ] Subdivisions only exist within Divisions
- [ ] Sections have sequential numbering (allow for inserted: 5A, 5B)
- [ ] Subsections use format (1), (2), (3)
- [ ] Paragraphs use format (a), (b), (c)
- [ ] Subparagraphs use format (i), (ii), (iii)
- [ ] Schedules are at the end of document
- [ ] Preliminary Part is first (if exists)
- [ ] Miscellaneous Part is last (if exists)

### Case Law Validation
- [ ] Medium neutral citation matches format [Year] Court Number
- [ ] Court code is valid (check COURT_CODE_MAP)
- [ ] Paragraph numbers are sequential: [1], [2], [3]...
- [ ] Paragraph numbers in square brackets, not round
- [ ] Catchwords appear before judgment proper
- [ ] Headnote is NOT part of judgment (separate)
- [ ] Orders appear at end of judgment
- [ ] Judge's name appears before judgment text (format: "NAME J:")

---

## Component Identification Tips

### Finding Section Boundaries
```python
def find_sections(text: str) -> List[Dict]:
    """Extract all sections from legislation text."""
    sections = []
    # Pattern: number followed by title in bold/caps
    pattern = r'^(\d+[A-Z]*)[.\s]+([A-Z][^\n]+)'
    for match in re.finditer(pattern, text, re.MULTILINE):
        sections.append({
            'number': match.group(1),
            'title': match.group(2).strip(),
            'start': match.start()
        })
    return sections
```

### Finding Judgment Paragraphs
```python
def find_paragraphs(text: str) -> List[Dict]:
    """Extract numbered paragraphs from judgment."""
    paragraphs = []
    # Pattern: [number] at start of line or after whitespace
    pattern = r'(?:^|\s)\[(\d+)\]\s+([^\[]+?)(?=\s\[\d+\]|$)'
    for match in re.finditer(pattern, text, re.DOTALL):
        paragraphs.append({
            'number': int(match.group(1)),
            'text': match.group(2).strip()
        })
    return paragraphs
```

### Detecting Headings
```python
def is_heading(line: str) -> bool:
    """Determine if line is a heading."""
    line = line.strip()

    # All caps (5+ chars)
    if re.match(r'^[A-Z\s]{5,}$', line):
        return True

    # Starts with structural marker
    if re.match(r'^(?:Part|Division|Chapter|Schedule)\s+', line):
        return True

    # Title case + short (< 100 chars)
    if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$', line) and len(line) < 100:
        return True

    return False
```

---

## Edge Cases and Special Handling

### Inserted Provisions
```
Original: s 5, s 6, s 7
Amended:  s 5, s 5A, s 5B, s 6, s 7

Parsing: Treat "5A" as a valid section number
Pattern: \d+[A-Z]+
```

### Multiple Judges
```
Judgment may have:
- Main judgment (first)
- Concurring judgments (agree but different reasoning)
- Dissenting judgments (disagree)

Indicator: New paragraph starting with judge name
Example: "BELL J:" or "GAGELER J:"
```

### Schedules with Short Titles
```
Citation: Criminal Code Act 1995 (Cth) sch 1
Short Title: 'Criminal Code'
Reference: Criminal Code s 5.1

Parsing: Extract short title from first mention
Pattern: sch \d+ \('([^']+)'\)
```

### Pre-2000 Judgments
```
Issue: No paragraph numbering
Solution: Use page numbers if available
Format: (2000) CLR 123, 456
         ^^^^^^^^^^^  ^^^
         Reporter     Page number
```

---

## Performance Optimization Tips

### 1. Pre-compile Regex Patterns
```python
import re

class Patterns:
    SECTION = re.compile(r's(?:ection)?\s+(\d+[A-Z]*)')
    MNC = re.compile(r'\[(\d{4})\]\s+([A-Z]+)\s+(\d+)')
    # ... etc

# Use:
match = Patterns.SECTION.search(text)
```

### 2. Extract Document Type First
```python
def get_document_type(text: str) -> str:
    """Fast document type detection."""
    # Check first 1000 chars only
    header = text[:1000]

    if re.search(r'\[\d{4}\]\s+[A-Z]+\s+\d+', header):
        return "case_law"
    elif re.search(r'\bAct\s+\d{4}\s*\(', header):
        return "legislation"
    elif re.search(r'\b(?:Rules|Regulations)\s+\d{4}', header):
        return "regulation"
    elif re.search(r'\bBill\s+\d{4}', header):
        return "bill"
    return "unknown"
```

### 3. Parse in Chunks
```python
def parse_large_document(text: str) -> Dict:
    """Parse large documents in sections."""
    # 1. Extract metadata (first 2000 chars)
    metadata = extract_metadata(text[:2000])

    # 2. Parse structure (full text)
    structure = parse_structure(text)

    # 3. Extract specific provisions on-demand
    return {
        'metadata': metadata,
        'structure': structure,
        'get_section': lambda n: extract_section(text, n)
    }
```

---

## Common Parsing Errors

### 1. Subsection Spacing
```python
# WRONG: No space between section and subsection
❌ s79(4)

# CORRECT: Space before opening parenthesis
✓ s 79(4)

# Pattern should handle both:
r's(?:ection)?\s*(\d+[A-Z]*)\s*\((\d+)\)'
```

### 2. Paragraph Range Format
```python
# WRONG: Using hyphen
❌ [14]-[21]

# CORRECT: Using en-dash
✓ [14]--[21]

# Pattern:
r'\[(\d+)\]--\[(\d+)\]'
```

### 3. Heading Detection
```python
# False positives:
- All caps text in body (not just headings)
- Roman numerals in lists (I, II, III)

# Solution: Check context
def is_heading(line: str, prev_line: str, next_line: str) -> bool:
    if not line.strip():
        return False

    # Blank lines before/after suggest heading
    if not prev_line.strip() and not next_line.strip():
        if re.match(r'^[A-Z\s]+$', line):
            return True

    return False
```

---

## Integration with GSW System

### Extracted Components → GSW Actors

```python
# Section → Actor
section = {
    'number': '79',
    'title': 'Property settlement orders'
}
# Becomes:
actor = Actor(
    name="Section 79",
    actor_type=ActorType.LEGAL_DOCUMENT,
    roles=["property_settlement_provision"],
    metadata={'title': 'Property settlement orders'}
)

# Judgment → Actors
case = {
    'citation': '[2020] HCA 35',
    'parties': ['Smith', 'Jones']
}
# Becomes:
actors = [
    Actor(name="Smith", actor_type=ActorType.PERSON, roles=["applicant"]),
    Actor(name="Jones", actor_type=ActorType.PERSON, roles=["respondent"]),
    Actor(name="[2020] HCA 35", actor_type=ActorType.LEGAL_DOCUMENT,
          roles=["judgment"], metadata={'court': 'HCA'})
]
```

### Document Structure → Spatio-Temporal Links

```python
# Link sections to their Part
link = SpatioTemporalLink(
    linked_entity_ids=[
        "section_79", "section_80", "section_81"
    ],
    tag_type=LinkType.SPATIAL,
    tag_value="Part VIII - Property"
)

# Link judgment paragraphs to date
link = SpatioTemporalLink(
    linked_entity_ids=[
        "para_1", "para_2", "para_3"
    ],
    tag_type=LinkType.TEMPORAL,
    tag_value="2020-03-15"  # Judgment date
)
```

---

## Quick Reference: Document Types

| Type | Citation Example | Top Structure | Provision Unit | Paragraph Format |
|------|-----------------|---------------|----------------|------------------|
| **Act** | `Family Law Act 1975 (Cth)` | Part/Chapter | Section (s) | (1), (2), (a), (i) |
| **Regulation** | `Family Law Rules 2004 (Cth)` | Part | Regulation/Rule (r) | (1), (2), (a), (i) |
| **Case** | `[2020] HCA 35` | - | Paragraph | [1], [2], [3] |
| **Bill** | `Tax Laws Bill 2020 (Cth)` | Part | Clause | (1), (2), (a) |

---

**Last Updated:** 2025-11-29
**Related Documentation:**
- C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\docs\AUSTRALIAN_LEGAL_DOCUMENT_STRUCTURES.md
- C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\document_schemas.py
