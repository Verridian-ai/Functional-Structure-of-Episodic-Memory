"""
Legal Authority Configuration
=============================

Defines the hierarchy and weighting of legal authorities in the Australian jurisdiction.
Used for scoring case relevance and precedence.
"""

from typing import Dict, TypedDict

class AuthorityConfig(TypedDict):
    weight: int
    name: str
    abbreviations: list[str]

# Hierarchy weights for Australian courts (Higher = More Authoritative)
COURT_HIERARCHY: Dict[str, AuthorityConfig] = {
    'HCA': { 'weight': 10, 'name': 'High Court of Australia', 'abbreviations': ['HCA', 'High Court'] },
    'FCAFC': { 'weight': 9, 'name': 'Federal Court Full Court', 'abbreviations': ['FCAFC'] },
    'FamCAFC': { 'weight': 8, 'name': 'Family Court Full Court', 'abbreviations': ['FamCAFC', 'FCAFC (Family)'] },
    'NSWCA': { 'weight': 8, 'name': 'NSW Court of Appeal', 'abbreviations': ['NSWCA'] },
    'VSCA': { 'weight': 8, 'name': 'Victorian Court of Appeal', 'abbreviations': ['VSCA'] },
    'QCA': { 'weight': 8, 'name': 'Queensland Court of Appeal', 'abbreviations': ['QCA'] },
    'FCA': { 'weight': 7, 'name': 'Federal Court of Australia', 'abbreviations': ['FCA'] },
    'FamCA': { 'weight': 6, 'name': 'Family Court of Australia', 'abbreviations': ['FamCA'] },
    'NSWSC': { 'weight': 6, 'name': 'NSW Supreme Court', 'abbreviations': ['NSWSC'] },
    'VSC': { 'weight': 6, 'name': 'Supreme Court of Victoria', 'abbreviations': ['VSC'] },
    'QSC': { 'weight': 6, 'name': 'Supreme Court of Queensland', 'abbreviations': ['QSC'] },
    'SASC': { 'weight': 6, 'name': 'Supreme Court of SA', 'abbreviations': ['SASC'] },
    'WASC': { 'weight': 6, 'name': 'Supreme Court of WA', 'abbreviations': ['WASC'] },
    'ACTSC': { 'weight': 6, 'name': 'Supreme Court of ACT', 'abbreviations': ['ACTSC'] },
    'NTSC': { 'weight': 6, 'name': 'Supreme Court of NT', 'abbreviations': ['NTSC'] },
    'TasSC': { 'weight': 6, 'name': 'Supreme Court of Tasmania', 'abbreviations': ['TasSC'] },
    'FCCA': { 'weight': 5, 'name': 'Federal Circuit Court', 'abbreviations': ['FCCA', 'FedCirFam'] },
    'NSWDC': { 'weight': 4, 'name': 'District Court of NSW', 'abbreviations': ['NSWDC'] },
    'VCC': { 'weight': 4, 'name': 'County Court of Victoria', 'abbreviations': ['VCC'] },
    'QDC': { 'weight': 4, 'name': 'District Court of Queensland', 'abbreviations': ['QDC'] },
    'AAT': { 'weight': 2, 'name': 'Administrative Appeals Tribunal', 'abbreviations': ['AAT'] },
    'Tribunal': { 'weight': 2, 'name': 'Administrative Tribunal', 'abbreviations': ['Tribunal', 'VCAT', 'NCAT', 'QCAT'] },
}

def get_authority_score(citation: str) -> float:
    """
    Calculates an authority boost score based on the citation's court.
    Returns a multiplier (e.g., 1.0 to 1.5).
    """
    import re
    
    # Extract court identifier from citation [YYYY] COURT ###
    court_match = re.search(r'\[\d{4}\]\s*(\w+)\s*\d+', citation)
    if not court_match:
        return 1.0
        
    court_code = court_match.group(1)
    
    # Direct lookup
    if court_code in COURT_HIERARCHY:
        weight = COURT_HIERARCHY[court_code]['weight']
        return 1 + (weight / 20.0) # Max boost 1.5x
        
    # Uppercase lookup
    if court_code.upper() in COURT_HIERARCHY:
        weight = COURT_HIERARCHY[court_code.upper()]['weight']
        return 1 + (weight / 20.0)
        
    return 1.0

