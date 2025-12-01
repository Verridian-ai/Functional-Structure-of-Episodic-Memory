# Australian Court Citations - Quick Reference Guide

**For:** Citator & Ratio Miner Agents | **Version:** 1.0 | **Date:** Nov 29, 2025

---

## 1. INSTANT CITATION DECODER

### Pattern Recognition

```
[YEAR] COURT_CODE NUMBER [PARAGRAPH]
  ↓        ↓         ↓          ↓
[2024]   HCA       15        [42]
```

**Example:** `Smith v Jones [2024] HCA 15 [42]`
- **2024** = Year decided
- **HCA** = High Court of Australia
- **15** = 15th judgment of 2024
- **[42]** = Paragraph 42 (pinpoint)

---

## 2. FEDERAL COURTS - CHEAT SHEET

| Code | Court | Binds | Level | Example |
|------|-------|-------|-------|---------|
| **HCA** | High Court of Australia | **ALL COURTS** | 1 | [2024] HCA 1 |
| **FCAFC** | Federal Court Full Court | FCA, FedCFamC | 2 | [2024] FCAFC 45 |
| **FCA** | Federal Court | FedCFamC | 3 | [2024] FCA 123 |
| **FedCFamC** | Federal Circuit & Family | Tribunals | 4 | [2024] FedCFamC 567 |
| **AATA** | Admin Appeals Tribunal | None | Tribunal | [2023] AATA 3456 |

**Obsolete (pre-2021):** FamCA, FamCAFC, FCCA

---

## 3. STATE SUPREME COURTS

| State | Code | Example | Binds | Appeals To |
|-------|------|---------|-------|------------|
| NSW | **NSWSC** | [2024] NSWSC 1 | NSWDC, NSWLC | NSWCA → HCA |
| VIC | **VSC** | [2024] VSC 1 | VCC, VMC | VSCA → HCA |
| QLD | **QSC** | [2024] QSC 1 | QDC, QMC | QCA → HCA |
| SA | **SASC** | [2024] SASC 1 | SADC, SAMC | SASCFC → HCA |
| WA | **WASC** | [2024] WASC 1 | WADC, WAMC | WASCA → HCA |
| TAS | **TASSC** | [2024] TASSC 1 | TASMC | TASCCA → HCA |
| ACT | **ACTSC** | [2024] ACTSC 1 | ACTMC | HCA |
| NT | **NTSC** | [2024] NTSC 1 | NTLC | NTCA → HCA |

---

## 4. STATE INTERMEDIATE & LOWER COURTS

### District/County Courts (Level 2)

| State | Code | Example |
|-------|------|---------|
| NSW | **NSWDC** | [2024] NSWDC 200 |
| VIC | **VCC** | [2024] VCC 200 |
| QLD | **QDC** | [2024] QDC 150 |
| SA | **SADC** | [2024] SADC 100 |
| WA | **WADC** | [2024] WADC 120 |

### Magistrates/Local Courts (Level 3)

| State | Code | Example |
|-------|------|---------|
| NSW | **NSWLC** | [2024] NSWLC 500 |
| VIC | **VMC** | [2024] VMC 500 |
| QLD | **QMC** | [2024] QMC 400 |
| SA | **SAMC** | [2024] SAMC 250 |
| WA | **WAMC** | [2024] WAMC 300 |
| TAS | **TASMC** | [2024] TASMC 150 |
| ACT | **ACTMC** | [2024] ACTMC 80 |
| NT | **NTLC** | [2024] NTLC 100 |

---

## 5. APPELLATE COURTS

| State | Code | Name | Example |
|-------|------|------|---------|
| NSW | **NSWCA** | Court of Appeal | [2024] NSWCA 100 |
| NSW | **NSWCCA** | Court of Criminal Appeal | [2024] NSWCCA 50 |
| VIC | **VSCA** | Court of Appeal | [2024] VSCA 50 |
| QLD | **QCA** | Court of Appeal | [2024] QCA 75 |
| SA | **SASCFC** | Full Court | [2024] SASCFC 20 |
| WA | **WASCA** | Court of Appeal | [2024] WASCA 30 |
| TAS | **TASCCA** | Court of Criminal Appeal | [2024] TASCCA 10 |
| NT | **NTCA** | Court of Appeal | [2024] NTCA 8 |

