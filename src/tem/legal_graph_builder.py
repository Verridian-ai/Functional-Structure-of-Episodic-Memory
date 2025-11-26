"""
Legal Graph Builder (TEM Data Loader)
=====================================

Constructs the graph environment for the Tolman-Eichenbaum Machine (TEM).
Loads the Hier-SPCNet and generates training episodes (random walks).

Key Responsibilities:
1.  Load graph structure from JSONL (Nodes/Edges).
2.  Generate sequences of (Observation, Action) pairs.
    - Observation (x_t): Document embedding (or ID for lookup).
    - Action (a_t): Edge type traversed to reach the next node.
3.  Provide efficient batched streaming for PyTorch training.
"""

import json
import random
import numpy as np
import torch
from pathlib import Path
from typing import Dict, List, Tuple, Iterator, Optional
from collections import defaultdict

from src.tem.action_space import LegalAction, ACTION_TO_ID

class LegalGraphBuilder:
    def __init__(self, graph_dir: Path):
        self.graph_dir = graph_dir
        self.adj_list: Dict[str, List[Tuple[str, LegalAction]]] = defaultdict(list)
        self.nodes: Dict[str, Dict] = {} # ID -> Metadata
        self.node_ids: List[str] = []
        
        self._load_graph()

    def _load_graph(self):
        """Loads nodes and edges from JSONL files."""
        nodes_path = self.graph_dir / "spcnet_nodes.jsonl"
        edges_path = self.graph_dir / "spcnet_edges.jsonl"

        print(f"Loading graph from {self.graph_dir}...")

        # Load Nodes
        if nodes_path.exists():
            with open(nodes_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    node_id = data['id']
                    self.nodes[node_id] = data
                    self.node_ids.append(node_id)
        
        # Load Edges
        if edges_path.exists():
            with open(edges_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    source = data['source']
                    target = data['target']
                    rel_type = data.get('type', 'CITE')
                    
                    # Map string relation to LegalAction enum
                    # Default to CITE if unknown
                    try:
                        action = LegalAction[rel_type.upper()]
                    except KeyError:
                        action = LegalAction.CITE
                        
                    self.adj_list[source].append((target, action))
        
        print(f"Graph loaded: {len(self.nodes)} nodes, {sum(len(v) for v in self.adj_list.values())} edges.")

    def random_walk(self, start_node: str, length: int) -> Tuple[List[str], List[int]]:
        """
        Performs a random walk starting from a node.
        Returns:
            - path: List of Node IDs visited (x_0, x_1, ... x_T)
            - actions: List of Action IDs taken (a_1, ... a_T)
        """
        path = [start_node]
        actions = []
        
        current = start_node
        for _ in range(length - 1):
            neighbors = self.adj_list.get(current, [])
            if not neighbors:
                break # Dead end
            
            # Sample next node
            next_node, action = random.choice(neighbors)
            
            path.append(next_node)
            actions.append(ACTION_TO_ID[action])
            current = next_node
            
        return path, actions

    def batch_generator(self, batch_size: int, walk_length: int) -> Iterator[Dict[str, torch.Tensor]]:
        """
        Yields batches of training data for TEM.
        Each batch contains:
        - 'observations': (batch, seq_len) - Node IDs (indices in node_ids list)
        - 'actions': (batch, seq_len-1) - Action IDs
        """
        # Create efficient ID map for tensor conversion
        id_to_idx = {nid: i for i, nid in enumerate(self.node_ids)}
        
        while True:
            batch_obs = []
            batch_acts = []
            
            for _ in range(batch_size):
                # Pick random start node (prefer nodes with outgoing edges)
                # Simple heuristic: try 10 times to find a node with neighbors
                start_node = random.choice(self.node_ids)
                for _ in range(10):
                    if start_node in self.adj_list:
                        break
                    start_node = random.choice(self.node_ids)
                
                path_ids, actions = self.random_walk(start_node, walk_length)
                
                # Padding if walk ended early (dead end)
                actual_len = len(path_ids)
                pad_len = walk_length - actual_len
                
                # Convert to indices
                path_indices = [id_to_idx.get(nid, 0) for nid in path_ids]
                
                # Pad observations (repeat last node or use 0)
                path_indices += [0] * pad_len
                
                # Pad actions (use 0 - e.g. CITE or a special PAD token)
                # We need to handle actions length (always 1 less than path)
                # If path was full length (T), actions is T-1.
                # If path was 1 (start only), actions is 0.
                
                # Ensure actions match expected sequence length (T-1)
                target_act_len = walk_length - 1
                if len(actions) < target_act_len:
                    actions += [0] * (target_act_len - len(actions))
                
                batch_obs.append(path_indices)
                batch_acts.append(actions)
            
            yield {
                'observations': torch.tensor(batch_obs, dtype=torch.long),
                'actions': torch.tensor(batch_acts, dtype=torch.long)
            }

    def get_embedding_matrix(self, embedding_dim: int = 768) -> torch.Tensor:
        """
        Placeholder: Returns a tensor of embeddings for all nodes.
        In production, this loads pre-computed embeddings from P0.3.
        """
        num_nodes = len(self.node_ids)
        print(f"Generating random embeddings for {num_nodes} nodes (dim={embedding_dim})...")
        # Random normal for Pilot
        return torch.randn(num_nodes, embedding_dim)

