# Australian Legal Corpus Classification System

## Overview

The Australian Legal Corpus Classification System is a sophisticated multi-dimensional document classifier designed to categorize legal documents across 22 broad legal domains and 95+ granular subcategories. The system employs a 10-factor BOOST scoring methodology to achieve high-accuracy classification with confidence metrics.

## System Architecture

### Classification Pipeline

```
Document Input
    ↓
Document Type Detection
    ↓
Citation Extraction (Court, Legislation, Cases)
    ↓
Court Information Extraction
    ↓
Multi-Dimensional Scoring (10 BOOST Factors)
    ↓
Confidence Calculation
    ↓
MultiDomainClassification Output
```

### Classification Dimensions

The system evaluates documents across four primary dimensions:

1. **Keyword Patterns**: 16,407+ legal terms across 95 categories
2. **Legislation References**: 500+ Acts mapped to domains
3. **Landmark Case Citations**: 150+ key precedents
4. **Court Hierarchy**: 106+ court codes with authority scores

---

## 10-Factor BOOST Scoring System

The BOOST scoring system applies incremental score adjustments based on confidence signals, enabling precise multi-domain classification.

### BOOST 1: Citation Match (+10)

**Purpose**: Keywords appearing in the document citation receive higher weight.

**Example**:
```python
Citation: "Commissioner of Taxation v Smith [2020] FCA 123"
Keyword: "taxation" found in citation
Result: Tax_Federal category receives +10 boost
```

**Rationale**: Citation text is curated and highly reliable for domain classification.

---

### BOOST 2: Jurisdiction Alignment (+15-20)

**Purpose**: Domain-specific jurisdiction patterns boost relevant categories.

**Examples**:

| Pattern | Boost | Category |
|---------|-------|----------|
| "family" in jurisdiction | +20 | Family categories |
| "refugee" or "visa" in text | +15 | Admin_Migration |
| "criminal" in jurisdiction | +15 | Criminal categories |
| "employment" or "industrial" | +15 | Employment categories |

**Example**:
```python
Jurisdiction: "family court"
Search text: Contains "family court"
Result: All Family_* categories receive +20 boost
```

---

### BOOST 3: Court Domain Hint Alignment (+25)

**Purpose**: Specialist courts provide strong domain signals.

**Specialist Court Hints**:

| Court | Domain Hint | Example |
|-------|-------------|---------|
| FamCA | Family | Family Court of Australia |
| AAT | Administrative | Administrative Appeals Tribunal |
| FWC | Employment | Fair Work Commission |
| NSWLEC | Environment | NSW Land and Environment Court |
| NSWIC | Employment | NSW Industrial Court |

**Example**:
```python
Court: FamCA (Family Court of Australia)
Domain Hint: "Family"
Document category: Family_Property
Result: +25 boost (court hint matches category domain)
```

**Rationale**: This is the strongest single boost factor, as specialist court jurisdiction is highly deterministic.

---

### BOOST 4: Legislation Reference (+15)

**Purpose**: Referenced legislation provides direct domain mapping.

**Example**:
```python
Legislation Ref: "Fair Work Act 2009 s 394"
Mapped Domain: Employment
Mapped Subcategories: ['Emp_Unfair_Dismissal', 'Emp_General_Protections']
Result: Both subcategories receive +15 boost
```

**Key Legislation Examples**:

| Legislation | Domain | Subcategories |
|-------------|--------|---------------|
| Family Law Act 1975 s 79 | Family | Family_Property |
| Corporations Act 2001 s 180 | Commercial | Corp_Governance |
| Competition and Consumer Act 2010 s 18 | Commercial | Comm_Consumer |
| Income Tax Assessment Act 1997 | Tax | Tax_Income |
| Migration Act 1958 | Administrative | Admin_Migration |

---

### BOOST 5: Case Law Reference (+10)

**Purpose**: Citations to landmark cases indicate domain alignment.

**Example**:
```python
Case Ref: "Mabo v Queensland (No 2) (1992) 175 CLR 1"
Domain: Property
Subcategories: ['Native_Title']
Result: Native_Title receives +10 boost
```