---

## 6. SUPER-TRIBUNALS

| State | Code | Court of Record? | Example |
|-------|------|------------------|---------|
| NSW | **NCAT** | ❌ No | [2024] NCAT 789 |
| VIC | **VCAT** | ❌ No | [2024] VCAT 456 |
| QLD | **QCAT** | ✅ **YES** (unique) | [2024] QCAT 234 |
| SA | **SACAT** | ❌ No | [2024] SACAT 67 |
| WA | **WASAT** or **SAT** | ❌ No | [2024] WASAT 45 |
| ACT | **ACAT** | ❌ No | [2024] ACAT 23 |
| NT | **NTCAT** | ❌ No | [2024] NTCAT 12 |

**Key Point:** Only QCAT is a court; others are tribunals (not binding precedents)

---

## 7. BINDING PRECEDENT RULES - ONE PAGE

### Rule 1: VERTICAL BINDING (up the hierarchy)

```
Higher Court → BINDS → Lower Court (same hierarchy)
```

**Examples:**
- ✅ NSWSC **BINDS** NSWDC
- ✅ HCA **BINDS** all courts
- ❌ NSWDC does NOT bind NSWSC

---

### Rule 2: HORIZONTAL (same level)

```
Same Level Court → PERSUASIVE → Same Level Court
```

**Examples:**
- 🟡 NSWSC **persuasive** on VSC (both supreme courts, different states)
- 🟡 FCA **persuasive** on NSWSC (different hierarchies)

---

### Rule 3: HIGH COURT SUPREMACY

```
HCA → BINDS → EVERY Australian court
```

**Special:** HCA follows own precedents but can overrule itself

---

### Rule 4: INTER-STATE

```
State Court → NOT binding → Other State Courts
```

**Example:** NSW Supreme Court persuasive (not binding) on Victorian Supreme Court

---

### Rule 5: FEDERAL vs STATE

```
Federal Court → NOT binding → State Courts
State Courts → NOT binding → Federal Court
```

**Exception:** Highly persuasive when interpreting same Commonwealth law

---

## 8. DISTINGUISHING vs OVERRULING

| Action | Who Can Do It | Effect | Example |
|--------|---------------|--------|---------|
| **Distinguish** | Any court | "This precedent doesn't apply because facts differ" | Lower court avoiding unwanted precedent |
| **Overrule** | Higher court only | "That precedent was **wrong**" | HCA overruling HCA; QCA overruling QSC |
| **Reverse** | Appellate court | "This decision in **this case** is wrong" | Appeal in same case |

**Key Difference:**
- **Distinguish** = "Precedent doesn't apply here"
- **Overrule** = "Precedent is bad law everywhere"

---

## 9. RATIO vs OBITER - INSTANT CHECK

### Is it Ratio Decidendi? (BINDING)

✅ **YES if:**
- Necessary for the decision
- Court says "We hold that..."
- Remove it → outcome changes

❌ **NO if (Obiter):**
- Hypothetical scenario
- Alternative reasoning not used
- Court says "In passing we note..."
- General commentary

---

## 10. AUTHORIZED REPORT SERIES

### Federal

| Code | Court | Example |
|------|-------|---------|
| **CLR** | Commonwealth Law Reports (HCA) | (2020) 271 CLR 657 |
| **FCR** | Federal Court Reports | (2018) 265 FCR 123 |
| **FamLR** | Family Law Reports | (2019) 58 FamLR 456 |

### State

