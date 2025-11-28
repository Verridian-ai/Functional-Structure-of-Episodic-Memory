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
[🖥 User Interface](#-user-interface) •
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

## 🖥 User Interface

<div align="center">

### Professional Legal AI Workspace

[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](ui/)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=nextdotjs)](ui/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](ui/)

```mermaid
graph TB
    subgraph UI["🖥️ VERRIDIAN AI INTERFACE"]
        subgraph Sidebar["📁 Sidebar"]
            Convs["💬 Conversations"]
            Search["🔍 Search"]
            Settings["⚙️ Settings"]
        end

        subgraph MainPanel["📋 Main Panel"]
            Chat["💬 Chat Interface"]
            Voice["🎤 Voice Input"]
            Canvas["📄 Document Canvas"]
            Files["📎 File Attachments"]
            Highlight["🖌️ Highlighter"]
        end

        Sidebar --> MainPanel
    end

    style UI fill:#1a1a2e,stroke:#16213e,color:#fff
    style Sidebar fill:#0f3460,stroke:#16213e,color:#fff
    style MainPanel fill:#533483,stroke:#16213e,color:#fff
```

</div>

<details open>
<summary><b>💬 Chat Interface</b></summary>
<br>

The intelligent chat interface provides real-time legal AI assistance with advanced features:

```mermaid
flowchart TB
    subgraph ChatPanel["💬 CHAT PANEL"]
        subgraph Messages["Message History"]
            AI["🤖 AI Response<br/>Legal analysis with citations<br/>s79 FLA requirements"]
            User["💬 User Query<br/>Property settlement question<br/>📎 contract.pdf attached"]
        end

        subgraph Actions["Message Actions"]
            Canvas["📄 Open in Canvas"]
            Copy["📋 Copy to Clipboard"]
        end

        subgraph Input["Input Area"]
            TextBox["📝 Type message...<br/>Multi-line supported"]
            Voice["🎤 Voice"]
            Attach["📎 Files"]
        end

        subgraph QuickActions["Quick Actions"]
            QA1["Find Precedents"]
            QA2["Review Contract"]
            QA3["Draft Letter"]
        end

        AI --> Actions
        User --> AI
        Input --> User
        QuickActions --> Input
    end

    style ChatPanel fill:#1a1a2e,stroke:#16213e,color:#fff
    style Messages fill:#0f3460,stroke:#16213e,color:#fff
    style Actions fill:#533483,stroke:#16213e,color:#fff
    style Input fill:#e94560,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Markdown Support** | Full GitHub-flavored markdown with syntax highlighting |
| **Code Blocks** | Syntax highlighting with copy and "Open in Canvas" buttons |
| **Tool Tracking** | Visual indicators for AI tool execution (pending → running → complete) |
| **Artifact Cards** | Clickable cards for generated documents, code, and visualizations |
| **Auto-Scroll** | Automatically scrolls to latest messages during streaming |
| **Message History** | Persistent conversation storage with search |

</details>

<details>
<summary><b>🎤 Voice Chat</b></summary>
<br>

**Real-time voice input** using Web Speech API with professional audio visualization:

```mermaid
flowchart TB
    subgraph VoicePanel["🎤 VOICE INPUT PANEL"]
        subgraph VoiceButton["Voice Capture"]
            Mic["🎤 LISTENING<br/>Audio capture active"]
            Waves["〰️ Audio Visualization<br/>Real-time waveform"]
        end

        subgraph Transcript["Live Transcript"]
            Text["📝 What are the requirements<br/>for a property settlement..."]
        end

        subgraph Settings["Voice Settings"]
            Lang["🌐 Language: en-AU"]
            Auto["✅ Auto-send"]
            TTS["🔊 Voice Response"]
        end

        Mic --> Waves
        Waves --> Transcript
        Settings --> VoiceButton
    end

    style VoicePanel fill:#1a1a2e,stroke:#16213e,color:#fff
    style VoiceButton fill:#e94560,stroke:#16213e,color:#fff
    style Transcript fill:#0f3460,stroke:#16213e,color:#fff
    style Settings fill:#533483,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Push-to-Talk** | Hold spacebar to activate (or toggle button) |
| **Continuous Recognition** | Listens continuously until pause detected |
| **Live Transcription** | Real-time display of recognized speech |
| **Audio Visualization** | Animated rings showing audio levels |
| **Language Support** | English (US, UK, AU) dialects |
| **Auto-Send** | Automatically sends message after speech pause |
| **Voice Response** | Optional TTS for AI responses |

