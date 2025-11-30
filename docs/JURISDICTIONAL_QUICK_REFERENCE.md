# Jurisdictional Authority Quick Reference
## For Jurisdictional Sentinel Agent

---

## Quick Decision Trees

### Is it Federal or State?

```
START: What is the subject matter?

├─ Marriage/Divorce?
│  └─ FEDERAL (s51(xxi), (xxii)) - Commonwealth law prevails
│     └─ Exception: WA de facto = STATE
│
├─ Bankruptcy?
│  └─ FEDERAL (s51(xvii)) - Commonwealth occupied field
│
├─ Corporations (trading/financial/foreign)?
│  └─ FEDERAL (s51(xx)) - Commonwealth extensive regulation
│
├─ Immigration/Citizenship?
│  └─ FEDERAL EXCLUSIVE (s51(xix), (xxvii))
│
├─ Defence/Foreign Affairs?
│  └─ FEDERAL EXCLUSIVE (s51(vi), (xxix))
│
├─ Customs/Excise?
│  └─ FEDERAL EXCLUSIVE (s90)
│
├─ Trade between states or internationally?
│  └─ FEDERAL (s51(i))
│
├─ Criminal law (murder, theft, assault)?
│  └─ STATE RESIDUAL (unless federal offence)
│
├─ Land law/planning?
│  └─ STATE RESIDUAL
│
├─ Contracts/Torts (civil)?
│  └─ STATE RESIDUAL
│
├─ Education/Schools?
│  └─ STATE RESIDUAL (Commonwealth funds)
│
├─ Health/Hospitals?
│  └─ STATE RESIDUAL (Commonwealth funds)
│
├─ Police?
│  └─ STATE RESIDUAL (except AFP)
│
└─ Taxation?
   └─ CONCURRENT - both can tax (s51(ii))
```

### Which Court Heard This?

```
HIGH COURT OF AUSTRALIA
├─ Constitutional interpretation
├─ Disputes between states
├─ Special leave appeals
└─ TAG: CONSTITUTIONAL_APEX

FEDERAL COURT
├─ Corporations, IP, taxation, migration, admin law
├─ Appeals from lower federal courts
└─ TAG: FEDERAL_APPELLATE / FEDERAL_ORIGINAL

FEDERAL CIRCUIT & FAMILY COURT
├─ Division 1: Complex family law, appeals
│  └─ TAG: FEDERAL_FAMILY_APPELLATE
├─ Division 2: Most family law, migration, bankruptcy
│  └─ TAG: FEDERAL_ORIGINAL

WA FAMILY COURT (SPECIAL CASE)
├─ Married couples: Federal jurisdiction
├─ De facto couples: State jurisdiction
└─ TAG: STATE_FEDERAL_CONCURRENT

STATE SUPREME COURT
├─ Murder, manslaughter, serious crimes
├─ Complex civil matters
├─ Appeals from lower state courts
└─ TAG: STATE_APPELLATE / STATE_ORIGINAL_SUPERIOR

DISTRICT/COUNTY COURT (NSW, VIC, QLD, SA, WA only)
├─ Serious crimes (not murder/manslaughter)
├─ Civil claims up to ~$750k
└─ TAG: STATE_INTERMEDIATE

MAGISTRATES/LOCAL COURT
├─ Summary offences, minor crimes
├─ Civil claims under ~$100k
├─ Committal hearings
└─ TAG: STATE_ORIGINAL_INFERIOR

TERRITORY COURTS (ACT, NT)
├─ Same structure as states
└─ TAG: TERRITORY_SUPERIOR / TERRITORY_INFERIOR
```

### Section 109 Inconsistency Test

```
Is there inconsistency between Commonwealth and State law?

├─ Can you obey both laws simultaneously?
│  ├─ NO → Direct inconsistency → Commonwealth prevails
│  └─ YES → Continue to next test
│
└─ Does Commonwealth law intend to "cover the field"?
   ├─ YES → Indirect inconsistency → Commonwealth prevails
   └─ NO → Both laws operate → No inconsistency
```

---

## Power Distribution at a Glance

### EXCLUSIVE FEDERAL (Only Commonwealth)

