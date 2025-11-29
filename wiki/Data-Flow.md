# Data Flow

This page documents how data moves through the Verridian AI system, from raw legal documents to verified responses.

---

## High-Level Overview

```mermaid
flowchart TB
    subgraph Input["Phase 0: Input"]
        DOCS[Legal Documents]
    end

    subgraph Ingestion["Phase 1: Ingestion"]
        CHUNK[Text Chunker]
        OPERATOR[Legal Operator<br/>6 Tasks]
        RECONCILE[Reconciler]
    end

    subgraph Memory["Phase 2: Memory Storage"]
        subgraph GSW["Global Semantic Workspace"]
            ACTORS[(Actors<br/>5,170)]
            VERBS[(Verbs)]
            QUESTIONS[(Questions<br/>7,615)]
            LINKS[(Links<br/>646)]
        end
    end

    subgraph Query["Phase 3: Query Processing"]
        TEM[Layer 1: TEM<br/>Navigate]
        AGENCY[Layer 2: Agency<br/>Gap Check]
        VSA[Layer 3: VSA<br/>Verify]
    end

    subgraph Output["Phase 4: Output"]
        RESPONSE[Verified Response]
    end

    DOCS --> CHUNK
    CHUNK --> OPERATOR
    OPERATOR --> RECONCILE
    RECONCILE --> ACTORS
    RECONCILE --> VERBS
    RECONCILE --> QUESTIONS
    RECONCILE --> LINKS

    GSW --> TEM
    TEM --> AGENCY
    AGENCY --> VSA
    VSA --> RESPONSE
```

---

## Phase 1: Document Ingestion

### Step 1.1: Text Chunking

**File**: `src/gsw/text_chunker.py`

Documents are split into manageable chunks for processing:

```mermaid
flowchart TB
    subgraph Input["Input"]
        RAW[Raw Legal Document<br/>100+ pages]
    end

    subgraph Chunker["Text Chunker"]
        SPLIT[Split by Paragraph]
        RESPECT[Respect Sentences]
        OVERLAP[Apply Overlap]
    end

    subgraph Output["Output"]
        C1[Chunk 1<br/>512-1024 tokens]
        C2[Chunk 2<br/>512-1024 tokens]
        C3[Chunk 3<br/>512-1024 tokens]
        CN[Chunk N<br/>...]
    end

    RAW --> SPLIT
    SPLIT --> RESPECT
    RESPECT --> OVERLAP
    OVERLAP --> C1
    OVERLAP --> C2
    OVERLAP --> C3
    OVERLAP --> CN

    C1 -.->|50 token overlap| C2
    C2 -.->|50 token overlap| C3
```

**Configuration**:
| Parameter | Value | Purpose |
|-----------|-------|---------|
| Chunk size | 512-1024 tokens | Optimal for LLM context |
| Overlap | 50 tokens | Preserve cross-boundary context |
| Boundary | Paragraph/sentence aware | Clean splits |

---

### Step 1.2: 6-Task Extraction Pipeline

**File**: `src/gsw/legal_operator.py`

Each chunk goes through the Legal Operator's 6-task extraction:

```mermaid
flowchart TB
    INPUT[Text Chunk] --> T1

    subgraph Pipeline["6-Task Extraction Pipeline"]
        T1[Task 1: Actor Identification<br/>Extract entities]
        T2[Task 2: Role Assignment<br/>Assign legal roles]
        T3[Task 3: State Identification<br/>Extract conditions]
        T4[Task 4: Verb Phrase Extraction<br/>Extract actions]
        T5[Task 5: Question Generation<br/>Generate predictive questions]
        T6[Task 6: Spatio-Temporal Links<br/>Link entities by context]

        T1 --> T2
        T2 --> T3
        T3 --> T4
        T4 --> T5
        T5 --> T6
    end

    T6 --> OUTPUT[ChunkExtraction Object]
```

```mermaid
sequenceDiagram
    participant C as Client
    participant O as LegalOperator
    participant LLM as Gemini API
    participant P as Parser

    C->>O: extract(text_chunk)

    loop 6 Tasks
        O->>LLM: Task prompt + context
        LLM->>O: Structured response
    end

    O->>P: Parse to ChunkExtraction
    P->>O: Validated model
    O->>C: Return ChunkExtraction
```

#### Task Outputs

```mermaid
graph LR
    subgraph "Task 1: Actors"
        A1[John Smith<br/>PERSON]
        A2[Jane Smith<br/>PERSON]
        A3[Matrimonial Home<br/>ASSET]
        A4[March 2020<br/>TEMPORAL]
    end

    subgraph "Task 2: Roles"
        R1[Applicant]
        R2[Respondent]
        R3[Marital Property]
    end

    subgraph "Task 3: States"
        S1[MaritalStatus: married<br/>2005-2020]
        S2[MaritalStatus: separated<br/>2020-present]
    end

    A1 --> R1
    A2 --> R2
    A3 --> R3
    A1 --> S1
    A1 --> S2
```

