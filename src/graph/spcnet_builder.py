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

# Regex for Australian Case Citations (Enhanced)
# Matches: [2023] HCA 1, (2023) 123 CLR 456, etc.
CITATION_PATTERNS = [
    re.compile(r'\[(\d{4})\]\s+([A-Z][A-Z]+[A-Za-z]*)\s+(\d+)'),  # [2023] HCA 1
    re.compile(r'\((\d{4})\)\s+(\d+)\s+([A-Z][A-Z]+[A-Za-z]*)\s+(\d+)'),  # (2023) 97 ALJR 123
    re.compile(r'\[(\d{4})\]\s+([A-Z]+SC[A-Z]*)\s+(\d+)'),  # [2023] NSWSC 456
]

# Action type patterns for citation context analysis
ACTION_PATTERNS = {
    'followed': re.compile(r'\b(follow(?:ing|ed|s)?|appli(?:ed|es|ying)|adopt(?:ed|s|ing))\b', re.IGNORECASE),
    'distinguished': re.compile(r'\b(distinguish(?:ed|es|ing)?|differ(?:s|ed|ent)?)\b', re.IGNORECASE),
    'overruled': re.compile(r'\b(overrul(?:ed|es|ing)?|overturn(?:ed|s|ing)?|reject(?:ed|s|ing)?)\b', re.IGNORECASE),
    'considered': re.compile(r'\b(consider(?:ed|s|ing)?|discuss(?:ed|es|ing)?|analyz(?:ed|es|ing)?)\b', re.IGNORECASE),
}

from src.utils.toon import ToonDecoder, ToonEncoder

