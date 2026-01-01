# GSW Observability Module
# LangFuse integration for Brain-Inspired Legal AI

# Core tracer and models
# Decorators
from .decorators import (
    score_retrieval_accuracy,
    trace_graph_traversal,
    trace_gsw_operation,
    trace_llm_generation,
)
from .models import (
    GraphActivation,
    LatencyBreakdown,
    OperationType,
    TraversalResult,
)

# Scoring
from .scoring import (
    AccuracyMetrics,
    RetrievalScorer,
    ScoreCategory,
    ScoringWeights,
    batch_evaluate,
    create_evaluation_dataset,
)

# Session memory
from .session_memory import (
    EpisodicSessionTracker,
    SessionState,
)

# Span wrappers
from .span_wrapper import DummySpan, SpanWrapper
from .tracer_core import GSWTracer

# Utilities
from .utils import get_session_tracker, safe_serialize

__all__ = [
    # Core tracer
    "GSWTracer",
    # Models
    "OperationType",
    "GraphActivation",
    "TraversalResult",
    "LatencyBreakdown",
    # Decorators
    "trace_gsw_operation",
    "trace_graph_traversal",
    "trace_llm_generation",
    "score_retrieval_accuracy",
    # Span wrappers
    "SpanWrapper",
    "DummySpan",
    # Utilities
    "get_session_tracker",
    "safe_serialize",
    # Session tracking
    "EpisodicSessionTracker",
    "SessionState",
    # Scoring
    "RetrievalScorer",
    "AccuracyMetrics",
    "ScoreCategory",
    "ScoringWeights",
    "create_evaluation_dataset",
    "batch_evaluate",
]
