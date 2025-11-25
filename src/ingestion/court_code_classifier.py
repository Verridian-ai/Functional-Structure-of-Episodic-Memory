"""
Court Code Classifier - Classify decisions by court code extracted from citations
Uses the court code as primary classifier (most reliable) + catchwords/legislation as secondary
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, Optional, Tuple


# Court code to domain mapping
# Based on analysis of NSW Caselaw, Federal Court, and High Court patterns
COURT_CODE_MAP = {
    # HIGH COURT
    'HCA': {'domain': 'Apex_Court', 'court': 'High Court of Australia', 'weight': 10},

    # FEDERAL COURTS
    'FCA': {'domain': 'Federal_Court', 'court': 'Federal Court of Australia', 'weight': 7},
    'FCAFC': {'domain': 'Federal_Court', 'court': 'Federal Court (Full Court)', 'weight': 9},
    'FamCA': {'domain': 'Family', 'court': 'Family Court of Australia', 'weight': 7},
    'FamCAFC': {'domain': 'Family', 'court': 'Family Court (Full Court)', 'weight': 8},
    'FCFCOA': {'domain': 'Family', 'court': 'Federal Circuit and Family Court', 'weight': 6},
    'AATA': {'domain': 'Administrative', 'court': 'Admin Appeals Tribunal', 'weight': 4},
    'ART': {'domain': 'Administrative', 'court': 'Admin Review Tribunal', 'weight': 4},

    # NSW COURTS
    'NSWCA': {'domain': 'Appeals', 'court': 'NSW Court of Appeal', 'weight': 8},
    'NSWCCA': {'domain': 'Criminal', 'court': 'NSW Court of Criminal Appeal', 'weight': 8},
    'NSWSC': {'domain': 'Supreme_Court', 'court': 'NSW Supreme Court', 'weight': 6},
    'NSWDC': {'domain': 'District_Court', 'court': 'NSW District Court', 'weight': 4},
    'NSWLC': {'domain': 'Local_Court', 'court': 'NSW Local Court', 'weight': 2},

    # NSW TRIBUNALS
    'NSWCATAD': {'domain': 'Admin_Tribunal', 'court': 'NCAT Admin Division', 'weight': 3},
    'NSWCATAP': {'domain': 'Admin_Tribunal', 'court': 'NCAT Appeal Panel', 'weight': 4},
    'NSWCATCD': {'domain': 'Consumer_Tribunal', 'court': 'NCAT Consumer Division', 'weight': 3},
    'NSWCATGD': {'domain': 'Guardianship', 'court': 'NCAT Guardianship Division', 'weight': 3},
    'NSWCATOD': {'domain': 'Occupational', 'court': 'NCAT Occupational Division', 'weight': 3},
    'NSWCAT': {'domain': 'Admin_Tribunal', 'court': 'NCAT (General)', 'weight': 3},
    'NSWIRComm': {'domain': 'Industrial', 'court': 'IRC NSW', 'weight': 4},
    'NSWWCC': {'domain': 'Workers_Comp', 'court': 'Workers Compensation Commission', 'weight': 3},
    'NSWWCCPD': {'domain': 'Workers_Comp', 'court': 'WCC Presidential Division', 'weight': 4},

    # NSW SPECIALIZED
    'NSWLEC': {'domain': 'Environment', 'court': 'Land and Environment Court', 'weight': 5},
    'NSWADTAP': {'domain': 'Admin_Tribunal', 'court': 'ADT Appeal Panel', 'weight': 4},
    'NSWADT': {'domain': 'Admin_Tribunal', 'court': 'Admin Decisions Tribunal', 'weight': 3},
    'NSWIRC': {'domain': 'Industrial', 'court': 'Industrial Relations Commission', 'weight': 4},
    'NSWDDT': {'domain': 'Dust_Diseases', 'court': 'Dust Diseases Tribunal', 'weight': 4},
    'NSWChC': {'domain': 'Children', 'court': "NSW Children's Court", 'weight': 3},
    'NSWCorC': {'domain': 'Coronial', 'court': "Coroner's Court", 'weight': 4},
    'NSWCompT': {'domain': 'Compensation', 'court': 'Compensation Court', 'weight': 4},

    # VICTORIA
    'VSCA': {'domain': 'Appeals', 'court': 'VIC Court of Appeal', 'weight': 8},
    'VSC': {'domain': 'Supreme_Court', 'court': 'VIC Supreme Court', 'weight': 6},
    'VCC': {'domain': 'County_Court', 'court': 'VIC County Court', 'weight': 4},
    'VCAT': {'domain': 'Admin_Tribunal', 'court': 'VCAT', 'weight': 3},
    'VMC': {'domain': 'Magistrates', 'court': 'VIC Magistrates Court', 'weight': 2},

    # QUEENSLAND
    'QCA': {'domain': 'Appeals', 'court': 'QLD Court of Appeal', 'weight': 8},
    'QSC': {'domain': 'Supreme_Court', 'court': 'QLD Supreme Court', 'weight': 6},
    'QDC': {'domain': 'District_Court', 'court': 'QLD District Court', 'weight': 4},
    'QCAT': {'domain': 'Admin_Tribunal', 'court': 'QCAT', 'weight': 3},
    'QMC': {'domain': 'Magistrates', 'court': 'QLD Magistrates Court', 'weight': 2},
    'QLC': {'domain': 'Land_Court', 'court': 'QLD Land Court', 'weight': 4},
    'QIRC': {'domain': 'Industrial', 'court': 'QLD Industrial Relations Commission', 'weight': 4},
    'ICQ': {'domain': 'Industrial', 'court': 'Industrial Court of QLD', 'weight': 5},

    # WESTERN AUSTRALIA
    'WASCA': {'domain': 'Appeals', 'court': 'WA Court of Appeal', 'weight': 8},
    'WASC': {'domain': 'Supreme_Court', 'court': 'WA Supreme Court', 'weight': 6},
    'WADC': {'domain': 'District_Court', 'court': 'WA District Court', 'weight': 4},
    'WASAT': {'domain': 'Admin_Tribunal', 'court': 'WA State Admin Tribunal', 'weight': 3},

    # SOUTH AUSTRALIA
    'SASCA': {'domain': 'Appeals', 'court': 'SA Court of Appeal', 'weight': 8},
    'SASC': {'domain': 'Supreme_Court', 'court': 'SA Supreme Court', 'weight': 6},
    'SADC': {'domain': 'District_Court', 'court': 'SA District Court', 'weight': 4},
    'SACAT': {'domain': 'Admin_Tribunal', 'court': 'SACAT', 'weight': 3},
    'SAET': {'domain': 'Employment', 'court': 'SA Employment Tribunal', 'weight': 4},

    # TASMANIA
    'TASSC': {'domain': 'Supreme_Court', 'court': 'TAS Supreme Court', 'weight': 6},
    'TASFC': {'domain': 'Appeals', 'court': 'TAS Full Court', 'weight': 7},
    'TASWRCT': {'domain': 'Workers_Comp', 'court': 'TAS Workers Rehab Tribunal', 'weight': 3},

    # ACT
    'ACTCA': {'domain': 'Appeals', 'court': 'ACT Court of Appeal', 'weight': 8},
    'ACTSC': {'domain': 'Supreme_Court', 'court': 'ACT Supreme Court', 'weight': 6},
    'ACAT': {'domain': 'Admin_Tribunal', 'court': 'ACT Civil and Admin Tribunal', 'weight': 3},

    # NT
    'NTCA': {'domain': 'Appeals', 'court': 'NT Court of Appeal', 'weight': 8},
    'NTSC': {'domain': 'Supreme_Court', 'court': 'NT Supreme Court', 'weight': 6},
    'NTCAT': {'domain': 'Admin_Tribunal', 'court': 'NT Civil and Admin Tribunal', 'weight': 3},
}

# Catchwords domain mapping (for secondary classification)
CATCHWORD_DOMAINS = {
    'Criminal': ['CRIMINAL', 'CRIME', 'OFFENCE', 'SENTENCE', 'CONVICTION', 'MURDER', 'ASSAULT'],
    'Migration': ['MIGRATION', 'VISA', 'REFUGEE', 'ASYLUM', 'DEPORTATION', 'IMMIGRATION'],
    'Tax': ['TAX', 'TAXATION', 'REVENUE', 'GST', 'INCOME TAX', 'COMMISSIONER OF TAXATION'],
    'Employment': ['EMPLOYMENT', 'INDUSTRIAL', 'UNFAIR DISMISSAL', 'WORKPLACE', 'AWARD'],
    'Family': ['FAMILY LAW', 'PARENTING', 'PROPERTY SETTLEMENT', 'DIVORCE', 'CHILDREN'],
    'Commercial': ['CORPORATIONS', 'CONTRACT', 'COMMERCIAL', 'COMPANY', 'INSOLVENCY'],
    'Property': ['REAL PROPERTY', 'CONVEYANCING', 'LAND', 'EASEMENT', 'STRATA'],
    'Torts': ['NEGLIGENCE', 'DEFAMATION', 'PERSONAL INJURY', 'TORT', 'DAMAGES'],
    'Administrative': ['ADMINISTRATIVE', 'JUDICIAL REVIEW', 'MERITS REVIEW', 'GOVERNMENT'],
    'Consumer': ['CONSUMER', 'MISLEADING', 'DECEPTIVE CONDUCT', 'FAIR TRADING'],
    'Environment': ['ENVIRONMENT', 'PLANNING', 'DEVELOPMENT', 'CONTAMINATION'],
    'IP': ['COPYRIGHT', 'PATENT', 'TRADEMARK', 'INTELLECTUAL PROPERTY'],
}


def extract_court_code(citation: str) -> Optional[str]:
    """Extract court code from citation string."""
    # Pattern: [Year] COURTCODE Number
    # Examples: [2020] FCA 1492, [2013] NSWSC 1668
    pattern = r'\[?\d{4}\]?\s*([A-Z]+(?:Comm|FC|CA|SC|DC|LC|CC|MC|CT|AT|PD|AP|CD|GD|OD)?)\s*\d+'
    match = re.search(pattern, citation)
    if match:
        return match.group(1)
    return None


def extract_catchwords_domain(text: str) -> Optional[str]:
    """Extract domain from catchwords section if present."""
    # Look for CATCHWORDS or catchwords section
    catchwords_match = re.search(r'(?:CATCHWORDS?|Catchwords?)[:\s]*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\nLEGISLATION|\nCases)', text[:5000])
    if catchwords_match:
        catchwords = catchwords_match.group(1).upper()
        for domain, keywords in CATCHWORD_DOMAINS.items():
            for kw in keywords:
                if kw in catchwords:
                    return domain
    return None


def classify_decision(doc: dict) -> Tuple[str, str, dict]:
    """
    Classify a court decision.

    Returns:
        (domain, court_code, metadata)
    """
    citation = doc.get('citation', '')
    text = doc.get('text', '')[:5000]  # First 5000 chars for catchwords

    # Primary: Extract court code
    court_code = extract_court_code(citation)

    if court_code and court_code in COURT_CODE_MAP:
        court_info = COURT_CODE_MAP[court_code]
        domain = court_info['domain']

        # Secondary: Check catchwords for more specific domain
        catchword_domain = extract_catchwords_domain(text)
        if catchword_domain:
            # Use catchword domain for general courts
            if domain in ['Supreme_Court', 'District_Court', 'Federal_Court', 'Apex_Court']:
                domain = catchword_domain

        return domain, court_code, court_info

    # Fallback: try to extract any court code pattern
    if court_code:
        return 'Unknown_Court', court_code, {'court': court_code, 'weight': 1}

    return 'Unclassified', 'UNKNOWN', {'court': 'Unknown', 'weight': 0}


class DomainFileManager:
    """Manages output files for each domain."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.files: Dict[str, object] = {}
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for f in self.files.values():
            f.close()

    def _get_file(self, domain: str):
        if domain not in self.files:
            filepath = self.output_dir / f"{domain.lower()}.jsonl"
            self.files[domain] = open(filepath, 'w', encoding='utf-8')
        return self.files[domain]

    def write(self, domain: str, doc: dict):
        f = self._get_file(domain)
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')


