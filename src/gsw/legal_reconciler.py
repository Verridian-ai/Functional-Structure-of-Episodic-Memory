"""
Legal Reconciler - Entity Merging and Question Answering

The Reconciler performs two critical functions:
1. Entity Reconciliation: Merge entities across chunks (e.g., "the husband" = "John Smith")
2. Question Answering: Check if new chunks answer previously unanswered questions

In the brain, this is analogous to:
- CA1: Integrating new information with existing memories
- CA3: Pattern completion (recognizing the same entity)
- DG: Pattern separation (distinguishing similar but different entities)

Based on: GSW_prompt_reconcile.pdf
Adapted for: Australian Legal Domain

NOTE: This module has been refactored into smaller components:
- reconciler_prompts.py: System and user prompts
- entity_matcher.py: Entity matching logic (LLM and rule-based)
- question_answerer.py: Question answering logic
- vector_reconciler.py: Vector-based reconciliation

This file contains the main LegalReconciler class and re-exports for compatibility.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.logic.gsw_schema import (
    Actor, State, PredictiveQuestion, ChunkExtraction, GlobalWorkspace
)
from .entity_matcher import EntityMatcher
from .question_answerer import QuestionAnswerer

# Re-export prompts for backwards compatibility
from .reconciler_prompts import RECONCILE_SYSTEM_PROMPT, RECONCILE_USER_PROMPT

# Re-export VectorReconciler for backwards compatibility
from .vector_reconciler import VectorReconciler


class LegalReconciler:
    """
    The Reconciler integrates new chunk extractions into the global workspace.

    Key functions:
    1. Entity Reconciliation - Match "the husband" to "John Smith"
    2. Question Answering - Find answers to pending questions
    3. State Updates - Update entity states with new information
    4. Conflict Resolution - Handle contradictory information
    """

    def __init__(
        self,
        model: str = "google/gemini-2.5-flash",
        api_key: Optional[str] = None,
        use_openrouter: bool = True,
        similarity_threshold: float = 0.85,
        use_toon: bool = True  # Enable TOON format for ~71% token reduction
    ):
        self.model = model
        self.use_openrouter = use_openrouter
        self.similarity_threshold = similarity_threshold
        self.use_toon = use_toon

        if api_key:
            self.api_key = api_key
        elif use_openrouter:
            self.api_key = os.getenv("OPENROUTER_API_KEY")
        else:
            self.api_key = os.getenv("GOOGLE_API_KEY")

        self._setup_client()

        # Initialize helper classes
        self.entity_matcher = EntityMatcher(
            client=self.client,
            model=self.model,
            use_toon=self.use_toon
        )
        self.question_answerer = QuestionAnswerer()

        # Optional: Vector store for entity embeddings
        self.vector_store = None

    def _setup_client(self) -> None:
        """Setup LLM client."""
        if self.use_openrouter and self.api_key:
            import httpx
            self.client = httpx.Client(
                base_url="https://openrouter.ai/api/v1",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )
        else:
            self.client = None

    def reconcile(
        self,
        new_extraction: ChunkExtraction,
        workspace: GlobalWorkspace,
        chunk_text: str
    ) -> Tuple[ChunkExtraction, List[Dict[str, Any]]]:
        """
        Reconcile a new chunk extraction with the global workspace.

        Args:
            new_extraction: The ChunkExtraction from the Operator
            workspace: The current GlobalWorkspace
            chunk_text: Original text of the chunk

        Returns:
            Tuple of (updated_extraction, reconciliation_log)
        """
        reconciliation_log = []

        # Step 1: Entity Reconciliation
        entity_matches = self.entity_matcher.reconcile_entities(
            new_extraction.actors,
            workspace,
            chunk_text
        )

        # Apply entity matches
        for match in entity_matches:
            new_id = match["new_entity_id"]
            existing_id = match["existing_entity_id"]

            # Find the new actor
            new_actor = next(
                (a for a in new_extraction.actors if a.id == new_id),
                None
            )

            if new_actor and existing_id in workspace.actors:
                existing_actor = workspace.actors[existing_id]

                # Merge information
                self._merge_actors(existing_actor, new_actor)

                # Update references in extraction
                self._update_references(new_extraction, new_id, existing_id)

                reconciliation_log.append({
                    "action": "merged",
                    "new_id": new_id,
                    "existing_id": existing_id,
                    "reason": match.get("reason", "")
                })

        # Step 2: Answer Pending Questions
        answered = self.question_answerer.answer_questions(
            workspace.get_unanswered_questions(),
            chunk_text,
            new_extraction
        )

        for answer in answered:
            q_id = answer["question_id"]
            if q_id in workspace.questions:
                workspace.questions[q_id].answerable = True
                workspace.questions[q_id].answer_text = answer["answer_text"]
                workspace.questions[q_id].answer_entity_id = answer.get("answer_entity_id")
                workspace.questions[q_id].answered_in_chunk_id = new_extraction.chunk_id

                reconciliation_log.append({
                    "action": "answered_question",
                    "question_id": q_id,
                    "answer": answer["answer_text"]
                })

        # Step 3: Add new entities to workspace
        for actor in new_extraction.actors:
            # Check if this actor was matched to an existing one
            was_matched = any(
                m["new_entity_id"] == actor.id for m in entity_matches
            )

            if not was_matched:
                workspace.add_actor(actor)
                reconciliation_log.append({
                    "action": "added_new",
                    "entity_id": actor.id,
                    "name": actor.name
                })

        # Step 4: Add new questions
        for question in new_extraction.questions:
            workspace.questions[question.id] = question

        # Step 5: Add verb phrases and links
        for verb in new_extraction.verb_phrases:
            workspace.verb_phrases[verb.id] = verb

        for link in new_extraction.spatio_temporal_links:
            workspace.spatio_temporal_links[link.id] = link

        # Update workspace metadata
        workspace.chunk_count += 1
        workspace.touch()

        return new_extraction, reconciliation_log

    def _merge_actors(self, existing: Actor, new: Actor) -> None:
        """Merge information from new actor into existing actor."""
        # Add new aliases
        for alias in new.aliases:
            if alias not in existing.aliases and alias != existing.name:
                existing.aliases.append(alias)

        # Add the new name as alias if different
        if new.name != existing.name and new.name not in existing.aliases:
            existing.aliases.append(new.name)

        # Add new roles
        for role in new.roles:
            if role not in existing.roles:
                existing.roles.append(role)

        # Add new states
        for state in new.states:
            # Check if we already have this state type with same value
            existing_state = next(
                (s for s in existing.states
                 if s.name == state.name and s.value == state.value),
                None
            )
            if not existing_state:
                state.entity_id = existing.id
                existing.states.append(state)

        # Track source chunks
        for chunk_id in new.source_chunk_ids:
            if chunk_id not in existing.source_chunk_ids:
                existing.source_chunk_ids.append(chunk_id)

    def _update_references(
        self,
        extraction: ChunkExtraction,
        old_id: str,
        new_id: str
    ) -> None:
        """Update all references from old_id to new_id in extraction."""
        # Update verb phrase references
        for verb in extraction.verb_phrases:
            if verb.agent_id == old_id:
                verb.agent_id = new_id
            verb.patient_ids = [
                new_id if pid == old_id else pid
                for pid in verb.patient_ids
            ]
            if verb.temporal_id == old_id:
                verb.temporal_id = new_id
            if verb.spatial_id == old_id:
                verb.spatial_id = new_id

        # Update spatio-temporal links
        for link in extraction.spatio_temporal_links:
            link.linked_entity_ids = [
                new_id if eid == old_id else eid
                for eid in link.linked_entity_ids
            ]

        # Update question references
        for q in extraction.questions:
            if q.target_entity_id == old_id:
                q.target_entity_id = new_id
            if q.answer_entity_id == old_id:
                q.answer_entity_id = new_id

    # Legacy methods for backwards compatibility
    def _reconcile_entities(
        self,
        new_actors: List[Actor],
        workspace: GlobalWorkspace,
        chunk_text: str
    ) -> List[Dict[str, Any]]:
        """Legacy method - delegates to EntityMatcher."""
        return self.entity_matcher.reconcile_entities(new_actors, workspace, chunk_text)

    def _llm_reconcile_entities(
        self,
        new_actors: List[Actor],
        workspace: GlobalWorkspace,
        chunk_text: str
    ) -> List[Dict[str, Any]]:
        """Legacy method - delegates to EntityMatcher."""
        return self.entity_matcher.llm_reconcile(new_actors, workspace, chunk_text)

    def _rule_based_reconciliation(
        self,
        new_actors: List[Actor],
        workspace: GlobalWorkspace
    ) -> List[Dict[str, Any]]:
        """Legacy method - delegates to EntityMatcher."""
        return self.entity_matcher.rule_based_reconcile(new_actors, workspace)

    def _answer_questions(
        self,
        questions: List[PredictiveQuestion],
        chunk_text: str,
        extraction: ChunkExtraction
    ) -> List[Dict[str, Any]]:
        """Legacy method - delegates to QuestionAnswerer."""
        return self.question_answerer.answer_questions(questions, chunk_text, extraction)


__all__ = [
    "LegalReconciler",
    "VectorReconciler",
    "RECONCILE_SYSTEM_PROMPT",
    "RECONCILE_USER_PROMPT",
]