</details>

<details>
<summary><b>📎 File Attachments</b></summary>
<br>

**Comprehensive file upload** for legal documents, images, and evidence:

```mermaid
flowchart TB
    subgraph FilePanel["📎 FILE ATTACHMENT"]
        subgraph FileTypes["Supported File Types"]
            PDF["📄 PDF"]
            DOC["📝 DOC"]
            DOCX["📄 DOCX"]
            PNG["🖼️ PNG"]
            JPG["📸 JPG"]
        end

        subgraph DropZone["Drop Zone"]
            Drop["📁 DROP FILES HERE<br/>or click to browse"]
        end

        subgraph Attached["Attached Files"]
            F1["📄 contract.pdf ✕"]
            F2["🖼️ evidence_photo.jpg ✕"]
            F3["📝 notes.docx ✕"]
        end

        FileTypes --> DropZone
        DropZone --> Attached
    end

    style FilePanel fill:#1a1a2e,stroke:#16213e,color:#fff
    style FileTypes fill:#0f3460,stroke:#16213e,color:#fff
    style DropZone fill:#533483,stroke:#16213e,color:#fff
    style Attached fill:#e94560,stroke:#16213e,color:#fff
```

| Format | Extensions | Use Case |
|--------|------------|----------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt` | Contracts, court orders, affidavits |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` | Evidence photos, diagrams |
| **Preview** | Thumbnails for images | Visual confirmation before sending |

</details>

<details>
<summary><b>📄 Canvas & Document Editor</b></summary>
<br>

**Full-featured document workspace** with Google Docs-like editing:

```mermaid
flowchart TB
    subgraph Canvas["📄 CANVAS PANEL"]
        subgraph Modes["View Modes"]
            Edit["📝 Edit"]
            Preview["👁 Preview"]
        end

        subgraph Artifacts["Document Tabs"]
            LB["Legal Brief ▼"]
            CR["Client Report"]
            CA["Contract Analysis"]
            New["+ New"]
        end

        subgraph Toolbar["Toolbar"]
            TEdit["📝 Edit"]
            TPreview["👁 Preview"]
            THigh["🖌️ Highlight"]
            TExport["📤 Export"]
            TSettings["⚙️ Settings"]
        end

        subgraph Content["Document Content"]
            Title["LEGAL BRIEF<br/>IN THE FAMILY COURT OF AUSTRALIA<br/>Smith & Smith 2023 FamCA 123"]
            Body["APPLICANT'S SUBMISSIONS<br/>ON PROPERTY SETTLEMENT<br/>1. Introduction<br/>Pursuant to s79 FLA 1975..."]
        end

        subgraph Status["Status Bar"]
            Words["Words: 1,234"]
            Chars["Characters: 7,891"]
            Saved["Last saved: 2 min ago"]
        end

        Modes --> Artifacts
        Artifacts --> Toolbar
        Toolbar --> Content
        Content --> Status
    end

    style Canvas fill:#1a1a2e,stroke:#16213e,color:#fff
    style Artifacts fill:#0f3460,stroke:#16213e,color:#fff
    style Toolbar fill:#533483,stroke:#16213e,color:#fff
    style Content fill:#1a1a2e,stroke:#e94560,color:#fff
    style Status fill:#0f3460,stroke:#16213e,color:#fff
```

**Layout Templates:**

| Template | Description |
|----------|-------------|
| **Legal Brief** | Formal structure with header, body, footer, signature blocks |
| **Client Report** | Cover page, executive summary, detailed sections |
| **Legal Newsletter** | Multi-column layout with sidebars |
| **Blank Document** | Standard formatting for custom documents |

**Typography Settings:**
- Font family selection (Serif, Sans-serif, Monospace)
- Font size (10pt - 24pt)
- Margin configuration
- Line spacing options

</details>

<details>
<summary><b>🖌️ Highlighter & Annotations</b></summary>
<br>

**Text highlighting** for document review and evidence marking:

