# VSA Anti-Hallucination Validation System

## Overview

The VSA (Vector Symbolic Architecture) Anti-Hallucination Validation system provides confidence scoring and hallucination detection for retrieval-augmented generation (RAG) systems in the legal domain.

This system implements **Phase 6** of the Legal GSW architecture, integrating VSA-based validation with the retrieval pipeline to ensure factual accuracy and detect unsupported claims.

## Architecture

### Components

1. **VSAValidator** (`src/retrieval/vsa_validator.py`)
   - Core validation engine
   - Claim extraction and concept encoding
   - Similarity-based validation
   - Confidence calibration

2. **LegalRetriever** (`src/retrieval/retriever.py`)
   - Enhanced with VSA validation
   - Integrated validation pipeline
   - Batch validation capabilities

3. **LegalVSA** (`src/vsa/legal_vsa.py`)
   - Hyperdimensional computing backend
   - Ontology-based reasoning
   - Symbolic logic validation

### Data Flow

```
Query → Retrieval → Response Generation → VSA Validation → Validated Response
                                              ↓
                                    Global Workspace
                                    (Ground Truth)
```

## Key Features

### 1. Claim Extraction

The system automatically extracts factual claims from generated responses:

- Filters out questions (`?`)
- Removes opinion statements (modal verbs: "may", "might", "could")
- Identifies factual assertions (verbs of being, action verbs)

**Example:**
```python
Input: "John married Jane in 2010. They might divorce soon."
Output: ["John married Jane in 2010"]  # Opinion filtered out
```

### 2. Confidence Calibration

VSA similarity scores are mapped to calibrated confidence values:

| Similarity | Confidence | Category |
|------------|------------|----------|
| > 0.9      | 0.95       | Very High |
| 0.7 - 0.9  | 0.80 - 0.95| High |
| 0.5 - 0.7  | 0.60 - 0.80| Medium |
| 0.3 - 0.5  | 0.40 - 0.60| Low |
| < 0.3      | 0.0 - 0.40 | Very Low |

### 3. Hallucination Detection

The system flags claims as hallucinations based on:

- **Low similarity** (< 0.3) to workspace knowledge
- **VSA ontology violations** (contradictions, missing requirements)
- **Multi-factor scoring** (60% similarity + 40% VSA confidence)

### 4. Severity Classification

Claims are categorized by risk level:

- **High Risk**: Similarity < 0.3 (likely hallucination)
- **Medium Risk**: Similarity 0.3 - 0.5 (uncertain)
- **Low Risk**: Similarity 0.5 - 0.7 (needs verification)
- **Verified**: Similarity >= 0.7 (high confidence)

## Usage

### Basic Validation

```python
from src.retrieval.vsa_validator import VSAValidator
from src.logic.gsw_schema import GlobalWorkspace

# Initialize validator
validator = VSAValidator()

# Create or load workspace
workspace = GlobalWorkspace()
# ... populate workspace with actors, states, etc.

# Validate a response
query = "When did John marry Jane?"
response = "John married Jane in 2010."

result = validator.validate_response(query, response, workspace)

print(f"Confidence: {result['overall_confidence']:.2f}")
print(f"Hallucination Detected: {result['hallucination_detected']}")
print(f"Verified Claims: {result['severity']['verified']}")
```

### Retrieval with Validation

```python
from src.retrieval.retriever import LegalRetriever

# Initialize retriever with validation enabled
retriever = LegalRetriever(enable_vsa_validation=True)

# Retrieve and validate
result = retriever.retrieve_with_validation(
    query="When did John marry Jane?",
    workspace=workspace,
    generate_response=True
)

print(f"Response: {result['response']}")
print(f"Confidence: {result['confidence']:.2f}")
if result['hallucination_risk']:
    print(f"Warning: {result['warning']}")
```

### Single Claim Validation

```python
# Validate individual claim
claim = "John divorced Jane in 2015"
result = retriever.validate_claim(claim, workspace)

print(f"Valid: {result['valid']}")
print(f"Confidence: {result['confidence']:.2f}")
if result['vsa_issues']:
    print(f"Issues: {result['vsa_issues']}")
```

### Batch Validation

```python
# Validate multiple claims
claims = [
    "John married Jane in 2010",
    "They separated in 2020",
    "John is a doctor"
]

results = retriever.batch_validate_claims(claims, workspace)

for claim, result in zip(claims, results):
    print(f"{claim}: {result['confidence']:.2f}")
```

## Validation Results

### Response Validation

```python
{
    'total_claims': 3,
    'valid_claims': 2,
    'overall_confidence': 0.75,
    'similarity_confidence': 0.80,
    'vsa_confidence': 0.65,
    'hallucination_detected': False,
    'severity': {
        'high_risk': 0,
        'medium_risk': 1,
        'low_risk': 0,
        'verified': 2
    },
    'individual_validations': [
        {
            'claim': 'John married Jane in 2010',
            'similarity': 0.85,
            'confidence': 0.87,
            'valid': True,
            'vsa_valid': True,
            'vsa_confidence': 0.82
        },
        # ... more claims
    ]
}
```