| Subject | Constitutional Basis | Examples |
|---------|---------------------|----------|
| **Defence** | s51(vi) | ADF, military operations |
| **Foreign Affairs** | s51(xxix) | Treaties, diplomatic relations |
| **Immigration** | s51(xxvii) | Visas, border control |
| **Customs/Excise** | s90 | Import duties, excise taxes |
| **Coinage** | s51(xii) | Currency, legal tender |
| **Naturalization** | s51(xix) | Citizenship |
| **Seat of Government** | s52(i) | ACT as capital |

### CONCURRENT (Both, but Commonwealth prevails if inconsistent)

| Subject | Constitutional Basis | Current Status | Examples |
|---------|---------------------|----------------|----------|
| **Marriage** | s51(xxi) | Cth occupied | Marriage Act 1961 |
| **Divorce** | s51(xxii) | Cth occupied | Family Law Act 1975 |
| **Bankruptcy** | s51(xvii) | Cth occupied | Bankruptcy Act 1966 |
| **Corporations** | s51(xx) | Cth extensive | Corporations Act 2001 |
| **Industrial Relations** | s51(xxxv) | Cth extensive | Fair Work Act 2009 |
| **Taxation** | s51(ii) | Both active | Income tax (Cth), payroll tax (State) |
| **Trade & Commerce** | s51(i) | Both active | Competition law (Cth), consumer law (State) |
| **Banking** | s51(xiii) | Cth extensive | Banking Act 1959 |
| **Insurance** | s51(xiv) | Cth extensive | Insurance Act 1973 |

### RESIDUAL STATE (Only States)

| Subject | Examples |
|---------|----------|
| **Criminal Law** | Crimes Act (NSW), Criminal Code (QLD, WA, TAS) |
| **Land Law** | Real Property Act, Planning & Environment Act |
| **Contract/Tort** | Common law, state legislation |
| **Education** | Education Act, school regulation |
| **Health** | Public Health Act, hospitals |
| **Police** | Police Act, state police forces |
| **Roads** | Road Traffic Act, driver licensing |
| **Local Government** | Local Government Act |

---

## Court Jurisdiction by Subject Matter

| Subject | Court(s) with Jurisdiction |
|---------|---------------------------|
| **Constitutional interpretation** | High Court |
| **Federal law (general)** | Federal Court, FCFCOA Div 2 |
| **Family law (married)** | FCFCOA Div 1 & 2 (except WA) |
| **Family law (WA married)** | WA Family Court (federal jurisdiction) |
| **Family law (WA de facto)** | WA Family Court (state jurisdiction) |
| **Murder/Manslaughter** | State Supreme Court |
| **Serious crimes** | State District/County Court OR Supreme Court |
| **Summary offences** | State Magistrates/Local Court |
| **Federal crimes** | Federal Court, FCFCOA Div 2 |
| **Migration** | Federal Court, FCFCOA Div 2 |
| **Bankruptcy** | Federal Court, FCFCOA Div 2 |
| **Corporations** | Federal Court, State Supreme Court |
| **IP/Trade Marks** | Federal Court |
| **Taxation disputes** | Federal Court, AAT |
| **Admin law review** | Federal Court, State Supreme Court |
| **Civil claims (large)** | State Supreme Court, Federal Court (federal matters) |
| **Civil claims (medium)** | State District/County Court |
| **Civil claims (small)** | State Magistrates/Local Court |

---

## Territory Special Rules

### Self-Governing Territories (ACT, NT)

**Can legislate on:**
- Any matter not inconsistent with Commonwealth law
- Any matter not exclusive to Commonwealth

**Cannot legislate on:**
- Customs/excise (s90)
- Defence
- Foreign affairs
- Immigration

**Subject to:**
- Section 122 Commonwealth override power
- Example: NT euthanasia law overturned 1997

**Court status:**
- Territory courts are NOT Chapter III courts
- Judges lack s72 constitutional protections
- Appeals to High Court only (no intermediate court)

### External Territories

**Norfolk Island:**
- Limited self-government (reduced 2015/2016)
- NSW law applies (via Commonwealth)

**Christmas Island & Cocos Islands:**
- WA law applies (via Commonwealth)

**Uninhabited Territories:**
- Ashmore & Cartier, Coral Sea Islands, Heard & McDonald, Antarctic Territory
- Direct Commonwealth governance

---

## WA Family Law Special Case

| Relationship Type | Court | Jurisdiction | Legislation |
|-------------------|-------|--------------|-------------|
| **Married couples** | WA Family Court | **Federal** | Family Law Act 1975 (Cth) |
| **De facto couples** | WA Family Court | **State** | Family Court Act 1997 (WA) |

