"""
Case Law Patterns for Corpus Labeling
=====================================
Maps landmark Australian cases to legal domains for enhanced document classification.

This module contains:
- LANDMARK_CASES: Dictionary of important cases mapped to domains
- Citation patterns for extracting case references
- Utility functions for case law matching
"""

import re
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CITATION PATTERNS
# ============================================================================

# Medium Neutral Citation: [2020] HCA 1, [2023] FCAFC 156
MEDIUM_NEUTRAL_PATTERN = re.compile(
    r'\[(\d{4})\]\s*([A-Z]{2,10})\s*(\d+)',
    re.IGNORECASE
)

# Authorized Report: (2020) 271 CLR 657, [2020] 1 AC 432
AUTHORIZED_REPORT_PATTERN = re.compile(
    r'\((\d{4})\)\s+(\d+)\s+([A-Z]{2,6})\s+(\d+)',
    re.IGNORECASE
)

# Case name pattern: Smith v Jones, R v Brown, ASIC v Healey
CASE_NAME_PATTERN = re.compile(
    r'([A-Z][a-zA-Z\'\-]+(?:\s+[A-Z][a-zA-Z\'\-]+)*)\s+v\s+([A-Z][a-zA-Z\'\-]+(?:\s+[A-Z][a-zA-Z\'\-]+)*)',
    re.IGNORECASE
)


# ============================================================================
# LANDMARK CASES MAPPED TO DOMAINS
# ============================================================================

