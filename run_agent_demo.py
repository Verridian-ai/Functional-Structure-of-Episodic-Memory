"""
Active Inference Demo (Phase 3.6)
=================================

Demonstrates the Legal Research Agent "foraging" for information.
Shows the balance between Epistemic Value (Exploration) and Pragmatic Value (Exploitation).
"""

import numpy as np
from src.agency.agent import LegalResearchAgent
from src.agency.pomdp import Observation, Action, HiddenState

def main():
    print("Initializing Legal Research Agent (Active Inference)...")
    agent = LegalResearchAgent()
    
    # Environment Simulation
    # In a real app, this would be the user/retriever/llm
    # Here we mock the environment response based on hidden state
    true_state = HiddenState.KNOWLEDGE_LOW
    
    print(f"Initial Belief: {agent.qs}")
    
    max_steps = 10
    obs = Observation.FINDING_IRRELEVANT # Start with nothing
    
    for t in range(max_steps):
        print(f"\n--- Step {t+1} ---")
        
        # 1. Agent Decides
        action = agent.step(obs)
        print(f"Agent Action: {action.name}")
        
        # 2. Environment Responds (Simulated Dynamics)
        prev_state = true_state
        
        if action == Action.SEARCH_BROAD:
            if true_state == HiddenState.KNOWLEDGE_LOW:
                # 80% chance to move to Medium
                if np.random.rand() < 0.8: true_state = HiddenState.KNOWLEDGE_MEDIUM
            elif true_state == HiddenState.KNOWLEDGE_MEDIUM:
                if np.random.rand() < 0.6: true_state = HiddenState.KNOWLEDGE_MEDIUM # Stay
                else: true_state = HiddenState.KNOWLEDGE_HIGH
                
        elif action == Action.SEARCH_SPECIFIC:
            if true_state == HiddenState.KNOWLEDGE_MEDIUM:
                 if np.random.rand() < 0.7: true_state = HiddenState.KNOWLEDGE_HIGH
                 
        elif action == Action.DRAFT_ANSWER:
            if true_state == HiddenState.KNOWLEDGE_HIGH:
                true_state = HiddenState.GOAL_MET
            else:
                # Failed attempt, state stays same
                pass
                
        print(f"True State: {prev_state.name} -> {true_state.name}")
        
        # 3. Generate Observation from True State
        # Simple deterministic obs for demo clarity
        if true_state == HiddenState.KNOWLEDGE_LOW:
            obs = Observation.FINDING_IRRELEVANT
        elif true_state == HiddenState.KNOWLEDGE_MEDIUM:
            obs = Observation.FINDING_RELEVANT
        elif true_state == HiddenState.KNOWLEDGE_HIGH:
            obs = Observation.FINDING_NOVEL
        elif true_state == HiddenState.GOAL_MET:
            obs = Observation.GOAL_SIGNAL_ON
            
        print(f"Observation: {obs.name}")
        print(f"Belief State: {np.round(agent.qs, 2)}")
        
        if obs == Observation.GOAL_SIGNAL_ON:
            print("\nSUCCESS! Goal met.")
            break

if __name__ == "__main__":
    main()

