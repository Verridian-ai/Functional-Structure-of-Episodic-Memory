# Temporal Tracker Agent - GSW Integration Guide

**Version:** 1.0
**Last Updated:** 2025-11-29
**Related Documents:**
- [Australian Legislative Lifecycle](./AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md)
- [Backend Agents Module](../wiki/Backend-Agents-Module.md)
- [GSW Global Semantic Workspace](../wiki/GSW-Global-Semantic-Workspace.md)

---

## Overview

The **Temporal Tracker Agent** extends the GSW (Global Semantic Workspace) system to track Australian legislation through its complete temporal lifecycle, from bill introduction through repeal.

### Purpose

Traditional legal systems track documents as static entities. The Temporal Tracker Agent introduces **temporal reasoning** by:

1. **Tracking State Transitions**: Bills → Acts, Assent → Commencement, In Force → Repealed
2. **Managing Temporal Anchors**: Key dates (assent, commencement, repeal)
3. **Handling Temporal Queries**: "Was this Act in force on date X?"
4. **Monitoring Lifecycle Events**: Sunset warnings, proclamation requirements, amendment tracking

### Integration Points

The Temporal Tracker integrates with existing GSW components:

```
┌─────────────────────────────────────────────────────────────────┐
│                    GSW ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   Operator   │────────▶│  Reconciler  │                     │
│  │  (Extract)   │         │  (Dedupe)    │                     │
│  └──────────────┘         └──────────────┘                     │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────────────────────────┐                      │
│  │     WORKSPACE (Actor-Centric)        │                      │
│  │  - Actors (Parties, Assets, Dates)   │                      │
│  │  - Roles (Applicant, Judge, etc.)    │                      │
│  │  - States (Married, Separated, etc.) │                      │
│  │  - Verb Phrases (filed, ordered)     │                      │
│  │  - Spatio-Temporal Links             │                      │
│  └──────────────────────────────────────┘                      │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────┐                      │
│  │   TEMPORAL TRACKER AGENT (NEW)       │◀────────────────────┐│
│  │                                       │                     ││
│  │  Input: Legislative Documents        │                     ││
│  │  - Bills (drafts, readings, passage) │                     ││
│  │  - Acts (assent, commencement)       │                     ││
│  │  - Regulations (registration, sunset)│                     ││
│  │                                       │                     ││
│  │  Tracks:                              │                     ││
│  │  - Current State (LegislativeState)  │                     ││
│  │  - State History (transitions)       │                     ││
│  │  - Temporal Anchors (key dates)      │                     ││
│  │  - Relationships (amendments, repeal)│                     ││
│  │                                       │                     ││
│  │  Queries:                             │                     ││
│  │  - In force on date X?               │                     ││
│  │  - Amendments to Act Y?              │                     ││
│  │  - Regulations pending sunset?       │                     ││
│  └──────────────────────────────────────┘                     ││
│         │                                                       ││
│         ▼                                                       ││
│  ┌──────────────────────────────────────┐                      ││
│  │      LEGAL GRAPH (Knowledge)         │                      ││
│  │  - Nodes: Acts, Regulations, Cases   │                      ││
│  │  - Edges: Amends, Repeals, Cites     │──────────────────────┘│
│  │  - Temporal Attributes               │                       │
│  └──────────────────────────────────────┘                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Architecture

### Component Structure

```
src/agents/
├── legislative_temporal_schema.py  # Core schema and tracker
├── temporal_tracker_example.py     # Usage examples
├── gsw_tools.py                    # Existing GSW tools
└── family_law_knowledge.py         # Existing knowledge base

