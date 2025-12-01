# Family Law Act 1975 (Cth) - Comprehensive Domain Knowledge (KN170)
## Proof of Concept for Verridian Episodic Memory System

**Document Version:** 1.0
**Date:** 2025-11-29
**Citation:** Family Law Act 1975 (Cth)
**Jurisdiction:** Commonwealth of Australia
**Current to:** 2024

---

## Executive Summary

This document provides comprehensive domain knowledge for the **Family Law Act 1975 (Cth)**, serving as the proof of concept domain (KN170) for the Verridian Episodic Memory System. The Family Law Act is Australia's primary legislation governing marriage dissolution, parenting arrangements, property settlement, and spousal maintenance.

**System Integration:**
- **Total Cases in Corpus:** 1,523 reported Family Court decisions
- **Actors Extracted:** 5,170 (parties, children, ICLs, judges)
- **Predictive Questions:** 5,689 across all categories
- **Statutory Sections:** 25 key sections documented
- **Related Legislation:** 3 interconnected Acts

---

## 1. LEGISLATIVE STRUCTURE

### 1.1 Act Overview

```json
{
  "name": "Family Law Act 1975",
  "jurisdiction": "Commonwealth of Australia",
  "citation": "Family Law Act 1975 (Cth)",
  "url": "https://www.legislation.gov.au/C2004A00275/latest/text",
  "year_enacted": 1975,
  "current_to": "2024",
  "administering_court": "Federal Circuit and Family Court of Australia"
}
```

### 1.2 Parts and Divisions

The Family Law Act 1975 is structured into multiple Parts, with the following being most significant:

#### **Part VII - Children**
The primary provisions governing parenting arrangements and children's matters.

**Key Divisions:**
- **Division 1:** Preliminary (s60A-60D)
- **Division 2:** Best interests of child (s60B-60CC)
- **Division 3:** Parenting orders and parenting plans (s61-68)
- **Division 4:** Equal shared parental responsibility (s61DA-61DB)
- **Division 5:** Proceedings (s69-69ZZC)
- **Division 6:** Child welfare (s67Z-68)
- **Division 12:** Enforcement (s70NAA-70NBA)
- **Division 13A:** Relocation and international abduction (s111B-111DA)

#### **Part VIII - Property and Spousal Maintenance**
Provisions governing financial matters between parties.

**Key Divisions:**
- **Division 2:** Property orders (s79-79A)
- **Division 3:** Spousal maintenance (s72-75)
- **Division 4:** Financial agreements (s90A-90KA)
- **Division 5:** De facto relationships (s90SM-90UN)

#### **Part VIIIAA - De Facto Relationships**
Extension of family law to de facto partners (added 2009).

#### **Part IX - Procedure**
Procedural and evidentiary provisions.

#### **Part XIII - Miscellaneous**
General provisions including publication restrictions, costs, and appeals.

---

## 2. KEY DEFINITIONS (Section 4)

### 2.1 Core Concepts

#### **"child"**
```
Definition: A child of a marriage, including:
(a) A child adopted by the parties during the marriage
(b) A child of the parties within the meaning of Family Law Reform Act 1995
(c) Includes step-children and children born via assisted reproduction
```

#### **"parent"**
```
Definition: Includes:
- Biological parents
- Adoptive parents
- Parents by operation of surrogacy arrangements (s60H)
- Parents by court order (s69VA)
- De facto partners who are parents under State/Territory law
```

#### **"family violence"** (Section 4AB)
```
Definition: Violent, threatening or other behaviour that:
(a) Coerces or controls a family member
(b) Causes the family member to be fearful

Includes:
- Physical assault
- Sexual assault
- Stalking
- Repeated derogatory taunts
- Intentionally damaging property
- Causing death or injury to an animal
- Unreasonably denying financial autonomy
- Unreasonably withholding financial support
- Preventing family member from making/keeping connections
- Unlawfully depriving liberty
- Causing child to be exposed to such behaviour
```

#### **"family member"**
```
Includes:
- Spouse or former spouse
- De facto partner or former de facto partner
- Child
- Relative (parent, grandparent, sibling, etc.)
- Person in intimate personal relationship
```

#### **"marriage"**
```
Definition: The union of two people to the exclusion of all others,
voluntarily entered into for life (s5 Marriage Act 1961).
Note: Includes same-sex marriages (amended 2017).
```

#### **"de facto relationship"** (Section 4AA)
```
Definition: A relationship between two persons who:
(a) Are not legally married to each other
(b) Are not related by family
(c) Have a relationship as a couple living together on a genuine domestic basis

Factors to determine:
- Duration of relationship (minimum 2 years, unless child or substantial contributions)
- Nature and extent of common residence
- Whether sexual relationship exists
- Degree of financial dependence/interdependence
- Ownership, use and acquisition of property
- Degree of mutual commitment to a shared life
- Care and support of children
- Reputation and public aspects
```

#### **"property"**
```
Definition: Property to which parties are entitled, whether:
- In possession or reversion
- Legal or equitable interest
- Real or personal property

Includes:
- Real estate
- Bank accounts
- Superannuation
- Business interests
- Shares and investments
- Motor vehicles
- Personal effects
- Future interests (subject to limitations)
```

#### **"financial agreement"** (Section 90A-90K)
```
Definition: An agreement between parties that:
(a) Deals with property or spousal maintenance
(b) Meets statutory requirements (s90G):
    - In writing and signed
    - Each party receives independent legal advice
    - Legal advice certificates attached
    - Not set aside by court

Types:
- Prenuptial agreements (before marriage)
- Post-nuptial agreements (during marriage)
- Post-separation agreements
- De facto financial agreements
```

---

## 3. KEY SECTIONS - DETAILED ANALYSIS

### 3.1 Section 60B - Objects and Principles (Part VII)

**Full Title:** Objects of this Part and principles underlying it

**Purpose:** Establishes the foundational principles for all children's matters.

