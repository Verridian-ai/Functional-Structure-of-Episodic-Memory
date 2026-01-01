"""
Ingestion Module - Document Classification and Processing
==========================================================

This module provides the core document classification and processing
capabilities for the Australian Legal Document Processing Pipeline.

Key Components:
- DomainClassifier: Multi-dimensional legal document classifier
- Court hierarchy and authority scoring
- Legislation and case pattern matching
- TOON format integration
"""

from .case_patterns import LANDMARK_CASES
from .classification_config import CLASSIFICATION_MAP, DOMAIN_MAPPING
from .corpus_domain_extractor import DomainClassifier
from .court_hierarchy import (
    COURT_CODES,
    extract_court_from_citation,
    get_authority_score,
    get_court_info,
    get_domain_hint,
)
from .legislation_patterns import LEGISLATION_TO_DOMAIN

__all__ = [
    "DomainClassifier",
    "COURT_CODES",
    "get_court_info",
    "get_authority_score",
    "get_domain_hint",
    "extract_court_from_citation",
    "CLASSIFICATION_MAP",
    "DOMAIN_MAPPING",
    "LEGISLATION_TO_DOMAIN",
    "LANDMARK_CASES",
]
