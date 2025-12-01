"""
Keyword Integration Script
==========================
Extracts keywords from all dictionary files and integrates them into classification_config.py

Usage:
    python scripts/integrate_keywords.py

This script:
1. Reads all Python dictionary files with extracted keywords
2. Normalizes and deduplicates keywords
3. Maps keywords to existing or new categories
4. Updates classification_config.py with new keywords and categories
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Add parent to path for imports
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))


# ============================================================================
# KEYWORD EXTRACTION FUNCTIONS
# ============================================================================

def normalize_keyword(kw: str) -> str:
    """Normalize a keyword to lowercase, strip whitespace."""
    # Remove section references in parentheses for cleaner matching
    # e.g., "duty of care and diligence (s180)" -> "duty of care and diligence"
    kw = re.sub(r'\s*\([^)]*\)\s*$', '', kw)
    return kw.strip().lower()


def extract_keywords_from_dict(data: dict, prefix: str = "") -> Dict[str, List[str]]:
    """
    Recursively extract keywords from nested dictionary structures.
    Returns dict of {category_name: [keywords]}
    """
    results = {}

    for key, value in data.items():
        current_key = f"{prefix}_{key}" if prefix else key

        if isinstance(value, dict):
            # Check if this level has keywords
            if "keywords" in value:
                keywords = value["keywords"]
                if isinstance(keywords, list):
                    results[current_key] = [normalize_keyword(k) for k in keywords]

            # Check for subcategories
            if "subcategories" in value:
                sub_results = extract_keywords_from_dict(value["subcategories"], current_key)
                results.update(sub_results)

            # Recursively check nested dicts (for structures like IP -> PATENTS)
            for sub_key, sub_value in value.items():
                if sub_key not in ["keywords", "legislation", "regulators", "tribunals_and_boards",
                                   "tribunals_bodies", "landmark_cases", "description", "domain_code",
                                   "subcategories"]:
                    if isinstance(sub_value, dict):
                        sub_results = extract_keywords_from_dict({sub_key: sub_value}, current_key)
                        results.update(sub_results)

    return results


def load_dictionary_file(filepath: Path) -> dict:
    """Load a Python dictionary file and extract the main dictionary."""
    content = filepath.read_text(encoding='utf-8')

    # Extract variable assignments
    # Match patterns like: VARIABLE_NAME = { ... }
    local_vars = {}
    try:
        exec(content, {"__builtins__": {}}, local_vars)
    except Exception as e:
        print(f"  [Warning] Could not exec {filepath.name}: {e}")
        return {}

    # Return the first dict found
    for var_name, var_value in local_vars.items():
        if isinstance(var_value, dict) and not var_name.startswith('_'):
            return var_value

    return {}


# ============================================================================
# CATEGORY MAPPING
# ============================================================================

# Map extracted categories to CLASSIFICATION_MAP categories
CATEGORY_MAPPING = {
    # Health/Medical -> New categories
    "Health_Practitioner_Regulation": "Health_Practitioner",
    "Mental_Health_Law": "Health_Mental",
    "Therapeutic_Goods": "Health_Therapeutic_Goods",
    "Private_Health_Hospital": "Health_Private",
    "Public_Health_Communicable": "Health_Public",
    "Aged_Care_NDIS": "Health_Aged_Care",
    "Reproductive_Health": "Health_Reproductive",
    "Food_Standards_Safety": "Health_Food_Safety",

    # IP -> Enhanced categories
    "INTELLECTUAL_PROPERTY_PATENTS": "IP_Patents",
    "INTELLECTUAL_PROPERTY_TRADEMARKS": "IP_Trademarks",
    "INTELLECTUAL_PROPERTY_COPYRIGHT": "IP_Copyright",
    "INTELLECTUAL_PROPERTY_DESIGNS": "IP_Designs",
    "INTELLECTUAL_PROPERTY_PLANT_BREEDERS_RIGHTS": "IP_Plant_Breeders",
    "INTELLECTUAL_PROPERTY_CIRCUIT_LAYOUTS": "IP_Circuits",

    # Sports Law -> New
    "SPORTS_LAW_ANTI_DOPING": "Sports_Anti_Doping",
    "SPORTS_LAW_PLAYER_CONTRACTS_EMPLOYMENT": "Sports_Contracts",
    "SPORTS_LAW_SPORTS_INTEGRITY_MATCH_FIXING": "Sports_Integrity",
    "SPORTS_LAW_GOVERNANCE_DISPUTES": "Sports_Governance",
    "SPORTS_LAW_DISCRIMINATION_SAFEGUARDING": "Sports_Safeguarding",
    "SPORTS_LAW_BROADCASTING_COMMERCIALISATION": "Sports_Broadcasting",

    # Commercial -> Map to existing or create new
    "1_CORPORATIONS_LAW_COMPANY_FORMATION_REGISTRATION": "Corp_Formation",
    "1_CORPORATIONS_LAW_DIRECTORS_DUTIES_RESPONSIBILITIES": "Corp_Governance",
    "1_CORPORATIONS_LAW_SHAREHOLDERS_MEETINGS": "Corp_Meetings",
    "1_CORPORATIONS_LAW_COMPANY_REGISTERS_RECORDS": "Corp_Records",
    "1_CORPORATIONS_LAW_SHARE_CAPITAL_FUNDRAISING": "Corp_Capital",
    "2_INSOLVENCY_LAW_CORPORATE_INSOLVENCY_TESTS": "Corp_Insolvency",
    "2_INSOLVENCY_LAW_LIQUIDATION_WINDING_UP": "Corp_Insolvency",
    "2_INSOLVENCY_LAW_VOLUNTARY_ADMINISTRATION": "Corp_Insolvency",
    "3_SECURITIES_FINANCIAL_SERVICES": "Securities_Licensing",
    "4_COMPETITION_LAW": "Competition_Cartels",
    "5_CONSUMER_LAW": "Comm_Consumer",
    "6_BANKING_FINANCE_LAW": "Comm_Banking",
    "7_INSURANCE_LAW": "Comm_Insurance",
    "8_SALE_OF_GOODS_SERVICES": "Comm_Contract",
    "9_PARTNERSHIP_LAW": "Comm_Partnership",
    "10_FRANCHISE_LAW": "Comm_Franchise",
    "11_AGENCY_LAW": "Comm_Agency",

    # Education Law -> New
    "EDUCATION_LAW": "Education_General",

    # Immigration/Citizenship -> Map to existing
    "IMMIGRATION_CITIZENSHIP_LAW": "Admin_Migration",

    # Charities/NFP -> New
    "CHARITIES_NOT_FOR_PROFIT_LAW": "Charities_NFP",

    # Privacy/Data -> New
    "PRIVACY_DATA_PROTECTION_LAW": "Privacy_Data",

    # Media/Communications -> New
    "MEDIA_COMMUNICATIONS_LAW": "Media_Communications",

    # Animal Law -> New
    "ANIMAL_LAW": "Animal_Welfare",

    # Elder Law -> New
    "ELDER_LAW": "Elder_Law",

    # Resources/Infrastructure/Energy Law -> New categories
    "MINING_LAW": "Resources_Mining",
    "PETROLEUM_GAS_LAW": "Resources_Petroleum",
    "WATER_LAW": "Resources_Water",
    "ENERGY_LAW": "Resources_Energy",
    "TELECOMMUNICATIONS_LAW": "Resources_Telecom",
    "BROADCASTING_LAW": "Resources_Broadcasting",
    "TRANSPORT_REGULATION_LAW": "Resources_Transport",
    "AVIATION_LAW": "Resources_Aviation",
    "MARITIME_ADMIRALTY_LAW": "Resources_Maritime",
    "CONSTRUCTION_BUILDING_LAW": "Resources_Construction",
    "INFRASTRUCTURE_MAJOR_PROJECTS_LAW": "Resources_Infrastructure",
    "AGRICULTURE_PRIMARY_PRODUCTION_LAW": "Resources_Agriculture",

    # Additional Mappings for Unmapped Categories
    "2_INSOLVENCY_LAW_VOIDABLE_TRANSACTIONS": "Corp_Insolvency",
    "2_INSOLVENCY_LAW_PERSONAL_BANKRUPTCY": "Corp_Insolvency",
    "Pharmacy_and_Drugs": "Health_Therapeutic_Goods",
    "Disability_NDIS": "Health_Aged_Care",
    "Coronial_Law": "Spec_Coronial",
    "Guardianship_and_Administration": "Health_Mental",
    "Privacy_and_Health_Records": "Privacy_Data",
    "Food_Safety": "Health_Food_Safety",
    "Veterinary_and_Animal_Law": "Animal_Welfare",
    "Professional_Discipline_NonHealth": "Admin_Disciplinary",
    "Professional_Discipline_Health": "Health_Practitioner",

    # Gaming and Liquor
    "GAMING_GAMBLING_CASINO_LICENSING": "Gaming_Gambling",
    "GAMING_GAMBLING_WAGERING_BETTING": "Gaming_Gambling",
    "GAMING_GAMBLING_LOTTERIES_KENO": "Gaming_Gambling",
    "GAMING_GAMBLING_GAMING_MACHINES": "Gaming_Gambling",
    "LIQUOR_LICENSING_LICENCE_TYPES": "Spec_Liquor",
    "LIQUOR_LICENSING_RSA_COMPLIANCE": "Spec_Liquor",
    "LIQUOR_LICENSING_VENUE_OPERATIONS_COMPLIANCE": "Spec_Liquor",
    "RACING_THOROUGHBRED_RACING": "Gaming_Gambling",
    "RACING_HARNESS_RACING": "Gaming_Gambling",
    "RACING_GREYHOUND_RACING": "Gaming_Gambling",
    "SPORTS_LAW_SPORTING_TRIBUNALS_DISCIPLINE": "Sports_Governance",

    # Catch-all for broad domains
    "CHARITIES_NOT_FOR_PROFIT": "Charities_NFP",
    "MILITARY_DEFENCE": "Spec_Military",
    "INTERNATIONAL_LAW": "Spec_International",

    # Map from domain knowledge file names
    "FAMILY_LAW_ACT_1975": "Family_General",
    "EMPLOYMENT_LAW": "Emp_Unfair_Dismissal",
    "CONSTITUTIONAL_LAW": "Const_Chapter_I",
    "EVIDENCE_PROCEDURE": "Proc_Evidence",
    "ADMINISTRATIVE_LAW": "Admin_Review",
    "TAX_LAW": "Tax_Income",
    "TORTS_LAW": "Tort_Negligence",
    "EQUITY_LAW": "Equity_Trusts",
    "CRIMINAL_LAW": "Crim_General",
    "PROPERTY_LAW": "Prop_Real",
    "COMMERCIAL_LAW": "Comm_Contract",
    "RESOURCES_INFRASTRUCTURE_ENERGY_LAW": "Resources_Energy",
}


# ============================================================================
# NEW CATEGORIES AND DOMAIN MAPPING
# ============================================================================

NEW_CATEGORIES = {
    # Health/Medical Domain
    'Health_Practitioner': [],
    'Health_Mental': [],
    'Health_Therapeutic_Goods': [],
    'Health_Private': [],
    'Health_Public': [],
    'Health_Aged_Care': [],
    'Health_Reproductive': [],
    'Health_Food_Safety': [],

    # Enhanced IP
    'IP_Patents': [],
    'IP_Trademarks': [],
    'IP_Designs': [],
    'IP_Plant_Breeders': [],
    'IP_Circuits': [],

    # Sports Law
    'Sports_Anti_Doping': [],
    'Sports_Contracts': [],
    'Sports_Integrity': [],
    'Sports_Governance': [],
    'Sports_Safeguarding': [],
    'Sports_Broadcasting': [],

    # Additional Commercial
    'Corp_Formation': [],
    'Corp_Meetings': [],
    'Corp_Records': [],
    'Corp_Capital': [],
    'Comm_Partnership': [],
    'Comm_Franchise': [],
    'Comm_Agency': [],

    # Resources/Infrastructure/Energy Law
    'Resources_Mining': [],
    'Resources_Petroleum': [],
    'Resources_Water': [],
    'Resources_Energy': [],
    'Resources_Telecom': [],
    'Resources_Broadcasting': [],
    'Resources_Transport': [],
    'Resources_Aviation': [],
    'Resources_Maritime': [],
    'Resources_Construction': [],
    'Resources_Infrastructure': [],
    'Resources_Agriculture': [],

    # Other New Domains
    'Education_General': [],
    'Charities_NFP': [],
    'Privacy_Data': [],
    'Media_Communications': [],
    'Animal_Welfare': [],
    'Elder_Law': [],
    'Gaming_Gambling': [],
    'Spec_Liquor': [],
    'Spec_Military': [],
    'Spec_International': [],
}

NEW_DOMAIN_MAPPING = {
    'Health': [
        'Health_Practitioner', 'Health_Mental', 'Health_Therapeutic_Goods',
        'Health_Private', 'Health_Public', 'Health_Aged_Care',
        'Health_Reproductive', 'Health_Food_Safety'
    ],
    'Sports': [
        'Sports_Anti_Doping', 'Sports_Contracts', 'Sports_Integrity',
        'Sports_Governance', 'Sports_Safeguarding', 'Sports_Broadcasting'
    ],
    'Resources': [
        'Resources_Mining', 'Resources_Petroleum', 'Resources_Water',
        'Resources_Energy', 'Resources_Telecom', 'Resources_Broadcasting',
        'Resources_Transport', 'Resources_Aviation', 'Resources_Maritime',
        'Resources_Construction', 'Resources_Infrastructure', 'Resources_Agriculture'
    ],
    'Education': ['Education_General'],
    'Charities': ['Charities_NFP'],
    'Privacy': ['Privacy_Data'],
    'Media': ['Media_Communications'],
    'Animal': ['Animal_Welfare'],
    'Elder': ['Elder_Law'],
    'Specialized': ['Gaming_Gambling', 'Spec_Liquor', 'Spec_Military', 'Spec_International'],
}


# ============================================================================
# MAIN INTEGRATION LOGIC
# ============================================================================

def extract_keywords_from_md(filepath: Path) -> Dict[str, List[str]]:
    """Extract keywords from markdown domain knowledge files."""
    results = {}
    content = filepath.read_text(encoding='utf-8')

    # Get domain name from filename
    domain_name = filepath.stem.replace('_DOMAIN_KNOWLEDGE', '').replace('_', ' ').title()
    domain_key = filepath.stem.replace('_DOMAIN_KNOWLEDGE', '')

    # Extract keywords from markdown patterns
    keywords = set()

    # Pattern 1: Keywords in lists (- keyword or * keyword)
    list_pattern = re.compile(r'^[\s]*[-*]\s+["\']?([^"\'\n,]+)["\']?', re.MULTILINE)
    for match in list_pattern.findall(content):
        kw = normalize_keyword(match)
        if len(kw) > 2 and len(kw) < 100:
            keywords.add(kw)

    # Pattern 2: Keywords in code blocks or quotes
    code_pattern = re.compile(r'["`]([a-z][a-z\s]{2,50})["`]', re.IGNORECASE)
    for match in code_pattern.findall(content):
        kw = normalize_keyword(match)
        if len(kw) > 2:
            keywords.add(kw)

    # Pattern 3: Legal terms in parentheses like (s180) or (Part IV)
    section_pattern = re.compile(r'\b(s\s*\d+[A-Za-z]?)\b|\b(Part\s+[IVX]+)\b|\b(Division\s+\d+)\b', re.IGNORECASE)
    for match in section_pattern.findall(content):
        for m in match:
            if m:
                keywords.add(m.lower())

    if keywords:
        results[domain_key] = list(keywords)

    return results


def load_all_dictionaries() -> Dict[str, List[str]]:
    """Load all dictionary files and extract keywords from all sources."""
    all_keywords = {}

    # Dictionary files in new location
    dictionary_dir = BASE_DIR / "law docs research" / "dictionaries"
    dictionary_files = [
        dictionary_dir / "COMPREHENSIVE_COMMERCIAL_LAW_DICTIONARY.py",
        dictionary_dir / "AUSTRALIAN_COMMERCIAL_LAW_COMPLETE_DICTIONARY.py",
        dictionary_dir / "AUSTRALIAN_HEALTH_MEDICAL_REGULATORY_LAW_COMPREHENSIVE.py",
        dictionary_dir / "AUSTRALIAN_SPECIALIZED_NICHE_LAW_DOMAINS.py",
        dictionary_dir / "resources_infrastructure_energy_law_dict.py",
    ]

    print("=" * 60)
    print("LOADING DICTIONARY FILES")
    print("=" * 60)

    for filepath in dictionary_files:
        if filepath.exists():
            print(f"Loading: {filepath.name}")
            data = load_dictionary_file(filepath)
            if data:
                extracted = extract_keywords_from_dict(data)
                print(f"  Extracted {len(extracted)} categories, {sum(len(v) for v in extracted.values())} keywords")
                all_keywords.update(extracted)
        else:
            print(f"  [Warning] File not found: {filepath}")

    # Also load from MD files in law docs research
    print("\n" + "=" * 60)
    print("LOADING MD DOMAIN KNOWLEDGE FILES")
    print("=" * 60)

    md_dir = BASE_DIR / "law docs research"
    md_files = []
    # Add multiple patterns to capture all relevant files
    patterns = ["*_DOMAIN_KNOWLEDGE.md", "*_COMPLETE.md", "*_KEYWORDS.md", "*_REFERENCE.md", "*_ANALYSIS.md"]
    for pattern in patterns:
        md_files.extend(list(md_dir.glob(pattern)))
    
    # Deduplicate files
    md_files = list(set(md_files))

    for filepath in md_files:
        print(f"Loading: {filepath.name}")
        extracted = extract_keywords_from_md(filepath)
        if extracted:
            print(f"  Extracted {sum(len(v) for v in extracted.values())} keywords")
            for key, keywords in extracted.items():
                if key in all_keywords:
                    all_keywords[key].extend(keywords)
                else:
                    all_keywords[key] = keywords

    # Deduplicate within each category
    for key in all_keywords:
        all_keywords[key] = list(set(all_keywords[key]))

    return all_keywords


def map_to_classification_categories(extracted: Dict[str, List[str]]) -> Dict[str, Set[str]]:
    """Map extracted keywords to classification categories."""
    mapped = defaultdict(set)
    unmapped = []

    for source_cat, keywords in extracted.items():
        # Try exact mapping first
        if source_cat in CATEGORY_MAPPING:
            target_cat = CATEGORY_MAPPING[source_cat]
            mapped[target_cat].update(keywords)
        else:
            # Try partial matching
            found = False
            for pattern, target in CATEGORY_MAPPING.items():
                if pattern in source_cat or source_cat in pattern:
                    mapped[target].update(keywords)
                    found = True
                    break

            if not found:
                unmapped.append((source_cat, len(keywords)))

    if unmapped:
        print(f"\n[Info] {len(unmapped)} categories could not be mapped:")
        for cat, count in unmapped[:10]:
            print(f"  - {cat}: {count} keywords")

    return mapped


def generate_config_update(mapped_keywords: Dict[str, Set[str]]) -> str:
    """Generate Python code to update classification_config.py."""

    lines = []
    lines.append("# ============================================================================")
    lines.append("# AUTO-GENERATED KEYWORD ADDITIONS")
    lines.append("# Generated by scripts/integrate_keywords.py")
    lines.append("# ============================================================================")
    lines.append("")

    # New categories
    lines.append("# --- NEW CATEGORIES ---")
    for cat_name in sorted(NEW_CATEGORIES.keys()):
        if cat_name in mapped_keywords and mapped_keywords[cat_name]:
            keywords = sorted(mapped_keywords[cat_name])
            lines.append(f"    '{cat_name}': [")
            for i, kw in enumerate(keywords[:50]):  # Limit to 50 for readability
                comma = "," if i < min(len(keywords), 50) - 1 else ""
                lines.append(f"        '{kw}'{comma}")
            if len(keywords) > 50:
                lines.append(f"        # ... and {len(keywords) - 50} more keywords")
            lines.append("    ],")
            lines.append("")

    # Keywords to add to existing categories
    lines.append("")
    lines.append("# --- KEYWORDS TO ADD TO EXISTING CATEGORIES ---")
    lines.append("KEYWORDS_TO_ADD = {")

    existing_cats = [
        'Corp_Governance', 'Corp_Insolvency', 'Comm_Contract', 'Comm_Banking',
        'Comm_Consumer', 'Comm_Insurance', 'IP_Copyright', 'IP_Patent_Trademark',
        'Securities_Licensing', 'Securities_Disclosure', 'Securities_Managed_Investments',
        'Securities_Market_Misconduct', 'Competition_Cartels', 'Competition_Market_Power',
        'Competition_Mergers', 'Competition_Restrictive', 'Admin_Migration',
        'Spec_Mental_Health'
    ]

    for cat_name in existing_cats:
        if cat_name in mapped_keywords and mapped_keywords[cat_name]:
            keywords = sorted(mapped_keywords[cat_name])[:30]
            lines.append(f"    '{cat_name}': [")
            for i, kw in enumerate(keywords):
                comma = "," if i < len(keywords) - 1 else ""
                lines.append(f"        '{kw}'{comma}")
            lines.append("    ],")

    lines.append("}")
    lines.append("")

    # New domain mapping
    lines.append("# --- NEW DOMAIN MAPPING ---")
    lines.append("NEW_DOMAIN_MAPPING = {")
    for domain, categories in NEW_DOMAIN_MAPPING.items():
        cats_str = ", ".join([f"'{c}'" for c in categories])
        lines.append(f"    '{domain}': [{cats_str}],")
    lines.append("}")

    return "\n".join(lines)


def merge_to_classification_config(mapped_keywords: Dict[str, Set[str]]) -> bool:
    """
    Merge the extracted keywords directly into classification_config.py.
    Returns True on success, False on failure.
    """
    from src.ingestion.classification_config import (
        CLASSIFICATION_MAP, DOMAIN_MAPPING,
        HIERARCHY_MAP, LEGISLATION_STATUS_MAP
    )

    # Merge keywords
    keywords_added = 0
    categories_added = 0

    for category, keywords in mapped_keywords.items():
        if category in CLASSIFICATION_MAP:
            # Add to existing category
            existing = set(CLASSIFICATION_MAP[category])
            new_keywords = keywords - existing
            if new_keywords:
                CLASSIFICATION_MAP[category].extend(sorted(new_keywords))
                keywords_added += len(new_keywords)
        else:
            # Add new category
            CLASSIFICATION_MAP[category] = sorted(keywords)
            keywords_added += len(keywords)
            categories_added += 1

    # Add new domain mappings
    domains_added = []
    for domain, categories in NEW_DOMAIN_MAPPING.items():
        if domain not in DOMAIN_MAPPING:
            DOMAIN_MAPPING[domain] = categories
            domains_added.append(domain)
        else:
            # Extend existing domain with new categories
            existing = set(DOMAIN_MAPPING[domain])
            for cat in categories:
                if cat not in existing:
                    DOMAIN_MAPPING[domain].append(cat)

    # Generate the new file content
    config_path = BASE_DIR / "src" / "ingestion" / "classification_config.py"
    lines = []
    lines.append("# classification_config.py")
    lines.append("# Auto-updated by scripts/integrate_keywords.py")
    lines.append(f"# Total categories: {len(CLASSIFICATION_MAP)}")
    lines.append(f"# Total keywords: {sum(len(v) for v in CLASSIFICATION_MAP.values())}")
    lines.append("")

    # Write HIERARCHY_MAP using repr for proper formatting
    lines.append("# Map citations/filenames to Hierarchy Weight (10 = Apex, 1 = Lower)")
    lines.append("HIERARCHY_MAP = {")
    for court, info in HIERARCHY_MAP.items():
        lines.append(f"    {repr(court)}: {repr(info)},")
    lines.append("}")
    lines.append("")

    # Write LEGISLATION_STATUS_MAP
    lines.append("# Map keywords to Legislative Status")
    lines.append("LEGISLATION_STATUS_MAP = {")
    for status, info in LEGISLATION_STATUS_MAP.items():
        lines.append(f"    {repr(status)}: {repr(info)},")
    lines.append("}")
    lines.append("")

    # Write CLASSIFICATION_MAP
    lines.append("# classification_dictionary.py")
    lines.append("")
    lines.append("CLASSIFICATION_MAP = {")

    # Group categories by domain for organization
    category_order = [
        # Criminal
        'Criminal_Violence', 'Criminal_Sexual', 'Criminal_Drugs', 'Criminal_Property',
        'Criminal_Traffic', 'Criminal_White_Collar', 'Criminal_Cyber', 'Criminal_Procedure',
        'Criminal_Defences', 'Criminal_General', 'Crim_General',
        # Administrative
        'Admin_Judicial_Review', 'Admin_Review', 'Admin_Merits_Review', 'Admin_Migration',
        'Admin_Social_Security', 'Admin_Information', 'Admin_Disciplinary', 'Admin_Regulatory',
        # Constitutional
        'Constitutional_Federal', 'Constitutional_State', 'Constitutional_Rights',
        'Const_Chapter_I', 'Const_Federal',
        # Family
        'Family_Parenting', 'Family_Property', 'Family_Child_Protection', 'Family_Violence',
        'Family_Child_Support', 'Family_Divorce', 'Family_De_Facto', 'Family_General',
        # Tax
        'Tax_Income', 'Tax_CGT', 'Tax_GST', 'Tax_FBT', 'Tax_International', 'Tax_Avoidance',
        'Tax_State', 'Tax_Superannuation',
        # Torts
        'Tort_Negligence', 'Tort_Defamation', 'Tort_Medical', 'Tort_Institutional',
        'Tort_Intentional', 'Tort_Nuisance', 'Tort_Product_Liability', 'Tort_Economic',
        'Comp_Workers', 'Comp_Motor_Accidents', 'Comp_Victims',
        # Equity
        'Equity_General', 'Equity_Fiduciary', 'Equity_Trusts', 'Equity_Estoppel',
        'Equity_Unconscionable', 'Equity_Remedies', 'Succession_Probate', 'Succession_Family_Provision',
        # Commercial
        'Corp_Formation', 'Corp_Governance', 'Corp_Meetings', 'Corp_Records', 'Corp_Capital',
        'Corp_Insolvency', 'Comm_Contract', 'Comm_Banking', 'Comm_Consumer', 'Comm_Insurance',
        'Comm_International', 'Comm_Partnership', 'Comm_Franchise', 'Comm_Agency',
        # IP
        'IP_Copyright', 'IP_Patent_Trademark', 'IP_Patents', 'IP_Trademarks', 'IP_Designs',
        'IP_Plant_Breeders', 'IP_Circuits',
        # Securities
        'Securities_Licensing', 'Securities_Disclosure', 'Securities_Managed_Investments',
        'Securities_Market_Misconduct',
        # Competition
        'Competition_Cartels', 'Competition_Market_Power', 'Competition_Mergers', 'Competition_Restrictive',
        # Property
        'Prop_Real', 'Prop_Torrens', 'Prop_Conveyancing', 'Prop_Leasing', 'Prop_Strata',
        'Prop_Easements', 'Prop_Mortgages', 'Prop_Neighbours',
        'Env_Development', 'Env_Protection', 'Env_Compulsory_Acq', 'Native_Title',
        # Employment
        'Emp_Contract', 'Emp_Rights', 'Emp_Termination', 'Emp_Unfair_Dismissal', 'Emp_Industrial',
        'Emp_Safety', 'Emp_WorkersComp', 'Emp_Discrimination',
        # Procedural
        'Proc_Civil', 'Proc_Evidence', 'Proc_Enforcement',
        # Health
        'Health_Practitioner', 'Health_Mental', 'Health_Therapeutic_Goods', 'Health_Private',
        'Health_Public', 'Health_Aged_Care', 'Health_Reproductive', 'Health_Food_Safety',
        # Resources/Infrastructure
        'Mining_Exploration', 'Mining_Operations', 'Mining_Native_Title', 'Mining_Commercial',
        'Resources_Mining', 'Resources_Petroleum', 'Resources_Water', 'Resources_Energy',
        'Resources_Telecom', 'Resources_Broadcasting', 'Resources_Transport', 'Resources_Aviation',
        'Resources_Maritime', 'Resources_Construction', 'Resources_Infrastructure', 'Resources_Agriculture',
        'Petroleum_Exploration', 'Petroleum_Offshore', 'Petroleum_Operations',
        'Water_Entitlements', 'Water_Trading', 'Water_Murray_Darling',
        'Energy_Electricity', 'Energy_Gas', 'Energy_Renewable',
        'Telecom_Licensing', 'Telecom_NBN', 'Telecom_Spectrum',
        'Transport_Heavy_Vehicles', 'Transport_Rail',
        'Construction_Security_Payment', 'Construction_Building', 'Construction_Infrastructure',
        'Agriculture_Biosecurity', 'Agriculture_Chemicals', 'Agriculture_GM',
        # Sports
        'Sports_Anti_Doping', 'Sports_Contracts', 'Sports_Integrity', 'Sports_Governance',
        'Sports_Safeguarding', 'Sports_Broadcasting',
        # Specialized
        'Spec_Maritime', 'Spec_Aviation', 'Spec_Mental_Health', 'Spec_Coronial',
        # Other
        'Education_General', 'Charities_NFP', 'Privacy_Data', 'Media_Communications',
        'Animal_Welfare', 'Elder_Law',
    ]

    # Helper function to escape keyword for Python string literal
    def escape_keyword(kw: str) -> str:
        """Escape a keyword for use in a Python string literal."""
        # Use repr() to properly escape special characters
        return repr(kw)

    # Write categories in order, then any remaining
    written_cats = set()
    for cat in category_order:
        if cat in CLASSIFICATION_MAP:
            keywords = CLASSIFICATION_MAP[cat]
            lines.append(f"    '{cat}': [")
            for i, kw in enumerate(sorted(keywords)):
                comma = "," if i < len(keywords) - 1 else ""
                lines.append(f"        {escape_keyword(kw)}{comma}")
            lines.append("    ],")
            written_cats.add(cat)

    # Write any categories not in the order list
    for cat in sorted(CLASSIFICATION_MAP.keys()):
        if cat not in written_cats:
            keywords = CLASSIFICATION_MAP[cat]
            lines.append(f"    '{cat}': [")
            for i, kw in enumerate(sorted(keywords)):
                comma = "," if i < len(keywords) - 1 else ""
                lines.append(f"        {escape_keyword(kw)}{comma}")
            lines.append("    ],")

    lines.append("}")
    lines.append("")

    # Write DOMAIN_MAPPING
    lines.append("# Domain Mapping (Granular -> Broad)")
    lines.append("DOMAIN_MAPPING = {")
    for domain in sorted(DOMAIN_MAPPING.keys()):
        cats = DOMAIN_MAPPING[domain]
        cats_str = ", ".join([f"'{c}'" for c in cats])
        lines.append(f"    '{domain}': [{cats_str}],")
    lines.append("}")
    lines.append("")

    # Write the file
    config_path.write_text("\n".join(lines), encoding='utf-8')

    print(f"\n[Merge Complete]")
    print(f"  Keywords added: {keywords_added}")
    print(f"  New categories: {categories_added}")
    print(f"  New domains: {', '.join(domains_added) if domains_added else 'None'}")
    print(f"  Total categories: {len(CLASSIFICATION_MAP)}")
    print(f"  Total keywords: {sum(len(v) for v in CLASSIFICATION_MAP.values())}")

    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Integrate keywords from dictionary files")
    parser.add_argument('--apply', action='store_true', help="Apply changes to classification_config.py")
    args = parser.parse_args()

    print("=" * 60)
    print("KEYWORD INTEGRATION SCRIPT")
    print("=" * 60)
    print()

    # Step 1: Load all dictionaries
    print("Step 1: Loading dictionary files...")
    extracted = load_all_dictionaries()
    print(f"\nTotal extracted: {len(extracted)} categories, {sum(len(v) for v in extracted.values())} keywords")

    # Step 2: Map to classification categories
    print("\nStep 2: Mapping to classification categories...")
    mapped = map_to_classification_categories(extracted)
    print(f"Mapped to {len(mapped)} classification categories")

    # Step 3: Generate output or apply
    if args.apply:
        print("\nStep 3: Applying changes to classification_config.py...")
        success = merge_to_classification_config(mapped)
        if success:
            print("\n[SUCCESS] Classification config updated!")
    else:
        print("\nStep 3: Generating configuration update...")
        output = generate_config_update(mapped)

        # Write to output file
        output_path = BASE_DIR / "data" / "keyword_additions.py"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')
        print(f"\nOutput written to: {output_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total categories mapped: {len(mapped)}")
    print(f"Total unique keywords: {sum(len(v) for v in mapped.values())}")

    if not args.apply:
        print("\nNew domains to add:")
        for domain in NEW_DOMAIN_MAPPING.keys():
            print(f"  - {domain}")

        print("\nNext steps:")
        print("1. Review data/keyword_additions.py")
        print("2. Run with --apply to merge into classification_config.py")
        print("3. Run corpus_domain_extractor.py")

    return mapped


if __name__ == "__main__":
    main()
