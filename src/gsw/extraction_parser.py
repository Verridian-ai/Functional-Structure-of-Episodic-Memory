"""
Extraction Parser
=================

Parsing helpers for converting LLM response data into schema objects.
"""

from typing import Dict, Any
from uuid import uuid4

from src.logic.gsw_schema import (
    Actor, ActorType, State, VerbPhrase, PredictiveQuestion,
    SpatioTemporalLink, QuestionType, LinkType
)


class ExtractionParser:
    """
    Parses raw LLM response data into GSW schema objects.
    """

    @staticmethod
    def parse_actor(data: Dict[str, Any], chunk_id: str) -> Actor:
        """Parse actor from response data."""
        # Parse states
        states = []
        for state_data in data.get("states", []):
            state = State(
                id=f"state_{uuid4().hex[:8]}",
                entity_id=data.get("id", ""),
                name=state_data.get("name", "Unknown"),
                value=state_data.get("value", ""),
                start_date=state_data.get("start_date"),
                end_date=state_data.get("end_date"),
                source_chunk_id=chunk_id
            )
            states.append(state)

        # Parse actor type
        actor_type_str = data.get("actor_type", "person").lower()
        try:
            actor_type = ActorType(actor_type_str)
        except ValueError:
            actor_type = ActorType.PERSON

        return Actor(
            id=data.get("id", f"actor_{uuid4().hex[:8]}"),
            name=data.get("name", "Unknown"),
            actor_type=actor_type,
            aliases=data.get("aliases", []),
            roles=data.get("roles", []),
            states=states,
            source_chunk_ids=[chunk_id]
        )

    @staticmethod
    def parse_verb_phrase(data: Dict[str, Any], chunk_id: str) -> VerbPhrase:
        """Parse verb phrase from response data."""
        # Ensure agent_id is string or None (LLM sometimes returns [])
        agent_id = data.get("agent_id")
        if not isinstance(agent_id, str):
            agent_id = None

        # Ensure patient_ids is a list of strings
        patient_ids = data.get("patient_ids", [])
        if not isinstance(patient_ids, list):
            patient_ids = []
        patient_ids = [p for p in patient_ids if isinstance(p, str)]

        return VerbPhrase(
            id=data.get("id", f"verb_{uuid4().hex[:8]}"),
            verb=data.get("verb", ""),
            agent_id=agent_id,
            patient_ids=patient_ids,
            temporal_id=data.get("temporal_id") if isinstance(data.get("temporal_id"), str) else None,
            spatial_id=data.get("spatial_id") if isinstance(data.get("spatial_id"), str) else None,
            is_implicit=data.get("is_implicit", False),
            source_chunk_id=chunk_id
        )

    @staticmethod
    def parse_question(data: Dict[str, Any], chunk_id: str) -> PredictiveQuestion:
        """Parse predictive question from response data."""
        # Parse question type
        q_type_str = data.get("question_type", "what").lower()
        try:
            q_type = QuestionType(q_type_str)
        except ValueError:
            q_type = QuestionType.WHAT

        return PredictiveQuestion(
            id=data.get("id", f"q_{uuid4().hex[:8]}"),
            question_text=data.get("question_text", ""),
            question_type=q_type,
            target_entity_id=data.get("target_entity_id"),
            answerable=data.get("answerable", False),
            answer_text=data.get("answer_text"),
            answer_entity_id=data.get("answer_entity_id"),
            source_chunk_id=chunk_id
        )

    @staticmethod
    def parse_link(data: Dict[str, Any], chunk_id: str) -> SpatioTemporalLink:
        """Parse spatio-temporal link from response data."""
        tag_type_str = data.get("tag_type", "temporal").lower()
        try:
            tag_type = LinkType(tag_type_str)
        except ValueError:
            tag_type = LinkType.TEMPORAL

        return SpatioTemporalLink(
            id=data.get("id", f"link_{uuid4().hex[:8]}"),
            linked_entity_ids=data.get("linked_entity_ids", []),
            tag_type=tag_type,
            tag_value=data.get("tag_value"),
            source_chunk_id=chunk_id
        )
