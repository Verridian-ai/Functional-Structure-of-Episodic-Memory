# Acts Interpretation Acts - Quick Reference

## Quick Start

```python
from src.logic.interpretation_acts import InterpretationActsDB

db = InterpretationActsDB()
```

## Common Lookups

### Get a Definition

```python
# Get definition of 'person' in Commonwealth legislation
person = db.get_definition('person', 'Commonwealth')
print(person.definition)
# "Includes a body politic or corporate as well as an individual"

# Get definition in specific state
month = db.get_definition('month', 'New South Wales')
```

### Classify Modal Verbs

```python
# Is 'may' mandatory or permissive?
modal = db.classify_modal('may', 'Commonwealth')
print(modal.modal_type)  # "PERMISSIVE"
print(modal.creates)     # "power"

# Is 'must' mandatory?
modal = db.classify_modal('must', 'Victoria')
print(modal.modal_type)  # "MANDATORY"
print(modal.creates)     # "duty"
```

### Calculate Time Periods

```python
# Calculate 1 month from a date (calendar month rule)
end_date = db.calculate_month('2024-01-31')
print(end_date)  # "2024-02-29" (leap year)

# Calculate commencement date
commencement = db.calculate_commencement('2024-06-01', 'Commonwealth')
print(commencement)  # "2024-06-29" (28 days after assent)

# Check if business day
is_business = db.is_business_day('2024-01-08')  # Monday
print(is_business)  # True
```

### Extract Obligations

```python
text = """
The Minister must approve applications.
The Minister may delegate this power.
A person must not provide false information.
"""

obligations = db.extract_obligations(text)

print(obligations['duties'])        # Mandatory requirements
print(obligations['powers'])        # Discretionary powers
print(obligations['prohibitions'])  # Things you must not do
```

## Key Default Definitions

| Term | Meaning | Applies To |
|------|---------|-----------|
| **person** | Includes corporations | All jurisdictions |
| **month** | Calendar month | All jurisdictions |
| **may** | Permissive/discretionary | All jurisdictions |
| **must** | Mandatory/imperative | All jurisdictions |
| **shall** | Mandatory (archaic) | All jurisdictions |
| **writing** | Includes electronic docs | All jurisdictions |
| **business day** | Not weekend/public holiday | Commonwealth, some states |

## Critical Legal Principles

### 1. Person = Corporations

**Rule:** "Person" ALWAYS includes corporations unless context excludes them.

```python
includes_corp = db.includes_corporations('person', 'Commonwealth')
print(includes_corp)  # True
```

**Implications:**
- Corporate liability for statutory duties
- Corporate rights under statutes
- Only excluded by physical impossibility or express language

### 2. May vs Must

**"May" = Discretionary**
- Creates a power or right
- NOT mandatory
- Can choose whether to exercise

**"Must" / "Shall" = Mandatory**
- Creates a legal duty
- No discretion
- Failure = breach of statutory obligation

```python
from src.logic.interpretation_acts import is_mandatory, is_permissive

is_mandatory('must')  # True
is_permissive('may')  # True
```

### 3. Month = Calendar Month

**Rule:** All Australian jurisdictions define "month" as calendar month.

**Calculation:**
- Go to same day next month
- If no corresponding day, use last day of that month

**Examples:**
```
1 month from Jan 31 = Feb 28 (or 29 in leap year)
1 month from Jan 15 = Feb 15
1 month from Mar 31 = Apr 30
```

### 4. Gender Neutrality

**Rule:** ALL jurisdictions require gender-neutral interpretation.

- "He" includes "she" and "they"
- "His" includes "her" and "their"
- Cannot rely on gender of pronouns

### 5. Headings Are Part of Act

**Rule:** Headings can be used for interpretation (all jurisdictions).

- Not merely organizational
- Can resolve ambiguity
- Subordinate to operative text

## Commencement Rules by Jurisdiction

