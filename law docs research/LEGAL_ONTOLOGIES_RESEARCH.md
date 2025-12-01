# Legal Ontologies and Knowledge Graph Schemas Research

## Executive Summary

This document presents comprehensive research on existing legal ontologies, knowledge graph schemas, and best practices for structuring legal data. The research covers international standards (LKIF, CLO, Akoma Ntoso, LegalRuleML), Australian-specific schemas (AustLII, Federal Register of Legislation), knowledge graph structures for law, and best practices from legal tech companies and academic research.

**Key Finding**: Modern legal knowledge graphs use a multi-layered approach combining:
1. **Foundational ontologies** (DOLCE, LKIF Core) for upper-level concepts
2. **Domain-specific schemas** (Akoma Ntoso, LegalRuleML) for document structure
3. **Graph relationships** (CITES, AMENDS, OVERRULES, DISTINGUISHES) for citation networks
4. **Temporal versioning** (FRBR, Component-Level Versioning) for tracking legal evolution
5. **Semantic Web standards** (RDF, OWL, SPARQL) for interoperability

---

## 1. EXISTING LEGAL ONTOLOGIES

### 1.1 LKIF (Legal Knowledge Interchange Format)

**Source**: [GitHub - LKIF Core Ontology](https://github.com/RinkeHoekstra/lkif-core) | [Wikipedia](https://en.wikipedia.org/wiki/Legal_Knowledge_Interchange_Format)

#### Overview
- Developed in the European ESTRELLA project
- Uses Web Ontology Language (OWL) for representing concepts
- Combination of OWL-DL and SWRL
- Standard for representing and interchanging policy, legislation, and cases

#### Modular Structure (15 Modules)

1. **Process Module**: Extends top ontology with definitions of changes, processes (causal changes), and physical objects
2. **Role Module**: Defines typology of roles (epistemic, functions, person roles, organization roles) with plays-property
3. **Action Module**: Vocabulary for representing actions performed by agents
4. **Expression Module**: Propositions, propositional attitudes (belief, intention), qualifications, statements, media

**Additional Modules**:
- Place, Time, Mereology
- Legal Action, Legal Role, Norm
- Process, Rights

#### Layered Architecture

**Three Types of Knowledge Supported**:
1. **Terminological knowledge**: Concepts and relationships
2. **Legal rules**: Conditional statements and reasoning
3. **Normative statements**: Obligations, permissions, prohibitions

**Top-Level Categories**:
- Mental concepts
- Physical concepts
- Abstract concepts
- Occurrences

#### Design Philosophy
- Complies with Semantic Web and Knowledge Representation philosophy
- Layered representational structure
- Terminological and rule layers
- Special set of deontic concepts for normative statements

**Implementation for Our System**:
```python
# Mapping LKIF to our GSW Schema
LKIF_TO_GSW_MAPPING = {
    # LKIF Roles -> Our Actor Roles
    "Legal_Role": ["APPLICANT", "RESPONDENT", "JUDGE"],
    "Person_Role": ["PARENT", "CHILD", "SPOUSE"],
    "Organisation_Role": ["COURT", "LEGAL_FIRM"],

    # LKIF Actions -> Our VerbPhrases
    "Legal_Action": ["filed", "ordered", "granted", "dismissed"],

    # LKIF Expressions -> Our States
    "Propositional_Attitude": ["believes", "intends", "claims"],

    # LKIF Norms -> Legal Rules
    "Norm": {
        "constitutive": "defines legal concepts",
        "regulative": "prescribes behavior"
    }
}
```

---

### 1.2 CLO (Core Legal Ontology) + DOLCE

**Source**: [ResearchGate - CLO](https://www.researchgate.net/publication/221539250_The_LKIF_Core_ontology_of_basic_legal_concepts) | [Ontology Design Patterns](http://ontologydesignpatterns.org/ont/dul010609/CoreLegal.owl)

#### Foundation
- Based on DOLCE+ (Descriptive Ontology for Linguistic and Cognitive Engineering)
- Extension of DOLCE with theory on Descriptions and Situations (D&S)
- Aligned to DOLCE-Ultralite OWL version by Aldo Gangemi

#### Conceptual Framework
**Legal World as Description of Social Reality**:
- Legal descriptions: Laws, norms, crime types
- Legal situations: Legal facts, cases, states of affairs
- Uses D&S distinction between descriptions and situations

#### Key Legal Concepts

**Legal Roles**:
- **Legal Subject**: Basic entity (person with legal capacity)
- **Legal Asset**: Non-agentive legal role (property, resources)
- **Legal Function**: Agentive legal role (judge, lawyer, party)

**Norms**:
- **Constitutive Norms**: Introduce new entities (e.g., "marriage creates spousal relationship")
- **Regulative Norms**: Provide constraints on existing entities (e.g., "must file within 28 days")
- Define Behaviour Courses with Modal Descriptions (obligation, permission, prohibition)

**Legal Facts**:
- **Natural Facts**: Dependent on phenomena (e.g., death, birth)
- **Human Facts**: Dependent on intentional actions
  - **Institutional Facts**: Created by institutions
  - **Legal Acts**: Dependent on legal agent's will
  - **Legal Transactions**: Dependent on legal agent's intentionality

#### Handling Polysemy
Rich axiomatic theories provide relations for systematic polysemy:
- Legal transaction (content of contract)
- Information object (linguistic encoding)
- Legal document (physical object)

**Implementation**:
```python
# CLO Conceptual Model for Family Law
class CLO_FamilyLaw:
    legal_subjects = ["Applicant", "Respondent", "Child"]
    legal_assets = ["Matrimonial Home", "Superannuation", "Vehicle"]
    legal_functions = ["Judge", "Independent Children's Lawyer"]

    constitutive_norms = {
        "marriage": "creates spousal relationship",
        "divorce": "terminates spousal relationship",
        "de_facto": "creates de facto relationship after 2 years"
    }

    regulative_norms = {
        "parenting_application": "must consider best interests of child",
        "property_settlement": "must be just and equitable",
        "family_violence": "must protect safety"
    }

    legal_facts = {
        "natural": ["birth", "death"],
        "institutional": ["court order", "marriage certificate"],
        "legal_act": ["application filed", "affidavit sworn"],
        "legal_transaction": ["consent orders", "financial agreement"]
    }
```

---

### 1.3 Akoma Ntoso (Legislative XML Standard)

**Source**: [OASIS Akoma Ntoso Specification](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html) | [Wikipedia](https://en.wikipedia.org/wiki/Akoma_Ntoso) | [Laws.Africa Guide](https://research.docs.laws.africa/getting-started/what-is-akoma-ntoso)

#### Overview
- **Name**: Architecture for Knowledge-Oriented Management of African Normative Texts
- **Meaning**: "Linked hearts" in Akan language (West Africa)
- **Status**: OASIS international standard (Version 1.0, August 2018)
- **Purpose**: Domain-specific legal XML vocabulary for structured legislative documents

#### Document Types Supported
- Executive documents
- Legislative documents (bills, acts)
- Judiciary documents (judgments, proceedings)
- Parliamentary documents (debate records, committee reports, questions)

#### Hierarchical Structure

**Body Element for Bills and Acts**:
```xml
<body>
  <part id="part1" name="Preliminary">
    <chapter id="chap1">
      <section id="sec1">
        <heading>Definitions</heading>
        <paragraph id="para1">
          <content>In this Act...</content>
        </paragraph>
      </section>
    </chapter>
  </part>
</body>
```

**Named Parts**:
- `<part>`, `<chapter>`, `<section>`, `<paragraph>`, `<clause>`, `<article>`
- Generic container: `<hcontainer>` (hierarchical container) for non-standard names

#### Modular Architecture
- **34 modules total**
- **1 core module** (always required)
- **33 optional modules** organized by:
  - Document types (legislation, reports, amendments, judgments, collections)
  - Optional features (titled blocks, tables of content, etc.)

#### Ontology Structure (FRBR-Based)

**Document Classes** (from FRBR standard):
1. **Work**: Abstract intellectual creation
2. **Expression**: Specific realization (language version)
3. **Manifestation**: Physical embodiment
4. **Item**: Single copy

**Non-Document Classes**:
- Agents, dates, events, references

#### Notable Adoptions
- **UK National Archives** (2014): Converted all legislation to AKN
  - Moved UK from 4th to 1st in Global Open Data Index for legislation
- **African countries**: Multiple jurisdictions
- **Laws.Africa**: Platform built on Akoma Ntoso

**Implementation for Australian Legislation**:
```xml
<!-- Example: Family Law Act 1975 in Akoma Ntoso -->
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="family_law_act_1975">
    <meta>
      <identification source="#au">
        <FRBRWork>
          <FRBRthis value="/au/act/1975/53/main"/>
          <FRBRuri value="/au/act/1975/53"/>
          <FRBRdate date="1975-06-05" name="enactment"/>
          <FRBRcountry value="au"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/au/act/1975/53/eng@2024-01-01/main"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
      </identification>
      <lifecycle source="#source">
        <eventRef date="1975-06-05" type="generation" source="#original"/>
        <eventRef date="2024-01-01" type="amendment" source="#amendment_123"/>
      </lifecycle>
    </meta>
    <body>
      <part id="part7">
        <heading>Children</heading>
        <section id="sec60CC">
          <num>60CC</num>
          <heading>How a court determines what is in a child's best interests</heading>
          <subsection id="sec60CC-1">
            <num>(1)</num>
            <content>
              <p>Subject to subsection (5), in determining what is in the child's best interests, the court must consider the matters set out in subsections (2) and (3).</p>
            </content>
          </subsection>
        </section>
      </part>
    </body>
  </act>
</akomaNtoso>
```

---

### 1.4 LegalRuleML

**Source**: [OASIS LegalRuleML Specification](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html) | [ResearchGate - LegalRuleML Overview](https://www.researchgate.net/publication/256536856_OASIS_LegalRuleML)

#### Overview
- XML-based representation framework for normative rules
- Extends RuleML standard for legal domain
- OASIS standardization initiative
- Enables modeling, reasoning, and comparison of legal arguments

#### Types of Rules Supported

**1. Constitutive Rules**:
- Define concepts that cannot exist without rules
- Example: "Property is defined as..."
- Creates legal categories and classifications

**2. Technical Rules**:
- State conditions for achieving outcomes
- Example: "To qualify for tax deduction, one must..."
- Govern processes like taxation

**3. Prescriptive Rules**:
- Regulate actions (obligatory, permitted, prohibited)
- Example: "Parties must disclose financial information"
- Obligations in contracts and legislation

#### Key Principles

**Multiple Semantic Annotations**:
- Same rule can have multiple interpretations
- Each annotation in separate block
- Parameters: provenance, jurisdiction, logical interpretation

**Temporal Management**:
- Universe includes: provisions, rules, applications, references
- All entities exist and change in time
- Unambiguous representation of temporal interactions

**Ontology Independence**:
- Independent from any specific legal ontology
- Mechanism for pointing to external ontologies
- Supports LKIF, CLO, custom ontologies

**Defeasibility**:
- Supports defeasible rules (can be overridden)
- Rule prioritization
- Exception handling

#### Capabilities
- Legal sources representation
- Time-aware modeling
- Defeasibility operators
- Deontic operators (obligation, permission, prohibition)

**Implementation Example**:
```xml
<!-- LegalRuleML Example: Best Interests of Child Rule -->
<lrml:LegalRuleML xmlns:lrml="http://docs.oasis-open.org/legalruleml/ns/v1.0/">
  <lrml:Statements>
    <lrml:PrescriptiveStatement key="rule_60CC">
      <lrml:hasStrength>
        <lrml:Strength type="strict"/>
      </lrml:hasStrength>

      <lrml:Condition>
        <lrml:Atom>
          <lrml:Rel>parenting_application</lrml:Rel>
          <lrml:Var>X</lrml:Var>
        </lrml:Atom>
      </lrml:Condition>

      <lrml:Conclusion>
        <lrml:Atom>
          <lrml:Rel>must_consider_best_interests</lrml:Rel>
          <lrml:Var>X</lrml:Var>
        </lrml:Atom>
      </lrml:Conclusion>

      <lrml:hasSource>
        <lrml:LegalSource>
          <lrml:refersTo href="#family_law_act_1975_s60CC"/>
        </lrml:LegalSource>
      </lrml:hasSource>

      <lrml:temporalCharacterization>
        <lrml:TemporalEntity>
          <lrml:startDate>1975-06-05</lrml:startDate>
          <lrml:endDate>9999-12-31</lrml:endDate>
        </lrml:TemporalEntity>
      </lrml:temporalCharacterization>
    </lrml:PrescriptiveStatement>
  </lrml:Statements>
</lrml:LegalRuleML>
```

---

## 2. AUSTRALIAN-SPECIFIC SCHEMAS

### 2.1 AustLII (Australasian Legal Information Institute)

**Source**: [AustLII Website](https://www.austlii.edu.au/) | [User Guide](https://www.austlii.edu.au/austlii/guide/user_guide.pdf) | [Globalex Guide](https://www.nyulawglobal.org/globalex/australia1.html)

#### Overview
- **Scale**: 1,045 databases (as of November 2025)
- **Coverage**: All Australasian jurisdictions
- **Content**: ~500,000 cases, all forms of legislation, treaties, journals, law reform reports
- **Access**: Free and open

#### Database Organization

**By Document Type** (Red Ribbon):
- Cases & Legislation
- Journals & Scholarship
- Law Reform
- Treaties
- Special Collections: Libraries, Communities, LawCite

**By Jurisdiction** (Grey Ribbon):
- Commonwealth (Cth)
- States: ACT, NSW, NT, Qld, SA, Tas, Vic, WA
- New Zealand, Pacific Islands

#### Legislation Database Structure
- Each section of an Act is a separate 'page'
- Each section is a separate searchable document (SINO search engine)
- Automated markup divides Acts into sections
- **22+ million automatically inserted hypertext links**
- Heuristic-based linking (intelligent guessing with occasional mistakes)

#### Document Metadata
- Amendment histories
- Associated notes
- Date order sorting (reverse chronological)
- Legislative date = date Act passed or Regulation made
- Medium neutral citations (MNC)
- Catchwords and topics

#### Content Types
- **Primary materials**: Legislation, court/tribunal decisions
- **Secondary materials**: Law reform reports, royal commission reports
- **Historical**: Some jurisdictions back to 1988

**Metadata Schema Inference**:
```python
# Inferred AustLII metadata structure
AUSTLII_CASE_METADATA = {
    "citation": "string (neutral + authorized)",
    "title": "case name",
    "court": "FamCA | FCCA | HCA | etc",
    "jurisdiction": "Cth | NSW | Vic | etc",
    "date": "ISO date",
    "catchwords": ["keyword1", "keyword2"],
    "parties": {
        "applicant": ["names"],
        "respondent": ["names"]
    },
    "judges": ["names"],
    "decision": "full text with paragraph numbers",
    "legislation_cited": ["act references"],
    "cases_cited": ["case citations"],
    "urls": {
        "austlii": "URL",
        "court": "URL"
    }
}
```

---

### 2.2 Federal Register of Legislation (Australia)

**Source**: [Legislation.gov.au](https://www.legislation.gov.au/) | [Structure Guide](https://www.legislation.gov.au/help-and-resources/understanding-legislation/structure-of-a-law) | [OPC](https://www.opc.gov.au/FRL)

#### Overview
- **Manager**: Office of Parliamentary Counsel
- **Authority**: Legislation Act 2003
- **Purpose**: Authorised whole-of-government website for Commonwealth legislation
- **Content**: Full text and lifecycle of individual laws

#### Hierarchical Structure of Acts

**Common Hierarchy** (top to bottom):
1. Chapters
2. Parts
3. Divisions
4. Subdivisions
5. Sections
6. Subsections
7. Paragraphs
8. Subparagraphs
9. Items
10. Clauses
11. Articles

**Document Layout**:
- **First pages**: Title, table of contents, overview
- **Middle**: Numbered provisions with headings
- **Final pages**: Endnotes, amendment history, process information

#### Lifecycle Tracking
- Enactment date
- Commencement date
- All amendments incorporated
- Consolidation dates
- Repeal information
- Relationships between laws

**Implementation Schema**:
```python
# Federal Register metadata structure
FED_REGISTER_SCHEMA = {
    "work": {
        "id": "act_id",
        "title": "Family Law Act 1975",
        "year": 1975,
        "number": 53,
        "assent_date": "1975-06-05",
        "commencement": "1975-01-05"
    },
    "expressions": [
        {
            "expression_id": "expr_001",
            "valid_from": "1975-01-05",
            "valid_to": "1976-12-31",
            "consolidation_date": "1976-12-31",
            "language": "en"
        },
        {
            "expression_id": "expr_123",
            "valid_from": "2024-01-01",
            "valid_to": None,  # Current
            "consolidation_date": "2024-01-01",
            "amendments_incorporated": [
                "Family Law Amendment Act 2023"
            ]
        }
    ],
    "structure": {
        "chapters": [...],
        "parts": [...],
        "sections": [...]
    }
}
```

---

### 2.3 BarNet JADE (Judgments And Decisions Enhanced)

**Source**: [JADE.io](https://jade.io/) | [Library Guides](https://unimelb.libguides.com/caselaw/new_south_wales)

#### Features
- Near real-time case publication (as soon as court releases)
- **Case Trace**: Citator showing all citing cases with paragraph pinpointing
- Email/RSS notifications for important cases
- User annotations capability
- Coverage: Australia and New Zealand

#### NSW Caselaw
- **Launched**: 1999
- **Publisher**: NSW Department of Communities and Justice
- **Coverage**: Selected judgments from all NSW courts/tribunals
- **Historical**: Some decisions back to 1988

#### Authorised Reports System
- **Authorised reports**: Reviewed by presiding judge
- Official approval by judiciary
- One designated report per jurisdiction

**Examples of Authorised Reports**:
- **Commonwealth Law Reports (CLR)**: High Court
- **Federal Court Reports (FCR)**: Federal Court
- **Family Court Reports (FamCR)**: Family Court
- **Industrial Reports (IR)**: Industrial relations

**Specialist Reports**:
- Administrative Appeals Reports (AAR)
- Australian Criminal Reports (A Crim R)
- Australian Law Journal Reports (ALJR)
- Australian Tax Reports (ATR)
- Local Government and Environmental Reports (LGERA)

---

## 3. KNOWLEDGE GRAPH STRUCTURES FOR LAW

### 3.1 Fundamental Elements

**Source**: [Legal Knowledge Graphs Overview](https://www.meegle.com/en_us/topics/knowledge-graphs/knowledge-graph-for-legal-tech) | [Neo4j Legal KG](https://neo4j.com/blog/developer/from-legal-documents-to-knowledge-graphs/)

#### Core Components
1. **Nodes**: Entities (legal documents, people, organizations, concepts)
2. **Edges**: Relationships between entities
3. **Properties**: Attributes of nodes and edges

#### Node Types

**Primary Nodes**:
```python
NODE_TYPES = {
    # Legal Documents
    "Legislation": {
        "properties": ["title", "jurisdiction", "year", "number", "status"],
        "subtypes": ["Act", "Regulation", "Rule", "By-law"]
    },

    "Case": {
        "properties": ["citation", "court", "date", "judges", "outcome"],
        "metadata": ["medium_neutral_citation", "catchwords", "decision_date"]
    },

    "Provision": {
        "properties": ["section_number", "heading", "text", "valid_from", "valid_to"],
        "parent": "Legislation"
    },

    # Parties
    "Person": {
        "properties": ["name", "role", "party_type"],
        "roles": ["Applicant", "Respondent", "Judge", "Lawyer", "Witness"]
    },

    "Organization": {
        "properties": ["name", "type", "jurisdiction"],
        "types": ["Court", "Tribunal", "Legal_Firm", "Government_Department"]
    },

    # Concepts
    "Legal_Concept": {
        "properties": ["name", "definition", "area_of_law"],
        "examples": ["Best interests of child", "Just and equitable", "Family violence"]
    },

    # Assets (Family Law specific)
    "Asset": {
        "properties": ["type", "value", "description"],
        "types": ["Real_Property", "Superannuation", "Vehicle", "Bank_Account", "Business"]
    }
}
```

### 3.2 Edge Types (Relationships)

**Source**: [Similar Cases Recommendation](https://arxiv.org/html/2107.04771v2) | [Graph-Structured Retrieval](https://law.co/blog/graph-structured-retrieval-for-legal-precedent-networks/)

#### Citation Relationships
```python
CITATION_EDGES = {
    "CITES": {
        "description": "Case A cites Case B",
        "properties": ["paragraph_number", "context", "purpose"],
        "types": ["positive", "neutral", "negative"]
    },

    "CITED_BY": {
        "description": "Inverse of CITES",
        "properties": ["frequency", "context"]
    },

    "FOLLOWS": {
        "description": "Case A follows precedent B",
        "strength": "strong_positive"
    },

    "DISTINGUISHES": {
        "description": "Case A distinguishes Case B (different facts)",
        "flag": "yellow",  # KeyCite system
        "properties": ["distinguishing_facts", "court_level"]
    },

    "OVERRULES": {
        "description": "Case A overrules Case B",
        "flag": "red",  # KeyCite system
        "impact": "Case B no longer good law"
    },

    "DISAPPROVES": {
        "description": "Case A disapproves reasoning in Case B",
        "flag": "orange"
    },

    "APPLIED": {
        "description": "Case A applies principle from Case B",
        "strength": "positive"
    },

    "CONSIDERED": {
        "description": "Case A considers Case B",
        "strength": "neutral"
    }
}
```

#### Legislative Relationships
```python
LEGISLATIVE_EDGES = {
    "AMENDS": {
        "description": "Act A amends Act B",
        "properties": ["amendment_date", "sections_affected", "nature_of_change"]
    },

    "REPEALS": {
        "description": "Act A repeals Act B",
        "properties": ["repeal_date", "transitional_provisions"]
    },

    "CONSOLIDATES": {
        "description": "Act A consolidates Acts B, C, D",
        "properties": ["consolidation_date", "source_acts"]
    },

    "REPLACES": {
        "description": "Act A replaces Act B",
        "properties": ["replacement_date"]
    },

    "INTERPRETS": {
        "description": "Case interprets Provision",
        "properties": ["interpretation", "principle_established"]
    },

    "APPLIES": {
        "description": "Case applies Provision",
        "properties": ["application_context", "outcome"]
    }
}
```

#### Structural Relationships
```python
STRUCTURAL_EDGES = {
    "HAS_PART": {
        "description": "Act has Part/Section",
        "hierarchy": ["Act → Part → Division → Section → Subsection"]
    },

    "CONTAINS": {
        "description": "Section contains text/concept",
        "properties": ["relevance_score"]
    },

    "CROSS_REFERENCES": {
        "description": "Section X references Section Y",
        "properties": ["reference_type", "context"]
    }
}
```

#### Party Relationships
```python
PARTY_EDGES = {
    "PARTY_TO": {
        "description": "Person is party to Case",
        "properties": ["party_type", "role"]
    },

    "REPRESENTS": {
        "description": "Lawyer represents Person",
        "properties": ["representation_type"]
    },

    "DECIDES": {
        "description": "Judge decides Case",
        "properties": ["decision_date", "judgment_type"]
    },

    "PARENT_OF": {
        "description": "Person is parent of Child",
        "properties": ["parental_responsibility", "living_arrangement"]
    },

    "MARRIED_TO": {
        "description": "Person married to Person",
        "properties": ["marriage_date", "separation_date", "divorce_date"]
    },

    "OWNS": {
        "description": "Person owns Asset",
        "properties": ["ownership_percentage", "acquisition_date", "value"]
    }
}
```

### 3.3 Network Analysis Metrics

**Source**: [Citation Network Analysis](https://scholarship.law.unc.edu/cgi/viewcontent.cgi?httpsredir=1&article=5717&context=nclr) | [CourtListener Visualizations](https://www.courtlistener.com/visualizations/scotus-mapper/)

#### Centrality Measures
```python
NETWORK_METRICS = {
    "in_degree": {
        "description": "Count of citations received",
        "indicates": "How influential/important a case is"
    },

    "out_degree": {
        "description": "Count of cases cited",
        "indicates": "How well-grounded the decision is"
    },

    "betweenness_centrality": {
        "description": "How often case appears on shortest path between others",
        "indicates": "Bridge between different legal areas"
    },

    "pagerank": {
        "description": "Iterative citation importance",
        "indicates": "Overall authority in network"
    },

    "temporal_influence": {
        "description": "Whether case remains authoritative over time",
        "measurement": "Citation frequency by year"
    }
}
```

#### Proximity Analysis
- **Shortest path**: Legal connection between concepts
- **Degrees of separation**: Citation distance (typically 3 degrees in Supreme Court)
- **Community detection**: Clusters of related cases (doctrinal areas)

---

## 4. TEMPORAL VALIDITY AND VERSIONING

**Source**: [Graph RAG for Legal Norms](https://arxiv.org/html/2505.00039) | [Deterministic Legal Agents](https://arxiv.org/html/2510.06002) | [Component-Level Versioning](https://arxiv.org/html/2506.07853)

### 4.1 Challenges
- Legal norms characterized by **formal hierarchy**
- Dense web of **cross-references**
- Continuous **diachronic evolution** (amendments, repeals, consolidations)
- **Temporally-naive** systems cannot retrieve correct historical versions
- Risk of **anachronistic and factually incorrect** answers

### 4.2 FRBR-Based Versioning Model

**Source**: [FRBR Wikipedia](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records) | [IFLA FRBR](https://www.ifla.org/files/assets/cataloguing/frbr/frbr.pdf)

#### FRBR Entities (WEMI)
1. **Work**: Abstract intellectual creation (e.g., "Family Law Act 1975")
2. **Expression**: Specific realization (e.g., "as amended on 2024-01-01", language version)
3. **Manifestation**: Physical embodiment (e.g., PDF, HTML)
4. **Item**: Single copy (e.g., specific downloaded file)

**Application to Legal Documents**:
```python
FRBR_LEGAL_MODEL = {
    "Work": {
        "id": "work_fla_1975",
        "title": "Family Law Act 1975",
        "type": "Act",
        "jurisdiction": "Commonwealth",
        "abstract": True  # Never changes
    },

    "Expressions": [
        {
            "id": "expr_fla_1975_original",
            "work_id": "work_fla_1975",
            "valid_from": "1975-01-05",
            "valid_to": "1976-12-31",
            "language": "en",
            "consolidation_date": "1975-01-05",
            "content": "original_text"
        },
        {
            "id": "expr_fla_1975_2024",
            "work_id": "work_fla_1975",
            "valid_from": "2024-01-01",
            "valid_to": None,  # Current
            "language": "en",
            "consolidation_date": "2024-01-01",
            "amendments_incorporated": ["act_123_2023"],
            "content": "current_text"
        }
    ]
}
```

### 4.3 Component-Level Versioning

**Multi-Layered Model**:
```python
COMPONENT_VERSIONING = {
    # Norm Level
    "Norm_Work": "Abstract law (unchanging)",
    "Norm_Temporal_Version": "Law as amended at specific date",
    "Norm_Language_Version": "Specific language rendering",

    # Component Level (Articles, Sections, Paragraphs)
    "Component_Work": "Abstract provision (e.g., Section 60CC)",
    "Component_Temporal_Version": "Provision text at specific date",
    "Component_Language_Version": "Provision in specific language",

    # Benefits
    "efficiency": "Reuse unchanged components across versions",
    "precision": "Track individual provision amendments",
    "determinism": "Reconstruct exact historical state"
}
```

### 4.4 Event-Centric Amendment Modeling

**Action Nodes**:
```python
AMENDMENT_ACTIONS = {
    "Action": {
        "id": "action_001",
        "type": "amendment",  # or "repeal", "enactment"
        "source_instrument": "Family Law Amendment Act 2023",
        "date": "2024-01-01",
        "affects": [
            {
                "component": "section_60CC",
                "nature": "text_replacement",
                "old_version": "ctv_60CC_v12",
                "new_version": "ctv_60CC_v13"
            }
        ]
    }
}
```

**Lifecycle Tracking**:
- Creation driven by legislative event
- Termination driven by amending event
- Causal links explicit via Action nodes
- Enables auditable provenance

### 4.5 Point-in-Time Retrieval

**Implementation**:
```python
def get_provision_at_date(provision_id: str, date: str):
    """
    Deterministic retrieval of provision text as it existed on specific date.

    Args:
        provision_id: Component Work ID (e.g., "section_60CC")
        date: ISO date (e.g., "2020-06-15")

    Returns:
        Component Temporal Version valid on that date
    """
    versions = get_temporal_versions(provision_id)

    for version in versions:
        if version.valid_from <= date <= (version.valid_to or "9999-12-31"):
            return version

    return None  # Provision did not exist on that date

# Example usage
section_60CC_june_2020 = get_provision_at_date("section_60CC", "2020-06-15")
section_60CC_today = get_provision_at_date("section_60CC", "2025-11-29")
```

---

## 5. SEMANTIC WEB STANDARDS

**Source**: [OWL W3C](https://www.w3.org/OWL/) | [RDF and SPARQL](https://www.w3.org/2007/03/VLDB/) | [Legal OWL Ontologies](https://www.semantic-web-journal.net/system/files/swj667_0.pdf)

### 5.1 RDF (Resource Description Framework)

**Foundational Data Model**:
```turtle
# RDF Triples for Legal Knowledge Graph
@prefix legal: <http://example.org/legal#> .
@prefix fla: <http://legislation.gov.au/Details/C2024C00001#> .

# Case nodes
legal:Hickey_v_Hickey a legal:FamilyCourtCase ;
    legal:citation "[1983] HCA 17" ;
    legal:court legal:HighCourtOfAustralia ;
    legal:date "1983-05-24"^^xsd:date ;
    legal:cites fla:section_79 ;
    legal:establishes legal:HickeyPrinciple .

# Legislation nodes
fla:section_79 a legal:LegislativeProvision ;
    legal:partOf fla:FamilyLawAct1975 ;
    legal:heading "Alteration of property interests" ;
    legal:validFrom "1975-01-05"^^xsd:date .

# Relationships
legal:Hickey_v_Hickey legal:interprets fla:section_79 .
legal:Jones_v_Jones legal:follows legal:Hickey_v_Hickey .
```

### 5.2 OWL (Web Ontology Language)

**Ontology Definition**:
```xml
<!-- OWL Class Hierarchy for Family Law -->
<owl:Class rdf:ID="LegalEntity"/>

<owl:Class rdf:ID="Party">
  <rdfs:subClassOf rdf:resource="#LegalEntity"/>
</owl:Class>

<owl:Class rdf:ID="Applicant">
  <rdfs:subClassOf rdf:resource="#Party"/>
</owl:Class>

<owl:Class rdf:ID="Respondent">
  <rdfs:subClassOf rdf:resource="#Party"/>
</owl:Class>

<!-- Object Properties (Relationships) -->
<owl:ObjectProperty rdf:ID="cites">
  <rdfs:domain rdf:resource="#Case"/>
  <rdfs:range rdf:resource="#Case"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="overrules">
  <rdfs:subPropertyOf rdf:resource="#cites"/>
  <rdfs:domain rdf:resource="#Case"/>
  <rdfs:range rdf:resource="#Case"/>
</owl:ObjectProperty>

<!-- Datatype Properties -->
<owl:DatatypeProperty rdf:ID="citation">
  <rdfs:domain rdf:resource="#Case"/>
  <rdfs:range rdf:resource="xsd:string"/>
</owl:DatatypeProperty>

<!-- Restrictions -->
<owl:Class rdf:ID="ParentingCase">
  <rdfs:subClassOf>
    <owl:Restriction>
      <owl:onProperty rdf:resource="#involvesChild"/>
      <owl:minCardinality rdf:datatype="xsd:nonNegativeInteger">1</owl:minCardinality>
    </owl:Restriction>
  </rdfs:subClassOf>
</owl:Class>
```

### 5.3 SPARQL (Query Language)

**Query Examples**:
```sparql
# Find all cases that cite Family Law Act Section 60CC
PREFIX legal: <http://example.org/legal#>
PREFIX fla: <http://legislation.gov.au/Details/C2024C00001#>

SELECT ?case ?citation ?date
WHERE {
    ?case a legal:FamilyCourtCase ;
          legal:citation ?citation ;
          legal:date ?date ;
          legal:cites fla:section_60CC .
}
ORDER BY DESC(?date)
LIMIT 100

# Find precedential chain (case A → B → C)
SELECT ?case1 ?case2 ?case3
WHERE {
    ?case1 legal:cites ?case2 .
    ?case2 legal:cites ?case3 .
    FILTER(?case1 = legal:CurrentCase)
}

# Find cases distinguishing Hickey v Hickey
SELECT ?case ?citation ?year
WHERE {
    ?case legal:distinguishes legal:Hickey_v_Hickey ;
          legal:citation ?citation ;
          legal:date ?date .
    BIND(YEAR(?date) AS ?year)
}
ORDER BY ?year

# Temporal query: Find law as it was on specific date
SELECT ?provision ?text
WHERE {
    ?version legal:componentWork ?provision ;
             legal:validFrom ?from ;
             legal:validTo ?to ;
             legal:text ?text .
    FILTER(?from <= "2020-06-15"^^xsd:date &&
           (?to >= "2020-06-15"^^xsd:date || !BOUND(?to)))
}
```

---

## 6. OPEN SOURCE LEGAL DATA PROJECTS

**Source**: [Awesome Legal Data](https://github.com/openlegaldata/awesome-legal-data) | [Open Legal Data Platform](https://github.com/openlegaldata/oldp) | [Free Law Project](https://github.com/freelawproject)

### 6.1 Data Collections

#### Pile-of-Law
- **Size**: 256GB
- **Language**: English
- **Content**: Legal and administrative text
- **Purpose**: Training legal NLP models

#### MultiLegalPile
- **Languages**: 24
- **Scope**: Multilingual/multijurisdiction
- **Purpose**: LLM training for global legal systems

#### JRC-Acquis & MultiEURLEX
- **JRC-Acquis**: Parallel corpus of EU law for MT/NLP
- **MultiEURLEX**: ~65,000 EU legal acts in 23 languages
- **Annotation**: EuroVoc labels

#### legislation.gov.uk
- **Content**: Official consolidated UK legislation
- **Types**: Acts, Statutory Instruments, devolved legislation
- **Access**: API & bulk XML download
- **Format**: Compatible with Akoma Ntoso principles

### 6.2 Platforms and Tools

#### CourtListener (Free Law Project)
- **URL**: CourtListener.com
- **Coverage**: All US court opinions (state and federal, historical and current)
- **Mission**: Free access to primary legal materials
- **Features**:
  - Search and retrieval
  - Citation networks
  - Aggregation and organization
  - Academic research support

#### Open Legal Data Platform (OLDP)
- **Technology**: Python 3.12, Django
- **Features**:
  - Legal text processing
  - REST API
  - Elasticsearch-based search
- **Goal**: Open Data platform for legal documents
- **Focus**: Court decisions and laws

#### Open Source Legislation
- **Format**: SQL knowledge-graph
- **Languages**: Python and TypeScript SDKs
- **Structure**: Unified schema for graph traversal
- **Optimization**: Designed for LLM use
- **Purpose**: Democratize legal knowledge

### 6.3 Machine Learning Datasets

#### Legal-BERT Training Corpus
- **EU Legislation**: 116,062 documents (EURLEX)
- **UK Legislation**: 61,826 documents
- **HUDOC Cases**: 12,554 (European Court of Human Rights)
- **US Cases**: 164,141 (Case Law Access Project)
- **US Contracts**: 76,366 (EDGAR)

#### LexGLUE
- **Purpose**: Legal NLP benchmarking
- **Content**: Seven refined document datasets
- **Access**: Easy-to-use corpus for legal NLP

#### Russian Law Open Data (RusLawOD)
- **Format**: XML (Akoma Ntoso compatible)
- **Coverage**: Laws of Russian Federation, Presidential decrees, Government regulations
- **Status**: As of December 31, 2023
- **Note**: Internal document structure markup in progress

---

## 7. BEST PRACTICES FROM LEGAL INFORMATICS RESEARCH

**Source**: [Legal Ontology Development](https://link.springer.com/chapter/10.1007/978-94-007-0120-5_1) | [VoxPopuLII Legal Research Ontology](https://blog.law.cornell.edu/voxpop/2015/08/20/legal-research-ontology-part-ii/) | [Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)

### 7.1 Design Principles

#### Gruber's Five Design Criteria (1995)
```python
ONTOLOGY_DESIGN_CRITERIA = {
    "clarity": {
        "description": "Effective communication of intended meaning",
        "practice": "Use natural language definitions backed by formal axioms"
    },

    "coherence": {
        "description": "Sanctioning inferences consistent with definitions",
        "practice": "Ensure logical consistency, run reasoners to validate"
    },

    "extendibility": {
        "description": "Ability to add new terms without revising existing",
        "practice": "Use modular design, clear hierarchies"
    },

    "minimal_encoding_bias": {
        "description": "Independence from symbol-level encoding",
        "practice": "Conceptualize at knowledge level, not implementation level"
    },

    "minimal_ontological_commitment": {
        "description": "Make few claims about modeled world",
        "practice": "Define only what's necessary, allow extensions"
    }
}
```

#### Visser & Bench-Capon Principle
- **No universally "better" ontology**
- Adequacy depends on **specific application**
- Context determines which ontology is most suitable

### 7.2 Development Methodologies

#### NeOn Methodology
- **Documentation**: Well-documented
- **Scenarios**: Fits various development scenarios
- **Legal Domain**: Suitable for legal ontology development

#### Recommended Approach
```python
ONTOLOGY_DEVELOPMENT_PROCESS = {
    "step_1": "Search for similar existing ontologies",
    "step_2": "Determine high-level ontologies to use or extend",
    "step_3": "Use ontology design patterns (ODPs)",
    "step_4": "Rely on established upper-level ontologies",
    "step_5": "Define domain and scope via competency questions",
    "step_6": "Enumerate important terms",
    "step_7": "Define class hierarchy",
    "step_8": "Define properties and constraints",
    "step_9": "Create instances (individuals)",
    "step_10": "Validate with competency questions"
}
```

### 7.3 Competency Questions

**Purpose**: Litmus test for ontology completeness

**Examples for Family Law KG**:
```python
COMPETENCY_QUESTIONS = [
    # Temporal
    "What was the text of Section 60CC on June 15, 2020?",
    "When was the Family Law Act 1975 last amended?",
    "What provisions were affected by the 2023 amendment?",

    # Citation Network
    "Which cases cite Hickey v Hickey?",
    "Has this case been overruled?",
    "What's the precedential chain from Case A to Case B?",

    # Legal Principles
    "What cases establish the principle of 'best interests of child'?",
    "How has the definition of 'family violence' evolved?",
    "What interpretations exist for 'just and equitable'?",

    # Party/Case
    "What assets were disputed in this case?",
    "Who had primary care of the children?",
    "What was the property settlement ratio?",

    # Cross-Document
    "What legislation does this case interpret?",
    "What subsequent cases distinguish this decision?",
    "Which tribunal decisions apply this High Court ruling?"
]
```

### 7.4 Notable Legal Ontologies for Reference

**Four Well-Known Frameworks**:
1. **McCarty's LLD** (Legal Logic and Deontics)
2. **Stamper's NORMA** (Normative Analysis)
3. **Valente's Functional Ontology of Law**
4. **Van Kralingen & Visser's Frame-based Ontology**

### 7.5 Tools

#### Web Protégé
- **Developer**: Stanford Center for Biomedical Informatics Research
- **Status**: Open-source
- **Language**: OWL (Web Ontology Language)
- **Features**:
  - Graphical interfaces
  - Class/property visualization
  - Reasoning engines
  - Consistency validation

---

## 8. PROPOSED KNOWLEDGE GRAPH SCHEMA FOR VERRIDIAN AI

### 8.1 Node Type Definitions

```python
from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime

class NodeType(str, Enum):
    # Legal Documents
    LEGISLATION = "legislation"
    CASE = "case"
    PROVISION = "provision"
    REGULATION = "regulation"

    # Parties
    PERSON = "person"
    ORGANIZATION = "organization"
    JUDGE = "judge"

    # Legal Concepts
    LEGAL_PRINCIPLE = "legal_principle"
    LEGAL_TEST = "legal_test"
    LEGAL_DEFINITION = "legal_definition"

    # Assets (Family Law)
    ASSET = "asset"

    # Temporal
    DATE = "date"
    TIME_PERIOD = "time_period"

    # Location
    LOCATION = "location"
    COURT = "court"

class LegislationNode:
    """
    Represents a piece of legislation (Act, Regulation, etc.)
    Based on: Akoma Ntoso, FRBR, Federal Register schema
    """
    id: str
    type: str = "legislation"

    # Metadata
    title: str
    short_title: str
    jurisdiction: str  # "Commonwealth", "NSW", etc.
    year: int
    number: int

    # FRBR Work level (abstract)
    work_id: str  # Unchanging identifier

    # Current expression
    current_expression_id: str
    consolidation_date: str

    # Lifecycle
    assent_date: Optional[str]
    commencement_date: Optional[str]
    repeal_date: Optional[str]
    status: str  # "in_force", "repealed", "not_in_force"

    # Content
    text: str  # Full text
    preamble: Optional[str]

    # Structure
    parts: List[str]  # IDs of Part nodes
    sections: List[str]  # IDs of Provision nodes

    # References
    cited_by_cases: List[str]
    amended_by: List[str]
    repeals: List[str]

    # Semantic
    area_of_law: List[str]  # ["family_law", "property_law"]
    keywords: List[str]

    # Provenance
    source_url: str
    scraped_date: str

class ProvisionNode:
    """
    Represents a specific provision (section, subsection, paragraph)
    Based on: Akoma Ntoso structure, Component-Level Versioning
    """
    id: str
    type: str = "provision"

    # Component Work (abstract)
    component_work_id: str

    # Component Temporal Version
    temporal_version_id: str
    valid_from: str
    valid_to: Optional[str]

    # Identity
    parent_legislation_id: str
    section_number: str  # "60CC", "79(4)(a)"
    heading: Optional[str]

    # Hierarchy
    part_id: Optional[str]
    division_id: Optional[str]
    parent_section_id: Optional[str]
    subsections: List[str]

    # Content
    text: str

    # Amendment tracking
    original_text: str
    amendment_history: List[Dict]  # [{action_id, date, nature, old_text, new_text}]

    # Semantic
    defines: List[str]  # Legal concepts defined
    prescribes: List[str]  # Obligations/permissions/prohibitions

    # References
    interpreted_by_cases: List[str]
    cross_references: List[str]  # Other provisions

class CaseNode:
    """
    Represents a court or tribunal decision
    Based on: AustLII structure, Citation network research
    """
    id: str
    type: str = "case"

    # Identity
    citation_neutral: str  # "[2023] FamCA 123"
    citation_authorized: Optional[str]  # "(2023) 45 FamCR 67"
    title: str  # "Smith v Smith"

    # Court
    court: str  # "FamCA", "FCCA", "HCA"
    jurisdiction: str

    # Parties
    applicants: List[str]  # Person node IDs
    respondents: List[str]
    judges: List[str]  # Judge node IDs
    lawyers: List[str]

    # Decision
    date: str
    outcome: str  # "granted", "dismissed", "partly_allowed"
    orders: List[str]

    # Content
    full_text: str
    headnote: Optional[str]
    catchwords: List[str]

    # Legal
    area_of_law: List[str]
    case_type: str  # "parenting", "property", "divorce"
    principles_established: List[str]  # Legal principle node IDs

    # Citations
    cites_cases: List[str]
    cited_by_cases: List[str]
    follows_cases: List[str]
    distinguishes_cases: List[str]
    overrules_cases: List[str]

    # Legislation
    cites_provisions: List[str]
    interprets_provisions: List[str]

    # Network metrics (computed)
    in_degree: int
    out_degree: int
    pagerank: float

    # Provenance
    source_url: str

class PersonNode:
    """
    Represents a person (party, judge, lawyer, child)
    Based on: CLO Legal Subject, GSW Actor
    """
    id: str
    type: str = "person"

    # Identity
    name: str
    aliases: List[str]

    # Roles (context-dependent)
    roles: List[str]  # ["Applicant", "Father", "Homemaker"]

    # Legal status
    legal_capacity: str  # "adult", "child", "incapacitated"

    # Relationships (in family law context)
    children: List[str]
    spouse: Optional[str]
    de_facto_partner: Optional[str]

    # States (temporal)
    states: List[Dict]  # {name, value, start_date, end_date}
    # Example: {name: "MaritalStatus", value: "married", start_date: "2010-03-15", end_date: "2020-06-01"}

    # Cases involved
    cases_as_applicant: List[str]
    cases_as_respondent: List[str]
    cases_as_judge: List[str]

class LegalPrincipleNode:
    """
    Represents an established legal principle or test
    Based on: LKIF Expression, CLO Legal Concept
    """
    id: str
    type: str = "legal_principle"

    # Identity
    name: str  # "Best interests of the child"
    definition: str

    # Source
    established_by_case: str  # Case node ID
    codified_in_provision: Optional[str]

    # Evolution
    refined_by_cases: List[str]
    superseded_by: Optional[str]

    # Application
    applied_in_cases: List[str]
    area_of_law: str

class AssetNode:
    """
    Represents a financial or property asset (Family Law specific)
    Based on: CLO Legal Asset, GSW Actor (asset type)
    """
    id: str
    type: str = "asset"

    # Identity
    asset_type: str  # "real_property", "superannuation", "vehicle", "bank_account"
    description: str

    # Ownership
    owners: List[Dict]  # [{person_id, percentage, acquisition_date}]

    # Valuation
    value: Optional[float]
    valuation_date: Optional[str]
    value_history: List[Dict]  # [{date, value, source}]

    # Context
    disputed_in_cases: List[str]
    awarded_to: Optional[str]  # After settlement
```

### 8.2 Edge Type Definitions

```python
class EdgeType(str, Enum):
    # Citation relationships
    CITES = "cites"
    CITED_BY = "cited_by"
    FOLLOWS = "follows"
    DISTINGUISHES = "distinguishes"
    OVERRULES = "overrules"
    DISAPPROVES = "disapproves"
    APPLIED = "applied"
    CONSIDERED = "considered"

    # Legislative relationships
    AMENDS = "amends"
    REPEALS = "repeals"
    CONSOLIDATES = "consolidates"
    REPLACES = "replaces"
    INTERPRETS = "interprets"
    APPLIES_PROVISION = "applies_provision"

    # Structural relationships
    HAS_PART = "has_part"
    PART_OF = "part_of"
    CONTAINS = "contains"
    CROSS_REFERENCES = "cross_references"

    # Party relationships
    PARTY_TO = "party_to"
    REPRESENTS = "represents"
    DECIDES = "decides"
    PARENT_OF = "parent_of"
    MARRIED_TO = "married_to"
    SEPARATED_FROM = "separated_from"
    OWNS = "owns"

    # Conceptual relationships
    DEFINES = "defines"
    ESTABLISHES = "establishes"
    REFINES = "refines"
    SUPERSEDES = "supersedes"

    # Temporal relationships
    VALID_DURING = "valid_during"
    SUCCEEDED_BY = "succeeded_by"

class Edge:
    """
    Generic edge with properties
    """
    id: str
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType

    # Properties
    properties: Dict[str, Any]
    # Examples:
    # - For CITES: {paragraph_number: "23", context: "positive", strength: 0.8}
    # - For AMENDS: {amendment_date: "2024-01-01", sections_affected: ["60CC"]}
    # - For OWNS: {ownership_percentage: 50, acquisition_date: "2015-03-01"}

    # Temporal validity
    valid_from: Optional[str]
    valid_to: Optional[str]

    # Provenance
    created_date: str
    source: str  # "extraction", "manual", "inference"
```

### 8.3 Graph Schema Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERRIDIAN KNOWLEDGE GRAPH                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         AMENDS          ┌──────────────┐
│ Legislation  │─────────────────────────→│ Legislation  │
│   (Work)     │         REPEALS         │   (Work)     │
└──────┬───────┘                          └──────┬───────┘
       │ HAS_PART                                │
       ↓                                         │
┌──────────────┐        INTERPRETS        ┌─────┴────────┐
│  Provision   │←─────────────────────────│     Case     │
│(Temporal Ver)│                          │              │
└──────┬───────┘                          └─────┬────────┘
       │ DEFINES                                │ CITES
       ↓                                        │ FOLLOWS
┌──────────────┐                               │ OVERRULES
│    Legal     │                               │ DISTINGUISHES
│  Principle   │                               ↓
└──────┬───────┘                          ┌──────────────┐
       │ APPLIED_IN                       │     Case     │
       └──────────────────────────────────→│              │
                                          └─────┬────────┘
                                                │ PARTY_TO
                                                ↓
┌──────────────┐        MARRIED_TO        ┌──────────────┐
│    Person    │←────────────────────────→│    Person    │
│ (Applicant)  │        PARENT_OF         │ (Respondent) │
└──────┬───────┘                          └──────┬───────┘
       │ OWNS                                    │ OWNS
       ↓                                         ↓
┌──────────────┐                          ┌──────────────┐
│     Asset    │                          │     Asset    │
│ (Real Prop)  │                          │    (Super)   │
└──────────────┘                          └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Temporal Layer: All nodes/edges have valid_from/valid_to       │
│  Component-Level Versioning: Provisions track text evolution    │
│  FRBR Model: Work (abstract) → Expression (temporal version)    │
└─────────────────────────────────────────────────────────────────┘
```

### 8.4 Integration with Existing GSW Schema

```python
# Mapping between GSW Schema and Knowledge Graph Schema
GSW_TO_KG_MAPPING = {
    # GSW Actor → KG Nodes
    "Actor (person)": "PersonNode",
    "Actor (organization)": "OrganizationNode",
    "Actor (asset)": "AssetNode",
    "Actor (temporal)": "DateNode",
    "Actor (legal_document)": "CaseNode | LegislationNode",

    # GSW VerbPhrase → KG Edges
    "VerbPhrase": {
        "filed": "PARTY_TO (with role=filer)",
        "ordered": "DECIDES (judge → case)",
        "married": "MARRIED_TO (person → person)",
        "owns": "OWNS (person → asset)"
    },

    # GSW State → KG Node Properties
    "State": "PersonNode.states[] | AssetNode.value_history[]",

    # GSW PredictiveQuestion → KG Query
    "PredictiveQuestion": "SPARQL query over graph",

    # GSW SpatioTemporalLink → KG Temporal Edges
    "SpatioTemporalLink (temporal)": "Edge.valid_from/valid_to",
    "SpatioTemporalLink (spatial)": "LOCATED_AT edge"
}

# Example: Converting GSW extraction to KG nodes
def gsw_to_kg(workspace: GlobalWorkspace) -> KnowledgeGraph:
    """
    Convert GSW workspace to Knowledge Graph representation
    """
    kg = KnowledgeGraph()

    # Convert Actors to Nodes
    for actor in workspace.actors.values():
        if actor.actor_type == ActorType.PERSON:
            kg.add_node(PersonNode(
                id=actor.id,
                name=actor.name,
                aliases=actor.aliases,
                roles=actor.roles,
                states=actor.states
            ))
        elif actor.actor_type == ActorType.ASSET:
            kg.add_node(AssetNode(
                id=actor.id,
                asset_type=actor.metadata.get("asset_type"),
                description=actor.name,
                value=actor.metadata.get("value")
            ))

    # Convert VerbPhrases to Edges
    for verb in workspace.verb_phrases.values():
        if verb.agent_id and verb.patient_ids:
            for patient_id in verb.patient_ids:
                kg.add_edge(Edge(
                    source_node_id=verb.agent_id,
                    target_node_id=patient_id,
                    edge_type=verb_to_edge_type(verb.verb),
                    properties=verb.metadata
                ))

    # Convert States to Node Properties with temporal validity
    for state in workspace.states.values():
        node = kg.get_node(state.entity_id)
        if node:
            node.states.append({
                "name": state.name,
                "value": state.value,
                "valid_from": state.start_date,
                "valid_to": state.end_date
            })

    return kg
```

---

## 9. IMPLEMENTATION RECOMMENDATIONS

### 9.1 Technology Stack

```python
RECOMMENDED_STACK = {
    "Graph Database": {
        "primary": "Neo4j",
        "reasons": [
            "Native graph storage and traversal",
            "Cypher query language (similar to SPARQL)",
            "Excellent visualization tools",
            "Strong community and legal tech adoption"
        ],
        "alternative": "Amazon Neptune (if cloud-native required)"
    },

    "Semantic Web Layer": {
        "technology": "RDF4J / Apache Jena",
        "reasons": [
            "Full RDF/OWL/SPARQL support",
            "Reasoning capabilities",
            "Interoperability with legal ontologies"
        ]
    },

    "Ontology Management": {
        "tool": "Protégé",
        "reasons": [
            "Industry standard",
            "OWL editing",
            "Reasoning validation",
            "LKIF/CLO compatible"
        ]
    },

    "Temporal Versioning": {
        "approach": "Component-Level FRBR model",
        "implementation": "Custom temporal graph layer in Neo4j",
        "query_support": "Point-in-time retrieval via temporal constraints"
    },

    "Integration": {
        "current_system": "GSW (Global Semantic Workspace)",
        "approach": "Dual storage: GSW for extraction, KG for querying",
        "sync": "Bidirectional mapping layer"
    }
}
```

### 9.2 Phased Implementation

```python
IMPLEMENTATION_PHASES = {
    "Phase 1": {
        "focus": "Core schema and basic graph",
        "deliverables": [
            "Define node/edge types (Legislation, Case, Provision, Person, Asset)",
            "Neo4j schema setup",
            "Import existing workspaces into graph",
            "Basic Cypher queries"
        ],
        "duration": "2-3 weeks"
    },

    "Phase 2": {
        "focus": "Citation network and case relationships",
        "deliverables": [
            "CITES, FOLLOWS, DISTINGUISHES, OVERRULES edges",
            "Citation parsing from case text",
            "Network metrics computation (PageRank, centrality)",
            "Precedent chain queries"
        ],
        "duration": "3-4 weeks"
    },

    "Phase 3": {
        "focus": "Legislative versioning and temporal validity",
        "deliverables": [
            "FRBR Work/Expression model",
            "Component-level versioning for provisions",
            "Amendment tracking (Action nodes)",
            "Point-in-time retrieval API"
        ],
        "duration": "4-5 weeks"
    },

    "Phase 4": {
        "focus": "Semantic Web integration",
        "deliverables": [
            "RDF export of graph",
            "LKIF/CLO ontology alignment",
            "SPARQL endpoint",
            "OWL reasoning for inference"
        ],
        "duration": "3-4 weeks"
    },

    "Phase 5": {
        "focus": "Australian legal data integration",
        "deliverables": [
            "AustLII scraper and ingestion",
            "Federal Register of Legislation sync",
            "NSW Caselaw integration",
            "Bulk import pipeline"
        ],
        "duration": "5-6 weeks"
    }
}
```

### 9.3 Sample Cypher Queries

```cypher
// Find all cases citing Family Law Act Section 60CC
MATCH (case:Case)-[:CITES]->(prov:Provision {section_number: "60CC"})
      -[:PART_OF]->(leg:Legislation {title: "Family Law Act 1975"})
RETURN case.citation, case.date, case.court
ORDER BY case.date DESC
LIMIT 100

// Find precedential chain (case A → B → C)
MATCH path = (start:Case {citation: "[2023] FamCA 123"})-[:CITES*1..3]->(end:Case)
RETURN path
ORDER BY length(path)

// Find cases that distinguish Hickey v Hickey
MATCH (case:Case)-[r:DISTINGUISHES]->(hickey:Case {citation: "[1983] HCA 17"})
RETURN case.citation, case.date, r.distinguishing_facts
ORDER BY case.date

// Point-in-time retrieval: Get Section 60CC as it was on 2020-06-15
MATCH (prov:Provision {component_work_id: "section_60CC"})
WHERE prov.valid_from <= date("2020-06-15")
  AND (prov.valid_to IS NULL OR prov.valid_to >= date("2020-06-15"))
RETURN prov.text, prov.temporal_version_id

// Find most influential cases by PageRank
MATCH (case:Case)
WHERE case.area_of_law CONTAINS "family_law"
RETURN case.citation, case.title, case.pagerank
ORDER BY case.pagerank DESC
LIMIT 20

// Find all assets owned by parties in a case
MATCH (case:Case {id: "case_12345"})
      -[:PARTY_TO]-(person:Person)
      -[:OWNS]->(asset:Asset)
RETURN person.name, collect(asset.description) AS assets

// Trace amendment history of a provision
MATCH (prov:Provision {component_work_id: "section_79"})
OPTIONAL MATCH (prov)<-[:AFFECTS]-(action:Action)
RETURN prov.temporal_version_id, prov.valid_from, prov.valid_to,
       action.date AS amendment_date, action.source_instrument
ORDER BY prov.valid_from
```

---

## 10. SOURCES AND FURTHER READING

### International Standards
- [GitHub - LKIF Core Ontology](https://github.com/RinkeHoekstra/lkif-core)
- [OASIS Akoma Ntoso Specification](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html)
- [OASIS LegalRuleML Specification](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html)
- [ResearchGate - CLO and DOLCE](https://www.researchgate.net/publication/221539250_The_LKIF_Core_ontology_of_basic_legal_concepts)
- [Laws.Africa - Akoma Ntoso Guide](https://research.docs.laws.africa/getting-started/what-is-akoma-ntoso)

### Australian Resources
- [AustLII Website](https://www.austlii.edu.au/)
- [Federal Register of Legislation](https://www.legislation.gov.au/)
- [BarNet JADE](https://jade.io/)
- [NSW Caselaw](https://www.caselaw.nsw.gov.au/about)

### Knowledge Graphs
- [Neo4j - Legal Knowledge Graphs](https://neo4j.com/blog/developer/from-legal-documents-to-knowledge-graphs/)
- [ArXiv - Similar Cases Recommendation using Legal Knowledge Graphs](https://arxiv.org/html/2107.04771v2)
- [Graph-Structured Retrieval for Legal Precedent Networks](https://law.co/blog/graph-structured-retrieval-for-legal-precedent-networks)
- [CourtListener Supreme Court Visualizations](https://www.courtlistener.com/visualizations/scotus-mapper/)

### Temporal Validity
- [ArXiv - Graph RAG for Legal Norms (Temporal)](https://arxiv.org/html/2505.00039)
- [ArXiv - Deterministic Legal Agents](https://arxiv.org/html/2510.06002)
- [ArXiv - Component-Level Versioning](https://arxiv.org/html/2506.07853)
- [IFLA - FRBR Specification](https://www.ifla.org/files/assets/cataloguing/frbr/frbr.pdf)

### Semantic Web
- [W3C - OWL Overview](https://www.w3.org/OWL/)
- [Semantic Web Journal - Legal OWL Ontologies](https://www.semantic-web-journal.net/system/files/swj667_0.pdf)
- [Semantic Web Standards - RDF, OWL, SPARQL](https://www.hakia.com/semantic-web-standards-a-deep-dive-into-rdf-owl-and-sparql)

### Open Source Projects
- [GitHub - Awesome Legal Data](https://github.com/openlegaldata/awesome-legal-data)
- [GitHub - Open Legal Data Platform](https://github.com/openlegaldata/oldp)
- [GitHub - Open Source Legislation](https://github.com/spartypkp/open-source-legislation)
- [Free Law Project](https://github.com/freelawproject)

### Best Practices
- [Springer - Legal Ontology Engineering](https://link.springer.com/chapter/10.1007/978-94-007-0120-5_1)
- [VoxPopuLII - Legal Research Ontology](https://blog.law.cornell.edu/voxpop/2015/08/20/legal-research-ontology-part-ii/)
- [Stanford - Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)
- [Cornell - Building Legal Research Ontology](https://blog.law.cornell.edu/voxpop/2014/03/19/building-a-legal-research-ontology/)

---

## CONCLUSION

This research reveals a mature ecosystem of legal ontologies and knowledge graph schemas that we can leverage for Verridian AI. The key insights are:

1. **LKIF and CLO provide foundational concepts** we should align with for interoperability
2. **Akoma Ntoso offers excellent legislative structure** we can adopt or adapt for Australian legislation
3. **LegalRuleML enables rule representation** that complements our case-based reasoning
4. **Temporal versioning is critical** and well-researched (FRBR + component-level versioning)
5. **Citation networks are well-understood** with established edge types and metrics
6. **Australian data sources** (AustLII, Federal Register) have implicit schemas we can formalize
7. **Open source projects** provide datasets and code we can build upon

**Recommendation**: Implement a **hybrid approach** that:
- Stores GSW extractions in their current format for episodic memory
- Exports to Neo4j knowledge graph for citation networks and complex queries
- Aligns with LKIF/CLO for semantic interoperability
- Implements FRBR-based temporal versioning for legislative history
- Uses RDF/OWL/SPARQL for advanced reasoning and external integration

This positions Verridian AI to be both cutting-edge (using GSW episodic memory) and standards-compliant (using established legal ontologies).