class SPCNetBuilder:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.nodes: Dict[str, Dict] = {}  # Full Citation -> Metadata
        self.edges: List[Tuple[str, str, str]] = []  # (Source, Target, Type)
        self.citation_index: Set[str] = set()  # Full citations
        self.short_to_full: Dict[str, str] = {}  # Short form -> Full citation mapping

    def _extract_short_citation(self, full_citation: str) -> str:
        """
        Extract short form citation from full citation.
        E.g., "Smith v Jones [2020] HCA 1" -> "[2020] HCA 1"
        """
        for pattern in CITATION_PATTERNS:
            match = pattern.search(full_citation)
            if match:
                return match.group(0)
        return full_citation  # Return full if no pattern found

    def build(self):
        """Main build process."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Pass 1: Index all nodes (Cases)
        logger.info("Pass 1: Indexing Nodes...")
        self._index_nodes()
        logger.info(f"Indexed {len(self.nodes)} nodes.")
        logger.info(f"Built short-form index with {len(self.short_to_full)} mappings.")

        # Pass 2: Extract Edges (Citations)
        logger.info("Pass 2: Extracting Edges...")
        self._extract_edges()
        logger.info(f"Extracted {len(self.edges)} edges.")

        # Export
        self._export()

    def _index_nodes(self):
        """Scan all files to build the node index."""
        # Support both JSONL and TOON formats
        jsonl_files = list(self.input_dir.rglob('*.jsonl'))
        toon_files = list(self.input_dir.rglob('*.toon'))

        # Process JSONL files (current format)
        for file_path in jsonl_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        doc = json.loads(line)
                        citation = doc.get('citation', '').strip()

                        if citation:
                            classification = doc.get('_classification', {})
                            self.nodes[citation] = {
                                'id': citation,
                                'title': doc.get('citation', ''),
                                'date': doc.get('date', ''),
                                'court': classification.get('court', ''),
                                'type': doc.get('type', 'case'),
                                'domain': classification.get('primary_domain', ''),
                                'category': classification.get('primary_category', ''),
                                'text': doc.get('text', '')  # Store for edge extraction
                            }
                            self.citation_index.add(citation)

                            # Build short-form mapping for citation matching
                            short_form = self._extract_short_citation(citation)
                            if short_form != citation:  # Only map if we found a short form
                                self.short_to_full[short_form] = citation
            except Exception as e:
                logger.error(f"Error parsing JSONL {file_path}: {e}")
                continue

        # Process TOON files (future format)
        for file_path in toon_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                tables = ToonDecoder.decode(content)
                for table_name, rows in tables.items():
                    for row in rows:
                        citation = row.get('citation')
                        if citation:
                            citation = citation.strip()
                            self.nodes[citation] = {
                                'id': citation,
                                'title': row.get('category', ''),
                                'date': '',
                                'court': row.get('court', ''),
                                'type': row.get('type', 'case'),
                                'domain': row.get('domain', ''),
                                'category': row.get('category', ''),
                                'text': row.get('text', '')
                            }
                            self.citation_index.add(citation)

                            # Build short-form mapping
                            short_form = self._extract_short_citation(citation)
                            if short_form != citation:
                                self.short_to_full[short_form] = citation
            except Exception as e:
                logger.error(f"Error parsing TOON {file_path}: {e}")
                continue

    def _extract_citations_from_text(self, text: str, source_citation: str) -> List[str]:
        """
        Extract all unique citations from text using multiple patterns.
        Filters out self-references by comparing short forms.
        """
        citations = set()
        source_short = self._extract_short_citation(source_citation)

        for pattern in CITATION_PATTERNS:
            matches = pattern.finditer(text)
            for match in matches:
                citation_short = match.group(0).strip()
                # Exclude self-references (compare short forms)
                if citation_short != source_short:
                    citations.add(citation_short)

        return list(citations)

    def _classify_citation_action(self, text: str, cited_case: str) -> str:
        """
        Classify the action type based on citation context.

        Looks at text surrounding the citation to determine relationship:
        - followed: Case was followed/applied
        - distinguished: Case was distinguished
        - overruled: Case was overruled/rejected
        - considered: Case was merely considered/discussed
        - cited: Default (no specific context found)
        """
        # Find position of citation in text
        citation_pos = text.find(cited_case)
        if citation_pos == -1:
            return 'cited'

        # Extract context window (500 chars before/after)
        context_start = max(0, citation_pos - 500)
        context_end = min(len(text), citation_pos + len(cited_case) + 500)
        context = text[context_start:context_end]

        # Check for action patterns (prioritized order)
        for action, pattern in ACTION_PATTERNS.items():
            if pattern.search(context):
                return action

        return 'cited'  # Default

    def _extract_edges(self):
        """Extract citation edges from indexed nodes."""
        logger.info("Extracting edges from node texts...")

        edges_found = 0
        edges_matched = 0

        for citation, node in self.nodes.items():
            text = node.get('text', '')
            if not text:
                continue

            # Extract short-form citations from text
            found_citations = self._extract_citations_from_text(text, citation)
            edges_found += len(found_citations)

            for short_citation in found_citations:
                # Map short form to full citation
                full_target = self.short_to_full.get(short_citation, short_citation)

                # Only create edge if target exists in our index
                if full_target in self.citation_index:
                    # Classify the action type
                    action = self._classify_citation_action(text, short_citation)
                    self.edges.append((citation, full_target, action.upper()))
                    edges_matched += 1

        logger.info(f"Found {edges_found} citation patterns, matched {edges_matched} to indexed nodes")
        logger.info(f"Extracted {len(self.edges)} citation relationships")

    def _export(self):
        """Export nodes and edges to TOON."""
        nodes_path = self.output_dir / "spcnet_nodes.toon"
        edges_path = self.output_dir / "spcnet_edges.toon"
        stats_path = self.output_dir / "graph_statistics.json"

        logger.info(f"Exporting nodes to {nodes_path}")

        # Convert nodes to list format for ToonEncoder (without text)
        node_headers = ["id", "title", "court", "type", "domain", "category", "date"]
        node_rows = []
        for n in self.nodes.values():
            node_rows.append([
                n['id'],
                n['title'],
                n['court'],
                n['type'],
                n['domain'],
                n.get('category', ''),
                n.get('date', '')
            ])

        with open(nodes_path, 'w', encoding='utf-8') as f:
            f.write(ToonEncoder.encode("Nodes", node_headers, node_rows))

        logger.info(f"Exporting edges to {edges_path}")

        edge_headers = ["source", "target", "action"]
        edge_rows = [[s, t, r] for s, t, r in self.edges]

        with open(edges_path, 'w', encoding='utf-8') as f:
            f.write(ToonEncoder.encode("Edges", edge_headers, edge_rows))

        # Generate and export statistics
        logger.info(f"Generating statistics...")
        stats = self._generate_statistics()

        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        logger.info(f"Graph statistics saved to {stats_path}")

        # Print summary
        logger.info("=" * 60)
        logger.info(f"GRAPH BUILD COMPLETE")
        logger.info(f"Nodes: {stats['node_count']}")
        logger.info(f"Edges: {stats['edge_count']}")
        logger.info(f"Graph Density: {stats['density']:.6f}")
        logger.info(f"Avg Out-Degree: {stats['avg_out_degree']:.2f}")
        logger.info("=" * 60)

    def _generate_statistics(self) -> Dict:
        """Generate graph statistics."""
        node_count = len(self.nodes)
        edge_count = len(self.edges)

        # Calculate density: edges / (nodes * (nodes - 1))
        max_edges = node_count * (node_count - 1) if node_count > 1 else 1
        density = edge_count / max_edges if max_edges > 0 else 0

        # Calculate degree distribution
        out_degree = defaultdict(int)
        in_degree = defaultdict(int)
        action_counts = defaultdict(int)

        for source, target, action in self.edges:
            out_degree[source] += 1
            in_degree[target] += 1
            action_counts[action] += 1

        avg_out_degree = sum(out_degree.values()) / node_count if node_count > 0 else 0
        avg_in_degree = sum(in_degree.values()) / node_count if node_count > 0 else 0

        # Domain distribution
        domain_counts = defaultdict(int)
        for node in self.nodes.values():
            domain = node.get('domain', 'Unknown')
            domain_counts[domain] += 1

        return {
            'node_count': node_count,
            'edge_count': edge_count,
            'density': density,
            'avg_out_degree': avg_out_degree,
            'avg_in_degree': avg_in_degree,
            'max_out_degree': max(out_degree.values()) if out_degree else 0,
            'max_in_degree': max(in_degree.values()) if in_degree else 0,
            'action_distribution': dict(action_counts),
            'domain_distribution': dict(domain_counts),
            'isolated_nodes': node_count - len(set(out_degree.keys()) | set(in_degree.keys()))
        }

def main():
    parser = argparse.ArgumentParser(description="Build Hier-SPCNet from OALC data.")
    parser.add_argument('--input_dir', type=Path, default=Path('data/by_court'), help="Directory containing JSONL files.")
    parser.add_argument('--output_dir', type=Path, default=Path('data/processed/graph'), help="Output directory for graph data.")
    
    args = parser.parse_args()
    
    builder = SPCNetBuilder(args.input_dir, args.output_dir)
    builder.build()

if __name__ == '__main__':
    main()

