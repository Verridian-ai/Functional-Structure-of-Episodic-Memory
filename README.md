<div align="center">

<img src="assets/images/verridian_logo.png" alt="Verridian AI" width="200">

# VERRIDIAN AI

### Brain-Inspired Legal Intelligence Platform

[![arXiv](https://img.shields.io/badge/arXiv-2511.07587-b31b1b?style=flat-square)](https://arxiv.org/abs/2511.07587)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-Next.js_16-3178C6?style=flat-square&logo=typescript&logoColor=white)](ui/)
[![PyTorch](https://img.shields.io/badge/PyTorch-TEM+VSA-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](src/tem/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[![Wiki](https://img.shields.io/badge/Documentation-Wiki-blue?style=for-the-badge)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki)
[![Contributing](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

---

**85% Accuracy** · **56% Fewer Tokens** · **42x Faster** · **100% Query Success**

[Quick Start](#-quick-start) · [Documentation](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki) · [Architecture](#-architecture) · [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

Verridian AI is a **proof-of-concept** legal intelligence system that implements a novel **brain-inspired cognitive architecture**. Unlike traditional RAG systems, Verridian maintains persistent actor-centric memory and uses symbolic logic verification to prevent hallucinations.

<div align="center">
<img src="assets/images/RAG VS GSW.png" alt="RAG vs GSW Comparison" width="100%">
</div>

### Key Differentiators

| Feature | Traditional RAG | Verridian AI |
|---------|----------------|--------------|
| **Memory Model** | Document chunks | Actor-centric persistent memory |
| **Entity Tracking** | Lost between queries | Maintained across session |
| **Hallucination Prevention** | None | VSA logic verification |
| **Accuracy** | 77% | **85%** |
| **Token Usage** | ~8,000/query | **~3,500/query** |

---

## Documentation

<div align="center">

### 📚 [Full Documentation on Wiki](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki)

</div>

| Guide | Description |
|-------|-------------|
| [**Home**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki) | Documentation overview and navigation |
| [**Architecture Overview**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Architecture-Overview) | System design and component interactions |
| [**Three-Layer System**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Three-Layer-System) | TEM + Agency + VSA deep dive |
| [**Quick Start**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Quick-Start) | Get running in 10 minutes |
| [**API Reference**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Frontend-API-Routes) | REST API documentation |
| [**Glossary**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Glossary) | Legal AI terminology |

### Module Documentation

| Module | Description |
|--------|-------------|
| [**GSW Module**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-GSW-Module) | Global Semantic Workspace - 6-task extraction pipeline |
| [**TEM Module**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-TEM-Module) | Tolman-Eichenbaum Machine - PyTorch navigation layer |
| [**VSA Module**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-VSA-Module) | Vector Symbolic Architecture - Anti-hallucination logic |
| [**Agency Module**](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/wiki/Backend-Agency-Module) | Active Inference - Gap detection and decision making |

---

## 🏗 Architecture

Verridian implements a **three-layer cognitive architecture** based on neuroscience research:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: NAVIGATION (Tolman-Eichenbaum Machine)               │
│  Separates case STRUCTURE from FACTS                            │
│  Enables zero-shot inference on new case patterns               │
│  Implementation: src/tem/model.py                               │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: AGENCY (Active Inference)                             │
│  Detects missing evidence and information gaps                  │
│  Balances exploitation vs exploration                           │
│  Implementation: src/agency/agent.py                            │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: LOGIC (Vector Symbolic Architecture)                  │
│  Hyperdimensional computing (D=10,000)                          │
│  Anti-hallucination verification via logic rules                │
│  Implementation: src/vsa/legal_vsa.py                           │
└─────────────────────────────────────────────────────────────────┘
```

### Core Innovation: Actor-Centric Memory

Traditional NLP uses verb-centric triples: `(Subject, Verb, Object)`

Verridian uses **actor-centric memory**:

```python
Actor: {
    name: "John Smith",
    type: "PERSON",
    roles: ["applicant", "husband", "father"],
    states: ["married → separated → divorced"],
    timeline: {"2010": "married", "2020": "separated"},
    relationships: ["Jane Smith", "Children", "Family Home"]
}
```

This mirrors how humans actually remember—and achieves **85% accuracy** vs 77% for traditional RAG.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenRouter API key ([get one here](https://openrouter.ai))

### Installation

```bash
# Clone repository
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env

# Start the UI
cd ui && npm install && npm run dev
```

Open **http://localhost:3000** to access the interface.

### Run Demos

```bash
python run_vsa_demo.py      # VSA anti-hallucination demo
python run_micro_tem.py     # TEM navigation demo
python run_agent_demo.py    # Active inference demo
python run_full_system.py   # Full cognitive system
```

---

## 📊 Performance

### Benchmark Results

| Metric | Result |
|--------|--------|
| **Accuracy** | 85% (vs 77% RAG) |
| **Token Usage** | ~3,500/query (56% reduction) |
| **Response Time** | 11.83ms average |
| **Query Success** | 100% |

### Knowledge Base

| Metric | Count |
|--------|-------|
| Total Actors | 5,170 |
| Predictive Questions | 7,615 |
| Spatio-Temporal Links | 646 |
| Family Law Cases | 714 |

---

## 🗂 Project Structure

```
├── src/
│   ├── gsw/          # Global Semantic Workspace
│   ├── tem/          # Tolman-Eichenbaum Machine (PyTorch)
│   ├── vsa/          # Vector Symbolic Architecture
│   ├── agency/       # Active Inference Agent
│   ├── agents/       # LangChain Tools
│   └── retrieval/    # Hybrid Search
├── ui/               # Next.js 16 Frontend
├── data/             # Knowledge Base
├── tests/            # Test Suite
└── docs/             # Research Papers
```

---

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

```bash
# Fork, clone, and create branch
git checkout -b feature/your-feature

# Make changes with tests
pytest tests/

# Submit PR
git push origin feature/your-feature
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 Research

This project implements research from:

> **"Functional Structure of Episodic Memory"**
> [arXiv:2511.07587](https://arxiv.org/abs/2511.07587)

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

### Built by [Verridian AI](https://github.com/Verridian-ai)

*Cognitive AI for Legal Intelligence*

[![GitHub](https://img.shields.io/badge/GitHub-Verridian--ai-181717?style=flat-square&logo=github)](https://github.com/Verridian-ai)
[![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b?style=flat-square)](https://arxiv.org/abs/2511.07587)
[![Issues](https://img.shields.io/badge/Issues-Report-red?style=flat-square)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)
[![Discussions](https://img.shields.io/badge/Discussions-Join-purple?style=flat-square)](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/discussions)

---

**Proof of Concept** · Production-ready architecture · Demonstration data scale

</div>
