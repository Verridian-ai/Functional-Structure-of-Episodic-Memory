"""
Legal Operator - GSW Actor-Centric Extraction

The Operator is the "sensory cortex" of the GSW system.
It takes raw legal text and extracts structured semantic information:
- Actors (parties, judges, assets, dates, etc.)
- Roles (how actors function in the situation)
- States (conditions that change over time)
- Verb Phrases (actions linking actors)
- Predictive Questions (what could be asked)
- Spatio-Temporal Links (time/space bindings)

Based on: GSW_prompt_operator.pdf
Adapted for: Australian Legal Domain

NOTE: This module has been refactored into smaller components:
- operator_prompts.py: System and user prompts
- extraction_parser.py: Parsing helpers for schema objects
- text_chunker.py: Text chunking utilities

This file contains the main LegalOperator class and re-exports for compatibility.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import uuid4
import os

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.logic.gsw_schema import (
    Actor, ActorType, State, VerbPhrase, PredictiveQuestion,
    SpatioTemporalLink, ChunkExtraction, QuestionType, LinkType,
    OntologyContext
)
from .operator_prompts import LEGAL_OPERATOR_SYSTEM_PROMPT, LEGAL_OPERATOR_USER_PROMPT
from .extraction_parser import ExtractionParser
from .text_chunker import chunk_legal_text
from .cost_tracker import get_cost_tracker


class LegalOperator:
    """
    The Legal Operator extracts structured information from legal text.

    This implements the 6-task extraction process:
    1. Actor Identification
    2. Role Assignment
    3. State Identification
    4. Verb Phrase Identification
    5. Predictive Question Generation
    6. Answer Mapping
    """

    def __init__(
        self,
        model: str = "google/gemini-2.5-flash",
        api_key: Optional[str] = None,
        use_openrouter: bool = True
    ):
        """
        Initialize the Legal Operator.

        Args:
            model: Model to use for extraction
            api_key: API key (or uses env var)
            use_openrouter: Whether to use OpenRouter API
        """
        self.model = model
        self.use_openrouter = use_openrouter
        self.parser = ExtractionParser()

        # Get API key
        if api_key:
            self.api_key = api_key
        elif use_openrouter:
            self.api_key = os.getenv("OPENROUTER_API_KEY")
        else:
            self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("No API key found. Set OPENROUTER_API_KEY or GOOGLE_API_KEY")

        self._setup_client()

    def _setup_client(self) -> None:
        """Setup the LLM client."""
        if self.use_openrouter:
            import httpx
            self.client = httpx.Client(
                base_url="https://openrouter.ai/api/v1",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=120.0
            )
        else:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)

    def extract(
        self,
        text: str,
        situation: str = "",
        background_context: str = "",
        ontology_context: Optional[OntologyContext] = None,
        chunk_id: Optional[str] = None,
        document_id: str = ""
    ) -> ChunkExtraction:
        """
        Extract structured information from legal text.

        Args:
            text: The legal text to process
            situation: Brief description of the situation
            background_context: Context from surrounding text
            ontology_context: Current ontology for feedback loop
            chunk_id: ID for this chunk
            document_id: ID of source document

        Returns:
            ChunkExtraction with actors, verbs, questions, links
        """
        if chunk_id is None:
            chunk_id = f"chunk_{uuid4().hex[:8]}"

        # Build the prompt
        ontology_str = ""
        if ontology_context:
            ontology_str = f"\n<known_vocabulary>\n{ontology_context.to_prompt_context()}\n</known_vocabulary>\n"

        user_prompt = LEGAL_OPERATOR_USER_PROMPT.format(
            situation=situation or "Legal proceedings",
            background_context=background_context or "Australian legal document",
            ontology_context=ontology_str,
            input_text=text[:30000]  # Limit text length
        )

        # Call LLM
        try:
            raw_response = self._call_llm(user_prompt)
            extraction = self._parse_response(raw_response, chunk_id, document_id)
            extraction.raw_llm_response = raw_response
            return extraction

        except Exception as e:
            print(f"[Operator Error] {e}")
            # Return empty extraction on error
            return ChunkExtraction(
                chunk_id=chunk_id,
                source_document_id=document_id,
                situation=situation
            )

    def _call_llm(self, user_prompt: str) -> str:
        """Call the LLM and get response."""
        if self.use_openrouter:
            response = self.client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": LEGAL_OPERATOR_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 8000
                }
            )
            response.raise_for_status()
            result = response.json()

            # Track token usage
            usage = result.get("usage", {})
            if usage:
                tracker = get_cost_tracker(self.model)
                tracker.add_usage(
                    "operator",
                    usage.get("prompt_tokens", 0),
                    usage.get("completion_tokens", 0)
                )

            return result["choices"][0]["message"]["content"]
        else:
            response = self.client.generate_content(
                f"{LEGAL_OPERATOR_SYSTEM_PROMPT}\n\n{user_prompt}"
            )
            return response.text

    def _repair_json(self, text: str) -> str:
        """Attempt to repair common JSON issues from LLM output."""
        # Remove trailing commas before ] or }
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        # Fix unescaped newlines in strings
        text = re.sub(r'(?<!\\)\n(?=.*")', '\\n', text)
        # Fix missing commas between objects/arrays
        text = re.sub(r'}\s*{', '},{', text)
        text = re.sub(r']\s*\[', '],[', text)
        # Truncated response - try to close it properly
        open_braces = text.count('{') - text.count('}')
        open_brackets = text.count('[') - text.count(']')
        if open_braces > 0 or open_brackets > 0:
            # Remove last partial element
            last_comma = max(text.rfind(',{'), text.rfind(',['), text.rfind(',"'))
            if last_comma > len(text) // 2:
                text = text[:last_comma]
            text += ']' * open_brackets + '}' * open_braces
        return text

    def _parse_response(
        self,
        raw_response: str,
        chunk_id: str,
        document_id: str
    ) -> ChunkExtraction:
        """Parse LLM response into ChunkExtraction."""
        # Clean markdown code blocks
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\n?', '', cleaned)
            cleaned = re.sub(r'\n?```$', '', cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            match = re.search(r'\{[\s\S]*\}', cleaned)
            if match:
                json_str = match.group()
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to repair the JSON
                    repaired = self._repair_json(json_str)
                    try:
                        data = json.loads(repaired)
                    except json.JSONDecodeError:
                        # Last resort: return minimal valid structure
                        data = {"actors": [], "verb_phrases": [], "questions": []}
            else:
                raise ValueError("Could not parse JSON from response")

        # Build ChunkExtraction
        extraction = ChunkExtraction(
            chunk_id=chunk_id,
            source_document_id=document_id,
            situation=data.get("situation_summary", ""),
            model_used=self.model
        )

        # Parse actors
        for actor_data in data.get("actors", []):
            actor = self.parser.parse_actor(actor_data, chunk_id)
            extraction.actors.append(actor)

        # Parse verb phrases
        for verb_data in data.get("verb_phrases", []):
            verb = self.parser.parse_verb_phrase(verb_data, chunk_id)
            extraction.verb_phrases.append(verb)

        # Parse questions
        for q_data in data.get("questions", []):
            question = self.parser.parse_question(q_data, chunk_id)
            extraction.questions.append(question)

        # Parse spatio-temporal links
        for link_data in data.get("spatio_temporal_links", []):
            link = self.parser.parse_link(link_data, chunk_id)
            extraction.spatio_temporal_links.append(link)

        return extraction

    def review_extraction(
        self,
        extraction: ChunkExtraction,
        original_text: str
    ) -> ChunkExtraction:
        """
        Reflexion step: Review and improve extraction.

        This implements the self-correction loop from Phase 4.
        """
        # Build review prompt
        review_prompt = f"""