docs/
├── AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md  # Complete reference
└── TEMPORAL_TRACKER_INTEGRATION.md      # This document
```

### Data Flow

```
┌──────────────────┐
│ Legal Document   │ (Bill, Act, Regulation)
│ (Raw Text)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  GSW Operator    │ Extracts:
│  (Extract)       │ - Actors (parties, judges, assets)
│                  │ - Temporal entities (dates)
│                  │ - Events (filed, ordered, assented)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Temporal Tracker │ Creates:
│ (Classify)       │ - LegislativeDocument
│                  │ - Current State
│                  │ - Temporal Anchors
│                  │ - State History
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  GSW Reconciler  │ Deduplicates:
│  (Dedupe)        │ - Same Act, multiple mentions
│                  │ - Compilations vs original
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Workspace       │ Stores:
│  (Persist)       │ - Unified legislative timeline
│                  │ - Actor-centric memory
│                  │ - Temporal relationships
└──────────────────┘
```

---

## Integration Example: Processing a Case Judgment

Let's walk through how the Temporal Tracker integrates when processing a Family Law judgment.

### Scenario

Processing judgment: *Smith v Smith [2024] FamCA 123*

**Text Extract:**
> "The parties were married on 10 June 2010 pursuant to the Marriage Act 1961 (Cth).
> On 15 March 2020, they separated. The applicant filed an application for property
> settlement on 1 July 2023 under s 79 of the Family Law Act 1975 (Cth)..."

### Step 1: GSW Operator Extraction

The **Operator** extracts actors and temporal entities:

```python
from src.gsw.legal_operator import LegalOperator

operator = LegalOperator()
extraction = operator.extract(text)

# Extracted actors:
# - actor_001: "Husband" (person)
# - actor_002: "Wife" (person)
# - actor_003: "Marriage Act 1961 (Cth)" (legislation)
# - actor_004: "Family Law Act 1975 (Cth)" (legislation)
# - actor_005: "10 June 2010" (temporal)
# - actor_006: "15 March 2020" (temporal)
# - actor_007: "1 July 2023" (temporal)

# Extracted verb phrases:
# - verb_001: married(actor_001, actor_002, actor_005)
# - verb_002: separated(actor_001, actor_002, actor_006)
# - verb_003: filed(actor_001, "property application", actor_007)
```

### Step 2: Temporal Tracker Classification

The **Temporal Tracker** identifies legislative mentions and checks their status:

```python
from src.agents.legislative_temporal_schema import (
    TemporalTracker, LegislationQuery,
    LegislativeDocument, Jurisdiction,
    LegislationType, LegislativeState
)

tracker = TemporalTracker()
query = LegislationQuery(tracker)

# Check if Marriage Act 1961 is already tracked
marriage_act = tracker.get_document("MA_1961")

if not marriage_act:
    # Create new legislative document
    marriage_act = LegislativeDocument(
        document_id="MA_1961",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Marriage Act 1961",
        year=1961,
        number=12,
        current_state=LegislativeState.IN_FORCE,
        assent_date=date(1961, 5, 6),
        commencement_date=date(1961, 9, 1),
        is_principal_act=True
    )
    tracker.add_document(marriage_act)

# Check Family Law Act 1975
fla = tracker.get_document("FLA_1975")
if not fla:
    fla = LegislativeDocument(
        document_id="FLA_1975",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Act 1975",
        year=1975,
        number=53,
        current_state=LegislativeState.IN_FORCE,
        assent_date=date(1975, 6, 12),
        commencement_date=date(1976, 1, 5),
        is_principal_act=True
    )
    tracker.add_document(fla)
```

### Step 3: Temporal Validation

Validate that legislation was in force when events occurred:

```python
# Was Marriage Act 1961 in force on marriage date (10 June 2010)?
marriage_date = date(2010, 6, 10)
was_in_force = marriage_act.is_in_force_on(marriage_date)

print(f"Marriage Act 1961 in force on {marriage_date}: {was_in_force}")
# Output: True

# Was FLA 1975 s 79 in force on application date (1 July 2023)?
application_date = date(2023, 7, 1)
was_in_force = fla.is_in_force_on(application_date)

print(f"FLA 1975 in force on {application_date}: {was_in_force}")
# Output: True

# Find which compilation was current on application date
compilation = fla.get_compilation_on_date(application_date)
if compilation:
    print(f"Compilation No. {compilation.compilation_number} current on {application_date}")
    print(f"Incorporated amendments: {len(compilation.incorporates_amendments)}")
```

### Step 4: GSW Reconciler Integration

Link legislative actors to workspace:

```python
from src.gsw.legal_reconciler import LegalReconciler

reconciler = LegalReconciler()

# Add legislative documents to workspace
workspace.add_actor(
    actor_id="actor_003",
    name="Marriage Act 1961 (Cth)",
    actor_type="legislation",
    metadata={
        "temporal_tracker_id": "MA_1961",
        "in_force": marriage_act.current_state == LegislativeState.IN_FORCE,
        "commencement_date": str(marriage_act.commencement_date)
    }
)

