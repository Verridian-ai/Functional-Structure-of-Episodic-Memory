#!/usr/bin/env python
"""
Long-running corpus extraction with progress tracking.
Designed to run for 48+ hours with checkpoints and resume capability.

Usage:
    python scripts/run_corpus_labeling.py          # Fresh start
    python scripts/run_corpus_labeling.py --resume # Resume from checkpoint
"""
import json
import logging
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CORPUS_PATH = Path("data/corpus.jsonl")
OUTPUT_DIR = Path("data/processed/domains")
STATE_FILE = Path("data/processed/extraction_state.json")
CHECKPOINT_INTERVAL = 10000  # Save state every N docs

def format_time(seconds):
    """Format seconds as HH:MM:SS."""
    return str(timedelta(seconds=int(seconds)))

def format_eta(seconds):
    """Format ETA nicely."""
    if seconds < 3600:
        return f"{seconds/60:.1f} min"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hrs"
    else:
        return f"{seconds/86400:.1f} days"

def load_checkpoint():
    """Load checkpoint if exists."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load checkpoint: {e}")
    return None

def save_checkpoint(line_num, doc_count, bytes_read, elapsed, domain_counts):
    """Save checkpoint for resume."""
    state = {
        "last_line": line_num,
        "doc_count": doc_count,
        "bytes_read": bytes_read,
        "elapsed_seconds": elapsed,
        "saved_at": datetime.now().isoformat(),
        "domain_counts": domain_counts
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()
    
    print("=" * 70)
    print("  CORPUS DOMAIN LABELING - LONG RUNNING PROCESS (48+ hours)")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Corpus:  {CORPUS_PATH}")
    print(f"  Output:  {OUTPUT_DIR}")
    print("=" * 70)
    
    file_size = CORPUS_PATH.stat().st_size
    print(f"\n  Corpus size: {file_size / 1e9:.2f} GB")
    
    print("\n  Loading classifier...", flush=True)
    from src.ingestion.corpus_domain_extractor import (
        CorpusDomainExtractor, DomainFileManager
    )
    
    extractor = CorpusDomainExtractor(CORPUS_PATH, OUTPUT_DIR)
    print(f"  ✓ {len(extractor.classifier.patterns)} keyword patterns")
    print(f"  ✓ {len(extractor.classifier.legislation_names)} legislation refs")
    print(f"  ✓ {len(extractor.classifier.case_names)} case refs")
    
    start_line = 0
    start_bytes = 0
    elapsed_before = 0
    append_mode = False
    
    if args.resume:
        checkpoint = load_checkpoint()
        if checkpoint:
            start_line = checkpoint.get("last_line", 0)
            start_bytes = checkpoint.get("bytes_read", 0)
            elapsed_before = checkpoint.get("elapsed_seconds", 0)
            append_mode = True
            print(f"\n  ✓ RESUMING from line {start_line:,}")
            print(f"    Already processed: {start_bytes/1e9:.2f} GB")
        else:
            print("\n  No checkpoint found, starting fresh")
    
    print("\n" + "-" * 70)
    print(f"  {'Documents':>12} | {'Progress':>8} | {'Rate':>10} | {'Elapsed':>12} | {'ETA':>12}")
    print("-" * 70)
    
    start_time = time.time()
    last_print = start_time
    doc_count = 0
    bytes_read = start_bytes
    
    try:
        with DomainFileManager(OUTPUT_DIR, append=append_mode) as file_manager:
            with open(CORPUS_PATH, 'r', encoding='utf-8') as infile:
                for line_num, line in enumerate(infile):
                    if line_num < start_line:
                        continue
                    
                    bytes_read += len(line.encode('utf-8'))
                    
                    try:
                        doc = json.loads(line)
                        extractor._process_document(doc, file_manager, line_num)
                        doc_count += 1
                    except:
                        continue
                    
                    now = time.time()
                    
                    # Progress every 10 seconds
                    if now - last_print >= 10:
                        last_print = now
                        session_elapsed = now - start_time
                        total_elapsed = session_elapsed + elapsed_before
                        rate = doc_count / session_elapsed if session_elapsed > 0 else 0
                        pct = (bytes_read / file_size) * 100
                        
                        if bytes_read > start_bytes and session_elapsed > 0:
                            bytes_per_sec = (bytes_read - start_bytes) / session_elapsed
                            eta_sec = (file_size - bytes_read) / bytes_per_sec
                        else:
                            eta_sec = 0
                        
                        print(f"  {doc_count:>12,} | {pct:>7.2f}% | {rate:>8.1f}/s | {format_time(total_elapsed):>12} | {format_eta(eta_sec):>12}", flush=True)
                    
                    # Checkpoint every N docs
                    if doc_count % CHECKPOINT_INTERVAL == 0 and doc_count > 0:
                        domain_counts = {d: s.document_count for d, s in extractor.stats.items()}
                        total_elapsed = (now - start_time) + elapsed_before
                        save_checkpoint(line_num, doc_count, bytes_read, total_elapsed, domain_counts)
    
    except KeyboardInterrupt:
        print("\n\n  *** INTERRUPTED - Saving checkpoint ***")
        domain_counts = {d: s.document_count for d, s in extractor.stats.items()}
        total_elapsed = (time.time() - start_time) + elapsed_before
        save_checkpoint(line_num, doc_count, bytes_read, total_elapsed, domain_counts)
        print(f"  Saved at line {line_num:,}, {doc_count:,} docs")
        print("  Run with --resume to continue")
        return
    
    extractor._save_statistics()
    
    total_elapsed = (time.time() - start_time) + elapsed_before
    print("\n" + "=" * 70)
    print(f"  ✓ COMPLETE!")
    print(f"  Documents: {doc_count:,}")
    print(f"  Time: {format_time(total_elapsed)}")
    print(f"  Rate: {doc_count/total_elapsed:.1f} docs/sec" if total_elapsed > 0 else "")
    print("=" * 70)
    print("\n  Domain breakdown:")
    for domain, stat in sorted(extractor.stats.items(), key=lambda x: -x[1].document_count):
        if stat.document_count > 0:
            print(f"    {domain}: {stat.document_count:,}")

if __name__ == "__main__":
    main()

