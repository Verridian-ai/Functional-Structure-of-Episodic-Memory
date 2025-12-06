# VSA Validation Quick Start Guide

## 5-Minute Setup

### 1. Import Required Modules

```python
from src.retrieval.vsa_validator import VSAValidator
from src.retrieval.retriever import LegalRetriever
from src.logic.gsw_schema import GlobalWorkspace, Actor, ActorType, State
```

### 2. Create a Workspace

```python
# Initialize workspace
workspace = GlobalWorkspace()

# Add actors
john = Actor(
    name="John Smith",
    actor_type=ActorType.PERSON,
    roles=["husband"]
)
workspace.add_actor(john)

# Add states
john.add_state(State(
    entity_id=john.id,
    name="MaritalStatus",
    value="Married",
    start_date="2010-03-15"
))
```

### 3. Validate Claims

```python
# Option A: Direct validation
validator = VSAValidator()
result = validator.validate_claim("John is married", workspace)
print(f"Confidence: {result['confidence']:.2f}")

# Option B: Through retriever
retriever = LegalRetriever(enable_vsa_validation=True)
result = retriever.validate_claim("John is married", workspace)
print(f"Valid: {result['valid']}")
```

### 4. Validate Responses

```python
query = "Tell me about John"
response = "John is married and lives in Sydney."

result = validator.validate_response(query, response, workspace)

print(f"Confidence: {result['overall_confidence']:.2f}")
print(f"Hallucination: {result['hallucination_detected']}")
print(f"Verified claims: {result['severity']['verified']}")
```

## Common Use Cases

### Use Case 1: Validate Retrieval Results

```python
retriever = LegalRetriever(enable_vsa_validation=True)

result = retriever.retrieve_with_validation(
    query="When did John marry?",
    workspace=workspace,
    generate_response=True
)

if result['hallucination_risk']:
    print(f"Warning: {result['warning']}")
else:
    print(f"Safe to use: {result['response']}")
```

### Use Case 2: Batch Validate Claims

```python
claims = [
    "John is married",
    "John is a doctor",
    "John lives in Sydney"
]

results = retriever.batch_validate_claims(claims, workspace)

for claim, result in zip(claims, results):
    status = "✓" if result['valid'] else "✗"
    print(f"{status} {claim} ({result['confidence']:.2f})")
```

### Use Case 3: Check Confidence Levels

```python
result = validator.validate_response(query, response, workspace)

if result['overall_confidence'] > 0.8:
    print("High confidence - safe to use")
elif result['overall_confidence'] > 0.5:
    print("Medium confidence - review recommended")
else:
    print("Low confidence - do not use")
```

## Interpreting Results

### Confidence Levels
- **0.80 - 1.00**: High confidence (safe to use)
- **0.60 - 0.80**: Medium confidence (review recommended)
- **0.40 - 0.60**: Low confidence (verify sources)
- **0.00 - 0.40**: Very low confidence (likely hallucination)

### Severity Breakdown
- **verified**: Claims matching workspace (similarity ≥ 0.7)
- **low_risk**: Minor discrepancies (similarity 0.5-0.7)
- **medium_risk**: Significant issues (similarity 0.3-0.5)
- **high_risk**: Likely hallucinations (similarity < 0.3)

## Testing

### Run Tests
```bash
# All validation tests
pytest tests/test_vsa_validator.py -v

# Specific test
pytest tests/test_vsa_validator.py::TestValidation::test_validate_correct_fact -v
```

### Run Examples
```bash
# Full demonstration
python examples/vsa_validation_examples.py

# Results saved to: data/examples/vsa_validation_results.json
```

## Troubleshooting

### Problem: Low confidence on correct facts
**Solution**: Ensure workspace has relevant actors and states

### Problem: High confidence on wrong facts
**Solution**: Check workspace completeness and ontology

### Problem: Performance issues
**Solution**: Disable validation for non-critical queries
```python
retriever = LegalRetriever(enable_vsa_validation=False)
```

## Advanced Features

### Enhanced Validator with Context
```python
from src.retrieval.vsa_validator import EnhancedVSAValidator

validator = EnhancedVSAValidator()
result = validator.validate_with_context(
    query=query,
    response=response,
    workspace=workspace,
    context={'case_id': '123', 'date': '2024-01-01'}
)
```

### Custom Ontology
```python
from pathlib import Path

ontology_path = Path("data/ontology/custom_rules.json")
validator = VSAValidator(ontology_path=ontology_path)
```

## API Reference

### VSAValidator

**Methods:**
- `validate_response(query, response, workspace)` → Dict
- `validate_claim(claim, workspace)` → Dict
- `_extract_claims(response)` → List[str]
- `_calibrate_confidence(similarity)` → float

### LegalRetriever

**Methods:**
- `retrieve_with_validation(query, workspace, top_k, generate_response)` → Dict
- `validate_claim(claim, workspace)` → Dict
- `batch_validate_claims(claims, workspace)` → List[Dict]

## Full Documentation

For complete documentation, see: `docs/VSA_VALIDATION.md`
