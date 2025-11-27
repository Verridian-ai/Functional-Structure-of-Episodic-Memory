"""
Statutory Validation Module
============================

Provides statutory RAG validation capabilities for the Verridian AI project.

This module validates legal extractions against statutory corpus, ensuring
compliance with legal requirements and identifying potential conflicts.

Main Components:
    - StatutoryRAGValidator: Main validator class for checking compliance
    - StatutoryReference: Dataclass representing a statutory citation
    - ValidationResult: Dataclass containing validation results
    - CorpusLoader: Utility for loading and managing statutory corpus

Example Usage:
    ```python
    from validation import StatutoryRAGValidator

    # Initialize validator with corpus path
    validator = StatutoryRAGValidator(corpus_path="data/statutory_corpus")

    # Validate an extraction
    extraction = {
        "legal_test": "Best Interests of the Child",
        "elements": ["safety", "meaningful relationship"],
        "findings": ["The court found that safety is paramount"]
    }

    result = validator.validate_extraction(extraction)

    print(f"Valid: {result.is_valid}")
    print(f"Compliance Score: {result.compliance_score}")
    print(f"Citations: {len(result.supporting_citations)}")

    for conflict in result.conflicts:
        print(f"Conflict: {conflict}")

    for recommendation in result.recommendations:
        print(f"Recommendation: {recommendation}")
    ```
"""

from .statutory_rag import (
    StatutoryRAGValidator,
    StatutoryReference,
    ValidationResult
)

from .corpus_loader import CorpusLoader


__all__ = [
    'StatutoryRAGValidator',
    'StatutoryReference',
    'ValidationResult',
    'CorpusLoader',
]

__version__ = '1.0.0'
__author__ = 'Verridian AI Project'
