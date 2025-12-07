# Australian Legal Citation Formats

## Overview

Australian legal documents follow standardized citation formats governed by the Australian Guide to Legal Citation (AGLC4). The classification system extracts and parses three primary citation types: medium neutral citations, authorized reports, and legislation references.

---

## Medium Neutral Citations

### Format

```
[YEAR] COURT NUMBER
```

### Pattern

```python
MEDIUM_NEUTRAL_PATTERN = re.compile(
    r'\[(\d{4})\]\s*([A-Za-z]{2,10})\s*(\d+)',
    re.IGNORECASE
)
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Year** | Year of decision (4 digits) | 2020 |
| **Court** | Court abbreviation (2-10 letters) | HCA, NSWCA, FCA |
| **Number** | Sequential case number | 15, 123, 4567 |

### Examples

| Citation | Year | Court | Number | Description |
|----------|------|-------|--------|-------------|
| `[2020] HCA 15` | 2020 | HCA | 15 | High Court decision 15 of 2020 |
| `[2019] FCAFC 123` | 2019 | FCAFC | 123 | Federal Court Full Court |
| `[2021] NSWCA 45` | 2021 | NSWCA | 45 | NSW Court of Appeal |
| `[2020] FamCA 67` | 2020 | FamCA | 67 | Family Court of Australia |
| `[2022] VCAT 890` | 2022 | VCAT | 890 | Victorian tribunal |

### Characteristics

- **Official**: Assigned by the court
- **Unique**: No two cases share same citation
- **Persistent**: Remains consistent across databases
- **Jurisdiction-neutral**: No publisher dependency

### Extraction Example

```python
text = "The decision in Smith v Jones [2020] HCA 15 established..."
matches = MEDIUM_NEUTRAL_PATTERN.finditer(text)

for match in matches:
    year, court, number = match.groups()
    # year = "2020", court = "HCA", number = "15"
```

---

## Authorized Report Citations

### Format

```
(YEAR) VOLUME REPORT PAGE
```

### Pattern

```python
AUTHORIZED_REPORT_PATTERN = re.compile(
    r'\((\d{4})\)\s+(\d+)\s+([A-Z]{2,6})\s+(\d+)',
    re.IGNORECASE
)
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Year** | Year of publication | 2020 |
| **Volume** | Volume number | 271 |
| **Report** | Report series abbreviation | CLR, FCR, NSWLR |
| **Page** | Starting page number | 657 |

### Examples

| Citation | Year | Vol | Report | Page | Description |
|----------|------|-----|--------|------|-------------|
| `(2020) 271 CLR 657` | 2020 | 271 | CLR | 657 | Commonwealth Law Reports |
| `(2019) 268 FCR 123` | 2019 | 268 | FCR | 123 | Federal Court Reports |
| `(2021) 105 NSWLR 45` | 2021 | 105 | NSWLR | 45 | NSW Law Reports |
| `(2020) 60 FLR 234` | 2020 | 60 | FLR | 234 | Federal Law Reports |
| `(2018) 56 FLC 93-876` | 2018 | 56 | FLC | 93-876 | Family Law Cases |

### Major Report Series

| Abbreviation | Full Name | Court | Authority |
|--------------|-----------|-------|-----------|
| **CLR** | Commonwealth Law Reports | HCA | 100 |
| **FCR** | Federal Court Reports | FCA | 85 |
| **ALR** | Australian Law Reports | Multiple | 80 |
| **NSWLR** | New South Wales Law Reports | NSWCA/SC | 80 |
| **VR** | Victorian Reports | VSCA/VSC | 80 |
| **QdR** | Queensland Reports | QCA/QSC | 80 |
| **SASR** | South Australian State Reports | SASC | 80 |
| **WAR** | Western Australian Reports | WASC | 80 |
| **TasR** | Tasmanian Reports | TASSC | 80 |
| **FLC** | Family Law Cases | FamCA | 75 |
| **FLR** | Federal Law Reports | Multiple | 75 |
| **ACSR** | Australian Corporations and Securities Reports | Multiple | 75 |
| **IR** | Industrial Reports | IRC/FWC | 60 |

### Dual Citation

Most modern cases have both medium neutral and authorized report citations:

```
Smith v Jones [2020] HCA 15; (2020) 271 CLR 657
```

---

## Legislation Citations

### Format

```
[Act Name] YEAR (Jurisdiction) [section]
```

### Pattern

