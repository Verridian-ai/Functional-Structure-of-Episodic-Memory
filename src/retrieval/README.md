# GSW-Aware Retrieval System

## Quick Start

```python
from src.retrieval.hybrid_retriever import HybridRetriever

# Initialize retriever
retriever = HybridRetriever(
    workspace_dir="data/workspaces",
    data_dir="data"
)

# Simple search
results = retriever.retrieve("custody arrangement", top_k=5)

# With context
context = retriever.retrieve_with_context("property settlement", depth=2)

# Specialized searches
applicants = retriever.search_by_role("applicant")
separated = retriever.search_by_state("RelationshipStatus", "Separated")
```

## Retrieval Modes

### Auto Mode (Default)
Automatically selects GSW or BM25 based on query quality:
```python
results = retriever.retrieve(query, mode="auto")
```

### GSW Mode
Pure actor-centric semantic search:
```python
results = retriever.retrieve(query, mode="gsw")
```

### BM25 Mode
Traditional full-text search:
```python
results = retriever.retrieve(query, mode="bm25")
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   HybridRetriever                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  GSWRetriever    │         │  LegalRetriever  │     │
│  │                  │         │   (BM25)         │     │
│  │ - Concept Extract│         │ - Full-text      │     │
│  │ - Actor Scoring  │         │ - Citation index │     │
│  │ - Graph Expand   │         │ - TF-IDF         │     │
│  └──────────────────┘         └──────────────────┘     │
│          ↓                             ↓                │
│  ┌──────────────────────────────────────────────┐      │
│  │         Automatic Mode Selection             │      │
│  │  (GSW if score > threshold, else BM25)       │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Concept Extraction
Extracts weighted concepts from queries:
- Named entities (weight 2.0)
- Legal terms (weight 1.5)
- Actions (weight 1.5)
- Dates/amounts (weight 1.5)
- General terms (weight 1.0)

### 2. Actor Scoring
Multi-factor relevance scoring:
```
score = name_match × 3.0
      + alias_match × 2.5
      + role_match × 2.0
      + state_match × 1.5
      + type_match × 1.0
```

### 3. Graph Expansion
Expand to related entities via relationships:
```python
context = retriever.retrieve_with_context(
    query="property settlement",
    top_k=3,
    depth=2  # BFS to 2 hops
)

# Returns:
# - primary_matches: Direct hits
# - related_actors: Connected entities
# - temporal_links: Time context
# - spatial_links: Location context
```

### 4. Specialized Searches

**By Role**:
```python
# Find all actors with specific role
actors = retriever.search_by_role("applicant")
```

**By State**:
```python
# Find actors with state condition
actors = retriever.search_by_state("RelationshipStatus", "Separated")
```

## Result Format

### GSW Results
```python
{
    'id': 'actor_123',
    'type': 'actor',
    'name': 'John Smith',
    'actor_type': 'person',
    'roles': ['Applicant', 'Father'],
    'states': [
        {'name': 'RelationshipStatus', 'value': 'Separated'}
    ],
    'score': 5.5,
    'domain': 'family',
    'source': 'gsw'
}
```

### BM25 Results
```python
{
    'id': '[2020] FamCA 123',
    'type': 'case',
    'title': 'Smith v Jones',
    'text_preview': '...',
    'score': 3.2,
    'source': 'bm25'
}
```

## Performance

- **Speed**: <0.5ms per query (in-memory)
- **Scalability**: Linear with workspace size
- **Result quality**: High relevance scores (>2.0) for good matches

## Configuration

```python
retriever = HybridRetriever(
    workspace_dir="data/workspaces",
    data_dir="data",
    gsw_score_threshold=2.0,  # Minimum score for GSW
    blend_results=False        # Blend GSW + BM25?
)
```

## Testing

Run the test suite:
```bash
python tests/test_gsw_retrieval.py
```

Tests cover:
1. Concept extraction
2. Actor retrieval
3. Graph context expansion
4. Hybrid mode selection
5. Performance benchmarks
6. Role/state search

## Files

- `gsw_retriever.py` - GSW-aware retriever (650 lines)
- `hybrid_retriever.py` - Hybrid wrapper (380 lines)
- `retriever.py` - Original BM25 retriever
- `../tests/test_gsw_retrieval.py` - Test suite (400 lines)

## See Also

- `docs/GSW_RETRIEVAL_RESULTS.md` - Full implementation results
- `src/logic/gsw_schema.py` - GSW data models
- `src/gsw/workspace.py` - Workspace management
