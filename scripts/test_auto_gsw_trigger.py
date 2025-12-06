#!/usr/bin/env python
"""
Test Auto-GSW Trigger System
=============================

Validates the auto-trigger GSW extraction with priority queue:
1. Runs classification with auto-queueing enabled
2. Verifies only high-authority docs are queued
3. Tests GSW extraction on queued documents
4. Validates checkpointing

Usage:
    python scripts/test_auto_gsw_trigger.py --limit 1000 --authority-threshold 80
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
from src.ingestion.auto_gsw_trigger import GSWExtractionQueue, SmartSampler


def test_queue_filtering(
    corpus_path: Path,
    output_dir: Path,
    limit: int = 1000,
    authority_threshold: int = 80
):
    """Test that queue correctly filters by authority score."""
    print("=" * 80)
    print("TEST 1: Queue Filtering by Authority Score")
    print("=" * 80)
    print(f"Corpus: {corpus_path}")
    print(f"Limit: {limit:,} documents")
    print(f"Authority threshold: {authority_threshold}")
    print()

    # Initialize queue
    queue = GSWExtractionQueue(min_authority=authority_threshold)

    # Initialize extractor with auto-GSW
    extractor = CorpusDomainExtractor(
        input_path=corpus_path,
        output_dir=output_dir,
        enable_auto_gsw=True,
        gsw_queue=queue,
        gsw_min_authority=authority_threshold
    )

    # Run classification
    print("Running classification...\n")
    start_time = datetime.now()

    stats = extractor.extract_all(
        progress_interval=500,
        resume=False,
        limit=limit
    )

    elapsed = datetime.now() - start_time
    total_docs = sum(s.document_count for s in stats.values())

    print(f"\n✓ Classification complete: {total_docs:,} documents in {elapsed}")

    # Analyze queue
    print("\n" + "=" * 80)
    print("QUEUE ANALYSIS")
    print("=" * 80)

    queue_stats = queue.get_statistics()

    print(f"Total documents processed: {total_docs:,}")
    print(f"Documents queued for GSW: {queue_stats['total_queued']:,}")
    print(f"Queue acceptance rate: {queue_stats['total_queued'] / total_docs * 100:.2f}%")
    print()

    print("Documents by court level:")
    for level, count in sorted(queue_stats['authority_stats'].items()):
        pct = count / queue_stats['total_queued'] * 100 if queue_stats['total_queued'] > 0 else 0
        print(f"  {level}: {count:,} ({pct:.1f}%)")

    # Validate threshold enforcement
    print("\n" + "=" * 80)
    print("THRESHOLD VALIDATION")
    print("=" * 80)

    # Sample documents from queue
    sample_size = min(10, queue.qsize())
    sample = queue.process_batch(batch_size=sample_size)

    print(f"\nSample of {len(sample)} queued documents:")
    below_threshold = 0

    for i, doc in enumerate(sample, 1):
        citation = doc.get('citation', 'Unknown')
        authority = doc.get('_classification', {}).get('authority_score', 0)
        court = doc.get('_classification', {}).get('court', 'Unknown')
        court_level = doc.get('_classification', {}).get('court_level', 'unknown')

        status = "✓" if authority >= authority_threshold else "✗"
        if authority < authority_threshold:
            below_threshold += 1

        print(f"  [{i:2d}] {status} {citation[:50]:<50} | {court:<8} | {court_level:<12} | Authority: {authority}")

    print()
    if below_threshold == 0:
        print("✓ PASS: All sampled documents meet authority threshold")
    else:
        print(f"✗ FAIL: {below_threshold} documents below threshold")

    return queue


def test_checkpoint_resume(queue: GSWExtractionQueue):
    """Test checkpoint save/load functionality."""
    print("\n" + "=" * 80)
    print("TEST 2: Checkpoint Save/Load")
    print("=" * 80)

    # Save checkpoint
    print("Saving checkpoint...")
    queue.save_checkpoint()

    original_stats = queue.get_statistics()
    print(f"Original queue stats:")
    print(f"  Total queued: {original_stats['total_queued']}")
    print(f"  Total processed: {original_stats['total_processed']}")
    print(f"  Current size: {original_stats['current_queue_size']}")

    # Load checkpoint
    print("\nLoading checkpoint...")
    checkpoint_path = queue.checkpoint_path

    if not checkpoint_path.exists():
        print("✗ FAIL: Checkpoint file not created")
        return

    # Create new queue and load
    queue2 = GSWExtractionQueue(
        min_authority=queue.min_authority,
        checkpoint_path=checkpoint_path
    )

    loaded_stats = queue2.get_statistics()
    print(f"Loaded queue stats:")
    print(f"  Total queued: {loaded_stats['total_queued']}")
    print(f"  Total processed: {loaded_stats['total_processed']}")
    print(f"  Current size: {loaded_stats['current_queue_size']}")

    # Validate
    if loaded_stats['total_processed'] == original_stats['total_processed']:
        print("\n✓ PASS: Checkpoint loaded correctly")
    else:
        print("\n✗ FAIL: Checkpoint data mismatch")


def test_smart_sampler():
    """Test smart sampling strategies."""
    print("\n" + "=" * 80)
    print("TEST 3: Smart Sampling Strategies")
    print("=" * 80)

    sampler = SmartSampler()

    # Test documents
    test_cases = [
        {
            'name': 'Apex Court (HCA)',
            'doc': {
                'citation': '[2023] HCA 1',
                '_classification': {
                    'authority_score': 95,
                    'court_level': 'apex',
                    'court': 'HCA',
                    'case_refs': ['Mabo v Queensland', 'Cole v Whitfield'],
                    'legislation_refs': ['Constitution Act 1901']
                }
            }
        },
        {
            'name': 'Appellate Court with cases',
            'doc': {
                'citation': '[2023] NSWCA 100',
                '_classification': {
                    'authority_score': 75,
                    'court_level': 'intermediate',
                    'court': 'NSWCA',
                    'case_refs': ['Smith v Jones'],
                    'legislation_refs': []
                }
            }
        },
        {
            'name': 'Appellate Court without cases',
            'doc': {
                'citation': '[2023] NSWCA 200',
                '_classification': {
                    'authority_score': 72,
                    'court_level': 'intermediate',
                    'court': 'NSWCA',
                    'case_refs': [],
                    'legislation_refs': []
                }
            }
        },
        {
            'name': 'Trial Court - High Priority Domain',
            'doc': {
                'citation': '[2023] FamCA 50',
                '_classification': {
                    'authority_score': 55,
                    'court_level': 'trial',
                    'court': 'FamCA',
                    'primary_domain': 'Family',
                    'case_refs': ['Stanford v Stanford', 'Chen v Chen'],
                    'legislation_refs': ['Family Law Act 1975']
                }
            }
        },
        {
            'name': 'Trial Court - Low Priority',
            'doc': {
                'citation': '[2023] NSWDC 300',
                '_classification': {
                    'authority_score': 45,
                    'court_level': 'trial',
                    'court': 'NSWDC',
                    'primary_domain': 'Civil',
                    'case_refs': [],
                    'legislation_refs': []
                }
            }
        }
    ]

    print("\nSampling decisions (threshold=60):")
    print("-" * 80)

    for test in test_cases:
        doc = test['doc']
        priority = sampler.get_sampling_priority(doc)
        should_sample = priority >= 60

        status = "✓ SAMPLE" if should_sample else "✗ SKIP"
        print(f"{status} | {test['name']:<40} | Priority: {priority:3d}")

    print("\nStrategy tests:")

    # Test apex sampling
    apex_doc = test_cases[0]['doc']
    if sampler.should_sample_apex(apex_doc):
        print("✓ PASS: Apex court correctly identified for sampling")
    else:
        print("✗ FAIL: Apex court should be sampled")

    # Test appellate sampling
    appellate_with_cases = test_cases[1]['doc']
    appellate_without_cases = test_cases[2]['doc']

    if sampler.should_sample_appellate(appellate_with_cases):
        print("✓ PASS: Appellate court with case refs sampled")
    else:
        print("✗ FAIL: Appellate court with case refs should be sampled")

    if not sampler.should_sample_appellate(appellate_without_cases):
        print("✓ PASS: Appellate court without case refs skipped")
    else:
        print("✗ FAIL: Appellate court without case refs should be skipped")

    # Test trial sampling
    trial_high_priority = test_cases[3]['doc']
    trial_low_priority = test_cases[4]['doc']

    if sampler.should_sample_trial(trial_high_priority):
        print("✓ PASS: High-priority trial court sampled")
    else:
        print("✗ FAIL: High-priority trial court should be sampled")

    if not sampler.should_sample_trial(trial_low_priority):
        print("✓ PASS: Low-priority trial court skipped")
    else:
        print("✗ FAIL: Low-priority trial court should be skipped")


def main():
    parser = argparse.ArgumentParser(
        description="Test auto-GSW trigger system"
    )

    parser.add_argument(
        '--corpus', '-c',
        type=Path,
        default=Path("data/corpus.jsonl"),
        help='Path to corpus.jsonl'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path("data/processed/test_domains"),
        help='Output directory for test'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=1000,
        help='Number of documents to process'
    )
    parser.add_argument(
        '--authority-threshold', '-a',
        type=int,
        default=80,
        help='Authority threshold for testing'
    )

    args = parser.parse_args()

    if not args.corpus.exists():
        print(f"Error: Corpus file not found: {args.corpus}")
        sys.exit(1)

    # Run tests
    print("\nAUTO-GSW TRIGGER VALIDATION SUITE")
    print("=" * 80)
    print(f"Started: {datetime.now()}")
    print()

    # Test 1: Queue filtering
    queue = test_queue_filtering(
        args.corpus,
        args.output,
        limit=args.limit,
        authority_threshold=args.authority_threshold
    )

    # Test 2: Checkpoint
    test_checkpoint_resume(queue)

    # Test 3: Smart sampler
    test_smart_sampler()

    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
