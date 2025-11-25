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
[![UI](https://img.shields.io/badge/UI-Next.js_16-black?style=for-the-badge)](ui/)
[![LangFuse](https://img.shields.io/badge/LangFuse-Observability-purple?style=for-the-badge)](docker/langfuse/)

**232,000+ Documents** | **14 Legal Domains** | **71% Token Savings** | **85% Accuracy** | **100% Query Success**

[Get Started](#quick-start) | [Live Demo](#live-ui-demo) | [How It Works](#how-it-works) | [Roadmap](#roadmap)

</div>

---

## What's New

### Latest Release - Phase 7 Architecture

- **Brain-Inspired AI**: Tolman-Eichenbaum Machines (TEM) + Active Inference + Vector Symbolic Architectures
- **Working Chat UI**: Full Next.js interface at `localhost:3000` with GSW-powered legal assistant
- **LangFuse Observability**: Self-hosted tracing with Docker (graph traversal, accuracy scoring, latency)
- **Agent Tools**: LangChain-compatible tools for knowledge retrieval
- **Performance Testing**: 100% query success rate, 11.83ms average response time
- **Family Law Knowledge**: 5,170 actors, 7,615 predictive questions, 714 cases

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
| Query Success | Variable | **100%** |
| Avg Response Time | 500ms+ | **11.83ms** |

**This isn't incremental improvement. This is a paradigm shift.**

---

## Live UI Demo

<div align="center">

### Verridian LAW OS

**A production-ready legal AI chat interface**

</div>

```bash
# Start the UI
cd ui
npm install
npm run dev

# Access at http://localhost:3000
```

### Features

| Feature | Description |
|---------|-------------|
| **GSW-Powered Chat** | Legal questions answered with statute alignment and case citations |
| **Statutory Alignment** | Automatic citation of Family Law Act 1975 sections |
| **Case Retrieval** | HCA and NSWSC case law references |
| **Knowledge Base** | 5,170 actors, 7,615 questions, 714 family law cases |
| **Real-time Processing** | "Neural Processing" indicator with streaming responses |

### Example Interactions

**User:** "What are the key factors courts consider when determining child custody?"

**Verridian AI:**
> Using `statutory_alignment` tool...
>
> **Section 60CC of the Family Law Act 1975 (Cth)** outlines how the court determines what is in a child's best interests:
> - (a) The benefit to the child of having a meaningful relationship with both parents
> - (b) The need to protect the child from harm
>
> **Case References:** CDJ v VAJ [1998] HCA 67, AMS v AIF [1999] HCA 26

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

## Performance Benchmarks

### Agent Knowledge Retrieval (Latest Test)

| Metric | Result |
|--------|--------|
| **Queries Executed** | 29 |
| **Success Rate** | 100% |
| **Average Response Time** | 11.83ms |
| **Min Response Time** | 0.01ms |
| **Max Response Time** | 78.03ms |

### Query Performance by Type

| Query Type | Avg Time | Assessment |
|------------|----------|------------|
| `get_unanswered_questions` | 0.29ms | Excellent |
| `get_actors_by_role` | 3.20ms | Excellent |
| `find_parties` | 4.50ms | Excellent |
| `find_cases_by_type` | 4.70ms | Very Good |
| `get_context_json` | 20.54ms | Good |
| `get_context_toon` | 68.14ms | Acceptable |

### EpBench-200 Benchmark

| Method | F1 Score | Context Tokens |
|--------|----------|----------------|
| Embedding RAG | 0.771 | ~8,771 |
| HippoRAG2 | 0.753 | ~8,771 |
| GraphRAG | 0.714 | ~7,340 |
| **GSW (Ours)** | **0.850** | **~3,587** |

**+10% accuracy with 59% fewer tokens**

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

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for UI)
- Docker Desktop (for LangFuse observability)
- OpenRouter API key

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
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY
```

### Start the UI

```bash
cd ui
npm install
npm run dev
# Access at http://localhost:3000
```

### Start LangFuse Observability

```bash
cd docker/langfuse
docker compose up -d
# Access at http://localhost:3001
```

### Run Performance Tests

```bash
python tests/test_agent_performance.py
# View report: PERFORMANCE_REPORT.md
```

### Full Setup Guide

See [docs/SETUP.md](docs/SETUP.md) for comprehensive instructions including:
- Corpus download and domain splitting
- LangFuse configuration
- Ingestion pipeline
- Production deployment

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
│   ├── agents/                 # Agent Tools (NEW)
│   │   ├── family_law_knowledge.py  # Family Law GSW builder
│   │   └── gsw_tools.py        # LangChain-compatible tools
│   │
│   ├── observability/          # LangFuse Integration (NEW)
│   │   ├── langfuse_tracer.py  # Graph traversal tracing
│   │   ├── session_memory.py   # Episodic session tracking
│   │   ├── scoring.py          # Accuracy scoring (target 95%)
│   │   └── gsw_integration.py  # Integration examples
│   │
│   ├── logic/                  # Data Models
│   │   ├── gsw_schema.py       # Pydantic schemas
│   │   └── ontology_seed.py    # Legal ontology
│   │
│   ├── ingestion/              # Corpus Processing
│   │   └── classification_config.py  # 14 domain taxonomy
│   │
│   └── utils/
│       └── toon.py             # TOON encoder (71% compression)
│
├── ui/                         # Next.js Frontend (NEW)
│   ├── src/
│   │   ├── app/               # App router
│   │   ├── components/        # React components
│   │   │   ├── chat/         # Chat interface
│   │   │   ├── layout/       # Main layout
│   │   │   └── ui/           # UI components
│   │   └── lib/              # API utilities
│   └── package.json
│
├── docker/
│   └── langfuse/              # Self-hosted LangFuse (NEW)
│       └── docker-compose.yml
│
├── data/
│   ├── domains/               # Classified legal documents
│   ├── workspaces/            # GSW workspaces
│   └── legislation/           # Family Law Act sections
│
├── tests/
│   ├── test_observability.py  # 39 observability tests
│   └── test_agent_performance.py  # Performance benchmarks
│
├── docs/
│   └── SETUP.md               # Comprehensive setup guide
│
├── PERFORMANCE_REPORT.md      # Latest benchmark results
├── PHASE_7_IMPLEMENTATION_PLAN.md  # Brain-inspired architecture
└── VERRIDIAN_COMPLETE_SYSTEM.md    # Full system documentation
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

### Phase 2: Agent Architecture ✅ COMPLETE

- [x] LangChain-compatible agent tools
- [x] Family Law knowledge system (5,170 actors, 7,615 questions)
- [x] GSW query interface (100% success rate)
- [x] Statutory alignment tool

### Phase 3: Observability ✅ COMPLETE

- [x] LangFuse self-hosted setup (Docker)
- [x] Graph traversal tracing
- [x] Accuracy scoring framework (target 95%)
- [x] Session memory tracking
- [x] Latency breakdown instrumentation
- [x] 39 comprehensive tests (all passing)

### Phase 4: Frontend UI ✅ COMPLETE

- [x] Next.js 16 interface
- [x] GSW-powered chat assistant
- [x] Statutory alignment display
- [x] Case citation rendering
- [x] Real-time "Neural Processing" indicator

### Phase 5: Performance Testing ✅ COMPLETE

- [x] Automated test suite
- [x] Query performance benchmarks (11.83ms avg)
- [x] Knowledge coverage assessment
- [x] Performance report generation

### Phase 6: Documentation ✅ COMPLETE

- [x] Comprehensive SETUP.md
- [x] Performance report
- [x] System architecture documentation
- [x] API reference

### Phase 7: Brain-Inspired Architecture 🚧 IN PROGRESS

```
┌─────────────────────────────────────────────────────────────────┐
│            BRAIN-INSPIRED LEGAL AI ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Navigation (TEM) - "Legal Geometry"                   │
│  ───────────────────────────────────────────                    │
│  • Separates case STRUCTURE from case FACTS                     │
│  • Enables zero-shot inference on new case patterns             │
│  • Accuracy Impact: +15-20%                                     │
│                                                                  │
│  Layer 2: Agency (Active Inference) - "Curiosity Engine"        │
│  ─────────────────────────────────────────────────────          │
│  • Detects missing evidence and information gaps                │
│  • Computes Expected Value of Information (EVI)                 │
│  • Autonomously generates queries to fill gaps                  │
│  • Accuracy Impact: +10-15%                                     │
│                                                                  │
│  Layer 3: Logic (VSA) - "Anti-Hallucination Shield"             │
│  ──────────────────────────────────────────────────             │
│  • Vector Symbolic Architectures for reasoning                  │
│  • Symbolic binding for legal elements                          │
│  • Traceable inference chains                                   │
│  • Accuracy Impact: +5-10%                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Target Accuracy: 95%+ (from current 85%)**

- [ ] TEM spatial factorization for case structure
- [ ] Active Inference belief updating
- [ ] VSA hyperdimensional computing
- [ ] Combined three-layer inference

### Phase 8: Scale & Production 📋 PLANNED

- [ ] Vector database integration (Pinecone/Weaviate)
- [ ] Multi-jurisdiction support (UK, US, NZ)
- [ ] Enterprise authentication
- [ ] API rate limiting and quotas
- [ ] Horizontal scaling

### Phase 9: Advanced Features 📋 PLANNED

- [ ] Outcome prediction models
- [ ] Automatic brief generation
- [ ] Cross-reference linking
- [ ] Timeline visualizations
- [ ] Interactive entity graphs

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

## Australian Legal Corpus

We processed the **entire Australian legal corpus**:

| Metric | Value |
|--------|-------|
| **Total Documents** | 232,000+ |
| **Raw Data Size** | 9.4 GB |
| **Time Coverage** | 1903 - 2024 |
| **Jurisdictions** | All Australian (Federal + State) |
| **Family Law Cases** | 714 (with full GSW extraction) |
| **Actors Extracted** | 5,170 |
| **Questions Generated** | 7,615 |

### Domain Distribution

| Domain | Documents | Key Areas |
|--------|-----------|-----------|
| Administrative | 58,726+ | Migration, Social Security, FOI |
| Family | 714+ | Parenting, Property, Child Protection |
| Criminal | 1,541+ | Violence, Drugs, Traffic |
| Commercial | 1,842+ | Corporations, Insolvency |
| Torts | 2,000+ | Negligence, Defamation |
| Property | 310+ | Torrens, Strata, Native Title |
| Tax | 168+ | Income Tax, GST |
| Constitutional | 500+ | Federal/State Powers |
| Procedural | 980+ | Civil Procedure, Evidence |
| Industrial | 553+ | Fair Work |
| Equity | 800+ | Trusts, Succession |
| Specialized | 300+ | Maritime, Aviation |

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

*GSW is how we get there.*

</div>