---

### Step 1.3: Entity Reconciliation

**File**: `src/gsw/legal_reconciler.py`

Multiple chunks may reference the same entity with different names. The Reconciler merges them:

```mermaid
flowchart TB
    subgraph Chunks["Multiple Chunk References"]
        C1["Chunk 1<br/>John Smith<br/>Role: Applicant"]
        C2["Chunk 2<br/>Mr Smith<br/>Role: Father"]
        C3["Chunk 3<br/>the Husband<br/>Role: Applicant"]
    end

    subgraph Matcher["Entity Matcher"]
        M1[Fuzzy Name Match]
        M2[Role Overlap]
        M3[Context Similarity]
        M4[Alias Detection]
    end

    subgraph Result["Merged Actor"]
        MERGED["Actor: John Smith<br/>id: actor_a1b2c3d4<br/>aliases: Mr Smith, the Husband<br/>roles: Applicant, Father, Husband<br/>source_chunks: 1, 2, 3"]
    end

    C1 --> M1
    C2 --> M1
    C3 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> MERGED
```

**Reconciliation Steps**:
1. **Alias Matching**: "John Smith" = "Mr Smith" = "the Applicant"
2. **Role Merging**: Combine roles from all chunks
3. **State Timeline**: Order states chronologically
4. **Link Integration**: Merge spatio-temporal bindings

---

## Phase 2: Memory Storage

### Global Semantic Workspace (GSW)

**File**: `src/gsw/workspace.py`

All extracted and reconciled entities are stored in the GSW:

```mermaid
graph TB
    subgraph GSW["Global Semantic Workspace"]
        subgraph Banks["Memory Banks"]
            ACTORS[(Actor Memory<br/>Dict id→Actor<br/>5,170 actors)]
            VERBS[(Verb Memory<br/>Dict id→Verb)]
            QUESTIONS[(Question Memory<br/>Dict id→Quest<br/>7,615 questions)]
            LINKS[(Link Memory<br/>Dict id→Link<br/>646 ST links)]
            SUMMARIES[(Summaries<br/>Dict id→Text)]
        end
    end

    subgraph Persistence["Persistence Layer"]
        JSON[JSON File<br/>data/workspaces/]
    end

    subgraph Compression["TOON Compression"]
        STANDARD["Standard JSON<br/>~100 tokens"]
        TOON["TOON Format<br/>~60 tokens<br/>40% reduction"]
    end

    GSW --> JSON
    STANDARD --> TOON
    TOON --> LLM[LLM Context]
```

### TOON Format Example

```mermaid
flowchart LR
    subgraph Before["JSON Format ~100 tokens"]
        JSON["{actor: {name: John Smith,<br/>type: person, ...}}"]
    end

    subgraph After["TOON Format ~60 tokens"]
        TOON["A:John Smith|T:person|<br/>R:applicant,husband|<br/>S:separated@2020"]
    end

    JSON -->|40% reduction| TOON
```

---

## Phase 3: Query Processing

### Three-Layer Cognitive Engine

When a user query arrives, it flows through the three cognitive layers:

```mermaid
flowchart TB
    QUERY[User Query] --> CONTEXT

    subgraph Context["Context Retrieval"]
        CONTEXT[GSW Workspace<br/>→ TOON Format]
    end

    CONTEXT --> L1

    subgraph Layer1["Layer 1: Navigation - TEM"]
        L1[MEC Grid Cells]
        L2[HPC Memory Binding]
        L3[LEC Sensory Content]
        L1 --> L2
        L3 --> L2
    end

    L2 --> STRUCT[Structural Embedding]
    STRUCT --> AG1

    subgraph Layer2["Layer 2: Agency - Active Inference"]
        AG1[VFE Perception<br/>What do I know?]
        AG2[EFE Action<br/>What's missing?]
        AG3[Decision<br/>What to do?]
        AG1 --> AG3
        AG2 --> AG3
    end

    AG3 --> CLAIMS[Claims for Verification]
    CLAIMS --> V1

    subgraph Layer3["Layer 3: Logic - VSA"]
        V1[BINDING<br/>A ⊗ B]
        V2[BUNDLING<br/>Σ V]
        V3[PERMUTE<br/>ρ V]
    end

    V1 --> VERIFY
    V2 --> VERIFY
    V3 --> VERIFY
    VERIFY[Verification Check] --> RESPONSE[Verified Response<br/>Confidence: 0.95]
```

