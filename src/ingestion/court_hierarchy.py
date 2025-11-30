"""
Court Hierarchy for Corpus Labeling
====================================
Maps Australian court codes to hierarchy levels and jurisdictions.

This module contains:
- COURT_CODES: Dictionary mapping court abbreviations to metadata
- JURISDICTION_MAPPING: Maps jurisdictions to domains
- Utility functions for court identification
"""

import re
from typing import Dict, List, Optional, Tuple

# ============================================================================
# COURT HIERARCHY LEVELS
# ============================================================================

HIERARCHY_LEVELS = {
    'apex': 1,           # High Court only
    'superior_appellate': 2,  # State/Federal appellate courts
    'intermediate_appellate': 3,  # Full courts, courts of appeal
    'superior_trial': 4,  # Supreme Courts single judge
    'intermediate': 5,    # District/County courts
    'lower': 6,          # Local/Magistrates courts
    'tribunal': 7,       # Administrative tribunals
    'specialist': 8,     # Specialist courts/tribunals
}


# ============================================================================
# COURT CODES AND METADATA
# ============================================================================

COURT_CODES = {
    # --- FEDERAL COURTS ---
    'HCA': {
        'name': 'High Court of Australia',
        'level': 'apex',
        'jurisdiction': 'Commonwealth',
        'binding': True,  # Binds all Australian courts
        'authority_score': 100,
    },
    'FCAFC': {
        'name': 'Federal Court of Australia Full Court',
        'level': 'superior_appellate',
        'jurisdiction': 'Commonwealth',
        'binding': 'same_jurisdiction',
        'authority_score': 90,
    },
    'FCA': {
        'name': 'Federal Court of Australia',
        'level': 'superior_trial',
        'jurisdiction': 'Commonwealth',
        'binding': 'lower_federal',
        'authority_score': 80,
    },
    'FedCFamC': {
        'name': 'Federal Circuit and Family Court',
        'level': 'intermediate',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 60,
    },
    'FamCA': {
        'name': 'Family Court of Australia',
        'level': 'superior_trial',
        'jurisdiction': 'Commonwealth',
        'binding': 'family_matters',
        'authority_score': 75,
        'domain_hint': 'Family',
    },
    'FamCAFC': {
        'name': 'Family Court of Australia Full Court',
        'level': 'superior_appellate',
        'jurisdiction': 'Commonwealth',
        'binding': 'family_matters',
        'authority_score': 85,
        'domain_hint': 'Family',
    },
    'FCCA': {
        'name': 'Federal Circuit Court of Australia',
        'level': 'intermediate',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 55,
    },
    'AATA': {
        'name': 'Administrative Appeals Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 40,
        'domain_hint': 'Administrative',
    },
    'AAT': {
        'name': 'Administrative Appeals Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 40,
        'domain_hint': 'Administrative',
    },

    # --- NEW SOUTH WALES ---
    'NSWCA': {
        'name': 'NSW Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'NSW',
        'binding': 'nsw_courts',
        'authority_score': 85,
    },
    'NSWCCA': {
        'name': 'NSW Court of Criminal Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'NSW',
        'binding': 'nsw_criminal',
        'authority_score': 85,
        'domain_hint': 'Criminal',
    },
    'NSWSC': {
        'name': 'NSW Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'NSW',
        'binding': 'lower_nsw',
        'authority_score': 75,
    },
    'NSWDC': {
        'name': 'NSW District Court',
        'level': 'intermediate',
        'jurisdiction': 'NSW',
        'binding': False,
        'authority_score': 50,
    },
    'NSWLC': {
        'name': 'NSW Local Court',
        'level': 'lower',
        'jurisdiction': 'NSW',
        'binding': False,
        'authority_score': 30,
    },
    'NSWLEC': {
        'name': 'NSW Land and Environment Court',
        'level': 'specialist',
        'jurisdiction': 'NSW',
        'binding': 'nsw_environment',
        'authority_score': 70,
        'domain_hint': 'Environment',
    },
    'NSWIC': {
        'name': 'NSW Industrial Court',
        'level': 'specialist',
        'jurisdiction': 'NSW',
        'binding': 'nsw_industrial',
        'authority_score': 65,
        'domain_hint': 'Employment',
    },
    'NSWCATAD': {
        'name': 'NSW Civil and Administrative Tribunal (Admin Div)',
        'level': 'tribunal',
        'jurisdiction': 'NSW',
        'binding': False,
        'authority_score': 35,
        'domain_hint': 'Administrative',
    },
    'NCAT': {
        'name': 'NSW Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'NSW',
        'binding': False,
        'authority_score': 35,
    },

    # --- VICTORIA ---
    'VSCA': {
        'name': 'Victorian Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'VIC',
        'binding': 'vic_courts',
        'authority_score': 85,
    },
    'VSC': {
        'name': 'Victorian Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'VIC',
        'binding': 'lower_vic',
        'authority_score': 75,
    },
    'VCC': {
        'name': 'Victorian County Court',
        'level': 'intermediate',
        'jurisdiction': 'VIC',
        'binding': False,
        'authority_score': 50,
    },
    'VMC': {
        'name': 'Victorian Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'VIC',
        'binding': False,
        'authority_score': 30,
    },
    'VCAT': {
        'name': 'Victorian Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'VIC',
        'binding': False,
        'authority_score': 35,
    },

    # --- QUEENSLAND ---
    'QCA': {
        'name': 'Queensland Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'QLD',
        'binding': 'qld_courts',
        'authority_score': 85,
    },
    'QSC': {
        'name': 'Queensland Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'QLD',
        'binding': 'lower_qld',
        'authority_score': 75,
    },
    'QDC': {
        'name': 'Queensland District Court',
        'level': 'intermediate',
        'jurisdiction': 'QLD',
        'binding': False,
        'authority_score': 50,
    },
    'QMC': {
        'name': 'Queensland Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'QLD',
        'binding': False,
        'authority_score': 30,
    },
    'QCAT': {
        'name': 'Queensland Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'QLD',
        'binding': False,
        'authority_score': 35,
    },
    'ICQ': {
        'name': 'Industrial Court of Queensland',
        'level': 'specialist',
        'jurisdiction': 'QLD',
        'binding': 'qld_industrial',
        'authority_score': 65,
        'domain_hint': 'Employment',
    },

    # --- WESTERN AUSTRALIA ---
    'WASCA': {
        'name': 'WA Supreme Court Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'WA',
        'binding': 'wa_courts',
        'authority_score': 85,
    },
    'WASC': {
        'name': 'WA Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'WA',
        'binding': 'lower_wa',
        'authority_score': 75,
    },
    'WADC': {
        'name': 'WA District Court',
        'level': 'intermediate',
        'jurisdiction': 'WA',
        'binding': False,
        'authority_score': 50,
    },
    'WAMC': {
        'name': 'WA Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'WA',
        'binding': False,
        'authority_score': 30,
    },
    'SAT': {
        'name': 'State Administrative Tribunal (WA)',
        'level': 'tribunal',
        'jurisdiction': 'WA',
        'binding': False,
        'authority_score': 35,
    },
    'WAIRC': {
        'name': 'WA Industrial Relations Commission',
        'level': 'specialist',
        'jurisdiction': 'WA',
        'binding': 'wa_industrial',
        'authority_score': 60,
        'domain_hint': 'Employment',
    },

    # --- SOUTH AUSTRALIA ---
    'SASCFC': {
        'name': 'SA Supreme Court Full Court',
        'level': 'superior_appellate',
        'jurisdiction': 'SA',
        'binding': 'sa_courts',
        'authority_score': 85,
    },
    'SASC': {
        'name': 'SA Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'SA',
        'binding': 'lower_sa',
        'authority_score': 75,
    },
    'SADC': {
        'name': 'SA District Court',
        'level': 'intermediate',
        'jurisdiction': 'SA',
        'binding': False,
        'authority_score': 50,
    },
    'SAMC': {
        'name': 'SA Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'SA',
        'binding': False,
        'authority_score': 30,
    },
    'SACAT': {
        'name': 'SA Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'SA',
        'binding': False,
        'authority_score': 35,
    },
    'SAET': {
        'name': 'SA Employment Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'SA',
        'binding': False,
        'authority_score': 40,
        'domain_hint': 'Employment',
    },

    # --- TASMANIA ---
    'TASCCA': {
        'name': 'Tasmanian Court of Criminal Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'TAS',
        'binding': 'tas_criminal',
        'authority_score': 85,
        'domain_hint': 'Criminal',
    },
    'TASFC': {
        'name': 'Tasmanian Supreme Court Full Court',
        'level': 'superior_appellate',
        'jurisdiction': 'TAS',
        'binding': 'tas_courts',
        'authority_score': 85,
    },
    'TASSC': {
        'name': 'Tasmanian Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'TAS',
        'binding': 'lower_tas',
        'authority_score': 75,
    },
    'TASMC': {
        'name': 'Tasmanian Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'TAS',
        'binding': False,
        'authority_score': 30,
    },
    'TasCAT': {
        'name': 'Tasmanian Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'TAS',
        'binding': False,
        'authority_score': 35,
    },

    # --- ACT ---
    'ACTCA': {
        'name': 'ACT Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'ACT',
        'binding': 'act_courts',
        'authority_score': 85,
    },
    'ACTSC': {
        'name': 'ACT Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'ACT',
        'binding': 'lower_act',
        'authority_score': 75,
    },
    'ACTMC': {
        'name': 'ACT Magistrates Court',
        'level': 'lower',
        'jurisdiction': 'ACT',
        'binding': False,
        'authority_score': 30,
    },
    'ACAT': {
        'name': 'ACT Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'ACT',
        'binding': False,
        'authority_score': 35,
    },

    # --- NORTHERN TERRITORY ---
    'NTCA': {
        'name': 'NT Court of Appeal',
        'level': 'superior_appellate',
        'jurisdiction': 'NT',
        'binding': 'nt_courts',
        'authority_score': 85,
    },
    'NTSC': {
        'name': 'NT Supreme Court',
        'level': 'superior_trial',
        'jurisdiction': 'NT',
        'binding': 'lower_nt',
        'authority_score': 75,
    },
    'NTLC': {
        'name': 'NT Local Court',
        'level': 'lower',
        'jurisdiction': 'NT',
        'binding': False,
        'authority_score': 30,
    },
    'NTCAT': {
        'name': 'NT Civil and Administrative Tribunal',
        'level': 'tribunal',
        'jurisdiction': 'NT',
        'binding': False,
        'authority_score': 35,
    },

    # --- SPECIALIST COURTS/TRIBUNALS ---
    'FWC': {
        'name': 'Fair Work Commission',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 50,
        'domain_hint': 'Employment',
    },
    'FWCFB': {
        'name': 'Fair Work Commission Full Bench',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': 'fwc',
        'authority_score': 60,
        'domain_hint': 'Employment',
    },
    'IRC': {
        'name': 'Industrial Relations Commission',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 50,
        'domain_hint': 'Employment',
    },
    'AIRC': {
        'name': 'Australian Industrial Relations Commission',
        'level': 'tribunal',
        'jurisdiction': 'Commonwealth',
        'binding': False,
        'authority_score': 50,
        'domain_hint': 'Employment',
    },
}


