# API Reference

Complete API documentation for the Verridian AI system.

## Overview

The system provides two API layers:
1. **Frontend API Routes** (`/api/*`) - Next.js server routes
2. **Backend Python APIs** - Direct Python module access

---

## Frontend API Routes

### POST /api/chat

Stream chat completions from LLM with memory integration.

**Request:**
```typescript
{
    messages: Array<{
        role: 'user' | 'assistant' | 'system';
        content: string;
    }>;
    model?: string;           // Default: 'google/gemini-2.5-flash-preview-05-20'
    temperature?: number;     // Default: 0.7
    maxTokens?: number;       // Default: 4096
    apiKey: string;           // Required: OpenRouter API key
    systemPrompt?: string;    // Optional: System instructions
    tools?: Tool[];           // Optional: Function calling tools
    userId?: string;          // Optional: For Mem0 memory
}
```

**Response:** Server-Sent Events stream
```
data: {"id":"...","choices":[{"delta":{"content":"Hello"}}]}
data: {"id":"...","choices":[{"delta":{"content":" world"}}]}
data: [DONE]
```

**Example:**
```typescript
const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        messages: [{ role: 'user', content: 'What is property settlement?' }],
        apiKey: 'sk-or-...'
    })
});
```

---

### POST /api/gsw

Extract GSW structure from legal text.

**Request:**
```typescript
{
    text: string;             // Legal text to extract
    situation?: string;       // Brief description
    documentId?: string;      // Source document ID
    format?: 'json' | 'toon'; // Response format (default: 'json')
}
```

**Response (JSON format):**
```typescript
{
    success: boolean;
    extraction: {
        chunk_id: string;
        actors: Actor[];
        verb_phrases: VerbPhrase[];
        questions: PredictiveQuestion[];
        spatio_temporal_links: SpatioTemporalLink[];
    };
    error?: string;
}
```

**Response (TOON format):**
```
Actors[2]{id,name,type,roles}
a1,John Smith,person,Applicant|Father
a2,Jane Smith,person,Respondent|Mother

VerbPhrases[1]{id,verb,agent_id,patient_ids}
v1,filed,a1,a2

Questions[1]{id,text,type,answerable}
q1,When did parties separate?,when,false
```

TOON format reduces response size by ~40%. See [TOON-Format](TOON-Format) for details.

---

### POST /api/memory/add

Add memory to Mem0 for persistent context.

**Request:**
```typescript
{
    content: string;          // Memory content
    userId?: string;          // User identifier
    metadata?: {
        role?: string;
        timestamp?: string;
        context?: string;
    };
}
```

**Response:**
```typescript
{
    success: boolean;
    memoryId?: string;
    error?: string;
}
```

---

### POST /api/graph

Get knowledge graph data for visualization.

**Request:**
```typescript
{
    workspacePath?: string;   // Path to workspace JSON
    maxNodes?: number;        // Limit nodes returned
}
```

**Response:**
```typescript
{
    nodes: Array<{
        id: string;
        label: string;
        type: 'actor' | 'asset' | 'event' | 'question';
    }>;
    edges: Array<{
        source: string;
        target: string;
        label?: string;
    }>;
}
```

---

### POST /api/pdf/generate

Generate PDF from content.

**Request:**
```typescript
{
    content: string;          // Markdown content
    title?: string;           // Document title
    template?: string;        // Template name
}
```

**Response:** Binary PDF file

---

### POST /api/docx/generate

Generate DOCX from content.

**Request:**
```typescript
{
    content: string;          // Markdown content
    title?: string;           // Document title
}
```

**Response:** Binary DOCX file

---

### POST /api/execute

Execute code in sandbox.

**Request:**
```typescript
{
    code: string;             // Code to execute
    language?: string;        // Default: 'python'
}
```

**Response:**
```typescript
{
    success: boolean;
    output: string;
    error?: string;
}
```

---

## Python Backend APIs

### LegalOperator

**Module**: `src.gsw.legal_operator`

