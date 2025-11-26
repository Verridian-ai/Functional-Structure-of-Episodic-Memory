"""
Cognitive System Integration (Phase 5.1)
========================================

Implements the end-to-end integration of the cognitive architecture.
Unifies:
- Agency (Active Inference) -> Decides WHAT to do.
- Navigation (TEM) -> Decides WHERE to go.
- Logic (VSA) -> Validates WHAT was found.
"""

import time
import numpy as np
from typing import Dict, Any
from pathlib import Path

# Agency
from src.agency.agent import LegalResearchAgent
from src.agency.pomdp import Observation, Action, HiddenState

# Navigation
from src.tem.legal_graph_builder import LegalGraphBuilder
from src.tem.action_space import LegalAction

# Retrieval
from src.retrieval.retriever import LegalRetriever

# Logic
from src.vsa.legal_vsa import get_vsa_service
from src.vsa.encoder import GSWVSAEncoder
from src.logic.gsw_schema import GlobalWorkspace, Actor, ActorType, State

class LegalCognitiveSystem:
    def __init__(self, graph_dir='data/processed/graph'):
        print("[System] Initializing Cognitive Architecture...")
        
        # 1. Agency Layer
        self.agent = LegalResearchAgent()
        print("[System] Agency Layer (Active Inference) Online.")
        
        # 2. Navigation Layer
        try:
            self.graph = LegalGraphBuilder(Path(graph_dir))
            print(f"[System] Navigation Layer (TEM) Online. Graph Nodes: {len(self.graph.nodes)}")
        except Exception as e:
            print(f"[System] Warning: TEM Graph not found ({e}). Using mock navigation.")
            self.graph = None
            
        # 3. Retrieval Layer
        self.retriever = LegalRetriever()
        print("[System] Retrieval Layer Online.")
            
        # 4. Logic Layer
        self.vsa = get_vsa_service()
        self.encoder = GSWVSAEncoder(self.vsa)
        print("[System] Logic Layer (VSA) Online.")
        
        self.current_node = None
        self.gathered_facts = GlobalWorkspace()
        self.current_query = ""

    def process_query(self, query: str, max_steps: int = 10) -> Dict[str, Any]:
        print(f"\n[System] Processing Query: '{query}'")
        self.current_query = query
        
        history = []
        observation = Observation.FINDING_IRRELEVANT # Initial state
        
        for t in range(max_steps):
            print(f"\n--- Cycle {t+1} ---")
            
            # --- A. Agency: Decide Action ---
            action = self.agent.step(observation)
            print(f"[Agency] Selected Action: {action.name}")
            
            history.append({"step": t, "action": action.name})
            
            # --- B. Execution: Navigate & Retrieve ---
            if action == Action.STOP:
                print("[System] Agent decided to stop.")
                break
                
            elif action == Action.DRAFT_ANSWER:
                # Validate
                print("[System] Validating gathered facts with VSA...")
                
                # Extract concepts from gathered facts
                concepts = []
                
                # 1. From Query
                if "divorce" in query.lower(): concepts.append("DIVORCE")
                if "separate" in query.lower() or "separation" in query.lower(): concepts.append("SEPARATION")
                if "child" in query.lower(): concepts.append("CHILD")
                if "property" in query.lower(): concepts.append("PROPERTY_SETTLEMENT")
                if "violence" in query.lower(): concepts.append("FAMILY_VIOLENCE")
                
                # 2. From Retrieved Text (Simple Keyword Extraction)
                all_text = " ".join(self.gathered_facts.entity_summaries.values()).lower()
                
                if "marriage" in all_text or "married" in all_text: concepts.append("MARRIAGE")
                if "asset" in all_text or "pool" in all_text or "home" in all_text: concepts.append("ASSET")
                if "separation" in all_text or "separated" in all_text: concepts.append("SEPARATION")
                if "child" in all_text or "parenting" in all_text: concepts.append("CHILD")
                if "violence" in all_text or "abuse" in all_text: concepts.append("FAMILY_VIOLENCE")
                if "risk" in all_text: concepts.append("SAFETY_RISK")
                
                concepts = list(set(concepts)) # Deduplicate
                print(f"[System] Extracted Concepts: {concepts}")
                
                validation = self.vsa.verify_no_hallucination(concepts)
                
                if validation["valid"]:
                    print("[Logic] Validation PASSED. Drafting response.")
                    return {
                        "status": "success",
                        "answer": f"Based on {len(self.gathered_facts.entity_summaries)} documents found...",
                        "history": history,
                        "facts": len(self.gathered_facts.actors)
                    }
                else:
                    print(f"[Logic] Validation FAILED: {validation['issues']}")
                    observation = Observation.FINDING_IRRELEVANT
                    continue

            elif action in [Action.SEARCH_BROAD, Action.SEARCH_SPECIFIC]:
                # Use Real Retriever
                results = self.retriever.search(self.current_query, top_k=3)
                
                if results:
                    print(f"[Retrieval] Found {len(results)} documents.")
                    for doc in results:
                        print(f" - {doc.get('title', 'Untitled')} (Score: {doc.get('score', 0):.2f})")
                        # Add to gathered facts (simulate reading)
                        self.gathered_facts.entity_summaries[doc['id']] = doc.get('text_preview', '')
                    
                    observation = Observation.FINDING_RELEVANT
                else:
                    print("[Retrieval] No results found.")
                    observation = Observation.FINDING_IRRELEVANT
            
            elif action == Action.READ_DOCUMENT:
                # If we have results, read details
                if len(self.gathered_facts.entity_summaries) > 0:
                    print(f"[System] Reading {len(self.gathered_facts.entity_summaries)} cached documents...")
                    observation = Observation.FINDING_NOVEL
                else:
                    print("[System] Nothing to read.")
                    observation = Observation.FINDING_IRRELEVANT
                
        return {
            "status": "timeout",
            "history": history
        }
