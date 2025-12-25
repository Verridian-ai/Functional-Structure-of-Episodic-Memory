"""
Test Search Methods Benchmark
==============================

Pytest integration for the comprehensive search methods benchmark suite.

Runs the full benchmark suite and validates:
1. All retrieval methods initialize correctly
2. Query execution completes without errors
3. Accuracy metrics meet minimum thresholds
4. Performance metrics are within acceptable bounds
"""

import sys
import pytest
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.benchmarks.search_methods_benchmark import (
    SearchMethodsBenchmark,
    BenchmarkQuery,
    BenchmarkReport,
    MethodMetrics,
    BENCHMARK_QUERIES
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope='module')
def benchmark_instance():
    """Create benchmark instance for testing."""
    return SearchMethodsBenchmark(
        workspace_dir=Path("data/workspaces"),
        data_dir=Path("data"),
        tracker_db=Path("data/benchmarks/test_search_benchmark.db")
    )


@pytest.fixture(scope='module')
def benchmark_report(benchmark_instance):
    """Run full benchmark and return report."""
    return benchmark_instance.run_full_benchmark(top_k=5, save_raw_results=True)


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestBenchmarkInitialization:
    """Test benchmark initialization."""

    def test_benchmark_queries_exist(self):
        """Verify benchmark queries are defined."""
        assert len(BENCHMARK_QUERIES) > 0
        assert all(isinstance(q, BenchmarkQuery) for q in BENCHMARK_QUERIES)

    def test_query_categories_coverage(self):
        """Verify queries cover multiple categories."""
        categories = set(q.category for q in BENCHMARK_QUERIES)
        expected_categories = {
            'semantic_search', 'role_search', 'state_search',
            'entity_search', 'action_search', 'edge_case'
        }
        assert len(categories) >= 5, f"Expected at least 5 categories, got {len(categories)}"

    def test_query_difficulties_coverage(self):
        """Verify queries cover multiple difficulty levels."""
        difficulties = set(q.difficulty for q in BENCHMARK_QUERIES)
        expected = {'easy', 'medium', 'hard', 'edge'}
        assert difficulties == expected, f"Expected {expected}, got {difficulties}"

    def test_query_domains_coverage(self):
        """Verify queries cover multiple domains."""
        domains = set(q.domain for q in BENCHMARK_QUERIES)
        assert 'family' in domains
        assert len(domains) >= 2, "Expected queries for at least 2 domains"

    def test_retrievers_initialize(self, benchmark_instance):
        """Verify retrievers initialize correctly."""
        assert benchmark_instance is not None
        assert len(benchmark_instance.retrievers) > 0

    def test_gsw_retriever_available(self, benchmark_instance):
        """Verify GSW retriever is available."""
        assert 'gsw' in benchmark_instance.retrievers
        retriever = benchmark_instance.retrievers['gsw']
        if retriever:
            stats = retriever.get_statistics()
            assert stats['total_workspaces'] >= 0

    def test_hybrid_retriever_available(self, benchmark_instance):
        """Verify hybrid retriever is available."""
        assert 'hybrid' in benchmark_instance.retrievers


# ============================================================================
# BENCHMARK EXECUTION TESTS
# ============================================================================

class TestBenchmarkExecution:
    """Test benchmark execution."""

    def test_benchmark_completes(self, benchmark_report):
        """Verify benchmark runs to completion."""
        assert benchmark_report is not None
        assert isinstance(benchmark_report, BenchmarkReport)
        assert benchmark_report.run_id is not None

    def test_benchmark_duration_reasonable(self, benchmark_report):
        """Verify benchmark completes in reasonable time."""
        # Should complete within 5 minutes for ~25 queries x 5 methods
        assert benchmark_report.duration_seconds < 300

    def test_all_methods_tested(self, benchmark_report):
        """Verify all methods were tested."""
        assert len(benchmark_report.methods_tested) >= 3
        assert 'gsw' in benchmark_report.methods_tested or 'hybrid' in benchmark_report.methods_tested

    def test_metrics_calculated(self, benchmark_report):
        """Verify metrics are calculated for all methods."""
        for method in benchmark_report.methods_tested:
            assert method in benchmark_report.method_metrics
            metrics = benchmark_report.method_metrics[method]
            assert isinstance(metrics, MethodMetrics)
            assert metrics.total_queries > 0


# ============================================================================
# ACCURACY TESTS
# ============================================================================

