"""
VSA Demo: Neuro-Symbolic Reasoning
==================================

Demonstrates the complete Phase 2 stack:
1.  Ontology Initialization
2.  GSW -> Hypervector Encoding
3.  Symbolic Logic Checks (Anti-Hallucination)
"""

from src.logic.gsw_schema import GlobalWorkspace, Actor, ActorType, State, VerbPhrase
from src.vsa.legal_vsa import get_vsa_service
from src.vsa.encoder import GSWVSAEncoder

def main():
    print("1. Initializing VSA Service...")
    vsa = get_vsa_service()
    
    print("2. Creating Mock Legal Case (GSW)...")
    workspace = GlobalWorkspace(domain="family")
    
    # Actors
    husband = Actor(name="Mr Smith", actor_type=ActorType.PERSON, roles=["APPLICANT", "FINANCIAL_CONTRIBUTOR"])
    wife = Actor(name="Ms Jones", actor_type=ActorType.PERSON, roles=["RESPONDENT", "HOMEMAKER"])
    child = Actor(name="Child A", actor_type=ActorType.PERSON, roles=["CHILD"])
    
    workspace.add_actor(husband)
    workspace.add_actor(wife)
    workspace.add_actor(child)
    
    # States - Logic Violation Example (Divorce without Marriage)
    # To trigger the check, we need to extract concepts from the workspace first.
    # For this demo, we'll pass concept strings directly to verify_no_hallucination.
    
    # Let's try a valid case first
    print("\n3. Validating Logic Rules...")
    
    # Case A: Valid
    concepts_a = ["DIVORCE", "MARRIAGE", "SEPARATION"]
    result_a = vsa.verify_no_hallucination(concepts_a)
    print(f"Case A Concepts: {concepts_a}")
    print(f"Valid: {result_a['valid']}")
    
    # Case B: Invalid (Divorce without Marriage)
    concepts_b = ["DIVORCE"]
    result_b = vsa.verify_no_hallucination(concepts_b)
    print(f"\nCase B Concepts: {concepts_b}")
    print(f"Valid: {result_b['valid']}")
    print(f"Issues: {result_b['issues']}")
    
    print("\n4. Encoding GSW to Hypervector...")
    encoder = GSWVSAEncoder(vsa)
    scene_vec = encoder.encode_workspace(workspace)
    print(f"Scene Vector Shape: {scene_vec.shape}")
    print(f"Scene Vector Stats: Mean={scene_vec.float().mean():.4f}, Std={scene_vec.float().std():.4f}")
    
    print("\n5. Similarity Check (Retrieval)...")
    # Does the scene contain "Mr Smith"?
    v_smith = vsa.get_vector("Mr Smith")
    # Note: Scene is bundled, so similarity won't be 1.0, but should be > 0
    # However, Mr Smith is bound with Type/Roles, so raw "Mr Smith" vector might not appear directly 
    # if we don't encode the query similarly.
    # Let's check basic concept presence
    v_child = vsa.get_vector("CHILD")
    sim = vsa.similarity(scene_vec, v_child)
    print(f"Similarity to 'CHILD': {sim:.4f} (Expected: > 0 due to holistic inclusion)")

if __name__ == "__main__":
    main()

