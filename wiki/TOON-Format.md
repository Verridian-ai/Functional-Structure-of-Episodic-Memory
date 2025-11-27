# TOON Format

Token-Oriented Object Notation (TOON) is a compact serialization format optimized for LLM context efficiency.

## Overview

TOON achieves **~40% fewer tokens** than JSON while maintaining **73.9% parsing accuracy** (vs 60% for JSON). It's the preferred format for all LLM context injection in Verridian AI.

**Specification**: [github.com/toon-format/toon](https://github.com/toon-format/toon)

---

## Format Structure

```
EntityType[count]{header1,header2,header3}
value1,value2,value3
value1,value2,value3
```

### Example: JSON vs TOON

**JSON (127 tokens)**:
```json
{
    "actors": [
        {"id": "a1", "name": "John Smith", "type": "person", "roles": ["Applicant", "Father"]},
        {"id": "a2", "name": "Jane Smith", "type": "person", "roles": ["Respondent", "Mother"]}
    ]
}
```

**TOON (76 tokens - 40% reduction)**:
```
Actors[2]{id,name,type,roles}
a1,John Smith,person,Applicant|Father
a2,Jane Smith,person,Respondent|Mother
```

---

## Verridian AI Implementation

### Core Module

**File**: `src/utils/toon.py`

The implementation provides:

| Class | Purpose |
|-------|---------|
| `ToonEncoder` | Encode Python objects to TOON format |
| `ToonDecoder` | Parse TOON back to Python objects |

### Encoder Methods

```python
from src.utils.toon import ToonEncoder

# Generic encoding
toon = ToonEncoder.encode(
    name="MyEntities",
    headers=["id", "name", "value"],
    data=[["e1", "Entity One", 42], ["e2", "Entity Two", 99]]
)
# Result:
# MyEntities[2]{id,name,value}
# e1,Entity One,42
# e2,Entity Two,99

# Domain-specific encoders
toon_actors = ToonEncoder.encode_actors(actors_list)
toon_verbs = ToonEncoder.encode_verb_phrases(verb_list)
toon_questions = ToonEncoder.encode_questions(questions_list)
toon_links = ToonEncoder.encode_links(links_list)

# Full workspace encoding
toon_workspace = ToonEncoder.encode_workspace(workspace)

# Context summary (condensed)
toon_summary = ToonEncoder.encode_context_summary(workspace)
```

### Decoder Methods

```python
from src.utils.toon import ToonDecoder

# Parse TOON back to structured data
parsed = ToonDecoder.decode(toon_string)
# Returns: {"name": "MyEntities", "headers": [...], "data": [...]}

# Parse to domain objects
actors = ToonDecoder.decode_actors(toon_actors_string)
workspace = ToonDecoder.decode_workspace(toon_workspace_string)
```

---

## Usage Patterns

### 1. LLM Context Injection

```python
from src.utils.toon import ToonEncoder

def build_prompt(workspace, query):
    context = ToonEncoder.encode_context_summary(workspace)
    return f"""
Given the following case context:

{context}

Answer the question: {query}
"""
```

### 2. Entity Reconciliation

```python
from src.utils.toon import ToonEncoder

def reconcile_entities(existing_actors, new_actors):
    existing_toon = ToonEncoder.encode_actors(existing_actors)
    new_toon = ToonEncoder.encode_actors(new_actors)

    prompt = f"""
Existing entities:
{existing_toon}

New entities to reconcile:
{new_toon}

Identify matches and conflicts.
"""
    return prompt
```

### 3. API Response Format

```python
# In API routes
def get_workspace(format: str = "json"):
    workspace = load_workspace()

    if format == "toon":
        return ToonEncoder.encode_workspace(workspace)
    return workspace.model_dump_json()
```

---

## Format Specifications

### Headers

Headers define column names:
```
EntityType[count]{col1,col2,col3}
```

### Values

- **Strings**: Unquoted unless containing special characters
- **Lists**: Pipe-separated (`Applicant|Father|Husband`)
- **Nested objects**: Use reference IDs
- **Null values**: Empty string
- **Special characters**: Escape with backslash

### Multi-Block Documents

```
Actors[3]{id,name,type}
a1,John Smith,person
a2,Jane Smith,person
a3,Family Court,organization

VerbPhrases[2]{id,verb,agent_id,patient_ids}
v1,filed,a1,a3
v2,responded,a2,a3

Questions[1]{id,text,type,answerable}
q1,When did the parties separate?,when,false
```

---

## Integration Points

### GSW Layer

| File | TOON Usage |
|------|------------|
| `src/gsw/operator_prompts.py` | Ontology context encoding |
| `src/gsw/legal_reconciler.py` | Entity comparison prompts |
| `src/gsw/question_answerer.py` | Workspace context |
| `src/gsw/entity_matcher.py` | Match candidate encoding |

### TEM Layer

| File | TOON Usage |
|------|------------|
| `src/tem/structures.py` | Case graph serialization |
| `src/tem/legal_graph_builder.py` | Navigation context |

### Agency Layer

| File | TOON Usage |
|------|------------|
| `src/agency/agent.py` | Gap representation encoding |
| `src/agency/generative_model.py` | Matrix context |

### Frontend

| File | TOON Usage |
|------|------------|
| `ui/src/app/api/gsw/route.ts` | API response format |
| `ui/src/lib/api/tools.ts` | Context retrieval |

---

## Performance Benchmarks

### Token Reduction by Entity Type

| Entity Type | JSON Tokens | TOON Tokens | Reduction |
|-------------|-------------|-------------|-----------|
| Actor | 45 | 27 | 40% |
| VerbPhrase | 38 | 22 | 42% |
| State | 32 | 18 | 44% |
| Question | 52 | 31 | 40% |
| Link | 28 | 17 | 39% |

### Accuracy Comparison

| Format | Parsing Accuracy | Error Rate |
|--------|------------------|------------|
| JSON | 60% | 15% |
| TOON | 73.9% | 8% |

*Source: [TOON Benchmarks](https://github.com/toon-format/toon)*

### Cost Impact

For a typical case extraction (2,500 tokens JSON):
- **JSON cost**: ~$0.05 per extraction
- **TOON cost**: ~$0.03 per extraction
- **Annual savings** (10K extractions): ~$200

---

## Best Practices

### Do

1. Use TOON for all LLM context injection
2. Include the `use_toon=True` flag in reconciliation calls
3. Reference entities by ID in nested structures
4. Use pipe separators for lists

### Don't

1. Use TOON for human-readable output (use JSON)
2. Embed long text in TOON cells (truncate or summarize)
3. Nest TOON blocks (use references instead)

---

## Troubleshooting

### Parsing Errors

```python
# Enable debug mode
from src.utils.toon import ToonDecoder

result = ToonDecoder.decode(toon_string, strict=False)
if result.get("errors"):
    print(f"Parse warnings: {result['errors']}")
```

### Missing Data

TOON treats empty strings as null. To distinguish:
```
# Null value
a1,John,,person

# Empty string value
a1,John,"",person
```

---

## Related Pages

- [Data-Flow](Data-Flow) - System data flow with TOON transformation
- [Backend-GSW-Module](Backend-GSW-Module) - GSW extraction with TOON
- [API-Reference](API-Reference) - API format parameters
- [Data-Schemas](Data-Schemas) - Schema definitions
