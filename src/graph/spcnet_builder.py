"""
Hier-SPCNet Builder
===================

Constructs the Hierarchical Statute and Precedent Citation Network (Hier-SPCNet)
from the ingested OALC data.

This module:
1.  Iterates through processed JSONL files (by_court or by_source).
2.  Extracts the primary citation for each case (Node).
3.  Parses case text to find citations to other cases/statutes (Edges).
4.  Builds a graph structure (Adjacency List).
5.  Exports nodes and edges for graph database ingestion (e.g., Neo4j).

Usage:
    python -m src.graph.spcnet_builder --input_dir data/by_court --output_dir data/processed/graph
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Regex for Australian Case Citations (Simplified)
# Matches: [2023] HCA 1, (2023) 123 CLR 456, etc.
CITATION_PATTERN = re.compile(r'\[\d{4}\]\s+[A-Z]+\w+\s+\d+|\(\d{4}\)\s+\d+\s+[A-Z]+\w+\s+\d+')

class SPCNetBuilder:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.nodes: Dict[str, Dict] = {}  # Citation -> Metadata
        self.edges: List[Tuple[str, str, str]] = []  # (Source, Target, Type)
        self.citation_index: Set[str] = set()

    def build(self):
        """Main build process."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Pass 1: Index all nodes (Cases)
        logger.info("Pass 1: Indexing Nodes...")
        self._index_nodes()
        logger.info(f"Indexed {len(self.nodes)} nodes.")

        # Pass 2: Extract Edges (Citations)
        logger.info("Pass 2: Extracting Edges...")
        self._extract_edges()
        logger.info(f"Extracted {len(self.edges)} edges.")

        # Export
        self._export()

    def _index_nodes(self):
        """Scan all files to build the node index."""
        files = list(self.input_dir.glob('*.jsonl'))
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        doc = json.loads(line)
                        citation = doc.get('citation')
                        if citation:
                            # Normalize citation
                            citation = citation.strip()
                            self.nodes[citation] = {
                                'id': citation,
                                'title': doc.get('name', ''),
                                'date': doc.get('date', ''),
                                'court': doc.get('jurisdiction', ''),
                                'type': doc.get('type', 'case')
                            }
                            self.citation_index.add(citation)
                    except json.JSONDecodeError:
                        continue

    def _extract_edges(self):
        """Scan files again to find citations in text."""
        files = list(self.input_dir.glob('*.jsonl'))
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        doc = json.loads(line)
                        source_citation = doc.get('citation')
                        if not source_citation:
                            continue
                        
                        source_citation = source_citation.strip()
                        text = doc.get('text', '')
                        
                        # Find all citation matches
                        matches = CITATION_PATTERN.findall(text)
                        
                        # Deduplicate matches per case
                        unique_matches = set(matches)
                        
                        for target_citation in unique_matches:
                            # Self-citation check
                            if target_citation == source_citation:
                                continue
                                
                            # We capture the edge even if the target isn't in our node index
                            # (It might be an external case or one we missed)
                            self.edges.append((source_citation, target_citation, 'CITES'))
                            
                    except json.JSONDecodeError:
                        continue

    def _export(self):
        """Export nodes and edges to JSONL."""
        nodes_path = self.output_dir / "spcnet_nodes.jsonl"
        edges_path = self.output_dir / "spcnet_edges.jsonl"

        logger.info(f"Exporting nodes to {nodes_path}")
        with open(nodes_path, 'w', encoding='utf-8') as f:
            for node in self.nodes.values():
                f.write(json.dumps(node) + '\n')

        logger.info(f"Exporting edges to {edges_path}")
        with open(edges_path, 'w', encoding='utf-8') as f:
            for source, target, rel_type in self.edges:
                edge = {
                    'source': source,
                    'target': target,
                    'type': rel_type
                }
                f.write(json.dumps(edge) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Build Hier-SPCNet from OALC data.")
    parser.add_argument('--input_dir', type=Path, default=Path('data/by_court'), help="Directory containing JSONL files.")
    parser.add_argument('--output_dir', type=Path, default=Path('data/processed/graph'), help="Output directory for graph data.")
    
    args = parser.parse_args()
    
    builder = SPCNetBuilder(args.input_dir, args.output_dir)
    builder.build()

if __name__ == '__main__':
    main()

