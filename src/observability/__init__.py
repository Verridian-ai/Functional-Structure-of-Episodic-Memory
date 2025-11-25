# GSW Observability Module
# LangFuse integration for Brain-Inspired Legal AI

from .langfuse_tracer import (
    GSWTracer,
    trace_gsw_operation,
    trace_graph_traversal,
    trace_llm_generation,
    score_retrieval_accuracy,
    get_session_tracker,
)

from .session_memory import (
    EpisodicSessionTracker,
    SessionState,
)

from .scoring import (
    RetrievalScorer,
    AccuracyMetrics,
)

__all__ = [
    # Core tracer
    "GSWTracer",
    # Decorators
    "trace_gsw_operation",
    "trace_graph_traversal",
    "trace_llm_generation",
    # Scoring
    "score_retrieval_accuracy",
    "RetrievalScorer",
    "AccuracyMetrics",
    # Session tracking
    "get_session_tracker",
    "EpisodicSessionTracker",
    "SessionState",
]
