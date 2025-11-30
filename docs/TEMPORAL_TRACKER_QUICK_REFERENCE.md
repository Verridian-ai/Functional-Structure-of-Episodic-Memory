# Temporal Tracker Agent - Quick Reference Card

**Version:** 1.0 | **Last Updated:** 2025-11-29

---

## 1-Minute Overview

The **Temporal Tracker Agent** tracks Australian legislation through its complete lifecycle from bill → act → repeal.

**Key Capabilities:**
- Track 40+ legislative states (drafted → introduced → assented → in force → repealed)
- Manage temporal anchors (key dates: assent, commencement, repeal)
- Query: "Was Act X in force on date Y?"
- Monitor: Sunset warnings, proclamation requirements, amendment tracking

---

## Quick Start

```python
from src.agents.legislative_temporal_schema import (
    LegislativeDocument, TemporalTracker, LegislationQuery,
    LegislativeState, Jurisdiction, LegislationType
)
from datetime import date

# Create tracker
tracker = TemporalTracker()
query = LegislationQuery(tracker)

# Add an Act
act = LegislativeDocument(
    document_id="FLA_1975",
    jurisdiction=Jurisdiction.COMMONWEALTH,
    document_type=LegislationType.ACT,
    title="Family Law Act 1975",
    year=1975,
    current_state=LegislativeState.IN_FORCE,
    assent_date=date(1975, 6, 12),
    commencement_date=date(1976, 1, 5)
)
tracker.add_document(act)

# Query: Was it in force on a date?
in_force = act.is_in_force_on(date(2023, 7, 1))
print(f"In force: {in_force}")  # True
```

---

## 5 Core Concepts

### 1. Legislative States

**Bills:** `drafted` → `introduced` → `debated` → `passed_both_houses` → `assented`

**Acts:** `assented` → `pending_28_day` / `awaiting_proclamation` → `in_force` → `repealed`

**Regulations:** `registered` → `tabled` → `in_disallowance_period` → `in_force` → `sunsetted`

### 2. Commencement Methods

| Method | Description | Example |
|--------|-------------|---------|
| `on_assent` | Commences immediately on Royal Assent | `commencement_date = assent_date` |
| `28_days` | Auto-commences 28 days after assent | `assent_date + 28 days` |
| `proclamation` | Minister proclaims commencement | Wait for Gazette notice |
| `fixed_date` | Specific calendar date | `1 July 2025` |
| `event_triggered` | Upon occurrence of event | `When treaty ratified` |
| `partial` | Different sections different methods | See `section_commencements[]` |

### 3. Temporal Anchors

Key dates in lifecycle:
- **Introduction:** Bill first reading
- **Royal Assent:** Governor-General signs
- **Commencement:** Act becomes law (≠ assent!)
- **Proclamation:** Gazette notice for commencement
- **Repeal:** Act ceases to have effect

### 4. Amendment Tracking

**Principal Act:** Original Act being amended (e.g., Family Law Act 1975)

**Amending Act:** Act that modifies principal (e.g., FLA Amendment Act 2024)

**Amendment Types:**
- `OMIT` - Delete text
- `SUBSTITUTE` - Replace text
- `INSERT` - Add new text
- `REPEAL` - Remove entire provision

**Compilations:** "Cut and paste" versions showing Act as amended

### 5. Sunsetting (Regulations Only)

**Rule:** Regulations automatically sunset 10 years after registration

**Sunset Dates:** 1 April or 1 October (nearest after 10 years)

**Warning:** Sunsetting list tabled 18 months before sunset

**Options:**
- Remake regulation (if still needed)
- Let it sunset (if redundant)

---

## Common Queries

