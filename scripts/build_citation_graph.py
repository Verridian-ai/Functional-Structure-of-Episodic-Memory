"""
Build Citation Graph - Convenience Script
==========================================

Builds the SPCNet citation graph from classified domain files.
Generates TOON-formatted nodes and edges for TEM training.

Usage:
    # Build from all domains
    python scripts/build_citation_graph.py

    # Build from specific domain
    python scripts/build_citation_graph.py --domain family

    # Build with custom paths
    python scripts/build_citation_graph.py --input_dir data/processed/domains --output_dir data/processed/graph
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
import logging
from src.graph.spcnet_builder import SPCNetBuilder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def build_graph(input_dir: Path, output_dir: Path, domain_filter: str = None):
    """
    Build citation graph from domain files.

    Args:
        input_dir: Directory containing domain JSONL files
        output_dir: Directory to save graph TOON files
        domain_filter: Optional domain name to filter (e.g., 'family')
    """
    logger.info("=" * 70)
    logger.info("SPCNet Citation Graph Builder")
    logger.info("=" * 70)

    # If domain filter specified, create temporary directory with only that domain
    if domain_filter:
        logger.info(f"Building graph for domain: {domain_filter}")
        # Check if domain file exists
        domain_file = input_dir / f"{domain_filter.lower()}.jsonl"
        if not domain_file.exists():
            logger.error(f"Domain file not found: {domain_file}")
            return False

        # Create temp directory for single domain
        temp_input = input_dir / "_temp_single_domain"
        temp_input.mkdir(exist_ok=True)

        # Copy domain file to temp
        import shutil
        temp_domain_file = temp_input / domain_file.name
        shutil.copy(domain_file, temp_domain_file)

        # Use temp directory as input
        actual_input = temp_input
    else:
        logger.info("Building graph for all domains")
        actual_input = input_dir

    # Initialize builder
    builder = SPCNetBuilder(
        input_dir=actual_input,
        output_dir=output_dir
    )

    # Build graph
    try:
        logger.info("")
        logger.info("Starting graph build process...")
        builder.build()
        logger.info("")
        logger.info("Graph build completed successfully!")

        # Cleanup temp directory if used
        if domain_filter:
            import shutil
            shutil.rmtree(temp_input)

        return True

    except Exception as e:
        logger.error(f"Error building graph: {e}")
        import traceback
        traceback.print_exc()

        # Cleanup on error
        if domain_filter:
            import shutil
            if temp_input.exists():
                shutil.rmtree(temp_input)

        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build SPCNet citation graph from classified domain files."
    )

    parser.add_argument(
        '--input_dir',
        type=Path,
        default=Path('data/processed/domains'),
        help="Directory containing domain JSONL files (default: data/processed/domains)"
    )

    parser.add_argument(
        '--output_dir',
        type=Path,
        default=Path('data/processed/graph'),
        help="Output directory for graph TOON files (default: data/processed/graph)"
    )

    parser.add_argument(
        '--domain',
        type=str,
        default=None,
        help="Build graph for specific domain only (e.g., 'family', 'criminal')"
    )

    args = parser.parse_args()

    # Validate input directory
    if not args.input_dir.exists():
        logger.error(f"Input directory does not exist: {args.input_dir}")
        sys.exit(1)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Build graph
    success = build_graph(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        domain_filter=args.domain
    )

    if success:
        logger.info("")
        logger.info("Output files:")
        logger.info(f"  - Nodes: {args.output_dir / 'spcnet_nodes.toon'}")
        logger.info(f"  - Edges: {args.output_dir / 'spcnet_edges.toon'}")
        logger.info(f"  - Stats: {args.output_dir / 'graph_statistics.json'}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Verify graph with: python -m src.tem.legal_graph_builder")
        logger.info("  2. Train TEM with random walks")
        logger.info("")
        sys.exit(0)
    else:
        logger.error("Graph build failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
