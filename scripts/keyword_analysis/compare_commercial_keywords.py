"""
Script to compare COMPREHENSIVE_COMMERCIAL_LAW_DICTIONARY.py against classification_config.py
and identify missing keywords for Commercial Law domains.
"""

import re
import sys

def extract_dict_keywords(file_path):
    """Extract all keywords from the comprehensive dictionary."""
    keywords = []
    current_category = None
    in_keywords = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Detect category
            if '"1_CORPORATIONS_LAW"' in line:
                current_category = "CORPORATIONS"
            elif '"2_INSOLVENCY_LAW"' in line:
                current_category = "INSOLVENCY"
            elif '"3_SECURITIES_FINANCIAL_SERVICES"' in line:
                current_category = "SECURITIES"
            elif '"4_COMPETITION_LAW"' in line:
                current_category = "COMPETITION"
            elif '"5_CONSUMER_LAW"' in line:
                current_category = "CONSUMER"
            elif '"6_BANKING_FINANCE"' in line:
                current_category = "BANKING"
            elif '"7_INSURANCE_LAW"' in line:
                current_category = "INSURANCE"
            elif '"8_SALE_OF_GOODS"' in line:
                current_category = "SALE_OF_GOODS"
            elif '"9_PARTNERSHIP_LAW"' in line:
                current_category = "PARTNERSHIP"
            elif '"10_FRANCHISE_LAW"' in line:
                current_category = "FRANCHISE"
            elif '"11_AGENCY_LAW"' in line:
                current_category = "AGENCY"

            # Start of keywords list
            if '"keywords": [' in line:
                in_keywords = True
                continue

            # End of keywords list
            if in_keywords and ']' in line and '"' not in line:
                in_keywords = False
                continue

            # Extract keyword
            if in_keywords and current_category:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    keyword = match.group(1)
                    # Clean up keywords - remove section references in parentheses for comparison
                    clean_keyword = re.sub(r'\s*\([^)]*\)', '', keyword).strip().lower()
                    keywords.append({
                        'original': keyword,
                        'clean': clean_keyword,
                        'category': current_category
                    })

    return keywords

def extract_config_keywords(file_path):
    """Extract keywords from classification_config.py for Commercial Law categories."""
    keywords_by_category = {
        'Corp_Governance': [],
        'Corp_Insolvency': [],
        'Corp_Fundraising': [],
        'Comm_Banking': [],
        'Comm_Consumer': [],
        'Comm_Competition': [],
        'Comm_Insurance': [],
        'Comm_Contract': [],
        'Comm_Sale_of_Goods': [],
        'IP_Copyright': [],
        'IP_Patent': [],
        'IP_Trademark': [],
        'IP_Confidential': [],
        'IP_Designs': [],
        'IP_Patent_Trademark': []
    }

    current_category = None
    in_list = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Detect category
            for cat in keywords_by_category.keys():
                if f"'{cat}': [" in line:
                    current_category = cat
                    in_list = True
                    break

            if in_list:
                # End of list
                if line.strip() == '],':
                    in_list = False
                    current_category = None
                    continue

                # Extract keywords
                matches = re.findall(r"'([^']+)'", line)
                if matches and current_category:
                    keywords_by_category[current_category].extend([kw.lower().strip() for kw in matches])

    return keywords_by_category

def map_dict_to_config_category(dict_category):
    """Map dictionary category to config categories."""
    mapping = {
        'CORPORATIONS': ['Corp_Governance', 'Corp_Fundraising'],
        'INSOLVENCY': ['Corp_Insolvency'],
        'SECURITIES': ['Corp_Fundraising'],
        'COMPETITION': ['Comm_Competition'],
        'CONSUMER': ['Comm_Consumer'],
        'BANKING': ['Comm_Banking'],
        'INSURANCE': ['Comm_Insurance'],
        'SALE_OF_GOODS': ['Comm_Sale_of_Goods'],
        'PARTNERSHIP': ['Comm_Contract'],  # No specific category
        'FRANCHISE': ['Comm_Contract'],     # No specific category
        'AGENCY': ['Comm_Contract']         # No specific category
    }
    return mapping.get(dict_category, [])

def main():
    dict_file = r'C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\COMPREHENSIVE_COMMERCIAL_LAW_DICTIONARY.py'
    config_file = r'C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\classification_config.py'

    print("Extracting keywords from COMPREHENSIVE_COMMERCIAL_LAW_DICTIONARY.py...")
    dict_keywords = extract_dict_keywords(dict_file)
    print(f"Found {len(dict_keywords)} keywords in dictionary")

    print("\nExtracting keywords from classification_config.py...")
    config_keywords = extract_config_keywords(config_file)
    total_config = sum(len(v) for v in config_keywords.values())
    print(f"Found {total_config} keywords in config across {len(config_keywords)} categories")

    # Group dict keywords by category
    dict_by_category = {}
    for kw in dict_keywords:
        cat = kw['category']
        if cat not in dict_by_category:
            dict_by_category[cat] = []
        dict_by_category[cat].append(kw)

    # Find missing keywords
    missing_by_config_category = {}

    for dict_cat, dict_kws in dict_by_category.items():
        config_cats = map_dict_to_config_category(dict_cat)

        for config_cat in config_cats:
            if config_cat not in config_keywords:
                continue

            existing = set(config_keywords[config_cat])

            if config_cat not in missing_by_config_category:
                missing_by_config_category[config_cat] = []

            for kw_obj in dict_kws:
                # Check if keyword (or similar variant) exists
                clean = kw_obj['clean']
                if clean not in existing:
                    # Also check for partial matches
                    found = False
                    for exist_kw in existing:
                        # Check if keywords are very similar
                        if clean in exist_kw or exist_kw in clean:
                            found = True
                            break

                    if not found:
                        missing_by_config_category[config_cat].append(kw_obj['original'])

    # Report results
    print("\n" + "="*80)
    print("MISSING KEYWORDS ANALYSIS")
    print("="*80)

    total_missing = 0
    for config_cat in sorted(missing_by_config_category.keys()):
        missing = missing_by_config_category[config_cat]
        if missing:
            total_missing += len(missing)
            print(f"\n{config_cat}: {len(missing)} missing keywords")
            print("-" * 80)
            for i, kw in enumerate(sorted(set(missing))[:50], 1):  # Show first 50
                print(f"  {i}. {kw}")
            if len(set(missing)) > 50:
                print(f"  ... and {len(set(missing)) - 50} more")

    print("\n" + "="*80)
    print(f"TOTAL MISSING KEYWORDS: {total_missing}")
    print("="*80)

    # Write output to file for easier review
    with open('missing_keywords_report.txt', 'w', encoding='utf-8') as f:
        f.write("MISSING COMMERCIAL LAW KEYWORDS REPORT\n")
        f.write("="*80 + "\n\n")

        for config_cat in sorted(missing_by_config_category.keys()):
            missing = sorted(set(missing_by_config_category[config_cat]))
            if missing:
                f.write(f"\n{config_cat}: {len(missing)} missing keywords\n")
                f.write("-" * 80 + "\n")
                for kw in missing:
                    f.write(f"  '{kw}',\n")
                f.write("\n")

        f.write(f"\nTOTAL MISSING: {total_missing}\n")

    print("\nDetailed report written to: missing_keywords_report.txt")

if __name__ == "__main__":
    main()
