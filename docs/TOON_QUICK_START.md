# TOON Workspace Persistence - Quick Start Guide

## What is TOON?

TOON (Token-Oriented Object Notation) is a compact data format that reduces workspace file sizes by ~74% compared to JSON, making it ideal for LLM context optimization.

## Quick Examples

### Save workspace as TOON

```python
from src.gsw.workspace import WorkspaceManager
from pathlib import Path

# Create or load a workspace
manager = WorkspaceManager.load(Path("data/workspaces/my_workspace.json"))

# Save as TOON (automatically adds .toon extension)
manager.save_toon()
# Creates: data/workspaces/my_workspace.toon
```

### Load workspace from TOON

```python
# Method 1: Explicit TOON load
manager = WorkspaceManager.load_toon(Path("data/workspaces/my_workspace.toon"))

# Method 2: Auto-detection (recommended)
manager = WorkspaceManager.load(Path("data/workspaces/my_workspace.toon"))
# Automatically detects .toon extension and uses correct loader
```

### Use workspace to_toon() for LLM context

```python
# Get TOON representation for prompt injection
workspace = manager.workspace
toon_context = workspace.to_toon()

# Use in prompt
prompt = f"""
Here is the current workspace state:

{toon_context}

Based on this workspace, answer the following question...
"""
```

### Migrate existing workspaces

```bash
# Convert all JSON workspaces to TOON
python scripts/convert_workspaces_to_toon.py

# Output shows compression statistics for each file
# Prompts to optionally remove original JSON files
```

## File Size Comparison

| Format | Example Size | Use Case |
|--------|--------------|----------|
| JSON | 127 KB | Long-term storage, debugging |
| TOON | 33 KB | LLM context, API responses |

## When to Use Each Format

### Use TOON when:
- Injecting workspace into LLM prompts (saves ~22,700 tokens!)
- Sending workspace over network (74% smaller payload)
- Storing large workspaces with limited space
- Optimizing context window usage

### Use JSON when:
- Debugging (human-readable)
- Integration with JSON-only tools
- Initial development (familiar format)

## TOON Format Structure

```toon
# GSW Workspace: domain_name

Actors[count]{id,name,type,roles,states}
id1,name1,type1,role1|role2,state1=value1|state2=value2
id2,name2,type2,role3,

VerbPhrases[count]{id,verb,agent,patients,temporal,spatial,implicit}
vid1,filed,agent_id,patient1|patient2,,,0

Questions[count]{id,about,question,type,answered,answer}
qid1,actor_id,Question text?,when,1,Answer text

Links[count]{id,entities,type,value}
lid1,entity1|entity2|entity3,temporal,2024-01-01
```

### Key Features:
- **Pipe-delimited lists**: `role1|role2|role3`
- **Key-value pairs**: `state_name=state_value`
- **Boolean flags**: `0` = False, `1` = True
- **Optional values**: Empty strings for null/None

## API Reference

### WorkspaceManager Methods

```python
# Save methods
manager.save()              # Save as JSON (default)
manager.save_toon()         # Save as TOON

# Load methods (class methods)
WorkspaceManager.load(path)         # Auto-detect format by extension
WorkspaceManager.load_json(path)    # Explicit JSON load
WorkspaceManager.load_toon(path)    # Explicit TOON load

# GlobalWorkspace methods
workspace.to_toon()                 # Export as TOON string
workspace.to_toon_summary(max_actors=50)  # Condensed version
```

### ToonEncoder Methods

```python
from src.utils.toon import ToonEncoder

# Encode entire workspace
toon_str = ToonEncoder.encode_workspace(workspace.model_dump())

# Encode specific components
actors_toon = ToonEncoder.encode_actors(actor_list)
verbs_toon = ToonEncoder.encode_verb_phrases(verb_list)
questions_toon = ToonEncoder.encode_questions(question_list)
links_toon = ToonEncoder.encode_links(link_list)
```

### ToonDecoder Methods

```python
from src.utils.toon import ToonDecoder

# Decode entire workspace
workspace_dict = ToonDecoder.decode_workspace(toon_str)

# Decode generic TOON tables
tables = ToonDecoder.decode(toon_str)
# Returns: {"Actors": [...], "VerbPhrases": [...], ...}
```

## Testing

Run the TOON test suite:

```bash
python tests/test_toon_workspace.py
```

Expected output:
```
============================================================
ALL TESTS PASSED!
============================================================

TOON workspace persistence is fully functional:
  ✓ Round-trip conversion preserves all data
  ✓ File size reduction >30%
  ✓ Save/load operations work correctly
  ✓ Format auto-detection works
```

## Troubleshooting

### "ValueError: 'ActorType.PERSON' is not a valid ActorType"

This means the encoder is outputting full enum representations instead of values.
**Fix**: Ensure you're using the latest version of `src/utils/toon.py` with enum value extraction.

### Files not loading

Check file extension:
- `.json` → uses JSON loader
- `.toon` → uses TOON loader
- Other → defaults to JSON loader

### Round-trip conversion fails

Run the test suite to identify the issue:
```bash
python tests/test_toon_workspace.py
```

### Windows console encoding errors

Add to top of script:
```python
import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Performance Tips

1. **Use TOON for LLM context**: Saves ~73% of tokens
2. **Keep JSON for debugging**: Human-readable format useful during development
3. **Migrate incrementally**: Test TOON with one workspace before converting all
4. **Validate conversions**: Use `convert_workspaces_to_toon.py` which includes validation

## Best Practices

1. **Default to TOON**: Use `.toon` extension for new workspaces
2. **Use auto-detection**: Let `WorkspaceManager.load()` detect format
3. **Test round-trips**: Validate that save → load preserves all data
4. **Monitor compression**: Track actual file size reduction for your data
5. **Keep JSON backups**: Maintain JSON copies during initial TOON adoption

## Further Reading

- Full implementation details: `TOON_IMPLEMENTATION_RESULTS.md`
- Original TOON spec: https://github.com/toon-format/toon
- GSW schema documentation: `src/logic/gsw_schema.py`
