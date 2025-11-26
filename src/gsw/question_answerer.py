"""
Question Answerer
=================

Handles checking if chunks answer pending questions.
"""

import re
from typing import Dict, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.logic.gsw_schema import PredictiveQuestion, ChunkExtraction


class QuestionAnswerer:
    """
    Checks if chunk text answers pending questions.

    Uses pattern matching for common question types:
    - When questions (dates)
    - Who questions (person entities)
    - What value questions (monetary amounts)
    """

    def answer_questions(
        self,
        questions: List["PredictiveQuestion"],
        chunk_text: str,
        extraction: "ChunkExtraction"
    ) -> List[Dict[str, Any]]:
        """
        Check if the chunk text answers any pending questions.

        Args:
            questions: List of unanswered PredictiveQuestion objects
            chunk_text: The text of the current chunk
            extraction: The ChunkExtraction with entities

        Returns:
            List of answered question dictionaries
        """
        if not questions:
            return []

        answered = []
        chunk_lower = chunk_text.lower()

        for q in questions:
            q_text = q.question_text.lower()

            # Simple pattern matching for common question types
            answer_found = None

            # When questions
            if "when" in q_text:
                answer_found = self._find_when_answer(q_text, chunk_lower)

            # Who questions
            elif "who" in q_text:
                answer_found = self._find_who_answer(q_text, extraction)

            # What questions about value
            elif "value" in q_text or "worth" in q_text:
                answer_found = self._find_value_answer(chunk_lower)

            if answer_found:
                answered.append({
                    "question_id": q.id,
                    "answer_text": str(answer_found).title(),
                    "answer_entity_id": None,
                    "confidence": 0.7
                })

        return answered

    def _find_when_answer(self, q_text: str, chunk_lower: str) -> str | None:
        """Find date answers for 'when' questions."""
        date_patterns = [
            r'(\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4})',
            r'((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4})',
            r'(\d{4}-\d{2}-\d{2})',
        ]

        # Check if question topic is in chunk
        topic_words = ["separate", "marry", "divorce", "hear", "order", "file"]
        for word in topic_words:
            if word in q_text and word in chunk_lower:
                # Find nearby date
                for pattern in date_patterns:
                    matches = re.findall(pattern, chunk_lower)
                    if matches:
                        return matches[0]
                break

        return None

    def _find_who_answer(
        self,
        q_text: str,
        extraction: "ChunkExtraction"
    ) -> str | None:
        """Find person answers for 'who' questions."""
        for actor in extraction.actors:
            if actor.actor_type.value == "person":
                if any(role.lower() in q_text for role in actor.roles):
                    return actor.name
        return None

    def _find_value_answer(self, chunk_lower: str) -> str | None:
        """Find monetary value answers."""
        money_pattern = r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:million|m))?'
        matches = re.findall(money_pattern, chunk_lower)
        if matches:
            return matches[0]
        return None
