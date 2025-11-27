# Development Guide

Guide for setting up and developing the Verridian AI system.

## Prerequisites

- **Python**: 3.10+
- **Node.js**: 18+
- **Git**: Latest
- **API Keys**:
  - OpenRouter API key ([openrouter.ai](https://openrouter.ai))
  - Optional: Mem0 API key ([mem0.ai](https://mem0.ai))

---

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/Verridian-ai/Functional-Structure-of-Episodic-Memory.git
cd Functional-Structure-of-Episodic-Memory
```

### 2. Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ui
npm install
cd ..
```

### 4. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env`:
```bash
OPENROUTER_API_KEY=sk-or-your-key-here
MEM0_API_KEY=m0-your-key-here  # Optional
GOOGLE_API_KEY=your-google-key  # Optional, for Gemini direct
```

---

## Running the System

### Full System

```bash
# Terminal 1: Backend
python run_full_system.py

# Terminal 2: Frontend
cd ui && npm run dev
```

Access at: `http://localhost:3000`

### Individual Components

```bash
# GSW extraction demo
python run_vsa_demo.py

# TEM navigation demo
python run_micro_tem.py

# Active inference demo
python run_agent_demo.py

# Main pipeline
python gsw_pipeline.py
```

---

## Project Structure

```
.
├── src/                    # Python backend
│   ├── gsw/               # Actor-centric memory
│   ├── tem/               # Navigation (PyTorch)
│   ├── vsa/               # Logic verification
│   ├── agency/            # Active inference
│   ├── agents/            # LangChain tools
│   ├── ingestion/         # Document processing
│   └── logic/             # Schemas and rules
├── ui/                     # Next.js frontend
│   ├── src/app/           # App router
│   ├── src/components/    # React components
│   └── src/lib/           # Libraries
├── data/                   # Data files
│   └── workspaces/        # GSW workspaces
├── wiki/                   # Documentation
└── docs/                   # Additional docs
```

---

## Development Workflow

### Backend Development

```bash
# Run with auto-reload (using watchdog)
pip install watchdog
watchmedo auto-restart --patterns="*.py" --recursive -- python gsw_pipeline.py

# Or use Python's -c for quick tests
python -c "from src.gsw.legal_operator import LegalOperator; print('OK')"
```

### Frontend Development

```bash
cd ui
npm run dev          # Development server
npm run build        # Production build
npm run lint         # Linting
npm run type-check   # TypeScript check
```

### Type Checking

```bash
# Python (mypy)
pip install mypy
mypy src/

# TypeScript
cd ui && npm run type-check
```

---

## Testing

### Run Tests

```bash
# Python tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Frontend tests
cd ui && npm test
```

### Benchmarks

```bash
python run_benchmarks.py
```

---

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Docstrings for public functions

```python
def extract_actors(text: str, context: Optional[str] = None) -> List[Actor]:
    """
    Extract actors from legal text.

    Args:
        text: The legal text to process
        context: Optional background context

    Returns:
        List of extracted Actor objects
    """
    ...
```

### TypeScript

- Use strict mode
- Prefer interfaces over types
- Document exported functions

```typescript
interface Actor {
    id: string;
    name: string;
    roles: string[];
}

/**
 * Find actors by role in the workspace
 * @param role - The role to search for
 * @returns Array of matching actors
 */
export function findActorsByRole(role: string): Actor[] {
    ...
}
```

---

## Common Tasks

### Add a New GSW Tool

1. Define in `src/agents/gsw_tools.py`:
```python
@tool
def my_new_tool(param: str) -> str:
    """Description for LLM."""
    registry = get_registry()
    result = registry.agent.my_method(param)
    return json.dumps(result)
```

2. Add to tool list:
```python
def get_gsw_tools():
    return [
        ...,
        my_new_tool
    ]
```

### Add a New API Route

1. Create `ui/src/app/api/myroute/route.ts`:
```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    const body = await request.json();
    // Process...
    return NextResponse.json({ success: true });
}
```

### Add a New Component

1. Create `ui/src/components/mycomponent/MyComponent.tsx`:
```typescript
interface MyComponentProps {
    title: string;
}

export function MyComponent({ title }: MyComponentProps) {
    return <div>{title}</div>;
}
```

2. Export from index if needed.

---

## Debugging

### Backend Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use breakpoints
import pdb; pdb.set_trace()
```

### Frontend Debugging

```typescript
// Browser console
console.log('Debug:', data);

// React DevTools
// Install browser extension

// Network tab
// Monitor API requests
```

### LangFuse Observability

```python
from src.observability.langfuse_tracer import trace

@trace(name="my_operation")
def my_function():
    ...
```

---

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENROUTER_API_KEY` | Yes | LLM access via OpenRouter |
| `MEM0_API_KEY` | No | Persistent memory |
| `GOOGLE_API_KEY` | No | Direct Gemini access |
| `LANGFUSE_PUBLIC_KEY` | No | Observability |
| `LANGFUSE_SECRET_KEY` | No | Observability |

---

## Troubleshooting

### "Module not found"

```bash
# Ensure you're in the project root
cd Functional-Structure-of-Episodic-Memory

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key is required"

Add key to `.env` or pass via UI settings.

### "CUDA not available"

System works on CPU. For GPU:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### "Port in use"

```bash
cd ui && npm run dev -- -p 3001
```

---

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation

### Commit Messages

```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
```

Example:
```
feat(gsw): add actor state timeline query
fix(api): handle streaming errors
docs(wiki): add Data-Flow page
```

---

## Related Pages

- [Quick-Start](Quick-Start) - Quick setup guide
- [Contributing](Contributing) - Contribution guidelines
- [Deployment-Guide](Deployment-Guide) - Production deployment
- [File-Index](File-Index) - Complete file listing