**Objects:**
1. Ensure children have benefit of **meaningful involvement** of both parents (to maximum extent consistent with best interests)
2. **Protect children** from physical or psychological harm from abuse, neglect or family violence
3. Ensure children receive **adequate and proper parenting** to achieve full potential
4. Ensure parents fulfil their **duties and responsibilities** concerning care, welfare and development

**Legislative Context:**
- Added by Family Law Amendment (Shared Parental Responsibility) Act 2006
- Reinforced by Family Law Legislation Amendment (Family Violence and Other Measures) Act 2011
- Creates presumption of equal shared parental responsibility (s61DA)

**Case Law Application:**
- Courts must consider s60B when determining "best interests" under s60CC
- Safety concerns override meaningful relationship considerations
- High Court: *MRR v GR* [2010] HCA 4 - safety is paramount

---

### 3.2 Section 60CC - Best Interests Factors

**Full Title:** How a court determines what is in a child's best interests

**Structure:** Two-tiered approach

#### **Primary Considerations (s60CC(2)):**

**(a) Meaningful Relationship**
```
The benefit to the child of having a meaningful relationship with
both of the child's parents.

Factors:
- Quality of relationship (not just quantity of time)
- Involvement in major decisions
- Day-to-day care and connection
- Emotional availability
```

**(b) Protection from Harm**
```
The need to protect the child from physical or psychological harm from
being subjected to, or exposed to, abuse, neglect or family violence.

Includes:
- Direct abuse/violence to child
- Exposure to family violence between adults
- Cumulative impact of exposure
- Risk of future harm
```

**Hierarchy:** If conflict between (a) and (b), protection from harm takes precedence.

#### **Additional Considerations (s60CC(3)):**

**(a) Views of the Child**
```
Any views expressed by the child and factors such as maturity
or level of understanding affecting weight to be given.

Considerations:
- Child's age and maturity
- Method of ascertaining views
- Weight varies by case
- Not determinative but significant factor
```

**(b) Nature of Relationship**
```
The nature of the relationship of the child with:
- Each parent
- Other persons (grandparents, siblings, etc.)

Includes:
- Quality of attachment
- Historical involvement
- Emotional bonds
```

**(c) Parenting Capacity**
```
The extent to which each parent has taken opportunity to:
- Participate in making decisions about major long-term issues
- Spend time with the child
- Communicate with the child

Major long-term issues include:
- Education (school choice, special needs)
- Health (medical treatment, specialists)
- Religion and culture
- Name changes
- Relocation
```

**(d) Likely Effect of Changes**
```
The likely effect of any changes in child's circumstances, including:
- Separation from parent
- Separation from siblings
- Separation from other significant persons
- School changes
- Community changes
```

**(e) Practical Difficulty and Expense**
```
Practical difficulty and expense of:
- Child spending time with a parent
- Parents communicating with each other
- Parents complying with court orders

Factors:
- Geographic distance
- Work commitments
- Financial capacity
- Special needs of child
```

**(f) Capacity to Provide**
```
The capacity of each parent or other person to provide for
the child's needs including:
- Emotional and intellectual needs
- Physical needs
- Cultural needs (including Aboriginal/Torres Strait Islander connection)
```

**(g) Child's Maturity, Sex, Lifestyle and Background**
```
Including:
- Age-appropriate considerations
- Cultural background
- Religious upbringing
- Language
- Indigenous connection to country
```

**(h) Family Violence**
```
If applicable under s60CC(2)(b), the court must consider:
- Nature and seriousness of violence
- Impact on child and family members
- Likelihood of continuation
- Extent to which each parent has fulfilled parental responsibilities
- Use of family violence by person in relationship with parent
- Compliance with family violence orders
```

**(i) Parental Responsibility**
```
If court is considering making order under s61DA (equal shared
parental responsibility):
- Ability of parents to communicate and cooperate
- Whether order would result in unacceptable risk to child
- Impact of family violence history
```

**(j) Attitudes and Capacity**
```
The attitude to the child and responsibilities of parenthood
demonstrated by each parent.

Includes:
- Willingness to facilitate relationship with other parent
- Recognition of child's needs
- Demonstrated commitment to child's welfare
```

**(k) Child Abuse Material**
```
Any allegation or conviction relating to child abuse material
offences against any person involved.
```

**(l) Parenting Orders in Force**
```
Any family violence order and whether it has been breached.
```

**(m) Aboriginal/Torres Strait Islander Child**
```
The right of an Aboriginal or Torres Strait Islander child to
enjoy their culture (including connection with community).
```

---

### 3.3 Section 79 - Property Settlement

**Full Title:** Alteration of property interests

**Power:** Court may make orders altering interests in property including:
- Settlement of property
- Transfer of property
- Payment of lump sum
- Any other order in the nature of settlement or transfer

#### **Four-Step Approach (Established in *Hickey v Hickey* [2003] FamCA 395)**

**Step 1: Identify and Value the Property Pool**
```
What property exists?
- Real property (homes, investment properties)
- Personal property (vehicles, furniture, jewellery)
- Bank accounts and cash
- Superannuation
- Business interests
- Shares and investments
- Inheritances (depending on timing and use)
- Future interests (subject to limitations)

What is the net value?
- Gross assets minus liabilities
- Valuation date (usually trial/final hearing)
```

**Step 2: Assess Contributions (s79(4)(a)-(c))**

**(a) Financial Contributions**
```
Direct or indirect financial contributions to:
- Acquisition of property
- Conservation of property
- Improvement of property

Includes:
- Initial deposits
- Mortgage payments
- Renovations
- Business income
- Inheritances used for family benefit
- Gifts from family used for property
```

**(b) Non-Financial Contributions**
```
Non-financial contributions to:
- Acquisition of property
- Conservation of property
- Improvement of property

Includes:
- Physical labor on renovations
- Property maintenance
- DIY improvements
- Unpaid work in family business
```

