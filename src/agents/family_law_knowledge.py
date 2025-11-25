"""
Family Law GSW Knowledge System

Builds and manages a Global Semantic Workspace for Family Law documents.
Provides agent interface for querying legal knowledge.

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.logic.gsw_schema import (
    GlobalWorkspace, Actor, State, VerbPhrase, PredictiveQuestion,
    SpatioTemporalLink, ActorType, QuestionType, LinkType
)
from src.gsw.workspace import WorkspaceManager
from src.utils.toon import ToonEncoder, ToonDecoder


# ============================================================================
# FAMILY LAW DOMAIN VOCABULARY
# ============================================================================

FAMILY_LAW_ROLES = [
    "Applicant", "Respondent", "Independent Children's Lawyer", "Child",
    "Mother", "Father", "Husband", "Wife", "Partner", "De Facto Partner",
    "Judge", "Magistrate", "Registrar", "Family Consultant",
    "Expert Witness", "Valuer", "Accountant", "Psychologist"
]

FAMILY_LAW_STATES = [
    "RelationshipStatus", "CustodyArrangement", "ResidenceArrangement",
    "EmploymentStatus", "FinancialPosition", "PropertyValue",
    "SuperannuationBalance", "ChildSupportObligation", "SpousalMaintenance",
    "ParentingTime", "SchoolArrangement", "HealthStatus"
]

FAMILY_LAW_VERBS = [
    "filed", "ordered", "consented", "separated", "married", "divorced",
    "appealed", "granted", "dismissed", "varied", "contravened",
    "relocated", "valued", "distributed", "contributed", "disclosed"
]

FAMILY_LAW_QUESTIONS = {
    "parenting": [
        "Who has primary care of the children?",
        "What are the current parenting arrangements?",
        "When do the children spend time with each parent?",
        "Where do the children live?",
        "What school do the children attend?",
        "Is there a family violence history?",
        "What are the children's wishes?"
    ],
    "property": [
        "What is the total asset pool value?",
        "What are the contributions of each party?",
        "What are the future needs of each party?",
        "What property is held by each party?",
        "What superannuation does each party hold?",
        "What debts exist in the asset pool?",
        "How should the property be divided?"
    ],
    "procedural": [
        "When did the parties separate?",
        "When was the application filed?",
        "What orders are being sought?",
        "What is the current court stage?",
        "Are there any interim orders in place?"
    ]
}


# ============================================================================
# DOCUMENT PROCESSOR
# ============================================================================

@dataclass
class FamilyLawDocument:
    """Parsed family law document."""
    doc_id: str
    citation: str
    date: Optional[str]
    court: str
    jurisdiction: str
    text: str
    case_type: str = ""  # parenting, property, divorce, etc.

    # Extracted metadata
    parties: List[str] = field(default_factory=list)
    judge: Optional[str] = None
    catchwords: List[str] = field(default_factory=list)


class FamilyLawExtractor:
    """
    Extract structured information from family law documents.

    Uses pattern matching + heuristics for fast extraction without LLM.
    For production, combine with GSW Operator for deeper extraction.
    """

    # Common patterns in family law cases
    PARTY_PATTERNS = [
        r'([A-Z][a-z]+)\s+(?:and|&)\s+([A-Z][a-z]+)',  # "Smith and Jones"
        r'(?:Applicant|Mother|Father|Wife|Husband):\s*([A-Z][^,\n]+)',
        r'(?:Respondent):\s*([A-Z][^,\n]+)',
        r'\[([A-Z]+)\]\s+(?:and|&)\s+\[([A-Z]+)\]',  # [ABC] and [XYZ] anonymized
    ]

    JUDGE_PATTERNS = [
        r'(?:Before|Judge|Justice|Magistrate):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'(?:JUDGMENT OF|Decision of)\s+(?:Judge|Justice)\s+([A-Z][a-z]+)',
    ]

    DATE_PATTERNS = [
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(\d{4}-\d{2}-\d{2})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
    ]

    CASE_TYPE_KEYWORDS = {
        "parenting": ["parenting order", "children", "custody", "live with", "spend time",
                      "relocation", "school", "best interests of the child"],
        "property": ["property settlement", "asset pool", "contributions", "superannuation",
                     "section 79", "property adjustment", "financial"],
        "divorce": ["divorce", "dissolution", "marriage certificate"],
        "child_support": ["child support", "assessment", "departure"],
        "spousal_maintenance": ["spousal maintenance", "section 72", "maintenance order"],
        "contravention": ["contravention", "breach", "compliance"]
    }

    def extract_document(self, raw_doc: Dict) -> FamilyLawDocument:
        """Extract structured data from raw corpus document."""
        text = raw_doc.get("text", "")[:50000]  # Limit text size
        citation = raw_doc.get("citation", "")

        # Basic metadata
        doc = FamilyLawDocument(
            doc_id=raw_doc.get("version_id", f"doc_{hash(citation) % 100000}"),
            citation=citation,
            date=raw_doc.get("date"),
            court=self._extract_court(citation),
            jurisdiction=raw_doc.get("jurisdiction", ""),
            text=text
        )

        # Extract parties
        doc.parties = self._extract_parties(text, citation)

        # Extract judge
        doc.judge = self._extract_judge(text)

        # Determine case type
        doc.case_type = self._determine_case_type(text)

        # Extract catchwords if present
        doc.catchwords = self._extract_catchwords(text)

        return doc

    def _extract_court(self, citation: str) -> str:
        """Extract court from citation."""
        court_map = {
            "FamCA": "Family Court of Australia",
            "FamCAFC": "Family Court Full Court",
            "FCFCOA": "Federal Circuit and Family Court",
            "FCA": "Federal Court",
            "FCCA": "Federal Circuit Court",
        }
        for code, name in court_map.items():
            if code in citation:
                return name
        return "Unknown"

    def _extract_parties(self, text: str, citation: str) -> List[str]:
        """Extract party names from text."""
        parties = []

        # Try citation first (e.g., "Smith & Smith")
        citation_match = re.search(r'^([A-Z][a-z]+(?:\s+\([A-Z]+\))?)\s*(?:&|and|v)\s*([A-Z][a-z]+)', citation)
        if citation_match:
            parties.extend([citation_match.group(1), citation_match.group(2)])

        # Check for anonymized parties
        anon_matches = re.findall(r'\[([A-Z]{2,4})\]', citation)
        if anon_matches:
            parties.extend([f"[{m}]" for m in anon_matches])

        return list(set(parties))

    def _extract_judge(self, text: str) -> Optional[str]:
        """Extract judge name."""
        for pattern in self.JUDGE_PATTERNS:
            match = re.search(pattern, text[:2000], re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _determine_case_type(self, text: str) -> str:
        """Determine case type from keywords."""
        text_lower = text.lower()
        scores = {}

        for case_type, keywords in self.CASE_TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[case_type] = score

        if scores:
            return max(scores, key=scores.get)
        return "general"

    def _extract_catchwords(self, text: str) -> List[str]:
        """Extract catchwords section if present."""
        match = re.search(r'(?:CATCHWORDS?|Catchwords?):\s*([^\n]+(?:\n[^\n]+)*?)(?=\n\n|LEGISLATION)', text[:5000])
        if match:
            catchwords_text = match.group(1)
            # Split on common delimiters
            return [cw.strip() for cw in re.split(r'[;\-–]', catchwords_text) if cw.strip()]
        return []


# ============================================================================
# GSW BUILDER
# ============================================================================

class FamilyLawGSWBuilder:
    """
    Builds a Global Semantic Workspace from Family Law documents.

    This creates the knowledge structure for agent integration.
    """

    def __init__(self, workspace: Optional[GlobalWorkspace] = None):
        self.workspace = workspace or GlobalWorkspace(domain="family_law")
        self.extractor = FamilyLawExtractor()

        # Track statistics
        self.stats = {
            "documents_processed": 0,
            "actors_extracted": 0,
            "questions_generated": 0,
            "case_types": defaultdict(int)
        }

    def process_document(self, raw_doc: Dict) -> None:
        """Process a single document into the workspace."""
        doc = self.extractor.extract_document(raw_doc)

        # Create actors for parties
        for party_name in doc.parties:
            actor = self._create_party_actor(party_name, doc)
            self.workspace.add_actor(actor)
            self.stats["actors_extracted"] += 1

        # Create actor for judge if present
        if doc.judge:
            judge_actor = Actor(
                name=doc.judge,
                actor_type=ActorType.PERSON,
                roles=["Judge"],
                source_chunk_ids=[doc.doc_id]
            )
            self.workspace.add_actor(judge_actor)

        # Create court/location actor
        court_actor = Actor(
            name=doc.court,
            actor_type=ActorType.ORGANIZATION,
            roles=["Court"],
            source_chunk_ids=[doc.doc_id]
        )
        self.workspace.add_actor(court_actor)

        # Create temporal link for case date
        if doc.date:
            temporal_actor = Actor(
                name=doc.date,
                actor_type=ActorType.TEMPORAL,
                roles=["Decision Date"]
            )
            self.workspace.add_actor(temporal_actor)

            # Link parties to this date
            party_ids = [self.workspace.find_actor_by_name(p).id
                        for p in doc.parties
                        if self.workspace.find_actor_by_name(p)]
            if party_ids:
                link = SpatioTemporalLink(
                    linked_entity_ids=party_ids + [temporal_actor.id],
                    tag_type=LinkType.TEMPORAL,
                    tag_value=doc.date,
                    source_chunk_id=doc.doc_id
                )
                self.workspace.add_spatio_temporal_link(link)

        # Generate predictive questions based on case type
        questions = self._generate_questions(doc)
        for q in questions:
            self.workspace.add_question(q)
            self.stats["questions_generated"] += 1

        self.stats["documents_processed"] += 1
        self.stats["case_types"][doc.case_type] += 1
        self.workspace.document_count += 1
        self.workspace.touch()

    def _create_party_actor(self, name: str, doc: FamilyLawDocument) -> Actor:
        """Create an actor for a party."""
        # Determine role from context
        roles = []
        text_lower = doc.text.lower()
        name_lower = name.lower().replace("[", "").replace("]", "")

        # Check for role keywords near party name
        if "applicant" in text_lower[:2000]:
            roles.append("Applicant")
        if "respondent" in text_lower[:2000]:
            roles.append("Respondent")
        if "mother" in text_lower and any(x in name_lower for x in ["ms", "mrs", "mother"]):
            roles.append("Mother")
        if "father" in text_lower and any(x in name_lower for x in ["mr", "father"]):
            roles.append("Father")

        if not roles:
            roles = ["Party"]

        return Actor(
            name=name,
            actor_type=ActorType.PERSON,
            roles=roles,
            involved_cases=[doc.citation],
            source_chunk_ids=[doc.doc_id]
        )

    def _generate_questions(self, doc: FamilyLawDocument) -> List[PredictiveQuestion]:
        """Generate predictive questions for a document."""
        questions = []

        # Get questions based on case type
        case_questions = FAMILY_LAW_QUESTIONS.get(doc.case_type, [])
        case_questions.extend(FAMILY_LAW_QUESTIONS.get("procedural", []))

        for q_text in case_questions[:5]:  # Limit to 5 questions per doc
            q = PredictiveQuestion(
                question_text=q_text,
                question_type=self._classify_question(q_text),
                answerable=False,  # Will be answered during agent interaction
                source_chunk_id=doc.doc_id
            )
            questions.append(q)

        return questions

    def _classify_question(self, question: str) -> QuestionType:
        """Classify question type."""
        q_lower = question.lower()
        if q_lower.startswith("who"):
            return QuestionType.WHO
        elif q_lower.startswith("what"):
            return QuestionType.WHAT
        elif q_lower.startswith("when"):
            return QuestionType.WHEN
        elif q_lower.startswith("where"):
            return QuestionType.WHERE
        elif q_lower.startswith("why"):
            return QuestionType.WHY
        elif q_lower.startswith("how much") or "value" in q_lower:
            return QuestionType.HOW_MUCH
        else:
            return QuestionType.HOW

    def build_from_jsonl(self, jsonl_path: Path, max_docs: Optional[int] = None,
                         progress_interval: int = 100) -> GlobalWorkspace:
        """Build workspace from JSONL file."""
        print(f"[GSW Builder] Processing: {jsonl_path}")
        start_time = datetime.now()

        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if max_docs and i >= max_docs:
                    break

                try:
                    doc = json.loads(line)
                    self.process_document(doc)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"[Warning] Error processing doc {i}: {e}")
                    continue

                if (i + 1) % progress_interval == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = (i + 1) / elapsed if elapsed > 0 else 0
                    print(f"[Progress] {i+1} docs | {rate:.0f}/sec | "
                          f"Actors: {len(self.workspace.actors)} | "
                          f"Questions: {len(self.workspace.questions)}")

        elapsed = datetime.now() - start_time
        print(f"\n[Complete] Processed {self.stats['documents_processed']} documents in {elapsed}")
        print(f"[Stats] Actors: {len(self.workspace.actors)}, "
              f"Questions: {len(self.workspace.questions)}, "
              f"Links: {len(self.workspace.spatio_temporal_links)}")

        return self.workspace

    def get_statistics(self) -> Dict[str, Any]:
        """Get builder statistics."""
        return {
            **self.stats,
            "workspace_stats": self.workspace.get_statistics()
        }


# ============================================================================
# AGENT INTERFACE
# ============================================================================

class FamilyLawAgent:
    """
    Agent interface for querying Family Law GSW knowledge.

    Provides natural language query capabilities over the workspace.
    Designed for integration with LangGraph/LangChain agents.
    """

    def __init__(self, workspace_path: Optional[Path] = None):
        if workspace_path and workspace_path.exists():
            self.manager = WorkspaceManager.load(workspace_path)
        else:
            self.manager = WorkspaceManager(GlobalWorkspace(domain="family_law"))

        self.workspace = self.manager.workspace

    @property
    def stats(self) -> Dict[str, Any]:
        """Get workspace statistics."""
        return self.manager.get_statistics()

    # =========================================================================
    # QUERY METHODS (for agent tool integration)
    # =========================================================================

    def find_parties(self, query: str = "") -> List[Dict[str, Any]]:
        """
        Find parties in the workspace.

        Args:
            query: Optional name filter

        Returns:
            List of party information dicts
        """
        results = []
        for actor in self.workspace.actors.values():
            if actor.actor_type == ActorType.PERSON and "Party" in actor.roles or any(
                r in actor.roles for r in ["Applicant", "Respondent", "Mother", "Father"]
            ):
                if not query or query.lower() in actor.name.lower():
                    results.append({
                        "id": actor.id,
                        "name": actor.name,
                        "roles": actor.roles,
                        "cases": actor.involved_cases[:5],
                        "states": [{"name": s.name, "value": s.value} for s in actor.states]
                    })
        return results[:50]  # Limit results

    def find_cases_by_type(self, case_type: str) -> List[Dict[str, Any]]:
        """Find cases by type (parenting, property, etc.)."""
        # This would require storing case_type in metadata
        # For now, search questions
        results = []
        case_type_lower = case_type.lower()

        for q in self.workspace.questions.values():
            q_text_lower = q.question_text.lower()
            if case_type_lower in ["parenting", "children", "custody"] and \
               any(kw in q_text_lower for kw in ["children", "parenting", "custody", "care"]):
                results.append({
                    "question_id": q.id,
                    "question": q.question_text,
                    "answered": q.answerable,
                    "answer": q.answer_text
                })
            elif case_type_lower in ["property", "financial", "asset"] and \
                 any(kw in q_text_lower for kw in ["property", "asset", "value", "contribution"]):
                results.append({
                    "question_id": q.id,
                    "question": q.question_text,
                    "answered": q.answerable,
                    "answer": q.answer_text
                })

        return results[:20]

    def get_unanswered_questions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get unanswered predictive questions."""
        unanswered = self.workspace.get_unanswered_questions()
        return [
            {
                "id": q.id,
                "question": q.question_text,
                "type": q.question_type.value,
                "target_entity": q.target_entity_id
            }
            for q in unanswered[:limit]
        ]

    def answer_question(self, question_id: str, answer: str) -> bool:
        """Mark a question as answered."""
        if question_id in self.workspace.questions:
            q = self.workspace.questions[question_id]
            q.answerable = True
            q.answer_text = answer
            self.workspace.touch()
            return True
        return False

    def get_timeline(self, party_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get chronological timeline of events."""
        return self.manager.get_timeline()

    def get_actors_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Find actors by their role."""
        actors = self.manager.query_actors_by_role(role)
        return [
            {
                "id": a.id,
                "name": a.name,
                "roles": a.roles,
                "type": a.actor_type.value
            }
            for a in actors
        ]

    # =========================================================================
    # CONTEXT GENERATION (for LLM prompts)
    # =========================================================================

    def get_context_toon(self, max_actors: int = 50) -> str:
        """
        Get workspace context in TOON format for LLM prompts.

        Returns compressed representation (~40% smaller than JSON).
        """
        return self.workspace.to_toon_summary(max_actors)

    def get_context_json(self, max_actors: int = 50) -> Dict[str, Any]:
        """Get workspace context as JSON for API integration."""
        ws_dict = self.manager._serialize_workspace(self.workspace)

        # Limit actors if needed
        if len(ws_dict.get("actors", {})) > max_actors:
            # Keep most connected actors
            actors = list(ws_dict["actors"].values())
            ws_dict["actors"] = {a["id"]: a for a in actors[:max_actors]}

        return ws_dict

    def get_ontology_context(self) -> str:
        """Get ontology context for Operator prompts."""
        return self.manager.get_ontology_context().to_prompt_context()

    # =========================================================================
    # PERSISTENCE
    # =========================================================================

    def save(self, path: Path) -> None:
        """Save workspace to file."""
        self.manager.storage_path = path
        self.manager.save()

    @classmethod
    def load(cls, path: Path) -> "FamilyLawAgent":
        """Load agent from saved workspace."""
        agent = cls()
        agent.manager = WorkspaceManager.load(path)
        agent.workspace = agent.manager.workspace
        return agent


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Build Family Law GSW from corpus."""
    import argparse

    parser = argparse.ArgumentParser(description="Build Family Law GSW Knowledge System")
    parser.add_argument("--input", required=True, help="Path to family.jsonl")
    parser.add_argument("--output", required=True, help="Output workspace path")
    parser.add_argument("--max-docs", type=int, default=None, help="Max documents to process")
    parser.add_argument("--progress", type=int, default=100, help="Progress interval")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    # Build workspace
    builder = FamilyLawGSWBuilder()
    workspace = builder.build_from_jsonl(
        input_path,
        max_docs=args.max_docs,
        progress_interval=args.progress
    )

    # Save workspace
    manager = WorkspaceManager(workspace, output_path)
    manager.save()

    # Print statistics
    stats = builder.get_statistics()
    print("\n" + "=" * 60)
    print("FAMILY LAW GSW KNOWLEDGE SYSTEM")
    print("=" * 60)
    print(f"Documents: {stats['documents_processed']}")
    print(f"Actors: {stats['actors_extracted']}")
    print(f"Questions: {stats['questions_generated']}")
    print(f"Case Types: {dict(stats['case_types'])}")
    print(f"\nWorkspace saved to: {output_path}")

    # Demo TOON output
    print("\n" + "=" * 60)
    print("TOON CONTEXT PREVIEW (for LLM prompts):")
    print("=" * 60)
    agent = FamilyLawAgent()
    agent.workspace = workspace
    toon_context = agent.get_context_toon(max_actors=10)
    print(toon_context[:2000])


if __name__ == "__main__":
    main()