```python
# Get all Acts in force on a date
acts = query.get_in_force_on_date(
    check_date=date(2023, 7, 1),
    jurisdiction=Jurisdiction.COMMONWEALTH,
    document_type=LegislationType.ACT
)

# Get amendments to an Act
amendments = query.get_amendments_to_act("FLA_1975")

# Get bills currently in Parliament
bills = query.get_bills_in_parliament(Jurisdiction.COMMONWEALTH)

# Get regulations pending sunset (next 18 months)
pending_sunset = query.get_regulations_pending_sunset(months_ahead=18)

# Get documents by state
in_force = query.get_documents_by_state(
    LegislativeState.IN_FORCE,
    Jurisdiction.COMMONWEALTH
)
```

---

## Common Operations

### Track Bill to Act

```python
# 1. Bill introduced
bill = LegislativeDocument(
    document_id="BILL_2024_045",
    document_type=LegislationType.BILL,
    current_state=LegislativeState.INTRODUCED,
    introduced_date=date(2024, 4, 10)
)

# 2. Bill passed both houses
bill.add_state_change(
    LegislativeState.PASSED_BOTH_HOUSES,
    "Passed Senate"
)

# 3. Royal Assent
tracker.transition_bill_to_assented(
    bill_id="BILL_2024_045",
    assent_date=date(2024, 6, 20)
)

# 4. Determine commencement
bill.commencement_method = CommencementMethod.AUTOMATIC_28_DAYS
tracker.determine_commencement_state("BILL_2024_045")

# 5. Check state
print(bill.current_state)  # PENDING_28_DAY
```

### Record Proclamation

```python
tracker.record_proclamation(
    act_id="ACT_2024_045",
    proclamation_date=date(2024, 8, 15),
    proclaimed_commencement_date=date(2024, 9, 1),
    gazette_reference="C2024G00156"
)
```

### Record Amendment

```python
# Amending Act amends Principal Act
tracker.record_amendment(
    principal_act_id="FLA_1975",
    amending_act=amending_act_doc
)

# Creates new compilation
print(principal.current_compilation.compilation_number)
```

### Record Repeal

```python
tracker.record_repeal(
    act_id="OLD_ACT",
    repeal_date=date(2024, 7, 1),
    repealing_act_id="REPEAL_ACT_2024",
    repeal_type=RepealType.EXPRESS
)
```

### Check Sunset

```python
# Check if regulation should sunset
tracker.check_sunset(
    regulation_id="REG_2024",
    current_date=date.today()
)

# Auto-transitions to SUNSET_PENDING or SUNSETTED
```

---

## Key Methods

### LegislativeDocument

| Method | Returns | Description |
|--------|---------|-------------|
| `add_state_change(new_state, reason)` | `None` | Record state transition |
| `is_in_force_on(date)` | `bool` | Check if in force on date |
| `get_state_on_date(date)` | `LegislativeState` | Get historical state |
| `get_compilation_on_date(date)` | `Compilation` | Get compilation current on date |
| `calculate_28_day_commencement()` | `date` | Calculate auto-commencement |
| `calculate_sunset_date()` | `date` | Calculate 10-year sunset |
| `add_temporal_anchor(...)` | `None` | Add key date event |

### TemporalTracker

| Method | Returns | Description |
|--------|---------|-------------|
| `add_document(doc)` | `None` | Add document to tracker |
| `get_document(id)` | `LegislativeDocument` | Retrieve document |
| `transition_bill_to_assented(...)` | `LegislativeDocument` | Royal Assent transition |
| `determine_commencement_state(id)` | `LegislativeDocument` | Set commencement state |
| `record_proclamation(...)` | `LegislativeDocument` | Record proclamation |
| `record_amendment(...)` | `LegislativeDocument` | Link amendment |
| `record_repeal(...)` | `LegislativeDocument` | Record repeal |
| `check_sunset(id, date)` | `LegislativeDocument` | Check sunset status |

### LegislationQuery