```python
from src.gsw.legal_operator import LegalOperator

operator = LegalOperator(
    model="google/gemini-2.5-flash",
    api_key=None,            # Uses OPENROUTER_API_KEY env
    use_openrouter=True
)

# Extract from text
extraction = operator.extract(
    text="Legal text here...",
    situation="Family law property settlement",
    document_id="doc_001"
)

# Access results
actors = extraction.actors
questions = extraction.questions
```

---

### WorkspaceManager

**Module**: `src.gsw.workspace`

```python
from src.gsw.workspace import WorkspaceManager
from pathlib import Path

# Load workspace
manager = WorkspaceManager.load(Path("data/workspace.json"))

# Get statistics
stats = manager.get_statistics()

# Query by role
applicants = manager.query_actors_by_role("applicant")

# Query by state
separated = manager.query_actors_by_state("MaritalStatus", "separated")

# Get ontology context
context = manager.get_ontology_context()

# Save workspace
manager.save()
```

---

### TolmanEichenbaumMachine

**Module**: `src.tem.model`

```python
import torch
from src.tem.model import TolmanEichenbaumMachine

# Initialize TEM
tem = TolmanEichenbaumMachine(
    input_dim=768,
    hidden_dim=256,
    action_dim=10
)

# Forward pass
observations = torch.randn(32, 5, 768)
actions = torch.randint(0, 10, (32, 5))
output = tem(observations, actions)

predictions = output['predictions']
```

---

### LegalVSA

**Module**: `src.vsa.legal_vsa`

```python
from src.vsa.legal_vsa import get_vsa_service

vsa = get_vsa_service()

# Add concepts
vsa.add_concept("PROPERTY_SETTLEMENT")
vsa.add_concept("MARRIAGE")

# Verify claims
result = vsa.verify_no_hallucination([
    "PROPERTY_SETTLEMENT",
    "DIVORCE"
])

print(result)
# {'valid': False, 'issues': ["'PROPERTY_SETTLEMENT' REQUIRES 'MARRIAGE'"]}
```

---

### LegalResearchAgent

**Module**: `src.agency.agent`

```python
from src.agency.agent import LegalResearchAgent
from src.agency.pomdp import Observation

agent = LegalResearchAgent()

# Process observation
obs = Observation(value=3)
action = agent.step(obs)

print(f"Selected action: {action.value}")
```

---

### GSW Tools

**Module**: `src.agents.gsw_tools`

```python
from src.agents.gsw_tools import (
    get_gsw_tools,
    set_workspace_path,
    GSWDirectAPI
)
from pathlib import Path

# Set workspace
set_workspace_path(Path("data/workspace.json"))

# Get LangChain tools
tools = get_gsw_tools()

# Or use Direct API
api = GSWDirectAPI(Path("data/workspace.json"))
parties = api.find_parties("Smith")
stats = api.get_stats()
```

---

## Error Handling

### API Error Responses

```typescript
// 400 Bad Request
{ error: 'API key is required' }

// 500 Internal Server Error
{ error: 'Processing failed: ...' }
```

### Python Exceptions

```python
from src.gsw.legal_operator import LegalOperator

try:
    extraction = operator.extract(text)
except json.JSONDecodeError:
    print("Invalid JSON from LLM")
except ValidationError as e:
    print(f"Schema validation failed: {e}")
except Exception as e:
    print(f"Extraction error: {e}")
```

---

## Rate Limiting

### OpenRouter Limits

| Tier | Requests/min | Tokens/min |
|------|-------------|------------|
| Free | 20 | 40,000 |
| Paid | 100+ | 200,000+ |

### Recommended Practices

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=20):
    def decorator(func):
        last_call = [0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < 60 / calls_per_minute:
                time.sleep(60 / calls_per_minute - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Authentication

### OpenRouter

```bash
# Environment variable
OPENROUTER_API_KEY=sk-or-your-key-here

# Or pass directly
apiKey: "sk-or-your-key-here"
```

### Mem0

```bash
MEM0_API_KEY=m0-your-key-here
```

---

## Related Pages

- [Frontend-API-Routes](Frontend-API-Routes) - Detailed API route docs
- [Backend-GSW-Module](Backend-GSW-Module) - GSW extraction
- [Backend-Agents-Module](Backend-Agents-Module) - Agent tools
- [Data-Schemas](Data-Schemas) - Schema definitions
