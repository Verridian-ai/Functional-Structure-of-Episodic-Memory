"""
System Integration Demo (Phase 5.1)
===================================

Runs the full cognitive architecture end-to-end.
"""

from src.integration.cognitive_system import LegalCognitiveSystem
from pathlib import Path

def main():
    # Ensure graph directory exists (even if empty)
    Path('data/processed/graph').mkdir(parents=True, exist_ok=True)
    
    # Initialize System
    system = LegalCognitiveSystem()
    
    # Run Query
    query = "What are the requirements for a divorce application in Australia?"
    result = system.process_query(query)
    
    print("\n=== Final Result ===")
    print(f"Status: {result['status']}")
    if 'answer' in result:
        print(f"Answer: {result['answer']}")
    print("Execution History:")
    for step in result['history']:
        print(f" - Step {step['step']}: {step['action']}")

if __name__ == "__main__":
    main()