```python
LEGISLATION_PATTERN = re.compile(
    r'([A-Z][a-zA-Z\s]+(?:Act|Regulation|Rules?))\s+(\d{4})\s*\(([A-Za-z]{2,4})\)(?:\s+s\s*(\d+[a-zA-Z]*(?:\([a-z0-9]+\))?))?',
    re.IGNORECASE
)
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Act Name** | Full or short title | Family Law Act |
| **Year** | Year of enactment | 1975 |
| **Jurisdiction** | Cth, NSW, VIC, etc. | Cth |
| **Section** | Optional section reference | s 79 |

### Examples

| Citation | Act | Year | Juris | Section |
|----------|-----|------|-------|---------|
| `Family Law Act 1975 (Cth)` | Family Law Act | 1975 | Cth | - |
| `Fair Work Act 2009 (Cth) s 394` | Fair Work Act | 2009 | Cth | s 394 |
| `Crimes Act 1900 (NSW)` | Crimes Act | 1900 | NSW | - |
| `Evidence Act 1995 (NSW) s 56` | Evidence Act | 1995 | NSW | s 56 |

### Jurisdiction Abbreviations

| Code | Jurisdiction |
|------|--------------|
| **Cth** | Commonwealth (Federal) |
| **NSW** | New South Wales |
| **Vic** | Victoria |
| **Qld** | Queensland |
| **WA** | Western Australia |
| **SA** | South Australia |
| **Tas** | Tasmania |
| **ACT** | Australian Capital Territory |
| **NT** | Northern Territory |

### Short Form Citations

After first mention, short forms are acceptable:

```
First: Family Law Act 1975 (Cth) s 79
Later: FLA s 79
```

Common abbreviations:
- **FLA** = Family Law Act
- **FWA** = Fair Work Act
- **ITAA** = Income Tax Assessment Act
- **CCA** = Competition and Consumer Act
- **PPSA** = Personal Property Securities Act

---

## Section and Subsection References

### Format Hierarchy

```
s SECTION(subsection)(paragraph)(subparagraph)
```

### Pattern

```python
SECTION_PATTERN = re.compile(
    r'(?:s|section|reg|regulation|r|rule)\s*(\d+[a-zA-Z]*(?:\([a-z0-9]+\))?(?:\.\d+)?)',
    re.IGNORECASE
)
```

### Examples

| Reference | Meaning |
|-----------|---------|
| `s 79` | Section 79 |
| `s 79(4)` | Section 79, subsection 4 |
| `s 79(4)(a)` | Section 79, subsection 4, paragraph (a) |
| `s 79(4)(a)(i)` | Section 79, subsection 4, paragraph (a), subparagraph (i) |
| `s 51(xxvi)` | Section 51, paragraph 26 (constitutional) |
| `reg 4.12` | Regulation 4.12 |

### Complex Examples

#### Family Law Act 1975 s 79

```
s 79     Power to alter property interests
s 79(2)  Court must not make order unless satisfied as to just and equitable
s 79(4)  Matters to consider (contributions)
s 79(4)(a)  Financial contributions
s 79(4)(b)  Non-financial contributions
s 79(4)(c)  Contributions as homemaker/parent
```

#### Constitution s 51

```
s 51       Legislative powers of Commonwealth
s 51(i)    Trade and commerce
s 51(xx)   Corporations power
s 51(xxvi) People of any race
```

---

## Part, Division, and Schedule References

### Part References

```python
PART_PATTERN = re.compile(
    r'\bPart\s+([IVXLCDM]+|\d+[A-Z]?)',
    re.IGNORECASE
)
```

**Examples**:
- `Part IV` (Roman numerals)
- `Part 2` (Arabic numerals)
- `Part VIIA` (with letter suffix)

### Division References

```python
DIVISION_PATTERN = re.compile(
    r'\bDivision\s+(\d+[A-Z]?)',
    re.IGNORECASE
)
```

**Examples**:
- `Division 2`
- `Division 7A` (tax)

### Schedule References

```python
SCHEDULE_PATTERN = re.compile(
    r'\bSchedule\s+(\d+[A-Z]?)',
    re.IGNORECASE
)
```

**Examples**:
- `Schedule 1`
- `Schedule 3A`

---

## Extraction Pipeline

### Complete Citation Extraction

```python
class CitationExtractor:
    @classmethod
    def extract_all(cls, text: str) -> Dict:
        return {
            'medium_neutral': cls.extract_medium_neutral(text),
            'authorized_reports': cls.extract_authorized_reports(text),
            'legislation': cls.extract_legislation(text),
            'sections': cls.extract_sections(text),
        }