| Code | State | Example |
|------|-------|---------|
| **NSWLR** | NSW Law Reports | (2022) 108 NSWLR 234 |
| **VR** | Victorian Reports | (2021) 62 VR 567 |
| **Qd R** | Queensland Reports | (2023) 5 Qd R 123 |
| **SASR** | SA State Reports | (2020) 130 SASR 89 |
| **WAR** | WA Reports | (2019) 50 WAR 345 |
| **Tas R** | Tasmanian Reports | (2018) 27 Tas R 12 |

### Unofficial (Cross-Jurisdictional)

| Code | Name | Coverage |
|------|------|----------|
| **ALR** | Australian Law Reports | General, significant cases |
| **ALJR** | Australian Law Journal Reports | HCA, appellate |
| **A Crim R** | Australian Criminal Reports | Criminal law |

---

## 11. CITATION PREFERENCE ORDER

When multiple citations exist, cite in this order:

```
1st Choice: Authorized Report
    ↓
2nd Choice: Medium Neutral
    ↓
3rd Choice: Unofficial Report
    ↓
4th Choice: AustLII URL
```

**Full Citation Format:**
`Case Name [Year] MNC; (Year) Volume Report Page`

**Examples:**
- `Kadir v The Queen [2020] HCA 1; (2020) 271 CLR 657`
- `Hill v Lang [2012] FCA 349; (2012) 201 FCR 456`

---

## 12. COMMON ERRORS TO AVOID

| ❌ Error | ✅ Correct |
|---------|-----------|
| Year in round brackets: (2024) | Square brackets: **[2024]** |
| Missing court code: [2024] 15 | Include court: **[2024] HCA 15** |
| Assuming NCAT binds VCAT | Tribunals are **persuasive only** |
| Saying FCA binds state courts | FCA is **persuasive** (not binding) |
| Using FamCA for 2024 case | Use **FedCFamC** (FamCA defunct 2021) |
| Thinking QCAT is just a tribunal | QCAT is a **court of record** |

---

## 13. AGENT DECISION TREE

### Is This Precedent Binding?

```
START: Court A decision → Applied in Court B

1. Is Court A = HCA?
   YES → BINDING on all courts ✅
   NO → Go to step 2

2. Is Court B in same state/hierarchy as Court A?
   NO → PERSUASIVE (stop) 🟡
   YES → Go to step 3

3. Is Court A higher than Court B?
   NO → PERSUASIVE (stop) 🟡
   YES → Go to step 4

4. Are facts sufficiently similar?
   NO → Can distinguish (not binding) 🟡
   YES → Go to step 5

5. Is principle ratio decidendi (not obiter)?
   NO → NOT BINDING 🟡
   YES → BINDING ✅
```

---

## 14. ABBREVIATION LOOKUP TABLE

### Quick Decode Chart

```
HCA    → High Court of Australia (binds all)
FCA    → Federal Court of Australia
FCAFC  → Federal Court Full Court

NSWSC  → NSW Supreme Court
NSWCA  → NSW Court of Appeal
NSWDC  → NSW District Court
NSWLC  → NSW Local Court

VSC    → Victorian Supreme Court
VSCA   → Victorian Court of Appeal
VCC    → Victorian County Court
VMC    → Victorian Magistrates

QSC    → Queensland Supreme Court
QCA    → Queensland Court of Appeal
QDC    → Queensland District Court

NCAT   → NSW Civil & Admin Tribunal (not a court)
VCAT   → Victorian Civil & Admin Tribunal (not a court)
QCAT   → Queensland Civil & Admin Tribunal (IS a court!)
```

---

## 15. ONE-MINUTE JURISDICTION CHECK

### Federal Matters

**Heard in:** HCA, FCA, FedCFamC

**Examples:**
- Constitutional challenges
- Taxation
- Immigration
- Intellectual property
- Corporations law
- Family law
- Administrative review

---

### State Matters

**Heard in:** State Supreme/District/Magistrates Courts

**Examples:**
- Criminal offences (murder, assault, theft)
- Contract disputes (non-federal)
- Tort claims (negligence, defamation)
- Property law
- Wills and estates
- Most civil disputes

---

### Tribunal Matters

