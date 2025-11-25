# Verridian Legal AI - Complete Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
   - [Step 1: Clone Repository](#step-1-clone-repository)
   - [Step 2: Environment Setup](#step-2-environment-setup)
   - [Step 3: Download Legal Corpus](#step-3-download-legal-corpus)
   - [Step 4: Split Domains](#step-4-split-domains)
   - [Step 5: Start LangFuse (Observability)](#step-5-start-langfuse-observability)
   - [Step 6: Run Ingestion Pipeline](#step-6-run-ingestion-pipeline)
   - [Step 7: Start the UI](#step-7-start-the-ui)
   - [Step 8: Verify System](#step-8-verify-system)
4. [Architecture Overview](#architecture-overview)
5. [Configuration Reference](#configuration-reference)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Backend processing |
| Node.js | 18+ | Frontend UI |
| Docker | 24+ | LangFuse observability |
| Git | 2.0+ | Version control |

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| Storage | 25GB | 50GB+ |
| CPU | 4 cores | 8+ cores |
| GPU | None | NVIDIA (for embeddings) |

### API Keys Required

- **OpenRouter API Key** - For LLM access (Gemini 2.0 Flash)
  - Get at: https://openrouter.ai/
- **Optional: Google AI API Key** - Direct Gemini access

---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/verridian-legal-ai.git
cd verridian-legal-ai

# 2. Run setup script (creates venv, installs deps, starts services)
./scripts/setup.sh

# 3. Open browser
# - UI: http://localhost:3000
# - LangFuse: http://localhost:3001
```

---

## Detailed Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/verridian-legal-ai.git
cd verridian-legal-ai

# Or if you have an existing clone
git pull origin main
```

### Step 2: Environment Setup

#### Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

Required environment variables:

```env
# LLM API (Required)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Optional: Direct Google AI access
GOOGLE_AI_API_KEY=your-google-ai-key

# LangFuse (Local self-hosted)
LANGFUSE_PUBLIC_KEY=pk-lf-local
LANGFUSE_SECRET_KEY=sk-lf-local
LANGFUSE_HOST=http://localhost:3001

# Database paths
DATA_DIR=./data
CORPUS_DIR=./data/corpus
PROCESSED_DIR=./data/processed

# Model settings
EMBEDDING_MODEL=BAAI/bge-m3
LLM_MODEL=google/gemini-2.0-flash-001
```

### Step 3: Download Legal Corpus

The system requires Australian Family Law court decisions. You have several options:

#### Option A: Use Provided Sample Data (Recommended for Testing)

```bash
# Download sample dataset (100 cases)
python scripts/download_sample_corpus.py

# Output: data/corpus/sample_cases.jsonl
```

#### Option B: Download Full Corpus from AustLII

```bash
# Download full corpus (requires AustLII access)
python scripts/download_austlii_corpus.py \
    --courts FamCA,FamCAFC,HCA \
    --years 2015-2024 \
    --output data/corpus/full_corpus.jsonl

# This may take several hours depending on your connection
```

#### Option C: Use Your Own Data

Place your legal documents in JSONL format:

```json
{"case_id": "FamCA_2020_001", "citation": "[2020] FamCA 1", "text": "Full judgment text...", "date": "2020-01-15", "court": "FamCA"}
{"case_id": "FamCA_2020_002", "citation": "[2020] FamCA 2", "text": "Full judgment text...", "date": "2020-01-20", "court": "FamCA"}
```

Save to: `data/corpus/your_corpus.jsonl`

### Step 4: Split Domains

The corpus needs to be split into legal domains for targeted processing:

```bash
# Run domain splitter
python -m src.ingestion.domain_splitter \
    --input data/corpus/full_corpus.jsonl \
    --output data/processed/ \
    --domains family,criminal,civil,property

# Output structure:
# data/processed/
# ├── family.jsonl          (Family law cases)
# ├── criminal.jsonl        (Criminal cases)
# ├── civil.jsonl           (Civil cases)
# ├── property.jsonl        (Property cases)
# └── extraction_statistics.json
```

#### Domain Classification

The splitter uses keyword and citation patterns:

| Domain | Keywords | Court Patterns |
|--------|----------|----------------|
| Family | custody, divorce, property, children, spouse | FamCA, FamCAFC |
| Criminal | guilty, sentence, offence, prosecution | CCA, DCC |
| Civil | damages, negligence, contract, tort | SC, DC |
| Property | conveyancing, lease, land, title | SC |

### Step 5: Start LangFuse (Observability)

LangFuse provides tracing, scoring, and analytics for the AI system.

```bash
# Navigate to LangFuse directory
cd docker/langfuse

# Start LangFuse services
docker compose up -d

# Check status
docker compose ps

# Expected output:
# NAME              STATUS    PORTS
# langfuse-server   running   0.0.0.0:3001->3000/tcp
# langfuse-db       running   0.0.0.0:5433->5432/tcp
```

#### Initial LangFuse Setup

1. **Open LangFuse UI**: http://localhost:3001
2. **Create Account**: Click "Sign up" and create a local account
3. **Create Project**: Name it "Verridian Legal AI"
4. **Get API Keys**: Go to Settings → API Keys → Create new key pair
5. **Update .env**: Add the keys to your `.env` file:

```env
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
LANGFUSE_HOST=http://localhost:3001
```

### Step 6: Run Ingestion Pipeline

Process the legal corpus into the Global Semantic Workspace (GSW):

```bash
# Return to project root
cd ../..

# Run the full ingestion pipeline
python -m src.ingestion.gsw_pipeline \
    --input data/processed/family.jsonl \
    --output data/processed/gsw_workspace.json \
    --mode full \
    --batch-size 10

# Options:
#   --mode full      : Full extraction + reconciliation
#   --mode extract   : Extraction only
#   --mode resume    : Resume from checkpoint
#   --batch-size N   : Process N cases at a time
```

#### Pipeline Stages

1. **Extraction** (TheOperator): Extract actors, states, verbs, questions
2. **Linking** (LegalSpacetime): Create spatio-temporal links
3. **Reconciliation** (LegalReconciler): Merge entities, answer questions
4. **Persistence** (WorkspaceManager): Save to JSON

Monitor progress:

```bash
# Watch the output
tail -f logs/ingestion.log

# Check statistics
cat data/processed/extraction_statistics.json
```

### Step 7: Start the UI

#### Install UI Dependencies

```bash
cd ui
npm install
```

#### Configure UI Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your API keys
nano .env.local
```

Required UI environment variables:

```env
# API Configuration
OPENROUTER_API_KEY=sk-or-v1-your-key

# GSW Data Path
GSW_DATA_PATH=../data/processed/gsw_workspace.json

# LangFuse (optional, for UI tracing)
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
```

#### Start Development Server

```bash
npm run dev
```

Access the UI at: **http://localhost:3000**

### Step 8: Verify System

#### Run Test Suite

```bash
# Return to project root
cd ..

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_observability.py -v
pytest tests/test_gsw.py -v
pytest tests/test_integration.py -v
```

#### Manual Verification Checklist

- [ ] **LangFuse**: http://localhost:3001 - Can log in, see project
- [ ] **UI**: http://localhost:3000 - Chat interface loads
- [ ] **Test Query**: Ask "What are my property rights after separation?"
- [ ] **Check Traces**: Verify traces appear in LangFuse dashboard
- [ ] **Check Scores**: Verify accuracy scores are recorded

#### Health Check Script

```bash
python scripts/health_check.py

# Expected output:
# ✓ LangFuse server: healthy
# ✓ Database: connected
# ✓ GSW workspace: loaded (1,523 cases)
# ✓ Embeddings model: ready
# ✓ LLM connection: verified
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                         (Next.js @ localhost:3000)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                       │
│                      (Next.js API Routes @ /api/gsw)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   OBSERVABILITY     │  │   GSW RETRIEVAL     │  │   LLM GENERATION    │
│   (LangFuse)        │  │   (Python Backend)  │  │   (OpenRouter)      │
│   localhost:3001    │  │                     │  │   Gemini 2.0 Flash  │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       GLOBAL SEMANTIC WORKSPACE (GSW)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Actors    │  │   States    │  │ VerbPhrases │  │  Questions  │        │
│  │   5,170+    │  │   8,000+    │  │   12,000+   │  │   7,615+    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KNOWLEDGE BASE                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────────┐   │
│  │  Family Law Act     │  │   1,523+ Cases      │  │  Vector Store     │   │
│  │  247 Sections       │  │   JSONL Format      │  │  BGE-M3 Embeddings│   │
│  └─────────────────────┘  └─────────────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Configuration Reference

### Project Structure

```
verridian-legal-ai/
├── data/
│   ├── corpus/                 # Raw legal documents
│   │   └── full_corpus.jsonl
│   ├── processed/              # Processed data
│   │   ├── family.jsonl
│   │   ├── gsw_workspace.json
│   │   └── extraction_statistics.json
│   └── domains/                # Domain-specific data
├── docker/
│   └── langfuse/               # LangFuse Docker setup
│       └── docker-compose.yml
├── docs/
│   ├── SETUP.md                # This file
│   └── API.md                  # API documentation
├── scripts/
│   ├── setup.sh                # Quick setup script
│   ├── download_sample_corpus.py
│   └── health_check.py
├── src/
│   ├── agents/                 # LangGraph agents
│   ├── embeddings/             # Vector store
│   ├── gsw/                    # GSW implementation
│   ├── ingestion/              # Data processing
│   ├── logic/                  # Schemas & rules
│   ├── observability/          # LangFuse integration
│   └── utils/                  # Utilities
├── tests/
│   ├── test_gsw.py
│   ├── test_observability.py
│   └── test_integration.py
├── ui/                         # Next.js frontend
│   ├── src/
│   └── package.json
├── .env.example
├── requirements.txt
└── README.md
```

### Key Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `docker/langfuse/docker-compose.yml` | LangFuse services |
| `ui/.env.local` | UI-specific config |
| `data/processed/ingestion_state.json` | Checkpoint state |

---

## Troubleshooting

### Common Issues

#### LangFuse won't start

```bash
# Check Docker logs
docker compose -f docker/langfuse/docker-compose.yml logs

# Common fix: Remove old volumes and restart
docker compose -f docker/langfuse/docker-compose.yml down -v
docker compose -f docker/langfuse/docker-compose.yml up -d
```

#### Database connection errors

```bash
# Check if PostgreSQL is running
docker compose -f docker/langfuse/docker-compose.yml ps langfuse-db

# Check database logs
docker compose -f docker/langfuse/docker-compose.yml logs langfuse-db
```

#### Embedding model download fails

```bash
# Manual download
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"

# Or use smaller model
export EMBEDDING_MODEL=all-MiniLM-L6-v2
```

#### Out of memory during ingestion

```bash
# Reduce batch size
python -m src.ingestion.gsw_pipeline --batch-size 5

# Or process in chunks
python -m src.ingestion.gsw_pipeline --start-line 0 --end-line 500
```

#### UI build errors

```bash
# Clear cache and reinstall
cd ui
rm -rf node_modules .next
npm install
npm run dev
```

### Getting Help

- **GitHub Issues**: https://github.com/yourusername/verridian-legal-ai/issues
- **Documentation**: See `/docs` folder
- **Logs**: Check `logs/` directory for detailed logs

---

## Next Steps

After completing setup:

1. **Explore the UI**: Try different legal queries
2. **Review Traces**: Check LangFuse for performance insights
3. **Customize**: Add your own legal documents
4. **Evaluate**: Run accuracy benchmarks
5. **Deploy**: See `docs/DEPLOYMENT.md` for production setup

---

*Last updated: November 2024*
*Version: 7.0*
