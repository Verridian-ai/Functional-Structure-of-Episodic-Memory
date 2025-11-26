"""
Span Wrapper Classes
====================

Wrapper classes for LangFuse spans with helper methods.
"""

import time
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .tracer_core import GSWTracer
    from .models import GraphActivation, TraversalResult


class SpanWrapper:
    """Wrapper around LangFuse span with additional helper methods."""

    def __init__(self, span: Any, start_time: float, tracer: "GSWTracer"):
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

    def record_graph_activation(self, activation: "GraphActivation"):
        """Record a graph activation within this span."""
        self._tracer.trace_graph_activation(activation, self)

    def record_traversal(self, result: "TraversalResult"):
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


class DummySpan:
    """Dummy span when tracing is disabled."""

    def set_output(self, output: Any): pass
    def set_metadata(self, metadata: Dict[str, Any]): pass
    def event(self, name: str, metadata: Optional[Dict[str, Any]] = None): pass
    def start_sub_timer(self, name: str): pass
    def stop_sub_timer(self, name: str) -> float: return 0.0
    def get_elapsed_ms(self) -> float: return 0.0
    def record_graph_activation(self, activation: "GraphActivation"): pass
    def record_traversal(self, result: "TraversalResult"): pass
    def score(self, name: str, value: float, comment: Optional[str] = None): pass


# Legacy aliases for backwards compatibility
_SpanWrapper = SpanWrapper
_DummySpan = DummySpan
