<div align="center">

# 🧠 Verridian AI Documentation

### Brain-Inspired Legal Intelligence Platform

[![arXiv](https://img.shields.io/badge/arXiv-2511.07587-b31b1b?style=for-the-badge&logo=arxiv)](https://arxiv.org/abs/2511.07587)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=nextdotjs)](ui/)

---

**85% Accuracy** • **56% Token Reduction** • **42x Faster** • **100% Success Rate**

</div>

---

## 👋 Welcome

Welcome to the **Verridian AI** documentation. This brain-inspired legal AI system achieves **85% accuracy** on complex Australian Family Law queries using a novel cognitive architecture that gives language models human-like episodic memory. The system includes comprehensive validation capabilities through statutory RAG verification, multi-judge evaluation, and span detection for evidence extraction.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   📄 Legal Document  ──▶  🧠 GSW Memory  ──▶  ⚡ Cognitive Engine  ──▶  ✅ ║
║                                                                           ║
║       Input               Actor-Centric       TEM + Agency + VSA    Verified ║
║                            Extraction                                Response ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 🚀 Quick Navigation

<table>
<tr>
<td width="50%" valign="top">

### 🏗 Getting Started
| Guide | Description |
|-------|-------------|
| **[Quick Start](Quick-Start)** | Get running in 10 minutes |
| [Architecture Overview](Architecture-Overview) | Understand the system |
| [Development Guide](Development-Guide) | Set up for development |

### 📚 Core Concepts
| Concept | Learn More |
|---------|------------|
| [Three-Layer System](Three-Layer-System) | TEM + Agency + VSA |
| [GSW Workspace](GSW-Global-Semantic-Workspace) | Actor-centric memory |
| [Data Flow](Data-Flow) | How data moves through |

</td>
<td width="50%" valign="top">

### ⚙️ Backend Modules
| Module | Purpose |
|--------|---------|
| [GSW Module](Backend-GSW-Module) | 6-task extraction |
| [TEM Module](Backend-TEM-Module) | Navigation layer |
| [VSA Module](Backend-VSA-Module) | Logic verification |
| [Agency Module](Backend-Agency-Module) | Gap detection |
| [Benchmarks Module](Backend-Benchmarks-Module) | Family Law Benchmark |
| [Validation Module](Backend-Validation-Module) | Statutory RAG |
| [Evaluation Module](Backend-Evaluation-Module) | Multi-Judge |
| [Span Detector](Backend-Span-Detector) | Span Detection |

### 🖥 Frontend
| Page | Description |
|------|-------------|
| [Frontend Overview](Frontend-Overview) | Next.js architecture |
| [API Routes](Frontend-API-Routes) | REST endpoints |
| [Components](Frontend-Components) | React components |

</td>
</tr>
</table>

---

## 🏗 System Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           VERRIDIAN AI ARCHITECTURE                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        INGESTION LAYER                                   │  │
│  │  ┌──────────┐    ┌──────────────┐    ┌────────────┐                     │  │
│  │  │ Chunker  │───▶│Legal Operator│───▶│ Reconciler │                     │  │
│  │  └──────────┘    │  (6 Tasks)   │    └────────────┘                     │  │
│  │                  └──────────────┘                                        │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                          │
│                                    ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                   GLOBAL SEMANTIC WORKSPACE (GSW)                        │  │
│  │                                                                          │  │
│  │   Actors: 5,170    Questions: 7,615    Links: 646    Cases: 714         │  │
│  │                                                                          │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                          │
│                                    ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                     THREE-LAYER COGNITIVE ENGINE                         │  │
│  │                                                                          │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │  │
│  │  │  Layer 1    │    │  Layer 2    │    │  Layer 3    │                  │  │
│  │  │    TEM      │───▶│   Agency    │───▶│    VSA      │                  │  │
│  │  │ Navigation  │    │ Gap Detect  │    │   Logic     │                  │  │
│  │  └─────────────┘    └─────────────┘    └─────────────┘                  │  │
│  │                                                                          │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Description | Impact |
|---------|-------------|--------|
| 🧠 **Actor-Centric Memory** | Tracks legal entities across queries | +10% accuracy |
| 🔐 **Anti-Hallucination** | VSA logic layer verifies claims | Prevents false outputs |
| 🎯 **Gap Detection** | Identifies missing evidence first | Better responses |
| 📚 **Statute Alignment** | Maps to Family Law Act sections | Legal accuracy |
| ⚡ **Token Efficiency** | 56% fewer tokens per query | Cost savings |
| ✅ **Multi-Judge Validation** | Comprehensive evaluation framework | Quality assurance |
| 🔍 **Span Detection** | Precise evidence extraction | Enhanced accuracy |

---

## 📊 Performance Metrics

```
╔═════════════════════════════════════════════════════════════╗
║                    BENCHMARK COMPARISON                     ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║   Accuracy        ████████████████████████░░░░  85%        ║
║   vs RAG 77%      ████████████████████░░░░░░░░  77%        ║
║                                                             ║
║   Token Usage     ████████████░░░░░░░░░░░░░░░░  3,500      ║
║   vs RAG 8K       ████████████████████████████  8,000      ║
║                                                             ║
║   Response Time   ██░░░░░░░░░░░░░░░░░░░░░░░░░░  11.83ms    ║
║   vs RAG ~500ms   ████████████████████░░░░░░░░  ~500ms     ║
║                                                             ║
╚═════════════════════════════════════════════════════════════╝
```

| Metric | Verridian | Traditional RAG |
|--------|-----------|-----------------|
| Accuracy | 85% | 77% |
| Response Time | 11.83ms | ~500ms |
| Tokens per Query | ~3,500 | ~8,000 |
| Query Success Rate | 100% | ~95% |

---

## 🗂 Documentation Sections

### 🏗 Architecture
- **[Architecture Overview](Architecture-Overview)** - High-level system design and component interactions
- **[Three-Layer System](Three-Layer-System)** - TEM, Agency, and VSA layer details
- **[GSW Workspace](GSW-Global-Semantic-Workspace)** - Actor-centric memory model
- **[Data Flow](Data-Flow)** - End-to-end data pipeline

### ⚙️ Backend Modules
- **[GSW Module](Backend-GSW-Module)** - 6-task extraction pipeline and Legal Operator
- **[TEM Module](Backend-TEM-Module)** - PyTorch navigation layer (Tolman-Eichenbaum Machine)
- **[VSA Module](Backend-VSA-Module)** - Hyperdimensional computing for logic verification
- **[Agency Module](Backend-Agency-Module)** - Active inference agent for gap detection
- **[Ingestion Module](Backend-Ingestion-Module)** - Document processing and classification
- **[Agents Module](Backend-Agents-Module)** - LangChain tool integration
- **[Benchmarks Module](Backend-Benchmarks-Module)** - Family Law benchmark dataset and evaluation
- **[Validation Module](Backend-Validation-Module)** - Statutory RAG validation system
- **[Evaluation Module](Backend-Evaluation-Module)** - Multi-judge evaluation framework
- **[Span Detector](Backend-Span-Detector)** - Span detection for evidence extraction

### 🖥 Frontend
- **[Frontend Overview](Frontend-Overview)** - Next.js 16 application architecture
- **[API Routes](Frontend-API-Routes)** - REST API documentation
- **[Components](Frontend-Components)** - React component catalog

### 📘 Guides
- **[Quick Start](Quick-Start)** - Get running in 10 minutes
- **[Development Guide](Development-Guide)** - Development environment setup
- **[Deployment Guide](Deployment-Guide)** - Production deployment
- **[Contributing](Contributing)** - Contribution guidelines

### 📚 Reference
- **[API Reference](API-Reference)** - Complete endpoint documentation
- **[Data Schemas](Data-Schemas)** - Pydantic schema definitions
- **[Glossary](Glossary)** - 50+ terminology definitions
- **[File Index](File-Index)** - Complete codebase file listing

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory

# Install dependencies
pip install -r requirements.txt
cd ui && npm install && cd ..

# Configure environment
cp .env.example .env
# Add your OPENROUTER_API_KEY

# Run the system
cd ui && npm run dev
```

Open **http://localhost:3000** to access the interface.

See [Quick Start Guide](Quick-Start) for detailed instructions.

---

## 🔬 Research

This project implements research from:

> **"Functional Structure of Episodic Memory"**
> [arXiv:2511.07587](https://arxiv.org/abs/2511.07587)

Based on neuroscience research:
- **Tolman-Eichenbaum Machine** (Whittington et al., 2020)
- **Active Inference** (Friston et al.)
- **Global Workspace Theory** (Baars)
- **Hyperdimensional Computing** (Kanerva)

---

## 🤝 Contributing

We welcome contributions! See the [Contributing Guidelines](Contributing) for:
- Bug reports and feature requests
- Pull request process
- Code style guidelines
- Testing requirements

---

<div align="center">

### Built by [Verridian AI](https://github.com/Verridian-ai)

*Cognitive AI for Legal Intelligence*

[![GitHub](https://img.shields.io/badge/GitHub-Verridian--ai-181717?style=flat-square&logo=github)](https://github.com/Verridian-ai)
[![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2511.07587)
[![Issues](https://img.shields.io/badge/Issues-Report-red?style=flat-square&logo=github)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)

</div>