**Landmark Case Examples**:

| Case | Domain | Key Area |
|------|--------|----------|
| Mabo v Queensland (No 2) | Property | Native Title |
| M v M (1988) 166 CLR 69 | Family | Family Property |
| Marks v GIO (1998) 196 CLR 494 | Torts | Negligence |
| FCT v Spotless Services | Tax | Tax Avoidance |

---

### BOOST 6: Case Title Pattern (+15-20)

**Purpose**: Party names in citations reveal case type.

**Pattern Rules**:

| Pattern | Boost | Categories |
|---------|-------|------------|
| "R v", "Regina v", "DPP v" | +20 | Criminal_General |
| "Minister" in citation | +15 | Admin_Review |
| "ACCC" in citation | +15 | Competition_Cartels, Comm_Consumer |
| "ASIC" in citation | +15 | Corp_Governance, Securities_Licensing |
| "Commissioner of Taxation" | +20 | Tax_Federal |

**Example**:
```python
Citation: "R v Smith [2020] NSWDC 45"
Pattern: "R v" detected
Result: Criminal_General receives +20 boost
```

---

### BOOST 7: Multi-Domain Confidence (+5)

**Purpose**: When multiple strong signals align, increase confidence.

**Example**:
```python
Strong categories (score >= 20): ['Family_Property', 'Family_Children', 'Equity_Trusts']
Count: 3 strong categories
Result: All 3 receive +5 boost
```

**Rationale**: Documents often span multiple related domains (e.g., family property division involving trusts).

---

### BOOST 8: Legislation Status (+10)

**Purpose**: Legislation documents receive type-specific boost.

**Example**:
```python
Document Type: PRIMARY_LEGISLATION
Result: All matched categories receive +10 boost
```

**Rationale**: Legislation classification is highly reliable from title keywords.

---

### BOOST 9: Common Law vs Statute Distinction (+5)

**Purpose**: Common law decisions favor equity/tort/property domains.

**Common Law Indicators**:
- "common law"
- "precedent"
- "stare decisis"
- "ratio decidendi"
- "obiter dicta"

**Example**:
```python
Text contains: "ratio decidendi"
Categories: Equity_Trusts, Tort_Negligence
Result: +5 boost to common law categories
```

---

### BOOST 10: Document Type Weighting (+2-15)

**Purpose**: Different document types have different classification reliability.

**Weights**:

| Document Type | Boost | Reason |
|---------------|-------|--------|
| Primary Legislation | +15 | Highly reliable from title |
| Secondary Legislation | +10 | Reliable from title |
| Case Law | +10 | Reliable from content |
| Tribunal Decision | +5 | Moderate reliability |
| Bill | +3 | Lower confidence |
| Explanatory Memo | +3 | Lower confidence |
| Practice Note | +2 | Lowest confidence |

---

## Multi-Domain Classification

### Primary Domain Selection

The **primary domain** is selected using:

1. **Highest scoring category** among all BOOST-adjusted scores
2. **Confidence score** = (primary score) / (total of all scores)

**Example**:
```python
Scores:
  Family_Property: 75 (highest)
  Family_Children: 45
  Equity_Trusts: 30
  Total: 150

Primary Domain: Family
Primary Category: Family_Property
Primary Confidence: 75/150 = 0.50 (50%)
```

### Secondary Domains

**Secondary domains** are included when:
- Category score confidence >= 10%
- Category maps to a **different** broad domain than primary
- Limited to top 5 secondary domains

**Example**:
```python
Secondary Domains:
  [('Equity', 'Equity_Trusts', 0.20),   # 20% confidence
   ('Property', 'Prop_Real', 0.15)]      # 15% confidence
```

---

## Confidence Scoring Methodology

### Confidence Calculation

```python
confidence = category_score / sum(all_category_scores)
```

### Confidence Tiers

| Tier | Range | Interpretation |
|------|-------|----------------|
| High | 0.60 - 1.00 | Clear single-domain document |
| Medium | 0.40 - 0.59 | Strong primary with related domains |
| Low | 0.20 - 0.39 | Multi-domain document |
| Very Low | 0.00 - 0.19 | Unclear or cross-cutting issues |

