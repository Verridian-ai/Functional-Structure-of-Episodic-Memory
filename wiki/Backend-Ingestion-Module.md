# Backend: Ingestion Module

The **Ingestion Module** handles bulk document processing, domain classification, and corpus management.

## Overview

**Location**: `src/ingestion/`

```mermaid
graph TB
    subgraph "Ingestion Module"
        LO[legal_operator.py<br/>TheOperator class]
        GO[gsw_operator.py<br/>GSW integration]
        DS[domain_splitter.py<br/>Domain classification]
        FL[filter_family_law.py<br/>Domain filtering]
        CC[court_code_classifier.py<br/>Court identification]
        CE[corpus_domain_extractor.py<br/>Bulk extraction]
        CL[corpus_label_splitter.py<br/>Label organization]
    end

    Corpus[Legal Corpus] --> DS
    DS --> FL
    FL --> LO
    LO --> GSW[Global Workspace]
```

---

## Ingestion Pipeline

```mermaid
flowchart LR
    subgraph Input
        RAW[Raw Documents]
        JSONL[Corpus JSONL]
    end

    subgraph Classification
        DC[Domain Classifier]
        CC[Court Classifier]
        FF[Family Filter]
    end

    subgraph Extraction
        OP[TheOperator]
        REC[Reconciler]
    end

    subgraph Storage
        GSW[Global Workspace]
        JSON[JSON Files]
    end

    RAW --> DC
    JSONL --> DC
    DC --> CC
    CC --> FF
    FF --> OP
    OP --> REC
    REC --> GSW
    GSW --> JSON
```

---

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `legal_operator.py` | Core extraction using Gemini | ~80 |
| `gsw_operator.py` | GSW-specific operator | ~150 |
| `domain_splitter.py` | Split corpus by legal domain | ~200 |
| `filter_family_law.py` | Filter Family Law documents | ~100 |
| `court_code_classifier.py` | Identify court/jurisdiction | ~150 |
| `corpus_domain_extractor.py` | Batch domain extraction | ~180 |
| `corpus_label_splitter.py` | Organize by labels | ~120 |
| `classification_config.py` | Classification settings | ~50 |
| `prompts.py` | LLM prompts for classification | ~100 |
| `reconciler.py` | Entity reconciliation | ~200 |

---

## TheOperator Class

**File**: `src/ingestion/legal_operator.py`

The Operator is the "Episodic Legal Observer" that extracts structured data from legal text.

```mermaid
sequenceDiagram
    participant C as Client
    participant O as TheOperator
    participant G as Gemini API
    participant S as Schema Parser

    C->>O: extract_timeline(text)
    O->>G: Send prompt + text
    G->>O: JSON response
    O->>S: Parse to LegalCase
    S->>O: Validated LegalCase
    O->>C: Return LegalCase
```

### Usage Example

```python
from src.ingestion.legal_operator import TheOperator

# Initialize operator
operator = TheOperator(api_key="your_google_api_key")

# Extract timeline from text
case = await operator.extract_timeline(legal_text)

if case:
    print(f"Title: {case.title}")
    print(f"Persons: {[p.name for p in case.persons]}")
    print(f"Timeline: {len(case.timeline)} events")
```

### Extraction Output

```python
LegalCase:
    case_id: str
    title: str
    persons: List[Person]      # Parties, judges, witnesses
    objects: List[Object]      # Assets, properties
    timeline: List[Event]      # Chronological events
    states: List[State]        # Conditions over time
    outcomes: List[Outcome]    # Case results
```

---

## Domain Classification

### Classification Flow

```mermaid
flowchart TD
    DOC[Document Text] --> KW[Keyword Analysis]
    DOC --> CT[Citation Check]
    DOC --> LLM[LLM Classification]

    KW --> SCORE[Score Aggregation]
    CT --> SCORE
    LLM --> SCORE

    SCORE --> DOMAIN{Domain Decision}

    DOMAIN -->|family| FAM[Family Law]
    DOMAIN -->|criminal| CRIM[Criminal Law]
    DOMAIN -->|commercial| COMM[Commercial Law]
    DOMAIN -->|property| PROP[Property Law]
    DOMAIN -->|employment| EMP[Employment Law]
```

