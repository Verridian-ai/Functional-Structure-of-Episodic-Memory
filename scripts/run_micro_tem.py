"""
Micro-TEM Demo
==============

Demonstrates the Heuristic TEM Factorizer (Phase 1B).
Creates a dummy extracted case and classifies it using the factorizer.
"""

from src.logic.gsw_schema import ChunkExtraction, Actor, State, ActorType
from src.tem.factorizer import HeuristicTEMFactorizer
from src.tem.structures import CaseArchetype

def main():
    print("Initializing Micro-TEM Factorizer...")
    factorizer = HeuristicTEMFactorizer()
    
    # Scenario 1: Long Marriage Property Case
    print("\n--- Scenario 1: Long Marriage ---")
    extraction1 = ChunkExtraction(
        chunk_id="1", 
        situation="Property settlement after 20 years"
    )
    
    # Add Actors
    husband = Actor(name="Mr Smith", actor_type=ActorType.PERSON)
    husband.states.append(State(
        entity_id=husband.id,
        name="RelationshipStatus",
        value="Married",
        start_date="2000-01-01",
        end_date="2020-01-01"
    ))
    
    home = Actor(name="Matrimonial Home", actor_type=ActorType.ASSET)
    
    extraction1.actors.extend([husband, home])
    
    structure1 = factorizer.factorize(extraction1)
    print(f"Archetype: {structure1.archetype.name}")
    print(f"Reasoning: {structure1.reasoning}")
    print(f"Features: {structure1.features}")
    
    # Scenario 2: Family Violence Parenting
    print("\n--- Scenario 2: Family Violence ---")
    extraction2 = ChunkExtraction(chunk_id="2")
    
    child = Actor(name="Child A", actor_type=ActorType.PERSON, roles=["Child"])
    father = Actor(name="Father", actor_type=ActorType.PERSON)
    
    # Add Violence State
    violence_state = State(
        entity_id=father.id,
        name="Allegation",
        value="Family Violence committed by Father"
    )
    father.states.append(violence_state)
    
    extraction2.actors.extend([child, father])
    
    structure2 = factorizer.factorize(extraction2)
    print(f"Archetype: {structure2.archetype.name}")
    print(f"Reasoning: {structure2.reasoning}")

if __name__ == "__main__":
    main()

