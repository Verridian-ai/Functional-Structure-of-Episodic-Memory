"""
Evaluation Utilities
====================

Batch evaluation and dataset creation for retrieval scoring.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .retrieval_scorer import RetrievalScorer


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
    scorer: "RetrievalScorer",
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