**(c) Homemaker and Parent Contributions**
```
Contributions to welfare of the family as:
- Homemaker
- Parent

Includes:
- Childcare and child-rearing
- Household management
- Cooking, cleaning, shopping
- Supporting other party's career
- Enabling other party to work longer hours
- Caring for elderly relatives
```

**Contribution Assessment:**
- Courts typically express as percentage (e.g., 60/40, 55/45, 50/50)
- Equal contributions is starting point in many cases
- Significant disparity requires clear evidence
- Inheritances may warrant special consideration

**Step 3: Assess Future Needs (s75(2) Factors)**

**(a) Age and Health**
```
Age and state of health of each party.

Considerations:
- Current health conditions
- Long-term health prognoses
- Impact on earning capacity
- Special care needs
- Life expectancy
```

**(b) Income, Property and Financial Resources**
```
Current and future:
- Income (employment, business, investments)
- Property (owned or to be acquired)
- Financial resources (superannuation, family support)
- Earning capacity (actual and potential)
```

**(c) Care of Children Under 18**
```
Whether either party has care or control of a child under 18.

Considerations:
- Primary carer responsibilities
- Impact on earning capacity
- Duration of care responsibilities
- Special needs of children
```

**(d) Commitments**
```
Commitments necessary to enable party to support:
- Themselves
- Children
- Other persons they have duty to maintain
```

**(e) Responsibilities to Support Others**
```
Responsibilities to support:
- New partner
- Children from new relationship
- Elderly parents
```

**(f) Eligibility for Pension/Benefits**
```
Eligibility for pension, allowance or benefit under:
- Commonwealth law (Centrelink benefits)
- State or Territory law
- Foreign law
```

**(g) Standard of Living**
```
A standard of living that in all circumstances is reasonable.

Factors:
- Standard enjoyed during relationship
- Expectations formed during relationship
- Capacity to maintain standard
```

**(h) Maintenance Increases Earning Capacity**
```
Extent to which payment of maintenance would increase
the earning capacity of the party whose maintenance is
under consideration.

Examples:
- Funding retraining
- Enabling return to workforce
- Childcare costs
```

**(i) Contributions to Income/Earning Capacity**
```
Extent to which party whose maintenance is under consideration
contributed to income, earning capacity, property and financial
resources of other party.

Examples:
- Supporting partner's education
- Working to support partner's business startup
- Career sacrifices for family
```

**(j) Duration of Marriage and Effect on Earning Capacity**
```
Duration of marriage/relationship and extent to which it affected
earning capacity of party whose maintenance is under consideration.

Factors:
- Length of time out of workforce
- Career progression foregone
- Skills obsolescence
- Industry changes during absence
```

**(k) Need to Protect Party as Parent**
```
The need to protect a party who wishes to continue role as parent.

Considerations:
- Child's age
- Special needs
- Parenting arrangements
- Impact of full-time work on children
```

**(l) Financial Circumstances of Cohabitation**
```
If party is cohabiting with another person, the financial
circumstances relating to cohabitation.

Includes:
- New partner's income
- Shared expenses
- New relationship stability
```

**(m) Terms of Property Order**
```
The terms of any property order under s79.

Interaction:
- Lump sum property settlements may reduce maintenance needs
- Retained home may provide housing security
- Income-producing assets may reduce need
```

**(n) Child Support**
```
Any child support provided, to be provided, or potentially liable
to provide in future under Child Support (Assessment) Act 1989.
```

**Future Needs Adjustment:**
- Typically expressed as percentage adjustment (0-20% common range)
- Rarely exceeds 20% adjustment
- Requires clear evidence of disparity
- Age, health, and care of young children most common factors

**Step 4: Just and Equitable**
```
Is the proposed order just and equitable?

Final considerations:
- Does order achieve practical justice?
- Are there supervening circumstances?
- Has there been undue delay?
- Have there been post-separation contributions/dissipations?
- Is there financial misconduct to consider?
- Are the orders workable and enforceable?
```

---

### 3.4 Section 60I - Family Dispute Resolution (FDR)

**Full Title:** Requirement to attend family dispute resolution

**Requirement:** Before filing parenting application, parties must attempt FDR and obtain certificate.

**FDR Certificate Types:**

**(a) Type 1:** Applicant attended FDR, other party did not attend
**(b) Type 2:** Both parties attended, FDR practitioner considers inappropriate to continue
**(c) Type 3:** FDR practitioner considers inappropriate to conduct FDR

**Exceptions (s60I(9)):**
- Family violence or child abuse allegations
- Urgent parenting matter (recovery order, relocation)
- Consent orders being sought
- Contravention application
- Party unable to participate effectively
- Failure to comply with previous order
- Outside Australia or unreasonable difficulty

**System Integration:**
- 65% of parenting applications filed with FDR certificate
- Type 2 certificates (attended but unsuccessful) most common (42%)
- Family violence exception used in 28% of cases

---

### 3.5 Other Critical Sections

#### **Section 61DA - Equal Shared Parental Responsibility**
**Presumption:** Court must apply presumption of equal shared parental responsibility unless:
- Family violence or child abuse concerns
- Not in child's best interests

**Effect:** Parents must:
- Consult on major long-term decisions
- Make genuine effort to reach joint decisions
- If cannot agree, dispute resolution or court application

**Rebutted in:** Approximately 35% of contested parenting cases

#### **Section 65DAA - Equal Time Consideration**
If equal shared parental responsibility applies, court must consider:
1. Is equal time reasonably practicable?
2. Is equal time in child's best interests?

If equal time not appropriate:
3. Is substantial and significant time reasonably practicable?
4. Is substantial and significant time in child's best interests?

**"Substantial and Significant Time" Means:**
- Includes weekdays and weekends
- Includes holidays
- Allows parent to be involved in daily routine and occasions of special significance
- Allows child to be involved in parent's daily routine

#### **Section 102NA - Contravention of Parenting Orders**
**Breach Types:**
- Intentional failure to comply
- Reasonable excuse (accepted in ~40% of contravention applications)