| Method | Returns | Description |
|--------|---------|-------------|
| `get_in_force_on_date(date, ...)` | `List[LegislativeDocument]` | Get in-force documents |
| `get_amendments_to_act(id)` | `List[LegislativeDocument]` | Get amendments |
| `get_acts_repealed_by(id)` | `List[LegislativeDocument]` | Get repealed acts |
| `get_bills_in_parliament(juris)` | `List[LegislativeDocument]` | Get active bills |
| `get_regulations_pending_sunset(m)` | `List[LegislativeDocument]` | Get pending sunsets |
| `get_documents_by_state(state, ...)` | `List[LegislativeDocument]` | Get by state |

---

## State Machine (Simplified)

```
BILLS:
  drafted → introduced → debated → passed_both_houses → assented

ACTS (Post-Assent):
  assented → [pending_28_day | awaiting_proclamation] → in_force → repealed

REGULATIONS:
  registered → tabled → in_disallowance_period → in_force → sunsetted
```

---

## Important Rules

### Assent ≠ Commencement

**An Act receiving Royal Assent does NOT mean it's in force!**

- Check `commencement_date`, not just `assent_date`
- Section 2 specifies commencement method
- Acts can be assented but awaiting proclamation indefinitely

### 28-Day Default (Commonwealth)

If Section 2 says nothing, Act auto-commences 28 days after assent (Acts Interpretation Act 1901 s 3A).

Exception: Does not apply if Act alters Constitution.

### Partial Commencement

Different sections can commence at different times:
- Sections 1-3: On assent
- Schedule 1: Fixed date
- Schedule 2: By proclamation

Check `section_commencements[]` array.

### Sunsetting (10 Years)

Regulations sunset 10 years after registration (Legislation Act 2003 s 50).

Sunset dates: **1 April** or **1 October**

Warning: 18 months before sunset

Exemptions:
- Savings/transitional provisions
- International obligations
- Ministerial directions
- Appropriation Act instruments

### Compilations vs Originals

**Original Act:** As passed and assented (historical)