### Layer Details

```mermaid
graph TB
    subgraph TEM["Layer 1: TEM - Navigation"]
        TEM1[Find structural patterns]
        TEM2[Navigate to similar cases]
        TEM3[Extract structural embedding]
    end

    subgraph Agency["Layer 2: Agency - Gap Detection"]
        AG1[CHECK: Marriage evidence?]
        AG2[CHECK: Separation evidence?]
        AG3[CHECK: Property to divide?]
        AG4[CHECK: All requirements met?]
    end

    subgraph VSA["Layer 3: VSA - Verification"]
        VSA1[RULE: PROPERTY_SETTLEMENT requires MARRIAGE]
        VSA2[RULE: DIVORCE requires 12_MONTH_SEPARATION]
        VSA3[CONTRADICTION CHECK: No conflicts]
    end

    TEM1 --> TEM2 --> TEM3
    AG1 --> AG2 --> AG3 --> AG4
    VSA1 --> VSA2 --> VSA3
```

### TOON Compression

**TOON (Token-Oriented Object Notation)** reduces token usage by ~40% with 73.9% parsing accuracy.

**File**: `src/utils/toon.py`

```mermaid
graph LR
    JSON[JSON Data] --> TE[ToonEncoder]
    TE --> TOON[TOON Format]
    TOON --> LLM[LLM Context]
    LLM --> TD[ToonDecoder]
    TD --> JSON2[JSON Response]
```

**Example Transformation**:

```python
# JSON format (~127 tokens)
{
    "actors": [
        {"id": "a1", "name": "John Smith", "type": "person", "roles": ["Applicant", "Father"]}
    ]
}

# TOON format (~76 tokens - 40% reduction)
Actors[1]{id,name,type,roles}
a1,John Smith,person,Applicant|Father
```

**Integration Points**:
| Layer | TOON Usage |
|-------|------------|
| GSW | Ontology context, entity reconciliation |
| TEM | Case graph serialization |
| Agency | Gap representation encoding |
| API | Response format option |

See [TOON-Format](TOON-Format) for complete documentation.

---

## API Data Flow

### Chat Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as /api/chat
    participant Mem0 as Mem0 Memory
    participant GSW as GSW Workspace
    participant LLM as OpenRouter/Gemini

    Client->>API: POST /api/chat<br/>{messages, apiKey, userId}

    API->>Mem0: Search relevant memories
    Mem0->>API: Past interactions context

    API->>GSW: Load workspace context
    GSW->>API: TOON-formatted entities

    API->>LLM: System prompt + memory + GSW context

    loop Streaming
        LLM->>API: delta content
        API->>Client: SSE data chunk
    end

    API->>Mem0: Store interaction
    Mem0->>API: Stored confirmation

    API->>Client: [DONE]
```

### Request/Response Structure

```mermaid
flowchart TB
    subgraph Request["1. Client Request"]
        REQ["POST /api/chat<br/>{messages, apiKey, userId}"]
    end

    subgraph Memory["2. Memory Search"]
        MEM["Mem0 Search<br/>→ Past interactions<br/>→ User context"]
    end

    subgraph Context["3. GSW Context"]
        CTX["Load workspace<br/>→ TOON format<br/>→ Actors, questions, links"]
    end

    subgraph LLM["4. LLM Request"]
        LLMR["OpenRouter API<br/>Model: gemini-2.5-flash<br/>Stream: true"]
    end

    subgraph Stream["5. Streaming Response"]
        STR["SSE chunks<br/>delta content"]
    end

    subgraph Store["6. Memory Storage"]
        STO["Store interaction<br/>for future context"]
    end

    REQ --> MEM
    MEM --> CTX
    CTX --> LLMR
    LLMR --> STR
    STR --> STO
```

---

## Data Format Transformations

### Complete Transformation Pipeline

```mermaid
flowchart TB
    subgraph S1["Stage 1: Raw Text"]
        RAW["String<br/>In the matter of Smith & Smith..."]
    end

    subgraph S2["Stage 2: Chunks"]
        CHUNKS["List[String]<br/>[chunk1, chunk2, ...]"]
    end

    subgraph S3["Stage 3: ChunkExtraction"]
        CE["Pydantic Model<br/>ChunkExtraction(<br/>  actors=[...],<br/>  verb_phrases=[...],<br/>  questions=[...]<br/>)"]
    end

    subgraph S4["Stage 4: GlobalWorkspace"]
        GW["Pydantic Model<br/>GlobalWorkspace(<br/>  actors={id: Actor},<br/>  questions={id: Q}<br/>)"]
    end

    subgraph S5["Stage 5: JSON"]
        JSON["Storage Format<br/>{metadata, actors, questions}"]
    end

    subgraph S6["Stage 6: TOON"]
        TOON["LLM Context<br/>A:John|T:person|R:applicant<br/>40% token reduction"]
    end

    subgraph S7["Stage 7: Response"]
        RESP["String + Citations<br/>{response, citations,<br/>confidence, verified}"]
    end

    RAW --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
