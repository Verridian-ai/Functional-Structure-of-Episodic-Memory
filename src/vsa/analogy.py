"""
NVSA Analogy Detection (Phase 2.6)
==================================

Implements Neuro-Vector Symbolic Analogy (NVSA) detection.
Uses "Raven's Matrices" logic to identify structural analogies between cases.

Logic:
Given a relationship A : B :: C : ?, we want to find D.
1. Calculate Transformation Vector T that maps A to B.
   T = Bind(A, B)  (since vectors are self-inverse bipolar, A*B maps A->B)
2. Apply T to C to get prediction D_pred.
   D_pred = Bind(T, C) = A * B * C
3. Search memory for the closest match to D_pred.
"""

import torch
from typing import List, Tuple, Optional

from src.vsa.legal_vsa import LegalVSA, get_vsa_service
from src.vsa.encoder import GSWVSAEncoder
from src.logic.gsw_schema import GlobalWorkspace

class AnalogyEngine:
    def __init__(self, vsa: LegalVSA = None):
        self.vsa = vsa if vsa else get_vsa_service()
        self.encoder = GSWVSAEncoder(self.vsa)

    def calculate_transformation(self, case_a: GlobalWorkspace, case_b: GlobalWorkspace) -> torch.Tensor:
        """
        Calculates the structural transformation between Case A and Case B.
        T = A * B
        """
        vec_a = self.encoder.encode_workspace(case_a)
        vec_b = self.encoder.encode_workspace(case_b)
        return self.vsa.bind(vec_a, vec_b)

    def solve_analogy(self, 
                      case_a: GlobalWorkspace, 
                      case_b: GlobalWorkspace, 
                      case_c: GlobalWorkspace,
                      candidates: List[GlobalWorkspace]) -> Tuple[Optional[GlobalWorkspace], float]:
        """
        Solves A : B :: C : ?
        Returns the best matching candidate case and similarity score.
        """
        # 1. Calculate Transformation T: A -> B
        T = self.calculate_transformation(case_a, case_b)
        
        # 2. Apply T to C: D_pred = T * C
        vec_c = self.encoder.encode_workspace(case_c)
        d_pred = self.vsa.bind(T, vec_c)
        
        # 3. Find closest candidate
        best_score = -1.0
        best_candidate = None
        
        for candidate in candidates:
            vec_cand = self.encoder.encode_workspace(candidate)
            score = self.vsa.similarity(d_pred, vec_cand)
            
            if score > best_score:
                best_score = score
                best_candidate = candidate
                
        return best_candidate, best_score

    def find_structural_analogies(self, 
                                query_case: GlobalWorkspace, 
                                knowledge_base: List[GlobalWorkspace]) -> List[Tuple[GlobalWorkspace, float]]:
        """
        Finds cases in the KB that are structurally analogous to the query.
        Uses pure similarity for now (Phase 1 style), but using VSA encoded vectors
        which capture structure (Roles/Relations) better than dense embeddings.
        """
        query_vec = self.encoder.encode_workspace(query_case)
        results = []
        
        for case in knowledge_base:
            case_vec = self.encoder.encode_workspace(case)
            sim = self.vsa.similarity(query_vec, case_vec)
            results.append((case, sim))
            
        return sorted(results, key=lambda x: x[1], reverse=True)

