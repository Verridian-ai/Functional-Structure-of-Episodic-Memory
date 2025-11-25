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
"""

import os
import time
import asyncio
import functools
from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
    Literal,
)
from dataclasses import dataclass, field
from contextlib import contextmanager, asynccontextmanager
from enum import Enum
import uuid
import json

# LangFuse imports - handle gracefully when not installed
try:
    from langfuse import Langfuse
    from langfuse.decorators import observe, langfuse_context
    from langfuse.client import StatefulSpanClient, StatefulTraceClient
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    # Create dummy types for type hints
    Langfuse = None
    StatefulSpanClient = Any
    StatefulTraceClient = Any
    observe = None
    langfuse_context = None
    print("[GSW Observability] LangFuse not installed. Run: pip install langfuse")


# Type variables for generic decorators
F = TypeVar('F', bound=Callable[..., Any])
AsyncF = TypeVar('AsyncF', bound=Callable[..., Any])


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


class GSWTracer:
    """
    Main tracer class for GSW observability.

    Integrates with LangFuse to provide:
    - Graph traversal tracing (node activations)
    - Accuracy scoring (0.0-1.0 scale)
    - Session memory tracking
    - Latency breakdown
    """

    _instance: Optional["GSWTracer"] = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern - one tracer instance per application."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
        enabled: bool = True,
        debug: bool = False,
    ):
        """
        Initialize the GSW tracer.

        Args:
            public_key: LangFuse public key (or set LANGFUSE_PUBLIC_KEY env var)
            secret_key: LangFuse secret key (or set LANGFUSE_SECRET_KEY env var)
            host: LangFuse host URL (default: https://cloud.langfuse.com)
            enabled: Whether tracing is enabled
            debug: Enable debug logging
        """
        if self._initialized:
            return

        self.enabled = enabled and LANGFUSE_AVAILABLE
        self.debug = debug

        if self.enabled:
            self.langfuse = Langfuse(
                public_key=public_key or os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=secret_key or os.getenv("LANGFUSE_SECRET_KEY"),
                host=host or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            )
        else:
            self.langfuse = None

        # Session tracking
        self._sessions: Dict[str, "EpisodicSessionTracker"] = {}
        self._current_trace: Optional[StatefulTraceClient] = None
        self._span_stack: List[StatefulSpanClient] = []

        # Latency tracking
        self._latency_timers: Dict[str, float] = {}

        self._initialized = True

        if self.debug:
            print(f"[GSW Tracer] Initialized. Enabled: {self.enabled}")

    # =========================================================================
    # TRACE MANAGEMENT
    # =========================================================================

    def start_trace(
        self,
        name: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[StatefulTraceClient]:
        """
        Start a new trace for a GSW operation.

        Args:
            name: Name of the trace (e.g., "legal_query_processing")
            session_id: Session ID for episodic memory tracking
            user_id: User identifier
            metadata: Additional metadata to attach
            tags: Tags for filtering in LangFuse UI

        Returns:
            LangFuse trace client or None if disabled
        """
        if not self.enabled:
            return None

        trace = self.langfuse.trace(
            name=name,
            session_id=session_id,
            user_id=user_id,
            metadata={
                "system": "gsw_legal_ai",
                "version": "7.0",
                **(metadata or {}),
            },
            tags=tags or ["gsw", "legal-ai", "episodic-memory"],
        )

        self._current_trace = trace

        if self.debug:
            print(f"[GSW Tracer] Started trace: {name} (session: {session_id})")

        return trace

    def end_trace(
        self,
        output: Optional[Any] = None,
        level: Literal["DEBUG", "DEFAULT", "WARNING", "ERROR"] = "DEFAULT",
    ):
        """End the current trace."""
        if self._current_trace:
            if output:
                self._current_trace.update(output=output, level=level)
            self._current_trace = None

    @contextmanager
    def trace_span(
        self,
        name: str,
        operation_type: Optional[OperationType] = None,
        input_data: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for tracing a span within a trace.

        Usage:
            with tracer.trace_span("graph_traversal", OperationType.GRAPH_TRAVERSAL) as span:
                results = do_traversal()
                span.set_output(results)
        """
        if not self.enabled or not self._current_trace:
            yield _DummySpan()
            return

        start_time = time.perf_counter()

        span = self._current_trace.span(
            name=name,
            input=input_data,
            metadata={
                "operation_type": operation_type.value if operation_type else None,
                **(metadata or {}),
            },
        )

        self._span_stack.append(span)

        # Create wrapper with additional methods
        span_wrapper = _SpanWrapper(span, start_time, self)

        try:
            yield span_wrapper
        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000
            span.update(
                metadata={
                    **(span.metadata or {}),
                    "latency_ms": latency_ms,
                }
            )
            span.end()
            self._span_stack.pop()

            if self.debug:
                print(f"[GSW Tracer] Span '{name}' completed in {latency_ms:.2f}ms")

    @asynccontextmanager
    async def async_trace_span(
        self,
        name: str,
        operation_type: Optional[OperationType] = None,
        input_data: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Async version of trace_span."""
        if not self.enabled or not self._current_trace:
            yield _DummySpan()
            return

        start_time = time.perf_counter()

        span = self._current_trace.span(
            name=name,
            input=input_data,
            metadata={
                "operation_type": operation_type.value if operation_type else None,
                **(metadata or {}),
            },
        )

        self._span_stack.append(span)
        span_wrapper = _SpanWrapper(span, start_time, self)

        try:
            yield span_wrapper
        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000
            span.update(
                metadata={
                    **(span.metadata or {}),
                    "latency_ms": latency_ms,
                }
            )
            span.end()
            self._span_stack.pop()

    # =========================================================================
    # GRAPH TRAVERSAL TRACING
    # =========================================================================

    def trace_graph_activation(
        self,
        activation: GraphActivation,
        span: Optional["_SpanWrapper"] = None,
    ):
        """
        Record a single graph node activation.

        Args:
            activation: The graph activation to record
            span: Optional span to attach to (uses current if not provided)
        """
        if not self.enabled:
            return

        target_span = span._span if span else (self._span_stack[-1] if self._span_stack else None)

        if target_span:
            # Record as an event within the span
            target_span.event(
                name="graph_node_activated",
                metadata={
                    "entity_id": activation.entity_id,
                    "entity_type": activation.entity_type,
                    "entity_name": activation.entity_name,
                    "activation_score": activation.activation_score,
                    "traversal_depth": activation.traversal_depth,
                    "connected_count": len(activation.connected_entities),
                    "metadata": activation.metadata,
                },
            )

    def trace_full_traversal(
        self,
        result: TraversalResult,
        span: Optional["_SpanWrapper"] = None,
    ):
        """
        Record a complete graph traversal result.

        Args:
            result: The complete traversal result
            span: Optional span to attach to
        """
        if not self.enabled:
            return

        target_span = span._span if span else (self._span_stack[-1] if self._span_stack else None)

        if target_span:
            target_span.update(
                output={
                    "traversal_summary": {
                        "query": result.query,
                        "total_nodes_scanned": result.total_nodes_scanned,
                        "nodes_activated": result.nodes_activated,
                        "max_depth_reached": result.max_depth_reached,
                        "latency_ms": result.latency_ms,
                        "traversal_path": result.traversal_path[:20],  # Limit for UI
                    },
                    "activated_nodes": [
                        {
                            "id": a.entity_id,
                            "type": a.entity_type,
                            "name": a.entity_name,
                            "score": a.activation_score,
                            "depth": a.traversal_depth,
                        }
                        for a in result.activated_nodes[:50]  # Top 50 for UI
                    ],
                    "relevance_scores": result.relevance_scores,
                },
                metadata={
                    "traversal_efficiency": result.nodes_activated / max(result.total_nodes_scanned, 1),
                    "avg_activation_score": sum(a.activation_score for a in result.activated_nodes) / max(len(result.activated_nodes), 1),
                },
            )

    # =========================================================================
    # ACCURACY SCORING
    # =========================================================================

    def score_retrieval(
        self,
        name: str,
        score: float,
        comment: Optional[str] = None,
        trace_id: Optional[str] = None,
        observation_id: Optional[str] = None,
        config_id: Optional[str] = None,
    ):
        """
        Score a retrieval operation (0.0 to 1.0).

        Args:
            name: Name of the score (e.g., "retrieval_relevance", "answer_accuracy")
            score: Score value between 0.0 and 1.0
            comment: Optional comment explaining the score
            trace_id: Optional trace ID (uses current if not provided)
            observation_id: Optional observation ID to attach score to
            config_id: Optional config ID for A/B testing
        """
        if not self.enabled:
            return

        # Clamp score to valid range
        score = max(0.0, min(1.0, score))

        target_trace_id = trace_id or (self._current_trace.id if self._current_trace else None)

        if not target_trace_id:
            if self.debug:
                print(f"[GSW Tracer] Cannot score - no active trace")
            return

        self.langfuse.score(
            name=name,
            value=score,
            comment=comment,
            trace_id=target_trace_id,
            observation_id=observation_id,
            config_id=config_id,
        )

        if self.debug:
            status = "PASS" if score >= 0.95 else "WARN" if score >= 0.80 else "FAIL"
            print(f"[GSW Tracer] Score '{name}': {score:.3f} [{status}]")

    def score_with_breakdown(
        self,
        scores: Dict[str, float],
        weights: Optional[Dict[str, float]] = None,
        trace_id: Optional[str] = None,
    ) -> float:
        """
        Score multiple aspects and compute weighted average.

        Args:
            scores: Dict of score_name -> score_value
            weights: Optional weights for each score (default: equal weights)
            trace_id: Optional trace ID

        Returns:
            Weighted average score
        """
        if not scores:
            return 0.0

        # Default to equal weights
        if weights is None:
            weights = {k: 1.0 for k in scores.keys()}

        # Record individual scores
        for name, score in scores.items():
            self.score_retrieval(name, score, trace_id=trace_id)

        # Compute weighted average
        total_weight = sum(weights.get(k, 1.0) for k in scores.keys())
        weighted_sum = sum(scores[k] * weights.get(k, 1.0) for k in scores.keys())
        avg_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Record composite score
        self.score_retrieval(
            "composite_retrieval_score",
            avg_score,
            comment=f"Weighted average of {len(scores)} metrics",
            trace_id=trace_id,
        )

        return avg_score

    # =========================================================================
    # LATENCY TRACKING
    # =========================================================================

    def start_timer(self, name: str):
        """Start a named timer for latency tracking."""
        self._latency_timers[name] = time.perf_counter()

    def stop_timer(self, name: str) -> float:
        """
        Stop a named timer and return elapsed milliseconds.

        Returns:
            Elapsed time in milliseconds
        """
        if name not in self._latency_timers:
            return 0.0

        elapsed_ms = (time.perf_counter() - self._latency_timers[name]) * 1000
        del self._latency_timers[name]
        return elapsed_ms

    def record_latency_breakdown(
        self,
        breakdown: LatencyBreakdown,
        span: Optional["_SpanWrapper"] = None,
    ):
        """
        Record detailed latency breakdown for an operation.

        Args:
            breakdown: The latency breakdown to record
            span: Optional span to attach to
        """
        if not self.enabled:
            return

        target_span = span._span if span else (self._span_stack[-1] if self._span_stack else None)

        if target_span:
            target_span.update(
                metadata={
                    "latency_breakdown": breakdown.to_dict(),
                    "latency_percentages": breakdown.get_breakdown_percentages(),
                },
            )

        # Also record as individual metrics on the trace
        if self._current_trace:
            for component, ms in breakdown.to_dict().items():
                if ms > 0:
                    self._current_trace.event(
                        name=f"latency_{component}",
                        metadata={"ms": ms},
                    )

    # =========================================================================
    # SESSION MEMORY TRACKING
    # =========================================================================

    def get_session_tracker(self, session_id: str) -> "EpisodicSessionTracker":
        """
        Get or create a session tracker for episodic memory tracking.

        Args:
            session_id: Unique session identifier

        Returns:
            EpisodicSessionTracker instance
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = EpisodicSessionTracker(
                session_id=session_id,
                tracer=self,
            )
        return self._sessions[session_id]

    def clear_session(self, session_id: str):
        """Clear a session tracker."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    # =========================================================================
    # LLM GENERATION TRACING
    # =========================================================================

    def trace_llm_call(
        self,
        model: str,
        input_messages: List[Dict[str, str]],
        output: str,
        usage: Optional[Dict[str, int]] = None,
        latency_ms: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Trace an LLM generation call.

        Args:
            model: Model identifier (e.g., "gemini-2.0-flash")
            input_messages: Input messages to the LLM
            output: Generated output
            usage: Token usage dict (prompt_tokens, completion_tokens, total_tokens)
            latency_ms: Latency in milliseconds
            metadata: Additional metadata
        """
        if not self.enabled or not self._current_trace:
            return

        self._current_trace.generation(
            name="llm_generation",
            model=model,
            input=input_messages,
            output=output,
            usage=usage,
            metadata={
                "latency_ms": latency_ms,
                "operation": "legal_ai_generation",
                **(metadata or {}),
            },
        )

    # =========================================================================
    # FLUSH & CLEANUP
    # =========================================================================

    def flush(self):
        """Flush all pending traces to LangFuse."""
        if self.enabled and self.langfuse:
            self.langfuse.flush()

    def shutdown(self):
        """Shutdown the tracer and flush all pending data."""
        if self.enabled and self.langfuse:
            self.langfuse.shutdown()


class _SpanWrapper:
    """Wrapper around LangFuse span with additional helper methods."""

    def __init__(self, span: StatefulSpanClient, start_time: float, tracer: GSWTracer):
        self._span = span
        self._start_time = start_time
        self._tracer = tracer
        self._sub_timers: Dict[str, float] = {}

    def set_output(self, output: Any):
        """Set the output of the span."""
        self._span.update(output=output)

    def set_metadata(self, metadata: Dict[str, Any]):
        """Add metadata to the span."""
        self._span.update(metadata=metadata)

    def event(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        """Record an event within the span."""
        self._span.event(name=name, metadata=metadata)

    def start_sub_timer(self, name: str):
        """Start a sub-timer within this span."""
        self._sub_timers[name] = time.perf_counter()

    def stop_sub_timer(self, name: str) -> float:
        """Stop a sub-timer and return elapsed ms."""
        if name not in self._sub_timers:
            return 0.0
        elapsed = (time.perf_counter() - self._sub_timers[name]) * 1000
        del self._sub_timers[name]
        return elapsed

    def get_elapsed_ms(self) -> float:
        """Get elapsed time since span start."""
        return (time.perf_counter() - self._start_time) * 1000

    def record_graph_activation(self, activation: GraphActivation):
        """Record a graph activation within this span."""
        self._tracer.trace_graph_activation(activation, self)

    def record_traversal(self, result: TraversalResult):
        """Record a traversal result within this span."""
        self._tracer.trace_full_traversal(result, self)

    def score(self, name: str, value: float, comment: Optional[str] = None):
        """Score this span's operation."""
        self._tracer.score_retrieval(
            name=name,
            score=value,
            comment=comment,
            observation_id=self._span.id,
        )


class _DummySpan:
    """Dummy span when tracing is disabled."""

    def set_output(self, output: Any): pass
    def set_metadata(self, metadata: Dict[str, Any]): pass
    def event(self, name: str, metadata: Optional[Dict[str, Any]] = None): pass
    def start_sub_timer(self, name: str): pass
    def stop_sub_timer(self, name: str) -> float: return 0.0
    def get_elapsed_ms(self) -> float: return 0.0
    def record_graph_activation(self, activation: GraphActivation): pass
    def record_traversal(self, result: TraversalResult): pass
    def score(self, name: str, value: float, comment: Optional[str] = None): pass


# =============================================================================
# DECORATORS
# =============================================================================

def trace_gsw_operation(
    operation_type: Union[str, OperationType] = OperationType.GRAPH_TRAVERSAL,
    name: Optional[str] = None,
    capture_input: bool = True,
    capture_output: bool = True,
) -> Callable[[F], F]:
    """
    Decorator to trace a GSW operation.

    Usage:
        @trace_gsw_operation(operation_type="retrieval")
        def my_function(query: str) -> Results:
            ...

        @trace_gsw_operation(OperationType.LLM_GENERATION, name="extract_entities")
        async def extract(text: str) -> List[Entity]:
            ...
    """
    def decorator(func: F) -> F:
        op_type = OperationType(operation_type) if isinstance(operation_type, str) else operation_type
        span_name = name or func.__name__

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracer = GSWTracer()

            if not tracer.enabled:
                return func(*args, **kwargs)

            with tracer.trace_span(
                name=span_name,
                operation_type=op_type,
                input_data={"args": str(args)[:500], "kwargs": {k: str(v)[:200] for k, v in kwargs.items()}} if capture_input else None,
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    if capture_output:
                        span.set_output(_safe_serialize(result))
                    return result
                except Exception as e:
                    span.set_metadata({"error": str(e), "error_type": type(e).__name__})
                    raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracer = GSWTracer()

            if not tracer.enabled:
                return await func(*args, **kwargs)

            async with tracer.async_trace_span(
                name=span_name,
                operation_type=op_type,
                input_data={"args": str(args)[:500], "kwargs": {k: str(v)[:200] for k, v in kwargs.items()}} if capture_input else None,
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    if capture_output:
                        span.set_output(_safe_serialize(result))
                    return result
                except Exception as e:
                    span.set_metadata({"error": str(e), "error_type": type(e).__name__})
                    raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def trace_graph_traversal(
    name: Optional[str] = None,
    track_activations: bool = True,
) -> Callable[[F], F]:
    """
    Specialized decorator for graph traversal operations.

    Automatically extracts graph activations if the function returns
    a TraversalResult or similar structure.

    Usage:
        @trace_graph_traversal()
        def traverse_knowledge_graph(query: str) -> TraversalResult:
            ...
    """
    return trace_gsw_operation(
        operation_type=OperationType.GRAPH_TRAVERSAL,
        name=name,
    )


def trace_llm_generation(
    model: Optional[str] = None,
    name: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Specialized decorator for LLM generation operations.

    Usage:
        @trace_llm_generation(model="gemini-2.0-flash")
        async def generate_response(prompt: str) -> str:
            ...
    """
    def decorator(func: F) -> F:
        span_name = name or func.__name__

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracer = GSWTracer()
            start_time = time.perf_counter()

            result = await func(*args, **kwargs)

            latency_ms = (time.perf_counter() - start_time) * 1000

            if tracer.enabled:
                tracer.trace_llm_call(
                    model=model or "unknown",
                    input_messages=[{"role": "user", "content": str(args)[:1000]}],
                    output=str(result)[:2000] if result else "",
                    latency_ms=latency_ms,
                    metadata={"function": span_name},
                )

            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracer = GSWTracer()
            start_time = time.perf_counter()

            result = func(*args, **kwargs)

            latency_ms = (time.perf_counter() - start_time) * 1000

            if tracer.enabled:
                tracer.trace_llm_call(
                    model=model or "unknown",
                    input_messages=[{"role": "user", "content": str(args)[:1000]}],
                    output=str(result)[:2000] if result else "",
                    latency_ms=latency_ms,
                    metadata={"function": span_name},
                )

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def score_retrieval_accuracy(
    score_name: str = "retrieval_accuracy",
    target_score: float = 0.95,
) -> Callable[[F], F]:
    """
    Decorator that expects the function to return a tuple of (result, score).

    Usage:
        @score_retrieval_accuracy(target_score=0.95)
        def evaluate_retrieval(query: str, expected: List[str]) -> Tuple[List[str], float]:
            results = retrieve(query)
            score = compute_recall(results, expected)
            return results, score
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = GSWTracer()

            result = func(*args, **kwargs)

            if isinstance(result, tuple) and len(result) == 2:
                actual_result, score = result

                if tracer.enabled:
                    status = "TARGET_MET" if score >= target_score else "BELOW_TARGET"
                    tracer.score_retrieval(
                        name=score_name,
                        score=score,
                        comment=f"{status}: {score:.3f} (target: {target_score})",
                    )

                return actual_result

            return result

        return wrapper  # type: ignore

    return decorator


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_session_tracker(session_id: str) -> "EpisodicSessionTracker":
    """
    Convenience function to get a session tracker.

    Usage:
        tracker = get_session_tracker("user_123_session_456")
        tracker.update_context(new_entities=[...])
    """
    tracer = GSWTracer()
    return tracer.get_session_tracker(session_id)


def _safe_serialize(obj: Any, max_length: int = 5000) -> Any:
    """Safely serialize an object for LangFuse, handling common types."""
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple)):
        return [_safe_serialize(item, max_length // len(obj) if obj else max_length) for item in obj[:100]]

    if isinstance(obj, dict):
        return {k: _safe_serialize(v, max_length // len(obj) if obj else max_length) for k, v in list(obj.items())[:50]}

    if hasattr(obj, "__dict__"):
        return _safe_serialize(obj.__dict__, max_length)

    if hasattr(obj, "to_dict"):
        return _safe_serialize(obj.to_dict(), max_length)

    # Fallback to string representation
    s = str(obj)
    return s[:max_length] if len(s) > max_length else s


# Import session tracker (defined in separate file)
from .session_memory import EpisodicSessionTracker
