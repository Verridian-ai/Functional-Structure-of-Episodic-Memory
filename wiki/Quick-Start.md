# Quick Start Guide

Get Verridian AI running in under 10 minutes.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

---

## Step 1: Clone Repository

```bash
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory
```

## Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Install Frontend Dependencies

```bash
cd ui
npm install
cd ..
```

## Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# OPENROUTER_API_KEY=sk-or-your-key-here
```

**Required Environment Variables:**
```bash
OPENROUTER_API_KEY=sk-or-...  # Required for LLM
MEM0_API_KEY=m0-...           # Optional: persistent memory
```

## Step 5: Run the System

### Option A: Full System (Recommended)

```bash
# Terminal 1: Backend demos
python run_full_system.py

# Terminal 2: Frontend
cd ui && npm run dev
```

### Option B: Individual Components

```bash
# Run GSW extraction demo
python run_vsa_demo.py

# Run TEM navigation demo
python run_micro_tem.py

# Run Active Inference demo
python run_agent_demo.py
```

## Step 6: Access the UI

Open your browser to: **http://localhost:3000**

---

## First Query

Try asking:

> "What are the requirements for property settlement under Australian Family Law?"

Expected response includes:
- Family Law Act section references
- Requirements (marriage, separation)
- Relevant considerations

---

## Project Structure

```
.
├── src/                    # Python backend
│   ├── gsw/               # Actor-centric memory
│   ├── tem/               # Navigation (PyTorch)
│   ├── vsa/               # Logic verification
│   ├── agency/            # Active inference
│   └── agents/            # LangChain tools
├── ui/                     # Next.js frontend
│   ├── src/app/           # App router pages
│   └── src/components/    # React components
├── data/                   # Knowledge base
│   ├── workspaces/        # GSW workspaces
│   └── benchmarks/        # Test data
└── docs/                   # Documentation
```

---

## Common Issues

### "API key is required"
Add `OPENROUTER_API_KEY` to your `.env` file or configure in UI Settings.

### "Module not found"
Run `pip install -r requirements.txt` from project root.

### "Port 3000 in use"
```bash
cd ui && npm run dev -- -p 3001
```

### "CUDA not available"
The system works on CPU. For GPU acceleration, install PyTorch with CUDA support.

---

## Next Steps

1. **Explore the UI** - Try different query types
2. **Read Architecture** - [Architecture Overview](Architecture-Overview)
3. **Understand GSW** - [GSW Module](Backend-GSW-Module)
4. **Run Benchmarks** - `python run_benchmarks.py`

---

## Demo Scripts

| Script | Purpose |
|--------|---------|
| `run_full_system.py` | Complete system integration |
| `run_vsa_demo.py` | VSA anti-hallucination demo |
| `run_micro_tem.py` | TEM navigation demo |
| `run_agent_demo.py` | Active inference demo |
| `gsw_pipeline.py` | Main extraction pipeline |

---

## Support

- [GitHub Issues](https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory/issues)
- [Development Guide](Development-Guide)
- [API Reference](API-Reference)
