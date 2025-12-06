#!/usr/bin/env python
"""
Unified Pipeline Orchestrator
==============================

Runs the complete end-to-end pipeline:
1. Classification (with auto-queueing)
2. GSW Extraction (priority-based)
3. Graph Building

This orchestrator automatically triggers GSW extraction for high-authority
documents as they are classified, then builds the graph from extracted data.

Usage:
    # Run with defaults (authority threshold 60)
    python scripts/run_unified_pipeline.py

    # Run with custom threshold
    python scripts/run_unified_pipeline.py --authority-threshold 80 --limit 1000

    # Skip GSW extraction
    python scripts/run_unified_pipeline.py --no-gsw

    # Resume from checkpoint
    python scripts/run_unified_pipeline.py --resume
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
from src.ingestion.auto_gsw_trigger import GSWExtractionQueue, SmartSampler
from src.gsw.legal_operator import LegalOperator
from src.gsw.workspace import WorkspaceManager
from src.graph.spcnet_builder import SPCNetBuilder


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_CORPUS_PATH = Path("data/corpus.jsonl")
DEFAULT_OUTPUT_DIR = Path("data/processed/domains")
DEFAULT_WORKSPACE_DIR = Path("data/workspaces")
DEFAULT_GRAPH_DIR = Path("data/processed/graph")

# GSW extraction batch size
GSW_BATCH_SIZE = 10

# Checkpoint intervals
CLASSIFICATION_CHECKPOINT_INTERVAL = 5000
GSW_CHECKPOINT_INTERVAL = 50


# ============================================================================
# PIPELINE STAGES
# ============================================================================

class UnifiedPipeline:
    """
    Orchestrates the complete pipeline from corpus to graph.

    Stages:
    1. Classification: Domain classification with auto-GSW queuing
    2. GSW Extraction: Process high-authority documents
    3. Graph Building: Construct citation network
    """

    def __init__(
        self,
        corpus_path: Path = DEFAULT_CORPUS_PATH,
        output_dir: Path = DEFAULT_OUTPUT_DIR,
        workspace_dir: Path = DEFAULT_WORKSPACE_DIR,
        graph_dir: Path = DEFAULT_GRAPH_DIR,
        enable_gsw: bool = True,
        authority_threshold: int = 60,
        limit: Optional[int] = None,
        resume: bool = False
    ):
        self.corpus_path = corpus_path
        self.output_dir = output_dir
        self.workspace_dir = workspace_dir
        self.graph_dir = graph_dir
        self.enable_gsw = enable_gsw
        self.authority_threshold = authority_threshold
        self.limit = limit
        self.resume = resume

        # Initialize components
        self.gsw_queue = None
        self.extractor = None
        self.operator = None
        self.workspace_manager = None
        self.graph_builder = None

    def run(self) -> None:
        """Run the complete pipeline."""
        start_time = datetime.now()

        print("=" * 80)
        print("UNIFIED PIPELINE - Classification → GSW Extraction → Graph Building")
        print("=" * 80)
        print(f"Started: {start_time}")
        print(f"Corpus: {self.corpus_path}")
        print(f"GSW Enabled: {self.enable_gsw}")
        print(f"Authority Threshold: {self.authority_threshold}")
        print(f"Limit: {self.limit or 'None (full corpus)'}")
        print(f"Resume: {self.resume}")
        print("=" * 80)
        print()

        # Stage 1: Classification with auto-queueing
        print("[Stage 1/3] Classification + Auto-Queue")
        print("-" * 80)
        self._run_classification()
        print()

        # Stage 2: GSW Extraction (if enabled)
        if self.enable_gsw and self.gsw_queue:
            print("[Stage 2/3] GSW Extraction (Priority Queue)")
            print("-" * 80)
            self._run_gsw_extraction()
            print()
        else:
            print("[Stage 2/3] GSW Extraction - SKIPPED")
            print()

        # Stage 3: Graph Building
        print("[Stage 3/3] Graph Building")
        print("-" * 80)
        self._run_graph_building()
        print()

        # Summary
        elapsed = datetime.now() - start_time
        print("=" * 80)
        print(f"PIPELINE COMPLETE - Total time: {elapsed}")
        print("=" * 80)

    def _run_classification(self) -> None:
        """Stage 1: Classify documents and queue high-authority ones for GSW."""
        # Initialize queue if GSW enabled
        if self.enable_gsw:
            checkpoint_path = Path("data/processed/gsw_queue_checkpoint.json")
            self.gsw_queue = GSWExtractionQueue(
                min_authority=self.authority_threshold,
                checkpoint_path=checkpoint_path
            )

        # Initialize extractor
        self.extractor = CorpusDomainExtractor(
            input_path=self.corpus_path,
            output_dir=self.output_dir,
            enable_auto_gsw=self.enable_gsw,
            gsw_queue=self.gsw_queue,
            gsw_min_authority=self.authority_threshold
        )

        # Run extraction
        classification_start = datetime.now()
        stats = self.extractor.extract_all(
            progress_interval=CLASSIFICATION_CHECKPOINT_INTERVAL,
            resume=self.resume,
            limit=self.limit
        )

        elapsed = datetime.now() - classification_start
        total_docs = sum(s.document_count for s in stats.values())

        print(f"\n✓ Classification complete: {total_docs:,} documents in {elapsed}")

        # Show top domains
        print("\nTop domains:")
        for domain, stat in sorted(stats.items(), key=lambda x: -x[1].document_count)[:10]:
            if stat.document_count > 0:
                print(f"  {domain}: {stat.document_count:,}")

        # Show queue stats if enabled
        if self.gsw_queue:
            queue_stats = self.gsw_queue.get_statistics()
            print(f"\nGSW Queue statistics:")
            print(f"  Total queued: {queue_stats['total_queued']:,}")
            print(f"  Current size: {queue_stats['current_queue_size']:,}")
            print(f"  By court level:")
            for level, count in queue_stats['authority_stats'].items():
                print(f"    {level}: {count:,}")

            # Save checkpoint
            self.gsw_queue.save_checkpoint()

    def _run_gsw_extraction(self) -> None:
        """Stage 2: Process GSW extraction queue."""
        if not self.gsw_queue:
            print("No GSW queue available")
            return

        queue_size = self.gsw_queue.qsize()
        if queue_size == 0:
            print("Queue is empty - no documents to extract")
            return

        print(f"Processing {queue_size:,} documents from queue...\n")

        # Initialize operator
        try:
            self.operator = LegalOperator(
                model=["google/gemini-2.0-flash-exp", "google/gemini-1.5-flash"],
                use_openrouter=True,
                enable_validation=False,
                use_toon=True
            )
            print("✓ LegalOperator initialized")
        except Exception as e:
            print(f"✗ Failed to initialize LegalOperator: {e}")
            print("  Skipping GSW extraction...")
            return

        # Create workspace directory
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Process queue in batches
        batch_num = 0
        total_processed = 0
        start_time = datetime.now()

        while not self.gsw_queue.empty():
            batch_num += 1
            batch = self.gsw_queue.process_batch(batch_size=GSW_BATCH_SIZE)

            if not batch:
                break

            print(f"\n[Batch {batch_num}] Processing {len(batch)} documents...")

            for i, doc in enumerate(batch, 1):
                citation = doc.get('citation', 'Unknown')
                authority = doc.get('_classification', {}).get('authority_score', 0)
                domain = doc.get('_classification', {}).get('primary_domain', 'Unknown')

                print(f"  [{i}/{len(batch)}] {citation} (authority={authority}, domain={domain})")

                try:
                    # Extract GSW
                    text = doc.get('text', '')
                    if not text:
                        print(f"    ✗ No text content")
                        continue

                    extraction = self.operator.extract(
                        text=text[:30000],  # Limit text length
                        situation=f"{domain} case",
                        document_id=citation
                    )

                    # Save workspace for this document
                    workspace_file = self.workspace_dir / f"{self._sanitize_filename(citation)}_workspace.json"

                    # Create workspace from extraction
                    workspace_mgr = WorkspaceManager()
                    workspace_mgr.workspace.integrate_extraction(extraction)
                    workspace_mgr.save(workspace_file)

                    print(f"    ✓ Extracted: {len(extraction.actors)} actors, {len(extraction.questions)} questions")

                    # Mark as processed
                    self.gsw_queue.mark_processed(doc)
                    total_processed += 1

                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:100]}")
                    continue

            # Checkpoint after each batch
            if batch_num % GSW_CHECKPOINT_INTERVAL == 0:
                self.gsw_queue.save_checkpoint()
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = total_processed / elapsed if elapsed > 0 else 0
                print(f"\n[Checkpoint] Processed {total_processed} / {queue_size} ({rate:.1f} docs/sec)")

        # Final checkpoint
        self.gsw_queue.save_checkpoint()

        elapsed = datetime.now() - start_time
        print(f"\n✓ GSW extraction complete: {total_processed:,} documents in {elapsed}")

    def _run_graph_building(self) -> None:
        """Stage 3: Build citation graph from processed data."""
        print(f"Building graph from: {self.output_dir}")
        print(f"Output to: {self.graph_dir}\n")

        try:
            self.graph_builder = SPCNetBuilder(
                input_dir=self.output_dir,
                output_dir=self.graph_dir
            )

            graph_start = datetime.now()
            self.graph_builder.build()
            elapsed = datetime.now() - graph_start

            print(f"\n✓ Graph building complete in {elapsed}")

        except Exception as e:
            print(f"✗ Graph building failed: {e}")
            import traceback
            traceback.print_exc()

    def _sanitize_filename(self, citation: str) -> str:
        """Convert citation to safe filename."""
        # Replace problematic characters
        safe = citation.replace('[', '').replace(']', '')
        safe = safe.replace('/', '_').replace('\\', '_')
        safe = safe.replace(':', '_').replace(' ', '_')
        return safe[:100]  # Limit length


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run unified pipeline: Classification → GSW → Graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with defaults (authority threshold 60)
  python scripts/run_unified_pipeline.py

  # Run with custom threshold and limit
  python scripts/run_unified_pipeline.py --authority-threshold 80 --limit 1000

  # Skip GSW extraction
  python scripts/run_unified_pipeline.py --no-gsw

  # Resume from checkpoint
  python scripts/run_unified_pipeline.py --resume
        """
    )

    parser.add_argument(
        '--corpus', '-c',
        type=Path,
        default=DEFAULT_CORPUS_PATH,
        help='Path to corpus.jsonl'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help='Output directory for classified documents'
    )
    parser.add_argument(
        '--workspace-dir', '-w',
        type=Path,
        default=DEFAULT_WORKSPACE_DIR,
        help='Directory for GSW workspaces'
    )
    parser.add_argument(
        '--graph-dir', '-g',
        type=Path,
        default=DEFAULT_GRAPH_DIR,
        help='Directory for graph output'
    )
    parser.add_argument(
        '--authority-threshold', '-a',
        type=int,
        default=60,
        help='Minimum authority score for GSW extraction (0-100)'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='Limit number of documents to process'
    )
    parser.add_argument(
        '--no-gsw',
        action='store_true',
        help='Disable GSW extraction'
    )
    parser.add_argument(
        '--resume', '-r',
        action='store_true',
        help='Resume from checkpoint'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.corpus.exists():
        print(f"Error: Corpus file not found: {args.corpus}")
        sys.exit(1)

    # Run pipeline
    pipeline = UnifiedPipeline(
        corpus_path=args.corpus,
        output_dir=args.output,
        workspace_dir=args.workspace_dir,
        graph_dir=args.graph_dir,
        enable_gsw=not args.no_gsw,
        authority_threshold=args.authority_threshold,
        limit=args.limit,
        resume=args.resume
    )

    try:
        pipeline.run()
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nPipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
