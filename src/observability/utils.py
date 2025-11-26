"""
Observability Utilities
=======================

Helper functions for GSW observability.
"""

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .session_memory import EpisodicSessionTracker


def get_session_tracker(session_id: str) -> "EpisodicSessionTracker":
    """
    Convenience function to get a session tracker.

    Usage:
        tracker = get_session_tracker("user_123_session_456")
        tracker.update_context(new_entities=[...])
    """
    from .tracer_core import GSWTracer
    tracer = GSWTracer()
    return tracer.get_session_tracker(session_id)


def safe_serialize(obj: Any, max_length: int = 5000) -> Any:
    """Safely serialize an object for LangFuse, handling common types."""
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple)):
        return [safe_serialize(item, max_length // len(obj) if obj else max_length) for item in obj[:100]]

    if isinstance(obj, dict):
        return {k: safe_serialize(v, max_length // len(obj) if obj else max_length) for k, v in list(obj.items())[:50]}

    if hasattr(obj, "__dict__"):
        return safe_serialize(obj.__dict__, max_length)

    if hasattr(obj, "to_dict"):
        return safe_serialize(obj.to_dict(), max_length)

    # Fallback to string representation
    s = str(obj)
    return s[:max_length] if len(s) > max_length else s


# Legacy alias for backwards compatibility
_safe_serialize = safe_serialize