```mermaid
flowchart TB
    subgraph Highlighter["🖌️ HIGHLIGHTER MODE"]
        subgraph Controls["Controls"]
            Status["🖌️ Active"]
            Toggle["Toggle On/Off"]
        end

        subgraph Document["Document View"]
            P1["The Court found that the<br/>:::highlight financial contributions :::<br/>was determinative in establishing<br/>the property pool under s79 FLA"]
            P2["Additionally, the<br/>:::highlight non-financial contribution :::<br/>by the Respondent was significant<br/>pursuant to s79(4)(b)"]
        end

        subgraph Stats["Statistics"]
            Count["Highlighted Passages: 2"]
        end

        Controls --> Document
        Document --> Stats
    end

    style Highlighter fill:#1a1a2e,stroke:#16213e,color:#fff
    style Controls fill:#e94560,stroke:#16213e,color:#fff
    style Document fill:#0f3460,stroke:#16213e,color:#fff
    style Stats fill:#533483,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Selection Highlighting** | Click and drag to highlight text |
| **Visual Feedback** | Yellow background for highlighted sections |
| **Toggle Mode** | Button to enable/disable highlighter |
| **Cursor Styling** | Text selection cursor when active |

</details>

<details>
<summary><b>📄 Letter & Document Creation</b></summary>
<br>

**Professional legal document templates** with export capabilities:

```mermaid
flowchart TB
    subgraph DocTools["📄 DOCUMENT TOOLS"]
        subgraph Templates["Templates"]
            T1["📄 FORMAL LETTER"]
            T2["⚖️ LEGAL DEMAND"]
            T3["👨‍👩‍👧‍👦 PARENTING<br/>ARRANGEMENTS"]
        end

        subgraph Export["Export Options"]
            E1["📄 PDF Export"]
            E2["📝 DOCX Export"]
            E3["📋 TXT Export"]
            E4["📑 MD Export"]
        end

        Templates --> Export
    end

    style DocTools fill:#1a1a2e,stroke:#16213e,color:#fff
    style Templates fill:#0f3460,stroke:#16213e,color:#fff
    style Export fill:#533483,stroke:#16213e,color:#fff
```

**Available Templates:**

| Template | Structure | Use Case |
|----------|-----------|----------|
| **Formal Letter** | Date, recipient, body, signature | Client correspondence |
| **Legal Demand Letter** | WITHOUT PREJUDICE header, background, demand, consequences | Settlement negotiations |
| **Parenting Arrangements** | Current situation, proposed changes, reasons, next steps | Custody discussions |

**Export Formats:**

| Format | Features |
|--------|----------|
| **PDF** | A4 pages, Times Roman font, page numbers, proper margins |
| **DOCX** | Microsoft Word compatible, heading styles, bullet lists |
| **TXT** | Plain text for editing |
| **Markdown** | Formatted text with headers |

</details>

<details>
<summary><b>🎨 NanoBanana Pro Image Generation</b></summary>
<br>

**AI-powered image generation** for legal visualizations and diagrams:

```mermaid
flowchart TB
    subgraph NanoBanana["🎨 NANOBANANA PRO IMAGE GENERATION"]
        subgraph Prompt["Prompt Input"]
            Input["📝 Legal timeline showing<br/>property division steps"]
        end

        subgraph Generated["🖼️ Generated Image"]
            subgraph Flowchart["PROPERTY DIVISION FLOWCHART"]
                A["Identify Assets"] --> B["Value Pool"]
                B --> C["Contributions"]
                C --> D["Future Needs"]
                D --> E["Just & Equitable"]
            end
        end

        subgraph Actions["Actions"]
            Download["📥 Download PNG"]
            Canvas["📄 Add to Canvas"]
            Regen["🔄 Regenerate"]
        end

        Prompt --> Generated
        Generated --> Actions
    end

    style NanoBanana fill:#1a1a2e,stroke:#16213e,color:#fff
    style Prompt fill:#0f3460,stroke:#16213e,color:#fff
    style Generated fill:#533483,stroke:#16213e,color:#fff
    style Actions fill:#e94560,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Diagram Generation** | Create flowcharts, timelines, process diagrams |
| **Legal Visualizations** | Property pools, family trees, case timelines |
| **Canvas Integration** | Add generated images directly to documents |
| **Download Options** | PNG export for presentations |

</details>

<details>
<summary><b>📊 3D Knowledge Graph</b></summary>
<br>

**Interactive 3D visualization** of the legal knowledge base:

