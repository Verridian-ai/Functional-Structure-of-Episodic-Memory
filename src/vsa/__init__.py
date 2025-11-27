"""
VSA (Vector Symbolic Architecture) Module
==========================================

This module provides the Vector Symbolic Architecture implementation for
the Verridian AI legal reasoning system, including:

- Legal VSA engine with hyperdimensional computing
- Span-level issue detection and localization
- Ontology-based symbolic reasoning
- Anti-hallucination verification

Key Components:
    - LegalVSA: Main VSA engine for legal reasoning
    - SpanAlignedVSA: Span-level issue detection
    - SpanIssue: Dataclass for representing detected issues
"""

from .legal_vsa import LegalVSA, get_vsa_service
from .span_detector import SpanIssue, SpanAlignedVSA

__all__ = [
    # Main VSA classes
    "LegalVSA",
    "get_vsa_service",

    # Span detection classes
    "SpanIssue",
    "SpanAlignedVSA",
]
