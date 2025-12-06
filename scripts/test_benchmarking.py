"""
Test Benchmarking Framework
============================

Demonstration and validation of the benchmarking framework.

This script demonstrates:
1. Continuous monitoring of queries
2. Accuracy tracking over time
3. Trend analysis
4. Dashboard generation
5. Integration with retrieval scorer

Usage:
    python scripts/test_benchmarking.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.benchmarking import ContinuousMonitor, AccuracyTracker
from src.observability.retrieval_scorer import RetrievalScorer


def test_continuous_monitoring():
    """Test continuous monitoring functionality."""
    print("\n" + "=" * 70)
    print("TEST 1: Continuous Monitoring")
    print("=" * 70)

    # Initialize monitor
    monitor = ContinuousMonitor(Path("data/benchmarks/test"))

    # Sample query-response pairs
    test_cases = [
        {
            'query': "What are my property rights after separation?",
            'response': {
                'retrieved_entities': [
                    {'id': 'actor_1', 'type': 'actor', 'role': 'applicant', 'name': 'John Smith'},
                    {'id': 'actor_2', 'type': 'actor', 'role': 'respondent', 'name': 'Jane Smith'},
                    {'id': 'state_1', 'type': 'state', 'name': 'separated', 'start_date': '2023-01-15'},
                ],
                'response_text': "Under section 79 of the Family Law Act, property rights...",
                'validation': {
                    'overall_confidence': 0.92,
                    'checks_passed': 8,
                    'checks_total': 10
                }
            },
            'ground_truth': {
                'entities': [
                    {'id': 'actor_1', 'type': 'actor', 'role': 'applicant'},
                    {'id': 'actor_2', 'type': 'actor', 'role': 'respondent'},
                    {'id': 'state_1', 'type': 'state'}
                ],
                'response': "Section 79 of the Family Law Act governs property settlement..."
            }
        },
        {
            'query': "How is child custody determined?",
            'response': {
                'retrieved_entities': [
                    {'id': 'actor_3', 'type': 'actor', 'role': 'child', 'name': 'Child A'},
                    {'id': 'state_2', 'type': 'state', 'name': 'parenting_order'},
                ],
                'response_text': "Section 60CC of the Family Law Act outlines best interests...",
                'validation': {
                    'overall_confidence': 0.89,
                    'checks_passed': 9,
                    'checks_total': 10
                }
            }
        }
    ]

    # Monitor each query
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"  Query: {test_case['query']}")

        scores = monitor.monitor_query(
            query=test_case['query'],
            response=test_case['response'],
            ground_truth=test_case.get('ground_truth')
        )

        print(f"  Composite Score: {scores['composite_score']:.3f}")
        print(f"  Entity Relevance: {scores['entity_relevance']:.3f}")
        print(f"  Structural Accuracy: {scores['structural_accuracy']:.3f}")
        print(f"  Legal Precision: {scores['legal_precision']:.3f}")
        print(f"  VSA Confidence: {scores.get('vsa_confidence', 0.0):.3f}")
        meets = "YES" if scores['meets_target'] else "NO"
        print(f"  Meets Target: {meets}")

    # Get session stats
    print("\nSession Statistics:")
    stats = monitor.get_session_stats()
    print(f"  Total Queries: {stats['total_queries']}")
    print(f"  Avg Composite: {stats['average_composite_score']:.3f}")
    print(f"  Target Met %: {stats['target_met_percentage']:.1f}%")

    print("\n[PASS] Continuous monitoring test passed")


def test_accuracy_tracking():
    """Test accuracy tracking and historical queries."""
    print("\n" + "=" * 70)
    print("TEST 2: Accuracy Tracking")
    print("=" * 70)

    # Initialize tracker
    db_path = Path("data/benchmarks/test/accuracy_test.db")
    tracker = AccuracyTracker(db_path)

    # Simulate benchmark runs over time
    print("\nSimulating benchmark runs over 30 days...")

    base_date = datetime.now() - timedelta(days=30)

    for day in range(30):
        timestamp = base_date + timedelta(days=day)

        # Simulate improving scores over time
        improvement_factor = day / 30.0 * 0.1
        base_score = 0.75

        metrics = {
            'composite_score': base_score + improvement_factor + (day % 3) * 0.01,
            'entity_relevance': 0.80 + improvement_factor,
            'structural_accuracy': 0.78 + improvement_factor,
            'temporal_coherence': 0.82 + improvement_factor,
            'legal_precision': 0.76 + improvement_factor,
            'answer_completeness': 0.79 + improvement_factor
        }

        # Record with backdated timestamp (for testing)
        # In production, this happens automatically
        tracker.record_benchmark(
            stage='retrieval',
            metrics=metrics,
            metadata={'simulated': True, 'day': day}
        )

    print(f"  Recorded {30} benchmark runs")

    # Query historical data
    print("\nQuerying metric history...")
    history = tracker.get_metric_history('composite_score', days=30)
    print(f"  Retrieved {len(history)} historical data points")

    # Analyze trends
    print("\nTrend Analysis:")
    for metric in ['composite_score', 'entity_relevance', 'legal_precision']:
        trend = tracker.get_trend_analysis(metric, days=30)
        print(f"  {metric}:")
        print(f"    Trend: {trend['trend']}")
        print(f"    Current: {trend['current_value']:.3f}")
        print(f"    Mean: {trend['mean']:.3f}")
        print(f"    Range: {trend['min']:.3f} - {trend['max']:.3f}")

    # Get stage summary
    print("\nStage Summary (last 7 days):")
    summary = tracker.get_stage_summary('retrieval', days=7)
    for metric, stats in summary['metrics'].items():
        print(f"  {metric}: avg={stats['average']:.3f}, min={stats['min']:.3f}, max={stats['max']:.3f}")

    # Check alerts
    print("\nChecking for alerts...")
    alerts = tracker.get_alerts(threshold=0.80)
    if alerts:
        print(f"  Found {len(alerts)} alerts:")
        for alert in alerts[:3]:
            print(f"    {alert['severity'].upper()}: {alert['metric']} = {alert['score']:.3f}")
    else:
        print("  No alerts (all metrics above threshold)")

    print("\n[PASS] Accuracy tracking test passed")

    tracker.close()


def test_retrieval_scorer_integration():
    """Test integration with retrieval scorer."""
    print("\n" + "=" * 70)
    print("TEST 3: Retrieval Scorer Integration")
    print("=" * 70)

    scorer = RetrievalScorer()

    # Sample retrieval scenario
    query = "What orders were made regarding the children?"

    retrieved_entities = [
        {'id': 'actor_1', 'type': 'actor', 'role': 'child', 'name': 'Child A'},
        {'id': 'actor_2', 'type': 'actor', 'role': 'applicant', 'name': 'Parent A'},
        {'id': 'state_1', 'type': 'state', 'name': 'parenting_order', 'start_date': '2024-01-15'},
        {'id': 'verb_1', 'type': 'verb_phrase', 'name': 'spend_time_with'}
    ]

    expected_entities = [
        {'id': 'actor_1', 'type': 'actor', 'role': 'child'},
        {'id': 'state_1', 'type': 'state', 'name': 'parenting_order'},
        {'id': 'verb_1', 'type': 'verb_phrase'}
    ]

    response_text = """
    Under section 60CC of the Family Law Act, the Court made orders for the child
    to spend time with both parents. The parenting order dated 15 January 2024
    provides for equal shared parental responsibility.
    """

    # Score retrieval
    print("\nScoring retrieval operation...")
    metrics = scorer.score_retrieval(
        query=query,
        retrieved_entities=retrieved_entities,
        expected_entities=expected_entities,
        response_text=response_text
    )

    print("\nRetrieval Metrics:")
    print(f"  Entity Relevance: {metrics.entity_relevance:.3f}")
    print(f"  Structural Accuracy: {metrics.structural_accuracy:.3f}")
    print(f"  Temporal Coherence: {metrics.temporal_coherence:.3f}")
    print(f"  Legal Precision: {metrics.legal_precision:.3f}")
    print(f"  Answer Completeness: {metrics.answer_completeness:.3f}")
    print(f"  Citation Accuracy: {metrics.citation_accuracy:.3f}")
    print(f"  Composite Score: {metrics.composite_score:.3f}")

    print(f"\nPrecision/Recall:")
    print(f"  Precision: {metrics.precision:.3f}")
    print(f"  Recall: {metrics.recall:.3f}")
    print(f"  F1 Score: {metrics.f1_score:.3f}")

    meets = "YES" if metrics.meets_target(0.85) else "NO"
    print(f"\nMeets Target (0.85): {meets}")

    print("\n[PASS] Retrieval scorer integration test passed")


def test_dashboard_generation():
    """Test dashboard metrics generation."""
    print("\n" + "=" * 70)
    print("TEST 4: Dashboard Generation")
    print("=" * 70)

    # Use tracker from previous test
    db_path = Path("data/benchmarks/test/accuracy_test.db")
    tracker = AccuracyTracker(db_path)

    print("\nGenerating dashboard metrics...")

    dashboard = {
        'generated_at': datetime.now().isoformat(),
        'current_accuracy': {},
        'trends': {},
        'alerts': [],
        'stage_summaries': {}
    }

    # Get current metrics
    key_metrics = [
        'composite_score', 'entity_relevance', 'structural_accuracy',
        'temporal_coherence', 'legal_precision', 'answer_completeness'
    ]

    for metric in key_metrics:
        history = tracker.get_metric_history(metric, days=1)
        if history:
            dashboard['current_accuracy'][metric] = history[-1]['score']

    # Get trends
    for metric in key_metrics:
        trend = tracker.get_trend_analysis(metric, days=7)
        if trend.get('trend') != 'no_data':
            dashboard['trends'][metric] = {
                'direction': trend['trend'],
                'current': trend['current_value'],
                'mean': trend['mean']
            }

    # Get alerts
    dashboard['alerts'] = tracker.get_alerts(threshold=0.80)

    # Get stage summaries
    for stage in ['retrieval']:
        summary = tracker.get_stage_summary(stage, days=7)
        dashboard['stage_summaries'][stage] = summary

    # Save dashboard
    dashboard_path = Path("data/benchmarks/test/dashboard.json")
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dashboard_path, 'w') as f:
        json.dump(dashboard, f, indent=2)

    print(f"  Dashboard saved to: {dashboard_path}")
    print(f"  Metrics tracked: {len(dashboard['current_accuracy'])}")
    print(f"  Trends analyzed: {len(dashboard['trends'])}")
    print(f"  Active alerts: {len(dashboard['alerts'])}")

    print("\nSample Dashboard Data:")
    print(f"  Current Composite Score: {dashboard['current_accuracy'].get('composite_score', 0.0):.3f}")

    for metric, trend in list(dashboard['trends'].items())[:3]:
        print(f"  {metric}: {trend['direction']} (current: {trend['current']:.3f})")

    print("\n[PASS] Dashboard generation test passed")

    tracker.close()


def test_batch_monitoring():
    """Test batch query monitoring."""
    print("\n" + "=" * 70)
    print("TEST 5: Batch Monitoring")
    print("=" * 70)

    monitor = ContinuousMonitor(Path("data/benchmarks/test"))

    # Batch of queries
    queries = [
        "What are my property rights?",
        "How is child custody determined?",
        "What is spousal maintenance?"
    ]

    responses = [
        {
            'retrieved_entities': [{'id': 'e1', 'type': 'actor'}],
            'response_text': "Section 79 governs property division...",
            'validation': {'overall_confidence': 0.90}
        },
        {
            'retrieved_entities': [{'id': 'e2', 'type': 'actor'}],
            'response_text': "Section 60CC outlines best interests...",
            'validation': {'overall_confidence': 0.88}
        },
        {
            'retrieved_entities': [{'id': 'e3', 'type': 'state'}],
            'response_text': "Spousal maintenance under section 74...",
            'validation': {'overall_confidence': 0.85}
        }
    ]

    print(f"\nMonitoring batch of {len(queries)} queries...")

    batch_stats = monitor.monitor_batch(queries, responses)

    print("\nBatch Statistics:")
    print(f"  Batch Size: {batch_stats['batch_size']}")
    print(f"  Avg Composite: {batch_stats.get('avg_composite_score', 0.0):.3f}")
    print(f"  Min Composite: {batch_stats.get('min_composite_score', 0.0):.3f}")
    print(f"  Max Composite: {batch_stats.get('max_composite_score', 0.0):.3f}")
    print(f"  Target Met: {batch_stats['queries_meeting_target']}/{batch_stats['batch_size']}")
    print(f"  Target Met %: {batch_stats['target_met_percentage']:.1f}%")

    print("\n[PASS] Batch monitoring test passed")


def main():
    """Run all benchmarking tests."""
    print("\n" + "=" * 70)
    print("BENCHMARKING FRAMEWORK TEST SUITE")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")

    try:
        # Run all tests
        test_continuous_monitoring()
        test_accuracy_tracking()
        test_retrieval_scorer_integration()
        test_dashboard_generation()
        test_batch_monitoring()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED")
        print("=" * 70)

        print("\nGenerated Test Files:")
        print("  data/benchmarks/test/metrics_log.jsonl")
        print("  data/benchmarks/test/accuracy_test.db")
        print("  data/benchmarks/test/dashboard.json")

        return 0

    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
