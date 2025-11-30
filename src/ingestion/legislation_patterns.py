"""
Legislation Patterns for Corpus Labeling
=========================================
Maps Australian legislation to legal domains for enhanced document classification.

This module contains:
- LEGISLATION_TO_DOMAIN: Maps Act names to primary legal domains
- SECTION_PATTERNS: Regex patterns for extracting section references
- Utility functions for legislation matching
"""

import re
from typing import Dict, List, Tuple, Optional

# ============================================================================
# SECTION REFERENCE PATTERNS
# ============================================================================

# Pattern to match section references like s 79, s 79(4), s 79(4)(a)(i)
SECTION_PATTERN = re.compile(
    r'\b(?:s|sec(?:tion)?)\s*(\d+[A-Za-z]?(?:\(\d+\))?(?:\([a-z]+\))?(?:\([ivx]+\))?)',
    re.IGNORECASE
)

# Pattern to match Part references like Part IV, Part 2, Part VIIA
PART_PATTERN = re.compile(
    r'\bPart\s+([IVXLCDM]+|\d+[A-Z]?)',
    re.IGNORECASE
)

# Pattern to match Division references
DIVISION_PATTERN = re.compile(
    r'\bDivision\s+(\d+[A-Z]?)',
    re.IGNORECASE
)

# Pattern to match Schedule references
SCHEDULE_PATTERN = re.compile(
    r'\bSchedule\s+(\d+[A-Z]?)',
    re.IGNORECASE
)


# ============================================================================
# LEGISLATION TO DOMAIN MAPPING
# ============================================================================