```

### Stage Details

```mermaid
graph LR
    subgraph Extraction["Extraction Phase"]
        E1[Raw Text] --> E2[Chunks]
        E2 --> E3[ChunkExtraction]
    end

    subgraph Storage["Storage Phase"]
        S1[GlobalWorkspace] --> S2[JSON File]
    end

    subgraph Query["Query Phase"]
        Q1[TOON Context] --> Q2[LLM Processing]
        Q2 --> Q3[Verified Response]
    end

    E3 --> S1
    S2 --> Q1
```

---

## Performance Metrics

### Processing Time by Stage

```mermaid
graph LR
    subgraph Extraction["Extraction ~3s"]
        EX[Chunk extraction<br/>2-3s per chunk]
    end

    subgraph Local["Local Processing ~0.5s"]
        LP[Reconciliation<br/>0.5s]
    end

    subgraph Inference["Neural Inference ~0.02s"]
        TEM[TEM: 0.01s]
        AG[Agency: 0.01s]
        VSA[VSA: 0.001s]
    end

    EX --> LP --> TEM --> AG --> VSA
```

| Stage | Typical Time | Tokens Used | Notes |
|-------|-------------|-------------|-------|
| Chunk extraction | 2-3s | ~2,000 | LLM call per chunk |
| Reconciliation | 0.5s | - | Local entity matching |
| TEM navigation | 0.01s | - | PyTorch inference |
| Agency inference | 0.01s | - | NumPy computation |
| VSA verification | 0.001s | - | Vector operations |
| **Total response** | **11.83ms avg** | **~3,500** | End-to-end |

### Performance Comparison

```mermaid
graph LR
    subgraph Verridian["Verridian AI"]
        V1[Response: 11.83ms]
        V2[Tokens: ~3,500]
    end

    subgraph Traditional["Traditional RAG"]
        T1[Response: ~500ms]
        T2[Tokens: ~8,000]
    end

    V1 -.-|42x faster| T1
    V2 -.-|56% fewer tokens| T2
```

---

## Code Examples

### Extraction Pipeline

```python
from src.gsw.legal_operator import LegalOperator
from src.gsw.workspace import WorkspaceManager
from pathlib import Path

# Initialize operator
operator = LegalOperator()

# Extract from legal text
text = """
In the matter of Smith & Smith [2023] FamCA 123,
the Applicant (John Smith) seeks property settlement
following separation from the Respondent (Jane Smith).
"""

extraction = operator.extract(
    text=text,
    situation="Family law property settlement"
)

# Store in workspace
manager = WorkspaceManager.load(Path("data/workspace.json"))
manager.add_extraction(extraction)
manager.save()

# Query workspace
actors = manager.query_actors_by_role("Applicant")
print(f"Found {len(actors)} applicants")
```

### Query Processing

```python
from src.tem.model import TolmanEichenbaumMachine
from src.agency.agent import LegalResearchAgent
from src.vsa.legal_vsa import get_vsa_service

# Load context from GSW
context = manager.get_context_toon(max_actors=50)

# Process through TEM (navigation)
tem = TolmanEichenbaumMachine(input_dim=768, hidden_dim=256, action_dim=10)
structural_embedding = tem.encode(context)

# Check for gaps (agency)
agent = LegalResearchAgent()
gaps = agent.check_completeness(query, context)

# Verify logic (VSA)
vsa = get_vsa_service()
result = vsa.verify_no_hallucination(["PROPERTY_SETTLEMENT", "MARRIAGE"])

if result["valid"]:
    print("Response verified - no hallucinations")
```

---

## Related Pages

- [Architecture-Overview](Architecture-Overview) - System design
- [Backend-GSW-Module](Backend-GSW-Module) - Extraction details
- [Backend-TEM-Module](Backend-TEM-Module) - Navigation layer
- [Backend-Agency-Module](Backend-Agency-Module) - Gap detection
- [Backend-VSA-Module](Backend-VSA-Module) - Logic verification
- [Backend-Ingestion-Module](Backend-Ingestion-Module) - Bulk processing
- [Three-Layer-System](Three-Layer-System) - Cognitive layers
- [Data-Schemas](Data-Schemas) - Schema definitions
- [TOON-Format](TOON-Format) - Token compression format
