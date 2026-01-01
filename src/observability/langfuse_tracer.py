"""
LangFuse Tracer for GSW (Global Semantic Workspace)
====================================================

Brain-Inspired Legal AI Observability

This module provides comprehensive tracing for the episodic memory retrieval system,
including graph traversal tracking, accuracy scoring, session memory, and latency breakdown.

Usage:
    from src.observability import GSWTracer, trace_gsw_operation

    # Initialize once at startup
    tracer = GSWTracer()

    # Use decorators on your functions
    @trace_gsw_operation(operation_type="retrieval")
    async def my_retrieval_function(query: str):
        ...

    # Or use context managers for fine-grained control
    with tracer.trace_span("graph_traversal") as span:
        results = traverse_graph(query)
        span.set_output(results)

NOTE: This module has been refactored into smaller components:
- models.py: Data classes (OperationType, GraphActivation, etc.)
- tracer_core.py: Main GSWTracer class
- decorators.py: Tracing decorators
- span_wrapper.py: Span wrapper classes
- utils.py: Helper functions

This file re-exports everything for backwards compatibility.
"""

# Re-export all public APIs from the refactored modules
from .models import (
    GraphActivation,
    LatencyBreakdown,
    OperationType,
    TraversalResult,
)
from .tracer_core import (
    LANGFUSE_AVAILABLE,
    GSWTracer,
)

# Re-export Langfuse for test patching compatibility
try:
    from langfuse import Langfuse
except ImportError:
    Langfuse = None

from .decorators import (
    score_retrieval_accuracy,
    trace_graph_traversal,
    trace_gsw_operation,
    trace_llm_generation,
)

# Import session tracker for type checking and legacy imports
from .session_memory import EpisodicSessionTracker
from .span_wrapper import (
    DummySpan,
    SpanWrapper,
    _DummySpan,
    # Legacy aliases
    _SpanWrapper,
)
from .utils import (
    # Legacy alias
    _safe_serialize,
    get_session_tracker,
    safe_serialize,
)

__all__ = [
    # Core tracer
    "GSWTracer",
    "LANGFUSE_AVAILABLE",
    # Data models
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
    "_SpanWrapper",  # Legacy
    "_DummySpan",  # Legacy
    # Utilities
    "get_session_tracker",
    "safe_serialize",
    "_safe_serialize",  # Legacy
    # Session
    "EpisodicSessionTracker",
]
