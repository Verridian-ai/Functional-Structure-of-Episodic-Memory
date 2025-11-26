"""
Legal VSA (Vector Symbolic Architecture)
========================================

Backend implementation of the Legal VSA service (Phase 2.2).
Provides symbolic reasoning, binding/unbinding of concepts, and anti-hallucination checks.

This module uses Hyperdimensional Computing (HDC) with bipolar vectors {-1, 1}.
Implemented using PyTorch for GPU acceleration.
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

from src.vsa.ontology import get_all_tokens, LOGIC_RULES

# Hypervector Dimension (D)
DIMENSION = 10000 

class LegalVSA:
    """
    Vector Symbolic Architecture engine for Legal Reasoning.
    """
    def __init__(self, dimension: int = DIMENSION, device: str = "cpu"):
        self.dimension = dimension
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        
        # Item Memory: Concept String -> Hypervector (D,)
        self.memory: Dict[str, torch.Tensor] = {} 
        self.inverse_memory: Dict[str, str] = {} # Hash -> Name (simplified)
        
        # Initialize Ontology (Phase 2.3)
        self._initialize_ontology()

    def _initialize_ontology(self):
        """Generates orthogonal vectors for all ontology terms."""
        tokens = get_all_tokens()
        print(f"Initializing VSA Memory with {len(tokens)} ontology terms...")
        for token in tokens:
            self.add_concept(token)
            
    def _generate_random_vector(self) -> torch.Tensor:
        """Generates a random bipolar hypervector {-1, 1}."""
        # Bernoulli(0.5) -> {0, 1} -> *2 -1 -> {-1, 1}
        v = torch.randint(0, 2, (self.dimension,), device=self.device, dtype=torch.float32)
        v = v * 2 - 1
        return v

    def add_concept(self, name: str) -> torch.Tensor:
        """Adds a new concept to memory."""
        if name not in self.memory:
            vec = self._generate_random_vector()
            self.memory[name] = vec
        return self.memory[name]

    def get_vector(self, name: str) -> torch.Tensor:
        """Retrieves a vector. Raises error if unknown (strict ontology)."""
        if name not in self.memory:
            # For now, auto-generate unknown terms (Open World Assumption)
            return self.add_concept(name)
        return self.memory[name]

    def bind(self, v1: torch.Tensor, v2: torch.Tensor) -> torch.Tensor:
        """
        Binding operation (MAP).
        Element-wise multiplication. For bipolar vectors, this is equivalent to XOR.
        Commutative: A * B = B * A
        Distributive over bundle: A * (B + C) = A*B + A*C
        Preserves distance: sim(A*B, A*C) = sim(B, C)
        Dissimilar to inputs: sim(A*B, A) ~ 0
        """
        return v1 * v2

    def bundle(self, vectors: List[torch.Tensor]) -> torch.Tensor:
        """
        Bundling operation (SUPERPOSITION).
        Element-wise addition followed by sign function (Majority Rule).
        Result is similar to all inputs.
        """
        if not vectors:
            return torch.zeros(self.dimension, device=self.device)
        
        # Sum
        sum_vec = torch.stack(vectors).sum(dim=0)
        
        # Binarize (Majority Rule)
        # Zeros are random tie-break
        zeros = sum_vec == 0
        if zeros.any():
            sum_vec[zeros] = torch.randint(0, 2, (zeros.sum(),), device=self.device, dtype=torch.float32) * 2 - 1
            
        return torch.sign(sum_vec)

    def permute(self, v: torch.Tensor, shifts: int = 1) -> torch.Tensor:
        """
        Permutation operation (ROTATE).
        Cyclic shift. Used for encoding sequences or order.
        sim(Roll(A), A) ~ 0
        """
        return torch.roll(v, shifts=shifts, dims=0)

    def similarity(self, v1: torch.Tensor, v2: torch.Tensor) -> float:
        """Cosine similarity."""
        # For bipolar vectors, cosine sim is dot product / D
        return torch.dot(v1, v2).item() / self.dimension

    def cleanup(self, noisy_vector: torch.Tensor, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Finds the closest concepts in memory to the noisy vector.
        Returns list of (Concept, Similarity).
        """
        results = []
        # Linear scan (ok for <10k items). For larger, use FAISS/quantization.
        for name, vec in self.memory.items():
            sim = self.similarity(noisy_vector, vec)
            if sim > threshold:
                results.append((name, sim))
        
        return sorted(results, key=lambda x: x[1], reverse=True)

    def encode_graph(self, triplets: List[Tuple[str, str, str]]) -> torch.Tensor:
        """
        Encodes a knowledge graph (Subject, Relation, Object) into a single hypervector.
        Graph = Sum( Subj * Rel * Obj )
        """
        edges = []
        for s, r, o in triplets:
            v_s = self.get_vector(s)
            v_r = self.get_vector(r)
            v_o = self.get_vector(o)
            
            # Binding: Subject * Relation * Object
            # Note: This is commutative. A*B*C = C*B*A.
            # To preserve direction, we could use permutation: A * Roll(B) * Roll(Roll(C))
            # Or specific role binding: (SUBJ*s) + (REL*r) + (OBJ*o)
            
            # Simple approach for now: Holistic Triplet
            edges.append(self.bind(self.bind(v_s, v_r), v_o))
            
        return self.bundle(edges)

    def verify_no_hallucination(self, statement_concepts: List[str]) -> Dict:
        """
        Checks consistency using symbolic logic.
        """
        # Encode Knowledge Base (Rules)
        kb_vector = self.encode_graph(LOGIC_RULES)
        
        issues = []
        
        # Check specific rules
        # Logic: If A requires B, and we have A, do we have B?
        
        present = set(statement_concepts)
        
        for subj, rel, obj in LOGIC_RULES:
            if rel == "REQUIRES":
                if subj in present and obj not in present:
                    issues.append(f"Logic Violation: '{subj}' REQUIRES '{obj}', but '{obj}' is missing.")
            
            if rel == "CONTRADICTS":
                if subj in present and obj in present:
                    issues.append(f"Contradiction: '{subj}' and '{obj}' cannot coexist.")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "confidence": 1.0 if len(issues) == 0 else 0.5
        }

# Singleton instance
_vsa_instance = None

def get_vsa_service() -> LegalVSA:
    global _vsa_instance
    if _vsa_instance is None:
        _vsa_instance = LegalVSA()
    return _vsa_instance
