#!/usr/bin/env python3
"""
Visualization Data Generator
=============================

Generates visualization-ready JSON from pipeline output for the LAW OS frontend.

This script is the bridge between the backend pipeline (run_full_pipeline.py)
and the frontend visualization (LegalGraph3D.tsx).

Output Format:
- visualization_data.json: Complete graph with nodes, edges, and metadata
- visualization_stats.json: Statistics for dashboard display
- domain_summary.json: Per-domain statistics for filtering

Usage:
    python scripts/generate_visualization_data.py
    python scripts/generate_visualization_data.py --limit 5000
    python scripts/generate_visualization_data.py --output ui/public/data
"""

import sys
import json
import math
import random
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# Court hierarchy colors (matching frontend)
COURT_COLORS = {
    # Apex Courts
    'HCA': '#fbbf24',      # Gold - High Court of Australia

    # Federal Courts
    'FCA': '#3b82f6',      # Blue - Federal Court
    'FCAFC': '#3b82f6',    # Blue - Federal Court Full Court
    'FedCFamC': '#60a5fa', # Light Blue - Federal Circuit

    # Family Courts
    'FamCA': '#ec4899',    # Pink - Family Court
    'FamCAFC': '#ec4899',  # Pink - Family Court Full Court

    # NSW Courts
    'NSWSC': '#22c55e',    # Green - NSW Supreme Court
    'NSWCA': '#a855f7',    # Purple - NSW Court of Appeal
    'NSWCCA': '#ef4444',   # Red - NSW Court of Criminal Appeal
    'NSWLEC': '#84cc16',   # Lime - NSW Land & Environment
    'NSWCATAD': '#f97316', # Orange - NSW Civil & Admin Tribunal

    # VIC Courts
    'VSC': '#10b981',      # Emerald - VIC Supreme Court
    'VSCA': '#8b5cf6',     # Violet - VIC Court of Appeal

    # QLD Courts
    'QSC': '#14b8a6',      # Teal - QLD Supreme Court
    'QCA': '#7c3aed',      # Indigo - QLD Court of Appeal

    # WA Courts
    'WASC': '#06b6d4',     # Cyan - WA Supreme Court
    'WASCA': '#06b6d4',    # Cyan - WA Supreme Court of Appeal

    # SA Courts
    'SASC': '#0ea5e9',     # Sky - SA Supreme Court
    'SASCFC': '#0ea5e9',   # Sky - SA Supreme Full Court

    # Other
    'AAT': '#f97316',      # Orange - Admin Appeals Tribunal
    'FWC': '#eab308',      # Yellow - Fair Work Commission
    'default': '#94a3b8',  # Gray - Unknown/Other
}

# Domain colors
DOMAIN_COLORS = {
    'Family': '#ec4899',
    'Criminal': '#ef4444',
    'Commercial': '#3b82f6',
    'Property': '#22c55e',
    'Administrative': '#f97316',
    'Employment': '#eab308',
    'Torts': '#8b5cf6',
    'Health': '#10b981',
    'Resources': '#14b8a6',
    'Education': '#06b6d4',
    'Privacy': '#a855f7',
    'Procedural': '#94a3b8',
    'Equity': '#fbbf24',
    'Tax': '#0ea5e9',
    'Environment': '#84cc16',
    'Constitutional': '#fbbf24',
    'Immigration': '#7c3aed',
    'default': '#6b7280',
}

# Court level hierarchy (for Y-axis positioning)
COURT_LEVELS = {
    'apex': 100,        # High Court
    'superior_appellate': 80,  # Courts of Appeal
    'superior_trial': 60,      # Supreme Courts
    'specialist': 40,          # Land & Environment, Family
    'tribunal': 20,            # AAT, NCAT, etc.
    'default': 50,
}


