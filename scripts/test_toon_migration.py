"""
Test script to verify TOON migration in corpus_domain_extractor.py

This script:
1. Runs the extractor on a limited number of documents (100)
2. Verifies the output folder structure
3. Validates TOON format in output files
4. Checks file sizes and compression
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
from src.utils.toon import ToonDecoder

def test_extraction():
    """Run extraction with 100 documents."""
    base_dir = Path(__file__).resolve().parents[1]
    input_path = base_dir / "data" / "corpus.jsonl"
    output_dir = base_dir / "data" / "processed" / "domains"

    print("=" * 80)
    print("TOON MIGRATION TEST")
    print("=" * 80)
    print(f"Input: {input_path}")
    print(f"Output: {output_dir}")
    print(f"Limit: 100 documents")
    print()

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return False

    # Run extraction
    extractor = CorpusDomainExtractor(
        input_path=input_path,
        output_dir=output_dir
    )

    stats = extractor.extract_all(
        progress_interval=25,
        resume=False,
        limit=100
    )

    print("\n" + "=" * 80)
    print("EXTRACTION COMPLETE - VERIFYING OUTPUT")
    print("=" * 80)

    return verify_output(output_dir, stats)

def verify_output(output_dir: Path, stats: dict):
    """Verify the output structure and TOON format."""

    print("\n1. FOLDER STRUCTURE CHECK:")
    print("-" * 80)

    # Check legislation folder
    legislation_dir = output_dir / "legislation"
    if legislation_dir.exists():
        print(f"[OK] Legislation folder exists: {legislation_dir}")
        acts_file = legislation_dir / "acts.toon"
        if acts_file.exists():
            print(f"  [OK] acts.toon exists ({acts_file.stat().st_size:,} bytes)")
        else:
            print(f"  [FAIL] acts.toon NOT FOUND")
    else:
        print(f"[FAIL] Legislation folder NOT FOUND")

    # Check cases folder
    cases_dir = output_dir / "cases"
    if cases_dir.exists():
        print(f"[OK] Cases folder exists: {cases_dir}")
        domain_folders = list(cases_dir.iterdir())
        print(f"  Found {len(domain_folders)} domain folders:")
        for domain_folder in sorted(domain_folders):
            if domain_folder.is_dir():
                toon_files = list(domain_folder.glob("*.toon"))
                if toon_files:
                    for toon_file in toon_files:
                        size = toon_file.stat().st_size
                        print(f"  [OK] {domain_folder.name}/{toon_file.name} ({size:,} bytes)")
                else:
                    print(f"  [FAIL] {domain_folder.name}/ (no .toon files)")
    else:
        print(f"[FAIL] Cases folder NOT FOUND")

    print("\n2. TOON FORMAT VALIDATION:")
    print("-" * 80)

    # Validate TOON files
    all_toon_files = []
    if legislation_dir.exists():
        all_toon_files.extend(legislation_dir.glob("*.toon"))
    if cases_dir.exists():
        all_toon_files.extend(cases_dir.rglob("*.toon"))

    valid_count = 0
    total_count = 0

    for toon_file in all_toon_files:
        total_count += 1
        try:
            # Read file
            with open(toon_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for TOON header pattern
            if "[" in content and "]" in content and "{" in content and "}" in content:
                # Try to decode
                decoded = ToonDecoder.decode(content)
                if decoded:
                    valid_count += 1
                    print(f"[OK] {toon_file.relative_to(output_dir)}")

                    # Print sample
                    for table_name, rows in decoded.items():
                        print(f"  Table: {table_name}, Rows: {len(rows)}")
                        if rows and len(rows) > 0:
                            # Show first row keys
                            print(f"  Columns: {', '.join(rows[0].keys())}")
                            # Show snippet of first citation
                            if 'citation' in rows[0]:
                                citation = rows[0]['citation'][:60]
                                print(f"  Sample: {citation}...")
                        break  # Only show first table
                else:
                    print(f"[FAIL] {toon_file.relative_to(output_dir)} - Failed to decode")
            else:
                print(f"[FAIL] {toon_file.relative_to(output_dir)} - Missing TOON header pattern")
        except Exception as e:
            print(f"[FAIL] {toon_file.relative_to(output_dir)} - Error: {e}")

    print(f"\nValidation: {valid_count}/{total_count} files passed")

    print("\n3. STATISTICS SUMMARY:")
    print("-" * 80)

    total_docs = sum(s.document_count for s in stats.values())
    print(f"Total documents processed: {total_docs}")
    print(f"Domains with documents: {len([d for d, s in stats.items() if s.document_count > 0])}")
    print("\nTop domains:")
    sorted_stats = sorted(stats.items(), key=lambda x: x[1].document_count, reverse=True)[:10]
    for domain, stat in sorted_stats:
        if stat.document_count > 0:
            print(f"  {domain}: {stat.document_count} docs")

    print("\n4. FILE SIZE ANALYSIS:")
    print("-" * 80)

    total_size = 0
    for toon_file in all_toon_files:
        total_size += toon_file.stat().st_size

    print(f"Total TOON file size: {total_size:,} bytes ({total_size/1024:.2f} KB)")
    if total_docs > 0:
        print(f"Average size per document: {total_size/total_docs:.0f} bytes")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    return valid_count == total_count and total_count > 0

if __name__ == "__main__":
    success = test_extraction()
    sys.exit(0 if success else 1)
