"""
Benchmarking Framework
======================

Continuous monitoring and comprehensive evaluation of system accuracy.

This module provides:
- Real-time monitoring of queries and responses
- 6-metric scoring system integration
- Accuracy tracking over time with SQLite backend
- Dashboard metrics generation
- CLAUSE framework integration for legal discrepancy detection

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory

Usage:
    from src.benchmarking import ContinuousMonitor, AccuracyTracker

    # Monitor queries in real-time
    monitor = ContinuousMonitor("data/benchmarks")
    scores = monitor.monitor_query(query, response, ground_truth)

    # Track accuracy over time
    tracker = AccuracyTracker("data/benchmarks/accuracy.db")
    tracker.record_benchmark("retrieval", metrics)
    history = tracker.get_metric_history("composite_score", days=30)
"""

from .continuous_monitor import ContinuousMonitor
from .accuracy_tracker import AccuracyTracker

__all__ = [
    "ContinuousMonitor",
    "AccuracyTracker",
]
