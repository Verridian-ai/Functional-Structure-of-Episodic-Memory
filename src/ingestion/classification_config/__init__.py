"""
Classification Configuration Module
====================================

This module provides classification configuration for the ingestion pipeline.
It includes court hierarchy mappings, legislative status definitions, and
domain-specific keyword dictionaries.

The configuration has been refactored from a single large file into a
modular structure for maintainability.

Structure:
    - hierarchy.py: Court and tribunal hierarchy mappings
    - legislation.py: Legislative status and type mappings
    - keywords/: Domain-specific keyword dictionaries
        - criminal.py: Criminal law keywords
        - family.py: Family law keywords
        - employment.py: Employment law keywords
        - property.py: Property law keywords
        - commercial.py: Commercial law keywords
        - administrative.py: Administrative law keywords
        - other.py: Other domain keywords

Usage:
    from src.ingestion.classification_config import (
        HIERARCHY_MAP,
        LEGISLATION_STATUS_MAP,
        CLASSIFICATION_MAP,
        get_keywords_for_domain,
    )
"""

from .hierarchy import HIERARCHY_MAP
from .legislation import LEGISLATION_STATUS_MAP
from .keywords import (
    CLASSIFICATION_MAP,
    get_keywords_for_domain,
    get_all_domains,
    get_keyword_count,
)

__all__ = [
    'HIERARCHY_MAP',
    'LEGISLATION_STATUS_MAP',
    'CLASSIFICATION_MAP',
    'get_keywords_for_domain',
    'get_all_domains',
    'get_keyword_count',
]
