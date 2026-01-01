"""
Court and Tribunal Hierarchy Configuration
==========================================

Defines the hierarchy weight mappings for Australian courts and tribunals.
Used for authority scoring in the classification pipeline.

Weight Scale:
    10 = Apex Court (High Court of Australia)
    9  = Full Court Appeals
    8  = State/Territory Court of Appeal
    7  = Federal Court (single judge)
    6  = Supreme Courts
    4-5 = Intermediate Courts / Major Tribunals
    2-3 = Lower Courts / Minor Tribunals
    1  = Lowest level
"""

from typing import TypedDict


class HierarchyEntry(TypedDict):
    """Type definition for hierarchy map entries."""
    jurisdiction: str
    court: str
    weight: int
    type: str


HIERARCHY_MAP: dict[str, HierarchyEntry] = {
    # ==========================================================================
    # Commonwealth Courts
    # ==========================================================================
    'HCA': {'jurisdiction': 'CTH', 'court': 'High Court', 'weight': 10, 'type': 'Case'},
    'FCAFC': {'jurisdiction': 'CTH', 'court': 'Federal Court (Full)', 'weight': 9, 'type': 'Case'},
    'FCA': {'jurisdiction': 'CTH', 'court': 'Federal Court', 'weight': 7, 'type': 'Case'},
    'FamCAFC': {'jurisdiction': 'CTH', 'court': 'Family Court (Appeal)', 'weight': 8, 'type': 'Case'},
    'FedCFamC1A': {'jurisdiction': 'CTH', 'court': 'Federal Circuit and Family Court (Div 1 Appeal)', 'weight': 8, 'type': 'Case'},
    'FedCFamC1F': {'jurisdiction': 'CTH', 'court': 'Federal Circuit and Family Court (Div 1)', 'weight': 6, 'type': 'Case'},
    'FedCFamC2F': {'jurisdiction': 'CTH', 'court': 'Federal Circuit and Family Court (Div 2)', 'weight': 5, 'type': 'Case'},

    # ==========================================================================
    # Commonwealth Tribunals
    # ==========================================================================
    'AATA': {'jurisdiction': 'CTH', 'court': 'Admin Appeals Tribunal', 'weight': 4, 'type': 'Tribunal'},
    'ART': {'jurisdiction': 'CTH', 'court': 'Admin Review Tribunal', 'weight': 4, 'type': 'Tribunal'},
    'FWCFB': {'jurisdiction': 'CTH', 'court': 'Fair Work Commission (Full Bench)', 'weight': 5, 'type': 'Tribunal'},
    'FWCA': {'jurisdiction': 'CTH', 'court': 'Fair Work Commission', 'weight': 4, 'type': 'Tribunal'},

    # ==========================================================================
    # New South Wales
    # ==========================================================================
    'NSWCA': {'jurisdiction': 'NSW', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'NSWCCA': {'jurisdiction': 'NSW', 'court': 'Court of Criminal Appeal', 'weight': 8, 'type': 'Case'},
    'NSWSC': {'jurisdiction': 'NSW', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'NSWDC': {'jurisdiction': 'NSW', 'court': 'District Court', 'weight': 4, 'type': 'Case'},
    'NSWLC': {'jurisdiction': 'NSW', 'court': 'Local Court', 'weight': 2, 'type': 'Case'},
    'NSWCAT': {'jurisdiction': 'NSW', 'court': 'NCAT', 'weight': 3, 'type': 'Tribunal'},
    'NSWLEC': {'jurisdiction': 'NSW', 'court': 'Land and Environment Court', 'weight': 5, 'type': 'Case'},
    'NSWIRC': {'jurisdiction': 'NSW', 'court': 'Industrial Relations Commission', 'weight': 4, 'type': 'Tribunal'},

    # ==========================================================================
    # Victoria
    # ==========================================================================
    'VSCA': {'jurisdiction': 'VIC', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'VSC': {'jurisdiction': 'VIC', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'VCC': {'jurisdiction': 'VIC', 'court': 'County Court', 'weight': 4, 'type': 'Case'},
    'VMC': {'jurisdiction': 'VIC', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},
    'VCAT': {'jurisdiction': 'VIC', 'court': 'VCAT', 'weight': 3, 'type': 'Tribunal'},

    # ==========================================================================
    # Queensland
    # ==========================================================================
    'QCA': {'jurisdiction': 'QLD', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'QSC': {'jurisdiction': 'QLD', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'QDC': {'jurisdiction': 'QLD', 'court': 'District Court', 'weight': 4, 'type': 'Case'},
    'QMC': {'jurisdiction': 'QLD', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},
    'QCAT': {'jurisdiction': 'QLD', 'court': 'QCAT', 'weight': 3, 'type': 'Tribunal'},
    'QIRC': {'jurisdiction': 'QLD', 'court': 'Industrial Relations Commission', 'weight': 4, 'type': 'Tribunal'},

    # ==========================================================================
    # Western Australia
    # ==========================================================================
    'WASCA': {'jurisdiction': 'WA', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'WASC': {'jurisdiction': 'WA', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'WADC': {'jurisdiction': 'WA', 'court': 'District Court', 'weight': 4, 'type': 'Case'},
    'WAMC': {'jurisdiction': 'WA', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},
    'WASAT': {'jurisdiction': 'WA', 'court': 'State Admin Tribunal', 'weight': 3, 'type': 'Tribunal'},

    # ==========================================================================
    # South Australia
    # ==========================================================================
    'SASCA': {'jurisdiction': 'SA', 'court': 'Supreme Court (Full)', 'weight': 8, 'type': 'Case'},
    'SASC': {'jurisdiction': 'SA', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'SADC': {'jurisdiction': 'SA', 'court': 'District Court', 'weight': 4, 'type': 'Case'},
    'SAMC': {'jurisdiction': 'SA', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},
    'SACAT': {'jurisdiction': 'SA', 'court': 'SACAT', 'weight': 3, 'type': 'Tribunal'},
    'SAET': {'jurisdiction': 'SA', 'court': 'Employment Tribunal', 'weight': 4, 'type': 'Tribunal'},

    # ==========================================================================
    # Tasmania
    # ==========================================================================
    'TASFC': {'jurisdiction': 'TAS', 'court': 'Full Court', 'weight': 8, 'type': 'Case'},
    'TASSC': {'jurisdiction': 'TAS', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'TASMC': {'jurisdiction': 'TAS', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},

    # ==========================================================================
    # Australian Capital Territory
    # ==========================================================================
    'ACTCA': {'jurisdiction': 'ACT', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'ACTSC': {'jurisdiction': 'ACT', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'ACTMC': {'jurisdiction': 'ACT', 'court': 'Magistrates Court', 'weight': 2, 'type': 'Case'},
    'ACAT': {'jurisdiction': 'ACT', 'court': 'ACT Civil and Admin Tribunal', 'weight': 3, 'type': 'Tribunal'},

    # ==========================================================================
    # Northern Territory
    # ==========================================================================
    'NTCA': {'jurisdiction': 'NT', 'court': 'Court of Appeal', 'weight': 8, 'type': 'Case'},
    'NTSC': {'jurisdiction': 'NT', 'court': 'Supreme Court', 'weight': 6, 'type': 'Case'},
    'NTLC': {'jurisdiction': 'NT', 'court': 'Local Court', 'weight': 2, 'type': 'Case'},
}


def get_court_weight(court_code: str) -> int:
    """Get the authority weight for a given court code."""
    entry = HIERARCHY_MAP.get(court_code.upper())
    return entry['weight'] if entry else 0


def get_court_info(court_code: str) -> HierarchyEntry | None:
    """Get full information for a given court code."""
    return HIERARCHY_MAP.get(court_code.upper())


def get_courts_by_jurisdiction(jurisdiction: str) -> dict[str, HierarchyEntry]:
    """Get all courts for a given jurisdiction."""
    return {
        code: entry
        for code, entry in HIERARCHY_MAP.items()
        if entry['jurisdiction'] == jurisdiction.upper()
    }
