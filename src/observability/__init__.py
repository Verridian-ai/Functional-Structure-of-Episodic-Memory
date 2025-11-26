# GSW Observability Module
# LangFuse integration for Brain-Inspired Legal AI

# Core tracer and models
from .tracer_core import GSWTracer
from .models import (
    OperationType,
    GraphActivation,
    TraversalResult,
    LatencyBreakdown,
)

# Decorators
from .decorators import (
    trace_gsw_operation,
    trace_graph_traversal,
    trace_llm_generation,
    score_retrieval_accuracy,
)

# Span wrappers
from .span_wrapper import SpanWrapper, DummySpan

# Utilities
from .utils import get_session_tracker, safe_serialize

# Session memory
from .session_memory import (
    EpisodicSessionTracker,
    SessionState,
)

# Scoring
from .scoring import (
    RetrievalScorer,
    AccuracyMetrics,
    ScoreCategory,
    ScoringWeights,
    create_evaluation_dataset,
    batch_evaluate,
)

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
