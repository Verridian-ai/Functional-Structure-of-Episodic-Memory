"""
Continuous Monitor
==================

Real-time monitoring of system accuracy and performance.

This module provides continuous monitoring capabilities for the LAW OS system,
tracking query-response pairs and calculating comprehensive accuracy metrics
in real-time.

Features:
- Real-time query-response monitoring
- Integration with 6-metric scoring system
- Supervised and unsupervised quality assessment
- JSONL logging for continuous tracking
- VSA validation confidence integration

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

from src.observability.retrieval_scorer import RetrievalScorer
from src.observability.score_types import AccuracyMetrics, ScoringWeights


class ContinuousMonitor:
    """
    Real-time monitoring of system accuracy and performance.

    This class monitors queries, responses, and retrieval operations in real-time,
    calculating comprehensive accuracy metrics and logging results for analysis.

    Example:
        >>> monitor = ContinuousMonitor(Path("data/benchmarks"))
        >>> scores = monitor.monitor_query(
        ...     query="What are my property rights?",
        ...     response=response_dict,
        ...     ground_truth=gt_dict
        ... )
        >>> print(f"Composite Score: {scores['composite_score']:.3f}")
    """

    def __init__(
        self,
        output_dir: Path,
        weights: Optional[ScoringWeights] = None,
        target_score: float = 0.85
    ):
        """
        Initialize the continuous monitor.

        Args:
            output_dir: Directory for storing monitoring logs
            weights: Custom scoring weights (uses defaults if None)
            target_score: Target composite score (default: 0.85 to match paper's 85% F1)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize metrics log
        self.metrics_log = self.output_dir / "metrics_log.jsonl"

        # Initialize scorer with custom or default weights
        self.scorer = RetrievalScorer(weights=weights, target_score=target_score)
        self.target_score = target_score

        # Statistics tracking
        self.session_stats = {
            'total_queries': 0,
            'queries_meeting_target': 0,
            'total_score_sum': 0.0,
            'session_start': datetime.now().isoformat()
        }

    def monitor_query(
        self,
        query: str,
        response: Dict[str, Any],
        ground_truth: Optional[Dict[str, Any]] = None,
        workspace_state: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Monitor a single query-response pair.

        Args:
            query: User query string
            response: Response dictionary containing:
                - retrieved_entities: List of retrieved graph entities
                - response_text: Generated response text
                - validation: Optional VSA validation results
            ground_truth: Optional ground truth for supervised evaluation
            workspace_state: Optional GlobalWorkspace state

        Returns:
            Dictionary containing all calculated scores and metadata
        """
        timestamp = datetime.now().isoformat()

        # Extract components from response
        retrieved_entities = response.get('retrieved_entities', response.get('entities', []))
        response_text = response.get('response_text', response.get('text', ''))

        # Calculate scores
        if ground_truth:
            # Supervised evaluation
            scores = self._supervised_metrics(
                query=query,
                retrieved_entities=retrieved_entities,
                response_text=response_text,
                ground_truth=ground_truth,
                workspace_state=workspace_state
            )
        else:
            # Unsupervised quality metrics
            scores = self._unsupervised_metrics(
                query=query,
                retrieved_entities=retrieved_entities,
                response_text=response_text,
                workspace_state=workspace_state
            )

        # Add VSA validation metrics if available
        if 'validation' in response:
            scores['vsa_confidence'] = response['validation'].get('overall_confidence', 0.0)
            scores['hallucination_risk'] = 1.0 - scores['vsa_confidence']
            scores['validation_checks_passed'] = response['validation'].get('checks_passed', 0)
            scores['validation_checks_total'] = response['validation'].get('checks_total', 0)

        # Add metadata
        scores['query'] = query
        scores['timestamp'] = timestamp
        scores['has_ground_truth'] = ground_truth is not None
        scores['response_length'] = len(response_text)
        scores['entities_retrieved'] = len(retrieved_entities)
        scores['meets_target'] = scores['composite_score'] >= self.target_score

        # Update session stats
        self._update_session_stats(scores)

        # Log metrics
        self._log_metrics(scores)

        return scores

    def monitor_batch(
        self,
        queries: List[str],
        responses: List[Dict[str, Any]],
        ground_truths: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Monitor a batch of query-response pairs.

        Args:
            queries: List of query strings
            responses: List of response dictionaries
            ground_truths: Optional list of ground truth dictionaries

        Returns:
            Aggregate statistics for the batch
        """
        batch_scores = []

        for i, (query, response) in enumerate(zip(queries, responses)):
            gt = ground_truths[i] if ground_truths else None
            scores = self.monitor_query(query, response, gt)
            batch_scores.append(scores)

        # Calculate batch statistics
        return self._calculate_batch_stats(batch_scores)

    def _supervised_metrics(
        self,
        query: str,
        retrieved_entities: List[Dict[str, Any]],
        response_text: str,
        ground_truth: Dict[str, Any],
        workspace_state: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive metrics using ground truth.

        Args:
            query: User query
            retrieved_entities: Retrieved graph entities
            response_text: Generated response text
            ground_truth: Ground truth dictionary with expected entities and response
            workspace_state: Optional workspace state

        Returns:
            Dictionary of all calculated metrics
        """
        # Get expected data from ground truth
        expected_entities = ground_truth.get('entities', [])
        expected_response = ground_truth.get('response', None)

        # Use retrieval scorer for comprehensive evaluation
        metrics: AccuracyMetrics = self.scorer.score_retrieval(
            query=query,
            retrieved_entities=retrieved_entities,
            expected_entities=expected_entities,
            response_text=response_text,
            ground_truth_response=expected_response,
            workspace_state=workspace_state
        )

        return metrics.to_dict()

    def _unsupervised_metrics(
        self,
        query: str,
        retrieved_entities: List[Dict[str, Any]],
        response_text: str,
        workspace_state: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate quality metrics without ground truth (unsupervised).

        Uses heuristic scoring methods that don't require ground truth:
        - Query-entity relevance based on term overlap
        - Structural coherence of retrieved graph
        - Temporal consistency
        - Legal precision (citation presence)
        - Response completeness

        Args:
            query: User query
            retrieved_entities: Retrieved graph entities
            response_text: Generated response text
            workspace_state: Optional workspace state

        Returns:
            Dictionary of calculated quality metrics
        """
        # Use retrieval scorer with heuristic methods
        metrics: AccuracyMetrics = self.scorer.score_retrieval(
            query=query,
            retrieved_entities=retrieved_entities,
            expected_entities=None,  # No ground truth
            response_text=response_text,
            workspace_state=workspace_state
        )

        return metrics.to_dict()

    def _update_session_stats(self, scores: Dict[str, Any]) -> None:
        """Update session-level statistics."""
        self.session_stats['total_queries'] += 1
        self.session_stats['total_score_sum'] += scores['composite_score']

        if scores.get('meets_target', False):
            self.session_stats['queries_meeting_target'] += 1

    def _log_metrics(self, scores: Dict[str, Any]) -> None:
        """
        Log metrics to JSONL file.

        Each line contains a complete JSON object with all metrics and metadata.
        """
        with open(self.metrics_log, 'a') as f:
            f.write(json.dumps(scores) + '\n')

    def _calculate_batch_stats(self, batch_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate aggregate statistics for a batch."""
        if not batch_scores:
            return {}

        # Calculate averages
        metrics_to_avg = [
            'entity_relevance', 'structural_accuracy', 'temporal_coherence',
            'legal_precision', 'answer_completeness', 'composite_score'
        ]

        stats = {
            'batch_size': len(batch_scores),
            'timestamp': datetime.now().isoformat()
        }

        for metric in metrics_to_avg:
            values = [s.get(metric, 0.0) for s in batch_scores]
            stats[f'avg_{metric}'] = sum(values) / len(values) if values else 0.0
            stats[f'min_{metric}'] = min(values) if values else 0.0
            stats[f'max_{metric}'] = max(values) if values else 0.0

        # Count targets met
        stats['queries_meeting_target'] = sum(
            1 for s in batch_scores if s.get('meets_target', False)
        )
        stats['target_met_percentage'] = (
            stats['queries_meeting_target'] / stats['batch_size'] * 100
        )

        return stats

    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get current session statistics.

        Returns:
            Dictionary with session-level metrics
        """
        if self.session_stats['total_queries'] > 0:
            avg_score = (
                self.session_stats['total_score_sum'] /
                self.session_stats['total_queries']
            )
            target_percentage = (
                self.session_stats['queries_meeting_target'] /
                self.session_stats['total_queries'] * 100
            )
        else:
            avg_score = 0.0
            target_percentage = 0.0

        return {
            **self.session_stats,
            'average_composite_score': avg_score,
            'target_met_percentage': target_percentage,
            'session_duration': (
                datetime.now() -
                datetime.fromisoformat(self.session_stats['session_start'])
            ).total_seconds()
        }

    def load_metrics_history(
        self,
        limit: Optional[int] = None,
        since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Load historical metrics from log file.

        Args:
            limit: Maximum number of entries to load (most recent)
            since: Only load entries after this datetime

        Returns:
            List of metric dictionaries
        """
        if not self.metrics_log.exists():
            return []

        metrics = []
        with open(self.metrics_log, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)

                    # Filter by timestamp if requested
                    if since:
                        entry_time = datetime.fromisoformat(entry['timestamp'])
                        if entry_time < since:
                            continue

                    metrics.append(entry)

        # Return most recent if limit specified
        if limit:
            return metrics[-limit:]

        return metrics

    def calculate_trend(
        self,
        metric_name: str,
        days: int = 7,
        window_size: int = 10
    ) -> Dict[str, Any]:
        """
        Calculate trend for a specific metric over time.

        Args:
            metric_name: Name of metric to analyze
            days: Number of days to look back
            window_size: Moving average window size

        Returns:
            Dictionary with trend analysis
        """
        since = datetime.now() - timedelta(days=days)
        history = self.load_metrics_history(since=since)

        if not history:
            return {'trend': 'insufficient_data'}

        # Extract metric values
        values = [h.get(metric_name, 0.0) for h in history]

        if len(values) < 2:
            return {'trend': 'insufficient_data'}

        # Calculate moving average
        moving_avg = []
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            moving_avg.append(sum(window) / len(window))

        # Determine trend direction
        if len(moving_avg) >= 2:
            recent_avg = sum(moving_avg[-5:]) / len(moving_avg[-5:]) if len(moving_avg) >= 5 else moving_avg[-1]
            early_avg = sum(moving_avg[:5]) / 5 if len(moving_avg) >= 5 else moving_avg[0]
            change = recent_avg - early_avg

            if abs(change) < 0.01:
                direction = 'stable'
            elif change > 0:
                direction = 'improving'
            else:
                direction = 'declining'
        else:
            direction = 'stable'

        return {
            'metric': metric_name,
            'trend': direction,
            'current_value': values[-1] if values else 0.0,
            'average_value': sum(values) / len(values),
            'min_value': min(values),
            'max_value': max(values),
            'data_points': len(values),
            'days_analyzed': days
        }


# Import for calculate_trend
from datetime import timedelta
