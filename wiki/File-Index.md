# File Index

Complete file listing for the Verridian AI codebase.

## Project Structure

```
.
├── src/                        # Python backend
├── ui/                         # Next.js frontend
├── data/                       # Data files
├── wiki/                       # Documentation
├── docs/                       # Additional docs
└── scripts/                    # Utility scripts
```

---

## Backend Source (`src/`)

### GSW Module (`src/gsw/`)

Actor-centric memory extraction.

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Module initialization | ~10 |
| `legal_operator.py` | Main LegalOperator class | ~350 |
| `workspace.py` | WorkspaceManager persistence | ~420 |
| `operator_prompts.py` | LLM prompts for extraction | ~200 |
| `extraction_parser.py` | JSON to schema parsing | ~150 |
| `text_chunker.py` | Text splitting | ~100 |
| `cost_tracker.py` | Token usage tracking | ~80 |
| `legal_reconciler.py` | Entity reconciliation | ~200 |
| `legal_summary.py` | Summary generation | ~150 |
| `legal_spacetime.py` | Spatio-temporal processing | ~120 |
| `entity_matcher.py` | Entity matching logic | ~180 |
| `vector_reconciler.py` | Vector-based reconciliation | ~150 |
| `reconciler_prompts.py` | Reconciliation prompts | ~100 |
| `question_answerer.py` | Question answering | ~120 |

### TEM Module (`src/tem/`)

Navigation layer (Tolman-Eichenbaum Machine).

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Module initialization | ~10 |
| `model.py` | TolmanEichenbaumMachine class | ~220 |
| `action_space.py` | Legal action definitions | ~50 |
| `factorizer.py` | Structural factorization | ~150 |
| `train.py` | Training utilities | ~180 |
| `spiking.py` | Spiking neural network variant | ~200 |
| `structures.py` | Data structures | ~80 |
| `legal_graph_builder.py` | Graph construction | ~150 |

### VSA Module (`src/vsa/`)

Logic layer (Vector Symbolic Architecture).

| File | Purpose | Lines |
|------|---------|-------|
| `legal_vsa.py` | Main LegalVSA class | ~320 |
| `ontology.py` | Legal ontology and rules | ~150 |
| `encoder.py` | Hypervector encoding | ~100 |
| `contradiction.py` | Contradiction detection | ~120 |
| `analogy.py` | Analogy reasoning | ~100 |

### Agency Module (`src/agency/`)

Active inference for gap detection.

| File | Purpose | Lines |
|------|---------|-------|
| `agent.py` | LegalResearchAgent class | ~360 |
| `pomdp.py` | POMDP definitions | ~80 |
| `generative_model.py` | A, B, C, D matrices | ~150 |

### Logic Module (`src/logic/`)

Schema and rules.

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Module initialization | ~10 |
| `gsw_schema.py` | Pydantic schema definitions | ~430 |
| `schema.py` | Additional schemas | ~200 |
| `rules_engine.py` | Logic rules engine | ~180 |
| `ontology_seed.py` | Seed ontology values | ~100 |
| `authority.py` | Legal authority handling | ~120 |
| `reconciler_prompt.py` | Reconciliation prompts | ~80 |

### Agents Module (`src/agents/`)

LangChain tools and agents.

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Module initialization | ~10 |
| `gsw_tools.py` | GSW tool registry | ~440 |
| `family_law_knowledge.py` | Family law agent | ~300 |

### Ingestion Module (`src/ingestion/`)

Document processing and classification.

| File | Purpose | Lines |
|------|---------|-------|
| `__init__.py` | Module initialization | ~10 |
| `legal_operator.py` | TheOperator class | ~80 |
| `gsw_operator.py` | GSW integration | ~150 |
| `domain_splitter.py` | Domain classification | ~200 |
| `filter_family_law.py` | Family law filter | ~100 |
| `court_code_classifier.py` | Court identification | ~150 |
| `corpus_domain_extractor.py` | Bulk extraction | ~180 |
| `corpus_label_splitter.py` | Label organization | ~120 |
| `classification_config.py` | Classification settings | ~50 |
| `prompts.py` | LLM prompts | ~100 |
| `reconciler.py` | Entity reconciliation | ~200 |

### Other Backend (`src/`)

