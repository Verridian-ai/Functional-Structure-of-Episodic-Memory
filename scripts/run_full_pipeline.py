#!/usr/bin/env python3
"""
Run Full Pipeline - End-to-End Corpus Processing

This script is the main entry point for running the complete legal corpus
processing pipeline from raw documents to query-ready system.

Usage Examples:

    # Run full pipeline with default settings
    python scripts/run_full_pipeline.py

    # Run with document limit (testing)
    python scripts/run_full_pipeline.py --limit 100

    # Run specific stages only
    python scripts/run_full_pipeline.py --stages classify gsw

    # Run with custom config file
    python scripts/run_full_pipeline.py --config configs/production.yaml

    # Resume from checkpoint
    python scripts/run_full_pipeline.py --resume

    # Override specific settings
    python scripts/run_full_pipeline.py --limit 1000 --authority-threshold 70

Stages:
    - classify: Classify documents into legal domains
    - gsw: Extract Global Semantic Workspace from high-authority cases
    - graph: Build citation network (Hier-SPCNet)
    - index: Create search indices (future)
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline.config import PipelineConfig, create_example_config
from src.pipeline.orchestrator import FullPipeline


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run full corpus processing pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Configuration
    parser.add_argument(
        "--config", "-c",
        type=Path,
        help="Path to YAML configuration file"
    )

    # Stages
    parser.add_argument(
        "--stages", "-s",
        nargs="+",
        choices=["classify", "gsw", "graph", "index"],
        help="Stages to run (default: all)"
    )

    # Resume
    parser.add_argument(
        "--resume", "-r",
        action="store_true",
        help="Resume from checkpoint"
    )

    # Input/Output overrides
    parser.add_argument(
        "--corpus",
        type=Path,
        help="Path to corpus.jsonl file"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for processed data"
    )

    parser.add_argument(
        "--workspaces",
        type=Path,
        help="Output directory for GSW workspaces"
    )

    parser.add_argument(
        "--graph-dir",
        type=Path,
        help="Output directory for graph data"
    )

    # Processing options
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of documents to process (for testing)"
    )

    parser.add_argument(
        "--authority-threshold", "-a",
        type=int,
        help="Minimum authority score for GSW extraction (0-100)"
    )

    parser.add_argument(
        "--disable-gsw",
        action="store_true",
        help="Disable automatic GSW extraction"
    )

    parser.add_argument(
        "--disable-graph",
        action="store_true",
        help="Disable graph building"
    )

    parser.add_argument(
        "--disable-checkpoints",
        action="store_true",
        help="Disable checkpointing"
    )

    # GSW settings
    parser.add_argument(
        "--gsw-model",
        type=str,
        help="Model to use for GSW extraction"
    )

    parser.add_argument(
        "--gsw-batch-size",
        type=int,
        help="Batch size for GSW extraction"
    )

    parser.add_argument(
        "--gsw-delay",
        type=float,
        help="Delay between GSW API calls (seconds)"
    )

    # Utility commands
    parser.add_argument(
        "--create-example-config",
        type=Path,
        metavar="PATH",
        help="Create example configuration file and exit"
    )

    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate configuration and exit"
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show configuration summary and exit"
    )

    # Logging
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--log-file",
        type=Path,
        help="Path to log file"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Handle utility commands
    if args.create_example_config:
        create_example_config(args.create_example_config)
        return 0

    # Load configuration
    if args.config:
        print(f"Loading configuration from: {args.config}")
        config = PipelineConfig.from_yaml(args.config)
    else:
        print("Using default configuration")
        config = PipelineConfig()

    # Apply command-line overrides
    if args.corpus:
        config.corpus_path = args.corpus
    if args.output:
        config.output_dir = args.output
    if args.workspaces:
        config.workspace_dir = args.workspaces
    if args.graph_dir:
        config.graph_dir = args.graph_dir

    if args.limit is not None:
        config.document_limit = args.limit
    if args.authority_threshold is not None:
        config.gsw_authority_threshold = args.authority_threshold

    if args.disable_gsw:
        config.enable_auto_gsw = False
    if args.disable_graph:
        config.enable_graph_building = False
    if args.disable_checkpoints:
        config.enable_checkpoints = False

    if args.gsw_model:
        config.gsw_model = args.gsw_model
    if args.gsw_batch_size is not None:
        config.gsw_batch_size = args.gsw_batch_size
    if args.gsw_delay is not None:
        config.gsw_delay = args.gsw_delay

    if args.verbose:
        config.verbose = True
    if args.log_file:
        config.log_file = args.log_file

    # Validate configuration
    errors = config.validate()
    if errors:
        print("\n[Error] Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    # Show configuration if requested
    if args.show_config or args.validate_config:
        print("\n" + config.summary())
        if args.validate_config:
            print("\nConfiguration is valid!")
        return 0

    # Run pipeline
    try:
        pipeline = FullPipeline(config)
        state = pipeline.run(
            stages=args.stages,
            resume=args.resume
        )

        # Check if all stages succeeded
        all_success = all(
            result.success
            for result in state.stage_results.values()
        )

        if all_success:
            print("\n[Success] Pipeline completed successfully!")
            return 0
        else:
            print("\n[Warning] Pipeline completed with errors")
            return 1

    except KeyboardInterrupt:
        print("\n\n[Interrupted] Pipeline stopped by user")
        print("[Info] Progress has been checkpointed and can be resumed with --resume")
        return 130

    except Exception as e:
        print(f"\n[Error] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