```

### Example Extraction

**Input Text**:
```
In Smith v Jones [2020] HCA 15; (2020) 271 CLR 657, the High Court
considered the application of s 79 of the Family Law Act 1975 (Cth).
The decision followed M v M (1988) 166 CLR 69.
```

**Extracted Citations**:
```python
{
  'medium_neutral': [
    {'citation': '[2020] HCA 15', 'year': 2020, 'court': 'HCA', 'number': 15}
  ],
  'authorized_reports': [
    {'citation': '(2020) 271 CLR 657', 'year': 2020, 'volume': 271, 'report': 'CLR', 'page': 657},
    {'citation': '(1988) 166 CLR 69', 'year': 1988, 'volume': 166, 'report': 'CLR', 'page': 69}
  ],
  'legislation': [
    {
      'name': 'Family Law Act',
      'year': 1975,
      'jurisdiction': 'Cth',
      'section': 's 79'
    }
  ],
  'sections': ['s 79']
}
```

---

## AGLC4 Compliance

The Australian Guide to Legal Citation (4th ed) sets citation standards:

### Case Law

#### First Citation
```
Smith v Jones [2020] HCA 15; (2020) 271 CLR 657
```

#### Subsequent Citations
```
Smith v Jones [2020] HCA 15; (2020) 271 CLR 657, 665 [23] (Gageler J)
```

Components:
- Case name (italics)
- Medium neutral citation
- Authorized report citation
- Pinpoint page reference
- Paragraph number in [brackets]
- Judge name (if needed)

### Legislation

#### Commonwealth Acts
```
Family Law Act 1975 (Cth) s 79
```

#### State Acts
```
Crimes Act 1900 (NSW) s 61I
```

#### Regulations
```
Family Law Regulations 1984 (Cth) reg 4.12
```

### Pinpoint References

```
at 665 [23]      Page 665, paragraph 23
at 657-659       Pages 657 to 659
at [15]-[20]     Paragraphs 15 to 20
```

---

## Case Name Parsing

### Party Name Extraction

Common patterns:

| Pattern | Type | Example |
|---------|------|---------|
| `A v B` | Civil | Smith v Jones |
| `R v A` | Criminal | R v Smith |
| `Re A` | In the matter of | Re ABC Pty Ltd |
| `Ex parte A` | Administrative | Ex parte Smith |

### Special Parties

| Party | Meaning |
|-------|---------|
| **R** or **Regina** or **Rex** | The Crown (criminal) |
| **DPP** | Director of Public Prosecutions |
| **Commonwealth** | Federal government |
| **Minister for...** | Government minister (admin law) |
| **Commissioner of Taxation** | Tax authority |
| **ASIC** | Australian Securities and Investments Commission |
| **ACCC** | Australian Competition and Consumer Commission |

---

## Citation Type Detection

### Detection Logic

```python
class CitationExtractor:
    @classmethod
    def detect_citation_type(cls, citation: str) -> CitationType:
        if cls.MEDIUM_NEUTRAL_PATTERN.search(citation):
            return CitationType.MEDIUM_NEUTRAL
        if cls.AUTHORIZED_REPORT_PATTERN.search(citation):
            return CitationType.AUTHORIZED_REPORT
        if cls.LEGISLATION_PATTERN.search(citation):
            return CitationType.LEGISLATION
        return CitationType.UNKNOWN
```

### Examples

| Citation | Type |
|----------|------|
| `[2020] HCA 15` | MEDIUM_NEUTRAL |
| `(2020) 271 CLR 657` | AUTHORIZED_REPORT |
| `Family Law Act 1975 (Cth)` | LEGISLATION |
| `Decision 123/2020` | UNKNOWN |

---

## Common Edge Cases

### Multiple Courts Same Year

```
[2020] NSWSC 123    NSW Supreme Court
[2020] NSWCA 123    NSW Court of Appeal (different case)
```

### Historical Cases

Pre-2000 cases may lack medium neutral citations:

```
Mabo v Queensland (No 2) (1992) 175 CLR 1
```

### Unreported Decisions

```
Smith v Jones (Unreported, Supreme Court of NSW, Young J, 15 March 2020)
```

### Tribunal Decisions

```
[2020] AATA 1234
Smith and Department of Immigration [2020] AATA 1234
```

---

## Extraction Best Practices

### 1. Use Regex with Context

Extract citations with surrounding text for disambiguation:

```python
# Extract with 20 chars context on each side
pattern = r'.{0,20}' + MEDIUM_NEUTRAL_PATTERN + r'.{0,20}'
```

### 2. Validate Extracted Citations

Check if court code exists in `COURT_CODES`:

```python
court_code = match.group(2)
if court_code not in COURT_CODES:
    # Might be false positive
    validate_further()
```

### 3. Handle Case Sensitivity

Court codes can be mixed case:

```python
# [2020] FamCA 123  (correct)
# [2020] FAMCA 123  (variant)
# Normalize to uppercase for lookup
```

### 4. Limit Results

Extract top N most relevant:

```python
legislation_refs[:10]  # Limit to 10 most mentioned
case_refs[:10]
```

---

## Related Documentation

- [COURT_HIERARCHY.md](COURT_HIERARCHY.md) - Court code definitions
- [CLASSIFICATION_SYSTEM.md](CLASSIFICATION_SYSTEM.md) - How citations inform classification
- [API_REFERENCE.md](API_REFERENCE.md) - CitationExtractor class reference