### Domain Splitter

**File**: `src/ingestion/domain_splitter.py`

```python
from src.ingestion.domain_splitter import DomainSplitter

splitter = DomainSplitter()
domain = splitter.classify(document_text)
# Returns: "family", "criminal", "commercial", etc.
```

### Supported Domains

| Domain | Description | Keywords |
|--------|-------------|----------|
| `family` | Family Law | divorce, custody, property settlement |
| `criminal` | Criminal Law | prosecution, sentence, offence |
| `commercial` | Commercial Law | contract, corporation, trade |
| `property` | Property Law | land, title, easement |
| `employment` | Employment Law | dismissal, award, workplace |

---

## Court Code Classifier

**File**: `src/ingestion/court_code_classifier.py`

```mermaid
graph LR
    CIT[Citation String] --> REGEX[Regex Parser]
    REGEX --> CODE{Court Code}

    CODE -->|FamCA| FC[Family Court of Australia]
    CODE -->|FamCAFC| FFC[Family Court Full Court]
    CODE -->|FCWA| WA[Family Court WA]
    CODE -->|HCA| HC[High Court]
    CODE -->|FCA| FED[Federal Court]
```

### Usage

```python
from src.ingestion.court_code_classifier import classify_court

result = classify_court("[2023] FamCA 123")
# Returns: {"court": "Family Court of Australia", "jurisdiction": "Federal"}
```

### Supported Courts

| Code | Court | Jurisdiction |
|------|-------|--------------|
| FamCA | Family Court of Australia | Federal |
| FamCAFC | Family Court Full Court | Federal |
| FCWA | Family Court of Western Australia | State |
| HCA | High Court of Australia | Federal |
| FCA | Federal Court of Australia | Federal |

---

## Corpus Processing

### Bulk Processing Pipeline

```mermaid
flowchart LR
    subgraph Input
        DIR[Input Directory]
        JSONL[corpus.jsonl]
    end

    subgraph Processing
        LOOP[For Each Document]
        CLASS[Classify Domain]
        FILT[Apply Filters]
        EXT[Extract Structure]
    end

    subgraph Output
        BY_DOM[By Domain/]
        BY_LAB[By Label/]
        STATS[Statistics]
    end

    DIR --> LOOP
    JSONL --> LOOP
    LOOP --> CLASS
    CLASS --> FILT
    FILT --> EXT
    EXT --> BY_DOM
    EXT --> BY_LAB
    EXT --> STATS
```

### Bulk Domain Extraction

**File**: `src/ingestion/corpus_domain_extractor.py`

```python
from src.ingestion.corpus_domain_extractor import process_corpus

# Process all documents in directory
results = process_corpus(
    input_dir="data/raw_corpus",
    output_dir="data/classified",
    domain_filter="family"
)

print(f"Processed: {results['total']}")
print(f"Family Law: {results['family']}")
```

### Label Organization

**File**: `src/ingestion/corpus_label_splitter.py`

```python
from src.ingestion.corpus_label_splitter import organize_by_labels

organize_by_labels(
    input_jsonl="data/extractions.jsonl",
    output_dir="data/by_label"
)
# Creates: data/by_label/parenting/, data/by_label/property/, etc.
```

---

## Family Law Filter

**File**: `src/ingestion/filter_family_law.py`

```mermaid
flowchart TD
    DOC[Document] --> CHECK1{Court Code?}

    CHECK1 -->|FamCA/FCWA| PASS[Include]
    CHECK1 -->|Other| CHECK2{Keywords?}

    CHECK2 -->|Family Law Act| PASS
    CHECK2 -->|parenting orders| PASS
    CHECK2 -->|property settlement| PASS
    CHECK2 -->|None| REJECT[Exclude]
```

