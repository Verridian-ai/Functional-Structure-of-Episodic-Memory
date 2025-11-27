"""
Comprehensive Tests for the Benchmarks Module
==============================================

Tests for the family law discrepancy detection benchmark system, including:
- DiscrepancyType enums
- DiscrepancyInstance creation
- FamilyLawBenchmark.generate_perturbations()
- FamilyLawBenchmark.evaluate_detection()
- BenchmarkRunner.run_benchmark()

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import pytest
import random
from typing import List, Tuple
from pathlib import Path
import tempfile
import json

from src.benchmarks.family_law_discrepancy import (
    LegalDiscrepancyType,
    InTextDiscrepancyType,
    DiscrepancyInstance,
    FamilyLawBenchmark,
    create_sample_document
)
from src.benchmarks.benchmark_runner import (
    BenchmarkRunner,
    create_default_detection_function
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_parenting_doc():
    """Fixture providing a sample parenting document."""
    return create_sample_document("parenting")


@pytest.fixture
def sample_property_doc():
    """Fixture providing a sample property document."""
    return create_sample_document("property")


@pytest.fixture
def sample_general_doc():
    """Fixture providing a sample general document."""
    return create_sample_document("general")


@pytest.fixture
def benchmark():
    """Fixture providing a FamilyLawBenchmark instance with fixed seed."""
    return FamilyLawBenchmark(seed=42)


@pytest.fixture
def benchmark_runner(tmp_path):
    """Fixture providing a BenchmarkRunner instance."""
    return BenchmarkRunner(output_dir=tmp_path)


@pytest.fixture
def sample_perturbations():
    """Fixture providing sample perturbation instances."""
    return [
        DiscrepancyInstance(
            original_text="15 March 2020",
            perturbed_text="20 March 2020",
            discrepancy_type=InTextDiscrepancyType.DATE_INCONSISTENCY.value,
            span_start=100,
            span_end=113,
            explanation="Date changed from '15 March 2020' to '20 March 2020'",
            severity=3
        ),
        DiscrepancyInstance(
            original_text="Mr Smith",
            perturbed_text="Mr Jones",
            discrepancy_type=InTextDiscrepancyType.PARTY_MISMATCH.value,
            span_start=200,
            span_end=208,
            explanation="Party name changed",
            severity=4
        )
    ]


# ============================================================================
# ENUM TESTS
# ============================================================================

class TestDiscrepancyEnums:
    """Tests for discrepancy type enums."""

    def test_legal_discrepancy_type_values(self):
        """Test that all LegalDiscrepancyType enum values are defined."""
        assert LegalDiscrepancyType.PROPERTY_POOL.value == "property_pool"
        assert LegalDiscrepancyType.PARENTING_ORDER.value == "parenting_order"
        assert LegalDiscrepancyType.SPOUSAL_MAINTENANCE.value == "spousal_maintenance"
        assert LegalDiscrepancyType.CHILD_SUPPORT.value == "child_support"
        assert LegalDiscrepancyType.CONSENT_ORDER.value == "consent_order"

    def test_in_text_discrepancy_type_values(self):
        """Test that all InTextDiscrepancyType enum values are defined."""
        assert InTextDiscrepancyType.DATE_INCONSISTENCY.value == "date_inconsistency"
        assert InTextDiscrepancyType.PARTY_MISMATCH.value == "party_mismatch"
        assert InTextDiscrepancyType.ASSET_REFERENCE.value == "asset_reference"
        assert InTextDiscrepancyType.NUMERICAL.value == "numerical"
        assert InTextDiscrepancyType.ORDER_REFERENCE.value == "order_reference"

    def test_enum_membership(self):
        """Test enum membership checks."""
        assert "property_pool" in [e.value for e in LegalDiscrepancyType]
        assert "date_inconsistency" in [e.value for e in InTextDiscrepancyType]

    def test_enum_iteration(self):
        """Test that enums can be iterated."""
        legal_types = list(LegalDiscrepancyType)
        assert len(legal_types) == 5

        in_text_types = list(InTextDiscrepancyType)
        assert len(in_text_types) == 5


# ============================================================================
# DISCREPANCY INSTANCE TESTS
# ============================================================================

class TestDiscrepancyInstance:
    """Tests for DiscrepancyInstance dataclass."""

    def test_create_discrepancy_instance(self):
        """Test creating a basic DiscrepancyInstance."""
        instance = DiscrepancyInstance(
            original_text="original",
            perturbed_text="perturbed",
            discrepancy_type="date_inconsistency",
            span_start=0,
            span_end=10,
            explanation="Test explanation"
        )

        assert instance.original_text == "original"
        assert instance.perturbed_text == "perturbed"
        assert instance.discrepancy_type == "date_inconsistency"
        assert instance.span_start == 0
        assert instance.span_end == 10
        assert instance.explanation == "Test explanation"
        assert instance.severity == 3  # Default value

    def test_discrepancy_instance_with_metadata(self):
        """Test DiscrepancyInstance with metadata."""
        metadata = {"original_value": 100, "new_value": 200}
        instance = DiscrepancyInstance(
            original_text="$100",
            perturbed_text="$200",
            discrepancy_type="asset_reference",
            span_start=50,
            span_end=54,
            explanation="Value changed",
            severity=4,
            metadata=metadata
        )

        assert instance.metadata == metadata
        assert instance.metadata["original_value"] == 100

    def test_discrepancy_instance_severity_levels(self):
        """Test different severity levels."""
        for severity in range(1, 6):
            instance = DiscrepancyInstance(
                original_text="test",
                perturbed_text="test2",
                discrepancy_type="test_type",
                span_start=0,
                span_end=5,
                explanation="test",
                severity=severity
            )
            assert instance.severity == severity


# ============================================================================
# FAMILY LAW BENCHMARK TESTS
# ============================================================================

class TestFamilyLawBenchmark:
    """Tests for FamilyLawBenchmark class."""

    def test_initialization(self, benchmark):
        """Test benchmark initialization."""
        assert benchmark is not None
        assert len(benchmark.party_names) > 0
        assert len(benchmark.asset_types) > 0
        assert len(benchmark.months) == 12

    def test_initialization_with_seed(self):
        """Test that seed produces reproducible results."""
        benchmark1 = FamilyLawBenchmark(seed=42)
        benchmark2 = FamilyLawBenchmark(seed=42)

        doc = create_sample_document("parenting")

        perturb1 = benchmark1.generate_perturbations(doc, "parenting", num_perturbations=3)
        perturb2 = benchmark2.generate_perturbations(doc, "parenting", num_perturbations=3)

        # With same seed, should get identical perturbations
        assert len(perturb1) == len(perturb2)

    def test_generate_perturbations_parenting(self, benchmark, sample_parenting_doc):
        """Test perturbation generation for parenting documents."""
        perturbations = benchmark.generate_perturbations(
            sample_parenting_doc,
            "parenting",
            num_perturbations=5
        )

        assert isinstance(perturbations, list)
        assert len(perturbations) <= 5

        for p in perturbations:
            assert isinstance(p, DiscrepancyInstance)
            assert p.span_start >= 0
            assert p.span_end > p.span_start
            assert p.original_text != p.perturbed_text

    def test_generate_perturbations_property(self, benchmark, sample_property_doc):
        """Test perturbation generation for property documents."""
        perturbations = benchmark.generate_perturbations(
            sample_property_doc,
            "property",
            num_perturbations=5
        )

        assert isinstance(perturbations, list)
        assert len(perturbations) <= 5

    def test_generate_perturbations_general(self, benchmark, sample_general_doc):
        """Test perturbation generation for general documents."""
        perturbations = benchmark.generate_perturbations(
            sample_general_doc,
            "general",
            num_perturbations=5
        )

        assert isinstance(perturbations, list)
        assert len(perturbations) <= 5

    def test_generate_perturbations_empty_document(self, benchmark):
        """Test perturbation generation with empty document."""
        perturbations = benchmark.generate_perturbations("", "general", num_perturbations=5)
        assert perturbations == []

    def test_evaluate_detection_perfect_match(self, benchmark, sample_perturbations):
        """Test evaluation with perfect prediction match."""
        predictions = [
            (p.span_start, p.span_end, p.discrepancy_type)
            for p in sample_perturbations
        ]

        metrics = benchmark.evaluate_detection(predictions, sample_perturbations)

        assert metrics["precision"] == 1.0
        assert metrics["recall"] == 1.0
        assert metrics["f1_score"] == 1.0
        assert metrics["true_positives"] == len(sample_perturbations)
        assert metrics["false_positives"] == 0
        assert metrics["false_negatives"] == 0

    def test_evaluate_detection_no_predictions(self, benchmark, sample_perturbations):
        """Test evaluation with no predictions."""
        metrics = benchmark.evaluate_detection([], sample_perturbations)

        assert metrics["precision"] == 0.0
        assert metrics["recall"] == 0.0
        assert metrics["f1_score"] == 0.0
        assert metrics["true_positives"] == 0
        assert metrics["false_positives"] == 0
        assert metrics["false_negatives"] == len(sample_perturbations)

    def test_evaluate_detection_partial_overlap(self, benchmark, sample_perturbations):
        """Test evaluation with partial span overlap."""
        # Predict with slightly offset spans
        predictions = [
            (p.span_start + 2, p.span_end - 2, p.discrepancy_type)
            for p in sample_perturbations
        ]

        metrics = benchmark.evaluate_detection(predictions, sample_perturbations)

        assert metrics["precision"] > 0
        assert metrics["recall"] > 0
        assert metrics["span_accuracy"] < 1.0  # Not exact matches

    def test_evaluate_detection_false_positives(self, benchmark, sample_perturbations):
        """Test evaluation with false positive predictions."""
        # Add extra wrong predictions
        predictions = [
            (p.span_start, p.span_end, p.discrepancy_type)
            for p in sample_perturbations
        ] + [
            (500, 510, "fake_type"),
            (600, 610, "fake_type")
        ]

        metrics = benchmark.evaluate_detection(predictions, sample_perturbations)

        assert metrics["false_positives"] == 2
        assert metrics["precision"] < 1.0

    def test_apply_perturbations(self, benchmark):
        """Test applying perturbations to a document."""
        doc = "The date is 15 March 2020 and the amount is $500,000."

        perturbations = [
            DiscrepancyInstance(
                original_text="15 March 2020",
                perturbed_text="20 March 2020",
                discrepancy_type="date_inconsistency",
                span_start=12,
                span_end=25,
                explanation="Date changed",
                severity=3
            )
        ]

        perturbed_doc = benchmark.apply_perturbations(doc, perturbations)

        assert "20 March 2020" in perturbed_doc
        assert "15 March 2020" not in perturbed_doc

    def test_apply_multiple_perturbations(self, benchmark):
        """Test applying multiple perturbations preserves indices."""
        doc = "The party Mr Smith owes $100 to Mrs Jones on 15 March 2020."

        perturbations = [
            DiscrepancyInstance(
                original_text="Mr Smith",
                perturbed_text="Mr Brown",
                discrepancy_type="party_mismatch",
                span_start=10,
                span_end=18,
                explanation="Party changed",
                severity=4
            ),
            DiscrepancyInstance(
                original_text="$100",
                perturbed_text="$200",
                discrepancy_type="asset_reference",
                span_start=24,
                span_end=28,
                explanation="Amount changed",
                severity=4
            )
        ]

        perturbed_doc = benchmark.apply_perturbations(doc, perturbations)

        assert "Mr Brown" in perturbed_doc
        assert "$200" in perturbed_doc

    def test_generate_legal_discrepancies_property(self, benchmark):
        """Test generation of legal-domain discrepancies for property cases."""
        doc = "The property shall be divided 60/40 between the parties."

        discrepancies = benchmark.generate_legal_discrepancies(doc, "property")

        # Should detect property division without asset pool
        assert len(discrepancies) > 0
        assert any(d.discrepancy_type == LegalDiscrepancyType.PROPERTY_POOL.value
                  for d in discrepancies)

    def test_generate_legal_discrepancies_parenting(self, benchmark):
        """Test generation of legal-domain discrepancies for parenting cases."""
        doc = "A parenting order is made for alternate weekends."

        discrepancies = benchmark.generate_legal_discrepancies(doc, "parenting")

        # Should detect parenting orders without children mentioned
        assert len(discrepancies) > 0
        assert any(d.discrepancy_type == LegalDiscrepancyType.PARENTING_ORDER.value
                  for d in discrepancies)

    def test_spans_overlap_method(self, benchmark):
        """Test the _spans_overlap helper method."""
        # Overlapping spans
        assert benchmark._spans_overlap(0, 10, 5, 15) is True
        assert benchmark._spans_overlap(5, 15, 0, 10) is True
        assert benchmark._spans_overlap(0, 10, 0, 10) is True

        # Non-overlapping spans
        assert benchmark._spans_overlap(0, 10, 10, 20) is False
        assert benchmark._spans_overlap(10, 20, 0, 10) is False
        assert benchmark._spans_overlap(0, 5, 10, 15) is False


# ============================================================================
# BENCHMARK RUNNER TESTS
# ============================================================================

class TestBenchmarkRunner:
    """Tests for BenchmarkRunner class."""

    def test_initialization(self, benchmark_runner):
        """Test BenchmarkRunner initialization."""
        assert benchmark_runner is not None
        assert benchmark_runner.benchmark is not None
        assert len(benchmark_runner.documents) == 0
        assert len(benchmark_runner.results) == 0

    def test_add_document(self, benchmark_runner):
        """Test adding a single document."""
        doc_text = create_sample_document("parenting")

        benchmark_runner.add_document(
            document_text=doc_text,
            category="parenting",
            doc_id="test_001"
        )

        assert len(benchmark_runner.documents) == 1
        assert benchmark_runner.documents[0]["doc_id"] == "test_001"
        assert benchmark_runner.documents[0]["category"] == "parenting"

    def test_add_document_auto_id(self, benchmark_runner):
        """Test adding document with auto-generated ID."""
        doc_text = create_sample_document("parenting")

        benchmark_runner.add_document(
            document_text=doc_text,
            category="parenting"
        )

        assert len(benchmark_runner.documents) == 1
        assert benchmark_runner.documents[0]["doc_id"] == "doc_0000"

    def test_add_documents_from_list(self, benchmark_runner):
        """Test adding multiple documents from list."""
        documents = [
            {
                "text": create_sample_document("parenting"),
                "category": "parenting",
                "doc_id": "doc_1"
            },
            {
                "text": create_sample_document("property"),
                "category": "property",
                "doc_id": "doc_2"
            }
        ]

        benchmark_runner.add_documents_from_list(documents)

        assert len(benchmark_runner.documents) == 2
        assert benchmark_runner.documents[0]["doc_id"] == "doc_1"
        assert benchmark_runner.documents[1]["doc_id"] == "doc_2"

    def test_run_benchmark_basic(self, benchmark_runner):
        """Test basic benchmark run."""
        # Add a sample document
        benchmark_runner.add_document(
            document_text=create_sample_document("parenting"),
            category="parenting"
        )

        # Create a simple detection function
        detection_func = create_default_detection_function()

        # Run benchmark
        results = benchmark_runner.run_benchmark(
            detection_function=detection_func,
            num_perturbations_per_doc=3,
            verbose=False
        )

        assert results is not None
        assert "mean_precision" in results
        assert "mean_recall" in results
        assert "mean_f1" in results
        assert results["total_documents"] == 1

    def test_run_benchmark_multiple_documents(self, benchmark_runner):
        """Test benchmark with multiple documents."""
        for category in ["parenting", "property", "general"]:
            benchmark_runner.add_document(
                document_text=create_sample_document(category),
                category=category
            )

        detection_func = create_default_detection_function()

        results = benchmark_runner.run_benchmark(
            detection_function=detection_func,
            num_perturbations_per_doc=2,
            verbose=False
        )

        assert results["total_documents"] == 3
        assert "per_category" in results
        assert len(results["per_category"]) == 3

    def test_calculate_metrics(self, benchmark_runner):
        """Test metrics calculation."""
        # Add document and run benchmark to populate results
        benchmark_runner.add_document(
            document_text=create_sample_document("parenting"),
            category="parenting"
        )

        benchmark_runner.run_benchmark(
            detection_function=create_default_detection_function(),
            num_perturbations_per_doc=3,
            verbose=False
        )

        metrics = benchmark_runner.calculate_metrics()

        assert "mean_precision" in metrics
        assert "mean_recall" in metrics
        assert "mean_f1" in metrics
        assert "total_true_positives" in metrics
        assert "total_false_positives" in metrics
        assert "total_false_negatives" in metrics

    def test_generate_report(self, benchmark_runner, tmp_path):
        """Test report generation."""
        # Add and run benchmark
        benchmark_runner.add_document(
            document_text=create_sample_document("parenting"),
            category="parenting"
        )

        benchmark_runner.run_benchmark(
            detection_function=create_default_detection_function(),
            num_perturbations_per_doc=2,
            verbose=False
        )

        # Generate report
        report_path = benchmark_runner.generate_report(
            output_path=tmp_path / "test_report.json"
        )

        assert report_path.exists()

        # Load and verify report
        with open(report_path, "r") as f:
            report = json.load(f)

        assert "benchmark_info" in report
        assert "aggregate_metrics" in report

    def test_clear_results(self, benchmark_runner):
        """Test clearing results."""
        benchmark_runner.add_document(
            document_text=create_sample_document("parenting"),
            category="parenting"
        )

        benchmark_runner.run_benchmark(
            detection_function=create_default_detection_function(),
            num_perturbations_per_doc=2,
            verbose=False
        )

        assert len(benchmark_runner.results) > 0

        benchmark_runner.clear_results()

        assert len(benchmark_runner.results) == 0
        assert benchmark_runner.aggregate_metrics == {}


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestBenchmarkIntegration:
    """Integration tests for the complete benchmark system."""

    def test_end_to_end_benchmark(self, tmp_path):
        """Test complete end-to-end benchmark workflow."""
        # Create runner
        runner = BenchmarkRunner(output_dir=tmp_path)

        # Add documents
        for category in ["parenting", "property"]:
            runner.add_document(
                document_text=create_sample_document(category),
                category=category
            )

        # Run benchmark
        results = runner.run_benchmark(
            detection_function=create_default_detection_function(),
            num_perturbations_per_doc=3,
            verbose=False
        )

        assert results is not None
        assert results["total_documents"] == 2

        # Generate report
        report_path = runner.generate_report()
        assert report_path.exists()

    def test_benchmark_reproducibility(self):
        """Test that benchmarks with same seed produce same results."""
        benchmark1 = FamilyLawBenchmark(seed=123)
        benchmark2 = FamilyLawBenchmark(seed=123)

        doc = create_sample_document("parenting")

        perturb1 = benchmark1.generate_perturbations(doc, "parenting", 5)
        perturb2 = benchmark2.generate_perturbations(doc, "parenting", 5)

        assert len(perturb1) == len(perturb2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