| Jurisdiction | Default Commencement |
|-------------|---------------------|
| Commonwealth | 28 days after Royal Assent |
| NSW | Date of assent |
| Victoria | Date of assent |
| Queensland | Date of assent |
| SA | Date of assent |
| Tasmania | Date of assent |
| NT | Date of assent |
| WA | Publication in Gazette |
| ACT | Notification on register |

```python
# Commonwealth - 28 days
db.calculate_commencement('2024-06-01', 'Commonwealth')
# Returns: '2024-06-29'

# NSW - immediate
db.calculate_commencement('2024-06-01', 'New South Wales')
# Returns: '2024-06-01'
```

## Convenience Functions

```python
from src.logic.interpretation_acts import (
    get_definition,
    is_mandatory,
    is_permissive
)

# Quick definition lookup (returns just the definition text)
definition = get_definition('person', 'Commonwealth')

# Quick modal checks
is_mandatory('must')     # True
is_permissive('may')     # True
```

## Jurisdictions

```python
jurisdictions = db.list_jurisdictions()
# [
#   'Commonwealth',
#   'New South Wales',
#   'Victoria',
#   'Queensland',
#   'Western Australia',
#   'South Australia',
#   'Tasmania',
#   'Australian Capital Territory',
#   'Northern Territory'
# ]
```

## Cross-Jurisdictional Comparison

```python
# Get all definitions of 'person' across jurisdictions
definitions = db.get_all_definitions_for_term('person')

for definition in definitions:
    print(f"{definition.jurisdiction}: {definition.definition}")
```

## Export for NLP

```python
# Export definitions in simple format for NLP processing
nlp_defs = db.export_definitions_for_nlp('Commonwealth')

# Returns: {'person': 'Includes a body...', 'month': 'Calendar month', ...}
```

## Common Patterns

### Pattern 1: Statutory Obligation Analysis

```python
text = "A person must lodge returns within 1 month."

# 1. Extract obligation
obligations = db.extract_obligations(text)
duty = obligations['duties'][0]  # "A person must lodge returns within 1 month."

# 2. Check if corporations bound
includes_corp = db.includes_corporations('person', 'Commonwealth')
# True - corporations must comply

# 3. Calculate deadline
deadline = db.calculate_month('2024-01-15')
# '2024-02-15' - deadline is 1 calendar month from start
```

### Pattern 2: Modal Verb Classification

```python
provision = "The Minister may grant exemptions."

# Classify modal
modal = db.classify_modal('may', 'Commonwealth')

# Determine legal effect
if modal.modal_type == 'PERMISSIVE':
    print("Minister has discretion - not required to grant exemptions")
elif modal.modal_type == 'MANDATORY':
    print("Minister must grant exemptions - no discretion")
```

### Pattern 3: Corporate Applicability

```python
statute = "A person must not engage in misleading conduct."

# Check definition
person_def = db.get_definition('person', 'Commonwealth')

# Check corporate applicability
if db.includes_corporations('person', 'Commonwealth'):
    print("Corporations are bound by this prohibition")
    print(f"Reason: {person_def.definition}")
```

## CLI Usage

```bash
# Look up definition
python -m src.logic.interpretation_acts define person Commonwealth

# Classify modal
python -m src.logic.interpretation_acts modal may Victoria

# Calculate month
python -m src.logic.interpretation_acts month 2024-01-31 NSW

# List jurisdictions
python -m src.logic.interpretation_acts list
```

## NLP Integration Points

### Entity Recognition

```python
# Tag 'person' entities as potentially including corporations
nlp_implications = db.get_nlp_implications()
person_entity = nlp_implications['entity_recognition']['person_entity']

# always_includes: ["individual", "corporation", "body_corporate", "body_politic"]
```

### Modal Verb Tagging

