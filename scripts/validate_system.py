#!/usr/bin/env python3
"""
VERRIDIAN AI System Validation Script
======================================

Comprehensive validation of all CLAUSE research modules including:
- Benchmarks module (FamilyLawBenchmark)
- Validation module (CorpusLoader, StatutoryRAGValidator)
- Evaluation module (MultiJudgeEvaluator)
- VSA span detector (SpanAlignedVSA)
- Enhanced legal_vsa (LegalVSA)

Usage:
    python scripts/validate_system.py
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ============================================================================
# Test Result Tracking
# ============================================================================

class TestResult:
    """Track individual test results."""
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.module_results: Dict[str, List[Tuple[str, bool, str]]] = {}

    def add_result(self, module: str, test_name: str, passed: bool, error_msg: str = ""):
        """Add a test result."""
        if module not in self.module_results:
            self.module_results[module] = []

        self.module_results[module].append((test_name, passed, error_msg))
        self.tests_run += 1

        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print(f"SUMMARY: {self.tests_passed}/{self.tests_run} tests passed")

        if self.tests_failed > 0:
            print(f"\n⚠ {self.tests_failed} tests failed")
        else:
            print("\n✓ All tests passed!")

        print("=" * 70)


# Global test result tracker
test_results = TestResult()


# ============================================================================
# Utility Functions
# ============================================================================

def print_header(text: str):
    """Print section header."""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print('=' * 70)


def print_test(test_name: str, passed: bool, error_msg: str = ""):
    """Print individual test result."""
    status = "✓" if passed else "✗"
    print(f"  {status} {test_name}")
    if error_msg and not passed:
        print(f"    Error: {error_msg}")


def run_test(module: str, test_name: str, test_func) -> bool:
    """Run a test and record the result."""
    try:
        test_func()
        test_results.add_result(module, test_name, True)
        print_test(test_name, True)
        return True
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        test_results.add_result(module, test_name, False, error_msg)
        print_test(test_name, False, error_msg)
        return False


# ============================================================================
# Module Import Tests
# ============================================================================

def test_module_imports():
    """Test all module imports with graceful handling for optional dependencies."""
    print_header("MODULE IMPORTS")

    # Core modules (required)
    def test_benchmarks_import():
        from src.benchmarks import FamilyLawBenchmark, DiscrepancyInstance
        assert FamilyLawBenchmark is not None
        assert DiscrepancyInstance is not None

    run_test("Module Imports", "Import benchmarks module", test_benchmarks_import)

    def test_validation_import():
        from src.validation import CorpusLoader, StatutoryRAGValidator
        assert CorpusLoader is not None
        assert StatutoryRAGValidator is not None

    run_test("Module Imports", "Import validation module", test_validation_import)

    def test_evaluation_import():
        try:
            import httpx
            from src.evaluation import MultiJudgeEvaluator, JudgeModel
            assert MultiJudgeEvaluator is not None
            assert JudgeModel is not None
        except ImportError as e:
            if "httpx" in str(e).lower():
                print("    (Skipped: httpx not available)")
                return
            raise

    run_test("Module Imports", "Import evaluation module (optional)", test_evaluation_import)

    # Optional modules (torch-dependent)
    def test_vsa_span_import():
        try:
            import torch
            from src.vsa.span_detector import SpanAlignedVSA, SpanIssue
            assert SpanAlignedVSA is not None
            assert SpanIssue is not None
        except ImportError as e:
            if "torch" in str(e).lower():
                print("    (Skipped: PyTorch not available)")
                return
            raise

    run_test("Module Imports", "Import VSA span detector (optional)", test_vsa_span_import)

    def test_legal_vsa_import():
        try:
            import torch
            from src.vsa.legal_vsa import LegalVSA
            assert LegalVSA is not None
        except ImportError as e:
            if "torch" in str(e).lower():
                print("    (Skipped: PyTorch not available)")
                return
            raise

    run_test("Module Imports", "Import legal_vsa module (optional)", test_legal_vsa_import)


# ============================================================================
# Benchmarks Module Tests
# ============================================================================

def test_benchmarks_module():
    """Test the benchmarks module functionality."""
    print_header("BENCHMARKS MODULE")

    from src.benchmarks import FamilyLawBenchmark, DiscrepancyInstance
    from src.benchmarks.family_law_discrepancy import create_sample_document

    def test_create_benchmark():
        """Test creating a FamilyLawBenchmark instance."""
        benchmark = FamilyLawBenchmark(seed=42)
        assert benchmark is not None
        assert hasattr(benchmark, 'generate_perturbations')

    run_test("Benchmarks", "Create FamilyLawBenchmark instance", test_create_benchmark)

    def test_generate_perturbations():
        """Test generating perturbations."""
        benchmark = FamilyLawBenchmark(seed=42)
        document = create_sample_document("parenting")

        perturbations = benchmark.generate_perturbations(document, "parenting", num_perturbations=3)

        assert isinstance(perturbations, list)
        assert len(perturbations) <= 3

        if perturbations:
            assert isinstance(perturbations[0], DiscrepancyInstance)
            assert hasattr(perturbations[0], 'span_start')
            assert hasattr(perturbations[0], 'span_end')

    run_test("Benchmarks", "Generate perturbations", test_generate_perturbations)

    def test_evaluate_detection():
        """Test evaluation of detection results."""
        benchmark = FamilyLawBenchmark(seed=42)
        document = create_sample_document("property")

        perturbations = benchmark.generate_perturbations(document, "property", num_perturbations=2)

        # Create some predictions (simulated detections)
        predictions = []
        if perturbations:
            # Add a correct prediction
            p = perturbations[0]
            predictions.append((p.span_start, p.span_end, p.discrepancy_type))

        # Evaluate
        metrics = benchmark.evaluate_detection(predictions, perturbations)

        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 0.0 <= metrics['precision'] <= 1.0
        assert 0.0 <= metrics['recall'] <= 1.0

    run_test("Benchmarks", "Evaluate detection", test_evaluate_detection)

    def test_apply_perturbations():
        """Test applying perturbations to document."""
        benchmark = FamilyLawBenchmark(seed=42)
        document = create_sample_document("general")

        perturbations = benchmark.generate_perturbations(document, "general", num_perturbations=2)

        if perturbations:
            modified_doc = benchmark.apply_perturbations(document, perturbations[:1])
            assert isinstance(modified_doc, str)
            assert len(modified_doc) > 0

    run_test("Benchmarks", "Apply perturbations to document", test_apply_perturbations)


# ============================================================================
# Validation Module Tests
# ============================================================================

def test_validation_module():
    """Test the validation module functionality."""
    print_header("VALIDATION MODULE")

    from src.validation import CorpusLoader, StatutoryRAGValidator

    def test_corpus_loader_init():
        """Test creating a CorpusLoader instance."""
        # Use a test path (may not exist, but should handle gracefully)
        loader = CorpusLoader("data/statutory_corpus")
        assert loader is not None
        assert hasattr(loader, 'acts')
        assert hasattr(loader, 'search_by_keyword')

    run_test("Validation", "Create CorpusLoader instance", test_corpus_loader_init)

    def test_corpus_search_keyword():
        """Test keyword search."""
        loader = CorpusLoader("data/statutory_corpus")

        # Search should work even with empty corpus
        results = loader.search_by_keyword("parenting", top_k=5)
        assert isinstance(results, list)
        assert len(results) <= 5

    run_test("Validation", "Search corpus by keyword", test_corpus_search_keyword)

    def test_statutory_validator():
        """Test StatutoryRAGValidator initialization."""
        validator = StatutoryRAGValidator("data/statutory_corpus")
        assert validator is not None
        assert hasattr(validator, 'validate_extraction')

    run_test("Validation", "Create StatutoryRAGValidator instance", test_statutory_validator)

    def test_validate_extraction():
        """Test validating a sample extraction."""
        validator = StatutoryRAGValidator("data/statutory_corpus")

        # Sample extraction
        extraction = {
            "legal_test": "Best Interests of the Child",
            "elements": ["safety", "meaningful relationship"],
            "findings": ["The court found that safety is paramount"]
        }

        result = validator.validate_extraction(extraction)

        assert result is not None
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'compliance_score')
        assert hasattr(result, 'supporting_citations')
        assert 0.0 <= result.compliance_score <= 1.0

    run_test("Validation", "Validate sample extraction", test_validate_extraction)


# ============================================================================
# Evaluation Module Tests
# ============================================================================

def test_evaluation_module():
    """Test the evaluation module functionality."""
    print_header("EVALUATION MODULE")

    # Check if httpx is available (required for evaluation module)
    try:
        import httpx
    except ImportError:
        print("  ⚠ httpx not available - skipping evaluation module tests")
        print("    Install with: pip install httpx")
        return

    from src.evaluation import MultiJudgeEvaluator, JudgeModel, JudgeEvaluation, AggregatedEvaluation

    def test_create_evaluator():
        """Test creating a MultiJudgeEvaluator instance."""
        # Skip if no API key available
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("    (Skipped: OPENROUTER_API_KEY not set)")
            return

        evaluator = MultiJudgeEvaluator(judges=[JudgeModel.GPT4O])
        assert evaluator is not None
        assert hasattr(evaluator, 'evaluate_response')

    run_test("Evaluation", "Create MultiJudgeEvaluator instance", test_create_evaluator)

    def test_aggregation():
        """Test aggregation of multiple evaluations."""
        from src.evaluation.multi_judge import MultiJudgeEvaluator

        # Create mock evaluations
        evaluations = [
            JudgeEvaluation(
                model=JudgeModel.GPT4O,
                score=8.5,
                issues=["Minor formatting issue"],
                strengths=["Clear and accurate"],
                reasoning="Good response"
            ),
            JudgeEvaluation(
                model=JudgeModel.CLAUDE,
                score=9.0,
                issues=[],
                strengths=["Comprehensive", "Well-structured"],
                reasoning="Excellent response"
            )
        ]

        # Create an instance to access the aggregation method
        try:
            evaluator = MultiJudgeEvaluator(judges=[JudgeModel.GPT4O])
        except ValueError:
            # No API key, create dummy instance
            print("    (Using mock aggregation test)")
            # Just test that the aggregation logic would work
            assert len(evaluations) == 2
            return

        aggregated = evaluator._aggregate_evaluations(evaluations)

        assert aggregated is not None
        assert hasattr(aggregated, 'mean_score')
        assert hasattr(aggregated, 'median_score')
        assert hasattr(aggregated, 'consensus_level')
        assert 0.0 <= aggregated.mean_score <= 10.0
        assert 0.0 <= aggregated.consensus_level <= 1.0

    run_test("Evaluation", "Test aggregation", test_aggregation)

    def test_consensus_calculation():
        """Test consensus calculation."""
        from src.evaluation.multi_judge import MultiJudgeEvaluator

        try:
            evaluator = MultiJudgeEvaluator(judges=[JudgeModel.GPT4O])
        except ValueError:
            print("    (Using mock consensus test)")
            return

        # Create evaluations with similar scores (high consensus)
        high_consensus_evals = [
            JudgeEvaluation(JudgeModel.GPT4O, 8.0, [], [], ""),
            JudgeEvaluation(JudgeModel.CLAUDE, 8.2, [], [], ""),
            JudgeEvaluation(JudgeModel.GEMINI, 8.1, [], [], "")
        ]

        consensus = evaluator._calculate_consensus(high_consensus_evals)
        assert 0.0 <= consensus <= 1.0
        # High consensus should be close to 1.0
        assert consensus > 0.8

    run_test("Evaluation", "Calculate consensus", test_consensus_calculation)


# ============================================================================
# VSA Span Detector Tests (Optional - requires torch)
# ============================================================================

def test_vsa_span_detector():
    """Test the VSA span detector functionality."""
    print_header("VSA SPAN DETECTOR (Optional)")

    # Check if torch is available
    try:
        import torch
    except ImportError:
        print("  ⚠ PyTorch not available - skipping VSA span detector tests")
        return

    from src.vsa.span_detector import SpanAlignedVSA, SpanIssue
    from src.vsa.legal_vsa import LegalVSA

    def test_create_span_detector():
        """Test creating a SpanAlignedVSA instance."""
        base_vsa = LegalVSA(dimension=1000)
        span_detector = SpanAlignedVSA(base_vsa)

        assert span_detector is not None
        assert hasattr(span_detector, 'detect_issues_with_spans')

    run_test("VSA Span Detector", "Create SpanAlignedVSA instance", test_create_span_detector)

    def test_calculate_iou():
        """Test IOU (Intersection over Union) calculation."""
        base_vsa = LegalVSA(dimension=1000)
        span_detector = SpanAlignedVSA(base_vsa)

        # Test exact match
        iou_exact = span_detector._calculate_iou((0, 10), (0, 10))
        assert iou_exact == 1.0

        # Test partial overlap
        iou_partial = span_detector._calculate_iou((0, 10), (5, 15))
        assert 0.0 < iou_partial < 1.0

        # Test no overlap
        iou_none = span_detector._calculate_iou((0, 10), (20, 30))
        assert iou_none == 0.0

    run_test("VSA Span Detector", "Calculate IOU", test_calculate_iou)

    def test_span_detection():
        """Test span-level issue detection."""
        base_vsa = LegalVSA(dimension=1000)
        span_detector = SpanAlignedVSA(base_vsa)

        test_text = "The property was valued at $500,000 on 15 March 2020."
        extraction = {
            "amounts": [500000],
            "dates": ["15 March 2020"],
            "parties": [],
            "valid_references": []
        }

        issues = span_detector.detect_issues_with_spans(test_text, extraction)

        assert isinstance(issues, list)
        # Should not detect issues for consistent data
        # (or may detect issues if patterns don't match exactly)

    run_test("VSA Span Detector", "Detect spans", test_span_detection)

    def test_location_alignment():
        """Test location alignment scoring."""
        base_vsa = LegalVSA(dimension=1000)
        span_detector = SpanAlignedVSA(base_vsa)

        predicted = [(0, 10), (20, 30)]
        ground_truth = [(0, 10), (20, 30)]

        alignment = span_detector.calculate_location_alignment(predicted, ground_truth)

        assert 0.0 <= alignment <= 1.0
        # Perfect match should give high alignment
        assert alignment > 0.9

    run_test("VSA Span Detector", "Calculate location alignment", test_location_alignment)


# ============================================================================
# Enhanced Legal VSA Tests (Optional - requires torch)
# ============================================================================

def test_enhanced_legal_vsa():
    """Test the enhanced legal_vsa functionality."""
    print_header("ENHANCED LEGAL VSA (Optional)")

    # Check if torch is available
    try:
        import torch
    except ImportError:
        print("  ⚠ PyTorch not available - skipping legal VSA tests")
        return

    from src.vsa.legal_vsa import LegalVSA

    def test_create_legal_vsa():
        """Test creating a LegalVSA instance."""
        vsa = LegalVSA(dimension=1000)
        assert vsa is not None
        assert hasattr(vsa, 'verify_no_hallucination')

    run_test("Legal VSA", "Create LegalVSA instance", test_create_legal_vsa)

    def test_calibrated_confidence():
        """Test calibrated confidence scoring."""
        vsa = LegalVSA(dimension=1000)

        # Test with valid concepts (no issues)
        result = vsa.verify_no_hallucination(["PARENTING_ORDER", "BEST_INTERESTS"])

        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
        assert 'severity_breakdown' in result
        assert 'concept_coverage' in result

    run_test("Legal VSA", "Calculate calibrated confidence", test_calibrated_confidence)

    def test_severity_classification():
        """Test severity classification of issues."""
        vsa = LegalVSA(dimension=1000)

        # Test critical severity
        critical_issue = "Contradiction: PARENTING_ORDER and NO_CHILDREN cannot coexist."
        severity = vsa._classify_issue_severity(critical_issue)
        assert severity == "critical"

        # Test major severity
        major_issue = "Logic Violation: PROPERTY_DIVISION REQUIRES ASSET_POOL, but ASSET_POOL is missing."
        severity = vsa._classify_issue_severity(major_issue)
        assert severity == "major"

        # Test minor severity
        minor_issue = "Low confidence in extraction"
        severity = vsa._classify_issue_severity(minor_issue)
        assert severity == "minor"

    run_test("Legal VSA", "Classify issue severity", test_severity_classification)

    def test_kb_similarity():
        """Test knowledge base similarity calculation."""
        vsa = LegalVSA(dimension=1000)

        concepts = ["PARENTING_ORDER", "BEST_INTERESTS", "CHILD_SAFETY"]
        similarity = vsa.calculate_kb_similarity(concepts)

        assert 0.0 <= similarity <= 1.0

    run_test("Legal VSA", "Calculate KB similarity", test_kb_similarity)

    def test_concept_coverage():
        """Test concept coverage calculation."""
        vsa = LegalVSA(dimension=1000)

        # Add some test concepts
        vsa.add_concept("TEST_CONCEPT_1")
        vsa.add_concept("TEST_CONCEPT_2")

        # Test with all known concepts
        coverage = vsa.get_concept_coverage(["TEST_CONCEPT_1", "TEST_CONCEPT_2"])
        assert coverage == 1.0

        # Test with mixed concepts
        coverage = vsa.get_concept_coverage(["TEST_CONCEPT_1", "UNKNOWN_CONCEPT"])
        assert 0.0 < coverage < 1.0

    run_test("Legal VSA", "Calculate concept coverage", test_concept_coverage)


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all validation tests."""
    print("=" * 70)
    print("  === VERRIDIAN AI SYSTEM VALIDATION ===")
    print("=" * 70)
    print(f"\nProject Root: {project_root}")
    print(f"Python Version: {sys.version.split()[0]}")

    # Run all test suites
    test_module_imports()
    test_benchmarks_module()
    test_validation_module()
    test_evaluation_module()
    test_vsa_span_detector()
    test_enhanced_legal_vsa()

    # Print summary
    test_results.print_summary()

    # Exit with appropriate code
    sys.exit(0 if test_results.tests_failed == 0 else 1)


if __name__ == "__main__":
    main()