### Claim Validation

```python
{
    'claim': 'John married Jane',
    'concepts': ['john', 'married', 'jane'],
    'similarity': 0.85,
    'confidence': 0.87,
    'valid': True,
    'vsa_valid': True,
    'vsa_issues': [],
    'vsa_confidence': 0.82
}
```

## Configuration

### Enable/Disable Validation

```python
# Disable validation for performance
retriever = LegalRetriever(enable_vsa_validation=False)

# Enable validation (default)
retriever = LegalRetriever(enable_vsa_validation=True)
```

### Custom Ontology

```python
from pathlib import Path

# Load custom ontology rules
ontology_path = Path("data/ontology/custom_rules.json")
validator = VSAValidator(ontology_path=ontology_path)
```

## Testing

### Run Tests

```bash
# Run all validation tests
pytest tests/test_vsa_validator.py -v

# Run specific test class
pytest tests/test_vsa_validator.py::TestClaimExtraction -v

# Run with coverage
pytest tests/test_vsa_validator.py --cov=src.retrieval.vsa_validator
```

### Run Examples

```bash
# Run demonstration examples
python examples/vsa_validation_examples.py
```

This will run 7 example scenarios:
1. Validating correct facts
2. Detecting hallucinations
3. Mixed correct/incorrect claims
4. Confidence calibration curves
5. Retrieval integration
6. Batch validation
7. Severity analysis

Results are saved to `data/examples/vsa_validation_results.json`.

## Performance Considerations

### Computational Complexity

- **Claim extraction**: O(n) where n = response length
- **Concept encoding**: O(m × d) where m = concepts, d = dimension
- **Similarity calculation**: O(d) where d = 10,000 (hypervector dimension)
- **Batch validation**: Linear in number of claims

### Optimization Tips

1. **Cache workspace encodings** for repeated queries
2. **Batch validate claims** instead of one-by-one
3. **Disable validation** for non-critical queries
4. **Use GPU acceleration** for large-scale validation

```python
# Initialize VSA with GPU (if available)
from src.vsa.legal_vsa import LegalVSA
vsa = LegalVSA(device="cuda")
```

## Limitations

### Current Limitations

1. **Simple claim extraction**: Uses regex-based sentence splitting
2. **No temporal reasoning**: Doesn't validate dates/timelines
3. **No entity resolution**: Doesn't handle aliases/coreference
4. **English only**: Not tested on other languages

### Future Enhancements

1. **Enhanced claim extraction** with dependency parsing
2. **Temporal validation** for date consistency
3. **Entity linking** with workspace actors
4. **Multi-language support**
5. **Active learning** for confidence calibration

## Integration with Legal GSW

The VSA validator integrates with the Global Semantic Workspace:

1. **Workspace encoding**: Actors, states, and relationships → hypervectors
2. **Claim encoding**: Response claims → hypervectors
3. **Similarity check**: Compare claim vectors to workspace vector
4. **Ontology validation**: Check against legal rules and constraints

```
GlobalWorkspace
    ├── Actors (encoded as hypervectors)
    ├── States (bound to actors)
    └── VerbPhrases (relationships)
         ↓
    Scene Vector (workspace representation)
         ↓
    Similarity Check ← Claim Vector
         ↓
    Validation Result
```

## Confidence Calibration Methodology

### Calibration Strategy

The confidence calibration curve is designed to:

1. **Penalize low similarity heavily** (< 0.3 → very low confidence)
2. **Reward high similarity moderately** (> 0.7 → high confidence)
3. **Provide smooth transitions** between levels
4. **Ensure monotonicity** (higher similarity = higher confidence)

### Validation Formula

```
Combined Confidence = (Similarity Confidence × 0.6) + (VSA Confidence × 0.4)
```

This weights:
- **Similarity**: 60% (data-driven, workspace alignment)
- **VSA Ontology**: 40% (rule-based, logic validation)

## Troubleshooting

### Low Confidence on Correct Facts

**Cause**: Workspace may be incomplete or concepts not in ontology

**Solution**:
- Ensure workspace is populated with relevant actors/states
- Check that concepts are in VSA ontology
- Review confidence calibration thresholds

### False Hallucination Warnings

**Cause**: Overly strict similarity threshold

**Solution**:
- Adjust threshold in `_aggregate_validations()` (default: 0.3)
- Use `EnhancedVSAValidator` with context
- Review VSA ontology rules

### Performance Issues

**Cause**: Large responses with many claims

**Solution**:
- Enable GPU acceleration
- Batch process claims
- Cache workspace encodings
- Disable validation for simple queries

## Citation

If you use this validation system in your research, please cite:

```bibtex
@article{episodic_memory_2024,
  title={Functional Structure of Episodic Memory},
  author={Your Research Team},
  journal={arXiv},
  year={2024},
  note={arXiv:2511.07587}
}
```

## License

This validation system is part of the Legal GSW project and follows the same license terms.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Consult the main project documentation
- Review test cases for examples