### Example Output

```python
{
  "document_id": "[2020] FamCA 123",
  "primary_domain": "Family",
  "primary_category": "Family_Property",
  "primary_confidence": 0.62,
  "secondary_domains": [
    {"domain": "Equity", "category": "Equity_Trusts", "confidence": 0.18},
    {"domain": "Property", "category": "Prop_Real", "confidence": 0.12}
  ],
  "boost_breakdown": {
    "citation_match": 10,
    "jurisdiction_alignment": 20,
    "court_domain_hint": 25,
    "legislation_reference": 15,
    "case_law_reference": 10,
    "case_title_pattern": 0,
    "multi_domain_confidence": 5,
    "legislation_status": 0,
    "common_statute_distinction": 0,
    "document_type_weight": 10,
    "total": 95
  }
}
```

---

## Classification Categories

### 22 Broad Domains

1. **Administrative** - Judicial review, migration, FOI
2. **Animal** - Animal welfare
3. **Charities** - NFP organizations
4. **Commercial** - Corporations, consumer law, IP
5. **Constitutional** - Federal/state powers
6. **Criminal** - All criminal offences and procedure
7. **Education** - Education law
8. **Elder** - Elder law
9. **Equity** - Trusts, succession, probate
10. **Family** - Marriage, children, property division
11. **Health** - Medical practitioners, mental health
12. **Industrial** - Employment, workplace safety
13. **Media** - Communications, broadcasting
14. **Privacy** - Data protection
15. **Procedural** - Civil procedure, evidence
16. **Property** - Real property, environment, planning
17. **Resources** - Mining, energy, infrastructure
18. **Specialized** - Maritime, aviation, military
19. **Sports** - Sports law, anti-doping
20. **Tax** - Federal and state taxation
21. **Torts** - Negligence, defamation, compensation
22. **Unclassified** - Fallback category

### 95+ Granular Subcategories

See [DOMAIN_TAXONOMY.md](DOMAIN_TAXONOMY.md) for complete category listing.

---

## Classification Workflow

### Document Processing

1. **Input**: Raw document with citation, text, metadata
2. **Court Extraction**: Parse citation for court code
3. **Authority Scoring**: Assign 0-100 authority score
4. **Citation Analysis**: Extract legislation and case references
5. **Keyword Matching**: Match against 16,407+ terms
6. **BOOST Application**: Apply 10 scoring factors
7. **Domain Attribution**: Calculate primary + secondary domains
8. **Confidence Scoring**: Compute confidence metrics
9. **Output**: Structured MultiDomainClassification

### Example End-to-End Classification

**Input Document**:
```json
{
  "citation": "Smith v Jones [2020] FamCA 45",
  "text": "The applicant seeks property orders under s 79 of the Family Law Act 1975...",
  "type": "case_law",
  "jurisdiction": "family court"
}
```

**Processing**:
1. Court: FamCA (authority: 75, domain_hint: Family)
2. Legislation: Family Law Act 1975 s 79 → Family_Property
3. Keywords: "property orders" (Family_Property), "applicant" (Family_General)
4. BOOST scores: citation_match(+10), jurisdiction(+20), court_hint(+25), legislation(+15)

**Output**:
```json
{
  "primary_domain": "Family",
  "primary_category": "Family_Property",
  "primary_confidence": 0.68,
  "authority_score": 75,
  "court_info": {
    "code": "FamCA",
    "name": "Family Court of Australia",
    "level": "superior_trial",
    "authority_score": 75
  }
}
```

---

## Version History

- **Version 2.0** (Current): Enhanced multi-domain classifier with 10-factor BOOST
- **Version 1.0**: Basic keyword-based classification

---

## Related Documentation

- [COURT_HIERARCHY.md](COURT_HIERARCHY.md) - Court codes and authority scoring
- [CITATION_FORMATS.md](CITATION_FORMATS.md) - Citation extraction patterns
- [DOMAIN_TAXONOMY.md](DOMAIN_TAXONOMY.md) - Complete domain taxonomy
- [API_REFERENCE.md](API_REFERENCE.md) - Code API documentation
