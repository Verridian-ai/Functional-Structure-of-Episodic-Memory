# Statutory RAG Validation Module

## Overview

The Statutory RAG Validation module provides comprehensive validation capabilities for legal extractions against statutory corpus using Retrieval-Augmented Generation (RAG) techniques. This module is part of the Verridian AI project and ensures that legal extractions comply with statutory requirements.

## Components

### 1. `statutory_rag.py`

Main validation module containing:

#### `StatutoryReference`
Dataclass representing a statutory citation with fields:
- `act_name`: Name of the legislation (e.g., "Family Law Act 1975")
- `section`: Section number (e.g., "60CC")
- `subsection`: Optional subsection identifier
- `content`: Text content of the provision
- `url`: URL reference to the legislation

#### `ValidationResult`
Dataclass containing validation outcomes:
- `is_valid`: Boolean indicating overall validity
- `compliance_score`: Float (0.0-1.0) indicating compliance level
- `supporting_citations`: List of relevant statutory references
- `conflicts`: List of identified conflicts with requirements
- `recommendations`: List of recommendations for improvement

#### `StatutoryRAGValidator`
Main validator class with methods:
- `__init__(corpus_path)`: Initialize with corpus directory path
- `validate_extraction(extraction, context)`: Validate a legal extraction
- `_extract_claims(extraction)`: Extract verifiable claims from extraction
- `_retrieve_statutes(claims)`: Retrieve relevant statutory provisions
- `_check_compliance(claims, statutes)`: Calculate compliance score
- `_detect_conflicts(claims, statutes)`: Identify conflicts with requirements
- `_generate_recommendations(conflicts)`: Generate improvement recommendations

### 2. `corpus_loader.py`

Corpus management module containing:

#### `CorpusLoader`
Class for loading and managing statutory corpus with methods:
- `__init__(corpus_dir)`: Initialize and load corpus from directory
- `get_section(section_number, act_name)`: Retrieve specific section
- `search_by_keyword(keyword, top_k)`: Search sections by keyword
- `search_by_text(query, top_k)`: Full-text search with relevance scoring
- `get_related_provisions(section_number)`: Find related provisions
- `get_sections_by_legal_test(legal_test)`: Search by legal test name
- `get_all_acts()`: Get metadata for all loaded acts

### 3. `__init__.py`

Module initialization and exports.

## Installation

No additional dependencies beyond the base project requirements. The module uses standard Python libraries.

## Usage

### Basic Validation

```python
from validation import StatutoryRAGValidator

# Initialize validator
validator = StatutoryRAGValidator(corpus_path="data/statutory_corpus")

# Prepare extraction for validation
extraction = {
    "legal_test": "Best Interests of the Child",
    "elements": {
        "safety": "Safety from harm is paramount",
        "meaningful_relationship": "Child benefits from relationship with both parents"
    },
    "findings": [
        "Court found no family violence concerns",
        "Child expressed preference for shared time"
    ]
}

# Validate
result = validator.validate_extraction(extraction)

# Check results
print(f"Valid: {result.is_valid}")
print(f"Compliance: {result.compliance_score:.2%}")

for citation in result.supporting_citations:
    print(f"Citation: {citation}")

for conflict in result.conflicts:
    print(f"Conflict: {conflict}")

for recommendation in result.recommendations:
    print(f"Recommendation: {recommendation}")
```

### Using Corpus Loader Directly

```python
from validation import CorpusLoader

# Initialize loader
loader = CorpusLoader("data/statutory_corpus")

# Get specific section
section = loader.get_section("60CC", act_name="Family Law Act 1975")
print(section['title'])
print(section['summary'])

# Search by keyword
results = loader.search_by_keyword("best interests", top_k=5)
for result in results:
    print(f"s{result['section']}: {result['title']}")

# Full-text search
results = loader.search_by_text("family violence and child safety", top_k=5)
for result in results:
    print(f"s{result['section']}: {result['title']} "
          f"(relevance: {result['relevance_score']:.2f})")

# Get related provisions
related = loader.get_related_provisions("60CC")
for provision in related:
    print(f"Related: s{provision['section']} - {provision['title']}")
```

## Corpus Format

The statutory corpus should be in JSON format with the following structure:

```json
{
  "act": {
    "name": "Act Name",
    "jurisdiction": "Jurisdiction",
    "citation": "Act Name Year (Jurisdiction)",
    "url": "https://legislation.gov.au/...",
    "version": "2024-current"
  },
  "sections": [
    {
      "section": "60CC",
      "title": "Section Title",
      "legal_test": "Legal Test Name",
      "keywords": ["keyword1", "keyword2"],
      "summary": "Summary of the section",
      "required_elements": [
        {
          "element": "element_name",
          "keywords": ["safety", "harm"],
          "weight": 0.95,
          "description": "Element description"
        }
      ],
      "threshold": 0.6,
      "minimum_elements": 2
    }
  ]
}
```

## Validation Logic

The validator performs the following steps:

1. **Claim Extraction**: Extracts verifiable legal claims from the extraction
2. **Statute Retrieval**: Uses hybrid search (keyword + text) to find relevant statutes
3. **Compliance Checking**: Calculates compliance score based on:
   - Term overlap between claims and statutory text
   - Presence of required elements
   - Matching of legal test criteria
4. **Conflict Detection**: Identifies:
   - Missing required elements
   - Contradictions with statutory requirements
   - Insufficient coverage of legal tests
5. **Recommendation Generation**: Provides specific recommendations based on detected issues

## Compliance Scoring

- **0.8-1.0**: Excellent compliance - extraction fully addresses statutory requirements
- **0.6-0.8**: Good compliance - extraction is valid with minor gaps
- **0.4-0.6**: Moderate compliance - extraction has significant gaps (invalid)
- **0.0-0.4**: Poor compliance - extraction fails to meet requirements (invalid)

Threshold for validity: **0.6** (60%)

## Testing

Run the test script to verify functionality:

```bash
python test_statutory_validation.py
```

This will run comprehensive tests including:
- Valid extractions with good compliance
- Incomplete extractions with missing elements
- Complex multi-issue cases
- Error handling for invalid inputs
- Corpus loader functionality

## Future Enhancements

Planned improvements include:

1. **Semantic Embeddings**: Integration with sentence transformers for semantic similarity
2. **Vector Database**: Use of FAISS or similar for efficient similarity search
3. **Multi-Act Validation**: Cross-referencing between different acts
4. **Citation Linking**: Automatic resolution of statutory cross-references
5. **Version Control**: Support for multiple versions of legislation
6. **Natural Language Generation**: Enhanced recommendation text generation
7. **Confidence Intervals**: Statistical confidence measures for compliance scores

## License

Part of the Verridian AI project. See main project LICENSE for details.

## Authors

Verridian AI Project Contributors

## Support

For issues or questions, refer to the main project documentation or raise an issue in the project repository.
