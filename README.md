<div align="center">

<!-- Logo & Title -->
<img src="assets/images/verridian_logo.png" alt="Verridian AI" width="180">

# VERRIDIAN AI

### Brain-Inspired Legal Intelligence Platform

*Giving Language Models Human-Like Episodic Memory*

<br>

<!-- Animated Badges Row 1 -->
[![arXiv](https://img.shields.io/badge/arXiv-2511.07587-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2511.07587)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-Next.js_16-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](ui/)

<!-- Badges Row 2 -->
[![PyTorch](https://img.shields.io/badge/PyTorch-TEM+VSA-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](src/tem/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](ui/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](src/logic/)
[![LangChain](https://img.shields.io/badge/LangChain-Tools-121212?style=for-the-badge)](src/agents/)

<br>

<!-- Performance Metrics Visual -->
```
╔══════════════════════════════════════════════════════════════════════════╗
║                         🎯 PERFORMANCE METRICS                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    ║
║   │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │    ║
║   │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │  │   ▓▓▓▓▓     │    ║
║   │   85%       │  │   56%       │  │   42x       │  │   100%      │    ║
║   │  ACCURACY   │  │  TOKEN      │  │  FASTER     │  │  SUCCESS    │    ║
║   │  vs 77% RAG │  │  REDUCTION  │  │  RESPONSE   │  │  RATE       │    ║
║   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    ║
╚══════════════════════════════════════════════════════════════════════════╝
```

<br>

<!-- Quick Links -->
[📖 Documentation](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki) •
[🚀 Quick Start](#-quick-start) •
[🏗 Architecture](#-architecture) •
[🔬 Research Validation](#-research-backed-validation) •
[📊 Benchmarks](#-performance) •
[🤝 Contributing](CONTRIBUTING.md)

---

</div>

## 🧠 What is Verridian AI?

<div align="center">
<img src="assets/images/GSW Giving Language Model a Human Like Episodic Memory.png" alt="GSW Episodic Memory" width="100%">
</div>

<br>

Verridian AI is a **proof-of-concept** legal intelligence system implementing a novel **brain-inspired cognitive architecture**. Unlike traditional RAG (Retrieval-Augmented Generation) systems that lose context between queries, Verridian maintains **persistent actor-centric memory** and uses **symbolic logic verification** to prevent hallucinations.

<details>
<summary><b>🔍 Why is this different from traditional RAG?</b></summary>
<br>

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL RAG vs VERRIDIAN                        │
├────────────────────────────────┬────────────────────────────────────────┤
│        TRADITIONAL RAG         │           VERRIDIAN AI                 │
├────────────────────────────────┼────────────────────────────────────────┤
│                                │                                        │
│   Query → Search → Response    │   Query → Remember → Reason → Verify   │
│                                │                                        │
│   ┌──────┐                     │   ┌──────┐    ┌──────┐    ┌──────┐    │
│   │Query │──→ Chunks ──→ LLM   │   │Query │──→ │Memory│──→ │Logic │    │
│   └──────┘                     │   └──────┘    │ GSW  │    │ VSA  │    │
│                                │               └──────┘    └──────┘    │
│   ❌ No memory between queries │   ✅ Persistent actor-centric memory  │
│   ❌ Entities lost each time   │   ✅ Tracks 5,170+ actors across time │
│   ❌ No hallucination check    │   ✅ Logic verification layer         │
│   ❌ ~8,000 tokens per query   │   ✅ ~3,500 tokens (56% reduction)    │
│                                │                                        │
└────────────────────────────────┴────────────────────────────────────────┘
```

</details>

<details>
<summary><b>📚 Core Concepts</b></summary>
<br>

| Concept | Description |
|---------|-------------|
| **Actor-Centric Memory** | Information organized around entities (actors) rather than events |
| **Persistent Memory** | Memory maintained across multiple queries (vs stateless retrieval) |
| **Structural Separation** | Distinguishing case structure from factual content |
| **Gap Detection** | Identifying missing evidence before responding |
| **Logic Verification** | Anti-hallucination through symbolic reasoning |

</details>

---

## 🏗 Architecture

<div align="center">

### Three-Layer Cognitive System

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ┌─────────────────────────────────────────────────────────────────┐    ║
║   │              LAYER 1: NAVIGATION                                 │    ║
║   │              ━━━━━━━━━━━━━━━━━━                                 │    ║
║   │                                                                  │    ║
║   │   🧭 Tolman-Eichenbaum Machine (TEM)                            │    ║
║   │                                                                  │    ║
║   │   ┌─────────┐      ┌─────────┐      ┌─────────┐                │    ║
║   │   │   MEC   │ ───▶ │  HPC    │ ◀─── │   LEC   │                │    ║
║   │   │  Grid   │      │ Memory  │      │ Sensory │                │    ║
║   │   │  Cells  │      │ Binding │      │ Encoding│                │    ║
║   │   └─────────┘      └─────────┘      └─────────┘                │    ║
║   │                                                                  │    ║
║   │   ► Separates case STRUCTURE from FACTS                         │    ║
║   │   ► Enables zero-shot inference on new case patterns            │    ║
║   │   ► Implementation: src/tem/model.py                            │    ║
║   │                                                                  │    ║
║   └─────────────────────────────────────────────────────────────────┘    ║
║                                  │                                        ║
║                                  ▼                                        ║
║   ┌─────────────────────────────────────────────────────────────────┐    ║
║   │              LAYER 2: AGENCY                                     │    ║
║   │              ━━━━━━━━━━━━━━━                                    │    ║
║   │                                                                  │    ║
║   │   🎯 Active Inference Agent                                     │    ║
║   │                                                                  │    ║
║   │   ┌─────────────────────────────────────────────────────┐       │    ║
║   │   │                                                      │       │    ║
║   │   │   Variational          Expected                      │       │    ║
║   │   │   Free Energy    +     Free Energy    =   Action    │       │    ║
║   │   │   (Perception)         (Exploration)      Selection │       │    ║
║   │   │                                                      │       │    ║
║   │   └─────────────────────────────────────────────────────┘       │    ║
║   │                                                                  │    ║
║   │   ► Detects missing evidence and information gaps               │    ║
║   │   ► Balances exploitation vs exploration                        │    ║
║   │   ► Implementation: src/agency/agent.py                         │    ║
║   │                                                                  │    ║
║   └─────────────────────────────────────────────────────────────────┘    ║
║                                  │                                        ║
║                                  ▼                                        ║
║   ┌─────────────────────────────────────────────────────────────────┐    ║
║   │              LAYER 3: LOGIC                                      │    ║
║   │              ━━━━━━━━━━━━━                                      │    ║
║   │                                                                  │    ║
║   │   🔐 Vector Symbolic Architecture (VSA)                         │    ║
║   │                                                                  │    ║
║   │   ┌─────────┐      ┌─────────┐      ┌─────────┐                │    ║
║   │   │ Binding │      │Bundling │      │Permute  │                │    ║
║   │   │  A ⊗ B  │      │  Σ(V)   │      │ ρ(V)    │                │    ║
║   │   │         │      │         │      │         │                │    ║
║   │   │Role-Fill│      │   Set   │      │Sequence │                │    ║
║   │   └─────────┘      └─────────┘      └─────────┘                │    ║
║   │                                                                  │    ║
║   │   ► Hyperdimensional computing (D=10,000)                       │    ║
║   │   ► Anti-hallucination verification via logic rules             │    ║
║   │   ► Implementation: src/vsa/legal_vsa.py                        │    ║
║   │                                                                  │    ║
║   └─────────────────────────────────────────────────────────────────┘    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</div>

<br>

<details>
<summary><b>🔄 Data Flow Through the System</b></summary>
<br>

```
                           ┌──────────────────────────────────────────────┐
                           │              📄 LEGAL DOCUMENT                │
                           │                                              │
                           │   "In the matter of Smith & Smith [2023]    │
                           │    FamCA 123, the Applicant (John Smith)    │
                           │    seeks property settlement..."            │
                           │                                              │
                           └──────────────────────┬───────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         📥 INGESTION LAYER                                   │
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │    Text      │───▶│    Legal     │───▶│  Reconciler  │                 │
│   │   Chunker    │    │   Operator   │    │              │                 │
│   │              │    │  (6 Tasks)   │    │              │                 │
│   └──────────────┘    └──────────────┘    └──────────────┘                 │
│                                                                              │
│   Tasks: 1. Actor ID  2. Roles  3. States  4. Verbs  5. Questions  6. Links│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      🧠 GLOBAL SEMANTIC WORKSPACE (GSW)                      │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                      │   │
│   │  ACTOR: John Smith                                                  │   │
│   │  ├── type: PERSON                                                   │   │
│   │  ├── roles: [applicant, husband, father]                           │   │
│   │  ├── aliases: [Mr Smith, the Applicant]                            │   │
│   │  ├── states: [married(2010) → separated(2020)]                     │   │
│   │  └── links: [Jane Smith, Family Home, Children]                    │   │
│   │                                                                      │   │
│   │  QUESTIONS: 7,615 predictive questions tracked                      │   │
│   │  LINKS: 646 spatio-temporal connections                            │   │
│   │                                                                      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      ⚡ THREE-LAYER COGNITIVE ENGINE                         │
│                                                                              │
│   Query: "What are the requirements for property settlement?"               │
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │     TEM      │───▶│   Agency     │───▶│     VSA      │                 │
│   │              │    │              │    │              │                 │
│   │  Navigate    │    │  Gap Check   │    │   Verify     │                 │
│   │  Structure   │    │  Evidence?   │    │   Logic      │                 │
│   └──────────────┘    └──────────────┘    └──────────────┘                 │
│                                                                              │
│   ✓ Find similar patterns    ✓ All evidence found    ✓ No contradictions  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
                           ┌──────────────────────────────────────────────┐
                           │            ✅ VERIFIED RESPONSE               │
                           │                                              │
                           │   "Property settlement under the Family     │
                           │    Law Act 1975 requires: 1) Valid marriage │
                           │    2) Separation period..."                 │
                           │                                              │
                           │   📚 Citations: s79 FLA, Smith v Smith      │
                           │   🎯 Confidence: 0.95                       │
                           │                                              │
                           └──────────────────────────────────────────────┘
```

</details>

<details>
<summary><b>💡 Core Innovation: Actor-Centric Memory</b></summary>
<br>

<div align="center">
<img src="assets/images/RAG VS GSW.png" alt="RAG vs GSW Comparison" width="100%">
</div>

Traditional NLP uses **verb-centric triples**: `(Subject, Verb, Object)`

Verridian uses **actor-centric memory** - organizing information around entities:

```python
# Traditional Verb-Centric (loses context)
("John", "married", "Jane")        # Who is John? Lost.
("John", "filed", "Application")   # Same John? Unknown.

# Verridian Actor-Centric (maintains context)
Actor: {
    name: "John Smith",
    type: "PERSON",
    roles: ["applicant", "husband", "father"],
    states: [
        {"name": "MaritalStatus", "value": "married", "when": "2010"},
        {"name": "MaritalStatus", "value": "separated", "when": "2020"}
    ],
    relationships: ["Jane Smith", "Children", "Family Home"],
    timeline: {"2010": "married", "2020": "separated", "2023": "filed"}
}
```

This mirrors how humans actually remember - achieving **85% accuracy** vs 77% for traditional RAG.

</details>

---

## 🔬 Research-Backed Validation

<div align="center">

### CLAUSE Paper Integration

**Implementing "Better Call CLAUSE" Benchmark for Australian Family Law**

[![CLAUSE Paper](https://img.shields.io/badge/Paper-arXiv:2511.00340-b31b1b?style=for-the-badge&logo=arxiv)](https://arxiv.org/abs/2511.00340v1)

</div>

Verridian AI integrates advanced validation techniques from cutting-edge legal AI research to ensure extraction accuracy and statutory compliance.

<details>
<summary><b>📊 Validation Pipeline</b></summary>
<br>

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                       STATUTORY VALIDATION PIPELINE                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐    ║
║   │ Document │  ──▶ │   GSW    │  ──▶ │Statutory │  ──▶ │  Multi-  │    ║
║   │          │      │Extraction│      │Validation│      │  Judge   │    ║
║   │  Input   │      │          │      │   RAG    │      │   Eval   │    ║
║   └──────────┘      └──────────┘      └──────────┘      └──────────┘    ║
║                           │                  │                 │         ║
║                           ▼                  ▼                 ▼         ║
║                     Actors, Roles      FLA 1975         GPT-4o          ║
║                     States, Links      CSAA 1989        Claude          ║
║                     Questions          FLR 2004         Gemini          ║
║                                                                           ║
║   ✓ 10-Category Discrepancy Detection                                   ║
║   ✓ Span-Level Issue Identification                                     ║
║   ✓ Calibrated Confidence Scoring                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</details>

### Key Features

<table>
<tr>
<td width="50%" valign="top">

#### 🎯 Discrepancy Detection
- **10-Category Benchmark**
  - 5 Legal: Payment, Liability, Termination, Jurisdiction, Warranty
  - 5 In-text: Numbers, Dates, Party Names, References, Definitions
- **Span-Level Precision**
  - Pinpoints exact location of issues
  - Character-level alignment metrics
- **Australian Family Law Adapted**
  - Family Law Act 1975
  - Child Support Assessment Act 1989
  - Family Law Rules 2004

</td>
<td width="50%" valign="top">

#### ✅ Validation & Evaluation
- **RAG Statutory Validation**
  - Verify against legislative corpus
  - Case law precedent checking
  - Regulatory compliance
- **Multi-Model Evaluation**
  - GPT-4o, Claude Sonnet, Gemini Pro
  - Consensus-based scoring
  - Hallucination detection
- **Calibrated Confidence**
  - Location alignment metrics
  - Evidence-based certainty
  - Explainable results

</td>
</tr>
</table>

<details>
<summary><b>💻 Quick Usage Example</b></summary>
<br>

```python
from src.validation import StatutoryRAGValidator
from src.benchmarks import FamilyLawDiscrepancyBenchmark
from src.evaluation import MultiJudgeEvaluator

# 1. Validate extraction against statutory corpus
validator = StatutoryRAGValidator("data/statutory_corpus")
result = validator.validate_extraction(
    extraction=gsw_extraction,
    context=original_document
)

# 2. Run discrepancy detection
benchmark = FamilyLawDiscrepancyBenchmark()
discrepancies = benchmark.detect_discrepancies(
    document=court_judgment,
    categories=["payment", "dates", "party_names"]
)

# 3. Multi-judge evaluation
evaluator = MultiJudgeEvaluator(models=["gpt-4o", "claude-sonnet", "gemini-pro"])
scores = evaluator.evaluate(
    extraction=result,
    ground_truth=validated_data
)

print(f"Validation Score: {scores['consensus']:.2f}")
print(f"Confidence: {scores['calibrated_confidence']:.2f}")
print(f"Issues Found: {len(discrepancies)}")
```

**Output:**
```
Validation Score: 0.94
Confidence: 0.89
Issues Found: 2

Discrepancies:
  [1] Payment Term (Line 45-47): Amount mismatch with s79 FLA requirements
  [2] Date Inconsistency (Line 123): Separation date conflicts with filing date
```

</details>

<div align="center">

**📄 Full Technical Report**: [CLAUSE Research Application Report](docs/CLAUSE-Research-Application-Report.md)

</div>

---

## 🚀 Quick Start

<details open>
<summary><b>📋 Prerequisites</b></summary>
<br>

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| Git | Latest | Version control |
| OpenRouter API Key | - | LLM access ([get one](https://openrouter.ai)) |

</details>

<details open>
<summary><b>⚡ Installation (5 minutes)</b></summary>
<br>

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory

# 2️⃣ Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3️⃣ Setup Frontend
cd ui && npm install && cd ..

# 4️⃣ Configure environment
cp .env.example .env
# Edit .env and add: OPENROUTER_API_KEY=sk-or-your-key-here

# 5️⃣ Start the UI
cd ui && npm run dev
```

🎉 **Open http://localhost:3000** - You're ready to go!

</details>

<details>
<summary><b>🎮 Demo Scripts</b></summary>
<br>

```bash
# Full cognitive system demo
python run_full_system.py

# Individual layer demos
python run_vsa_demo.py      # VSA anti-hallucination
python run_micro_tem.py     # TEM navigation
python run_agent_demo.py    # Active inference
```

</details>

---

## 📊 Performance

<div align="center">

### Benchmark Results

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     VERRIDIAN AI                              TRADITIONAL RAG             ║
║                                                                           ║
║     ████████████████████████████ 85%          ██████████████████████ 77%  ║
║                 ACCURACY                               ACCURACY           ║
║                                                                           ║
║     ████████████████ 3,500                    ████████████████████████████║
║        TOKENS/QUERY                             8,000 TOKENS/QUERY        ║
║                                                                           ║
║     ████ 11.83ms                              ████████████████ ~500ms     ║
║      RESPONSE TIME                                RESPONSE TIME           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</div>

| Metric | Verridian | Traditional RAG | Improvement |
|--------|-----------|-----------------|-------------|
| **Accuracy** | 85% | 77% | +10% |
| **Token Usage** | ~3,500/query | ~8,000/query | 56% reduction |
| **Response Time** | 11.83ms | ~500ms | 42x faster |
| **Query Success** | 100% | ~95% | +5% |

<details>
<summary><b>📈 Knowledge Base Statistics</b></summary>
<br>

| Metric | Count |
|--------|-------|
| **Total Actors** | 5,170 |
| **Predictive Questions** | 7,615 |
| **Spatio-Temporal Links** | 646 |
| **Family Law Cases** | 714 |
| **Python LOC** | 14,549 |
| **Documentation Pages** | 25+ |

</details>

---

## 📖 Documentation

<div align="center">

### 📚 [Full Documentation on Wiki](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki)

</div>

<table>
<tr>
<td width="50%" valign="top">

### 🏗 Architecture
- [Architecture Overview](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Architecture-Overview)
- [Three-Layer System](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Three-Layer-System)
- [GSW Workspace](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/GSW-Global-Semantic-Workspace)
- [Data Flow](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Data-Flow)

### ⚙️ Backend Modules
- [GSW Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-GSW-Module)
- [TEM Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-TEM-Module)
- [VSA Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-VSA-Module)
- [Agency Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-Agency-Module)
- [Agents Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-Agents-Module) ⭐
- [Ingestion Module](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-Ingestion-Module) ⭐

</td>
<td width="50%" valign="top">

### 🖥 Frontend
- [Frontend Overview](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Frontend-Overview)
- [API Routes](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Frontend-API-Routes)
- [Components](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Frontend-Components)

### 📘 Guides & Reference
- [Quick Start](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Quick-Start)
- [Development Guide](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Development-Guide)
- [Deployment Guide](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Deployment-Guide)
- [API Reference](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/API-Reference)
- [Data Schemas](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Data-Schemas) ⭐
- [File Index](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/File-Index) ⭐
- [Glossary](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Glossary)

</td>
</tr>
</table>

---

## 🗂 Project Structure

```
📦 Functional-Structure-of-Episodic-Memory
├── 🐍 src/                      # Python Backend (14,549 LOC)
│   ├── gsw/                     # Global Semantic Workspace
│   │   ├── legal_operator.py    # 6-task extraction pipeline
│   │   ├── workspace.py         # Workspace persistence
│   │   └── text_chunker.py      # Document chunking
│   ├── tem/                     # Tolman-Eichenbaum Machine
│   │   ├── model.py             # PyTorch TEM implementation
│   │   └── action_space.py      # Legal action definitions
│   ├── vsa/                     # Vector Symbolic Architecture
│   │   ├── legal_vsa.py         # Hyperdimensional logic
│   │   └── ontology.py          # Legal ontology rules
│   ├── agency/                  # Active Inference
│   │   ├── agent.py             # POMDP agent
│   │   └── generative_model.py  # A,B,C,D matrices
│   ├── agents/                  # LangChain Tools
│   ├── ingestion/               # Document Processing
│   └── logic/                   # Schemas & Rules
│
├── 🌐 ui/                       # Next.js 16 Frontend
│   ├── src/app/                 # App Router
│   │   ├── page.tsx             # Chat interface
│   │   ├── visualize/           # 3D graph visualization
│   │   └── api/                 # API routes
│   ├── src/components/          # React components
│   └── src/lib/                 # TypeScript libraries
│
├── 📊 data/                     # Knowledge Base
│   ├── workspaces/              # GSW workspace snapshots
│   ├── benchmarks/              # Test data
│   └── legislation/             # Family Law Act sections
│
├── 📚 wiki/                     # 25+ Documentation Pages
├── 🖼 assets/                   # Visual Assets
└── 🧪 tests/                    # Test Suite
```

---

## 🔬 Research

<div align="center">

This project implements research from:

[![arXiv](https://img.shields.io/badge/arXiv-2511.07587-b31b1b?style=for-the-badge&logo=arxiv)](https://arxiv.org/abs/2511.07587)

**"Functional Structure of Episodic Memory"**

Based on:
- **Tolman-Eichenbaum Machine** (Whittington et al., 2020)
- **Active Inference** (Friston et al.)
- **Global Workspace Theory** (Baars)
- **Hyperdimensional Computing** (Kanerva)

</div>

---

## 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md).

```bash
# Quick contribution workflow
git checkout -b feature/your-feature
# Make changes
pytest tests/
git commit -m "feat(module): description"
git push origin feature/your-feature
# Open Pull Request
```

<details>
<summary><b>📋 Contribution Areas</b></summary>
<br>

- 🐛 **Bug fixes** - Help squash bugs
- ✨ **New features** - Add new capabilities
- 📚 **Documentation** - Improve docs and examples
- 🧪 **Tests** - Increase test coverage
- 🎨 **UI/UX** - Enhance the frontend

</details>

---

## 📜 License

<div align="center">

MIT License - see [LICENSE](LICENSE) for details.

---

### Built by [Verridian AI](https://github.com/Verridian-ai)

*Cognitive AI for Legal Intelligence*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Verridian--ai-181717?style=for-the-badge&logo=github)](https://github.com/Verridian-ai)
[![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b?style=for-the-badge&logo=arxiv)](https://arxiv.org/abs/2511.07587)
[![Issues](https://img.shields.io/badge/Issues-Report-red?style=for-the-badge&logo=github)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)
[![Discussions](https://img.shields.io/badge/Discussions-Join-purple?style=for-the-badge&logo=github)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/discussions)

---

**Proof of Concept** • Production-ready Architecture • Demonstration Data Scale

<br>

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   "The brain doesn't search for memories - it reconstructs them."        ║
║                                                                           ║
║                              - Cognitive Neuroscience Principle          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</div>