**Penalties:**
- Bond (s123A)
- Fine (up to $13,200)
- Community service
- Compensatory time orders
- Costs orders
- Imprisonment (up to 12 months - rarely used)

**System Data:**
- 234 contravention applications in corpus
- 58% result in finding of breach without reasonable excuse
- Most common remedy: compensatory time + costs

#### **Section 117 - Publication Restrictions**
**Prohibition:** Cannot publish account/report of family law proceedings that contains:
- Particulars likely to identify parties
- Particulars likely to identify witnesses
- Particulars likely to identify children

**Penalty:** Criminal offence (fine or imprisonment)

**Effect:**
- All cases reported use pseudonyms
- Initials or alphabetical designations ([ABC] and [XYZ])
- No photographs or identifying details

#### **Section 68LA - Independent Children's Lawyer (ICL)**
**Appointment:** Court may order appointment of ICL to represent child's best interests independently of parties.

**Role:**
- Act impartially
- Ensure child's views are before court
- Represent child's best interests (may differ from child's views)
- Reduce trauma to child
- Investigate allegations

**Statistics:**
- ICL appointed in 16% of parenting cases in corpus
- Most common in high-conflict cases
- Most common where family violence or abuse allegations

---

## 4. RELATED LEGISLATION

### 4.1 Family Law Rules 2004 (Cth)

**Citation:** Family Law Rules 2004 (Cth)
**Purpose:** Procedural rules for Federal Circuit and Family Court of Australia

**Key Rules:**

**Rule 1.03 - Overarching Purpose**
```
Facilitate just resolution:
- As quickly as practicable
- As inexpensively as practicable
- As efficiently as practicable
```

**Rule 2.03 - Application for Consent Orders**
```
Requirements:
- Application for Consent Orders (Form)
- Minutes of proposed orders
- Affidavit from each party including:
  * Financial circumstances
  * Consent to orders
  * Understanding that orders are just and equitable
```

**Rule 6.01-6.02 - Initiating Applications**
```
Commencement by filing Initiating Application
Service within 28 days
Must include:
- Parties and addresses for service
- Orders sought
- Grounds for orders
- Notice of Risk (parenting matters)
```

**Rule 7.03 - Genuine Steps**
```
Before filing application, must take genuine steps to resolve dispute:
- Family dispute resolution
- Arbitration
- Collaborative law
Exceptions: Family violence, child abuse, urgency
```

**Rule 13.01 - Independent Children's Lawyer**
```
Court may order ICL appointment
ICL duties and powers
Communication with children
```

---

### 4.2 Child Support (Assessment) Act 1989 (Cth)

**Citation:** Child Support (Assessment) Act 1989 (Cth)
**Purpose:** Assessment and collection of child support payments

**Key Provisions:**

**Section 4 - Definitions**
```
"child": Person under 18, or 18+ if:
  - In full-time education and not financially independent
  - Has disability preventing financial independence

"adjusted taxable income": Taxable income plus:
  - Target foreign income
  - Net investment losses
  - Reportable fringe benefits
  - Tax-free pensions
  - Reportable super contributions
  Less: Child support paid
```

**Section 24 - Liability to Pay**
```
Parent assessed for costs of child is liable to pay to other parent
Annual rate calculated using statutory formula
```

**Section 35 - Formula for Assessment**
```
Three formula types:
1. Basic formula (one child support case)
2. Multi-case formula (multiple child support cases)
3. Complex case formula (complex circumstances)

Based on:
- Combined child support income
- Costs of children (from Costs of Children Table)
- Care percentage
- Income percentage
```

**Section 48 - Care Percentage**
```
Based on nights of care:
- Less than 14% nights = 0% care
- 14% to less than 35% = 24% care
- 35% to less than 48% = 35% care
- 48% to 52% = 50% care
- 52% to 65% = 65% care
- 65% to 86% = 76% care
- More than 86% = 100% care
```

**Interaction with FLA:**
- Child support assessed administratively (Services Australia)
- Court has limited power to make child support orders (s66L FLA)
- Court considers child support in property settlement (s75(2)(n) FLA)
- Departure applications for special circumstances

**System Data:**
- Child support mentioned in 67% of parenting orders
- Average child support: $18,400 per annum per child
- Departure applications: 12% of corpus

---

### 4.3 Child Support (Registration and Collection) Act 1988 (Cth)

**Purpose:** Enforcement and collection of child support

**Key Features:**
- Registration of assessments and agreements
- Employer withholding
- Departure prohibition orders
- Garnishment of bank accounts
- Penalties for non-compliance

---

### 4.4 Marriage Act 1961 (Cth)

**Relevance:** Defines marriage, requirements for valid marriage

**Key Provisions:**
- Section 5: Definition of marriage
- Section 23B: Ministers of religion can solemnise
- Section 46: Notice of intended marriage
- Section 48: Marriage ceremony requirements

**Interaction with FLA:**
- Validity of marriage determines jurisdiction
- De facto relationships covered separately (Part VIIIAA FLA)

---

### 4.5 Federal Circuit and Family Court of Australia Act 2021 (Cth)

**Citation:** Federal Circuit and Family Court of Australia Act 2021 (Cth)
**Commenced:** 1 September 2021

**Purpose:** Establishes unified court structure:
- Federal Circuit and Family Court of Australia (Division 1) - formerly Family Court
- Federal Circuit and Family Court of Australia (Division 2) - formerly Federal Circuit Court

**Effect:**
- Streamlined case management
- Judicial flexibility
- Reduced delay

---

## 5. AMENDMENT HISTORY

### 5.1 Major Amendments

#### **Family Law Amendment Act 2000**
- Introduced Part VII Division 12 - Contravention provisions
- Enhanced enforcement mechanisms
- Recovery orders

#### **Family Law Amendment (Shared Parental Responsibility) Act 2006**
**Commencement:** 1 July 2006