def detect_court_code(node_id: str) -> str:
    """Extract court code from case citation."""
    id_upper = node_id.upper()

    # Order matters - check specific codes first
    court_patterns = [
        ('FCAFC', 'FCAFC'),
        ('FCA', 'FCA'),
        ('HCA', 'HCA'),
        ('FamCAFC', 'FamCAFC'),
        ('FamCA', 'FamCA'),
        ('NSWCCA', 'NSWCCA'),
        ('NSWCA', 'NSWCA'),
        ('NSWSC', 'NSWSC'),
        ('NSWLEC', 'NSWLEC'),
        ('NSWCATAD', 'NSWCATAD'),
        ('VSCA', 'VSCA'),
        ('VSC', 'VSC'),
        ('QCA', 'QCA'),
        ('QSC', 'QSC'),
        ('WASCA', 'WASCA'),
        ('WASC', 'WASC'),
        ('SASCFC', 'SASCFC'),
        ('SASC', 'SASC'),
        ('AAT', 'AAT'),
        ('FWC', 'FWC'),
    ]

    for pattern, code in court_patterns:
        if pattern in id_upper:
            return code

    return 'default'


def detect_court_level(court_code: str) -> str:
    """Determine court level from code."""
    level_map = {
        'HCA': 'apex',
        'FCAFC': 'superior_appellate',
        'FCA': 'superior_trial',
        'FamCAFC': 'superior_appellate',
        'FamCA': 'specialist',
        'NSWCA': 'superior_appellate',
        'NSWCCA': 'superior_appellate',
        'NSWSC': 'superior_trial',
        'NSWLEC': 'specialist',
        'NSWCATAD': 'tribunal',
        'VSCA': 'superior_appellate',
        'VSC': 'superior_trial',
        'QCA': 'superior_appellate',
        'QSC': 'superior_trial',
        'WASCA': 'superior_appellate',
        'WASC': 'superior_trial',
        'SASCFC': 'superior_appellate',
        'SASC': 'superior_trial',
        'AAT': 'tribunal',
        'FWC': 'tribunal',
    }
    return level_map.get(court_code, 'default')


def extract_citation_patterns(node_id: str) -> List[str]:
    """Extract citation patterns from a full case name for edge matching."""
    import re
    patterns = []

    # MNC pattern: [YYYY] COURT NUM (e.g., [2013] NSWSC 1668)
    mnc_matches = re.findall(r'\[\d{4}\]\s+[A-Z]+\s+\d+', node_id)
    patterns.extend(mnc_matches)

    # CLR pattern: (YYYY) NUM REPORT NUM (e.g., (1986) 6 NSWLR 497)
    clr_matches = re.findall(r'\(\d{4}\)\s+\d+\s+[A-Z]+\s+\d+', node_id)
    patterns.extend(clr_matches)

    return patterns


def detect_state(node_id: str, court: str) -> str:
    """Detect state/jurisdiction from citation."""
    id_upper = node_id.upper()
    court_upper = court.upper() if court else ''

    # Federal
    if any(x in id_upper for x in ['HCA', 'FCA', 'FCAFC', 'FAMCA', 'AAT', 'FWC']):
        return 'Federal'
    if 'COMMONWEALTH' in court_upper or 'FEDERAL' in court_upper:
        return 'Federal'

    # States
    if 'NSW' in id_upper or 'NEW_SOUTH_WALES' in court_upper:
        return 'NSW'
    if 'VSC' in id_upper or 'VSCA' in id_upper or 'VICTORIA' in court_upper:
        return 'VIC'
    if 'QSC' in id_upper or 'QCA' in id_upper or 'QUEENSLAND' in court_upper:
        return 'QLD'
    if 'WASC' in id_upper or 'WESTERN_AUSTRALIA' in court_upper:
        return 'WA'
    if 'SASC' in id_upper or 'SOUTH_AUSTRALIA' in court_upper:
        return 'SA'
    if 'TASSC' in id_upper or 'TASMANIA' in court_upper:
        return 'TAS'
    if 'NTSC' in id_upper or 'NORTHERN_TERRITORY' in court_upper:
        return 'NT'
    if 'ACTSC' in id_upper or 'AUSTRALIAN_CAPITAL' in court_upper:
        return 'ACT'

    return 'Other'