**Heard in:** NCAT, VCAT, QCAT, etc.

**Examples:**
- Residential tenancies
- Planning disputes
- Guardianship
- Small claims
- Anti-discrimination
- Administrative review (state)

---

## 16. REGEX PATTERNS FOR CITATION PARSING

### Medium Neutral Citation

```regex
\[(\d{4})\]\s+([A-Z]{2,10})\s+(\d+)(?:\s+\[(\d+)\])?
```

**Captures:**
1. Year: `2024`
2. Court: `HCA`
3. Number: `15`
4. Paragraph (optional): `42`

---

### Law Report Citation

```regex
\((\d{4})\)\s+(\d+)\s+([A-Z][A-Za-z\s]+[A-Z])\s+(\d+)
```

**Captures:**
1. Year: `2020`
2. Volume: `271`
3. Report: `CLR`
4. Page: `657`

---

## 17. PRECEDENT STRENGTH SCALE

```
BINDING LEVEL: Must Follow
└─ High Court → All Courts (100% binding)
└─ Appellate → Lower in same state (100% binding)
└─ Superior → Inferior in hierarchy (100% binding)

HIGHLY PERSUASIVE: Should Follow
└─ Federal Court → State courts (same law)
└─ Other state Supreme Courts (well-reasoned)
└─ UK Supreme Court (historical ties)

PERSUASIVE: May Follow
└─ Same level different state
└─ Lower court in same state
└─ Commonwealth jurisdictions (Canada, NZ)

WEAKLY PERSUASIVE: Consider
└─ Tribunal decisions
└─ Foreign non-Commonwealth jurisdictions
└─ Obiter dicta from higher courts
```

---

## 18. WHEN TO CITE WHICH COURT

| Your Case Involves | Cite Precedents From |
|--------------------|---------------------|
| Constitutional issue | **HCA** primary |
| Federal taxation | **HCA, FCA** |
| NSW criminal law | **HCA, NSWCA, NSWCCA, NSWSC** |
| Victorian contract dispute | **HCA, VSCA, VSC** + persuasive from NSW |
| Family law | **HCA, FedCFamC(FC), FamCA (historic)** |
| Residential tenancy | **NCAT, VCAT, QCAT** (persuasive only) |
| Administrative law | **HCA, FCA, State Supreme Courts** |

---

## 19. GLOSSARY - 30 SECONDS

| Term | Meaning |
|------|---------|
| **Stare Decisis** | "Stand by decisions" - follow precedent |
| **Ratio Decidendi** | Binding legal reasoning |
| **Obiter Dicta** | Non-binding commentary |
| **Distinguish** | Show case is different, precedent doesn't apply |
| **Overrule** | Declare precedent wrong |
| **Reverse** | Overturn decision on appeal (same case) |
| **Binding** | Must follow |
| **Persuasive** | Should consider, not required |
| **Medium Neutral** | Court-assigned citation [YEAR] COURT NUM |
| **Authorized Report** | Official law report series (CLR, FCR, etc.) |
| **Court of Record** | Court whose decisions are formal precedents |

---

## 20. EMERGENCY LOOKUP

### "I need to know RIGHT NOW if this precedent binds!"

**Step 1:** Identify both courts
**Step 2:** Ask three questions:

```
Q1: Is precedent from HCA?
    YES → BINDS all courts ✅

Q2: Same state/territory?
    NO → Persuasive only 🟡

Q3: Is precedent court higher?
    NO → Persuasive only 🟡
    YES → BINDING ✅
```

**Example:**
- Precedent: [2020] NSWCA 50 (NSW Court of Appeal)
- Current case: In NSWDC (NSW District Court)
- Q1: HCA? No
- Q2: Same state? Yes (both NSW)
- Q3: Higher? Yes (CA > DC)
- **Result: BINDING** ✅

---

**END QUICK REFERENCE**

**For full details, see:** `AUSTRALIAN_COURT_HIERARCHY_AND_PRECEDENT.md`