**Compilation:** Act as currently amended (what's in force NOW)

Always use latest compilation for current law.

---

## Validation Checklist

When validating legislative authority:

- [ ] Was Act in force on the date in question?
- [ ] Was the specific section commenced?
- [ ] Which compilation was current?
- [ ] Had any amendments taken effect?
- [ ] Had any repeal occurred?

```python
def validate(act_id, section, date, tracker):
    doc = tracker.get_document(act_id)

    # Check Act in force
    if not doc.is_in_force_on(date):
        return False

    # Check section commenced
    for sec_comm in doc.section_commencements:
        if section in sec_comm.section_range:
            if not sec_comm.commencement_date or \
               sec_comm.commencement_date > date:
                return False

    # Check compilation
    compilation = doc.get_compilation_on_date(date)
    # Use this compilation for text

    return True
```

---

## Data Structure

```python
LegislativeDocument {
    # Identity
    document_id: str
    jurisdiction: Jurisdiction
    document_type: LegislationType
    title: str
    year: int

    # Current State
    current_state: LegislativeState
    state_history: List[StateTransition]

    # Bill Stage
    introduced_date: date
    passed_both_houses_date: date

    # Act Creation
    assent_date: date
    commencement_method: CommencementMethod
    commencement_date: date
    section_commencements: List[SectionCommencement]

    # Amendments
    is_principal_act: bool
    amended_by: List[str]  # Act IDs
    compilations: List[Compilation]

    # Termination
    is_repealed: bool
    repeal_date: date
    repeal_type: RepealType

    # Subordinate Legislation
    enabling_act_id: str
    registration_date: date
    sunset_date: date

    # Temporal
    temporal_anchors: List[TemporalAnchor]
}
```

---

## Common Pitfalls

### 1. Confusing Assent and Commencement

**Wrong:**
```python
if act.assent_date:
    print("Act is in force")  # NO! May not be commenced yet
```

**Right:**
```python
if act.is_in_force_on(date.today()):
    print("Act is in force")
```

### 2. Ignoring Partial Commencement

**Wrong:**
```python
if act.commencement_date:
    # Assume entire Act in force
```

**Right:**
```python
if act.commencement_method == CommencementMethod.PARTIAL:
    # Check section_commencements[]
    for section in act.section_commencements:
        if my_section in section.section_range:
            # Check section.commencement_date
```

### 3. Not Checking Compilations

**Wrong:**
```python
# Using original Act text from 1975
```

**Right:**
```python
compilation = act.get_compilation_on_date(reference_date)
# Use compilation text (includes all amendments)
```

### 4. Forgetting Sunset

**Wrong:**
```python
if regulation.current_state == LegislativeState.IN_FORCE:
    # Assume will stay in force
```

**Right:**
```python
if regulation.sunset_date:
    days_until = (regulation.sunset_date - date.today()).days
    if days_until < 180:  # 6 months
        warn("Regulation approaching sunset!")
```

---

## File Locations

```
docs/
├── AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md    # Complete reference (1450 lines)
├── TEMPORAL_TRACKER_INTEGRATION.md        # Integration guide (907 lines)
└── TEMPORAL_TRACKER_QUICK_REFERENCE.md    # This file

src/agents/
├── legislative_temporal_schema.py         # Core implementation (943 lines)
└── temporal_tracker_example.py            # Usage examples (610 lines)
```

---

## Getting Help

**Full Documentation:** `docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md`

**Integration Guide:** `docs/TEMPORAL_TRACKER_INTEGRATION.md`

**Code Examples:** `src/agents/temporal_tracker_example.py`

**Schema Reference:** `src/agents/legislative_temporal_schema.py`

---

## Enumerations Reference

### LegislativeState (40+ states)

**Bills:**
- `DRAFTED`, `INTRODUCED`, `DEBATED`, `IN_COMMITTEE`, `UNDER_AMENDMENT`
- `PASSED_HOUSE`, `IN_SENATE`, `SENATE_AMENDED`, `PASSED_BOTH_HOUSES`
- `REJECTED`, `LAPSED`, `WITHDRAWN`

**Acts:**
- `ASSENTED`, `PENDING_28_DAY`, `AWAITING_PROCLAMATION`, `PROCLAIMED`
- `SCHEDULED`, `AWAITING_TRIGGER`, `IN_FORCE`, `PARTIALLY_IN_FORCE`
- `SUSPENDED`, `SPENT`, `SUPERSEDED`, `REPEALED`

**Regulations:**
- `REGISTERED`, `TABLED`, `IN_DISALLOWANCE_PERIOD`
- `SUNSET_PENDING`, `SUNSETTED`, `DISALLOWED`, `REMADE`

### CommencementMethod

- `ON_ASSENT` - Immediate
- `AUTOMATIC_28_DAYS` - Default rule
- `PROCLAMATION` - Minister decides
- `FIXED_DATE` - Specific date
- `RETROSPECTIVE` - Backdated
- `EVENT_TRIGGERED` - Upon event
- `PARTIAL` - Different sections different methods

### AmendmentType

- `OMIT` - Delete text
- `SUBSTITUTE` - Replace text
- `INSERT` - Add new text
- `REPEAL` - Remove provision
- `RENUMBER` - Change numbering
- `RELOCATE` - Move provision

### RepealType

- `EXPRESS` - Explicitly repealed by another Act
- `IMPLIED` - Implicitly replaced (rare)
- `SUNSET` - Automatic 10-year sunset
- `DISALLOWANCE` - Parliament rejected

### Jurisdiction

- `COMMONWEALTH` - Federal
- `NSW`, `VICTORIA`, `QUEENSLAND`, `SOUTH_AUSTRALIA`, `WESTERN_AUSTRALIA`, `TASMANIA`
- `ACT`, `NORTHERN_TERRITORY`

---

**End of Quick Reference**

For complete details, see `docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md`