workspace.add_actor(
    actor_id="actor_004",
    name="Family Law Act 1975 (Cth)",
    actor_type="legislation",
    metadata={
        "temporal_tracker_id": "FLA_1975",
        "in_force": fla.current_state == LegislativeState.IN_FORCE,
        "current_compilation": fla.current_compilation.compilation_number,
        "amended_by": fla.amended_by
    }
)

# Create temporal links
workspace.add_spatio_temporal_link(
    linked_entities=["actor_001", "actor_002", "actor_003", "actor_005"],
    tag_type="temporal",
    tag_value="2010-06-10",
    context="Marriage under Marriage Act 1961"
)
```

---

## Use Cases

### Use Case 1: Validating Legislative Authority

**Scenario:** Check if a section was in force when an order was made.

```python
def validate_legislative_authority(
    act_id: str,
    section: str,
    order_date: date,
    tracker: TemporalTracker
) -> dict:
    """
    Validate that a section was in force when referenced.

    Returns:
        dict with validation results
    """
    doc = tracker.get_document(act_id)

    if not doc:
        return {"valid": False, "reason": "Act not found"}

    # Check if Act was in force
    if not doc.is_in_force_on(order_date):
        return {
            "valid": False,
            "reason": f"Act not in force on {order_date}",
            "act_state": doc.get_state_on_date(order_date)
        }

    # Check if section had commenced
    if doc.section_commencements:
        for section_comm in doc.section_commencements:
            if section in section_comm.section_range:
                if not section_comm.commencement_date or \
                   section_comm.commencement_date > order_date:
                    return {
                        "valid": False,
                        "reason": f"Section {section} not yet commenced on {order_date}",
                        "commencement_date": section_comm.commencement_date
                    }

    return {
        "valid": True,
        "compilation": doc.get_compilation_on_date(order_date),
        "state": doc.get_state_on_date(order_date)
    }

# Example usage
result = validate_legislative_authority(
    act_id="FLA_1975",
    section="79",
    order_date=date(2023, 7, 1),
    tracker=tracker
)

if result["valid"]:
    print(f"✓ Section 79 was in force on 2023-07-01")
    print(f"  Compilation: No. {result['compilation'].compilation_number}")
else:
    print(f"✗ Invalid: {result['reason']}")
```

### Use Case 2: Amendment Impact Analysis

**Scenario:** Determine which version of an Act applies to a case.

```python
def get_applicable_law_version(
    principal_act_id: str,
    reference_date: date,
    tracker: TemporalTracker,
    query: LegislationQuery
) -> dict:
    """
    Get the version of law applicable on a specific date.

    Returns:
        dict with applicable version and amendments
    """
    principal = tracker.get_document(principal_act_id)

    if not principal:
        return {"error": "Act not found"}

    # Get compilation current on date
    compilation = principal.get_compilation_on_date(reference_date)

    # Get amendments that had taken effect by reference date
    amendments = query.get_amendments_to_act(principal_act_id)
    applicable_amendments = [
        amend for amend in amendments
        if amend.commencement_date and amend.commencement_date <= reference_date
    ]

    return {
        "principal_act": principal.title,
        "reference_date": reference_date,
        "compilation": {
            "number": compilation.compilation_number,
            "as_at_date": compilation.as_at_date
        } if compilation else None,
        "amendments_count": len(applicable_amendments),
        "amendments": [
            {
                "title": amend.title,
                "commencement": amend.commencement_date,
                "items_count": len(amend.amendments)
            }
            for amend in applicable_amendments
        ]
    }

# Example usage
version_info = get_applicable_law_version(
    principal_act_id="FLA_1975",
    reference_date=date(2023, 7, 1),
    tracker=tracker,
    query=query
)

