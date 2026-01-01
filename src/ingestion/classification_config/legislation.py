"""
Legislative Status Configuration
================================

Defines the legislative status and type mappings for document classification.
"""

from typing import TypedDict


class LegislationEntry(TypedDict):
    """Type definition for legislation status entries."""
    type: str
    status: str
    weight: int


LEGISLATION_STATUS_MAP: dict[str, LegislationEntry] = {
    # ==========================================================================
    # Proposed / In Progress
    # ==========================================================================
    'Bill': {'type': 'Bill', 'status': 'Proposed', 'weight': 0},
    'Draft Bill': {'type': 'Bill', 'status': 'Draft', 'weight': 0},
    'Exposure Draft': {'type': 'Bill', 'status': 'Draft', 'weight': 0},

    # ==========================================================================
    # Interpretive Materials
    # ==========================================================================
    'Explanatory Memorandum': {'type': 'EM', 'status': 'Interpretive', 'weight': 1},
    'Second Reading': {'type': 'Speech', 'status': 'Interpretive', 'weight': 1},
    'Second Reading Speech': {'type': 'Speech', 'status': 'Interpretive', 'weight': 1},
    'Hansard': {'type': 'Hansard', 'status': 'Interpretive', 'weight': 1},
    'Statement of Compatibility': {'type': 'Statement', 'status': 'Interpretive', 'weight': 1},

    # ==========================================================================
    # Historical / Obsolete
    # ==========================================================================
    'Repealed': {'type': 'Act', 'status': 'Obsolete', 'weight': 0},
    'Expired': {'type': 'Act', 'status': 'Obsolete', 'weight': 0},
    'Superseded': {'type': 'Act', 'status': 'Obsolete', 'weight': 0},
    'As made': {'type': 'Act', 'status': 'Historical', 'weight': 5},
    'As passed': {'type': 'Act', 'status': 'Historical', 'weight': 5},
    'Original version': {'type': 'Act', 'status': 'Historical', 'weight': 4},

    # ==========================================================================
    # Current / In Force
    # ==========================================================================
    'In force': {'type': 'Act', 'status': 'Current', 'weight': 10},
    'Current': {'type': 'Act', 'status': 'Current', 'weight': 10},
    'Registered': {'type': 'Instrument', 'status': 'Current', 'weight': 8},
    'Compiled': {'type': 'Act', 'status': 'Current', 'weight': 10},

    # ==========================================================================
    # Subordinate Legislation
    # ==========================================================================
    'Regulation': {'type': 'Regulation', 'status': 'Current', 'weight': 8},
    'Regulations': {'type': 'Regulation', 'status': 'Current', 'weight': 8},
    'Rules': {'type': 'Rules', 'status': 'Current', 'weight': 7},
    'Rule': {'type': 'Rules', 'status': 'Current', 'weight': 7},
    'Legislative Instrument': {'type': 'Instrument', 'status': 'Current', 'weight': 6},
    'Determination': {'type': 'Determination', 'status': 'Current', 'weight': 6},
    'Order': {'type': 'Order', 'status': 'Current', 'weight': 6},
    'Direction': {'type': 'Direction', 'status': 'Current', 'weight': 5},
    'Proclamation': {'type': 'Proclamation', 'status': 'Current', 'weight': 5},
    'Notice': {'type': 'Notice', 'status': 'Current', 'weight': 4},
}


def get_legislation_weight(status_keyword: str) -> int:
    """Get the authority weight for a given legislative status."""
    entry = LEGISLATION_STATUS_MAP.get(status_keyword)
    return entry['weight'] if entry else 0


def get_legislation_info(status_keyword: str) -> LegislationEntry | None:
    """Get full information for a given legislative status."""
    return LEGISLATION_STATUS_MAP.get(status_keyword)


def is_current_legislation(status_keyword: str) -> bool:
    """Check if the legislation status indicates current/in-force."""
    entry = LEGISLATION_STATUS_MAP.get(status_keyword)
    return entry is not None and entry['status'] == 'Current'