**Appeals:**
- Federal jurisdiction → Federal Circuit & Family Court (Cth)
- State jurisdiction → WA Supreme Court

**All other states/territories:**
- Use Federal Circuit & Family Court for all family law
- De facto relationships: referred to Commonwealth under s51(xxxvii)

---

## Tagging Shorthand

### Court Authority Tags
```
HCA    = CONSTITUTIONAL_APEX
FCA    = FEDERAL_APPELLATE / FEDERAL_ORIGINAL
FCFCOA = FEDERAL_FAMILY_APPELLATE / FEDERAL_ORIGINAL
WAFC   = STATE_FEDERAL_CONCURRENT
SSC    = STATE_APPELLATE / STATE_ORIGINAL_SUPERIOR
DC/CC  = STATE_INTERMEDIATE
MC/LC  = STATE_ORIGINAL_INFERIOR
```

### Constitutional Authority Tags
```
s51    = SECTION_51_CONCURRENT
s52    = SECTION_52_EXCLUSIVE
s90    = SECTION_90_EXCLUSIVE
s109   = SECTION_109_INCONSISTENCY
s122   = SECTION_122_TERRITORIES
RES    = RESIDUAL_STATE
```

### Geographic Tags
```
States: NSW, VIC, QLD, WA, SA, TAS
Self-governing territories: ACT, NT
External territories: NORFOLK, CHRISTMAS, COCOS, etc.
National: JURISDICTION_NATIONAL
```

---

## Common Pitfalls to Avoid

### 1. Don't assume all family law is federal
- **WA de facto relationships = STATE LAW**
- Married couples everywhere = Federal
- De facto in other states = Federal (referred power)

### 2. Don't confuse concurrent with exclusive
- **Concurrent** = both can legislate, Commonwealth prevails if inconsistent
- **Exclusive** = only Commonwealth can legislate
- Example: Marriage is concurrent (s51(xxi)) but Commonwealth has occupied field

### 3. Don't treat territory courts like state courts
- Territory courts are NOT Chapter III courts
- No s72 protections for judges
- Subject to s122 override
- Different constitutional status

### 4. Don't forget states without intermediate courts
- **Tasmania, ACT, NT** have NO District/County Court
- Jump from Magistrates directly to Supreme Court

### 5. Don't assume all criminal law is state law
- Most criminal law = state residual power
- BUT federal crimes exist (tax evasion, immigration offences, customs, terrorism, etc.)
- Federal crimes heard in Federal Court or FCFCOA Div 2

### 6. Don't mix up s51 and s52
- **s51** = 39 concurrent powers (mostly)
- **s52** = 3 exclusive powers
- Some s51 powers are practically exclusive (defence, foreign affairs)

### 7. Remember corporations power is very broad
- **s51(xx)** extends to regulating corporate conduct in otherwise state areas
- Commonwealth can regulate workplace safety, consumer protection via corporations power
- Workchoices case expanded this significantly

---

## Key Cases for Reference

| Case | Year | Principle | Tag |
|------|------|-----------|-----|
| **Commonwealth v Australian Capital Territory** | 2013 | Marriage power includes same-sex marriage | s51(xxi), HCA |
| **Workchoices Case** (NSW v Commonwealth) | 2006 | Broad corporations power for IR | s51(xx), HCA |
| **Tasmanian Dams Case** | 1983 | Broad external affairs power | s51(xxix), HCA |
| **Clyde Engineering v Cowburn** | 1926 | Cover the field test for s109 | s109, HCA |

---

## Quick Validation Checklist

When tagging a document, ask:

- [ ] What is the subject matter?
- [ ] Which level of government has power?
- [ ] Is it exclusive, concurrent, or residual?
- [ ] Which court decided it?
- [ ] What is the geographic scope?
- [ ] Does s109 apply (state law inconsistent with Cth)?
- [ ] Is it a territory matter (s122)?
- [ ] Special case: WA family law de facto?
- [ ] Special case: Territory court (not Chapter III)?

---

**Version:** 1.0
**Date:** November 29, 2025
**Use:** Quick lookup for Jurisdictional Sentinel Agent
**Full Reference:** See `AUSTRALIAN_JURISDICTIONAL_HIERARCHY.md`