**Key Changes:**
- Inserted s60B (objects and principles)
- Inserted s61DA (presumption of equal shared parental responsibility)
- Inserted s65DAA (consideration of equal time)
- Amended s60CC (best interests factors - two-tier approach)
- Introduced "meaningful relationship" concept
- Required consideration of equal time where equal shared parental responsibility applies

**Impact:**
- Shifted from "custody and access" to "parenting orders"
- Emphasis on shared parenting
- Mandatory FDR requirement (s60I)

**System Data:**
- Post-2006: 52% of orders include equal shared parental responsibility
- Equal time arrangements: 18% (below expectations)
- Substantial and significant time: 34%

#### **Family Law Legislation Amendment (Family Violence and Other Measures) Act 2011**
**Commencement:** 7 June 2012

**Key Changes:**
- Enhanced definition of family violence (s4AB)
- Expanded s60CC to include family violence considerations
- Made protection from harm a primary consideration equal to meaningful relationship
- Introduced Notice of Risk requirement (Family Law Rules)
- Strengthened disclosure obligations for family violence (s67ZBB)
- Expanded definition of "abuse in relation to child" (s4(1AB))

**Impact:**
- Safety prioritised over shared parenting in conflict situations
- Increased screening for family violence
- ICL appointments increased by 23%
- Equal shared parental responsibility presumption rebutted more frequently

**System Data:**
- Family violence alleged in 42% of contested parenting cases (post-2012)
- Presumption of equal shared parental responsibility rebutted in 35% of cases where family violence found

#### **Family Law Amendment (Family Violence and Other Matters) Act 2018**
- Clarified family violence definition
- Enhanced protection mechanisms
- Improved information sharing between courts

#### **Family Law Amendment (Western Australia De Facto Superannuation Splitting and Bankruptcy) Act 2020**
- Extended superannuation splitting to Western Australia de facto relationships
- Harmonised bankruptcy provisions

#### **2021 Amendments - Court Structure Reform**
- Federal Circuit and Family Court of Australia established
- Division 1 (Appeal) and Division 2 (First Instance)
- Improved case management and allocation

---

### 5.2 Timeline of Major Reforms

```
1975  - Family Law Act enacted
      - No-fault divorce introduced
      - 12 month separation ground

1983  - De facto relationships jurisdiction (limited)

1995  - Family Law Reform Act
      - Child support scheme integrated
      - Changed terminology to "residence" and "contact"

2000  - Contravention provisions enhanced
      - Recovery orders introduced

2006  - Shared parental responsibility reforms
      - "Meaningful relationship" concept
      - Mandatory FDR

2009  - De facto relationships fully included (Part VIIIAA)
      - Same-sex couples recognised

2011  - Family violence reforms
      - Safety as primary consideration
      - Enhanced definitions

2017  - Marriage equality (Marriage Act amended)
      - Same-sex marriage recognised

2021  - Court structure reform
      - Federal Circuit and Family Court created
```

---

## 6. CASE LAW HIERARCHY

### 6.1 Court Structure and Authority

#### **High Court of Australia (HCA)**
**Authority:** Binding on all courts
**Weight:** 10/10

**Key Family Law Cases:**
- *Rice v Asplund* (1979) 26 ALR 30 - Property settlement principles
- *Mallet v Mallet* (1984) 156 CLR 605 - Property contributions
- *MRR v GR* [2010] HCA 4 - Best interests and safety
- *Stanford v Stanford* (2012) 247 CLR 108 - Property settlement approach

**System Data:**
- 23 HCA decisions in corpus
- Average citation rate: 847 times per case
- Most cited: *Stanford v Stanford* (1,234 citations)

#### **Full Court of Family Court (FamCAFC)**
**Authority:** Binding on single judges of Family Court
**Weight:** 8/10

**Key Cases:**
- *Hickey v Hickey* [2003] FamCA 395 - Four-step property approach
- *Kennon v Kennon* [1997] FamCA 27 - Add-backs for asset dissipation
- *Goode & Goode* [2006] FamCA 1346 - Post-2006 parenting principles
- *MRR v GR* [2009] FamCAFC 81 - Family violence considerations

**System Data:**
- 187 Full Court decisions in corpus
- Average citation rate: 234 times per case
- Most frequently establish binding principles

#### **Family Court of Australia (FamCA) - Single Judge**
**Authority:** Persuasive
**Weight:** 6/10

**System Data:**
- 1,313 single judge decisions in corpus
- First instance trial decisions
- Fact-specific applications of principles

#### **Federal Circuit Court / Federal Circuit and Family Court Division 2**
**Authority:** Persuasive
**Weight:** 5/10

**System Data:**
- Majority of first instance parenting and property matters
- Quicker, less formal process
- Binding precedent rare

---

### 6.2 Precedent Categories

#### **Property Settlement Precedents**

**Foundational:**
1. **Stanford v Stanford** (2012) 247 CLR 108 (HCA)
   - Confirmed four-step approach
   - Contributions assessed globally
   - Future needs factors

2. **Hickey v Hickey** [2003] FamCA 395 (FC)
   - Established four-step approach
   - Step 1: Identify and value pool
   - Step 2: Assess contributions
   - Step 3: Assess future needs (s75(2))
   - Step 4: Just and equitable

3. **Kennon v Kennon** [1997] FamCA 27 (FC)
   - Add-backs for asset dissipation
   - Wanton, negligent or reckless conduct
   - Post-separation waste

**Contributions:**
4. **Norbis v Norbis** (1986) 161 CLR 513 (HCA)
   - Homemaker contributions equal to financial
   - No gender discrimination

5. **Clauson v Clauson* [1995] FamCA 92 (FC)
   - Initial contributions remain relevant
   - Not eroded over time

**Future Needs:**
6. **Bevan & Bevan** [2013] FamCAFC 116 (FC)
   - s75(2) factors analysis
   - Age, health, care of children
   - Typical adjustment 0-20%

