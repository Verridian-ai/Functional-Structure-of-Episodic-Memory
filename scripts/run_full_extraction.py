#!/usr/bin/env python
"""
Run full corpus extraction with progress output.
"""
import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CORPUS_PATH = Path("data/corpus.jsonl")
OUTPUT_DIR = Path("data/processed/domains")
TOTAL_DOCS_ESTIMATE = 232560  # Estimated total documents

def progress_bar(current, total, width=40):
    """Create a progress bar string."""
    pct = current / total if total > 0 else 0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct*100:.1f}%"

def main():
    print("="*60)
    print("FULL CORPUS EXTRACTION - LOADING PROGRESS")
    print(f"Started: {datetime.now()}")
    print("="*60)

    # Get file size for progress
    file_size = CORPUS_PATH.stat().st_size
    print(f"Corpus: {file_size / 1e9:.2f} GB")
    print(f"Estimated docs: ~{TOTAL_DOCS_ESTIMATE:,}")
    print()

    # Loading classifier
    print("Loading classifier patterns...", flush=True)
    from src.ingestion.corpus_domain_extractor import (
        CorpusDomainExtractor, DomainFileManager, DomainClassifier
    )
    classifier = DomainClassifier()
    print(f"✓ Loaded {len(classifier.patterns)} keyword patterns")
    print(f"✓ Loaded {len(classifier.legislation_patterns)} legislation patterns")
    print(f"✓ Loaded {len(classifier.case_patterns)} case patterns")
    print()

    # Clear old state
    state_file = Path("data/processed/extraction_state.json")
    if state_file.exists():
        state_file.unlink()

    extractor = CorpusDomainExtractor(
        input_path=CORPUS_PATH,
        output_dir=OUTPUT_DIR
    )

    start_time = time.time()
    doc_count = 0
    bytes_read = 0

    print("Starting extraction...")
    print("-"*60)
    print("Doc Count | Progress | Rate | ETA", flush=True)

    last_print = time.time()

    with DomainFileManager(OUTPUT_DIR, append=False) as file_manager:
        with open(CORPUS_PATH, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile):
                bytes_read += len(line.encode('utf-8'))

                try:
                    doc = json.loads(line)
                    extractor._process_document(doc, file_manager, line_num)
                    doc_count += 1
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    continue

                # Progress every 2 seconds or every 1000 docs
                now = time.time()
                if now - last_print >= 2 or doc_count % 1000 == 0:
                    last_print = now
                    elapsed = now - start_time
                    rate = doc_count / elapsed if elapsed > 0 else 0
                    pct = (bytes_read / file_size) * 100
                    eta_sec = (file_size - bytes_read) / (bytes_read / elapsed) if bytes_read > 0 and elapsed > 0 else 0
                    eta_min = eta_sec / 60

                    print(f"{doc_count:>8,} | {pct:>5.1f}% | {rate:>6.0f}/s | {eta_min:>5.1f} min left", flush=True)

    # Save statistics
    extractor._save_statistics()

    elapsed = time.time() - start_time
    print()
    print("="*60)
    print(f"✓ COMPLETE: {doc_count:,} documents in {elapsed/60:.1f} minutes")
    print(f"  Rate: {doc_count/elapsed:.0f} docs/sec")
    print("="*60)
    print("\nDomain breakdown:")
    for domain, stat in sorted(extractor.stats.items(), key=lambda x: -x[1].document_count):
        if stat.document_count > 0:
            print(f"  {domain}: {stat.document_count:,}")

if __name__ == "__main__":
    main()


