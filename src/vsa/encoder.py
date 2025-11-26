"""
GSW-to-VSA Encoder (Phase 2.4)
==============================

Translates Global Semantic Workspace (GSW) objects into Hypervectors.
Allows the neuro-symbolic engine to reason about the extracted knowledge.

Encoding Strategy:
- Entity = Bind(ID, TYPE, NAME) + Bundle(ROLES) + Bundle(STATES)
- Workspace = Bundle(Entities) + Bundle(Relationships)
"""

import torch
from typing import Union, List

from src.logic.gsw_schema import GlobalWorkspace, ChunkExtraction, Actor, State, VerbPhrase
from src.vsa.legal_vsa import LegalVSA, get_vsa_service

class GSWVSAEncoder:
    def __init__(self, vsa: LegalVSA = None):
        self.vsa = vsa if vsa else get_vsa_service()

    def encode_actor(self, actor: Actor) -> torch.Tensor:
        """
        Encodes an Actor into a hypervector.
        Vector = Bind(Type, Name) + Bundle(Roles) + Bundle(States)
        """
        # 1. Core Identity: Type * Name
        # (Using string representations for now)
        v_type = self.vsa.get_vector(actor.actor_type.value.upper())
        v_name = self.vsa.get_vector(actor.name) # Names are auto-generated concepts
        identity = self.vsa.bind(v_type, v_name)
        
        # 2. Roles
        role_vectors = [self.vsa.get_vector(r.upper()) for r in actor.roles]
        roles_bundled = self.vsa.bundle(role_vectors)
        
        # 3. States
        # State = Name * Value
        state_vectors = []
        for state in actor.states:
            v_s_name = self.vsa.get_vector(state.name.upper())
            v_s_val = self.vsa.get_vector(state.value.upper())
            state_vectors.append(self.vsa.bind(v_s_name, v_s_val))
        states_bundled = self.vsa.bundle(state_vectors)
        
        # Combine all features
        return self.vsa.bundle([identity, roles_bundled, states_bundled])

    def encode_verb(self, verb: VerbPhrase, actor_map: dict) -> torch.Tensor:
        """
        Encodes a relationship (Verb Phrase).
        Vector = Agent * Action * Patient
        """
        # Find agent vector
        agent_vec = torch.zeros(self.vsa.dimension, device=self.vsa.device)
        if verb.agent_id and verb.agent_id in actor_map:
            agent_vec = actor_map[verb.agent_id]
            
        # Find patient vectors
        patient_vecs = []
        for pid in verb.patient_ids:
            if pid in actor_map:
                patient_vecs.append(actor_map[pid])
        patient_bundled = self.vsa.bundle(patient_vecs)
        
        # Action vector
        action_vec = self.vsa.get_vector(verb.verb.upper())
        
        # Bind Triplet
        return self.vsa.bind(self.vsa.bind(agent_vec, action_vec), patient_bundled)

    def encode_workspace(self, workspace: GlobalWorkspace) -> torch.Tensor:
        """
        Encodes an entire workspace into a single Scene Vector.
        """
        # 1. Encode all Actors
        actor_vectors = {} # ID -> Vector
        actor_list = []
        
        for actor_id, actor in workspace.actors.items():
            vec = self.encode_actor(actor)
            actor_vectors[actor_id] = vec
            actor_list.append(vec)
            
        # 2. Encode all Relationships (Verbs)
        verb_list = []
        for verb in workspace.verb_phrases.values():
            vec = self.encode_verb(verb, actor_vectors)
            verb_list.append(vec)
            
        # 3. Bundle Everything
        scene_vector = self.vsa.bundle(actor_list + verb_list)
        return scene_vector

    def encode_chunk(self, chunk: ChunkExtraction) -> torch.Tensor:
        """
        Encodes a single extraction chunk.
        """
        # Similar to workspace but for list structure
        actor_vectors = {}
        actor_list = []
        
        for actor in chunk.actors:
            vec = self.encode_actor(actor)
            actor_vectors[actor.id] = vec
            actor_list.append(vec)
            
        verb_list = []
        for verb in chunk.verb_phrases:
            # Need to handle IDs carefully if they refer to actors outside chunk?
            # For now assume self-contained or ignore missing
            vec = self.encode_verb(verb, actor_vectors)
            verb_list.append(vec)
            
        return self.vsa.bundle(actor_list + verb_list)