def generate_coordinates(
    node_id: str,
    court_code: str,
    court_level: str,
    domain: str,
    index: int,
    total: int
) -> Tuple[float, float, float]:
    """
    Generate 3D coordinates for visualization.

    Layout strategy:
    - X: Domain clustering (angle around Y-axis)
    - Y: Court hierarchy (apex at top, tribunals at bottom)
    - Z: Time-based or random spread
    """
    # Domain angle (X-Z plane)
    domain_list = list(DOMAIN_COLORS.keys())
    domain_idx = domain_list.index(domain) if domain in domain_list else 0
    domain_angle = (domain_idx / len(domain_list)) * math.pi * 2

    # Court level determines Y position
    y_base = COURT_LEVELS.get(court_level, COURT_LEVELS['default'])
    y = y_base + random.uniform(-10, 10)

    # Radius based on index and randomness
    radius = 30 + random.uniform(0, 30)

    # Add some noise to angle
    angle = domain_angle + random.uniform(-0.3, 0.3)

    x = radius * math.cos(angle)
    z = radius * math.sin(angle)

    return x, y, z


def load_domain_data(processed_dir: Path) -> Dict[str, List[Dict]]:
    """Load classified domain data from processed output."""
    domain_data = {}
    domains_dir = processed_dir / 'domains'

    if domains_dir.exists():
        for domain_file in domains_dir.glob('*.jsonl'):
            domain_name = domain_file.stem.title()
            domain_data[domain_name] = []

            with open(domain_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        doc = json.loads(line.strip())
                        domain_data[domain_name].append(doc)
                    except json.JSONDecodeError:
                        continue

    return domain_data


def load_graph_data(graph_dir: Path) -> Tuple[List[Dict], List[Dict]]:
    """Load graph nodes and edges from JSONL files."""
    nodes = []
    edges = []

    # Try demo files first, then full files
    nodes_file = graph_dir / 'spcnet_nodes_demo.jsonl'
    if not nodes_file.exists():
        nodes_file = graph_dir / 'spcnet_nodes.jsonl'

    edges_file = graph_dir / 'spcnet_edges_demo.jsonl'
    if not edges_file.exists():
        edges_file = graph_dir / 'spcnet_edges.jsonl'

    if nodes_file.exists():
        with open(nodes_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    nodes.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

    if edges_file.exists():
        with open(edges_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    edges.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

    return nodes, edges


def load_gsw_data(workspace_dir: Path) -> Dict[str, Any]:
    """Load GSW workspace data for actor information."""
    gsw_data = {}

    if workspace_dir.exists():
        for workspace_file in workspace_dir.glob('*_workspace.json'):
            domain = workspace_file.stem.replace('_workspace', '')
            try:
                with open(workspace_file, 'r', encoding='utf-8') as f:
                    gsw_data[domain] = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue

    return gsw_data


def load_extraction_stats(processed_dir: Path) -> Dict[str, Any]:
    """Load extraction statistics."""
    stats_file = processed_dir / 'extraction_statistics.json'
    if stats_file.exists():
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def generate_visualization_data(
    processed_dir: Path,
    workspace_dir: Path,
    graph_dir: Path,
    output_dir: Path,
    limit: int = 10000
) -> Dict[str, Any]:
    """
    Generate complete visualization data from pipeline output.

    Returns:
        Dict containing visualization-ready data
    """
    print("=" * 70)
    print("VISUALIZATION DATA GENERATOR")
    print("=" * 70)
    print(f"Processed dir: {processed_dir}")
    print(f"Workspace dir: {workspace_dir}")
    print(f"Graph dir: {graph_dir}")
    print(f"Output dir: {output_dir}")
    print(f"Node limit: {limit}")
    print("-" * 70)

    # Load source data
    print("\n[1/5] Loading graph data...")
    raw_nodes, raw_edges = load_graph_data(graph_dir)
    print(f"  Loaded {len(raw_nodes)} nodes, {len(raw_edges)} edges")

    print("\n[2/5] Loading domain classifications...")
    domain_data = load_domain_data(processed_dir)
    print(f"  Loaded {len(domain_data)} domains")
    for domain, docs in domain_data.items():
        print(f"    - {domain}: {len(docs)} documents")

    print("\n[3/5] Loading GSW workspaces...")
    gsw_data = load_gsw_data(workspace_dir)
    print(f"  Loaded {len(gsw_data)} workspaces")

    print("\n[4/5] Loading extraction statistics...")
    extraction_stats = load_extraction_stats(processed_dir)

    # Build node lookup from domain data
    domain_lookup = {}
    for domain, docs in domain_data.items():
        for doc in docs:
            doc_id = doc.get('citation') or doc.get('id')
            if doc_id:
                domain_lookup[doc_id] = domain

    # Process nodes
    print("\n[5/5] Generating visualization nodes...")
    viz_nodes = []
    node_ids = set()

    # Track statistics
    stats = {
        'by_state': defaultdict(int),
        'by_domain': defaultdict(int),
        'by_court_level': defaultdict(int),
        'by_court': defaultdict(int),
    }

    # Build citation lookup for edge matching (maps short citations to full IDs)
    citation_to_id = {}

    for i, raw_node in enumerate(raw_nodes[:limit]):
        node_id = raw_node.get('id') or raw_node.get('citation', f'node_{i}')

        if node_id in node_ids:
            continue
        node_ids.add(node_id)

        # Extract citation patterns and add to lookup
        citation_patterns = extract_citation_patterns(node_id)
        for pattern in citation_patterns:
            citation_to_id[pattern] = node_id

        # Detect attributes
        court_code = detect_court_code(node_id)
        court_level = detect_court_level(court_code)
        state = detect_state(node_id, raw_node.get('court', ''))

        # Get domain from lookup or raw data
        domain = domain_lookup.get(node_id) or raw_node.get('domain', 'Unclassified')
        if domain not in DOMAIN_COLORS:
            domain = 'Unclassified' if domain else 'Unclassified'

        # Generate coordinates
        x, y, z = generate_coordinates(
            node_id, court_code, court_level, domain, i, len(raw_nodes)
        )

        # Get color
        color = COURT_COLORS.get(court_code, COURT_COLORS['default'])

        # Build node
        viz_node = {
            'id': node_id,
            'x': round(x, 2),
            'y': round(y, 2),
            'z': round(z, 2),
            'color': color,
            'size': 0.5 + random.random() * 0.5,
            'label': raw_node.get('title', '') or node_id[:40],
            'type': 'statute' if raw_node.get('type') == 'legislation' else 'case',
            'uncertainty': random.random() * 0.3,
            'court': court_code,
            'courtLevel': court_level,
            'state': state,
            'domain': domain,
            'date': raw_node.get('date'),
        }

        viz_nodes.append(viz_node)

        # Update stats
        stats['by_state'][state] += 1
        stats['by_domain'][domain] += 1
        stats['by_court_level'][court_level] += 1
        stats['by_court'][court_code] += 1

    print(f"  Built citation lookup with {len(citation_to_id)} patterns")

    # Process edges
    print(f"\n  Generated {len(viz_nodes)} nodes")
    print("  Processing edges...")

    viz_edges = []
    edge_count = 0
    for raw_edge in raw_edges:
        source = raw_edge.get('source')
        target = raw_edge.get('target')

        # Resolve source and target using citation lookup
        resolved_source = citation_to_id.get(source) or source
        resolved_target = citation_to_id.get(target) or target

        # Include edge if both nodes exist (either directly or via lookup)
        source_exists = source in node_ids or resolved_source in node_ids
        target_exists = target in node_ids or resolved_target in node_ids

        if source_exists and target_exists:
            final_source = source if source in node_ids else resolved_source
            final_target = target if target in node_ids else resolved_target

            viz_edges.append({
                'source': final_source,
                'target': final_target,
                'weight': raw_edge.get('weight', 0.5),
                'type': raw_edge.get('type', 'cites'),
            })
            edge_count += 1

            # Limit edges for performance
            if edge_count >= limit * 3:
                break

    print(f"  Generated {len(viz_edges)} edges")

    # Build filter options
    filters = {
        'availableStates': sorted(stats['by_state'].keys()),
        'availableDomains': sorted(stats['by_domain'].keys()),
        'availableCourtLevels': sorted(stats['by_court_level'].keys()),
    }

    # Build final output
    visualization_data = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0.0',
        'nodes': viz_nodes,
        'edges': viz_edges,
        'stats': {
            'totalNodes': len(raw_nodes),
            'totalEdges': len(raw_edges),
            'loadedNodes': len(viz_nodes),
            'loadedEdges': len(viz_edges),
        },
        'filters': filters,
        'metadata': {
            'source': 'run_full_pipeline.py',
            'court_colors': COURT_COLORS,
            'domain_colors': DOMAIN_COLORS,
        }
    }

    # Write output files
    output_dir.mkdir(parents=True, exist_ok=True)

    # Main visualization data
    viz_file = output_dir / 'visualization_data.json'
    with open(viz_file, 'w', encoding='utf-8') as f:
        json.dump(visualization_data, f, indent=2)
    print(f"\n[Output] Visualization data: {viz_file}")

    # Statistics summary
    stats_output = {
        'generated_at': datetime.now().isoformat(),
        'total_nodes': len(viz_nodes),
        'total_edges': len(viz_edges),
        'by_state': dict(stats['by_state']),
        'by_domain': dict(stats['by_domain']),
        'by_court_level': dict(stats['by_court_level']),
        'by_court': dict(stats['by_court']),
        'extraction_stats': extraction_stats,
    }

    stats_file = output_dir / 'visualization_stats.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_output, f, indent=2)
    print(f"[Output] Statistics: {stats_file}")

    # Domain summary for filtering
    domain_summary = {
        domain: {
            'count': count,
            'color': DOMAIN_COLORS.get(domain, DOMAIN_COLORS['default']),
        }
        for domain, count in stats['by_domain'].items()
    }

    domain_file = output_dir / 'domain_summary.json'
    with open(domain_file, 'w', encoding='utf-8') as f:
        json.dump(domain_summary, f, indent=2)
    print(f"[Output] Domain summary: {domain_file}")

    # Also copy to frontend public directory
    frontend_data_dir = Path('ui/public/data')
    if frontend_data_dir.parent.exists():
        frontend_data_dir.mkdir(parents=True, exist_ok=True)

        # Write frontend-ready files
        with open(frontend_data_dir / 'graph.json', 'w', encoding='utf-8') as f:
            json.dump(visualization_data, f)
        print(f"[Output] Frontend data: {frontend_data_dir / 'graph.json'}")

    print("\n" + "=" * 70)
    print("VISUALIZATION DATA GENERATION COMPLETE")
    print("=" * 70)
    print(f"  Nodes: {len(viz_nodes)}")
    print(f"  Edges: {len(viz_edges)}")
    print(f"  States: {len(filters['availableStates'])}")
    print(f"  Domains: {len(filters['availableDomains'])}")
    print(f"  Court Levels: {len(filters['availableCourtLevels'])}")
    print("=" * 70)

    return visualization_data


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate visualization data from pipeline output"
    )
    parser.add_argument(
        '--processed-dir',
        type=Path,
        default=Path('data/processed'),
        help='Directory containing processed pipeline output'
    )
    parser.add_argument(
        '--workspace-dir',
        type=Path,
        default=Path('data/workspaces'),
        help='Directory containing GSW workspaces'
    )
    parser.add_argument(
        '--graph-dir',
        type=Path,
        default=Path('data/processed/graph'),
        help='Directory containing graph data'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('data/visualization'),
        help='Output directory for visualization data'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10000,
        help='Maximum number of nodes to include'
    )

    args = parser.parse_args()

    generate_visualization_data(
        processed_dir=args.processed_dir,
        workspace_dir=args.workspace_dir,
        graph_dir=args.graph_dir,
        output_dir=args.output,
        limit=args.limit
    )


if __name__ == '__main__':
    main()
