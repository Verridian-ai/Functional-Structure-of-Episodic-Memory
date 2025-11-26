"""
GSW Tracing Decorators
======================

Decorators for tracing GSW operations.
"""

import time
import asyncio
import functools
from typing import Any, Callable, TypeVar, Union

from .models import OperationType


# Type variables for generic decorators
F = TypeVar('F', bound=Callable[..., Any])
AsyncF = TypeVar('AsyncF', bound=Callable[..., Any])


def trace_gsw_operation(
    operation_type: Union[str, OperationType] = OperationType.GRAPH_TRAVERSAL,
    name: str = None,
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
        from .tracer_core import GSWTracer
        from .utils import safe_serialize

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
                        span.set_output(safe_serialize(result))
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
                        span.set_output(safe_serialize(result))
                    return result
                except Exception as e:
                    span.set_metadata({"error": str(e), "error_type": type(e).__name__})
                    raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator


def trace_graph_traversal(
    name: str = None,
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
    model: str = None,
    name: str = None,
) -> Callable[[F], F]:
    """
    Specialized decorator for LLM generation operations.

    Usage:
        @trace_llm_generation(model="gemini-2.0-flash")
        async def generate_response(prompt: str) -> str:
            ...
    """
    def decorator(func: F) -> F:
        from .tracer_core import GSWTracer

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
        from .tracer_core import GSWTracer

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
