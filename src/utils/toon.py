"""
Token-Oriented Object Notation (TOON) - GSW Integration

TOON provides ~40% token reduction vs JSON for LLM context optimization.
Format: name[count]{col1,col2}\nval1,val2...

Based on: https://github.com/toon-format/toon
Integrated with: GSW (Global Semantic Workspace) for episodic memory compression.

Example:
    JSON (45 tokens):
    {"actors": [{"id": "a1", "name": "John", "type": "person"}]}

    TOON (27 tokens):
    Actors[1]{id,name,type}
    a1,John,person
"""

from typing import List, Any, Dict, Optional, Union
import re


class ToonEncoder:
    """
    Token-Oriented Object Notation (TOON) Encoder.
    Native Python implementation for context optimization.
    """

    @staticmethod
    def _escape_value(val: Any) -> str:
        """Escape a value for TOON format."""
        if val is None:
            return ""
        s = str(val)
        # Quote if contains comma, newline, or leading/trailing whitespace
        if "," in s or "\n" in s or s != s.strip():
            s = s.replace('"', '""')  # Escape internal quotes
            return f'"{s}"'
        return s

    @staticmethod
    def encode(name: str, headers: List[str], data: List[List[Any]]) -> str:
        """
        Encodes a list of lists into a TOON string block.

        Args:
            name: Table name (e.g., "Actors", "VerbPhrases")
            headers: Column names
            data: List of rows, each row is a list of values

        Returns:
            TOON formatted string
        """
        if not data:
            return ""

        count = len(data)
        header_str = f"{name}[{count}]{{{','.join(headers)}}}"

        rows = []
        for row in data:
            processed_row = [ToonEncoder._escape_value(item) for item in row]
            rows.append(",".join(processed_row))

        return f"{header_str}\n" + "\n".join(rows)

    @staticmethod
    def encode_list(name: str, items: List[str]) -> str:
        """Encode a simple 1D list as a TOON table."""
        data = [[item] for item in items]
        return ToonEncoder.encode(name, ["value"], data)

    # =========================================================================
    # GSW-Specific Encoders
    # =========================================================================

    @staticmethod
    def encode_actors(actors: List[Dict]) -> str:
        """
        Encode GSW actors to TOON format.

        Input: List of actor dicts with id, name, actor_type, roles, states
        Output: TOON block with ~40% fewer tokens than JSON
        """
        if not actors:
            return ""

        headers = ["id", "name", "type", "roles", "states"]
        data = []
        for a in actors:
            roles = "|".join(a.get("roles", [])) if a.get("roles") else ""
            # Compact state representation: name=value|name=value
            states = a.get("states", [])
            if isinstance(states, list):
                state_str = "|".join(f"{s.get('name', '')}={s.get('value', '')}" for s in states)
            else:
                state_str = ""

            # Get actor_type value (handle both string and enum)
            actor_type = a.get("actor_type", a.get("type", ""))
            if hasattr(actor_type, "value"):
                actor_type = actor_type.value

            data.append([
                a.get("id", ""),
                a.get("name", ""),
                actor_type,
                roles,
                state_str
            ])

        return ToonEncoder.encode("Actors", headers, data)

    @staticmethod
    def encode_verb_phrases(verbs: List[Dict]) -> str:
        """
        Encode GSW verb phrases to TOON format.

        Columns: id, verb, agent_id, patient_ids (pipe-separated), temporal_id, spatial_id
        """
        if not verbs:
            return ""

        headers = ["id", "verb", "agent", "patients", "temporal", "spatial", "implicit"]
        data = []
        for v in verbs:
            patients = v.get("patient_ids", [])
            patient_str = "|".join(patients) if patients else ""

            data.append([
                v.get("id", ""),
                v.get("verb", ""),
                v.get("agent_id", "") or "",
                patient_str,
                v.get("temporal_id", "") or "",
                v.get("spatial_id", "") or "",
                "1" if v.get("is_implicit") else "0"
            ])

        return ToonEncoder.encode("VerbPhrases", headers, data)

    @staticmethod
    def encode_questions(questions: List[Dict]) -> str:
        """
        Encode GSW questions to TOON format.

        Columns: id, about_id, question, type, answerable, answer
        """
        if not questions:
            return ""

        headers = ["id", "about", "question", "type", "answered", "answer"]
        data = []
        for q in questions:
            # Get question_type value (handle both string and enum)
            q_type = q.get("question_type", "what")
            if hasattr(q_type, "value"):
                q_type = q_type.value

            data.append([
                q.get("id", ""),
                q.get("target_entity_id", "") or "",
                q.get("question_text", ""),
                q_type,
                "1" if q.get("answerable") else "0",
                q.get("answer_text", "") or ""
            ])

        return ToonEncoder.encode("Questions", headers, data)

    @staticmethod
    def encode_links(links: List[Dict]) -> str:
        """
        Encode GSW spatio-temporal links to TOON format.

        Columns: id, entities (pipe-separated), type, value
        """
        if not links:
            return ""

        headers = ["id", "entities", "type", "value"]
        data = []
        for link in links:
            entities = link.get("linked_entity_ids", [])
            entity_str = "|".join(entities) if entities else ""

            # Get tag_type value (handle both string and enum)
            tag_type = link.get("tag_type", "temporal")
            if hasattr(tag_type, "value"):
                tag_type = tag_type.value

            data.append([
                link.get("id", ""),
                entity_str,
                tag_type,
                link.get("tag_value", "") or ""
            ])

        return ToonEncoder.encode("Links", headers, data)

    @staticmethod
    def encode_workspace(workspace_dict: Dict) -> str:
        """
        Encode entire GSW workspace to TOON format.

        This provides massive token savings for context injection.
        Typically ~40-55% reduction vs JSON.

        Args:
            workspace_dict: GlobalWorkspace.model_dump() output

        Returns:
            Full TOON representation of workspace
        """
        blocks = []

        # Header with domain
        domain = workspace_dict.get("domain", "unknown")
        blocks.append(f"# GSW Workspace: {domain}")
        blocks.append("")

        # Actors
        actors = list(workspace_dict.get("actors", {}).values())
        if actors:
            blocks.append(ToonEncoder.encode_actors(actors))
            blocks.append("")

        # Verb Phrases
        verbs = list(workspace_dict.get("verb_phrases", {}).values())
        if verbs:
            blocks.append(ToonEncoder.encode_verb_phrases(verbs))
            blocks.append("")

        # Questions
        questions = list(workspace_dict.get("questions", {}).values())
        if questions:
            blocks.append(ToonEncoder.encode_questions(questions))
            blocks.append("")

        # Spatio-temporal Links
        links = list(workspace_dict.get("spatio_temporal_links", {}).values())
        if links:
            blocks.append(ToonEncoder.encode_links(links))

        return "\n".join(blocks)

    @staticmethod
    def encode_context_summary(workspace_dict: Dict, max_actors: int = 50) -> str:
        """
        Encode a condensed workspace summary for LLM context.

        Useful when full workspace is too large - prioritizes:
        - Most connected actors
        - Unanswered questions
        - Recent verb phrases

        Args:
            workspace_dict: GlobalWorkspace.model_dump() output
            max_actors: Maximum actors to include

        Returns:
            Condensed TOON context
        """
        blocks = []
        domain = workspace_dict.get("domain", "unknown")
        blocks.append(f"# Context: {domain}")
        blocks.append("")

        # Get actors sorted by connection count
        actors = list(workspace_dict.get("actors", {}).values())
        links = list(workspace_dict.get("spatio_temporal_links", {}).values())

        # Count connections per actor
        connection_count = {}
        for link in links:
            for eid in link.get("linked_entity_ids", []):
                connection_count[eid] = connection_count.get(eid, 0) + 1

        # Sort actors by connections
        actors_sorted = sorted(
            actors,
            key=lambda a: connection_count.get(a.get("id", ""), 0),
            reverse=True
        )[:max_actors]

        if actors_sorted:
            blocks.append(ToonEncoder.encode_actors(actors_sorted))
            blocks.append("")

        # Only unanswered questions
        questions = list(workspace_dict.get("questions", {}).values())
        unanswered = [q for q in questions if not q.get("answerable")]
        if unanswered:
            blocks.append(ToonEncoder.encode_questions(unanswered))

        return "\n".join(blocks)