print(f"Law applicable on {version_info['reference_date']}:")
print(f"  Compilation No. {version_info['compilation']['number']}")
print(f"  Incorporated {version_info['amendments_count']} amendments")
```

### Use Case 3: Monitoring Sunset Compliance

**Scenario:** Alert when regulations are approaching sunset.

```python
def generate_sunset_report(
    tracker: TemporalTracker,
    query: LegislationQuery,
    months_ahead: int = 18
) -> dict:
    """
    Generate report of regulations approaching sunset.

    Returns:
        dict with pending sunsets categorized by urgency
    """
    pending = query.get_regulations_pending_sunset(months_ahead=months_ahead)

    # Categorize by urgency
    urgent = []      # < 6 months
    warning = []     # 6-12 months
    advisory = []    # 12-18 months

    today = date.today()

    for reg in pending:
        days_until = (reg.sunset_date - today).days
        months_until = days_until / 30

        reg_info = {
            "title": reg.title,
            "registration_date": reg.registration_date,
            "sunset_date": reg.sunset_date,
            "days_until_sunset": days_until,
            "enabling_act": reg.enabling_act_id
        }

        if months_until < 6:
            urgent.append(reg_info)
        elif months_until < 12:
            warning.append(reg_info)
        else:
            advisory.append(reg_info)

    return {
        "report_date": today,
        "total_pending": len(pending),
        "urgent": urgent,
        "warning": warning,
        "advisory": advisory
    }

# Example usage
report = generate_sunset_report(tracker, query, months_ahead=18)

print(f"\n=== SUNSET COMPLIANCE REPORT ({report['report_date']}) ===")
print(f"Total regulations pending sunset: {report['total_pending']}\n")

print(f"URGENT (<6 months): {len(report['urgent'])}")
for reg in report['urgent']:
    print(f"  ⚠️  {reg['title']}")
    print(f"      Sunsets: {reg['sunset_date']} ({reg['days_until_sunset']} days)")

print(f"\nWARNING (6-12 months): {len(report['warning'])}")
for reg in report['warning']:
    print(f"  ⚡ {reg['title']}")
    print(f"      Sunsets: {reg['sunset_date']}")
```

### Use Case 4: Legislative Timeline Visualization

**Scenario:** Generate timeline of legislative events for a document.

```python
def generate_legislative_timeline(
    document_id: str,
    tracker: TemporalTracker
) -> list:
    """
    Generate chronological timeline of legislative events.

    Returns:
        list of events sorted by date
    """
    doc = tracker.get_document(document_id)

    if not doc:
        return []

    timeline = []

    # Add temporal anchors
    for anchor in doc.temporal_anchors:
        timeline.append({
            "date": anchor.date,
            "event_type": anchor.event_type,
            "description": anchor.description,
            "source": anchor.source_document,
            "category": "anchor"
        })

    # Add state transitions
    for transition in doc.state_history:
        timeline.append({
            "date": transition.transition_date,
            "event_type": "state_change",
            "description": f"{transition.from_state} → {transition.to_state}",
            "reason": transition.reason,
            "category": "transition"
        })

    # Add key dates
    if doc.introduced_date:
        timeline.append({
            "date": doc.introduced_date,
            "event_type": "introduction",
            "description": "Bill introduced to Parliament",
            "category": "lifecycle"
        })

    if doc.assent_date:
        timeline.append({
            "date": doc.assent_date,
            "event_type": "assent",
            "description": "Royal Assent received",
            "category": "lifecycle"
        })

    if doc.commencement_date:
        timeline.append({
            "date": doc.commencement_date,
            "event_type": "commencement",
            "description": "Act commenced (in force)",
            "category": "lifecycle"
        })

    if doc.repeal_date:
        timeline.append({
            "date": doc.repeal_date,
            "event_type": "repeal",
            "description": f"Repealed ({doc.repeal_type})",
            "category": "lifecycle"
        })

    # Sort by date
    timeline.sort(key=lambda e: e["date"])

    return timeline

# Example usage
timeline = generate_legislative_timeline("FLA_1975", tracker)

print(f"\n=== LEGISLATIVE TIMELINE: Family Law Act 1975 ===\n")
for event in timeline:
    print(f"{event['date']} - {event['description']}")
    if event.get('reason'):
        print(f"             Reason: {event['reason']}")
```

---

## API Reference

### Core Classes

#### `LegislativeDocument`

Represents a legislative document with full temporal tracking.

```python
from src.agents.legislative_temporal_schema import LegislativeDocument

