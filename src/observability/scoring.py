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
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime
from enum import Enum
import re


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


class RetrievalScorer:
    """
    Comprehensive scorer for GSW retrieval operations.

    Usage:
        scorer = RetrievalScorer()

        # Score a retrieval result
        metrics = scorer.score_retrieval(
            query="What are my property rights after separation?",
            retrieved_entities=retrieved,
            expected_entities=expected,
            response_text=response,
        )

        # Check if target met
        if metrics.meets_target(0.95):
            print("Retrieval quality meets target!")

        # Manual scoring
        score = scorer.score_entity_relevance(retrieved, expected)
    """

    def __init__(
        self,
        weights: Optional[ScoringWeights] = None,
        target_score: float = 0.95,
    ):
        """
        Initialize the scorer.

        Args:
            weights: Custom weights for composite score
            target_score: Target composite score (default 0.95)
        """
        self.weights = weights or ScoringWeights()
        self.target_score = target_score

        # Validate weights
        if not self.weights.validate():
            raise ValueError("Scoring weights must sum to 1.0")

        # Legal patterns for citation checking
        self._section_pattern = re.compile(
            r"(?:section|s|sec\.?)\s*(\d+[A-Z]*(?:\(\d+\))?(?:\([a-z]\))?)",
            re.IGNORECASE
        )
        self._case_pattern = re.compile(
            r"\[(\d{4})\]\s*(FamCA|FamCAFC|HCA|FCA|FCCA|FCWA|FLC)\s*(\d+)",
            re.IGNORECASE
        )

    # =========================================================================
    # COMPREHENSIVE SCORING
    # =========================================================================

    def score_retrieval(
        self,
        query: str,
        retrieved_entities: List[Dict[str, Any]],
        expected_entities: Optional[List[Dict[str, Any]]] = None,
        response_text: Optional[str] = None,
        ground_truth_response: Optional[str] = None,
        workspace_state: Optional[Any] = None,
    ) -> AccuracyMetrics:
        """
        Perform comprehensive scoring of a retrieval operation.

        Args:
            query: The user's query
            retrieved_entities: Entities retrieved from the knowledge graph
            expected_entities: Ground truth entities (for supervised evaluation)
            response_text: Generated response text
            ground_truth_response: Expected response (for supervised evaluation)
            workspace_state: Current GlobalWorkspace state

        Returns:
            AccuracyMetrics with all scores
        """
        metrics = AccuracyMetrics(query=query)

        # Entity Relevance
        if expected_entities:
            metrics.entity_relevance = self.score_entity_relevance(
                retrieved_entities, expected_entities
            )
            # Update TP/FP/FN counts
            self._count_retrieval_stats(metrics, retrieved_entities, expected_entities)
        else:
            # Use heuristic scoring when no ground truth
            metrics.entity_relevance = self.score_entity_relevance_heuristic(
                query, retrieved_entities
            )

        # Structural Accuracy
        metrics.structural_accuracy = self.score_structural_accuracy(
            query, retrieved_entities, workspace_state
        )

        # Temporal Coherence
        metrics.temporal_coherence = self.score_temporal_coherence(
            retrieved_entities
        )

        # Legal Precision (requires response text)
        if response_text:
            metrics.legal_precision = self.score_legal_precision(response_text)
            metrics.citation_accuracy = self.score_citation_accuracy(response_text)

        # Answer Completeness
        if response_text:
            metrics.answer_completeness = self.score_answer_completeness(
                query, response_text, ground_truth_response
            )

        # Role Binding Accuracy
        metrics.role_binding_accuracy = self.score_role_binding(retrieved_entities)

        # Compute composite score
        metrics.composite_score = self._compute_composite_score(metrics)

        return metrics

    def score_with_llm_judge(
        self,
        query: str,
        response: str,
        retrieved_context: str,
        judge_fn: Callable[[str, str, str], float],
    ) -> float:
        """
        Use an LLM as a judge for scoring.

        Args:
            query: User query
            response: Generated response
            retrieved_context: Context that was retrieved
            judge_fn: Function that takes (query, response, context) and returns 0.0-1.0

        Returns:
            LLM judge score
        """
        return judge_fn(query, response, retrieved_context)

    # =========================================================================
    # INDIVIDUAL SCORING FUNCTIONS
    # =========================================================================

    def score_entity_relevance(
        self,
        retrieved: List[Dict[str, Any]],
        expected: List[Dict[str, Any]],
    ) -> float:
        """
        Score entity relevance against ground truth.

        Uses Jaccard similarity between retrieved and expected entity sets.
        """
        if not expected:
            return 1.0 if not retrieved else 0.5  # No ground truth

        retrieved_ids = {self._get_entity_id(e) for e in retrieved}
        expected_ids = {self._get_entity_id(e) for e in expected}

        if not retrieved_ids and not expected_ids:
            return 1.0

        intersection = len(retrieved_ids & expected_ids)
        union = len(retrieved_ids | expected_ids)

        return intersection / union if union > 0 else 0.0

    def score_entity_relevance_heuristic(
        self,
        query: str,
        retrieved: List[Dict[str, Any]],
    ) -> float:
        """
        Heuristic scoring when no ground truth is available.

        Scores based on:
        - Entity type diversity (actors, states, verb_phrases)
        - Query keyword overlap
        - Entity confidence scores
        """
        if not retrieved:
            return 0.0

        scores = []

        # 1. Type diversity (good retrieval has multiple types)
        types = {e.get("type", e.get("entity_type", "unknown")) for e in retrieved}
        type_score = min(len(types) / 3, 1.0)  # Max score at 3+ types
        scores.append(type_score)

        # 2. Query keyword overlap
        query_words = set(query.lower().split())
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "my", "our", "what", "how", "when", "why"}
        query_words -= stop_words

        entity_words = set()
        for e in retrieved:
            name = e.get("name", e.get("entity_name", ""))
            if name:
                entity_words.update(name.lower().split())

        if query_words:
            overlap = len(query_words & entity_words) / len(query_words)
            scores.append(overlap)

        # 3. Average confidence
        confidences = [e.get("confidence", e.get("relevance", 1.0)) for e in retrieved]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        scores.append(avg_confidence)

        return sum(scores) / len(scores) if scores else 0.0

    def score_structural_accuracy(
        self,
        query: str,
        retrieved: List[Dict[str, Any]],
        workspace: Optional[Any] = None,
    ) -> float:
        """
        Score how well the graph structure matches the query.

        Evaluates:
        - Connected entity chains (actors linked by verb_phrases)
        - Spatio-temporal coherence
        - Role consistency
        """
        if not retrieved:
            return 0.0

        scores = []

        # 1. Entity connectivity (are retrieved entities linked?)
        entity_ids = {self._get_entity_id(e) for e in retrieved}
        linked_count = 0

        for entity in retrieved:
            connected = entity.get("connected_entities", entity.get("linked_entity_ids", []))
            if any(c in entity_ids for c in connected):
                linked_count += 1

        connectivity_score = linked_count / len(retrieved) if retrieved else 0.0
        scores.append(connectivity_score)

        # 2. Role balance (for legal queries, expect both parties)
        roles = [e.get("role", e.get("roles", [])) for e in retrieved]
        flat_roles = []
        for r in roles:
            if isinstance(r, list):
                flat_roles.extend(r)
            elif r:
                flat_roles.append(r)

        role_set = set(flat_roles)
        legal_roles = {"applicant", "respondent", "child", "judge", "witness"}
        role_coverage = len(role_set & legal_roles) / min(len(legal_roles), 3)
        scores.append(min(role_coverage, 1.0))

        # 3. Check for both parties in property/custody queries
        query_lower = query.lower()
        if any(term in query_lower for term in ["property", "custody", "parenting", "division"]):
            has_applicant = any("applicant" in str(r).lower() for r in flat_roles)
            has_respondent = any("respondent" in str(r).lower() for r in flat_roles)
            party_score = 1.0 if (has_applicant and has_respondent) else 0.5 if (has_applicant or has_respondent) else 0.0
            scores.append(party_score)

        return sum(scores) / len(scores) if scores else 0.0

    def score_temporal_coherence(
        self,
        retrieved: List[Dict[str, Any]],
    ) -> float:
        """
        Score temporal coherence of retrieved entities.

        Checks:
        - Date consistency (no future dates, logical ordering)
        - Temporal links are valid
        - State transitions are chronological
        """
        if not retrieved:
            return 1.0  # No entities = no temporal issues

        scores = []

        # 1. Check for valid dates
        valid_dates = 0
        total_dates = 0

        for entity in retrieved:
            for date_field in ["start_date", "end_date", "date", "timestamp"]:
                date_val = entity.get(date_field)
                if date_val:
                    total_dates += 1
                    if self._is_valid_legal_date(date_val):
                        valid_dates += 1

        if total_dates > 0:
            scores.append(valid_dates / total_dates)

        # 2. Check temporal ordering of states
        states = [e for e in retrieved if e.get("type") == "state" or "state" in e.get("entity_type", "")]

        if len(states) >= 2:
            ordered_states = self._check_state_ordering(states)
            scores.append(1.0 if ordered_states else 0.5)

        # 3. Check for temporal links
        temp_links = [e for e in retrieved if e.get("type") == "spatio_temporal_link"]
        if temp_links:
            valid_links = sum(1 for l in temp_links if l.get("tag_value"))
            scores.append(valid_links / len(temp_links))

        return sum(scores) / len(scores) if scores else 1.0

    def score_legal_precision(
        self,
        response_text: str,
    ) -> float:
        """
        Score legal precision of the response.

        Checks:
        - Contains statutory citations
        - Citations are properly formatted
        - No contradictory legal statements
        """
        if not response_text:
            return 0.0

        scores = []

        # 1. Has statutory citations
        section_matches = self._section_pattern.findall(response_text)
        has_sections = len(section_matches) > 0
        scores.append(1.0 if has_sections else 0.3)

        # 2. Has case citations
        case_matches = self._case_pattern.findall(response_text)
        has_cases = len(case_matches) > 0
        scores.append(1.0 if has_cases else 0.5)

        # 3. Mentions Family Law Act
        mentions_fla = "family law act" in response_text.lower() or "fla" in response_text.lower()
        scores.append(1.0 if mentions_fla else 0.6)

        # 4. No obvious legal errors (basic check)
        error_phrases = [
            "you are guilty",  # Family law doesn't have guilt
            "criminal charge",  # Family law is civil
            "beyond reasonable doubt",  # Wrong standard
        ]
        has_errors = any(phrase in response_text.lower() for phrase in error_phrases)
        scores.append(0.0 if has_errors else 1.0)

        return sum(scores) / len(scores)

    def score_citation_accuracy(
        self,
        response_text: str,
        valid_sections: Optional[Set[str]] = None,
    ) -> float:
        """
        Score accuracy of statutory citations.

        Args:
            response_text: Response to check
            valid_sections: Optional set of valid section numbers
        """
        section_matches = self._section_pattern.findall(response_text)

        if not section_matches:
            return 0.5  # No citations to validate

        # Common valid Family Law Act sections
        common_sections = {
            "60B", "60C", "60CC", "60CA", "60D",
            "61DA", "64B", "65DAA", "65DAC",
            "68B", "68C",
            "74", "75", "79", "79A",
            "90", "90A", "90B", "90C", "90SM",
        }

        valid_set = valid_sections or common_sections

        valid_count = 0
        for section in section_matches:
            # Normalize section number
            section_num = re.sub(r'[^\dA-Za-z]', '', section).upper()
            if any(section_num.startswith(v) for v in valid_set):
                valid_count += 1

        return valid_count / len(section_matches) if section_matches else 0.5

    def score_answer_completeness(
        self,
        query: str,
        response: str,
        ground_truth: Optional[str] = None,
    ) -> float:
        """
        Score how completely the response answers the query.
        """
        if not response:
            return 0.0

        scores = []

        # 1. Response length adequacy
        word_count = len(response.split())
        length_score = min(word_count / 100, 1.0)  # Target ~100+ words
        scores.append(length_score)

        # 2. Query term coverage
        query_terms = set(query.lower().split()) - {"the", "a", "an", "is", "my", "what", "how", "when", "why", "are"}
        response_lower = response.lower()
        covered = sum(1 for term in query_terms if term in response_lower)
        term_coverage = covered / len(query_terms) if query_terms else 1.0
        scores.append(term_coverage)

        # 3. Has structure (sections, bullet points, etc.)
        has_structure = any([
            "##" in response,
            "1." in response or "1)" in response,
            "- " in response or "* " in response,
            ":" in response,
        ])
        scores.append(1.0 if has_structure else 0.7)

        # 4. Ground truth comparison (if available)
        if ground_truth:
            gt_terms = set(ground_truth.lower().split())
            overlap = len(gt_terms & set(response_lower.split())) / len(gt_terms) if gt_terms else 0.0
            scores.append(overlap)

        return sum(scores) / len(scores)

    def score_role_binding(
        self,
        retrieved: List[Dict[str, Any]],
    ) -> float:
        """
        Score accuracy of role-entity bindings.

        Ensures entities are correctly bound to roles (applicant, respondent, etc.)
        without confusion or overlap.
        """
        if not retrieved:
            return 1.0

        # Group entities by role
        role_entities: Dict[str, List[str]] = {}

        for entity in retrieved:
            roles = entity.get("roles", entity.get("role", []))
            if isinstance(roles, str):
                roles = [roles]

            entity_id = self._get_entity_id(entity)

            for role in roles:
                if role:
                    if role not in role_entities:
                        role_entities[role] = []
                    role_entities[role].append(entity_id)

        if not role_entities:
            return 0.5  # No roles to check

        scores = []

        # 1. Check for role conflicts (same entity as both applicant and respondent)
        applicants = set(role_entities.get("applicant", []))
        respondents = set(role_entities.get("respondent", []))

        if applicants and respondents:
            conflict = applicants & respondents
            no_conflict = len(conflict) == 0
            scores.append(1.0 if no_conflict else 0.0)

        # 2. Check role uniqueness (one primary party per role)
        for role, entities in role_entities.items():
            if role in ["applicant", "respondent"]:
                # These should typically have one primary entity
                uniqueness = 1.0 if len(entities) <= 2 else 0.5
                scores.append(uniqueness)

        return sum(scores) / len(scores) if scores else 1.0

    # =========================================================================
    # COMPOSITE SCORING
    # =========================================================================

    def _compute_composite_score(self, metrics: AccuracyMetrics) -> float:
        """Compute weighted composite score."""
        return (
            self.weights.entity_relevance * metrics.entity_relevance +
            self.weights.structural_accuracy * metrics.structural_accuracy +
            self.weights.temporal_coherence * metrics.temporal_coherence +
            self.weights.legal_precision * metrics.legal_precision +
            self.weights.answer_completeness * metrics.answer_completeness
        )

    def _count_retrieval_stats(
        self,
        metrics: AccuracyMetrics,
        retrieved: List[Dict[str, Any]],
        expected: List[Dict[str, Any]],
    ):
        """Count TP, FP, FN for precision/recall calculation."""
        retrieved_ids = {self._get_entity_id(e) for e in retrieved}
        expected_ids = {self._get_entity_id(e) for e in expected}

        metrics.true_positives = len(retrieved_ids & expected_ids)
        metrics.false_positives = len(retrieved_ids - expected_ids)
        metrics.false_negatives = len(expected_ids - retrieved_ids)

    # =========================================================================
    # HELPERS
    # =========================================================================

    def _get_entity_id(self, entity: Dict[str, Any]) -> str:
        """Extract entity ID from various formats."""
        return entity.get("id", entity.get("entity_id", entity.get("actor_id", str(entity))))

    def _is_valid_legal_date(self, date_val: Any) -> bool:
        """Check if a date is valid for legal purposes."""
        if date_val is None:
            return False

        try:
            if isinstance(date_val, str):
                # Parse common date formats
                for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%Y"]:
                    try:
                        dt = datetime.strptime(date_val, fmt)
                        # Valid if not in future and not too far in past
                        return datetime(1900, 1, 1) <= dt <= datetime.now()
                    except ValueError:
                        continue
            elif isinstance(date_val, datetime):
                return datetime(1900, 1, 1) <= date_val <= datetime.now()
        except Exception:
            pass

        return False

    def _check_state_ordering(self, states: List[Dict[str, Any]]) -> bool:
        """Check if states are chronologically ordered."""
        dates = []

        for state in states:
            start = state.get("start_date")
            if start:
                try:
                    if isinstance(start, str):
                        dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                    else:
                        dt = start
                    dates.append(dt)
                except Exception:
                    continue

        if len(dates) < 2:
            return True

        # Check if dates are monotonically increasing
        return all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))


