"""
GSW Tracer Core
===============

Main tracer class for GSW observability with LangFuse integration.
"""

import os
import time
from typing import Any, Dict, List, Optional, Literal, TYPE_CHECKING
from contextlib import contextmanager, asynccontextmanager

from .models import OperationType, GraphActivation, TraversalResult, LatencyBreakdown
from .span_wrapper import SpanWrapper, DummySpan

# LangFuse imports - handle gracefully when not installed
try:
    from langfuse import Langfuse
    from langfuse.client import StatefulSpanClient, StatefulTraceClient
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    Langfuse = None
    StatefulSpanClient = Any
    StatefulTraceClient = Any
    print("[GSW Observability] LangFuse not installed. Run: pip install langfuse")

if TYPE_CHECKING:
    from .session_memory import EpisodicSessionTracker


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
            yield DummySpan()
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
        span_wrapper = SpanWrapper(span, start_time, self)

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
            yield DummySpan()
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
        span_wrapper = SpanWrapper(span, start_time, self)

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
        span: Optional[SpanWrapper] = None,
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
        span: Optional[SpanWrapper] = None,
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
                        "traversal_path": result.traversal_path[:20],
                    },
                    "activated_nodes": [
                        {
                            "id": a.entity_id,
                            "type": a.entity_type,
                            "name": a.entity_name,
                            "score": a.activation_score,
                            "depth": a.traversal_depth,
                        }
                        for a in result.activated_nodes[:50]
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

        if weights is None:
            weights = {k: 1.0 for k in scores.keys()}

        for name, score in scores.items():
            self.score_retrieval(name, score, trace_id=trace_id)

        total_weight = sum(weights.get(k, 1.0) for k in scores.keys())
        weighted_sum = sum(scores[k] * weights.get(k, 1.0) for k in scores.keys())
        avg_score = weighted_sum / total_weight if total_weight > 0 else 0.0

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
        span: Optional[SpanWrapper] = None,
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
            from .session_memory import EpisodicSessionTracker
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
