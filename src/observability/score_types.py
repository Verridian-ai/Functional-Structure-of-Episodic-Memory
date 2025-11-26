"""
Scoring Types and Data Classes
==============================

Data classes for retrieval accuracy scoring.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime
from enum import Enum


class ScoreCategory(str, Enum):
    """Categories of accuracy scoring."""
    ENTITY_RELEVANCE = "entity_relevance"
    STRUCTURAL_ACCURACY = "structural_accuracy"
    TEMPORAL_COHERENCE = "temporal_coherence"
    LEGAL_PRECISION = "legal_precision"
    ANSWER_COMPLETENESS = "answer_completeness"
    CITATION_ACCURACY = "citation_accuracy"
    ROLE_BINDING = "role_binding"


@dataclass
class AccuracyMetrics:
    """
    Complete accuracy metrics for a retrieval operation.

    All scores are on 0.0-1.0 scale, where:
    - 0.95+ = Excellent (target)
    - 0.85-0.95 = Good
    - 0.70-0.85 = Acceptable
    - <0.70 = Needs improvement
    """
    # Core metrics
    entity_relevance: float = 0.0
    structural_accuracy: float = 0.0
    temporal_coherence: float = 0.0
    legal_precision: float = 0.0
    answer_completeness: float = 0.0

    # Detailed metrics
    citation_accuracy: float = 0.0
    role_binding_accuracy: float = 0.0

    # Composite
    composite_score: float = 0.0

    # Metadata
    query: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    evaluation_notes: List[str] = field(default_factory=list)

    # Counts for precision/recall calculation
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    true_negatives: int = 0

    @property
    def precision(self) -> float:
        """Retrieval precision: TP / (TP + FP)"""
        total = self.true_positives + self.false_positives
        return self.true_positives / total if total > 0 else 0.0

    @property
    def recall(self) -> float:
        """Retrieval recall: TP / (TP + FN)"""
        total = self.true_positives + self.false_negatives
        return self.true_positives / total if total > 0 else 0.0

    @property
    def f1_score(self) -> float:
        """F1 score: harmonic mean of precision and recall"""
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    def meets_target(self, target: float = 0.95) -> bool:
        """Check if composite score meets target threshold."""
        return self.composite_score >= target

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "entity_relevance": self.entity_relevance,
            "structural_accuracy": self.structural_accuracy,
            "temporal_coherence": self.temporal_coherence,
            "legal_precision": self.legal_precision,
            "answer_completeness": self.answer_completeness,
            "citation_accuracy": self.citation_accuracy,
            "role_binding_accuracy": self.role_binding_accuracy,
            "composite_score": self.composite_score,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "meets_target": self.meets_target(),
            "query": self.query,
            "evaluation_notes": self.evaluation_notes,
        }


@dataclass
class ScoringWeights:
    """Configurable weights for composite score calculation."""
    entity_relevance: float = 0.25
    structural_accuracy: float = 0.20
    temporal_coherence: float = 0.15
    legal_precision: float = 0.20
    answer_completeness: float = 0.20

    def validate(self) -> bool:
        """Ensure weights sum to 1.0."""
        total = (
            self.entity_relevance +
            self.structural_accuracy +
            self.temporal_coherence +
            self.legal_precision +
            self.answer_completeness
        )
        return abs(total - 1.0) < 0.001

    def to_dict(self) -> Dict[str, float]:
        return {
            "entity_relevance": self.entity_relevance,
            "structural_accuracy": self.structural_accuracy,
            "temporal_coherence": self.temporal_coherence,
            "legal_precision": self.legal_precision,
            "answer_completeness": self.answer_completeness,
        }