doc = LegislativeDocument(
    document_id="FLA_2024_045",
    jurisdiction=Jurisdiction.COMMONWEALTH,
    document_type=LegislationType.ACT,
    title="Family Law Amendment Act 2024",
    year=2024,
    current_state=LegislativeState.IN_FORCE
)
```

**Key Methods:**
- `add_state_change(new_state, reason)` - Record state transition
- `is_in_force_on(date)` - Check if in force on date
- `get_state_on_date(date)` - Get historical state
- `calculate_28_day_commencement()` - Calculate automatic commencement
- `calculate_sunset_date()` - Calculate sunset for regulations

#### `TemporalTracker`

Manages documents and state transitions.

```python
from src.agents.legislative_temporal_schema import TemporalTracker

tracker = TemporalTracker()
tracker.add_document(doc)
```

**Key Methods:**
- `add_document(doc)` - Add document to tracker
- `get_document(document_id)` - Retrieve document
- `transition_bill_to_assented(bill_id, assent_date)` - Royal Assent
- `determine_commencement_state(act_id)` - Set commencement state
- `record_proclamation(act_id, ...)` - Record proclamation
- `record_amendment(principal_id, amending_act)` - Link amendment
- `record_repeal(act_id, ...)` - Record repeal
- `check_sunset(regulation_id)` - Check sunset status

#### `LegislationQuery`

Query documents by temporal criteria.

```python
from src.agents.legislative_temporal_schema import LegislationQuery

query = LegislationQuery(tracker)
```

**Key Methods:**
- `get_in_force_on_date(date, jurisdiction, type)` - Get in-force documents
- `get_amendments_to_act(principal_id)` - Get amendments
- `get_acts_repealed_by(repealing_id)` - Get repealed acts
- `get_bills_in_parliament(jurisdiction)` - Get active bills
- `get_regulations_pending_sunset(months)` - Get pending sunsets
- `get_documents_by_state(state, jurisdiction)` - Get by state

---

## Integration with Existing Agents

### Family Law Knowledge Agent

Enhance the existing Family Law knowledge agent with temporal tracking:

```python
# src/agents/family_law_knowledge.py

from src.agents.legislative_temporal_schema import (
    TemporalTracker, LegislationQuery,
    LegislativeDocument, LegislativeState
)

class FamilyLawKnowledgeAgent:
    """Enhanced with temporal tracking"""

    def __init__(self):
        self.knowledge_base = {...}  # Existing knowledge
        self.temporal_tracker = TemporalTracker()
        self.query = LegislationQuery(self.temporal_tracker)

        # Initialize core legislation
        self._init_core_legislation()

    def _init_core_legislation(self):
        """Initialize core Family Law Acts"""

        # Family Law Act 1975
        fla = LegislativeDocument(
            document_id="FLA_1975",
            jurisdiction=Jurisdiction.COMMONWEALTH,
            document_type=LegislationType.ACT,
            title="Family Law Act 1975",
            year=1975,
            number=53,
            current_state=LegislativeState.IN_FORCE,
            is_principal_act=True,
            assent_date=date(1975, 6, 12),
            commencement_date=date(1976, 1, 5),
        )
        self.temporal_tracker.add_document(fla)

        # Add more acts...

    def validate_section_authority(
        self,
        act_id: str,
        section: str,
        reference_date: date
    ) -> bool:
        """Check if section was in force on date"""
        doc = self.temporal_tracker.get_document(act_id)
        return doc and doc.is_in_force_on(reference_date)

    def get_applicable_amendments(
        self,
        principal_act_id: str,
        as_at_date: date
    ) -> list:
        """Get amendments applicable on date"""
        amendments = self.query.get_amendments_to_act(principal_act_id)
        return [
            a for a in amendments
            if a.commencement_date and a.commencement_date <= as_at_date
        ]
```

---

## Testing

### Unit Tests

```python
# tests/test_temporal_tracker.py

import pytest
from datetime import date, timedelta
from src.agents.legislative_temporal_schema import (
    LegislativeDocument, TemporalTracker,
    LegislativeState, CommencementMethod
)

def test_28_day_commencement():
    """Test automatic 28-day commencement calculation"""
    doc = LegislativeDocument(
        document_id="TEST_ACT",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Test Act",
        year=2024,
        current_state=LegislativeState.ASSENTED,
        assent_date=date(2024, 1, 1)
    )

    expected = date(2024, 1, 1) + timedelta(days=28)
    assert doc.calculate_28_day_commencement() == expected

