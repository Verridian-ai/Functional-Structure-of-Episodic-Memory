"""
Accuracy Tracker
================

Track system accuracy over time using SQLite backend.

This module provides persistent storage and historical tracking of benchmark
results, enabling trend analysis and performance monitoring over time.

Features:
- SQLite-based persistent storage
- Track benchmark results by stage (classification, extraction, retrieval, etc.)
- Historical metric queries with time filtering
- Trend analysis and performance tracking
- Export capabilities for reporting

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import statistics


class AccuracyTracker:
    """
    Track system accuracy over time using SQLite.

    Provides persistent storage of benchmark results with rich querying
    capabilities for historical analysis and trend detection.

    Example:
        >>> tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))
        >>> tracker.record_benchmark("retrieval", {
        ...     'composite_score': 0.87,
        ...     'entity_relevance': 0.90,
        ...     'legal_precision': 0.85
        ... })
        >>> history = tracker.get_metric_history("composite_score", days=30)
    """

    def __init__(self, db_path: Path):
        """
        Initialize the accuracy tracker.

        Args:
            db_path: Path to SQLite database file (created if doesn't exist)
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database schema."""
        cursor = self.conn.cursor()

        # Main benchmark runs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                stage TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                score REAL NOT NULL,
                metadata TEXT,
                run_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON benchmark_runs(timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_stage_metric
            ON benchmark_runs(stage, metric_name)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_run_id
            ON benchmark_runs(run_id)
        ''')

        # Table for tracking benchmark suite runs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmark_suite_runs (
                run_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_benchmarks INTEGER,
                benchmarks_passed INTEGER,
                overall_score REAL,
                status TEXT,
                metadata TEXT
            )
        ''')

        self.conn.commit()

    def record_benchmark(
        self,
        stage: str,
        metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None,
        run_id: Optional[str] = None
    ) -> None:
        """
        Record benchmark results for a specific stage.

        Args:
            stage: Benchmark stage (e.g., 'classification', 'retrieval', 'end_to_end')
            metrics: Dictionary of metric names and scores
            metadata: Optional metadata to store with the benchmark
            run_id: Optional run identifier to group related benchmarks
        """
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None

        cursor = self.conn.cursor()

        for metric_name, score in metrics.items():
            cursor.execute('''
                INSERT INTO benchmark_runs (timestamp, stage, metric_name, score, metadata, run_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, stage, metric_name, score, metadata_json, run_id))

        self.conn.commit()

    def record_suite_run(
        self,
        run_id: str,
        start_time: datetime,
        end_time: datetime,
        total_benchmarks: int,
        benchmarks_passed: int,
        overall_score: float,
        status: str = 'completed',
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a complete benchmark suite run.

        Args:
            run_id: Unique identifier for this suite run
            start_time: When the suite started
            end_time: When the suite ended
            total_benchmarks: Total number of benchmarks run
            benchmarks_passed: Number of benchmarks that passed
            overall_score: Overall composite score
            status: Run status (completed, failed, partial)
            metadata: Optional metadata
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO benchmark_suite_runs
            (run_id, start_time, end_time, total_benchmarks, benchmarks_passed,
             overall_score, status, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            run_id,
            start_time.isoformat(),
            end_time.isoformat(),
            total_benchmarks,
            benchmarks_passed,
            overall_score,
            status,
            json.dumps(metadata) if metadata else None
        ))

        self.conn.commit()

    def get_metric_history(
        self,
        metric_name: str,
        days: int = 30,
        stage: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical metric values.

        Args:
            metric_name: Name of the metric to retrieve
            days: Number of days to look back
            stage: Optional filter by benchmark stage

        Returns:
            List of dictionaries with timestamp, score, and metadata
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        cursor = self.conn.cursor()

        if stage:
            cursor.execute('''
                SELECT timestamp, score, metadata, stage
                FROM benchmark_runs
                WHERE metric_name = ? AND timestamp > ? AND stage = ?
                ORDER BY timestamp
            ''', (metric_name, cutoff, stage))
        else:
            cursor.execute('''
                SELECT timestamp, score, metadata, stage
                FROM benchmark_runs
                WHERE metric_name = ? AND timestamp > ?
                ORDER BY timestamp
            ''', (metric_name, cutoff))

        results = []
        for row in cursor.fetchall():
            results.append({
                'timestamp': row['timestamp'],
                'score': row['score'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else {},
                'stage': row['stage']
            })

        return results

    def get_latest_metrics(
        self,
        stage: str,
        limit: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get the most recent benchmark results for a stage.

        Args:
            stage: Benchmark stage
            limit: Number of recent runs to retrieve

        Returns:
            List of dictionaries with all metrics from recent runs
        """
        cursor = self.conn.cursor()

        # Get unique timestamps for this stage
        cursor.execute('''
            SELECT DISTINCT timestamp
            FROM benchmark_runs
            WHERE stage = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (stage, limit))

        timestamps = [row['timestamp'] for row in cursor.fetchall()]

        results = []
        for ts in timestamps:
            # Get all metrics for this timestamp
            cursor.execute('''
                SELECT metric_name, score, metadata
                FROM benchmark_runs
                WHERE stage = ? AND timestamp = ?
            ''', (stage, ts))

            metrics = {}
            metadata = None
            for row in cursor.fetchall():
                metrics[row['metric_name']] = row['score']
                if row['metadata'] and not metadata:
                    metadata = json.loads(row['metadata'])

            results.append({
                'timestamp': ts,
                'stage': stage,
                'metrics': metrics,
                'metadata': metadata or {}
            })

        return results

    def get_trend_analysis(
        self,
        metric_name: str,
        days: int = 30,
        stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze trends for a specific metric.

        Args:
            metric_name: Metric to analyze
            days: Number of days to analyze
            stage: Optional filter by stage

        Returns:
            Dictionary with trend statistics
        """
        history = self.get_metric_history(metric_name, days, stage)

        if not history:
            return {
                'metric': metric_name,
                'trend': 'no_data',
                'data_points': 0
            }

        scores = [h['score'] for h in history]

        # Calculate statistics
        analysis = {
            'metric': metric_name,
            'stage': stage,
            'data_points': len(scores),
            'current_value': scores[-1],
            'mean': statistics.mean(scores),
            'median': statistics.median(scores),
            'min': min(scores),
            'max': max(scores),
            'range': max(scores) - min(scores)
        }

        # Add standard deviation if enough data
        if len(scores) > 1:
            analysis['std_dev'] = statistics.stdev(scores)

        # Determine trend direction
        if len(scores) >= 10:
            # Compare first half to second half
            mid = len(scores) // 2
            first_half_avg = statistics.mean(scores[:mid])
            second_half_avg = statistics.mean(scores[mid:])

            change = second_half_avg - first_half_avg
            change_percent = (change / first_half_avg * 100) if first_half_avg != 0 else 0

            if abs(change_percent) < 2:
                trend = 'stable'
            elif change_percent > 0:
                trend = 'improving'
            else:
                trend = 'declining'

            analysis['trend'] = trend
            analysis['change_percent'] = change_percent
        else:
            analysis['trend'] = 'insufficient_data'

        return analysis

    def get_stage_summary(self, stage: str, days: int = 7) -> Dict[str, Any]:
        """
        Get summary statistics for all metrics in a stage.

        Args:
            stage: Benchmark stage
            days: Number of days to summarize

        Returns:
            Dictionary with summary statistics per metric
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT metric_name, AVG(score) as avg_score, MIN(score) as min_score,
                   MAX(score) as max_score, COUNT(*) as count
            FROM benchmark_runs
            WHERE stage = ? AND timestamp > ?
            GROUP BY metric_name
        ''', (stage, cutoff))

        summary = {
            'stage': stage,
            'days': days,
            'metrics': {}
        }

        for row in cursor.fetchall():
            summary['metrics'][row['metric_name']] = {
                'average': row['avg_score'],
                'min': row['min_score'],
                'max': row['max_score'],
                'count': row['count']
            }

        return summary

    def get_suite_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get history of benchmark suite runs.

        Args:
            limit: Number of recent suite runs to retrieve

        Returns:
            List of suite run summaries
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT run_id, start_time, end_time, total_benchmarks,
                   benchmarks_passed, overall_score, status, metadata
            FROM benchmark_suite_runs
            ORDER BY start_time DESC
            LIMIT ?
        ''', (limit,))

        results = []
        for row in cursor.fetchall():
            start = datetime.fromisoformat(row['start_time'])
            end = datetime.fromisoformat(row['end_time']) if row['end_time'] else datetime.now()
            duration = (end - start).total_seconds()

            results.append({
                'run_id': row['run_id'],
                'start_time': row['start_time'],
                'end_time': row['end_time'],
                'duration_seconds': duration,
                'total_benchmarks': row['total_benchmarks'],
                'benchmarks_passed': row['benchmarks_passed'],
                'pass_rate': row['benchmarks_passed'] / row['total_benchmarks'] * 100 if row['total_benchmarks'] > 0 else 0,
                'overall_score': row['overall_score'],
                'status': row['status'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else {}
            })

        return results

    def export_to_csv(self, output_path: Path, days: int = 30) -> None:
        """
        Export benchmark data to CSV for external analysis.

        Args:
            output_path: Path for CSV file
            days: Number of days to export
        """
        import csv

        cutoff = (datetime.now() - timedelta(days=days)).isoformat()

        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, stage, metric_name, score, metadata
            FROM benchmark_runs
            WHERE timestamp > ?
            ORDER BY timestamp
        ''', (cutoff,))

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'stage', 'metric_name', 'score', 'metadata'])

            for row in cursor.fetchall():
                writer.writerow([
                    row['timestamp'],
                    row['stage'],
                    row['metric_name'],
                    row['score'],
                    row['metadata'] or ''
                ])

    def get_alerts(self, threshold: float = 0.80) -> List[Dict[str, Any]]:
        """
        Get metrics that are currently below threshold.

        Args:
            threshold: Score threshold for alerts

        Returns:
            List of metrics with scores below threshold
        """
        alerts = []

        # Get latest score for each metric/stage combination
        cursor = self.conn.cursor()
        cursor.execute('''
            WITH latest_scores AS (
                SELECT stage, metric_name, MAX(timestamp) as latest_ts
                FROM benchmark_runs
                GROUP BY stage, metric_name
            )
            SELECT br.stage, br.metric_name, br.score, br.timestamp
            FROM benchmark_runs br
            INNER JOIN latest_scores ls
                ON br.stage = ls.stage
                AND br.metric_name = ls.metric_name
                AND br.timestamp = ls.latest_ts
            WHERE br.score < ?
            ORDER BY br.score
        ''', (threshold,))

        for row in cursor.fetchall():
            severity = 'high' if row['score'] < 0.70 else 'medium'
            alerts.append({
                'stage': row['stage'],
                'metric': row['metric_name'],
                'score': row['score'],
                'timestamp': row['timestamp'],
                'severity': severity,
                'threshold': threshold
            })

        return alerts

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
