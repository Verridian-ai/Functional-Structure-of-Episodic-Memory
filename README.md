<div align="center">

# VERRIDIAN AI

<img src="assets/images/verridian_logo.png" alt="Verridian AI" width="250">

**Pioneering Cognitive AI for Legal Intelligence**

---

<img src="assets/images/RAG VS GSW.png" alt="RAG vs GSW" width="100%">

---

# Legal GSW

### *The World's First Actor-Centric Memory System for Legal AI*

[![arXiv](https://img.shields.io/badge/arXiv-2511.07587-b31b1b?style=for-the-badge)](https://arxiv.org/abs/2511.07587)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**232,000+ Documents** | **14 Legal Domains** | **71% Token Savings** | **85% Accuracy**

[Get Started](#quick-start) | [How It Works](#how-it-works) | [Why GSW](#why-gsw-wins) | [Roadmap](#roadmap)

</div>

---

## The Pitch

> **What if AI could remember legal cases the way lawyers do?**

Every lawyer knows that winning a case isn't about finding documents - it's about understanding **people**, **relationships**, and **how situations evolve over time**. Current AI systems retrieve text chunks. They don't *understand* them.

**Legal GSW changes everything.**

We've built the first AI system that processes legal documents the way the human brain processes memories - by organizing information around **actors** (the people, assets, and entities involved) rather than keywords or embeddings.

The result?

| Metric | Traditional RAG | **Legal GSW** |
|--------|----------------|---------------|
| Accuracy | 77% | **85%** |
| Token Usage | ~8,000/query | **~3,500/query** |
| Context Retention | None | **Full Timeline** |
| Entity Tracking | Lost between queries | **Persistent Memory** |

**This isn't incremental improvement. This is a paradigm shift.**

---

## What We Built

<div align="center">
<img src="assets/images/GSW Giving Language Model a Human Like Episodic Memory.png" alt="GSW Architecture" width="100%">
</div>

### The Global Semantic Workspace (GSW)

Inspired by cognitive neuroscience research on how human episodic memory works, GSW implements a **brain-like architecture** for document understanding:

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW HUMAN MEMORY WORKS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   When you remember a wedding, you don't remember "verbs"        │
│                                                                  │
│   You remember:                                                  │
│   • WHO was there (the couple, guests, officiant)               │
│   • WHERE it happened (the venue, the garden)                   │
│   • WHEN it occurred (June 15th, summer)                        │
│   • WHAT their states were (happy, nervous, married)            │
│                                                                  │
│   GSW mirrors this exact structure for legal documents.          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The 6-Task Extraction Pipeline

Every document passes through our cognitive extraction pipeline:

| Task | What It Does | Example Output |
|------|--------------|----------------|
| **1. Actor Identification** | Find all entities | `John Smith`, `Family Court`, `$1.2M Property` |
| **2. Role Assignment** | Define their function | `Applicant`, `Husband`, `Father` |
| **3. State Tracking** | Track conditions over time | `Married → Separated → Divorced` |
| **4. Verb Extraction** | Capture actions as links | `filed`, `ordered`, `separated` |
| **5. Question Generation** | Predict useful queries | `"What is the property value?"` |
| **6. Answer Mapping** | Connect answers to questions | `Property value = $1.2 million` |

<div align="center">
<img src="assets/images/operatorv2.png" alt="Operator Pipeline" width="80%">
</div>

---

## Why GSW Wins

### The Problem with RAG

**Retrieval-Augmented Generation (RAG)** is the current industry standard. It works like this:

1. Split documents into chunks
2. Create embeddings
3. Retrieve "similar" chunks for each query
4. Hope the LLM figures it out

**This fundamentally breaks on legal documents:**

```
❌ "The husband" in paragraph 5 ≠ "John Smith" in paragraph 200
❌ No memory between queries - every question starts fresh
❌ Context is fragmented - relationships are destroyed
❌ Wastes tokens stuffing raw text into prompts
```

### The GSW Solution

GSW doesn't retrieve text. It **builds knowledge**:

```
✅ "The husband" = "John Smith" = "the applicant" (Entity Resolution)
✅ Persistent workspace tracks ALL entities across queries
✅ Relationships preserved: John → married to → Jane → parent of → Emma
✅ 71% fewer tokens via TOON compression
```

### Real Example

**Input Text:**
> "The parties married on 10 June 2010 in Sydney. They separated on 1 March 2020. The husband is employed as an accountant earning $150,000. The wife is the primary carer of the two children."

**RAG Output:** A text chunk (no structure)

**GSW Output:**
```
ACTORS:
├── John Smith (person)
│   ├── Roles: [Husband, Applicant, Father]
│   ├── States: [Married→Separated, Employed as Accountant]
│   └── Income: $150,000
├── Jane Smith (person)
│   ├── Roles: [Wife, Respondent, Mother, Primary Carer]
│   └── States: [Married→Separated]
├── Children (persons)
│   └── Roles: [Subject Children]
└── Marriage (temporal)
    ├── Start: 2010-06-10
    └── End: 2020-03-01

RELATIONSHIPS:
├── John ←married→ Jane (2010-2020)
├── John ←parent→ Children
└── Jane ←primary_carer→ Children

QUESTIONS ANSWERED:
✓ When did they marry? → June 10, 2010
✓ When did they separate? → March 1, 2020
✓ What is the husband's income? → $150,000
? What is the property value? → UNANSWERED
```

---

## The TOON Format: 71% Token Savings

We invented **Token-Oriented Object Notation (TOON)** - a compression format that dramatically reduces LLM context usage.

### Before (JSON): 575 tokens
```json
{
  "actors": [
    {
      "id": "actor_001",
      "name": "John Smith",
      "actor_type": "person",
      "roles": ["husband", "applicant"],
      "states": [{"name": "RelationshipStatus", "value": "separated"}]
    }
  ]
}
```

### After (TOON): 167 tokens
```
Actors[1]{id,name,type,roles,states}
actor_001,John Smith,person,husband|applicant,RelationshipStatus=separated
```

**Result: 71% reduction in tokens = 71% reduction in API costs**

---

## Australian Legal Corpus

We processed the **entire Australian legal corpus**:

| Metric | Value |
|--------|-------|
| **Total Documents** | 232,000+ |
| **Raw Data Size** | 9.4 GB |
| **Time Coverage** | 1903 - 2024 |
| **Jurisdictions** | All Australian (Federal + State) |

### Intelligent Domain Classification

Every document is automatically classified into one of **14 legal domains**:

| Domain | Documents | Key Areas |
|--------|-----------|-----------|
| Administrative | 58,726+ | Migration, Social Security, FOI |
| Family | 200+ | Parenting, Property, Child Protection |
| Criminal | 1,541+ | Violence, Drugs, Traffic, Procedure |
| Commercial | 1,842+ | Corporations, Insolvency, Consumer |
| Torts | 2,000+ | Negligence, Defamation, Medical |
| Property | 310+ | Torrens, Strata, Native Title |
| Tax | 168+ | Income Tax, GST, Duties |
| Constitutional | 500+ | Federal/State Powers |
| Procedural | 980+ | Civil Procedure, Evidence |
| Industrial | 553+ | Fair Work, Enterprise Agreements |
| Equity | 800+ | Trusts, Succession |
| Specialized | 300+ | Maritime, Aviation, Mental Health |

---

## How It Works

<div align="center">
<img src="assets/images/motivation.png" alt="Motivation" width="80%">
</div>

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT                                    │
│                    Legal Document                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN CLASSIFIER                             │
│         Automatic classification into 14 legal domains           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GSW OPERATOR                                │
│                                                                  │
│   ┌─────────┐  ┌───────┐  ┌────────┐  ┌───────┐  ┌──────────┐  │
│   │ Actors  │→ │ Roles │→ │ States │→ │ Verbs │→ │Questions │  │
│   └─────────┘  └───────┘  └────────┘  └───────┘  └──────────┘  │
│                                                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SPACETIME LINKER                               │
│           Bind entities by WHEN and WHERE                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RECONCILER                                  │
│        "the husband" = "John Smith" = "the applicant"           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  GLOBAL WORKSPACE                                │
│              Persistent Actor-Centric Memory                     │
│                                                                  │
│   Query this workspace for ANY question about the document       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENROUTER_API_KEY="your-key-here"
```

### Basic Usage

```python
from src.gsw.legal_operator import LegalOperator
from src.logic.gsw_schema import GlobalWorkspace

# Initialize
operator = LegalOperator()
workspace = GlobalWorkspace(domain="family")

# Extract from legal text
text = """
The parties married on 10 June 2010 in Sydney. They separated on
1 March 2020. The husband is employed as an accountant earning
$150,000 per annum. The wife is the primary carer of the children.
"""

extraction = operator.extract(text, chunk_id="doc_001")

# View actors
for actor in extraction.actors:
    print(f"{actor.name}: {actor.roles}")

# Export compressed format (71% smaller)
print(workspace.to_toon())
```

### Process Legal Corpus

```bash
# Extract domains from corpus
python gsw_pipeline.py extract --input corpus.jsonl

# Process family law domain
python gsw_pipeline.py process --domain family --limit 100

# Generate reports
python gsw_pipeline.py analyze
```

---

## Roadmap

### Phase 1: Core System ✅ COMPLETE

- [x] GSW Operator extraction pipeline
- [x] Spatio-temporal binding
- [x] Entity reconciliation
- [x] TOON compression (71% savings)
- [x] Australian corpus classification (14 domains)
- [x] Pydantic schema system

### Phase 2: Agent Architecture 🚧 IN PROGRESS

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT ARCHITECTURE                            │
│                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │   PYDANTIC   │    │  LANGGRAPH   │    │   LANGFUSE   │     │
│   │    AGENTS    │◄──►│    FLOWS     │◄──►│ OBSERVABILITY│     │
│   └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                  │
│   • Type-safe structured outputs                                │
│   • Multi-step legal reasoning chains                           │
│   • Full tracing and evaluation                                 │
│   • Production monitoring                                       │
└─────────────────────────────────────────────────────────────────┘
```

- [ ] Pydantic AI agents with structured outputs
- [ ] LangGraph multi-step reasoning workflows
- [ ] LangFuse observability integration
- [ ] LangChain tool ecosystem

### Phase 3: Intelligence Hub 📋 PLANNED

```
┌─────────────────────────────────────────────────────────────────┐
│                 LEGAL INTELLIGENCE HUB                           │
│                                                                  │
│   SEARCH           │   MATCH            │   ANALYZE              │
│   ─────────────    │   ─────────────    │   ─────────────        │
│   • Natural lang   │   • Find similar   │   • Timeline view      │
│   • Cross-refs     │   • Case matching  │   • Asset pools        │
│   • Citations      │   • Outcome pred   │   • Risk scoring       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

- [ ] Semantic search across 232K documents
- [ ] Case matching by facts and outcomes
- [ ] Automatic cross-reference linking
- [ ] Outcome prediction models

### Phase 4: Frontend UI 📋 PLANNED

- [ ] React/Next.js interface
- [ ] Interactive entity graphs
- [ ] Timeline visualizations
- [ ] AI chat assistant

---

## Project Structure

```
Functional-Structure-of-Episodic-Memory/
│
├── src/
│   ├── gsw/                    # Core GSW System
│   │   ├── legal_operator.py   # 6-task extraction
│   │   ├── legal_spacetime.py  # Temporal binding
│   │   ├── legal_reconciler.py # Entity resolution
│   │   └── workspace.py        # Memory management
│   │
│   ├── logic/                  # Data Models
│   │   ├── gsw_schema.py       # Pydantic schemas
│   │   └── ontology_seed.py    # Legal ontology
│   │
│   ├── ingestion/              # Corpus Processing
│   │   ├── classification_config.py  # 14 domain taxonomy
│   │   └── corpus_domain_extractor.py
│   │
│   └── utils/
│       └── toon.py             # TOON encoder (71% compression)
│
├── assets/
│   ├── images/                 # Documentation visuals
│   └── videos/                 # Demo videos
│
├── docs/research/              # Academic papers
├── data/workspaces/            # Extracted workspaces
├── reports/                    # Analysis reports
│
├── gsw_pipeline.py             # Main CLI
├── requirements.txt
└── README.md
```

---

## Research Foundation

This project implements the research from:

> **"Functional Structure of Episodic Memory"**
> arXiv:2511.07587

The paper demonstrates that human episodic memory is organized around **actors** (entities), not events. GSW is the first implementation of this insight for document AI.

### Key Innovation

Traditional NLP uses **verb-centric** representations:
```
(Subject, Verb, Object) → (John, married, Jane)
```

GSW uses **actor-centric** representations:
```
John: {
  type: person,
  roles: [husband, applicant, father],
  states: [married → separated],
  timeline: [2010: married, 2020: separated],
  links: [Jane, Children, Property]
}
```

This mirrors how humans actually remember - and it works dramatically better.

---

## Performance

### Benchmark: EpBench-200

| Method | F1 Score | Context Tokens |
|--------|----------|----------------|
| Embedding RAG | 0.771 | ~8,771 |
| HippoRAG2 | 0.753 | ~8,771 |
| GraphRAG | 0.714 | ~7,340 |
| **GSW (Ours)** | **0.850** | **~3,587** |

**+10% accuracy with 59% fewer tokens**

---

## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md).

```bash
# Fork, clone, branch
git checkout -b feature/your-feature

# Make changes, commit
git commit -m "Add your feature"

# Push and PR
git push origin feature/your-feature
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

### Built by Verridian AI

*Cognitive AI for Legal Intelligence*

[Website](https://github.com/Verridian-ai) | [Paper](https://arxiv.org/abs/2511.07587) | [Issues](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)

---

**If AI is going to help lawyers, it needs to think like one.**

*GSW is the first step.*

</div>