class ToonDecoder:
    """
    TOON Decoder - Parse TOON format back to structured data.
    """

    HEADER_PATTERN = re.compile(r'^(\w+)\[(\d+)\]\{([^}]*)\}$')

    @staticmethod
    def decode(toon_str: str) -> Dict[str, List[Dict]]:
        """
        Decode TOON string to dictionary of tables.

        Returns:
            Dict mapping table names to list of row dicts
        """
        result = {}
        lines = toon_str.strip().split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                i += 1
                continue

            # Try to match header
            match = ToonDecoder.HEADER_PATTERN.match(line)
            if match:
                name = match.group(1)
                count = int(match.group(2))
                headers = [h.strip() for h in match.group(3).split(",")]

                # Read data rows
                rows = []
                for j in range(count):
                    if i + 1 + j < len(lines):
                        row_line = lines[i + 1 + j]
                        values = ToonDecoder._parse_row(row_line, len(headers))
                        row_dict = dict(zip(headers, values))
                        rows.append(row_dict)

                result[name] = rows
                i += count + 1
            else:
                i += 1

        return result

    @staticmethod
    def _parse_row(line: str, expected_cols: int) -> List[str]:
        """Parse a TOON row handling quoted values."""
        values = []
        current = ""
        in_quotes = False

        for char in line:
            if char == '"' and not in_quotes:
                in_quotes = True
            elif char == '"' and in_quotes:
                in_quotes = False
            elif char == ',' and not in_quotes:
                values.append(current)
                current = ""
            else:
                current += char

        values.append(current)

        # Pad if needed
        while len(values) < expected_cols:
            values.append("")

        return values

    @staticmethod
    def decode_workspace(toon_str: str) -> Dict:
        """
        Decode TOON workspace back to dict matching GlobalWorkspace schema.

        This reverses the ToonEncoder.encode_workspace() process.

        Args:
            toon_str: TOON formatted workspace string

        Returns:
            Dict compatible with WorkspaceManager._deserialize_workspace()
        """
        # Parse all tables from TOON
        tables = ToonDecoder.decode(toon_str)

        # Extract domain from header comment
        domain = "unknown"
        for line in toon_str.split("\n"):
            if line.startswith("# GSW Workspace:"):
                domain = line.split(":", 1)[1].strip()
                break

        # Initialize workspace structure
        workspace = {
            "metadata": {
                "created_at": "",
                "last_updated": "",
                "chunk_count": 0,
                "document_count": 0,
                "domain": domain
            },
            "actors": {},
            "verb_phrases": {},
            "questions": {},
            "spatio_temporal_links": {},
            "entity_summaries": {}
        }

        # Decode Actors
        for actor_row in tables.get("Actors", []):
            actor_id = actor_row.get("id", "")

            # Parse roles (pipe-separated)
            roles_str = actor_row.get("roles", "")
            roles = [r.strip() for r in roles_str.split("|") if r.strip()]

            # Parse states (name=value|name=value format)
            states_str = actor_row.get("states", "")
            states = []
            if states_str:
                for state_pair in states_str.split("|"):
                    if "=" in state_pair:
                        name, value = state_pair.split("=", 1)
                        states.append({
                            "id": f"state_{len(states)}",
                            "entity_id": actor_id,
                            "name": name.strip(),
                            "value": value.strip(),
                            "start_date": None,
                            "end_date": None,
                            "source_chunk_id": ""
                        })

            workspace["actors"][actor_id] = {
                "id": actor_id,
                "name": actor_row.get("name", ""),
                "actor_type": actor_row.get("type", "person"),
                "aliases": [],
                "roles": roles,
                "states": states,
                "spatio_temporal_link_ids": [],
                "involved_cases": [],
                "source_chunk_ids": []
            }

        # Decode VerbPhrases
        for verb_row in tables.get("VerbPhrases", []):
            verb_id = verb_row.get("id", "")

            # Parse patient_ids (pipe-separated)
            patients_str = verb_row.get("patients", "")
            patient_ids = [p.strip() for p in patients_str.split("|") if p.strip()]

            workspace["verb_phrases"][verb_id] = {
                "id": verb_id,
                "verb": verb_row.get("verb", ""),
                "agent_id": verb_row.get("agent", "") or None,
                "patient_ids": patient_ids,
                "temporal_id": verb_row.get("temporal", "") or None,
                "spatial_id": verb_row.get("spatial", "") or None,
                "is_implicit": verb_row.get("implicit", "0") == "1",
                "source_chunk_id": ""
            }

        # Decode Questions
        for q_row in tables.get("Questions", []):
            q_id = q_row.get("id", "")

            workspace["questions"][q_id] = {
                "id": q_id,
                "question_text": q_row.get("question", ""),
                "question_type": q_row.get("type", "what"),
                "target_entity_id": q_row.get("about", "") or None,
                "answerable": q_row.get("answered", "0") == "1",
                "answer_text": q_row.get("answer", "") or None,
                "answer_entity_id": None,
                "source_chunk_id": "",
                "answered_in_chunk_id": None
            }

        # Decode Links
        for link_row in tables.get("Links", []):
            link_id = link_row.get("id", "")

            # Parse linked_entity_ids (pipe-separated)
            entities_str = link_row.get("entities", "")
            entity_ids = [e.strip() for e in entities_str.split("|") if e.strip()]

            workspace["spatio_temporal_links"][link_id] = {
                "id": link_id,
                "linked_entity_ids": entity_ids,
                "tag_type": link_row.get("type", "temporal"),
                "tag_value": link_row.get("value", "") or None,
                "source_chunk_id": ""
            }

        return workspace


def measure_compression(json_str: str, toon_str: str) -> Dict[str, Any]:
    """
    Measure token compression between JSON and TOON.

    Returns dict with char counts and estimated token savings.
    """
    json_chars = len(json_str)
    toon_chars = len(toon_str)

    # Rough token estimate (4 chars per token average)
    json_tokens = json_chars / 4
    toon_tokens = toon_chars / 4

    return {
        "json_chars": json_chars,
        "toon_chars": toon_chars,
        "char_reduction": f"{(1 - toon_chars/json_chars)*100:.1f}%",
        "json_tokens_est": int(json_tokens),
        "toon_tokens_est": int(toon_tokens),
        "token_reduction": f"{(1 - toon_tokens/json_tokens)*100:.1f}%"
    }
