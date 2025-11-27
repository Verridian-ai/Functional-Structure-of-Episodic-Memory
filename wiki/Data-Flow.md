# Data Flow

This page documents how data moves through the Verridian AI system, from raw legal documents to verified responses.

## High-Level Flow

```mermaid
graph TB
    subgraph "Input"
        D[Legal Documents]
        Q[User Query]
    end

    subgraph "Extraction Layer"
        C[Text Chunker]
        O[Legal Operator]
        R[Reconciler]
    end

    subgraph "Memory Layer"
        GSW[Global Semantic Workspace]
    end

    subgraph "Cognitive Layer"
        TEM[Navigation - TEM]
        AI[Agency - Active Inference]
        VSA[Logic - VSA]
    end

    subgraph "Output"
        RES[Verified Response]
        CIT[Citations]
    end

    D --> C
    C --> O
    O --> R
    R --> GSW
    Q --> GSW
    GSW --> TEM
    TEM --> AI
    AI --> VSA
    VSA --> RES
    VSA --> CIT
```

---

## Phase 1: Document Ingestion

### Text Chunking

**File**: `src/gsw/text_chunker.py`

Documents are split into manageable chunks for processing:

```mermaid
sequenceDiagram
    participant Doc as Document
    participant TC as TextChunker
    participant Chunks as Chunk[]

    Doc->>TC: Raw legal text
    TC->>TC: Split by paragraphs
    TC->>TC: Respect sentence boundaries
    TC->>TC: Apply overlap
    TC->>Chunks: Sized chunks (512-1024 tokens)
```

Configuration:
- **Chunk size**: 512-1024 tokens
- **Overlap**: 50 tokens
- **Boundary detection**: Paragraph and sentence aware

---

## Phase 2: 6-Task Extraction

### Legal Operator Pipeline

**File**: `src/gsw/legal_operator.py`

Each chunk goes through the 6-task extraction pipeline:

```mermaid
graph TB
    Text[Legal Text Chunk] --> T1[1. Actor Identification]
    T1 --> T2[2. Role Assignment]
    T2 --> T3[3. State Identification]
    T3 --> T4[4. Verb Phrase Extraction]
    T4 --> T5[5. Question Generation]
    T5 --> T6[6. Spatio-Temporal Links]
    T6 --> CE[ChunkExtraction]
```

**Output Structure**:
```python
ChunkExtraction:
    - actors: List[Actor]           # Who is involved
    - verb_phrases: List[VerbPhrase] # What happened
    - questions: List[Question]      # What could be asked
    - spatio_temporal_links: List[Link]  # When/where bindings
```

---

## Phase 3: Reconciliation

### Entity Merging

**File**: `src/gsw/legal_reconciler.py`

Multiple chunks may reference the same entity. The Reconciler merges them:

```mermaid
graph LR
    subgraph "Chunk 1"
        A1["John Smith (Applicant)"]
    end

    subgraph "Chunk 2"
        A2["Mr Smith (Husband)"]
    end

    subgraph "Chunk 3"
        A3["the Applicant (Father)"]
    end

    A1 --> M[Entity Matcher]
    A2 --> M
    A3 --> M

    M --> R[Reconciled Actor]

    R --> GSW[Global Workspace]
```

Reconciliation steps:
1. **Alias matching**: "John Smith" = "Mr Smith" = "the Applicant"
2. **Role merging**: Combine roles from all chunks
3. **State timeline**: Order states chronologically
4. **Link integration**: Merge spatio-temporal bindings

---

## Phase 4: Workspace Storage

### Global Semantic Workspace

**File**: `src/gsw/workspace.py`

```mermaid
graph TB
    subgraph "GlobalWorkspace"
        AM[Actor Memory<br/>Dict: id -> Actor]
        VM[Verb Memory<br/>Dict: id -> VerbPhrase]
        QM[Question Memory<br/>Dict: id -> Question]
        LM[Link Memory<br/>Dict: id -> STLink]
        SM[Summaries<br/>Dict: id -> Summary]
    end

    CE[ChunkExtraction] --> AM
    CE --> VM
    CE --> QM
    CE --> LM

    AM --> JSON[JSON Persistence]
    VM --> JSON
    QM --> JSON
    LM --> JSON
```

---

## Phase 5: Query Processing

### Three-Layer Cognitive Engine

When a user query arrives:

```mermaid
sequenceDiagram
    participant U as User
    participant GSW as Workspace
    participant TEM as Navigation
    participant AI as Agency
    participant VSA as Logic

    U->>GSW: Legal query
    GSW->>GSW: Retrieve context
    GSW->>TEM: Context + Query

    Note over TEM: Layer 1: Navigate structure
    TEM->>TEM: Separate content from structure
    TEM->>TEM: Find relevant patterns
    TEM->>AI: Structural embedding

    Note over AI: Layer 2: Gap detection
    AI->>AI: Check completeness
    AI->>AI: Identify missing info
    alt Missing Evidence
        AI->>GSW: Request more context
    end
    AI->>VSA: Claims to verify

    Note over VSA: Layer 3: Verify logic
    VSA->>VSA: Check requirements
    VSA->>VSA: Detect contradictions
    VSA->>U: Verified response
```

---

## Data Format Transformations

### Input to Output

```
Raw Text (String)
    ↓
Chunks (List[String])
    ↓
ChunkExtraction (Pydantic Model)
    ↓
GlobalWorkspace (Pydantic Model)
    ↓
JSON (Storage)
    ↓
TOON (LLM Context)
    ↓
Response (String + Citations)
```

### TOON Compression

TOON format reduces token usage by ~40%:

```python
# JSON format (~100 tokens)
{"actor": {"name": "John Smith", "type": "person", "roles": ["applicant"]}}

# TOON format (~60 tokens)
A:John Smith|T:person|R:applicant
```

---

## API Data Flow

### Chat Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant API as /api/chat
    participant M0 as Mem0
    participant OR as OpenRouter
    participant GSW as Workspace

    C->>API: POST {messages, apiKey}
    API->>M0: Search relevant memories
    M0->>API: Memory context
    API->>GSW: Get workspace context
    GSW->>API: TOON context
    API->>OR: Chat completion (stream)
    OR-->>API: SSE chunks
    API-->>C: Streamed response
    API->>M0: Store interaction
```

---

## Performance Metrics

| Stage | Typical Time | Tokens Used |
|-------|-------------|-------------|
| Chunk extraction | 2-3s | ~2000 |
| Reconciliation | 0.5s | - |
| TEM navigation | 0.01s | - |
| Agency inference | 0.01s | - |
| VSA verification | 0.001s | - |
| Total response | 11.83ms avg | ~3500 |

---

## Related Pages

- [Architecture-Overview](Architecture-Overview) - System design
- [Backend-GSW-Module](Backend-GSW-Module) - Extraction details
- [Backend-Ingestion-Module](Backend-Ingestion-Module) - Bulk processing
- [Three-Layer-System](Three-Layer-System) - Cognitive layers
