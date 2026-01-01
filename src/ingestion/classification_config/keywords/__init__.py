"""
Domain-Specific Keyword Configuration
======================================

This module aggregates keywords from all domain-specific files into
the CLASSIFICATION_MAP dictionary used by the classifier.

For backwards compatibility with the original classification_config.py,
the CLASSIFICATION_MAP is maintained as a unified dictionary.

Domain Modules:
    - criminal.py: Criminal law keywords
    - family.py: Family law keywords
    - employment.py: Employment/industrial law keywords
    - property.py: Property and conveyancing keywords
    - commercial.py: Commercial and corporate keywords
    - administrative.py: Administrative law keywords
    - other.py: Other specialized domains

Note: Due to the large size of the original keyword dictionary (16,000+ keywords),
the actual keyword content remains in the legacy file until a full migration is
performed using the migrate_keywords.py script.
"""

import logging

logger = logging.getLogger(__name__)

# Domain category prefixes for organization
DOMAIN_PREFIXES = {
    "Criminal": [
        "Criminal_Violence",
        "Criminal_Sexual",
        "Criminal_Drugs",
        "Criminal_Property",
        "Criminal_Traffic",
        "Criminal_Procedure",
        "Criminal_Sentencing",
    ],
    "Family": [
        "Family_Property",
        "Family_Children",
        "Family_Violence",
        "Family_Financial",
        "Family_Procedure",
    ],
    "Employment": [
        "Employment_Unfair",
        "Employment_General",
        "Employment_WHS",
        "Employment_Enterprise",
        "Employment_Discrimination",
    ],
    "Property": [
        "Property_Conveyancing",
        "Property_Strata",
        "Property_Landlord",
        "Property_Planning",
    ],
    "Commercial": [
        "Commercial_Contract",
        "Commercial_Consumer",
        "Commercial_Insolvency",
        "Commercial_Competition",
        "Commercial_IP",
    ],
    "Administrative": [
        "Administrative_Migration",
        "Administrative_Review",
        "Administrative_FOI",
        "Administrative_Environment",
    ],
}


def _load_legacy_keywords() -> dict[str, list[str]]:
    """
    Load keywords from the legacy classification_config.py file.

    This function imports the CLASSIFICATION_MAP from the original file
    for backwards compatibility.

    Returns:
        Dictionary mapping category names to keyword lists
    """
    try:
        # Import from the legacy file location
        from src.ingestion.classification_config_legacy import CLASSIFICATION_MAP as legacy_map

        return legacy_map
    except ImportError:
        # If no legacy file exists, try the original location
        try:
            import sys
            from pathlib import Path

            # Add parent directory to path
            parent = Path(__file__).resolve().parents[2]
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))

            from classification_config import CLASSIFICATION_MAP as orig_map

            return orig_map
        except ImportError:
            logger.warning("Could not load legacy classification map, using empty dict")
            return {}


# Load the classification map
# For now, this loads from the legacy file
# After migration, this will import from domain-specific modules
try:
    CLASSIFICATION_MAP = _load_legacy_keywords()
except Exception as e:
    logger.error(f"Failed to load classification map: {e}")
    CLASSIFICATION_MAP = {}


def get_keywords_for_domain(domain_prefix: str) -> dict[str, list[str]]:
    """
    Get all keyword categories for a specific legal domain.

    Args:
        domain_prefix: The domain prefix (e.g., 'Criminal', 'Family')

    Returns:
        Dictionary of category names to keyword lists for that domain
    """
    prefix = domain_prefix if domain_prefix.endswith("_") else f"{domain_prefix}_"
    return {
        category: keywords
        for category, keywords in CLASSIFICATION_MAP.items()
        if category.startswith(prefix)
    }


def get_all_domains() -> list[str]:
    """
    Get list of all unique domain prefixes.

    Returns:
        List of domain prefix strings
    """
    domains = set()
    for category in CLASSIFICATION_MAP:
        if "_" in category:
            domain = category.split("_")[0]
            domains.add(domain)
    return sorted(domains)


def get_keyword_count() -> dict[str, int]:
    """
    Get count of keywords per category.

    Returns:
        Dictionary mapping category names to keyword counts
    """
    return {category: len(keywords) for category, keywords in CLASSIFICATION_MAP.items()}


def get_total_keyword_count() -> int:
    """Get total number of keywords across all categories."""
    return sum(len(keywords) for keywords in CLASSIFICATION_MAP.values())


def search_keywords(term: str, case_sensitive: bool = False) -> dict[str, list[str]]:
    """
    Search for keywords containing a specific term.

    Args:
        term: Search term
        case_sensitive: Whether search is case-sensitive

    Returns:
        Dictionary of category -> matching keywords
    """
    results = {}
    search_term = term if case_sensitive else term.lower()

    for category, keywords in CLASSIFICATION_MAP.items():
        matches = []
        for keyword in keywords:
            compare_keyword = keyword if case_sensitive else keyword.lower()
            if search_term in compare_keyword:
                matches.append(keyword)
        if matches:
            results[category] = matches

    return results
