"""
Agents Module - GSW-powered AI agents for legal analysis

Provides agent interfaces for:
- Family Law knowledge querying
- Legal document analysis
- Case timeline reconstruction
- LangGraph/LangChain tool integration
"""

from src.agents.family_law_knowledge import (
    FamilyLawAgent,
    FamilyLawGSWBuilder,
    FamilyLawExtractor,
    FamilyLawDocument
)

from src.agents.gsw_tools import (
    GSWToolRegistry,
    GSWDirectAPI,
    get_gsw_tools,
    set_workspace_path,
    find_parties,
    get_case_questions,
    get_unanswered_questions,
    answer_question,
    find_actors_by_role,
    get_knowledge_context,
    get_workspace_stats,
    get_ontology_vocabulary
)

__all__ = [
    # Knowledge Builder
    "FamilyLawAgent",
    "FamilyLawGSWBuilder",
    "FamilyLawExtractor",
    "FamilyLawDocument",
    # Tool Integration
    "GSWToolRegistry",
    "GSWDirectAPI",
    "get_gsw_tools",
    "set_workspace_path",
    # Individual Tools
    "find_parties",
    "get_case_questions",
    "get_unanswered_questions",
    "answer_question",
    "find_actors_by_role",
    "get_knowledge_context",
    "get_workspace_stats",
    "get_ontology_vocabulary"
]