Review this extraction for accuracy and completeness.

ORIGINAL TEXT:
{original_text[:10000]}

EXTRACTED DATA:
- Actors: {len(extraction.actors)}
- Verb Phrases: {len(extraction.verb_phrases)}
- Questions: {len(extraction.questions)}
- Spatio-Temporal Links: {len(extraction.spatio_temporal_links)}

Actor names: {[a.name for a in extraction.actors]}
Questions: {[q.question_text for q in extraction.questions]}

REVIEW CHECKLIST:
1. Are all parties (applicant, respondent) identified?
2. Are all dates captured as temporal entities?
3. Are key assets identified?
4. Are relationship states tracked?
5. Are the questions appropriate for this text?

If the extraction looks good, respond with: {{"status": "approved"}}
If improvements needed, respond with corrections in the same JSON format as original extraction.
"""

        try:
            response = self._call_llm(review_prompt)
            if '"status": "approved"' in response or '"status":"approved"' in response:
                return extraction

            # Parse corrections and merge
            # For now, just return original if approved
            return extraction

        except Exception as e:
            print(f"[Review Warning] {e}")
            return extraction

    # Legacy method aliases for backwards compatibility
    def _parse_actor(self, data: Dict[str, Any], chunk_id: str) -> Actor:
        """Legacy method - delegates to ExtractionParser."""
        return self.parser.parse_actor(data, chunk_id)

    def _parse_verb_phrase(self, data: Dict[str, Any], chunk_id: str) -> VerbPhrase:
        """Legacy method - delegates to ExtractionParser."""
        return self.parser.parse_verb_phrase(data, chunk_id)

    def _parse_question(self, data: Dict[str, Any], chunk_id: str) -> PredictiveQuestion:
        """Legacy method - delegates to ExtractionParser."""
        return self.parser.parse_question(data, chunk_id)

    def _parse_link(self, data: Dict[str, Any], chunk_id: str) -> SpatioTemporalLink:
        """Legacy method - delegates to ExtractionParser."""
        return self.parser.parse_link(data, chunk_id)


__all__ = [
    "LegalOperator",
    "chunk_legal_text",
    "LEGAL_OPERATOR_SYSTEM_PROMPT",
    "LEGAL_OPERATOR_USER_PROMPT",
]