| Directory | Purpose |
|-----------|---------|
| `analysis/` | Report generation |
| `embeddings/` | Vector store operations |
| `graph/` | Graph construction (SPCNet) |
| `integration/` | System integration |
| `observability/` | LangFuse tracing |
| `retrieval/` | Document retrieval |
| `utils/` | Utility functions |
| `aiml/` | ML utilities |

---

## Frontend Source (`ui/src/`)

### App Router (`ui/src/app/`)

| File | Purpose |
|------|---------|
| `layout.tsx` | Root layout |
| `page.tsx` | Home page (chat) |
| `visualize/page.tsx` | 3D visualization |

### API Routes (`ui/src/app/api/`)

| Route | File | Purpose |
|-------|------|---------|
| `/api/chat` | `chat/route.ts` | Chat completions |
| `/api/gsw` | `gsw/route.ts` | GSW extraction |
| `/api/graph` | `graph/route.ts` | Graph data |
| `/api/memory/add` | `memory/add/route.ts` | Mem0 memory |
| `/api/execute` | `execute/route.ts` | Code execution |
| `/api/pdf/generate` | `pdf/generate/route.ts` | PDF generation |
| `/api/docx/generate` | `docx/generate/route.ts` | DOCX generation |

### Components (`ui/src/components/`)

| Directory | Files |
|-----------|-------|
| `chat/` | ChatPanel, ChatMessage, ChatInput |
| `ui/` | SynapseLoader, VerridianBrainUltimate |
| `layout/` | MainLayout |
| `visualization/` | LegalGraph3D |
| `admin/` | AdminPanel |
| `voice/` | VoicePanel |
| `tools/` | DocumentTools, CodeInterpreter |
| `canvas/` | CanvasPanel |

### Libraries (`ui/src/lib/`)

| Directory | Purpose |
|-----------|---------|
| `api/` | API clients (gemini.ts, tools.ts) |
| `store/` | Zustand state management |
| `tem/` | TEM TypeScript types |
| `vsa/` | VSA TypeScript implementation |
| `active_inference/` | Agency TypeScript |

### Other Frontend

| File/Directory | Purpose |
|----------------|---------|
| `hooks/useSound.ts` | Sound effects hook |
| `types/index.ts` | TypeScript type definitions |
| `lib/validation.ts` | Input validation |

---

## Root Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment template |
| `gsw_pipeline.py` | Main backend entry |
| `run_full_system.py` | Full system demo |
| `run_vsa_demo.py` | VSA demo script |
| `run_micro_tem.py` | TEM demo script |
| `run_agent_demo.py` | Agency demo script |
| `run_benchmarks.py` | Benchmark runner |

---

## Data Files

```
data/
├── workspaces/              # GSW workspace JSON files
├── benchmarks/              # Test data and benchmarks
├── corpus/                  # Legal document corpus
└── models/                  # Trained model weights
```

---

## Wiki Files

```
wiki/
├── Home.md                  # Wiki home page
├── _Sidebar.md              # Navigation sidebar
├── Architecture-Overview.md
├── Three-Layer-System.md
├── GSW-Global-Semantic-Workspace.md
├── Data-Flow.md
├── Backend-GSW-Module.md
├── Backend-TEM-Module.md
├── Backend-VSA-Module.md
├── Backend-Agency-Module.md
├── Backend-Ingestion-Module.md
├── Backend-Agents-Module.md
├── Frontend-Overview.md
├── Frontend-API-Routes.md
├── Frontend-Components.md
├── Quick-Start.md
├── Development-Guide.md
├── Deployment-Guide.md
├── Contributing.md
├── API-Reference.md
├── Data-Schemas.md
├── Glossary.md
└── File-Index.md
```

---

## Line Count Summary

| Module | Files | Lines (approx) |
|--------|-------|----------------|
| GSW | 14 | ~2,500 |
| TEM | 8 | ~1,000 |
| VSA | 5 | ~800 |
| Agency | 3 | ~600 |
| Logic | 7 | ~1,100 |
| Agents | 3 | ~750 |
| Ingestion | 11 | ~1,400 |
| Frontend | ~30 | ~4,000 |
| **Total** | **~80** | **~12,000** |

---

## Related Pages

- [Architecture-Overview](Architecture-Overview) - System design
- [Development-Guide](Development-Guide) - Setup instructions
- [Data-Schemas](Data-Schemas) - Schema definitions
