"""
VSA Contradiction Detector (Phase 2.7)
======================================

Identifies split authorities and legal contradictions.
Detects cases where similar facts lead to different outcomes.

Algorithm:
1. Encode Facts/Structure (S) separately from Outcome (O).
2. Compare pairs of cases.
3. Contradiction = High Fact Similarity + Low Outcome Similarity.
"""

from typing import List, Tuple
import torch

from src.logic.gsw_schema import GlobalWorkspace, LegalCase
from src.vsa.legal_vsa import LegalVSA, get_vsa_service
from src.vsa.encoder import GSWVSAEncoder

class ContradictionDetector:
    def __init__(self, vsa: LegalVSA = None):
        self.vsa = vsa if vsa else get_vsa_service()
        self.encoder = GSWVSAEncoder(self.vsa)

    def detect_contradictions(self, cases: List[LegalCase], threshold: float = 0.4) -> List[Tuple[str, str, float]]:
        """
        Scans a list of cases for contradictions.
        Returns list of (CaseID_A, CaseID_B, ContradictionScore).
        """
        vectors = []
        # Pre-compute vectors
        for case in cases:
            # Separate Facts vs Outcome
            # Note: GSW Schema needs explicit Outcome field for this to work perfectly.
            # For now, we'll assume Outcome is a specific State type or extracted text.
            # Simplification: Assume 'workspace' contains facts, and we have a separate 'outcome' string.
            
            fact_vec = self.encoder.encode_workspace(case.workspace)
            
            # Encode Outcome (using simple concept lookup for now)
            # In reality, this would be a complex vector of the orders made.
            outcome_vec = torch.zeros(self.vsa.dimension, device=self.vsa.device)
            # Hack: Use case title/type as proxy for outcome if not explicitly available,
            # or assume outcome is encoded in states with name "Outcome" or "Order".
            
            # Let's look for "Order" states
            order_states = [s for a in case.workspace.actors.values() for s in a.states if "Order" in s.name]
            if order_states:
                outcome_vec = self.vsa.bundle([
                    self.vsa.get_vector(s.value.upper()) for s in order_states
                ])
            
            vectors.append({
                "id": case.case_id,
                "facts": fact_vec,
                "outcome": outcome_vec
            })
            
        contradictions = []
        
        # Pairwise comparison (O(N^2))
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                case_a = vectors[i]
                case_b = vectors[j]
                
                # 1. Fact Similarity
                sim_facts = self.vsa.similarity(case_a["facts"], case_b["facts"])
                
                # 2. Outcome Similarity
                sim_outcome = self.vsa.similarity(case_a["outcome"], case_b["outcome"])
                
                # 3. Contradiction Score
                # We want High Fact Sim AND Low Outcome Sim
                # Score = Facts - Outcome
                score = sim_facts - sim_outcome
                
                if score > threshold:
                    contradictions.append((case_a["id"], case_b["id"], score))
                    
        return sorted(contradictions, key=lambda x: x[2], reverse=True)