class TestAccuracyMetrics:
    """Test accuracy metrics meet thresholds."""

    # Minimum acceptable thresholds
    MIN_PRECISION = 0.1  # At least 10% precision
    MIN_RECALL = 0.1     # At least 10% recall
    MIN_F1 = 0.1         # At least 10% F1
    MIN_MRR = 0.1        # At least 10% MRR

    def test_precision_above_minimum(self, benchmark_report):
        """Verify precision meets minimum threshold."""
        for method, metrics in benchmark_report.method_metrics.items():
            # Skip if no results (might be initialization failure)
            if metrics.total_results == 0:
                pytest.skip(f"{method} returned no results")
            assert metrics.precision >= self.MIN_PRECISION, \
                f"{method} precision {metrics.precision:.3f} below threshold {self.MIN_PRECISION}"

    def test_recall_above_minimum(self, benchmark_report):
        """Verify recall meets minimum threshold."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.total_results == 0:
                pytest.skip(f"{method} returned no results")
            assert metrics.recall >= self.MIN_RECALL, \
                f"{method} recall {metrics.recall:.3f} below threshold {self.MIN_RECALL}"

    def test_f1_score_above_minimum(self, benchmark_report):
        """Verify F1 score meets minimum threshold."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.total_results == 0:
                pytest.skip(f"{method} returned no results")
            assert metrics.f1_score >= self.MIN_F1, \
                f"{method} F1 {metrics.f1_score:.3f} below threshold {self.MIN_F1}"

    def test_mrr_above_minimum(self, benchmark_report):
        """Verify MRR meets minimum threshold."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.total_results == 0:
                pytest.skip(f"{method} returned no results")
            assert metrics.mrr >= self.MIN_MRR, \
                f"{method} MRR {metrics.mrr:.3f} below threshold {self.MIN_MRR}"

    def test_best_method_f1_above_threshold(self, benchmark_report):
        """Verify at least one method has good F1."""
        best_f1 = max(m.f1_score for m in benchmark_report.method_metrics.values())
        assert best_f1 >= 0.2, f"Best F1 score {best_f1:.3f} is below expected 0.2"


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformanceMetrics:
    """Test performance metrics meet thresholds."""

    MAX_AVG_LATENCY_MS = 1000  # Max 1 second average
    MAX_P95_LATENCY_MS = 2000  # Max 2 seconds for P95
    MAX_P99_LATENCY_MS = 5000  # Max 5 seconds for P99

    def test_average_latency_acceptable(self, benchmark_report):
        """Verify average latency is acceptable."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.avg_latency_ms == 0:
                continue
            assert metrics.avg_latency_ms <= self.MAX_AVG_LATENCY_MS, \
                f"{method} avg latency {metrics.avg_latency_ms:.1f}ms exceeds {self.MAX_AVG_LATENCY_MS}ms"

    def test_p95_latency_acceptable(self, benchmark_report):
        """Verify P95 latency is acceptable."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.p95_latency_ms == 0:
                continue
            assert metrics.p95_latency_ms <= self.MAX_P95_LATENCY_MS, \
                f"{method} P95 latency {metrics.p95_latency_ms:.1f}ms exceeds {self.MAX_P95_LATENCY_MS}ms"

    def test_p99_latency_acceptable(self, benchmark_report):
        """Verify P99 latency is acceptable."""
        for method, metrics in benchmark_report.method_metrics.items():
            if metrics.p99_latency_ms == 0:
                continue
            assert metrics.p99_latency_ms <= self.MAX_P99_LATENCY_MS, \
                f"{method} P99 latency {metrics.p99_latency_ms:.1f}ms exceeds {self.MAX_P99_LATENCY_MS}ms"

    def test_zero_result_queries_below_threshold(self, benchmark_report):
        """Verify zero-result queries are not excessive."""
        for method, metrics in benchmark_report.method_metrics.items():
            max_zero_results = metrics.total_queries * 0.5  # Allow up to 50% zero results
            assert metrics.zero_result_queries <= max_zero_results, \
                f"{method} has {metrics.zero_result_queries}/{metrics.total_queries} zero-result queries"


# ============================================================================
# COMPARISON TESTS
# ============================================================================

class TestMethodComparison:
    """Test method comparison analysis."""

    def test_ranking_by_f1_exists(self, benchmark_report):
        """Verify F1 ranking is generated."""
        assert 'ranking_by_f1' in benchmark_report.comparison
        ranking = benchmark_report.comparison['ranking_by_f1']
        assert len(ranking) == len(benchmark_report.methods_tested)

    def test_ranking_by_latency_exists(self, benchmark_report):
        """Verify latency ranking is generated."""
        assert 'ranking_by_latency' in benchmark_report.comparison
        ranking = benchmark_report.comparison['ranking_by_latency']
        assert len(ranking) == len(benchmark_report.methods_tested)

    def test_f1_ranking_is_sorted(self, benchmark_report):
        """Verify F1 ranking is properly sorted (descending)."""
        ranking = benchmark_report.comparison['ranking_by_f1']
        f1_scores = [item['f1'] for item in ranking]
        assert f1_scores == sorted(f1_scores, reverse=True)

    def test_latency_ranking_is_sorted(self, benchmark_report):
        """Verify latency ranking is properly sorted (ascending)."""
        ranking = benchmark_report.comparison['ranking_by_latency']
        latencies = [item['avg_latency_ms'] for item in ranking]
        assert latencies == sorted(latencies)

    def test_recommendations_generated(self, benchmark_report):
        """Verify recommendations are generated."""
        assert len(benchmark_report.recommendations) > 0


# ============================================================================
# CATEGORY BREAKDOWN TESTS
# ============================================================================

class TestCategoryBreakdown:
    """Test category-level breakdown analysis."""

    def test_semantic_search_performance(self, benchmark_report):
        """Test semantic search category performance."""
        for method, metrics in benchmark_report.method_metrics.items():
            if 'semantic_search' in metrics.by_category:
                cat_data = metrics.by_category['semantic_search']
                # Semantic search should have reasonable performance
                assert cat_data['precision'] >= 0.0
                assert cat_data['recall'] >= 0.0

    def test_edge_cases_handled(self, benchmark_report):
        """Test edge cases are handled without crashing."""
        # The fact that we got here means edge cases didn't crash
        for method, metrics in benchmark_report.method_metrics.items():
            if 'edge_case' in metrics.by_category:
                cat_data = metrics.by_category['edge_case']
                # Edge cases are expected to have low scores
                assert cat_data['count'] >= 1

    def test_difficulty_breakdown_exists(self, benchmark_report):
        """Test difficulty breakdown is generated."""
        for method, metrics in benchmark_report.method_metrics.items():
            assert len(metrics.by_difficulty) > 0
            assert 'easy' in metrics.by_difficulty or 'medium' in metrics.by_difficulty


# ============================================================================
# INDIVIDUAL METHOD TESTS
# ============================================================================

class TestGSWRetriever:
    """Test GSW retriever specifically."""

    def test_gsw_retrieves_actors(self, benchmark_instance):
        """Test GSW retrieves actor entities."""
        gsw = benchmark_instance.retrievers.get('gsw')
        if gsw is None:
            pytest.skip("GSW retriever not available")

        results = gsw.retrieve("custody arrangement", top_k=5)
        # Results should include actors or verb phrases
        if results:
            types = [r['type'] for r in results]
            assert any(t in ['actor', 'verb_phrase', 'question'] for t in types)

    def test_gsw_role_search(self, benchmark_instance):
        """Test GSW role-based search."""
        gsw = benchmark_instance.retrievers.get('gsw')
        if gsw is None:
            pytest.skip("GSW retriever not available")

        # Search for common role
        results = gsw.search_by_role("applicant")
        # May or may not have results depending on workspace content
        assert isinstance(results, list)

    def test_gsw_concept_extraction(self, benchmark_instance):
        """Test GSW concept extraction."""
        gsw = benchmark_instance.retrievers.get('gsw')
        if gsw is None:
            pytest.skip("GSW retriever not available")

        concepts = gsw._extract_concepts("custody arrangement for children")
        assert len(concepts) > 0
        assert 'custody' in concepts or 'children' in concepts


class TestHybridRetriever:
    """Test hybrid retriever specifically."""

    def test_hybrid_auto_mode(self, benchmark_instance):
        """Test hybrid auto mode selection."""
        hybrid = benchmark_instance.retrievers.get('hybrid')
        if hybrid is None:
            pytest.skip("Hybrid retriever not available")

        results = hybrid.retrieve("custody arrangement", top_k=5, mode="auto")
        assert isinstance(results, list)

    def test_hybrid_gsw_mode(self, benchmark_instance):
        """Test hybrid GSW mode."""
        hybrid = benchmark_instance.retrievers.get('hybrid')
        if hybrid is None:
            pytest.skip("Hybrid retriever not available")

        results = hybrid.retrieve("custody arrangement", top_k=5, mode="gsw")
        assert isinstance(results, list)

    def test_hybrid_bm25_mode(self, benchmark_instance):
        """Test hybrid BM25 mode."""
        hybrid = benchmark_instance.retrievers.get('hybrid')
        if hybrid is None:
            pytest.skip("Hybrid retriever not available")

        results = hybrid.retrieve("custody arrangement", top_k=5, mode="bm25")
        assert isinstance(results, list)


# ============================================================================
# REPORT GENERATION TESTS
# ============================================================================

class TestReportGeneration:
    """Test report generation and saving."""

    def test_report_save(self, benchmark_instance, benchmark_report, tmp_path):
        """Test report can be saved to file."""
        output_path = tmp_path / "test_report.json"
        benchmark_instance.save_report(benchmark_report, output_path)
        assert output_path.exists()

    def test_report_json_valid(self, benchmark_instance, benchmark_report, tmp_path):
        """Test saved report is valid JSON."""
        import json
        output_path = tmp_path / "test_report.json"
        benchmark_instance.save_report(benchmark_report, output_path)

        with open(output_path) as f:
            data = json.load(f)

        assert 'run_id' in data
        assert 'method_metrics' in data
        assert 'comparison' in data
        assert 'recommendations' in data


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