### Usage

```python
from src.ingestion.filter_family_law import filter_family_law

# Filter JSONL file
filtered = filter_family_law(
    input_path="data/corpus.jsonl",
    output_path="data/family_law_corpus.jsonl"
)

print(f"Family Law documents: {filtered}")
```

### Filter Criteria

- **Court codes**: FamCA, FamCAFC, FCWA
- **Keywords**: "Family Law Act", "parenting orders", "property settlement"
- **Case types**: parenting, property, divorce, maintenance

---

## Reconciliation

**File**: `src/ingestion/reconciler.py`

```mermaid
flowchart LR
    subgraph Extractions
        E1[Extraction 1]
        E2[Extraction 2]
        E3[Extraction 3]
    end

    subgraph Matching
        FM[Fuzzy Name Match]
        AR[Alias Resolution]
        RM[Role Merging]
    end

    subgraph Output
        MA[Merged Actors]
        MS[Merged States]
        MQ[Merged Questions]
    end

    E1 --> FM
    E2 --> FM
    E3 --> FM
    FM --> AR
    AR --> RM
    RM --> MA
    RM --> MS
    RM --> MQ
```

### Usage

```python
from src.ingestion.reconciler import EntityReconciler

reconciler = EntityReconciler()

# Add extractions
reconciler.add_extraction(extraction1)
reconciler.add_extraction(extraction2)

# Get merged entities
merged_actors = reconciler.get_merged_actors()
```

### Reconciliation Rules

| Step | Operation | Description |
|------|-----------|-------------|
| 1 | Name matching | Fuzzy match on actor names |
| 2 | Alias resolution | Map aliases to canonical names |
| 3 | Role merging | Combine roles from multiple sources |
| 4 | Timeline ordering | Sort states chronologically |

---

## Configuration

**File**: `src/ingestion/classification_config.py`

```python
CLASSIFICATION_CONFIG = {
    "model": "gemini-2.0-flash",
    "temperature": 0.1,
    "max_tokens": 2048,
    "domains": ["family", "criminal", "commercial", "property"],
    "confidence_threshold": 0.8
}
```

---

## Full Pipeline Example

```mermaid
sequenceDiagram
    participant C as Client
    participant S as DomainSplitter
    participant O as TheOperator
    participant R as Reconciler
    participant W as WorkspaceManager

    C->>S: classify(text)
    S->>C: "family"

    C->>O: extract_timeline(text)
    O->>C: LegalCase

    C->>R: add_extraction(case)
    R->>R: Match entities
    R->>C: Merged entities

    C->>W: add_actors(actors)
    W->>W: Persist to JSON
    W->>C: Success
```

### Code Example

```python
import asyncio
from pathlib import Path
from src.ingestion.legal_operator import TheOperator
from src.ingestion.domain_splitter import DomainSplitter
from src.gsw.workspace import WorkspaceManager

async def ingest_document(text: str, workspace_path: Path):
    # 1. Classify domain
    splitter = DomainSplitter()
    domain = splitter.classify(text)

    if domain != "family":
        return None

    # 2. Extract structure
    operator = TheOperator()
    case = await operator.extract_timeline(text)

    if not case:
        return None

    # 3. Add to workspace
    manager = WorkspaceManager.load(workspace_path)
    # ... add actors, states, etc.
    manager.save()

    return case

# Run
asyncio.run(ingest_document(text, Path("data/workspace.json")))
```

---

## Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Domain classification | 0.5s | Per document |
| Court code extraction | 0.1s | Regex-based |
| Timeline extraction | 2-3s | LLM call |
| Reconciliation | 0.1s | Per 100 entities |
| Bulk processing | ~1000/hr | With rate limiting |

---

## Related Pages

- [Backend-GSW-Module](Backend-GSW-Module) - Extraction details
- [Data-Flow](Data-Flow) - System data flow
- [Data-Schemas](Data-Schemas) - Schema definitions
- [Development-Guide](Development-Guide) - Setup instructions
