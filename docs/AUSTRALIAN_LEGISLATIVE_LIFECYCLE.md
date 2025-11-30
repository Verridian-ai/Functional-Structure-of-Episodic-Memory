# Australian Legislative Lifecycle for Temporal Tracker Agent

**Document Version:** 1.0
**Last Updated:** 2025-11-29
**Purpose:** Complete reference for tracking Australian legislation temporal states and transitions

---

## Table of Contents

1. [Overview](#overview)
2. [Stage 1: Bill Stage](#stage-1-bill-stage)
3. [Stage 2: Act Creation](#stage-2-act-creation)
4. [Stage 3: Amendment Lifecycle](#stage-3-amendment-lifecycle)
5. [Stage 4: Termination](#stage-4-termination)
6. [Stage 5: Subordinate Legislation](#stage-5-subordinate-legislation)
7. [Temporal State Machine](#temporal-state-machine)
8. [Implementation Guide](#implementation-guide)
9. [Sources](#sources)

---

## Overview

Australian legislation follows a complex lifecycle from initial proposal through termination. The Temporal Tracker Agent must understand:

- **Temporal States**: Current status of a legislative document
- **Temporal Transitions**: Events that move documents between states
- **Temporal Anchors**: Key dates (introduction, assent, commencement, repeal)
- **Jurisdictional Variations**: Federal vs State/Territory differences

### Key Jurisdictions

- **Commonwealth (Federal)**: Parliament of Australia (House of Representatives + Senate)
- **States**: NSW, Victoria, Queensland, South Australia, Western Australia, Tasmania
- **Territories**: ACT, Northern Territory

---

## Stage 1: Bill Stage

A **Bill** is a proposed law before it receives Royal Assent. Bills progress through multiple readings and debates.

### 1.1 Bill Types

#### Government Bills
- **Definition**: Bills introduced by government ministers
- **Source**: Drafted by public servants on behalf of ministers
- **Success Rate**: ~90% passage rate
- **Volume**: ~200 bills per year in federal Parliament
- **Who Can Introduce**: Ministers in either House

#### Private Member Bills / Private Senator Bills
- **Definition**: Bills introduced by non-ministerial MPs/Senators
- **Success Rate**: Extremely rare (14 successful between 1998-2022)
- **Restrictions**: Cannot introduce money or taxation bills

### 1.2 Parliamentary Process

#### In the House of Representatives

**First Reading**
- **Event**: Bill is introduced to the House
- **Action**: Title read, no debate
- **Temporal Marker**: `bill.introduced_date`
- **State Transition**: `null → introduced`

**Second Reading**
- **Event**: Members debate and vote on the main idea
- **Duration**: Can take days/weeks
- **Temporal Marker**: `bill.second_reading_date`
- **State Transition**: `introduced → debated`
- **Notes**: Explanatory Memorandum published

**House Committee Stage (Optional)**
- **Event**: Public inquiry into the bill
- **Action**: Committee reports back to House
- **Temporal Marker**: `bill.committee_referral_date`, `bill.committee_report_date`
- **State Transition**: `debated → in_committee`

**Consideration in Detail (Optional)**
- **Event**: Members discuss bill clause-by-clause
- **Action**: Amendments proposed and voted on
- **Temporal Marker**: `bill.amendment_proposed_date[]`
- **State Transition**: `debated → under_amendment`

**Third Reading**
- **Event**: Members vote on final form
- **Action**: Final vote in House
- **Temporal Marker**: `bill.third_reading_date`
- **State Transition**: `debated → passed_house`

#### In the Senate

**Senate Referral (Can occur during House process)**
- **Event**: Senate committee may inquire while bill is in House
- **Action**: Parallel review process
- **Temporal Marker**: `bill.senate_referral_date`
- **State**: `parallel_senate_review`

**Senate Passage**
- **Event**: Bill must pass Senate in identical form
- **Stages**: Same as House (1st, 2nd, 3rd reading)
- **Temporal Marker**: `bill.passed_senate_date`
- **State Transition**: `passed_house → passed_both_houses`

**Senate Amendments**
- **Event**: Senate proposes changes
- **Action**: Bill returns to House for consideration
- **Temporal Marker**: `bill.senate_amendment_date`
- **State Transition**: `passed_house → senate_amended → returned_to_house`

### 1.3 Constitutional Restrictions

#### Money and Taxation Bills
- **Rule**: Must originate in House of Representatives (Constitution s 53)
- **Senate Powers**: Can only approve, reject, or defer (cannot amend)
- **State Marker**: `bill.is_money_bill = true`

#### Appropriation Bills
- **Rule**: Authorise government expenditure
- **Senate Powers**: Cannot introduce or amend
- **State Marker**: `bill.is_appropriation_bill = true`

### 1.4 Temporal States for Bills

```
States:
- drafted (pre-introduction)
- introduced (1st reading)
- debated (2nd reading)
- in_committee (committee review)
- under_amendment (consideration in detail)
- passed_house (passed House of Reps)
- in_senate (transmitted to Senate)
- passed_senate (passed Senate)
- passed_both_houses (ready for assent)
- rejected (failed to pass)
- lapsed (Parliament prorogued/dissolved)
- withdrawn (sponsor withdrew)
```

---

## Stage 2: Act Creation

Once a bill passes both Houses, it becomes an **Act** upon Royal Assent. However, **assent ≠ commencement**.

### 2.1 Royal Assent

#### Commonwealth Level
- **Who**: Governor-General
- **Authority**: Queen's representative
- **Process**: Governor-General signs the bill
- **Temporal Marker**: `act.assent_date`
- **State Transition**: `passed_both_houses → assented`
- **Legal Effect**: Bill becomes an Act (but may not yet be "in force")

#### State Level
- **Who**: State Governor
- **Authority**: Queen's representative for the state
- **Process**: Similar to Commonwealth
- **Temporal Marker**: `act.assent_date`

#### Territory Level
- **ACT**: Administrator of the Territory
- **NT**: Administrator of the Territory

### 2.2 Commencement (When Act Becomes Law)

**Critical Distinction**: An Act receiving assent does NOT automatically mean it's in force.

#### 2.2.1 Commencement Provisions (Section 2)

**Standard Location**: Section 2 of the Act specifies commencement rules

**Example Section 2 Format:**
```
Section 2 - Commencement

(1) Each provision of this Act specified in column 1 of the table
    commences, or is taken to have commenced, in accordance with
    column 2 of the table.

| Provision(s) | Commencement | Date/Details |
|--------------|--------------|--------------|
| Sections 1-3 | The day this Act receives Royal Assent | [assent_date] |
| Schedule 1   | 1 July 2025 | 1 July 2025 |
| Schedule 2   | By Proclamation | [to be proclaimed] |
| Schedule 3   | The day after Royal Assent | [assent_date + 1 day] |
```

**Temporal Markers:**
- `act.section_2_provisions[]` - array of commencement rules
- `act.commencement_date` - when entire Act (or sections) come into force

#### 2.2.2 Commencement Methods

**1. On Royal Assent**
- **Rule**: Act comes into force on `assent_date`
- **Common**: Simple Acts, urgent legislation
- **Temporal State**: `assented → in_force` (same day)
- **Example**: "This Act commences on the day it receives Royal Assent"

**2. Automatic Commencement (28-Day Rule)**
- **Rule**: Acts Interpretation Act 1901 (Cth) s 3A
- **Default**: If no commencement specified, Act commences 28 days after assent
- **Calculation**: `commencement_date = assent_date + 28 days`
- **Temporal State**: `assented → pending_28_day → in_force`
- **Exception**: Does not apply if Act alters the Constitution
- **State Variations**: Each state has own Interpretation Act with similar provisions

**3. Proclamation Commencement**
- **Rule**: Government decides when to "proclaim" commencement
- **Who Decides**: Responsible Minister
- **Publication**: Proclamation published in Government Gazette
- **Temporal Markers**:
  - `act.proclamation_issued_date`
  - `act.proclaimed_commencement_date`
- **Temporal State**: `assented → awaiting_proclamation → proclaimed → in_force`
- **Risk**: Act may never be proclaimed (indefinite delay)
- **Example**: "This Schedule commences on a day to be fixed by Proclamation"

**4. Fixed Date Commencement**
- **Rule**: Act specifies exact calendar date
- **Format**: "1 July 2025", "The first day of the next financial year"
- **Temporal Marker**: `act.fixed_commencement_date`
- **Temporal State**: `assented → scheduled → in_force`
- **Can Be**: Future date or retrospective date

**5. Retrospective Commencement**
- **Rule**: Act deemed to have commenced before assent
- **Purpose**: Validate past actions, fix legislative gaps
- **Temporal Marker**: `act.retrospective_date`
- **Legal Risk**: May affect rights retrospectively
- **Example**: "This Act is taken to have commenced on 1 January 2024"

**6. Event-Triggered Commencement**
- **Rule**: Commencement upon occurrence of specified event
- **Examples**:
  - "On the commencement of the XYZ Act 2024"
  - "When Australia ratifies the ABC Treaty"
  - "When the Minister is satisfied that..."
- **Temporal Marker**: `act.trigger_event`, `act.trigger_date`
- **Temporal State**: `assented → awaiting_trigger → triggered → in_force`

#### 2.2.3 Partial Commencement

Acts can have **different commencement dates for different provisions**.

**Tracking Requirements:**
- `act.section_commencements[]` - array mapping sections to dates
- `act.schedule_commencements[]` - array mapping schedules to dates

**Example State:**
```json
{
  "act_id": "FLA_2024_125",
  "title": "Family Law Amendment Act 2024",
  "assent_date": "2024-12-15",
  "sections": [
    {
      "section_range": "1-3",
      "commencement_method": "on_assent",
      "commencement_date": "2024-12-15",
      "status": "in_force"
    },
    {
      "section_range": "Schedule 1",
      "commencement_method": "proclamation",
      "commencement_date": null,
      "status": "awaiting_proclamation"
    },
    {
      "section_range": "Schedule 2",
      "commencement_method": "28_days",
      "commencement_date": "2025-01-12",
      "status": "in_force"
    }
  ]
}
```

### 2.3 Temporal States for Acts

```
States (Post-Assent):
- assented (Royal Assent received, not yet in force)
- pending_28_day (waiting for automatic commencement)
- awaiting_proclamation (waiting for Minister to proclaim)
- scheduled (fixed date set, waiting for date)
- awaiting_trigger (waiting for event)
- in_force (law is operational)
- partially_in_force (some sections operational)
- suspended (temporarily not in force)
- repealed (no longer in force)
```

---

## Stage 3: Amendment Lifecycle

Acts can be modified by **Amending Acts** without replacing the entire original.

### 3.1 Principal Act vs Amending Act

**Principal Act**
- **Definition**: The original/main Act being amended
- **Also Called**: "Parent Act", "Base Act"
- **Example**: Family Law Act 1975
- **Temporal Marker**: `act.is_principal = true`

**Amending Act**
- **Definition**: Act that modifies a Principal Act
- **Also Called**: "Amendment Act"
- **Example**: Family Law Amendment Act 2024
- **Temporal Marker**: `act.amends_act_id = "FLA_1975"`
- **Title Pattern**: Usually includes "Amendment" in title

### 3.2 How Amendments Work

#### 3.2.1 Amendment Commands

Australian amendments use specific verbs:

**OMIT**
- **Action**: Remove existing text
- **Format**: "Omit '[old text]'"
- **Example**: "Omit 'director'"
- **Effect**: Deletes specified words/provisions

**SUBSTITUTE**
- **Action**: Replace existing text with new text
- **Format**: "Omit '[old text]', substitute '[new text]'"
- **Example**: "Omit 'director', substitute 'executive officer'"
- **Effect**: Deletes old, inserts new

**INSERT**
- **Action**: Add new text
- **Format**: "Insert after section X: '[new text]'"
- **Example**: "Insert after section 10A: '10B Purpose of Part'"
- **Effect**: Adds new provision

**REPEAL**
- **Action**: Remove entire provision
- **Format**: "Repeal section X"
- **Example**: "Repeal Schedule 3"
- **Effect**: Provision deleted entirely

**RENUMBER**
- **Action**: Change section numbering
- **Format**: "Renumber sections X-Y as sections A-B"
- **Effect**: Changes reference numbers

**RELOCATE**
- **Action**: Move provision to different location
- **Format**: "Relocate section X to Part Y"
- **Effect**: Provision moves within Act structure

#### 3.2.2 Schedule Format

Amending Acts typically use **Schedules** to organize amendments.

**Example Schedule Structure:**
```
Family Law Amendment Act 2024

Schedule 1 - Amendments to Family Law Act 1975

Part 1 - Main amendments

Item 1
Section 4 (definition of "de facto relationship")
Omit "2 years", substitute "12 months".

Item 2
After section 60CC
Insert:
60CCA Considerations for parenting orders - family violence
(1) In making a parenting order, the court must consider...

Item 3
Section 79(4)(c)
Repeal the paragraph, substitute:
(c) the financial resources available to each party;

Item 4
Schedule 2
Omit the Schedule.

Part 2 - Consequential amendments

[Further items...]
```

**Temporal Markers for Amendments:**
- `amendment.item_number` - Sequential item in schedule
- `amendment.target_section` - Which provision is amended
- `amendment.amendment_type` - "omit", "substitute", "insert", "repeal"
- `amendment.effective_date` - When amendment takes effect
- `amendment.amending_act_id` - Which Act made the amendment

### 3.3 Legal Fiction: "One Continuous Act"

**Rule**: When a Principal Act is amended, the two Acts are regarded as "one connected and combined expression of the will of Parliament"

**Implication**: You read the Principal Act AS IF the amendments were always there (from commencement of amendment)

### 3.4 Compiled/Consolidated Acts

**Definition**: "Cut and paste" version showing Act as currently amended

**Authority**: Official compilations published on Federal Register of Legislation

**Temporal Markers:**
- `compilation.as_at_date` - Date compilation reflects amendments up to
- `compilation.version_number` - Sequential version number
- `compilation.incorporates_amendments[]` - List of amendments included

**Example:**
```
Family Law Act 1975
Compilation No. 78
Compilation date: 1 July 2024
Registered: 15 July 2024

Includes amendments up to:
- Family Law Amendment Act 2023 (No. 125, 2023)
- Family Law Amendment Act 2024 (No. 45, 2024) [commenced 1 July 2024]
```

### 3.5 Temporal States for Amendments

```
States:
- proposed (amendment bill introduced)
- enacted (amendment Act assented)
- pending_commencement (assented but not yet in force)
- in_force (amendment operational)
- superseded (later amendment overrides)
```

---

## Stage 4: Termination

Acts and provisions can cease to have legal effect through several mechanisms.

### 4.1 Repeal

#### 4.1.1 Express Repeal

**Definition**: Act explicitly repealed by another Act

**Format:**
```
Repealing Act: Family Law Repeal Act 2025

Section 3 - Repeal
The Family Law Act 1975 is repealed.
```

**Temporal Markers:**
- `act.repealed_by_act_id` - Which Act repealed it
- `act.repeal_date` - When repeal takes effect
- `act.status = "repealed"`

**State Transition**: `in_force → repealed`

#### 4.1.2 Implied Repeal

**Definition**: New Act implicitly replaces old Act (rare in modern practice)

**Rule**: "Later law prevails" - if irreconcilable inconsistency

**Temporal Markers:**
- `act.implicitly_repealed_by_act_id`
- `act.repeal_type = "implied"`

**Risk**: Less clear, courts must determine

### 4.2 Sunsetting

**Definition**: Automatic repeal after fixed period

**Authority**: Legislation Act 2003 (Cth) s 50

**Default Rule**: Legislative instruments sunset 10 years after registration

**Sunset Dates**: 1 April or 1 October

**Process:**
1. Instrument registered on Federal Register
2. 18 months before sunset: Sunsetting list tabled in Parliament
3. Agency must:
   - Remake instrument (if still needed), OR
   - Let it sunset (if redundant)
4. On sunset date: Instrument automatically repealed

**Exemptions from Sunsetting:**
- Instruments with saving/transitional provisions (unless moved to another instrument)
- Instruments giving effect to international obligations
- Instruments establishing bodies with contracting power
- Ministerial directions
- Territory governance instruments
- Superannuation instruments (non-regulation)
- Appropriation Act instruments

**Temporal Markers:**
- `instrument.registration_date`
- `instrument.sunset_date` - Calculated: registration_date + 10 years (nearest 1 Apr or 1 Oct)
- `instrument.sunsetting_list_tabled_date` - 18 months before sunset
- `instrument.remake_date` - If remade
- `instrument.sunset_exemption` - Boolean or exemption reason

**State Transition**: `in_force → sunset_pending → sunsetted`

### 4.3 Spent Acts

**Definition**: Acts that have achieved their purpose and have no ongoing effect

**Examples:**
- Transitional Acts (after transition complete)
- One-off appropriation Acts (after funds spent)
- Acts establishing bodies (after body established)

**Repeal Process:**
- Legislation Act 2003 s 48E allows bulk repeal of spent instruments
- Dedicated "Spent Acts Repeal" legislation

**Temporal Markers:**
- `act.is_spent = true`
- `act.spent_reason` - "transition_complete", "purpose_achieved"
- `act.spent_determination_date`

**State**: `in_force → spent → repealed`

### 4.4 Savings and Transitional Provisions

**Purpose**: Manage the transition when laws change

**Savings Provisions**
- **Definition**: Preserve rights/obligations created under old law
- **Example**: "Rights accrued under the repealed Act continue"
- **Temporal Effect**: Past actions remain valid despite repeal

**Transitional Provisions**
- **Definition**: Special arrangements for changeover period
- **Example**: "Applications lodged before commencement are dealt with under old law"
- **Duration**: Usually specify end date or condition

**Location:**
- Within the repealing Act (e.g., Schedule 2 - Transitional Provisions)
- Separate "Consequential and Transitional Provisions Act"

**Temporal Markers:**
- `act.has_savings_provisions = true`
- `act.has_transitional_provisions = true`
- `act.transition_end_date` - When transition period ends

**Impact on Sunsetting:**
- Instruments with transitional provisions CANNOT automatically sunset
- Must be explicitly repealed or provisions moved

### 4.5 Temporal States for Termination

```
States:
- in_force (operational)
- spent (purpose achieved)
- sunset_pending (approaching automatic repeal)
- sunsetted (automatically repealed)
- repealed_express (explicitly repealed)
- repealed_implied (implicitly replaced)
- superseded (replaced by new version)
```

---

## Stage 5: Subordinate Legislation

Regulations and other instruments made under enabling Acts.

### 5.1 Types of Subordinate Legislation

**Legislative Instruments** (Commonwealth)
- Regulations
- Rules
- Ordinances
- Determinations
- Directions
- Standards

**Subordinate Laws** (ACT terminology)
- Regulations
- Rules

### 5.2 Enabling Acts

**Definition**: Primary legislation that authorizes rule-maker to make subordinate legislation

**Example:**
```
Family Law Act 1975, Section 123
The Governor-General may make regulations prescribing matters:
  (a) required or permitted by this Act to be prescribed; or
  (b) necessary or convenient to be prescribed for carrying out or giving effect to this Act.
```

**Temporal Markers:**
- `regulation.enabling_act_id` - Parent Act
- `regulation.enabling_section` - Specific section authorizing
- `regulation.rule_maker` - "Governor-General", "Minister"

### 5.3 Disallowance

**Definition**: Parliament can repeal (disallow) a legislative instrument

**Authority**: Legislation Act 2003 s 42

**Process:**
1. Instrument presented to both Houses within 6 sitting days of registration
2. Disallowance period: 15 sitting days from tabling
3. Either House can move to disallow
4. If disallowed: Instrument repealed from that time

**Effects of Disallowance:**
- Instrument repealed
- May revive previous laws (if not sunsetted)
- Rule-maker must wait 6 months before remaking substantially same instrument

**Exemptions from Disallowance:**
- Instruments requiring Parliamentary approval
- Ministerial directions
- Superannuation instruments (non-regulation)
- Appropriation Act instruments

**Temporal Markers:**
- `regulation.tabled_date_house`
- `regulation.tabled_date_senate`
- `regulation.disallowance_period_ends`
- `regulation.disallowed_date` (if disallowed)
- `regulation.disallowance_exempt = true/false`

**State Transition**: `in_force → disallowed`

### 5.4 Sunsetting of Subordinate Legislation

**Rule**: Legislative instruments sunset 10 years after registration (Legislation Act 2003 s 50)

**See Section 4.2** for detailed sunsetting process.

**Key Differences from Acts:**
- Acts generally do NOT sunset (only instruments)
- Instruments must be reviewed and remade or allowed to lapse

### 5.5 Temporal States for Subordinate Legislation

```
States:
- drafted (pre-registration)
- registered (on Federal Register)
- tabled (presented to Parliament)
- in_disallowance_period (15 sitting days window)
- in_force (operational)
- sunset_pending (approaching 10-year anniversary)
- remade (replaced with new version)
- sunsetted (automatically repealed)
- disallowed (Parliament repealed)
```

---

## Temporal State Machine

### Complete State Diagram

```
BILLS:
drafted → introduced → debated → [in_committee] → [under_amendment]
  → passed_house → in_senate → passed_senate → passed_both_houses
  → assented (becomes ACT)

Failure paths:
  → rejected (bill fails)
  → lapsed (Parliament dissolved)
  → withdrawn (sponsor withdraws)

ACTS (Post-Assent):
assented → [pending_28_day | awaiting_proclamation | scheduled | awaiting_trigger]
  → in_force
  → [spent | sunset_pending | superseded]
  → repealed

Partial states:
  → partially_in_force (some sections operational)

Temporary states:
  → suspended (temporarily not operational)

AMENDMENTS:
proposed → enacted → pending_commencement → in_force
  → superseded (later amendment overrides)

SUBORDINATE LEGISLATION:
drafted → registered → tabled → in_disallowance_period → in_force
  → sunset_pending → [remade | sunsetted | disallowed]
```

### State Definitions

| State | Applies To | Meaning | Next Possible States |
|-------|-----------|---------|---------------------|
| `drafted` | Bill, Regulation | Document prepared, not yet introduced | `introduced`, `withdrawn` |
| `introduced` | Bill | 1st reading complete | `debated`, `rejected`, `withdrawn` |
| `debated` | Bill | 2nd reading in progress | `in_committee`, `under_amendment`, `passed_house`, `rejected` |
| `in_committee` | Bill | Committee review | `debated`, `passed_house`, `rejected` |
| `under_amendment` | Bill | Consideration in detail | `debated`, `passed_house`, `rejected` |
| `passed_house` | Bill | Passed House of Reps | `in_senate`, `lapsed` |
| `in_senate` | Bill | Senate considering | `passed_senate`, `senate_amended`, `rejected`, `lapsed` |
| `senate_amended` | Bill | Senate proposed changes | `returned_to_house`, `lapsed` |
| `passed_senate` | Bill | Passed both Houses | `assented` |
| `passed_both_houses` | Bill | Awaiting Royal Assent | `assented` |
| `rejected` | Bill | Failed to pass | (terminal) |
| `lapsed` | Bill | Parliament prorogued/dissolved | (terminal) |
| `withdrawn` | Bill | Sponsor withdrew | (terminal) |
| `assented` | Act | Royal Assent received, may not be in force yet | `pending_28_day`, `awaiting_proclamation`, `scheduled`, `awaiting_trigger`, `in_force` |
| `pending_28_day` | Act | Waiting for automatic commencement | `in_force` |
| `awaiting_proclamation` | Act | Waiting for proclamation | `proclaimed`, `in_force` |
| `scheduled` | Act | Fixed commencement date set | `in_force` |
| `awaiting_trigger` | Act | Waiting for event | `triggered`, `in_force` |
| `in_force` | Act, Regulation | Operational law | `spent`, `sunset_pending`, `suspended`, `superseded`, `repealed` |
| `partially_in_force` | Act | Some sections operational | `in_force`, `repealed` |
| `suspended` | Act | Temporarily not operational | `in_force`, `repealed` |
| `spent` | Act | Purpose achieved | `repealed` |
| `sunset_pending` | Regulation | Approaching automatic repeal | `remade`, `sunsetted` |
| `sunsetted` | Regulation | Automatically repealed | (terminal) |
| `superseded` | Act, Amendment | Replaced by newer version | `repealed` (historical) |
| `repealed` | Act | No longer in force | (terminal) |
| `disallowed` | Regulation | Parliament rejected | (terminal) |
| `registered` | Regulation | Registered on Federal Register | `tabled`, `in_force` |
| `tabled` | Regulation | Presented to Parliament | `in_disallowance_period` |
| `in_disallowance_period` | Regulation | 15 sitting days window | `in_force`, `disallowed` |
| `remade` | Regulation | New version created before sunset | `registered` (new cycle) |

---

## Implementation Guide

### Data Schema for Temporal Tracker

```python
from enum import Enum
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class LegislationType(str, Enum):
    BILL = "bill"
    ACT = "act"
    REGULATION = "regulation"
    RULE = "rule"
    DETERMINATION = "determination"
    PROCLAMATION = "proclamation"

class Jurisdiction(str, Enum):
    COMMONWEALTH = "commonwealth"
    NSW = "nsw"
    VICTORIA = "vic"
    QUEENSLAND = "qld"
    SOUTH_AUSTRALIA = "sa"
    WESTERN_AUSTRALIA = "wa"
    TASMANIA = "tas"
    ACT = "act"
    NORTHERN_TERRITORY = "nt"

class LegislativeState(str, Enum):
    # Bills
    DRAFTED = "drafted"
    INTRODUCED = "introduced"
    DEBATED = "debated"
    IN_COMMITTEE = "in_committee"
    UNDER_AMENDMENT = "under_amendment"
    PASSED_HOUSE = "passed_house"
    IN_SENATE = "in_senate"
    SENATE_AMENDED = "senate_amended"
    PASSED_SENATE = "passed_senate"
    PASSED_BOTH_HOUSES = "passed_both_houses"
    REJECTED = "rejected"
    LAPSED = "lapsed"
    WITHDRAWN = "withdrawn"

    # Acts (post-assent)
    ASSENTED = "assented"
    PENDING_28_DAY = "pending_28_day"
    AWAITING_PROCLAMATION = "awaiting_proclamation"
    SCHEDULED = "scheduled"
    AWAITING_TRIGGER = "awaiting_trigger"
    IN_FORCE = "in_force"
    PARTIALLY_IN_FORCE = "partially_in_force"
    SUSPENDED = "suspended"
    SPENT = "spent"
    SUNSET_PENDING = "sunset_pending"
    SUPERSEDED = "superseded"
    REPEALED = "repealed"
    SUNSETTED = "sunsetted"
    DISALLOWED = "disallowed"

    # Regulations
    REGISTERED = "registered"
    TABLED = "tabled"
    IN_DISALLOWANCE_PERIOD = "in_disallowance_period"
    REMADE = "remade"

class CommencementMethod(str, Enum):
    ON_ASSENT = "on_assent"
    AUTOMATIC_28_DAYS = "28_days"
    PROCLAMATION = "proclamation"
    FIXED_DATE = "fixed_date"
    RETROSPECTIVE = "retrospective"
    EVENT_TRIGGERED = "event_triggered"
    PARTIAL = "partial"  # Different sections different methods

class AmendmentType(str, Enum):
    OMIT = "omit"
    SUBSTITUTE = "substitute"
    INSERT = "insert"
    REPEAL = "repeal"
    RENUMBER = "renumber"
    RELOCATE = "relocate"

class RepealType(str, Enum):
    EXPRESS = "express"
    IMPLIED = "implied"
    SUNSET = "sunset"
    DISALLOWANCE = "disallowance"

class BillType(str, Enum):
    GOVERNMENT = "government"
    PRIVATE_MEMBER = "private_member"
    PRIVATE_SENATOR = "private_senator"

# === MODELS ===

class TemporalAnchor(BaseModel):
    """Key date in legislative lifecycle"""
    date: date
    event_type: str
    description: str
    source_document: Optional[str] = None

class SectionCommencement(BaseModel):
    """Commencement details for Act sections"""
    section_range: str  # "1-3", "Schedule 1", "Part 2"
    commencement_method: CommencementMethod
    commencement_date: Optional[date] = None
    proclamation_reference: Optional[str] = None
    trigger_event: Optional[str] = None
    status: LegislativeState

class Amendment(BaseModel):
    """Amendment to a Principal Act"""
    amendment_id: str
    amending_act_id: str
    item_number: int
    target_section: str
    amendment_type: AmendmentType
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    effective_date: Optional[date] = None
    status: LegislativeState

class Compilation(BaseModel):
    """Compiled version of Act"""
    compilation_number: int
    as_at_date: date
    registered_date: date
    incorporates_amendments: List[str]  # List of amending Act IDs

class LegislativeDocument(BaseModel):
    """Complete legislative document with temporal tracking"""

    # Identity
    document_id: str
    jurisdiction: Jurisdiction
    document_type: LegislationType
    title: str
    year: int
    number: Optional[int] = None  # Act No. X of YYYY

    # Current State
    current_state: LegislativeState
    state_history: List[dict]  # [{state, date, reason}, ...]

    # Bill Stage (if applicable)
    bill_type: Optional[BillType] = None
    introduced_date: Optional[date] = None
    second_reading_date: Optional[date] = None
    third_reading_date: Optional[date] = None
    passed_house_date: Optional[date] = None
    passed_senate_date: Optional[date] = None
    is_money_bill: bool = False
    is_appropriation_bill: bool = False

    # Act Creation (if applicable)
    assent_date: Optional[date] = None
    commencement_method: Optional[CommencementMethod] = None
    commencement_date: Optional[date] = None
    section_commencements: List[SectionCommencement] = []
    proclamation_date: Optional[date] = None
    proclamation_reference: Optional[str] = None

    # Amendments (if this is amending Act)
    is_amending_act: bool = False
    amends_act_id: Optional[str] = None
    amendments: List[Amendment] = []

    # Amendments (if this is principal Act)
    is_principal_act: bool = False
    amended_by: List[str] = []  # List of amending Act IDs
    compilations: List[Compilation] = []
    current_compilation: Optional[Compilation] = None

    # Termination
    is_repealed: bool = False
    repeal_date: Optional[date] = None
    repealed_by_act_id: Optional[str] = None
    repeal_type: Optional[RepealType] = None
    is_spent: bool = False
    spent_reason: Optional[str] = None

    # Transitional
    has_savings_provisions: bool = False
    has_transitional_provisions: bool = False
    transition_end_date: Optional[date] = None

    # Subordinate Legislation (if applicable)
    enabling_act_id: Optional[str] = None
    enabling_section: Optional[str] = None
    rule_maker: Optional[str] = None  # "Governor-General", "Minister"
    registration_date: Optional[date] = None
    sunset_date: Optional[date] = None
    sunset_exempt: bool = False
    sunset_exemption_reason: Optional[str] = None
    tabled_date_house: Optional[date] = None
    tabled_date_senate: Optional[date] = None
    disallowance_period_ends: Optional[date] = None
    disallowance_exempt: bool = False

    # Temporal Anchors
    temporal_anchors: List[TemporalAnchor] = []

    # Metadata
    source_url: Optional[str] = None
    last_updated: datetime

    def add_state_change(self, new_state: LegislativeState, reason: str):
        """Record state transition"""
        self.state_history.append({
            "from_state": self.current_state,
            "to_state": new_state,
            "date": datetime.now().date(),
            "reason": reason
        })
        self.current_state = new_state

    def calculate_28_day_commencement(self) -> Optional[date]:
        """Calculate automatic commencement date"""
        if self.assent_date:
            from datetime import timedelta
            return self.assent_date + timedelta(days=28)
        return None

    def calculate_sunset_date(self) -> Optional[date]:
        """Calculate sunset date for subordinate legislation"""
        if self.registration_date and self.document_type in [
            LegislationType.REGULATION,
            LegislationType.RULE,
            LegislationType.DETERMINATION
        ]:
            # 10 years from registration, nearest 1 Apr or 1 Oct
            from datetime import timedelta
            ten_years = self.registration_date.replace(year=self.registration_date.year + 10)

            # Find nearest 1 Apr or 1 Oct
            april_1 = date(ten_years.year, 4, 1)
            oct_1 = date(ten_years.year, 10, 1)

            if ten_years <= april_1:
                return april_1
            elif ten_years <= oct_1:
                return oct_1
            else:
                return date(ten_years.year + 1, 4, 1)
        return None

    def is_in_force_on(self, check_date: date) -> bool:
        """Check if Act/regulation was in force on a specific date"""
        # Must be commenced
        if not self.commencement_date or check_date < self.commencement_date:
            return False

        # Must not be repealed (or check before repeal)
        if self.is_repealed and self.repeal_date and check_date >= self.repeal_date:
            return False

        # Must not be sunsetted
        if self.sunset_date and check_date >= self.sunset_date:
            return False

        return True
```

### State Transition Functions

```python
class TemporalTracker:
    """Manages legislative document state transitions"""

    def __init__(self):
        self.documents = {}  # document_id -> LegislativeDocument

    def transition_bill_to_assented(
        self,
        bill_id: str,
        assent_date: date
    ) -> LegislativeDocument:
        """Transition bill to Act upon Royal Assent"""
        doc = self.documents[bill_id]

        if doc.current_state != LegislativeState.PASSED_BOTH_HOUSES:
            raise ValueError("Bill must pass both houses before assent")

        doc.assent_date = assent_date
        doc.add_state_change(LegislativeState.ASSENTED, "Royal Assent received")
        doc.document_type = LegislationType.ACT

        # Add temporal anchor
        doc.temporal_anchors.append(TemporalAnchor(
            date=assent_date,
            event_type="royal_assent",
            description="Royal Assent by Governor-General"
        ))

        return doc

    def determine_commencement_state(
        self,
        act_id: str
    ) -> LegislativeDocument:
        """Determine commencement state after assent"""
        doc = self.documents[act_id]

        if doc.current_state != LegislativeState.ASSENTED:
            raise ValueError("Act must be assented before commencement")

        # Check Section 2 commencement provisions
        if doc.commencement_method == CommencementMethod.ON_ASSENT:
            doc.commencement_date = doc.assent_date
            doc.add_state_change(LegislativeState.IN_FORCE, "Commenced on assent")

        elif doc.commencement_method == CommencementMethod.AUTOMATIC_28_DAYS:
            doc.commencement_date = doc.calculate_28_day_commencement()
            doc.add_state_change(
                LegislativeState.PENDING_28_DAY,
                "Awaiting automatic commencement"
            )

        elif doc.commencement_method == CommencementMethod.PROCLAMATION:
            doc.add_state_change(
                LegislativeState.AWAITING_PROCLAMATION,
                "Awaiting proclamation"
            )

        elif doc.commencement_method == CommencementMethod.FIXED_DATE:
            doc.add_state_change(
                LegislativeState.SCHEDULED,
                f"Scheduled for {doc.commencement_date}"
            )

        elif doc.commencement_method == CommencementMethod.EVENT_TRIGGERED:
            doc.add_state_change(
                LegislativeState.AWAITING_TRIGGER,
                "Awaiting trigger event"
            )

        elif doc.commencement_method == CommencementMethod.PARTIAL:
            doc.add_state_change(
                LegislativeState.PARTIALLY_IN_FORCE,
                "Partial commencement"
            )

        return doc

    def record_proclamation(
        self,
        act_id: str,
        proclamation_date: date,
        proclaimed_commencement_date: date,
        reference: str
    ) -> LegislativeDocument:
        """Record proclamation of commencement"""
        doc = self.documents[act_id]

        if doc.current_state != LegislativeState.AWAITING_PROCLAMATION:
            raise ValueError("Act must be awaiting proclamation")

        doc.proclamation_date = proclamation_date
        doc.commencement_date = proclaimed_commencement_date
        doc.proclamation_reference = reference

        doc.add_state_change(
            LegislativeState.IN_FORCE,
            f"Proclaimed to commence {proclaimed_commencement_date}"
        )

        doc.temporal_anchors.append(TemporalAnchor(
            date=proclamation_date,
            event_type="proclamation",
            description=f"Proclamation issued: {reference}"
        ))

        return doc

    def record_amendment(
        self,
        principal_act_id: str,
        amending_act: LegislativeDocument
    ) -> LegislativeDocument:
        """Record amendment to principal Act"""
        principal = self.documents[principal_act_id]

        # Add to principal's amendment list
        principal.amended_by.append(amending_act.document_id)

        # Create new compilation
        compilation = Compilation(
            compilation_number=len(principal.compilations) + 1,
            as_at_date=amending_act.commencement_date or datetime.now().date(),
            registered_date=datetime.now().date(),
            incorporates_amendments=principal.amended_by.copy()
        )
        principal.compilations.append(compilation)
        principal.current_compilation = compilation

        return principal

    def record_repeal(
        self,
        act_id: str,
        repeal_date: date,
        repealing_act_id: str,
        repeal_type: RepealType
    ) -> LegislativeDocument:
        """Record repeal of Act"""
        doc = self.documents[act_id]

        doc.is_repealed = True
        doc.repeal_date = repeal_date
        doc.repealed_by_act_id = repealing_act_id
        doc.repeal_type = repeal_type

        doc.add_state_change(
            LegislativeState.REPEALED,
            f"Repealed by {repealing_act_id}"
        )

        doc.temporal_anchors.append(TemporalAnchor(
            date=repeal_date,
            event_type="repeal",
            description=f"Repealed ({repeal_type})"
        ))

        return doc

    def check_sunset(
        self,
        regulation_id: str,
        current_date: date
    ) -> LegislativeDocument:
        """Check if regulation should sunset"""
        doc = self.documents[regulation_id]

        if doc.document_type not in [
            LegislationType.REGULATION,
            LegislationType.RULE,
            LegislationType.DETERMINATION
        ]:
            return doc

        if doc.sunset_exempt:
            return doc

        if not doc.sunset_date:
            doc.sunset_date = doc.calculate_sunset_date()

        # Check if approaching sunset (18 months window)
        from datetime import timedelta
        if doc.sunset_date - timedelta(days=547) <= current_date < doc.sunset_date:
            if doc.current_state != LegislativeState.SUNSET_PENDING:
                doc.add_state_change(
                    LegislativeState.SUNSET_PENDING,
                    f"Approaching sunset on {doc.sunset_date}"
                )

        # Check if sunset date reached
        if current_date >= doc.sunset_date:
            doc.add_state_change(
                LegislativeState.SUNSETTED,
                "Automatically sunsetted"
            )
            doc.is_repealed = True
            doc.repeal_date = doc.sunset_date
            doc.repeal_type = RepealType.SUNSET

        return doc
```

### Query Functions

```python
class LegislationQuery:
    """Query legislative documents by temporal criteria"""

    def __init__(self, tracker: TemporalTracker):
        self.tracker = tracker

    def get_in_force_on_date(
        self,
        date: date,
        jurisdiction: Optional[Jurisdiction] = None
    ) -> List[LegislativeDocument]:
        """Get all Acts/regulations in force on a specific date"""
        results = []
        for doc in self.tracker.documents.values():
            if jurisdiction and doc.jurisdiction != jurisdiction:
                continue
            if doc.is_in_force_on(date):
                results.append(doc)
        return results

    def get_amendments_to_act(
        self,
        principal_act_id: str
    ) -> List[LegislativeDocument]:
        """Get all amendments to a principal Act"""
        principal = self.tracker.documents[principal_act_id]
        return [
            self.tracker.documents[aid]
            for aid in principal.amended_by
        ]

    def get_acts_repealed_by(
        self,
        repealing_act_id: str
    ) -> List[LegislativeDocument]:
        """Get all Acts repealed by a specific Act"""
        results = []
        for doc in self.tracker.documents.values():
            if doc.repealed_by_act_id == repealing_act_id:
                results.append(doc)
        return results

    def get_bills_in_parliament(
        self,
        jurisdiction: Jurisdiction
    ) -> List[LegislativeDocument]:
        """Get all bills currently in Parliament"""
        active_bill_states = [
            LegislativeState.INTRODUCED,
            LegislativeState.DEBATED,
            LegislativeState.IN_COMMITTEE,
            LegislativeState.UNDER_AMENDMENT,
            LegislativeState.PASSED_HOUSE,
            LegislativeState.IN_SENATE,
            LegislativeState.SENATE_AMENDED,
            LegislativeState.PASSED_SENATE,
            LegislativeState.PASSED_BOTH_HOUSES
        ]

        results = []
        for doc in self.tracker.documents.values():
            if (doc.jurisdiction == jurisdiction and
                doc.document_type == LegislationType.BILL and
                doc.current_state in active_bill_states):
                results.append(doc)
        return results

    def get_regulations_pending_sunset(
        self,
        months_ahead: int = 18
    ) -> List[LegislativeDocument]:
        """Get regulations approaching sunset"""
        from datetime import timedelta, date
        cutoff = date.today() + timedelta(days=months_ahead * 30)

        results = []
        for doc in self.tracker.documents.values():
            if (doc.document_type in [LegislationType.REGULATION, LegislationType.RULE] and
                doc.sunset_date and
                doc.sunset_date <= cutoff and
                not doc.sunset_exempt):
                results.append(doc)
        return results
```

---

## Sources

This documentation is based on extensive research of Australian legislative processes and frameworks:

### Legislative Process & Bills
- [The usual path of a bill - Parliamentary Education Office](https://peo.gov.au/understand-our-parliament/how-parliament-works/bills-and-laws/the-usual-path-of-a-bill)
- [Legislative Process - Researching Legislation - Deakin University](https://deakin.libguides.com/legislation/legislative-process)
- [The legislative process - ANU Law LibGuides](https://libguides.anu.edu.au/c.php?g=634887&p=4446812)
- [Guide to the legislation process - PM&C](https://www.pmc.gov.au/resources/guide-legislation-process)
- [Bills and Legislation – Parliament of Australia](https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation)

### Royal Assent & Commencement
- [Frequently Asked Questions - Office of Parliamentary Counsel](https://www.opc.gov.au/faq)
- [Commencement of Acts - Deakin University LibGuides](https://deakin.libguides.com/legislation/commencement-of-acts)
- [Presentation of bills for assent – Parliament of Australia](https://www.aph.gov.au/About_Parliament/House_of_Representatives/Powers_practice_and_procedure/Practice7/HTML/Chapter10/Presentation_of_bills_for_assent)
- [Acts in force - University of Western Australia](https://guides.library.uwa.edu.au/c.php?g=324818&p=2178288)
- [Commencement: determining when an Act commences - State Law Publisher WA](https://www.slp.wa.gov.au/faq.nsf/Web/Topics/263812DF508A472D48256CC90023B552?opendocument)

### Amendments
- [Acts - Australian Legislation - University of Melbourne](https://unimelb.libguides.com/c.php?g=941273&p=6980902)
- [CIVIL LAW AND JUSTICE LEGISLATION AMENDMENT ACT 2018 - AustLII](https://www8.austlii.edu.au/cgi-bin/viewdoc/au/legis/cth/num_act/clajlaa2018392/sch6.html)
- [LEGISLATION ACT 2001 - NOTES - AustLII](https://classic.austlii.edu.au/au/legis/act/consol_act/la2001133/notes.html)

### Repeal & Sunsetting
- [Repeal, Disallowance and Sunsetting - Federal Register of Legislation](https://www.legislation.gov.au/help-and-resources/understanding-legislation/repealdisallowanceandsunsetting)
- [Legislation Act 2003 - Attorney-General's Department](https://www.ag.gov.au/legal-system/administrative-law/legislation-act-2003)
- [LEGISLATION ACT 2003 - SECT 50 Sunsetting - AustLII](https://www6.austlii.edu.au/cgi-bin/viewdoc/au/legis/cth/consol_act/la2003133/s50.html)
- [Glossary - Federal Register of Legislation](https://www.legislation.gov.au/help-and-resources/understanding-legislation/glossary)

### Subordinate Legislation
- [Subordinate Legislation Act 1994 Guidelines - Parliament of Victoria](https://www.parliament.vic.gov.au/4961ea/globalassets/tabled-paper-documents/tabled-paper-7465/subordinate-legislation-act-1994-guidelines-september-2023.pdf)
- [Exemptions from disallowance and sunsetting - AustLII](https://www6.austlii.edu.au/cgi-bin/viewdoc/au/other/cth/AUSStaCSDLM/2023/144.html)
- [ACT Legislation Register - About ACT Legislation](https://www.legislation.act.gov.au/Static/UsefulResources/About/about_act_legislation.html)

### Parliament Structure
- [Law-making - Parliamentary Education Office](https://peo.gov.au/understand-our-parliament/how-parliament-works/bills-and-laws/law-making)
- [Passage of Legislation - Senate](https://senate.gov.au/passage-of-legislation/index.html)
- [Australian Senate - Wikipedia](https://en.wikipedia.org/wiki/Australian_Senate)
- [Australian House of Representatives - Wikipedia](https://en.wikipedia.org/wiki/Australian_House_of_Representatives)

---

## Appendix: Example Lifecycle Timeline

### Example: Family Law Amendment Act 2024

```
Timeline for Document ID: FLA_2024_045

=== BILL STAGE ===
2024-03-15: DRAFTED
  - Government bill prepared by Attorney-General's Department

2024-04-10: INTRODUCED (1st Reading - House of Representatives)
  - Bill No. 045/2024
  - Explanatory Memorandum published

2024-04-15: DEBATED (2nd Reading - House of Representatives)
  - Debate over 2 sitting days

2024-04-22: IN_COMMITTEE
  - Referred to Legal and Constitutional Affairs Committee

2024-05-20: Committee Report Tabled
  - Recommended passage with amendments

2024-05-25: UNDER_AMENDMENT (Consideration in Detail)
  - 3 government amendments accepted

2024-05-27: PASSED_HOUSE (3rd Reading)
  - Vote: 78 Ayes, 52 Noes

2024-06-01: IN_SENATE
  - Transmitted to Senate

2024-06-05: SENATE_AMENDED
  - Senate proposes 2 additional amendments

2024-06-10: Returned to House
  - House accepts Senate amendments

2024-06-12: PASSED_SENATE
  - Vote: 44 Ayes, 28 Noes

2024-06-15: PASSED_BOTH_HOUSES
  - Awaiting Royal Assent

=== ACT CREATION ===
2024-06-20: ASSENTED
  - Royal Assent by Governor-General
  - Act No. 45 of 2024

Section 2 Commencement Provisions:
  - Sections 1-3: On Royal Assent (2024-06-20) → IN_FORCE
  - Schedule 1 (Items 1-10): 1 July 2024 → SCHEDULED
  - Schedule 2 (Items 11-15): By Proclamation → AWAITING_PROCLAMATION

2024-06-20: PARTIALLY_IN_FORCE
  - Sections 1-3 operational

2024-07-01: Schedule 1 Commenced
  - Fixed date commencement

2024-08-15: PROCLAIMED
  - Proclamation C2024G00156 issued
  - Schedule 2 to commence 2024-09-01

2024-09-01: IN_FORCE (Fully)
  - All provisions operational

=== AMENDMENT LIFECYCLE ===
Schedule 1 - Amendments to Family Law Act 1975

Item 1:
  Target: Section 79(4)(c)
  Amendment Type: SUBSTITUTE
  Effective Date: 2024-07-01
  Old Text: "the financial resources of each of the parties"
  New Text: "the financial resources available to each party, including earning capacity"

Item 2:
  Target: After section 60CC
  Amendment Type: INSERT
  Effective Date: 2024-07-01
  New Text: [New section 60CCA - Family violence considerations]

2024-07-05: COMPILATION REGISTERED
  - Family Law Act 1975 (Compilation No. 79)
  - As at 1 July 2024
  - Incorporates: FLA Amendment Act 2024 (No. 45, 2024)

=== POTENTIAL TERMINATION ===
[This Act currently remains IN_FORCE]

Hypothetical Future Events:
2034-09-01: SPENT (if all amendments incorporated and no ongoing effect)
2035-01-15: REPEALED (via Spent Acts Repeal Act 2035)
```

---

**End of Document**