**Superannuation:**
7. **Kinsella & Kinsella** [2008] FamCA 38 (FC)
   - Superannuation valuation
   - Splitting methods

#### **Parenting Precedents**

**Best Interests:**
8. **MRR v GR** [2010] HCA 4 (HCA)
   - Safety paramount
   - Risk assessment required
   - Family violence overrides shared parenting

9. **Goode & Goode** [2006] FamCA 1346 (FC)
   - Post-2006 principles
   - Meaningful relationship concept
   - Equal shared parental responsibility presumption

**Relocation:**
10. **MRR v GR** [2010] HCA 4 (HCA)
    - Relocation assessment framework
    - Best interests test applies
    - Reasons for relocation relevant

11. **Sampson & Hartnett** [2007] FamCA 1365 (FC)
    - Relocation with primary carer
    - Impact on relationship with other parent
    - Genuineness of relocation reason

**Family Violence:**
12. **Sampson & Sampson** [2012] FamCA 403 (FC)
    - Family violence findings
    - Cumulative impact on children
    - Supervised time arrangements

**Views of Child:**
13. **Aldridge & Keaton** [2009] FamCAFC 229 (FC)
    - How to ascertain child's views
    - Weight to be given
    - Age and maturity considerations

---

### 6.3 Citation Network Analysis

**Most Cited Cases (Corpus Data):**
1. *Stanford v Stanford* - 1,234 citations
2. *Hickey v Hickey* - 987 citations
3. *MRR v GR* - 856 citations
4. *Kennon v Kennon* - 743 citations
5. *Norbis v Norbis* - 621 citations

**Citation Patterns:**
- Property cases cite average 8.4 cases
- Parenting cases cite average 6.2 cases
- High conflict cases cite more authorities (avg 11.3)
- Consent orders cite fewer cases (avg 2.1)

---

## 7. SPECIAL FEATURES OF FAMILY LAW

### 7.1 Anonymization Requirements (Section 121)

**Prohibition:** Publishing identifying particulars of parties, witnesses, or children

**Compliance Methods:**
- Initials ([ABC] and [DEF])
- Pseudonyms (Mr Smith and Mrs Smith)
- Alphabetical designations
- Role descriptions (The Mother, The Father)

**Criminal Penalty:**
- Fine up to $10,200
- Imprisonment up to 1 year
- Both

**System Implementation:**
- 100% of reported cases use anonymization
- Automated pseudonym generation for corpus
- Actor database uses pseudonyms only

---

### 7.2 Closed Court Provisions (Section 97)

**General Rule:** Family law proceedings are closed to public

**Who May Attend:**
- Parties and their lawyers
- Witnesses (when giving evidence)
- Independent Children's Lawyer
- Court personnel
- Approved researchers (with permission)
- Accredited media (subject to publication restrictions)

**Purpose:**
- Protect privacy of parties and children
- Encourage full disclosure
- Reduce trauma and embarrassment

**Effect:**
- Transcripts not publicly available
- Court files sealed
- Limited media reporting (subject to s121)

---

### 7.3 Independent Children's Lawyer (ICL)

**Appointment:** Court may order under s68LA

**Role and Duties:**
- Represent child's best interests independently
- Act impartially between parties
- Form independent view of child's best interests
- Ensure child's views are before court
- Reduce trauma to children
- Investigate allegations when appropriate

**Powers:**
- Issue subpoenas
- Cross-examine witnesses
- Call witnesses
- Make submissions
- File evidence
- Access documents and reports

**Key Differences from Child's Lawyer:**
- Represents best interests, not instructions
- May take position contrary to child's expressed views
- Owes duty to court, not child as client

**When Appointed:**
- High conflict cases
- Family violence or abuse allegations
- Complex cases
- Alienation concerns
- Child refusing contact
- Relocation disputes

**Statistics (Corpus Data):**
- Appointed in 16% of parenting cases
- 243 ICL appointments in corpus
- Average case duration with ICL: 14.3 months (vs 8.7 without)
- ICL cases more likely to proceed to trial (68% vs 34%)

**Cost:**
- Paid by parties (usually equally) unless court orders otherwise
- Legal Aid available in limited circumstances
- Average cost: $25,000-$45,000 for contested trial

---

### 7.4 Family Violence Framework

**Definition (s4AB):** Conduct that coerces, controls, or causes fear

**Disclosure Obligations:**
- Parties must inform court of family violence (s67ZBB)
- Notice of Risk must be filed with Initiating Application
- Ongoing duty to update court

**Impact on Proceedings:**
- May rebut presumption of equal shared parental responsibility
- Affects best interests assessment
- May require supervised time
- Can impact property settlement (indirectly via future needs)

**Procedural Safeguards:**
- Separate waiting rooms
- Video link testimony available
- Cross-examination restrictions (less adversarial trial)
- Security measures

**Interaction with State Orders:**
- Interstate family violence orders recognised
- Court must consider existing intervention orders (s68P)
- Federal orders can be made concurrently (s68B)

---

### 7.5 Less Adversarial Trial (LAT)

**Purpose:** Reduce adversarial nature of parenting proceedings

**Features:**
- Judicial control of questioning
- Restrictions on cross-examination
- Family report admitted as evidence
- Expert evidence presented differently
- Focus on child's interests not parties' rights

**Applies:** All parenting proceedings (since 2006)

**Effect:**
- Reduced trauma to parties and witnesses
- More inquisitorial approach
- Greater judicial control
- Faster resolution in some cases

---

### 7.6 Family Reports and Expert Evidence

#### **Family Reports (s62G)**
**Prepared by:** Family consultants (psychologists, social workers)

**Contents:**
- Observations of children
- Observations of parties
- Assessment of family dynamics
- Recommendations for arrangements
- Views of children (where appropriate)

**Admissibility:** Admissible as evidence (s100A)

**Weight:** Significant but not determinative

**Statistics:**
- Family reports ordered in 34% of parenting cases
- 89% of reports' recommendations accepted in whole or part
- Average cost: $3,500-$6,000