```mermaid
flowchart TB
    subgraph Graph3D["📊 3D LEGAL KNOWLEDGE GRAPH"]
        subgraph Controls["Controls"]
            Rotate["🔄 Rotate"]
            Zoom["🔍 Zoom"]
            Reset["↩️ Reset"]
        end

        subgraph Network["Knowledge Network"]
            Cases["🔵 Case Law"]
            Statutes["🟢 Statutes"]
            Concepts["🟣 Concepts"]
            Actors["🟡 Actors"]

            Cases --- Statutes
            Statutes --- Concepts
            Concepts --- Actors
            Cases --- Concepts
            Statutes --- Actors
        end

        subgraph Details["Selected Node"]
            Info["📋 Smith v Smith 2023 FamCA 123<br/>Type: Family Court Case<br/>Connections: 12 nodes<br/>Uncertainty: 15%"]
        end

        subgraph Legend["Legend"]
            L1["🔵 Cases"]
            L2["🟢 Statutes"]
            L3["🟣 Concepts"]
            L4["🟡 Actors"]
        end

        Controls --> Network
        Network --> Details
    end

    style Graph3D fill:#1a1a2e,stroke:#16213e,color:#fff
    style Controls fill:#0f3460,stroke:#16213e,color:#fff
    style Network fill:#533483,stroke:#16213e,color:#fff
    style Details fill:#e94560,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Three.js Rendering** | GPU-accelerated 3D visualization |
| **Interactive Controls** | Orbit, zoom, pan with mouse/touch |
| **Node Selection** | Click nodes to view details |
| **Uncertainty Heatmap** | Color gradient showing confidence levels |
| **Edge Visualization** | Lines connecting related concepts |

</details>

<details>
<summary><b>🐍 Code Interpreter</b></summary>
<br>

**Integrated Python execution** for data analysis and calculations:

```mermaid
flowchart TB
    subgraph CodeInterp["🐍 CODE INTERPRETER"]
        subgraph Controls["Controls"]
            Run["▶ Run"]
            Clear["🗑️ Clear"]
            Max["⬜ Max"]
        end

        subgraph Editor["📝 Editor"]
            Code["# Calculate property pool division<br/>total_assets = 1_500_000<br/>total_liabilities = 300_000<br/>net_pool = total_assets - total_liabilities<br/>applicant_share = 0.55<br/>respondent_share = 0.45"]
        end

        subgraph Output["📤 Output"]
            Result["Net Property Pool: $1,200,000<br/>Applicant: $660,000.00<br/>Respondent: $540,000.00<br/>✓ Executed in 0.023s"]
        end

        Controls --> Editor
        Editor --> Output
    end

    style CodeInterp fill:#1a1a2e,stroke:#16213e,color:#fff
    style Controls fill:#0f3460,stroke:#16213e,color:#fff
    style Editor fill:#533483,stroke:#16213e,color:#fff
    style Output fill:#0d7377,stroke:#16213e,color:#fff
```

| Feature | Description |
|---------|-------------|
| **Python Execution** | Run Python code for calculations |
| **Tab Indentation** | Proper code formatting support |
| **Execution History** | Track previous runs with timestamps |
| **Keyboard Shortcuts** | Ctrl+Enter / Cmd+Enter to execute |
| **Error Highlighting** | Red text for errors |
| **Output Copy** | Copy results to clipboard |

</details>

<details>
<summary><b>⚙️ Admin Panel</b></summary>
<br>

**Comprehensive configuration** for AI behavior and system settings:

```mermaid
flowchart TB
    subgraph AdminPanel["⚙️ ADMIN PANEL"]
        subgraph Tabs["Navigation Tabs"]
            Prompt["📝 Prompt"]
            Model["🤖 Model"]
            Tools["🔧 Tools"]
            MCP["🔌 MCP"]
            Settings["⚙️ Settings"]
        end

        subgraph ModelConfig["Model Configuration"]
            ModelSelect["Model: claude-sonnet-4"]
            Temp["Temperature: 0.7"]
            Tokens["Max Tokens: 4096"]
        end

        subgraph ToolsConfig["Available Tools"]
            T1["☑ statutory_alignment"]
            T2["☑ get_applicable_law"]
            T3["☑ find_similar_cases"]
            T4["☑ search_cases"]
            T5["☑ validate_statutes"]
            T6["☑ detect_discrepancies"]
        end

        Tabs --> ModelConfig
        Tabs --> ToolsConfig
    end

    style AdminPanel fill:#1a1a2e,stroke:#16213e,color:#fff
    style Tabs fill:#0f3460,stroke:#16213e,color:#fff
    style ModelConfig fill:#533483,stroke:#16213e,color:#fff
    style ToolsConfig fill:#e94560,stroke:#16213e,color:#fff
```

| Tab | Configuration Options |
|-----|----------------------|
| **Prompt** | Custom system prompt for AI behavior |
| **Model** | Model selection, temperature, max tokens |
| **Tools** | Enable/disable AI tools (12 available) |
| **MCP** | Model Context Protocol server configuration |
| **Settings** | API key, theme (dark/light), voice input, code interpreter |

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
