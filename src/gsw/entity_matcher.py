"""
Entity Matcher
==============

Rule-based and LLM-based entity matching for reconciliation.
"""

import json
import re
from typing import Dict, List, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.logic.gsw_schema import Actor, GlobalWorkspace

from .reconciler_prompts import RECONCILE_SYSTEM_PROMPT, RECONCILE_USER_PROMPT
from src.utils.toon import ToonEncoder
from .cost_tracker import get_cost_tracker


class EntityMatcher:
    """
    Handles entity matching between new extractions and workspace.

    Supports both LLM-based and rule-based reconciliation.
    """

    def __init__(
        self,
        client: Optional[Any] = None,
        model: str = "google/gemini-2.5-flash",
        use_toon: bool = True
    ):
        self.client = client
        self.model = model
        self.use_toon = use_toon

    def reconcile_entities(
        self,
        new_actors: List["Actor"],
        workspace: "GlobalWorkspace",
        chunk_text: str
    ) -> List[Dict[str, Any]]:
        """
        Find matches between new actors and existing workspace actors.
        """
        if not workspace.actors or not new_actors:
            return []

        # Try LLM-based reconciliation first
        if self.client:
            try:
                return self.llm_reconcile(new_actors, workspace, chunk_text)
            except Exception as e:
                print(f"[EntityMatcher Warning] LLM reconciliation failed: {e}")

        # Fall back to rule-based reconciliation
        return self.rule_based_reconcile(new_actors, workspace)

    def llm_reconcile(
        self,
        new_actors: List["Actor"],
        workspace: "GlobalWorkspace",
        chunk_text: str
    ) -> List[Dict[str, Any]]:
        """Use LLM for entity reconciliation."""
        # Build existing entities summary
        existing_summary = []
        for actor in list(workspace.actors.values())[:50]:  # Limit for context
            existing_summary.append({
                "id": actor.id,
                "name": actor.name,
                "aliases": actor.aliases,
                "roles": actor.roles,
                "type": actor.actor_type.value
            })

        # Build new entities summary
        new_summary = []
        for actor in new_actors:
            new_summary.append({
                "id": actor.id,
                "name": actor.name,
                "aliases": actor.aliases,
                "roles": actor.roles,
                "type": actor.actor_type.value
            })

        # Build unanswered questions summary
        unanswered = workspace.get_unanswered_questions()[:20]
        questions_summary = [
            {"id": q.id, "question": q.question_text}
            for q in unanswered
        ]

        # Format entities using TOON (~71% token reduction) or JSON
        if self.use_toon:
            existing_str = self._format_actors_toon(existing_summary)
            new_str = self._format_actors_toon(new_summary)
            questions_str = self._format_questions_toon(questions_summary)
        else:
            existing_str = json.dumps(existing_summary, indent=2)
            new_str = json.dumps(new_summary, indent=2)
            questions_str = json.dumps(questions_summary, indent=2)

        prompt = RECONCILE_USER_PROMPT.format(
            existing_entities=existing_str,
            new_entities=new_str,
            unanswered_questions=questions_str,
            chunk_text=chunk_text[:5000]
        )

        response = self.client.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": RECONCILE_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 4000
            }
        )
        response.raise_for_status()
        result = response.json()

        # Track token usage
        usage = result.get("usage", {})
        if usage:
            tracker = get_cost_tracker(self.model)
            tracker.add_usage(
                "reconciler",
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0)
            )

        content = result["choices"][0]["message"]["content"]

        # Parse response
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\n?', '', cleaned)
            cleaned = re.sub(r'\n?```$', '', cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r'\{[\s\S]*\}', cleaned)
            if match:
                json_str = match.group()
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
                    repaired = self._repair_json(json_str)
                    try:
                        data = json.loads(repaired)
                    except json.JSONDecodeError:
                        return []
            else:
                return []
        return data.get("entity_matches", [])

    def rule_based_reconcile(
        self,
        new_actors: List["Actor"],
        workspace: "GlobalWorkspace"
    ) -> List[Dict[str, Any]]:
        """
        Rule-based entity reconciliation fallback.

        Matches entities based on:
        - Exact name match
        - Alias match
        - Role alignment
        """
        matches = []

        for new_actor in new_actors:
            new_name = new_actor.name.lower().strip()
            new_aliases = [a.lower().strip() for a in new_actor.aliases]

            for existing_id, existing_actor in workspace.actors.items():
                existing_name = existing_actor.name.lower().strip()
                existing_aliases = [a.lower().strip() for a in existing_actor.aliases]

                # Check for name/alias matches
                match_found = False
                reason = ""

                # Exact name match
                if new_name == existing_name:
                    match_found = True
                    reason = f"Exact name match: {new_actor.name}"

                # New name in existing aliases
                elif new_name in existing_aliases:
                    match_found = True
                    reason = f"Name matches alias: {new_actor.name}"

                # Existing name in new aliases
                elif existing_name in new_aliases:
                    match_found = True
                    reason = f"Alias matches name: {existing_actor.name}"

                # Cross-alias match
                elif set(new_aliases) & set(existing_aliases):
                    match_found = True
                    common = list(set(new_aliases) & set(existing_aliases))[0]
                    reason = f"Common alias: {common}"

                # Role-based matching for common legal terms
                if not match_found:
                    match_found, reason = self._check_role_match(
                        new_name, new_aliases, existing_actor
                    )

                if match_found:
                    matches.append({
                        "new_entity_id": new_actor.id,
                        "existing_entity_id": existing_id,
                        "confidence": 0.8,
                        "reason": reason
                    })
                    break  # Only match to one existing entity

        return matches

    def _check_role_match(
        self,
        new_name: str,
        new_aliases: List[str],
        existing_actor: "Actor"
    ) -> tuple:
        """Check for role-based entity matches."""
        # Match "the husband"/"the wife" patterns
        role_mappings = {
            "the husband": ["husband", "applicant husband", "respondent husband"],
            "the wife": ["wife", "applicant wife", "respondent wife"],
            "the applicant": ["applicant"],
            "the respondent": ["respondent"],
            "the child": ["child", "subject child"],
        }

        for term, related_roles in role_mappings.items():
            if new_name == term or term in new_aliases:
                # Check if existing actor has matching role
                existing_roles_lower = [r.lower() for r in existing_actor.roles]
                if any(r in existing_roles_lower for r in related_roles):
                    return True, f"Role-based match: {term} -> {existing_actor.name}"

        return False, ""

    def _repair_json(self, text: str) -> str:
        """Attempt to repair common JSON issues from LLM output."""
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        text = re.sub(r'}\s*{', '},{', text)
        text = re.sub(r']\s*\[', '],[', text)
        open_braces = text.count('{') - text.count('}')
        open_brackets = text.count('[') - text.count(']')
        if open_braces > 0 or open_brackets > 0:
            last_comma = max(text.rfind(',{'), text.rfind(',['), text.rfind(',"'))
            if last_comma > len(text) // 2:
                text = text[:last_comma]
            text += ']' * open_brackets + '}' * open_braces
        return text

    # =========================================================================
    # TOON Formatting Helpers (~71% token reduction)
    # =========================================================================

    def _format_actors_toon(self, actors: List[Dict]) -> str:
        """
        Format actors in TOON format for compact LLM prompts.

        Example output:
        Actors[3]{id,name,type,aliases,roles}
        actor_001,John Smith,person,the husband|Mr Smith,Applicant|Husband
        actor_002,Jane Smith,person,the wife,Respondent|Wife
        actor_003,Family Court,organization,,Court
        """
        if not actors:
            return "No existing entities."

        headers = ["id", "name", "type", "aliases", "roles"]
        data = []
        for a in actors:
            aliases = a.get("aliases", [])
            aliases_str = "|".join(aliases) if aliases else ""
            roles = a.get("roles", [])
            roles_str = "|".join(roles) if roles else ""

            data.append([
                a.get("id", ""),
                a.get("name", ""),
                a.get("type", ""),
                aliases_str,
                roles_str
            ])

        return ToonEncoder.encode("Actors", headers, data)

    def _format_questions_toon(self, questions: List[Dict]) -> str:
        """
        Format questions in TOON format for compact LLM prompts.

        Example output:
        Questions[2]{id,question}
        q_001,When did the parties separate?
        q_002,What is the value of the matrimonial home?
        """
        if not questions:
            return "No unanswered questions."

        headers = ["id", "question"]
        data = [
            [q.get("id", ""), q.get("question", "")]
            for q in questions
        ]

        return ToonEncoder.encode("Questions", headers, data)