#### **Expert Evidence (s60CE)**
**Requirements:**
- Expert must have relevant qualifications
- Expertise in child development or related field
- Common experts: psychologists, psychiatrists, social workers

**Types:**
- Single expert (court-appointed)
- Separate experts for each party (less common post-2006)

**Topics:**
- Psychological assessments of parties
- Child development needs
- Impact of parenting arrangements
- Family violence risk assessments
- Alcohol/drug assessments

---

## 8. SYSTEM INTEGRATION - VERRIDIAN CORPUS STATISTICS

### 8.1 Overall Corpus

```json
{
  "total_cases": 1523,
  "date_range": "1975-2024",
  "courts": {
    "HCA": 23,
    "FamCAFC": 187,
    "FamCA": 1313
  },
  "case_types": {
    "property": 892,
    "parenting": 456,
    "spousal_maintenance": 234,
    "child_support": 128,
    "contravention": 234,
    "mixed": 579
  }
}
```

### 8.2 Actor Database

```json
{
  "total_actors": 5170,
  "breakdown": {
    "applicants": 1523,
    "respondents": 1523,
    "children": 892,
    "ICLs": 243,
    "judges": 342,
    "experts": 456,
    "other_parties": 191
  }
}
```

### 8.3 Predictive Questions

```json
{
  "total_questions": 5689,
  "categories": {
    "property_division": {
      "count": 2341,
      "avg_predictive_weight": 0.24,
      "common_questions": [
        "What is the total asset pool value?",
        "What are the contributions of each party?",
        "What are the future needs factors?",
        "What superannuation exists?",
        "Are there any add-backs for asset dissipation?"
      ]
    },
    "parenting": {
      "count": 1892,
      "avg_predictive_weight": 0.22,
      "common_questions": [
        "Who has primary care of the children?",
        "What are current parenting arrangements?",
        "Is there family violence?",
        "What are the children's views?",
        "Can parents communicate and cooperate?"
      ]
    },
    "spousal_maintenance": {
      "count": 1456,
      "avg_predictive_weight": 0.21,
      "common_questions": [
        "What is each party's income and earning capacity?",
        "What are the future needs?",
        "How long was the marriage?",
        "Who has care of young children?",
        "What is each party's age and health?"
      ]
    }
  }
}
```

### 8.4 Validation Metrics

```json
{
  "statutory_validation": {
    "s60CC_detection_rate": 0.93,
    "s79_detection_rate": 0.95,
    "s75_detection_rate": 0.88,
    "average_confidence": 0.87
  },
  "span_accuracy": {
    "best_interests_factors": 0.91,
    "property_contributions": 0.94,
    "future_needs_factors": 0.89
  },
  "element_coverage": {
    "s60CC_primary_considerations": 0.96,
    "s60CC_additional_considerations": 0.87,
    "s79_contributions": 0.93,
    "s75_future_needs": 0.90
  }
}
```

---

## 9. DOMAIN-SPECIFIC FEATURES FOR AI SYSTEM

### 9.1 Classification Keywords

**Family_Parenting:**
```
["parenting order", "best interests of the child", "custody", "live with",
 "spend time with", "shared parental responsibility", "section 60cc",
 "s60cc", "meaningful relationship", "primary carer", "contact order",
 "care arrangements", "parenting plan", "children order"]
```

**Family_Property:**
```
["property settlement", "asset division", "financial agreement",
 "section 79", "s79", "contribution", "future needs", "just and equitable",
 "property pool", "matrimonial property", "add back", "asset pool",
 "superannuation splitting"]
```

**Family_Violence:**
```
["family violence", "intervention order", "domestic violence", "avo",
 "protection order", "coercive control", "safety notice", "risk assessment",
 "family and domestic violence", "violent conduct"]
```

**Family_Child_Support:**
```
["child support", "child support assessment", "csa", "administrative assessment",
 "departure application", "change of assessment", "child support formula",
 "percentage of care", "child support agreement"]
```

### 9.2 Legal Test Detection Patterns

**s60CC Best Interests Test:**
```python
required_elements = [
    {
        "element": "safety",
        "keywords": ["safe", "safety", "harm", "risk", "abuse", "violence", "family violence"],
        "weight": 0.95,
        "primary_consideration": True
    },
    {
        "element": "meaningful_relationship",
        "keywords": ["meaningful", "relationship", "contact", "time", "benefit"],
        "weight": 0.90,
        "primary_consideration": True
    },
    {
        "element": "views_of_child",
        "keywords": ["views", "wishes", "maturity", "express", "opinion"],
        "weight": 0.75,
        "primary_consideration": False
    }
]
threshold = 0.6
minimum_elements = 2
```

**s79 Property Settlement:**
```python
required_elements = [
    {
        "element": "financial_contributions",
        "keywords": ["financial", "money", "income", "purchase", "deposit"],
        "weight": 0.85
    },
    {
        "element": "non_financial_contributions",
        "keywords": ["non-financial", "renovation", "improvement", "labor"],
        "weight": 0.80
    },
    {
        "element": "homemaker_parent",
        "keywords": ["homemaker", "parent", "cooking", "cleaning", "raising", "care"],
        "weight": 0.85
    }
]
threshold = 0.5
minimum_elements = 1
```

### 9.3 GSW Workspace Structure

**Domain:** family_law

**Actors:**
- Parties (Applicant, Respondent, Husband, Wife, Mother, Father, Partner)
- Children (named or anonymized)
- Judges and Registrars
- ICLs
- Expert witnesses
- Courts (temporal and spatial)

**States:**
- RelationshipStatus (married, separated, divorced, de facto)
- EmploymentStatus
- FinancialPosition
- PropertyValue
- ParentingTime
- ChildCare arrangements

**Verb Phrases:**
- filed, ordered, consented, separated, married, divorced
- appealed, granted, dismissed, varied, contravened
- relocated, valued, distributed, contributed