# ============================================================================
# JURISDICTION TO DOMAIN HINTS
# ============================================================================

JURISDICTION_DOMAIN_HINTS = {
    'family': 'Family',
    'industrial': 'Employment',
    'employment': 'Employment',
    'criminal': 'Criminal',
    'land': 'Property',
    'environment': 'Environment',
    'administrative': 'Administrative',
    'migration': 'Administrative',
    'refugee': 'Administrative',
    'taxation': 'Tax',
    'revenue': 'Tax',
}


# ============================================================================
# REPORT SERIES
# ============================================================================

REPORT_SERIES = {
    'CLR': {
        'name': 'Commonwealth Law Reports',
        'jurisdiction': 'Commonwealth',
        'court': 'HCA',
        'authority_score': 100,
    },
    'FCR': {
        'name': 'Federal Court Reports',
        'jurisdiction': 'Commonwealth',
        'court': 'FCA',
        'authority_score': 85,
    },
    'ALR': {
        'name': 'Australian Law Reports',
        'jurisdiction': 'Commonwealth',
        'court': 'Multiple',
        'authority_score': 80,
    },
    'NSWLR': {
        'name': 'NSW Law Reports',
        'jurisdiction': 'NSW',
        'court': 'NSWCA/NSWSC',
        'authority_score': 80,
    },
    'VR': {
        'name': 'Victorian Reports',
        'jurisdiction': 'VIC',
        'court': 'VSCA/VSC',
        'authority_score': 80,
    },
    'QdR': {
        'name': 'Queensland Reports',
        'jurisdiction': 'QLD',
        'court': 'QCA/QSC',
        'authority_score': 80,
    },
    'SASR': {
        'name': 'South Australian State Reports',
        'jurisdiction': 'SA',
        'court': 'SASC',
        'authority_score': 80,
    },
    'WAR': {
        'name': 'Western Australian Reports',
        'jurisdiction': 'WA',
        'court': 'WASC',
        'authority_score': 80,
    },
    'TasR': {
        'name': 'Tasmanian Reports',
        'jurisdiction': 'TAS',
        'court': 'TASSC',
        'authority_score': 80,
    },
    'FLC': {
        'name': 'Family Law Cases',
        'jurisdiction': 'Commonwealth',
        'court': 'FamCA',
        'authority_score': 75,
        'domain_hint': 'Family',
    },
    'FLR': {
        'name': 'Federal Law Reports',
        'jurisdiction': 'Commonwealth',
        'court': 'Multiple',
        'authority_score': 75,
    },
    'ACSR': {
        'name': 'Australian Corporations and Securities Reports',
        'jurisdiction': 'Commonwealth',
        'court': 'Multiple',
        'authority_score': 75,
        'domain_hint': 'Commercial',
    },
    'IR': {
        'name': 'Industrial Reports',
        'jurisdiction': 'Multiple',
        'court': 'IRC/FWC',
        'authority_score': 60,
        'domain_hint': 'Employment',
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_court_info(court_code: str) -> Optional[Dict]:
    """Get court information by code."""
    return COURT_CODES.get(court_code.upper())


def get_hierarchy_level(court_code: str) -> int:
    """Get numeric hierarchy level for a court (1=highest)."""
    info = get_court_info(court_code)
    if info:
        return HIERARCHY_LEVELS.get(info['level'], 10)
    return 10  # Unknown courts get lowest priority


def get_authority_score(court_code: str) -> int:
    """Get authority score for a court (higher = more authoritative)."""
    info = get_court_info(court_code)
    return info.get('authority_score', 0) if info else 0


def get_jurisdiction(court_code: str) -> Optional[str]:
    """Get jurisdiction for a court code."""
    info = get_court_info(court_code)
    return info.get('jurisdiction') if info else None


def get_domain_hint(court_code: str) -> Optional[str]:
    """Get domain hint for a specialist court."""
    info = get_court_info(court_code)
    return info.get('domain_hint') if info else None


def extract_court_from_citation(citation: str) -> Optional[str]:
    """Extract court code from a medium neutral citation."""
    pattern = re.compile(r'\[\d{4}\]\s*([A-Z]{2,10})\s*\d+')
    match = pattern.search(citation)
    if match:
        return match.group(1).upper()
    return None


def is_binding_authority(citing_court: str, cited_court: str) -> bool:
    """
    Determine if a cited court's decision is binding on the citing court.

    Returns True if the cited court binds the citing court.
    """
    cited_info = get_court_info(cited_court)
    citing_info = get_court_info(citing_court)

    if not cited_info or not citing_info:
        return False

    # High Court binds all
    if cited_court.upper() == 'HCA':
        return True

    # Compare hierarchy levels
    cited_level = get_hierarchy_level(cited_court)
    citing_level = get_hierarchy_level(citing_court)

    # Higher court (lower number) generally binds lower court (higher number)
    # But only if same jurisdiction
    if cited_info.get('jurisdiction') == citing_info.get('jurisdiction'):
        return cited_level < citing_level

    return False


def get_report_series_info(series_abbr: str) -> Optional[Dict]:
    """Get information about a report series."""
    return REPORT_SERIES.get(series_abbr.upper())
