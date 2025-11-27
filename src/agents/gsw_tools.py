"""
GSW Tools - LangGraph/LangChain Compatible Tools for GSW Knowledge Access

These tools enable AI agents to query the Global Semantic Workspace.
Designed for integration with:
- LangGraph (ReAct agents)
- LangChain (Tool calling)
- Pydantic AI (structured outputs)

The GSW provides episodic memory capabilities:
- Actor-centric knowledge retrieval
- Predictive question tracking
- Spatio-temporal context binding
- TOON-compressed context for prompts
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Annotated
from pydantic import BaseModel, Field

# For LangChain compatibility
try:
    from langchain_core.tools import tool, BaseTool
    from langchain_core.callbacks import CallbackManagerForToolRun
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    # Provide fallback decorator
    def tool(func):
        func._is_tool = True
        return func

from src.agents.family_law_knowledge import FamilyLawAgent
from src.validation.statutory_rag import StatutoryRAGValidator, ValidationResult
from src.evaluation.multi_judge import MultiJudgeEvaluator, JudgeModel
from src.vsa.span_detector import SpanAlignedVSA, SpanIssue


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUTS
# ============================================================================

class PartyInfo(BaseModel):
    """Information about a party in a case."""
    id: str = Field(description="Unique identifier for the party")
    name: str = Field(description="Name of the party")
    roles: List[str] = Field(description="Roles held by this party (e.g., Applicant, Mother)")
    cases: List[str] = Field(description="Cases this party is involved in")


class QuestionInfo(BaseModel):
    """A predictive question from the GSW."""
    id: str = Field(description="Question identifier")
    question: str = Field(description="The question text")
    type: str = Field(description="Question type (who, what, when, where, why, how)")
    answered: bool = Field(description="Whether the question has been answered")
    answer: Optional[str] = Field(description="The answer if available")


class KnowledgeContext(BaseModel):
    """Compressed knowledge context for LLM prompts."""
    format: str = Field(description="Format of the context (toon or json)")
    content: str = Field(description="The knowledge context content")
    stats: Dict[str, Any] = Field(description="Workspace statistics")


class QueryResult(BaseModel):
    """Generic query result."""
    success: bool = Field(description="Whether the query succeeded")
    results: List[Dict[str, Any]] = Field(description="Query results")
    count: int = Field(description="Number of results")


# ============================================================================
# GSW TOOL REGISTRY
# ============================================================================

class GSWToolRegistry:
    """
    Registry of GSW tools for agent integration.

    Manages the connection to the GSW workspace and provides
    tool methods that can be exposed to LLM agents.
    """

    def __init__(self, workspace_path: Optional[Path] = None):
        """
        Initialize the tool registry.

        Args:
            workspace_path: Path to the GSW workspace JSON file
        """
        self.workspace_path = workspace_path
        self._agent: Optional[FamilyLawAgent] = None

    @property
    def agent(self) -> FamilyLawAgent:
        """Lazy-load the agent."""
        if self._agent is None:
            if self.workspace_path and self.workspace_path.exists():
                self._agent = FamilyLawAgent.load(self.workspace_path)
            else:
                self._agent = FamilyLawAgent()
        return self._agent

    def reload(self, path: Optional[Path] = None) -> None:
        """Reload the workspace from disk."""
        if path:
            self.workspace_path = path
        self._agent = None  # Force reload on next access


# Global registry instance
_registry: Optional[GSWToolRegistry] = None


def get_registry() -> GSWToolRegistry:
    """Get or create the global registry."""
    global _registry
    if _registry is None:
        # Default path
        default_path = Path("data/workspaces/family_law_gsw.json")
        _registry = GSWToolRegistry(default_path)
    return _registry


def set_workspace_path(path: Path) -> None:
    """Set the workspace path for all tools."""
    get_registry().workspace_path = path
    get_registry().reload()


# ============================================================================
# TOOLS - Compatible with LangChain @tool decorator
# ============================================================================

@tool
def find_parties(query: str = "") -> str:
    """
    Find parties (people) in the legal knowledge base.

    Use this tool to search for parties involved in family law cases.
    You can search by name or leave empty to get all parties.

    Args:
        query: Optional name to search for (case-insensitive partial match)

    Returns:
        JSON string with list of parties and their roles
    """
    registry = get_registry()
    results = registry.agent.find_parties(query)
    return json.dumps({
        "success": True,
        "count": len(results),
        "parties": results
    }, indent=2)


@tool
def get_case_questions(case_type: str = "parenting") -> str:
    """
    Get questions about a specific case type from the knowledge base.

    Use this to find what questions are being tracked for parenting,
    property, or other family law matters.

    Args:
        case_type: Type of case - "parenting", "property", "divorce", "child_support"

    Returns:
        JSON string with relevant questions and their answer status
    """
    registry = get_registry()
    results = registry.agent.find_cases_by_type(case_type)
    return json.dumps({
        "success": True,
        "case_type": case_type,
        "count": len(results),
        "questions": results
    }, indent=2)


@tool
def get_unanswered_questions(limit: int = 10) -> str:
    """
    Get unanswered predictive questions from the knowledge base.

    These are questions the system has identified but hasn't answered yet.
    Answering these helps build the knowledge graph.

    Args:
        limit: Maximum number of questions to return (default 10)

    Returns:
        JSON string with unanswered questions
    """
    registry = get_registry()
    results = registry.agent.get_unanswered_questions(limit)
    return json.dumps({
        "success": True,
        "count": len(results),
        "questions": results
    }, indent=2)


@tool
def answer_question(question_id: str, answer: str) -> str:
    """
    Record an answer to a predictive question in the knowledge base.

    Use this to update the knowledge graph with answers to tracked questions.

    Args:
        question_id: The ID of the question to answer (e.g., "q_abc123")
        answer: The answer text

    Returns:
        JSON string confirming the update
    """
    registry = get_registry()
    success = registry.agent.answer_question(question_id, answer)
    return json.dumps({
        "success": success,
        "question_id": question_id,
        "message": "Question answered" if success else "Question not found"
    }, indent=2)


@tool
def find_actors_by_role(role: str) -> str:
    """
    Find all actors with a specific role in the knowledge base.

    Use this to find all Applicants, Respondents, Judges, Mothers, Fathers, etc.

    Args:
        role: The role to search for (e.g., "Applicant", "Judge", "Mother")

    Returns:
        JSON string with matching actors
    """
    registry = get_registry()
    results = registry.agent.get_actors_by_role(role)
    return json.dumps({
        "success": True,
        "role": role,
        "count": len(results),
        "actors": results
    }, indent=2)


@tool
def get_knowledge_context(format: str = "toon", max_actors: int = 30) -> str:
    """
    Get compressed knowledge context for inclusion in prompts.

    Returns the workspace knowledge in either TOON format (40% smaller)
    or JSON format. Use TOON for prompts to save tokens.

    Args:
        format: Output format - "toon" or "json"
        max_actors: Maximum number of actors to include

    Returns:
        Knowledge context in requested format
    """
    registry = get_registry()

    if format.lower() == "toon":
        context = registry.agent.get_context_toon(max_actors)
    else:
        context = json.dumps(registry.agent.get_context_json(max_actors), indent=2)

    stats = registry.agent.stats

    return json.dumps({
        "format": format,
        "stats": {
            "total_actors": stats.get("total_actors", 0),
            "total_questions": stats.get("total_questions", 0),
            "answered_questions": stats.get("answered_questions", 0),
            "domain": stats.get("domain", "unknown")
        },
        "context": context[:5000]  # Limit size for tool output
    }, indent=2)


@tool
def get_workspace_stats() -> str:
    """
    Get statistics about the current knowledge workspace.

    Returns counts of actors, questions, links, and other metadata.

    Returns:
        JSON string with workspace statistics
    """
    registry = get_registry()
    stats = registry.agent.stats
    return json.dumps({
        "success": True,
        "statistics": stats
    }, indent=2)


@tool
def get_ontology_vocabulary() -> str:
    """
    Get the current ontology vocabulary from the knowledge base.

    Returns the common roles, states, and verbs extracted from documents.
    Use this to understand the domain vocabulary for better queries.

    Returns:
        JSON string with ontology vocabulary
    """
    registry = get_registry()
    context = registry.agent.get_ontology_context()
    return json.dumps({
        "success": True,
        "vocabulary": context
    }, indent=2)


@tool
def validate_against_statutes(extraction_json: str, context: str = "") -> str:
    """
    Validate a GSW extraction against Australian statutory sources.

    Use this to check if extracted information complies with Family Law Act
    and related legislation.

    Args:
        extraction_json: JSON string of the extraction to validate
        context: Original document context

    Returns:
        JSON string with validation results including compliance score
    """
    try:
        validator = StatutoryRAGValidator()
        extraction = json.loads(extraction_json)
        result = validator.validate(extraction, context)

        return json.dumps({
            "success": True,
            "compliance_score": result.compliance_score if hasattr(result, 'compliance_score') else 0.0,
            "validation": result.to_dict() if hasattr(result, 'to_dict') else str(result)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@tool
def detect_discrepancies(text: str, extraction_json: str = "") -> str:
    """
    Detect discrepancies and issues in legal text with span-level precision.

    Finds numerical inconsistencies, date conflicts, party mismatches,
    and reference errors.

    Args:
        text: The legal text to analyze
        extraction_json: Optional extraction context

    Returns:
        JSON string with detected issues and their locations
    """
    try:
        detector = SpanAlignedVSA()
        extraction = json.loads(extraction_json) if extraction_json else None
        issues = detector.detect(text, extraction)

        return json.dumps({
            "success": True,
            "issue_count": len(issues) if isinstance(issues, list) else 0,
            "issues": [issue.to_dict() if hasattr(issue, 'to_dict') else str(issue) for issue in issues] if isinstance(issues, list) else []
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@tool
def get_statutory_reference(section: str, act: str = "Family Law Act 1975") -> str:
    """
    Look up a specific section from Australian legislation.

    Args:
        section: Section number to look up
        act: Name of the act (default: Family Law Act 1975)

    Returns:
        JSON string with section content and related provisions
    """
    try:
        validator = StatutoryRAGValidator()
        reference = validator.lookup_section(section, act)

        return json.dumps({
            "success": True,
            "section": section,
            "act": act,
            "content": reference if isinstance(reference, dict) else {"text": str(reference)}
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "section": section,
            "act": act
        }, indent=2)


# ============================================================================
# LANGCHAIN TOOL LIST
# ============================================================================

def get_gsw_tools() -> List:
    """
    Get all GSW tools as a list for LangChain/LangGraph integration.

    Usage:
        from src.agents.gsw_tools import get_gsw_tools, set_workspace_path

        # Set the workspace path
        set_workspace_path(Path("data/workspaces/family_law_gsw.json"))

        # Get tools for agent
        tools = get_gsw_tools()

        # Use with LangGraph
        agent = create_react_agent(model, tools)

    Returns:
        List of tool functions
    """
    return [
        find_parties,
        get_case_questions,
        get_unanswered_questions,
        answer_question,
        find_actors_by_role,
        get_knowledge_context,
        get_workspace_stats,
        get_ontology_vocabulary,
        validate_against_statutes,
        detect_discrepancies,
        get_statutory_reference
    ]


# ============================================================================
# DIRECT API (for non-LangChain usage)
# ============================================================================

class GSWDirectAPI:
    """
    Direct API for GSW access without LangChain.

    Use this for custom integrations or testing.
    """

    def __init__(self, workspace_path: Path):
        set_workspace_path(workspace_path)
        self.registry = get_registry()

    def find_parties(self, query: str = "") -> List[Dict]:
        return self.registry.agent.find_parties(query)

    def get_questions(self, case_type: str = "") -> List[Dict]:
        return self.registry.agent.find_cases_by_type(case_type)

    def get_unanswered(self, limit: int = 20) -> List[Dict]:
        return self.registry.agent.get_unanswered_questions(limit)

    def answer(self, question_id: str, answer: str) -> bool:
        return self.registry.agent.answer_question(question_id, answer)

    def get_context(self, format: str = "toon", max_actors: int = 50) -> str:
        if format == "toon":
            return self.registry.agent.get_context_toon(max_actors)
        return json.dumps(self.registry.agent.get_context_json(max_actors))

    def get_stats(self) -> Dict:
        return self.registry.agent.stats


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    # Demo the tools
    print("GSW Tools Demo")
    print("=" * 60)

    # Set workspace
    workspace = Path("data/workspaces/family_law_gsw.json")
    if workspace.exists():
        set_workspace_path(workspace)

        # Use Direct API for demo (works without LangChain)
        api = GSWDirectAPI(workspace)

        # Test tools
        print("\n1. Workspace Stats:")
        stats = api.get_stats()
        print(f"   Actors: {stats.get('total_actors', 0)}")
        print(f"   Questions: {stats.get('total_questions', 0)}")
        print(f"   Answered: {stats.get('answered_questions', 0)}")
        print(f"   Domain: {stats.get('domain', 'N/A')}")

        print("\n2. Find Parties (first 5):")
        parties = api.find_parties("")[:5]
        for p in parties:
            print(f"   - {p['name']}: {p['roles']}")

        print("\n3. Unanswered Questions (first 5):")
        questions = api.get_unanswered(5)
        for q in questions:
            print(f"   - [{q['type']}] {q['question']}")

        print("\n4. TOON Context Preview:")
        toon = api.get_context("toon", 5)
        print(toon[:800])

        print("\n5. Actors by Role (Judges):")
        judges = api.registry.agent.get_actors_by_role("Judge")[:5]
        for j in judges:
            print(f"   - {j['name']}")

    else:
        print(f"Workspace not found at {workspace}")
        print("Run: python -m src.agents.family_law_knowledge --input <family.jsonl> --output <output.json>")