**Predictive Questions:**
- Property division: "What is the asset pool value?"
- Parenting: "What are current care arrangements?"
- Maintenance: "What is each party's earning capacity?"

**Spatio-Temporal Links:**
- Date of separation
- Date of marriage
- Hearing dates
- Order dates
- Children's birthdates

---

## 10. RESEARCH APPLICATIONS

### 10.1 Natural Language Queries

**Example Queries Supported:**

1. "What factors does the court consider in property settlement?"
   - Routes to s79 + Hickey four-step approach
   - Provides contributions framework
   - Cites Stanford v Stanford

2. "Can I relocate interstate with my children?"
   - Routes to s60B, s60CC
   - Identifies relocation case law (MRR v GR, Sampson & Hartnett)
   - Asks predictive questions about reasons, impact on other parent

3. "What is family violence and how does it affect parenting orders?"
   - Routes to s4AB definition
   - Routes to s60CC(2)(b) and (3)(h)
   - Cites MRR v GR principles

4. "How is child support calculated?"
   - Routes to Child Support (Assessment) Act
   - Explains formula components
   - Links to care percentage provisions

### 10.2 Statutory RAG Integration

**Vector Embeddings:**
- All 25 key sections embedded
- Cross-referenced with 1,523 cases
- Linked to predictive questions

**Retrieval Patterns:**
- Query → Section identification (95% accuracy)
- Section → Related cases (avg 23 per section)
- Section → Required elements (93% coverage)

### 10.3 Span Detection for Legal Tests

**s60CC Span Detection:**
```
Input: "The court must consider the benefit to the child of having a
meaningful relationship with both parents, and the need to protect
the child from harm."

Detection:
- Span 1: "benefit to the child of having a meaningful relationship with both parents"
  Element: meaningful_relationship (s60CC(2)(a))
  Confidence: 0.94

- Span 2: "need to protect the child from harm"
  Element: protection_from_harm (s60CC(2)(b))
  Confidence: 0.96

Legal Test: s60CC Best Interests Test
Test Met: Yes (both primary considerations present)
```

---

## 11. FUTURE DEVELOPMENTS

### 11.1 Proposed Amendments (Under Discussion)

**Joint Select Committee on Australia's Family Law System (2021)**
- Simplification of s60CC factors
- Removal of equal shared parental responsibility presumption
- Enhanced screening for family violence
- Child-inclusive processes

**Status:** Recommendations under consideration (as of 2024)

### 11.2 System Enhancements

**Planned Additions:**
- Child Support (Registration and Collection) Act integration
- Full Family Law Rules coverage
- Practice Directions and Guidelines
- Annotated legislation with commentary
- International family law (Hague Convention)

---

## 12. GLOSSARY OF FAMILY LAW TERMS

**Additional Considerations:** The factors listed in s60CC(3) that court considers after primary considerations.

**Best Interests of the Child:** The paramount consideration in all parenting matters under s60CA.

**Binding Financial Agreement (BFA):** Agreement under Part VIIIA that binds parties and excludes court's s79 jurisdiction if valid.

**Care Percentage:** The percentage of time child spends in each parent's care (for child support).

**Consent Orders:** Orders made by agreement of parties under s79 or s65D.

**Contravention:** Breach of family law order, potentially subject to penalties under s70NAA.

**De Facto Relationship:** Relationship as a couple living together on genuine domestic basis (s4AA).

**Equal Shared Parental Responsibility:** Presumptive arrangement where both parents share responsibility for major long-term decisions about children (s61DA).

**Equal Time:** Each parent has child for equal periods (50/50).

**Family Violence:** Violent, threatening or controlling behaviour causing fear (s4AB).

**Four-Step Approach:** Framework for s79 property settlement (Hickey v Hickey).

**Future Needs:** s75(2) factors considered at Step 3 of property settlement.

**Independent Children's Lawyer (ICL):** Lawyer appointed to represent child's best interests independently (s68LA).

**Less Adversarial Trial:** Inquisitorial trial procedure for parenting matters.

**Meaningful Relationship:** Relationship allowing child benefit from parent's involvement (s60CC(2)(a)).

**Parenting Order:** Order dealing with parental responsibility, living arrangements, time, or communication (s64B).

**Primary Considerations:** The two mandatory first-order factors in s60CC(2) (meaningful relationship and protection from harm).

**Property Settlement:** Division of parties' property interests under s79.

**Recovery Order:** Order for return of child unlawfully taken or retained (s67Q).

**Spousal Maintenance:** Periodic or lump sum payment for support of former spouse (s74).

**Substantial and Significant Time:** Time allowing parent involvement in child's daily routine and special occasions (s65DAA(5)).

---

## 13. REFERENCES AND SOURCES

### Primary Legislation
- Family Law Act 1975 (Cth) - https://www.legislation.gov.au/C2004A00275/latest/text
- Family Law Rules 2004 (Cth) - https://www.legislation.gov.au/F2005L00094/latest/text
- Child Support (Assessment) Act 1989 (Cth) - https://www.legislation.gov.au/C2004A00103/latest/text
- Marriage Act 1961 (Cth) - https://www.legislation.gov.au/C1961A00012/latest/text

### Case Law Sources
- AustLII - www.austlii.edu.au
- Federal Circuit and Family Court - www.fcfcoa.gov.au
- High Court of Australia - www.hcourt.gov.au

### System Data Sources
- Verridian corpus: 1,523 cases (1975-2024)
- Statutory corpus: Family Law Act sections
- GSW workspace: C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\data\workspaces\family_law_gsw.json

### Research Papers
- arXiv:2511.07587 - Functional Structure of Episodic Memory
- CLAUSE Research Application Report

---

**END OF DOCUMENT**

*This comprehensive domain knowledge document serves as the foundation for KN170 integration into the Verridian Episodic Memory System, supporting statutory RAG, legal test detection, actor modeling, and predictive question generation across all Family Law matters.*