LANDMARK_CASES = {
    # --- ADMINISTRATIVE LAW ---
    'Craig v South Australia': {
        'citation': '(1995) 184 CLR 163',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['jurisdictional error', 'judicial review'],
    },
    'Kirk v Industrial Court (NSW)': {
        'citation': '(2010) 239 CLR 531',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['constitutional minimum', 'supervisory jurisdiction'],
    },
    'Minister for Immigration v Li': {
        'citation': '(2013) 249 CLR 332',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review', 'Admin_Migration'],
        'keywords': ['legal unreasonableness', 'irrationality'],
    },
    'Kioa v West': {
        'citation': '(1985) 159 CLR 550',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['natural justice', 'procedural fairness'],
    },
    'SZBEL v Minister for Immigration': {
        'citation': '(2006) 228 CLR 152',
        'domain': 'Administrative',
        'subcategories': ['Admin_Migration'],
        'keywords': ['procedural fairness', 'migration'],
    },
    'Plaintiff M70 v Minister for Immigration': {
        'citation': '(2011) 244 CLR 144',
        'domain': 'Administrative',
        'subcategories': ['Admin_Migration'],
        'keywords': ['offshore processing', 'refugees'],
    },
    'Plaintiff S157 v Commonwealth': {
        'citation': '(2003) 211 CLR 476',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['privative clause', 'jurisdictional error'],
    },
    'Project Blue Sky v ABA': {
        'citation': '(1998) 194 CLR 355',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['statutory interpretation', 'validity'],
    },
    'Ebner v Official Trustee': {
        'citation': '(2000) 205 CLR 337',
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'keywords': ['apprehended bias', 'disqualification'],
    },

    # --- CONSTITUTIONAL LAW ---
    'Amalgamated Society of Engineers v Adelaide Steamship': {
        'citation': '(1920) 28 CLR 129',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'keywords': ['engineers case', 'implied immunities'],
    },
    'Commonwealth v Tasmania': {
        'citation': '(1983) 158 CLR 1',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'keywords': ['tasmanian dam', 'external affairs'],
    },
    'Australian Capital Television v Commonwealth': {
        'citation': '(1992) 177 CLR 106',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_III'],
        'keywords': ['implied freedom', 'political communication'],
    },
    'Lange v ABC': {
        'citation': '(1997) 189 CLR 520',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_III'],
        'keywords': ['implied freedom', 'qualified privilege'],
    },
    'Kable v DPP (NSW)': {
        'citation': '(1996) 189 CLR 51',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_III'],
        'keywords': ['kable doctrine', 'state courts'],
    },
    'Roach v Electoral Commissioner': {
        'citation': '(2007) 233 CLR 162',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'keywords': ['prisoner voting', 'representative democracy'],
    },
    'Pape v Commissioner of Taxation': {
        'citation': '(2009) 238 CLR 1',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'keywords': ['appropriation', 'executive power'],
    },
    'Williams v Commonwealth': {
        'citation': '(2012) 248 CLR 156',
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'keywords': ['school chaplains', 'appropriation'],
    },

    # --- CORPORATIONS LAW ---
    'ASIC v Healey': {
        'citation': '(2011) 196 FCR 291',
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance'],
        'keywords': ['directors duties', 'centro', 'financial literacy'],
    },
    'ASIC v Adler': {
        'citation': '(2002) 168 FLR 253',
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance'],
        'keywords': ['directors duties', 'hih', 'breach of duty'],
    },
    'Bell Group v Westpac': {
        'citation': '(2008) WASC 239',
        'domain': 'Commercial',
        'subcategories': ['Corp_Insolvency'],
        'keywords': ['bell group', 'insolvency', 'subordination'],
    },
    'ASIC v Rich': {
        'citation': '(2009) 75 ACSR 1',
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance'],
        'keywords': ['one.tel', 'directors duties'],
    },
    'Vrisakis v Australian Securities Commission': {
        'citation': '(1993) 9 WAR 395',
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance'],
        'keywords': ['directors duties', 'continuous disclosure'],
    },
    'Re HIH Insurance': {
        'citation': '(2002) 42 ACSR 303',
        'domain': 'Commercial',
        'subcategories': ['Corp_Insolvency'],
        'keywords': ['hih', 'liquidation', 'winding up'],
    },

    # --- COMPETITION LAW ---
    'Queensland Wire v BHP': {
        'citation': '(1989) 167 CLR 177',
        'domain': 'Commercial',
        'subcategories': ['Competition_Market_Power'],
        'keywords': ['misuse of market power', 's46'],
    },
    'Rural Press v ACCC': {
        'citation': '(2003) 216 CLR 53',
        'domain': 'Commercial',
        'subcategories': ['Competition_Cartels'],
        'keywords': ['cartel', 'market sharing'],
    },
    'Boral v ACCC': {
        'citation': '(2003) 215 CLR 374',
        'domain': 'Commercial',
        'subcategories': ['Competition_Market_Power'],
        'keywords': ['predatory pricing', 'market power'],
    },
    'Flight Centre v ACCC': {
        'citation': '(2016) 244 FCR 450',
        'domain': 'Commercial',
        'subcategories': ['Competition_Cartels'],
        'keywords': ['price fixing', 'agency'],
    },
    'ACCC v Coles': {
        'citation': '(2014) 317 ALR 73',
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer', 'Competition_Cartels'],
        'keywords': ['unconscionable conduct', 'suppliers'],
    },

    # --- CONSUMER LAW ---
    'Parkdale v Puxu': {
        'citation': '(1982) 149 CLR 191',
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer'],
        'keywords': ['misleading conduct', 'passing off'],
    },
    'Google v ACCC': {
        'citation': '(2013) 249 CLR 435',
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer'],
        'keywords': ['misleading conduct', 'sponsored links'],
    },
    'ACCC v TPG': {
        'citation': '(2013) 250 CLR 640',
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer'],
        'keywords': ['misleading conduct', 'advertising'],
    },
    'Commercial Bank of Australia v Amadio': {
        'citation': '(1983) 151 CLR 447',
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer', 'Equity_Trusts'],
        'keywords': ['unconscionable conduct', 'special disadvantage'],
    },

    # --- CONTRACT LAW ---
    'Codelfa Construction v State Rail': {
        'citation': '(1982) 149 CLR 337',
        'domain': 'Commercial',
        'subcategories': ['Comm_Contract'],
        'keywords': ['implied terms', 'business efficacy'],
    },
    'BP Refinery v Hastings': {
        'citation': '(1977) 180 CLR 266',
        'domain': 'Commercial',
        'subcategories': ['Comm_Contract'],
        'keywords': ['implied terms', 'five criteria'],
    },
    'Waltons Stores v Maher': {
        'citation': '(1988) 164 CLR 387',
        'domain': 'Commercial',
        'subcategories': ['Comm_Contract', 'Equity_Trusts'],
        'keywords': ['promissory estoppel', 'unconscionable'],
    },
    'Toll v Alphapharm': {
        'citation': '(2004) 219 CLR 165',
        'domain': 'Commercial',
        'subcategories': ['Comm_Contract'],
        'keywords': ['exclusion clause', 'incorporation'],
    },
    'Ermogenous v Greek Orthodox Community': {
        'citation': '(2002) 209 CLR 95',
        'domain': 'Commercial',
        'subcategories': ['Comm_Contract'],
        'keywords': ['intention', 'legal relations'],
    },

    # --- TORTS ---
    'Donoghue v Stevenson': {
        'citation': '[1932] AC 562',
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
        'keywords': ['duty of care', 'neighbour principle'],
    },
    'Perre v Apand': {
        'citation': '(1999) 198 CLR 180',
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
        'keywords': ['pure economic loss', 'duty of care'],
    },
    'Sullivan v Moody': {
        'citation': '(2001) 207 CLR 562',
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
        'keywords': ['duty of care', 'public authority'],
    },
    'Tame v New South Wales': {
        'citation': '(2002) 211 CLR 317',
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
        'keywords': ['psychiatric injury', 'nervous shock'],
    },
    'Rogers v Whitaker': {
        'citation': '(1992) 175 CLR 479',
        'domain': 'Torts',
        'subcategories': ['Tort_Medical'],
        'keywords': ['medical negligence', 'informed consent'],
    },
    'Cattanach v Melchior': {
        'citation': '(2003) 215 CLR 1',
        'domain': 'Torts',
        'subcategories': ['Tort_Medical'],
        'keywords': ['wrongful birth', 'damages'],
    },
    'Ipp v Rosniak': {
        'citation': '(1997) 188 CLR 418',
        'domain': 'Torts',
        'subcategories': ['Tort_Defamation'],
        'keywords': ['defamation', 'qualified privilege'],
    },

    # --- FAMILY LAW ---
    'Stanford v Stanford': {
        'citation': '(2012) 247 CLR 108',
        'domain': 'Family',
        'subcategories': ['Family_Property'],
        'keywords': ['property settlement', 's79', 'just and equitable'],
    },
    'Mallet v Mallet': {
        'citation': '(1984) 156 CLR 605',
        'domain': 'Family',
        'subcategories': ['Family_Property'],
        'keywords': ['property settlement', 'contributions'],
    },
    'Rice v Asplund': {
        'citation': '(1979) FLC 90-725',
        'domain': 'Family',
        'subcategories': ['Family_Children'],
        'keywords': ['parenting', 'best interests'],
    },
    'U v U': {
        'citation': '(2002) 211 CLR 238',
        'domain': 'Family',
        'subcategories': ['Family_Children'],
        'keywords': ['relocation', 'parenting orders'],
    },
    'Goode v Goode': {
        'citation': '(2006) FLC 93-286',
        'domain': 'Family',
        'subcategories': ['Family_Children'],
        'keywords': ['equal shared parental responsibility'],
    },

    # --- EMPLOYMENT LAW ---
    'Byrne v Australian Airlines': {
        'citation': '(1995) 185 CLR 410',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['unfair dismissal', 'reinstatement'],
    },
    'Barclay v Board of Bendigo Hospital': {
        'citation': '(2012) 248 CLR 500',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['adverse action', 'workplace rights'],
    },
    'Construction Forestry v BHP Coal': {
        'citation': '(2014) 253 CLR 243',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['industrial action', 'protected action'],
    },
    'Commonwealth Bank v Barker': {
        'citation': '(2014) 253 CLR 169',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['implied term', 'good faith'],
    },

    # --- CRIMINAL LAW ---
    'R v Baden-Clay': {
        'citation': '(2016) 258 CLR 308',
        'domain': 'Criminal',
        'subcategories': ['Crim_Homicide'],
        'keywords': ['murder', 'manslaughter', 'unreasonable verdict'],
    },
    'R v Tang': {
        'citation': '(2008) 237 CLR 1',
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
        'keywords': ['slavery', 'servitude'],
    },
    'Patel v The Queen': {
        'citation': '(2012) 247 CLR 531',
        'domain': 'Criminal',
        'subcategories': ['Crim_Homicide'],
        'keywords': ['manslaughter', 'criminal negligence'],
    },
    'The Queen v Falconer': {
        'citation': '(1990) 171 CLR 30',
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
        'keywords': ['automatism', 'dissociation'],
    },
    'R v Runjanjic': {
        'citation': '(1991) 56 SASR 114',
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
        'keywords': ['battered woman syndrome', 'self defence'],
    },

    # --- EQUITY ---
    'Hospital Products v United States Surgical': {
        'citation': '(1984) 156 CLR 41',
        'domain': 'Equity',
        'subcategories': ['Equity_Trusts'],
        'keywords': ['fiduciary duty', 'breach of fiduciary'],
    },
    'Chan v Cresdon': {
        'citation': '(1989) 168 CLR 242',
        'domain': 'Equity',
        'subcategories': ['Equity_Trusts'],
        'keywords': ['fiduciary duty', 'conflict of interest'],
    },
    'Baumgartner v Baumgartner': {
        'citation': '(1987) 164 CLR 137',
        'domain': 'Equity',
        'subcategories': ['Equity_Trusts'],
        'keywords': ['constructive trust', 'de facto'],
    },
    'Muschinski v Dodds': {
        'citation': '(1985) 160 CLR 583',
        'domain': 'Equity',
        'subcategories': ['Equity_Trusts'],
        'keywords': ['constructive trust', 'joint endeavour'],
    },

    # --- PROPERTY LAW ---
    'Mabo v Queensland (No 2)': {
        'citation': '(1992) 175 CLR 1',
        'domain': 'Property',
        'subcategories': ['Prop_Native_Title'],
        'keywords': ['native title', 'terra nullius'],
    },
    'Wik v Queensland': {
        'citation': '(1996) 187 CLR 1',
        'domain': 'Property',
        'subcategories': ['Prop_Native_Title'],
        'keywords': ['native title', 'pastoral leases'],
    },
    'Breskvar v Wall': {
        'citation': '(1971) 126 CLR 376',
        'domain': 'Property',
        'subcategories': ['Prop_Real'],
        'keywords': ['torrens title', 'indefeasibility'],
    },
    'Frazer v Walker': {
        'citation': '[1967] 1 AC 569',
        'domain': 'Property',
        'subcategories': ['Prop_Real'],
        'keywords': ['indefeasibility', 'immediate'],
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_case_citations(text: str) -> List[Dict]:
    """
    Extract case citations from text.

    Returns:
        List of dicts with citation info
    """
    results = []

    # Find medium neutral citations
    for match in MEDIUM_NEUTRAL_PATTERN.finditer(text):
        year, court, number = match.groups()
        results.append({
            'citation': match.group(0),
            'year': year,
            'court': court,
            'number': number,
            'type': 'medium_neutral'
        })

    # Find authorized report citations
    for match in AUTHORIZED_REPORT_PATTERN.finditer(text):
        year, volume, report, page = match.groups()
        results.append({
            'citation': match.group(0),
            'year': year,
            'volume': volume,
            'report': report,
            'page': page,
            'type': 'authorized_report'
        })

    return results


def match_landmark_case(text: str) -> List[Tuple[str, str, List[str]]]:
    """
    Match landmark cases in text.

    Returns:
        List of (case_name, domain, subcategories) tuples
    """
    results = []
    text_lower = text.lower()

    for case_name, info in LANDMARK_CASES.items():
        if case_name.lower() in text_lower:
            results.append((case_name, info['domain'], info['subcategories']))

    return results


def get_domain_for_case(case_name: str) -> Optional[str]:
    """Get the domain for a landmark case."""
    for name, info in LANDMARK_CASES.items():
        if name.lower() in case_name.lower() or case_name.lower() in name.lower():
            return info['domain']
    return None


# Compile case name patterns for fast matching
CASE_NAME_PATTERNS = {}
for case_name in LANDMARK_CASES.keys():
    pattern = re.compile(re.escape(case_name), re.IGNORECASE)
    CASE_NAME_PATTERNS[case_name] = pattern
