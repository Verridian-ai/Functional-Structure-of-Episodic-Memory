# ADR-0002: TOON Format for Token Compression

## Status

Accepted

## Context

LLM context windows have token limits and costs associated with input tokens.
When sending extracted legal information to LLMs for processing:

- JSON format is verbose with repeated keys
- Large workspaces can exceed context limits
- API costs scale with token count

We need a compact representation that:
- Reduces token count by 40%+
- Maintains semantic clarity for LLMs
- Is easy to parse programmatically

## Decision

Implement TOON (Table-Oriented Notation) format for workspace serialization.

### Format Specification

```
structure_name[count]{column1,column2,...}
value1,value2,...
value1,value2,...
```

### Example

Instead of JSON:
```json
{
  "actors": [
    {"name": "John Smith", "role": "Applicant", "type": "Person"},
    {"name": "Jane Smith", "role": "Respondent", "type": "Person"}
  ]
}
```

Use TOON:
```
actors[2]{name,role,type}
John Smith,Applicant,Person
Jane Smith,Respondent,Person
```

### Token Reduction

| Format | Characters | Est. Tokens | Reduction |
|--------|-----------|-------------|-----------|
| JSON   | 180       | 45          | baseline  |
| TOON   | 95        | 24          | 47%       |

## Consequences

### Positive

- 40-74% token reduction (measured 62-74% in production)
- Lower API costs
- Fits more context in limited windows
- LLMs can still parse the format reliably

### Negative

- Custom format requires parser implementation
- Less human-readable than pretty JSON
- Escaping commas in values requires care

### Neutral

- Requires ToonEncoder/ToonDecoder utilities
- Both JSON and TOON can coexist

## Alternatives Considered

1. **Gzip/Compression**: LLMs can't read compressed data
2. **Minimal JSON**: Still has structural overhead from keys
3. **CSV**: No structure metadata, harder for LLMs to interpret
4. **MessagePack/Binary**: Not readable by LLMs

## References

- `src/utils/toon.py` - Implementation
- `docs/TOON_QUICK_START.md` - Usage guide
