"""
Observability Data Models
=========================

Data classes and types for GSW observability.
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class OperationType(str, Enum):
    """Types of GSW operations to trace."""
    GRAPH_TRAVERSAL = "graph_traversal"
    LLM_GENERATION = "llm_generation"
    ENTITY_EXTRACTION = "entity_extraction"
    RECONCILIATION = "reconciliation"
    SPACETIME_LINKING = "spacetime_linking"
    VECTOR_SEARCH = "vector_search"
    QUESTION_ANSWERING = "question_answering"
    SESSION_UPDATE = "session_update"


@dataclass
class GraphActivation:
    """Represents a single node/edge activation in the knowledge graph."""
    entity_id: str
    entity_type: str  # actor, state, verb_phrase, question, spatio_temporal_link
    entity_name: Optional[str] = None
    activation_score: float = 1.0
    traversal_depth: int = 0
    connected_entities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TraversalResult:
    """Complete result of a graph traversal operation."""
    query: str
    activated_nodes: List[GraphActivation]
    traversal_path: List[str]  # Ordered list of entity_ids visited
    total_nodes_scanned: int
    nodes_activated: int
    max_depth_reached: int
    latency_ms: float
    relevance_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class LatencyBreakdown:
    """Detailed latency metrics for a GSW operation."""
    total_ms: float
    graph_traversal_ms: float = 0.0
    vector_search_ms: float = 0.0
    llm_generation_ms: float = 0.0
    reconciliation_ms: float = 0.0
    spacetime_linking_ms: float = 0.0
    serialization_ms: float = 0.0
    other_ms: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "total_ms": self.total_ms,
            "graph_traversal_ms": self.graph_traversal_ms,
            "vector_search_ms": self.vector_search_ms,
            "llm_generation_ms": self.llm_generation_ms,
            "reconciliation_ms": self.reconciliation_ms,
            "spacetime_linking_ms": self.spacetime_linking_ms,
            "serialization_ms": self.serialization_ms,
            "other_ms": self.other_ms,
        }

    def get_breakdown_percentages(self) -> Dict[str, float]:
        """Get latency as percentages of total."""
        if self.total_ms == 0:
            return {}
        return {k: (v / self.total_ms) * 100 for k, v in self.to_dict().items() if k != "total_ms"}