def test_in_force_query():
    """Test in-force date query"""
    doc = LegislativeDocument(
        document_id="TEST_ACT",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Test Act",
        year=2024,
        current_state=LegislativeState.IN_FORCE,
        commencement_date=date(2024, 1, 1),
        repeal_date=date(2024, 12, 31),
        is_repealed=True
    )

    assert doc.is_in_force_on(date(2024, 6, 1)) == True
    assert doc.is_in_force_on(date(2023, 12, 31)) == False
    assert doc.is_in_force_on(date(2025, 1, 1)) == False

def test_sunset_calculation():
    """Test 10-year sunset calculation"""
    doc = LegislativeDocument(
        document_id="TEST_REG",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.REGULATION,
        title="Test Regulation",
        year=2024,
        current_state=LegislativeState.IN_FORCE,
        registration_date=date(2024, 3, 15)
    )

    sunset = doc.calculate_sunset_date()
    # Should be 10 years later, nearest 1 Apr or 1 Oct
    assert sunset.year == 2034
    assert sunset.month in [4, 10]
    assert sunset.day == 1
```

---

## Performance Considerations

### Caching

Implement caching for frequently accessed documents:

```python
from functools import lru_cache

class TemporalTracker:
    @lru_cache(maxsize=1000)
    def get_document_cached(self, document_id: str):
        """Cached document retrieval"""
        return self.documents.get(document_id)
```

### Indexing

Create indexes for common queries:

```python
class TemporalTracker:
    def __init__(self):
        self.documents = {}
        self.indexes = {
            "by_year": {},        # year -> [doc_ids]
            "by_state": {},       # state -> [doc_ids]
            "by_jurisdiction": {} # jurisdiction -> [doc_ids]
        }

    def add_document(self, doc):
        self.documents[doc.document_id] = doc

        # Update indexes
        self.indexes["by_year"].setdefault(doc.year, []).append(doc.document_id)
        self.indexes["by_state"].setdefault(doc.current_state, []).append(doc.document_id)
        self.indexes["by_jurisdiction"].setdefault(doc.jurisdiction, []).append(doc.document_id)
```

---

## Future Enhancements

### 1. State/Territory Variations

Extend schema to handle state-specific processes:

```python
class StateVariations:
    """Handle state-specific legislative processes"""

    NSW_COMMENCEMENT_RULES = {
        "default_days": 28,
        "interpretation_act": "Interpretation Act 1987 (NSW)"
    }

    VIC_COMMENCEMENT_RULES = {
        "default_days": 28,
        "interpretation_act": "Interpretation of Legislation Act 1984 (Vic)"
    }
```

### 2. Automated Monitoring

Implement automated monitoring of Federal Register:

```python
class FederalRegisterMonitor:
    """Monitor Federal Register for updates"""

    def check_for_updates(self):
        """Check for new Acts, proclamations, sunsets"""
        pass

    def notify_sunset_pending(self):
        """Alert when regulations approach sunset"""
        pass
```

### 3. Visual Timeline

Generate visual timelines for documents:

```python
def generate_visual_timeline(doc: LegislativeDocument) -> str:
    """Generate ASCII timeline"""
    # Implementation would create visual representation
    pass
```

---

## Conclusion

The Temporal Tracker Agent extends the GSW system with sophisticated temporal reasoning for Australian legislation. By tracking state transitions, temporal anchors, and lifecycle events, it enables powerful queries like:

- "Was this section in force when the order was made?"
- "Which amendments applied on this date?"
- "Which regulations are approaching sunset?"

This integration maintains the actor-centric philosophy of GSW while adding critical temporal intelligence for legal reasoning.

---

## References

- [Australian Legislative Lifecycle](./AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md) - Complete reference
- [Legislative Temporal Schema](../src/agents/legislative_temporal_schema.py) - Implementation
- [Usage Examples](../src/agents/temporal_tracker_example.py) - Code examples
- [Backend Agents Module](../wiki/Backend-Agents-Module.md) - Agent architecture
- [GSW Global Semantic Workspace](../wiki/GSW-Global-Semantic-Workspace.md) - GSW overview