def classify_decisions(input_path: Path, output_dir: Path, progress_interval: int = 10000):
    """Classify all decisions by court code."""

    domain_counts = defaultdict(int)
    court_counts = defaultdict(int)
    total = 0
    start_time = datetime.now()

    print(f"[Classifier] Input: {input_path}")
    print(f"[Classifier] Output: {output_dir}")
    print("-" * 60)

    with open(input_path, 'r', encoding='utf-8') as f_in:
        with DomainFileManager(output_dir) as manager:
            for line in f_in:
                if not line.strip():
                    continue

                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue

                total += 1

                domain, court_code, court_info = classify_decision(doc)

                # Add classification metadata to document
                doc['_classification'] = {
                    'domain': domain,
                    'court_code': court_code,
                    'court_name': court_info.get('court', 'Unknown'),
                    'weight': court_info.get('weight', 0)
                }

                domain_counts[domain] += 1
                court_counts[court_code] += 1
                manager.write(domain, doc)

                if total % progress_interval == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = total / elapsed if elapsed > 0 else 0
                    top_domains = sorted(domain_counts.items(), key=lambda x: -x[1])[:5]
                    domain_str = " | ".join([f"{k}:{v}" for k, v in top_domains])
                    print(f"[Progress] {total:,} docs | {rate:.0f}/sec | {domain_str}")

    elapsed = datetime.now() - start_time
    print(f"\n[Complete] Processed {total:,} documents in {elapsed}")

    # Save statistics
    stats = {
        "total_documents": total,
        "started_at": start_time.isoformat(),
        "completed_at": datetime.now().isoformat(),
        "domain_counts": dict(domain_counts),
        "court_counts": dict(court_counts)
    }

    stats_path = output_dir / "classification_statistics.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    print(f"[Stats] Saved to {stats_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("DOMAIN DISTRIBUTION:")
    print("=" * 60)
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        pct = (count / total) * 100
        print(f"  {domain}: {count:,} ({pct:.1f}%)")

    print("\n" + "=" * 60)
    print("TOP COURT CODES:")
    print("=" * 60)
    for court, count in sorted(court_counts.items(), key=lambda x: -x[1])[:20]:
        pct = (count / total) * 100
        print(f"  {court}: {count:,} ({pct:.1f}%)")

    return domain_counts, court_counts


def main():
    parser = argparse.ArgumentParser(description="Classify decisions by court code")
    parser.add_argument("--input", required=True, help="Path to decisions.jsonl")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--progress", type=int, default=10000, help="Progress interval")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    classify_decisions(input_path, output_dir, args.progress)


if __name__ == "__main__":
    main()