# =============================================================================
# EVALUATION UTILITIES
# =============================================================================

def create_evaluation_dataset(
    queries: List[str],
    expected_results: List[List[Dict[str, Any]]],
    ground_truth_responses: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Create an evaluation dataset for batch scoring.

    Args:
        queries: List of test queries
        expected_results: Expected entities for each query
        ground_truth_responses: Optional ground truth responses

    Returns:
        List of evaluation items
    """
    dataset = []

    for i, query in enumerate(queries):
        item = {
            "id": f"eval_{i}",
            "query": query,
            "expected_entities": expected_results[i] if i < len(expected_results) else [],
        }

        if ground_truth_responses and i < len(ground_truth_responses):
            item["ground_truth_response"] = ground_truth_responses[i]

        dataset.append(item)

    return dataset


def batch_evaluate(
    scorer: RetrievalScorer,
    retrieval_fn: Callable[[str], Tuple[List[Dict], str]],
    evaluation_dataset: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Run batch evaluation on a dataset.

    Args:
        scorer: RetrievalScorer instance
        retrieval_fn: Function that takes query and returns (entities, response)
        evaluation_dataset: Dataset from create_evaluation_dataset

    Returns:
        Aggregate evaluation results
    """
    all_metrics = []

    for item in evaluation_dataset:
        query = item["query"]
        expected = item.get("expected_entities", [])
        ground_truth = item.get("ground_truth_response")

        # Run retrieval
        retrieved, response = retrieval_fn(query)

        # Score
        metrics = scorer.score_retrieval(
            query=query,
            retrieved_entities=retrieved,
            expected_entities=expected,
            response_text=response,
            ground_truth_response=ground_truth,
        )

        all_metrics.append(metrics)

    # Aggregate results
    n = len(all_metrics)
    if n == 0:
        return {"error": "No evaluations completed"}

    avg_composite = sum(m.composite_score for m in all_metrics) / n
    passing = sum(1 for m in all_metrics if m.meets_target())

    return {
        "total_evaluations": n,
        "passing_evaluations": passing,
        "pass_rate": passing / n,
        "average_composite_score": avg_composite,
        "average_precision": sum(m.precision for m in all_metrics) / n,
        "average_recall": sum(m.recall for m in all_metrics) / n,
        "average_f1": sum(m.f1_score for m in all_metrics) / n,
        "metrics_by_category": {
            "entity_relevance": sum(m.entity_relevance for m in all_metrics) / n,
            "structural_accuracy": sum(m.structural_accuracy for m in all_metrics) / n,
            "temporal_coherence": sum(m.temporal_coherence for m in all_metrics) / n,
            "legal_precision": sum(m.legal_precision for m in all_metrics) / n,
            "answer_completeness": sum(m.answer_completeness for m in all_metrics) / n,
        },
        "individual_results": [m.to_dict() for m in all_metrics],
    }
