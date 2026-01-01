"""
Domain-Specific Classification Keywords

This package contains expanded keyword sets for specific legal domains:
- employment.py: Employment/Industrial Relations Law
- administrative.py: Administrative/Migration Law
- criminal.py: Criminal Law (state-specific)

Usage:
    from src.ingestion.domains.employment import EMPLOYMENT_KEYWORDS
    from src.ingestion.domains.administrative import ADMINISTRATIVE_KEYWORDS
    from src.ingestion.domains.criminal import CRIMINAL_KEYWORDS
"""

# Import domain keywords when available
try:
    from .employment import EMPLOYMENT_CASES, EMPLOYMENT_KEYWORDS, EMPLOYMENT_LEGISLATION
except ImportError:
    EMPLOYMENT_KEYWORDS = {}
    EMPLOYMENT_LEGISLATION = {}
    EMPLOYMENT_CASES = {}

try:
    from .administrative import (
        ADMINISTRATIVE_CASES,
        ADMINISTRATIVE_KEYWORDS,
        ADMINISTRATIVE_LEGISLATION,
    )
except ImportError:
    ADMINISTRATIVE_KEYWORDS = {}
    ADMINISTRATIVE_LEGISLATION = {}
    ADMINISTRATIVE_CASES = {}

try:
    from .criminal import CRIMINAL_CASES, CRIMINAL_KEYWORDS, CRIMINAL_LEGISLATION
except ImportError:
    CRIMINAL_KEYWORDS = {}
    CRIMINAL_LEGISLATION = {}
    CRIMINAL_CASES = {}

__all__ = [
    "EMPLOYMENT_KEYWORDS",
    "EMPLOYMENT_LEGISLATION",
    "EMPLOYMENT_CASES",
    "ADMINISTRATIVE_KEYWORDS",
    "ADMINISTRATIVE_LEGISLATION",
    "ADMINISTRATIVE_CASES",
    "CRIMINAL_KEYWORDS",
    "CRIMINAL_LEGISLATION",
    "CRIMINAL_CASES",
]
