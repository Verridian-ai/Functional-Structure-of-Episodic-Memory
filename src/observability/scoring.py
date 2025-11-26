"""
Retrieval Accuracy Scoring for GSW
===================================

Custom scoring functions for evaluating retrieval quality in the
brain-inspired legal AI system. Target accuracy: >0.95

Scoring Dimensions:
1. Entity Relevance - Are the right actors/states retrieved?
2. Structural Accuracy - Does the graph structure match the query?
3. Temporal Coherence - Are time-bound entities correctly linked?
4. Legal Precision - Are statutory references accurate?
5. Answer Completeness - Are all aspects of the query addressed?

NOTE: This module has been refactored into smaller components:
- score_types.py: Data classes (ScoreCategory, AccuracyMetrics, ScoringWeights)
- retrieval_scorer.py: Main RetrievalScorer class
- evaluation.py: Batch evaluation utilities

This file re-exports everything for backwards compatibility.
"""

# Re-export all public APIs from refactored modules
from .score_types import (
    ScoreCategory,
    AccuracyMetrics,
    ScoringWeights,
)

from .retrieval_scorer import (
    RetrievalScorer,
)

from .evaluation import (
    create_evaluation_dataset,
    batch_evaluate,
)

__all__ = [
    # Types
    "ScoreCategory",
    "AccuracyMetrics",
    "ScoringWeights",
    # Main scorer
    "RetrievalScorer",
    # Evaluation utilities
    "create_evaluation_dataset",
    "batch_evaluate",
]