LEGISLATION_TO_DOMAIN = {
    # --- CORPORATIONS AND COMMERCIAL LAW ---
    'Corporations Act 2001': {
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance', 'Corp_Insolvency', 'Securities_Licensing'],
        'key_sections': {
            's180': 'Corp_Governance',  # Duty of care
            's181': 'Corp_Governance',  # Good faith
            's182': 'Corp_Governance',  # Improper use of position
            's183': 'Corp_Governance',  # Improper use of information
            's588G': 'Corp_Insolvency',  # Insolvent trading
            's588GA': 'Corp_Insolvency',  # Safe harbour
            's601ED': 'Securities_Managed_Investments',
            's911A': 'Securities_Licensing',
            's1041A': 'Securities_Market_Misconduct',
        }
    },
    'Corporations Act': {
        'domain': 'Commercial',
        'subcategories': ['Corp_Governance', 'Corp_Insolvency', 'Securities_Licensing'],
    },
    'Australian Securities and Investments Commission Act 2001': {
        'domain': 'Commercial',
        'subcategories': ['Securities_Licensing'],
    },
    'ASIC Act 2001': {
        'domain': 'Commercial',
        'subcategories': ['Securities_Licensing'],
    },

    # --- INSOLVENCY ---
    'Bankruptcy Act 1966': {
        'domain': 'Commercial',
        'subcategories': ['Corp_Insolvency'],
    },
    'Insolvency Practice Rules': {
        'domain': 'Commercial',
        'subcategories': ['Corp_Insolvency'],
    },

    # --- COMPETITION AND CONSUMER ---
    'Competition and Consumer Act 2010': {
        'domain': 'Commercial',
        'subcategories': ['Competition_Cartels', 'Comm_Consumer'],
        'key_sections': {
            's18': 'Comm_Consumer',  # Misleading conduct
            's20': 'Comm_Consumer',  # Unconscionable conduct
            's21': 'Comm_Consumer',  # Unconscionable conduct in trade
            's45': 'Competition_Cartels',  # Cartel conduct
            's46': 'Competition_Market_Power',  # Misuse of market power
            's50': 'Competition_Mergers',  # Mergers
        }
    },
    'Trade Practices Act 1974': {
        'domain': 'Commercial',
        'subcategories': ['Competition_Cartels', 'Comm_Consumer'],
    },
    'Australian Consumer Law': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer'],
    },
    'ACL': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Consumer'],
    },

    # --- BANKING AND FINANCE ---
    'National Consumer Credit Protection Act 2009': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Banking'],
    },
    'NCCP Act': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Banking'],
    },
    'Personal Property Securities Act 2009': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Banking'],
    },
    'PPSA': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Banking'],
    },
    'Banking Act 1959': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Banking'],
    },
    'Insurance Contracts Act 1984': {
        'domain': 'Commercial',
        'subcategories': ['Comm_Insurance'],
    },

    # --- FAMILY LAW ---
    'Family Law Act 1975': {
        'domain': 'Family',
        'subcategories': ['Family_General', 'Family_Children', 'Family_Property'],
        'key_sections': {
            's60B': 'Family_Children',  # Objects
            's61DA': 'Family_Children',  # Equal shared parental responsibility
            's79': 'Family_Property',  # Property orders
            's72': 'Family_Maintenance',  # Spousal maintenance
            's90B': 'Family_Property',  # Financial agreements before marriage
            's90C': 'Family_Property',  # Financial agreements during marriage
        }
    },
    'Family Law Act': {
        'domain': 'Family',
        'subcategories': ['Family_General'],
    },
    'Child Support (Assessment) Act 1989': {
        'domain': 'Family',
        'subcategories': ['Family_Children'],
    },

    # --- EMPLOYMENT LAW ---
    'Fair Work Act 2009': {
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal', 'Emp_General_Protections'],
        'key_sections': {
            's394': 'Emp_Unfair_Dismissal',  # Unfair dismissal application
            's385': 'Emp_Unfair_Dismissal',  # What is unfair dismissal
            's340': 'Emp_General_Protections',  # General protections
            's351': 'Emp_General_Protections',  # Discrimination
        }
    },
    'Fair Work Act': {
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
    },
    'Work Health and Safety Act 2011': {
        'domain': 'Employment',
        'subcategories': ['Emp_WHS'],
    },
    'WHS Act': {
        'domain': 'Employment',
        'subcategories': ['Emp_WHS'],
    },
    'Workers Compensation Act': {
        'domain': 'Employment',
        'subcategories': ['Emp_Workers_Comp'],
    },
    'Long Service Leave Act': {
        'domain': 'Employment',
        'subcategories': ['Emp_Leave'],
    },

    # --- ADMINISTRATIVE LAW ---
    'Administrative Decisions (Judicial Review) Act 1977': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
    },
    'ADJR Act': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
    },
    'Administrative Appeals Tribunal Act 1975': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
    },
    'AAT Act': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
    },
    'Judiciary Act 1903': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Review'],
        'key_sections': {
            's39B': 'Admin_Review',  # Constitutional writs
        }
    },
    'Freedom of Information Act 1982': {
        'domain': 'Administrative',
        'subcategories': ['Admin_FOI'],
    },
    'FOI Act': {
        'domain': 'Administrative',
        'subcategories': ['Admin_FOI'],
    },
    'Privacy Act 1988': {
        'domain': 'Administrative',
        'subcategories': ['Privacy_Data'],
    },
    'Migration Act 1958': {
        'domain': 'Administrative',
        'subcategories': ['Admin_Migration'],
    },

    # --- TAX LAW ---
    'Income Tax Assessment Act 1997': {
        'domain': 'Tax',
        'subcategories': ['Tax_Income'],
    },
    'ITAA 1997': {
        'domain': 'Tax',
        'subcategories': ['Tax_Income'],
    },
    'Income Tax Assessment Act 1936': {
        'domain': 'Tax',
        'subcategories': ['Tax_Income'],
    },
    'ITAA 1936': {
        'domain': 'Tax',
        'subcategories': ['Tax_Income'],
    },
    'A New Tax System (Goods and Services Tax) Act 1999': {
        'domain': 'Tax',
        'subcategories': ['Tax_GST'],
    },
    'GST Act': {
        'domain': 'Tax',
        'subcategories': ['Tax_GST'],
    },
    'Fringe Benefits Tax Assessment Act 1986': {
        'domain': 'Tax',
        'subcategories': ['Tax_FBT'],
    },
    'FBT Act': {
        'domain': 'Tax',
        'subcategories': ['Tax_FBT'],
    },
    'Taxation Administration Act 1953': {
        'domain': 'Tax',
        'subcategories': ['Tax_Admin'],
    },
    'Superannuation Industry (Supervision) Act 1993': {
        'domain': 'Tax',
        'subcategories': ['Tax_Super'],
    },
    'SIS Act': {
        'domain': 'Tax',
        'subcategories': ['Tax_Super'],
    },

    # --- CRIMINAL LAW ---
    'Criminal Code Act 1995': {
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
    },
    'Criminal Code': {
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
    },
    'Crimes Act 1914': {
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
    },
    'Crimes Act 1900': {
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
    },
    'Criminal Procedure Act': {
        'domain': 'Criminal',
        'subcategories': ['Crim_Procedure'],
    },
    'Bail Act': {
        'domain': 'Criminal',
        'subcategories': ['Crim_Bail'],
    },
    'Sentencing Act': {
        'domain': 'Criminal',
        'subcategories': ['Crim_Sentencing'],
    },
    'Drug Misuse and Trafficking Act': {
        'domain': 'Criminal',
        'subcategories': ['Crim_Drugs'],
    },
    'Proceeds of Crime Act 2002': {
        'domain': 'Criminal',
        'subcategories': ['Crim_General'],
    },

    # --- PROPERTY LAW ---
    'Real Property Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Real'],
    },
    'Conveyancing Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Real'],
    },
    'Transfer of Land Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Real'],
    },
    'Strata Schemes Management Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Strata'],
    },
    'Residential Tenancies Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Tenancies'],
    },
    'Retail Leases Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Tenancies'],
    },
    'Land Acquisition Act': {
        'domain': 'Property',
        'subcategories': ['Prop_Acquisition'],
    },

    # --- TORTS ---
    'Civil Liability Act': {
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
    },
    'Motor Accidents Compensation Act': {
        'domain': 'Torts',
        'subcategories': ['Tort_Motor'],
    },
    'Defamation Act': {
        'domain': 'Torts',
        'subcategories': ['Tort_Defamation'],
    },
    'Compensation to Relatives Act': {
        'domain': 'Torts',
        'subcategories': ['Tort_Negligence'],
    },

    # --- EQUITY AND TRUSTS ---
    'Trustee Act': {
        'domain': 'Equity',
        'subcategories': ['Equity_Trusts'],
    },
    'Succession Act': {
        'domain': 'Equity',
        'subcategories': ['Equity_Succession'],
    },
    'Wills Act': {
        'domain': 'Equity',
        'subcategories': ['Equity_Succession'],
    },
    'Powers of Attorney Act': {
        'domain': 'Equity',
        'subcategories': ['Equity_Succession'],
    },
    'Guardianship Act': {
        'domain': 'Equity',
        'subcategories': ['Equity_Succession'],
    },

    # --- EVIDENCE AND PROCEDURE ---
    'Evidence Act 1995': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Evidence'],
    },
    'Evidence Act': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Evidence'],
    },
    'Civil Procedure Act': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'Uniform Civil Procedure Rules': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'UCPR': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'Supreme Court Rules': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'Federal Court Rules': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'High Court Rules': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Civil'],
    },
    'Limitation Act': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Limitation'],
    },
    'Limitations of Actions Act': {
        'domain': 'Procedure',
        'subcategories': ['Proc_Limitation'],
    },

    # --- CONSTITUTIONAL LAW ---
    'Constitution': {
        'domain': 'Constitutional',
        'subcategories': ['Const_Chapter_I'],
        'key_sections': {
            's51': 'Const_Chapter_I',  # Legislative powers
            's71': 'Const_Chapter_III',  # Judicial power
            's75': 'Const_Chapter_III',  # Original jurisdiction
            's76': 'Const_Chapter_III',  # Additional original jurisdiction
            's109': 'Const_Chapter_V',  # Inconsistency
            's128': 'Const_Chapter_VIII',  # Referendum
        }
    },
    'Australia Act 1986': {
        'domain': 'Constitutional',
        'subcategories': ['Const_Federation'],
    },
    'Statute of Westminster': {
        'domain': 'Constitutional',
        'subcategories': ['Const_Federation'],
    },

    # --- INTELLECTUAL PROPERTY ---
    'Patents Act 1990': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Patents'],
    },
    'Trade Marks Act 1995': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Trademarks'],
    },
    'Copyright Act 1968': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Copyright'],
    },
    'Designs Act 2003': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Designs'],
    },
    'Plant Breeder\'s Rights Act 1994': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Plant_Breeders'],
    },
    'Circuit Layouts Act 1989': {
        'domain': 'Intellectual_Property',
        'subcategories': ['IP_Circuits'],
    },

    # --- RESOURCES AND ENERGY ---
    'Petroleum and Gas Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Petroleum'],
    },
    'Mining Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Mining'],
    },
    'Mineral Resources Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Mining'],
    },
    'Water Act 2007': {
        'domain': 'Resources',
        'subcategories': ['Resources_Water'],
    },
    'Water Management Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Water'],
    },
    'National Electricity Law': {
        'domain': 'Resources',
        'subcategories': ['Resources_Energy'],
    },
    'NEL': {
        'domain': 'Resources',
        'subcategories': ['Resources_Energy'],
    },
    'National Gas Law': {
        'domain': 'Resources',
        'subcategories': ['Resources_Energy'],
    },
    'NGL': {
        'domain': 'Resources',
        'subcategories': ['Resources_Energy'],
    },
    'Renewable Energy (Electricity) Act 2000': {
        'domain': 'Resources',
        'subcategories': ['Resources_Energy'],
    },
    'Telecommunications Act 1997': {
        'domain': 'Resources',
        'subcategories': ['Resources_Telecom'],
    },
    'Broadcasting Services Act 1992': {
        'domain': 'Resources',
        'subcategories': ['Resources_Broadcasting'],
    },
    'Building and Construction Industry Security of Payment Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Construction'],
    },
    'Security of Payment Act': {
        'domain': 'Resources',
        'subcategories': ['Resources_Construction'],
    },
    'Heavy Vehicle National Law': {
        'domain': 'Resources',
        'subcategories': ['Resources_Transport'],
    },
    'Civil Aviation Act 1988': {
        'domain': 'Resources',
        'subcategories': ['Resources_Aviation'],
    },
    'Navigation Act 2012': {
        'domain': 'Resources',
        'subcategories': ['Resources_Maritime'],
    },
    'Admiralty Act 1988': {
        'domain': 'Resources',
        'subcategories': ['Resources_Maritime'],
    },

    # --- ENVIRONMENT ---
    'Environment Protection and Biodiversity Conservation Act 1999': {
        'domain': 'Environment',
        'subcategories': ['Env_EPBC'],
    },
    'EPBC Act': {
        'domain': 'Environment',
        'subcategories': ['Env_EPBC'],
    },
    'Environmental Planning and Assessment Act': {
        'domain': 'Environment',
        'subcategories': ['Env_Planning'],
    },
    'Protection of the Environment Operations Act': {
        'domain': 'Environment',
        'subcategories': ['Env_Pollution'],
    },
    'Native Title Act 1993': {
        'domain': 'Environment',
        'subcategories': ['Env_Native_Title'],
    },

    # --- HEALTH AND MEDICAL ---
    'Health Practitioner Regulation National Law': {
        'domain': 'Health',
        'subcategories': ['Health_Practitioner'],
    },
    'Therapeutic Goods Act 1989': {
        'domain': 'Health',
        'subcategories': ['Health_Therapeutic_Goods'],
    },
    'Mental Health Act': {
        'domain': 'Health',
        'subcategories': ['Health_Mental'],
    },
    'Public Health Act': {
        'domain': 'Health',
        'subcategories': ['Health_Public'],
    },
    'Aged Care Act 1997': {
        'domain': 'Health',
        'subcategories': ['Health_Aged_Care'],
    },
    'National Disability Insurance Scheme Act 2013': {
        'domain': 'Health',
        'subcategories': ['Health_Aged_Care'],
    },
    'NDIS Act': {
        'domain': 'Health',
        'subcategories': ['Health_Aged_Care'],
    },

    # --- DISCRIMINATION ---
    'Sex Discrimination Act 1984': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Racial Discrimination Act 1975': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Disability Discrimination Act 1992': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Age Discrimination Act 2004': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Australian Human Rights Commission Act 1986': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Anti-Discrimination Act': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },
    'Equal Opportunity Act': {
        'domain': 'Human_Rights',
        'subcategories': ['HR_Discrimination'],
    },

    # --- SPORTS LAW ---
    'Australian Sports Anti-Doping Authority Act 2006': {
        'domain': 'Sports',
        'subcategories': ['Sports_Anti_Doping'],
    },
    'Interactive Gambling Act 2001': {
        'domain': 'Sports',
        'subcategories': ['Sports_Integrity'],
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_legislation_refs(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract legislation references from text.

    Returns:
        List of (act_name, section, domain) tuples
    """
    results = []
    text_lower = text.lower()

    for act_name, info in LEGISLATION_TO_DOMAIN.items():
        if act_name.lower() in text_lower:
            domain = info['domain']

            # Find section references near the act name
            sections = SECTION_PATTERN.findall(text)
            if sections:
                for section in sections[:10]:  # Limit to first 10
                    results.append((act_name, f"s{section}", domain))
            else:
                results.append((act_name, '', domain))

    return results


def get_domain_for_legislation(act_name: str) -> Optional[str]:
    """Get the primary domain for a legislation name."""
    for name, info in LEGISLATION_TO_DOMAIN.items():
        if name.lower() in act_name.lower() or act_name.lower() in name.lower():
            return info['domain']
    return None


def get_subcategories_for_section(act_name: str, section: str) -> List[str]:
    """Get subcategories for a specific section of an Act."""
    for name, info in LEGISLATION_TO_DOMAIN.items():
        if name.lower() in act_name.lower():
            if 'key_sections' in info and section in info['key_sections']:
                return [info['key_sections'][section]]
            return info.get('subcategories', [])
    return []


# Compile patterns for fast matching
LEGISLATION_PATTERNS = {}
for act_name in LEGISLATION_TO_DOMAIN.keys():
    pattern = re.compile(re.escape(act_name), re.IGNORECASE)
    LEGISLATION_PATTERNS[act_name] = pattern