```python
# Pattern: \b(must|shall|is required to|is to)\b → MANDATORY_MODAL
# Pattern: \b(may|is empowered to|has power to)\b → PERMISSIVE_MODAL
# Pattern: \b(must not|shall not|is prohibited from)\b → PROHIBITED_MODAL
```

### Temporal Entity Recognition

```python
# "1 month" → calculate using calendar month rule
# "business day" → exclude weekends and public holidays
# "year" → 12-month period (may not be calendar year)
```

## Automated Reasoning

### Definition Hierarchy

```python
def get_legal_definition(term, act_id, jurisdiction):
    # Priority order:
    # 1. Act-specific definition
    # 2. Interpretation Act definition
    # 3. Common law meaning
    # 4. Dictionary meaning

    act_def = lookup_act_definition(term, act_id)
    if act_def:
        return act_def

    interp_def = db.get_definition(term, jurisdiction)
    if interp_def:
        return interp_def

    return lookup_common_law_or_dictionary(term)
```

### Obligation Extraction Logic

```python
# MUST(agent, action, conditions) → Duty
# MAY(agent, action, conditions) → Power
# MUST_NOT(agent, action, conditions) → Prohibition

obligations = db.extract_obligations(statutory_text)

for duty in obligations['duties']:
    create_compliance_requirement(duty)

for power in obligations['powers']:
    create_discretionary_power(power)

for prohibition in obligations['prohibitions']:
    create_prohibition_rule(prohibition)
```

## Testing

```bash
# Run test suite
pytest tests/test_interpretation_acts.py -v

# Run specific test
pytest tests/test_interpretation_acts.py::TestDefinitionLookup -v

# Run with coverage
pytest tests/test_interpretation_acts.py --cov=src.logic.interpretation_acts
```

## Example Usage Script

```bash
# Run comprehensive examples
python examples/interpretation_acts_usage.py
```

## Documentation

- **Comprehensive Report:** `ACTS_INTERPRETATION_RESEARCH.md`
- **JSON Database:** `data/legislation/acts_interpretation_acts_research.json`
- **API Documentation:** `src/logic/interpretation_acts.py` (docstrings)
- **Test Suite:** `tests/test_interpretation_acts.py`
- **Examples:** `examples/interpretation_acts_usage.py`

## Important Notes

1. **These are DEFAULT definitions** - Act-specific definitions take precedence
2. **All jurisdictions covered** - Commonwealth + 8 states/territories
3. **Uniform principles** - Most key definitions consistent across Australia
4. **Purposive interpretation** - Always consider legislative purpose
5. **Technology neutral** - "Writing" includes electronic documents

## Getting Help

```python
# List all jurisdictions
db.list_jurisdictions()

# Get Act citation
db.get_act_citation('Commonwealth')

# Get Act URL
db.get_act_url('Commonwealth')

# Search definitions
db.search_definitions('corporation')

# Get uniform definitions info
db.get_uniform_definitions()

# Get NLP implications
db.get_nlp_implications()

# Get reasoning rules
db.get_automated_reasoning_rules()
```

## References

- **Commonwealth:** Acts Interpretation Act 1901 (Cth)
- **NSW:** Interpretation Act 1987 (NSW)
- **Victoria:** Interpretation of Legislation Act 1984 (Vic)
- **Queensland:** Acts Interpretation Act 1954 (Qld)
- **WA:** Interpretation Act 1984 (WA)
- **SA:** Acts Interpretation Act 1915 (SA)
- **Tasmania:** Acts Interpretation Act 1931 (Tas)
- **ACT:** Legislation Act 2001 (ACT)
- **NT:** Interpretation Act 1978 (NT)

## Key Case Law

- **Project Blue Sky Inc v ABC** (1998) 194 CLR 355 - Purposive interpretation
- **CIC Insurance v Bankstown FC** (1997) 187 CLR 384 - Avoid inconvenience
- **R v L** (1994) 49 FCR 138 - Interpretation Act application
- **Pearce v Button** (1985) 156 CLR 590 - Context for modal verbs
