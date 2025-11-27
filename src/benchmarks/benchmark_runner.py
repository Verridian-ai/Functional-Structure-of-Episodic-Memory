"""
Benchmark Runner for Discrepancy Detection
===========================================

Orchestrates benchmark evaluation across multiple documents and provides
comprehensive reporting on detection performance.

This module:
1. Runs benchmarks across document sets
2. Aggregates metrics across multiple runs
3. Generates detailed performance reports
4. Tracks performance over time

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Tuple
from collections import defaultdict
import statistics

from src.benchmarks.family_law_discrepancy import (
    FamilyLawBenchmark,
    DiscrepancyInstance,
    LegalDiscrepancyType,
    InTextDiscrepancyType,
    create_sample_document
)


# ============================================================================
# BENCHMARK RUNNER
# ============================================================================

class BenchmarkRunner:
    """
    Runs comprehensive benchmarking of discrepancy detection systems.

    This class orchestrates the full evaluation pipeline:
    1. Document loading and preprocessing
    2. Perturbation generation
    3. System evaluation
    4. Metrics calculation
    5. Report generation

    Example:
        >>> runner = BenchmarkRunner()
        >>> runner.add_documents(document_list)
        >>> results = runner.run_benchmark(detection_function)
        >>> runner.generate_report("results/benchmark_report.json")
    """

    def __init__(
        self,
        benchmark: Optional[FamilyLawBenchmark] = None,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize the benchmark runner.

        Args:
            benchmark: FamilyLawBenchmark instance (creates new if None)
            output_dir: Directory for saving results and reports
        """
        self.benchmark = benchmark or FamilyLawBenchmark()
        self.output_dir = output_dir or Path("data/benchmark_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Storage for benchmark runs
        self.documents: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []
        self.aggregate_metrics: Dict[str, Any] = {}

        # Timing information
        self.run_start_time: Optional[datetime] = None
        self.run_end_time: Optional[datetime] = None

    def add_document(
        self,
        document_text: str,
        category: str,
        doc_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a document to the benchmark set.

        Args:
            document_text: The document text
            category: Document category (parenting, property, general)
            doc_id: Unique document identifier (auto-generated if None)
            metadata: Additional document metadata
        """
        if doc_id is None:
            doc_id = f"doc_{len(self.documents):04d}"

        self.documents.append({
            "doc_id": doc_id,
            "text": document_text,
            "category": category,
            "metadata": metadata or {},
            "added_at": datetime.now().isoformat()
        })

    def add_documents_from_list(
        self,
        documents: List[Dict[str, Any]]
    ) -> None:
        """
        Add multiple documents from a list.

        Args:
            documents: List of document dictionaries with keys:
                       - text: document text
                       - category: document category
                       - doc_id (optional): document identifier
                       - metadata (optional): additional metadata
        """
        for doc in documents:
            self.add_document(
                document_text=doc["text"],
                category=doc["category"],
                doc_id=doc.get("doc_id"),
                metadata=doc.get("metadata")
            )

    def run_benchmark(
        self,
        detection_function: Callable[[str, List[DiscrepancyInstance]], List[Tuple[int, int, str]]],
        num_perturbations_per_doc: int = 5,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run the benchmark across all documents.

        Args:
            detection_function: Function that takes (document, ground_truth) and returns
                              predictions as List[(start, end, type)]
            num_perturbations_per_doc: Number of perturbations per document
            verbose: Whether to print progress information

        Returns:
            Dictionary containing aggregated benchmark results
        """
        self.run_start_time = datetime.now()
        self.results = []

        if verbose:
            print(f"[Benchmark Runner] Starting benchmark at {self.run_start_time}")
            print(f"[Benchmark Runner] Documents: {len(self.documents)}")
            print(f"[Benchmark Runner] Perturbations per doc: {num_perturbations_per_doc}")
            print("=" * 70)

        for i, doc in enumerate(self.documents):
            if verbose:
                print(f"\n[{i+1}/{len(self.documents)}] Processing: {doc['doc_id']}")

            # Generate perturbations
            perturbations = self.benchmark.generate_perturbations(
                document=doc["text"],
                category=doc["category"],
                num_perturbations=num_perturbations_per_doc
            )

            # Apply perturbations to create test document
            perturbed_text = self.benchmark.apply_perturbations(doc["text"], perturbations)

            if verbose:
                print(f"  Generated {len(perturbations)} perturbations")

            # Run detection
            start_time = time.time()
            try:
                predictions = detection_function(perturbed_text, perturbations)
            except Exception as e:
                if verbose:
                    print(f"  ERROR: Detection function failed: {e}")
                predictions = []

            detection_time = time.time() - start_time

            # Evaluate
            metrics = self.benchmark.evaluate_detection(predictions, perturbations)

            # Store results
            result = {
                "doc_id": doc["doc_id"],
                "category": doc["category"],
                "num_perturbations": len(perturbations),
                "num_predictions": len(predictions),
                "detection_time": detection_time,
                "metrics": metrics,
                "perturbations": [
                    {
                        "type": p.discrepancy_type,
                        "span": [p.span_start, p.span_end],
                        "severity": p.severity,
                        "explanation": p.explanation
                    }
                    for p in perturbations
                ],
                "timestamp": datetime.now().isoformat()
            }

            self.results.append(result)

            if verbose:
                print(f"  Predictions: {len(predictions)}")
                print(f"  Metrics: P={metrics['precision']:.3f}, R={metrics['recall']:.3f}, F1={metrics['f1_score']:.3f}")
                print(f"  Time: {detection_time:.3f}s")

        self.run_end_time = datetime.now()

        # Calculate aggregate metrics
        self.aggregate_metrics = self.calculate_metrics()

        if verbose:
            print("\n" + "=" * 70)
            print("[Benchmark Runner] Benchmark complete!")
            print(f"Total time: {(self.run_end_time - self.run_start_time).total_seconds():.2f}s")
            self._print_summary()

        return self.aggregate_metrics

    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate aggregate metrics across all benchmark runs.

        Returns:
            Dictionary containing aggregated metrics:
            - mean_precision, mean_recall, mean_f1
            - median_precision, median_recall, median_f1
            - std_precision, std_recall, std_f1
            - total_tp, total_fp, total_fn
            - per_category_metrics
            - per_discrepancy_type_metrics
        """
        if not self.results:
            return {}

        # Extract metric values
        precisions = [r["metrics"]["precision"] for r in self.results]
        recalls = [r["metrics"]["recall"] for r in self.results]
        f1_scores = [r["metrics"]["f1_score"] for r in self.results]
        span_accuracies = [r["metrics"]["span_accuracy"] for r in self.results]

        # Calculate aggregates
        aggregate = {
            "mean_precision": statistics.mean(precisions),
            "mean_recall": statistics.mean(recalls),
            "mean_f1": statistics.mean(f1_scores),
            "mean_span_accuracy": statistics.mean(span_accuracies),
            "median_precision": statistics.median(precisions),
            "median_recall": statistics.median(recalls),
            "median_f1": statistics.median(f1_scores),
            "median_span_accuracy": statistics.median(span_accuracies),
            "total_true_positives": sum(r["metrics"]["true_positives"] for r in self.results),
            "total_false_positives": sum(r["metrics"]["false_positives"] for r in self.results),
            "total_false_negatives": sum(r["metrics"]["false_negatives"] for r in self.results),
            "total_documents": len(self.results),
            "total_perturbations": sum(r["num_perturbations"] for r in self.results),
            "total_predictions": sum(r["num_predictions"] for r in self.results),
            "avg_detection_time": statistics.mean(r["detection_time"] for r in self.results),
        }

        # Add standard deviations if we have enough samples
        if len(precisions) > 1:
            aggregate["std_precision"] = statistics.stdev(precisions)
            aggregate["std_recall"] = statistics.stdev(recalls)
            aggregate["std_f1"] = statistics.stdev(f1_scores)
            aggregate["std_span_accuracy"] = statistics.stdev(span_accuracies)

        # Per-category breakdown
        category_metrics = self._calculate_category_metrics()
        aggregate["per_category"] = category_metrics

        # Per-discrepancy-type breakdown
        type_metrics = self._calculate_type_metrics()
        aggregate["per_discrepancy_type"] = type_metrics

        # Round all float values
        aggregate = self._round_metrics(aggregate)

        return aggregate

    def _calculate_category_metrics(self) -> Dict[str, Dict[str, float]]:
        """Calculate metrics broken down by document category."""
        category_results = defaultdict(list)

        for result in self.results:
            category_results[result["category"]].append(result)

        category_metrics = {}
        for category, results in category_results.items():
            precisions = [r["metrics"]["precision"] for r in results]
            recalls = [r["metrics"]["recall"] for r in results]
            f1_scores = [r["metrics"]["f1_score"] for r in results]

            category_metrics[category] = {
                "count": len(results),
                "mean_precision": statistics.mean(precisions) if precisions else 0.0,
                "mean_recall": statistics.mean(recalls) if recalls else 0.0,
                "mean_f1": statistics.mean(f1_scores) if f1_scores else 0.0,
                "total_perturbations": sum(r["num_perturbations"] for r in results),
            }

        return category_metrics

    def _calculate_type_metrics(self) -> Dict[str, Dict[str, int]]:
        """Calculate metrics broken down by discrepancy type."""
        type_counts = defaultdict(lambda: {"total": 0, "severity_sum": 0})

        for result in self.results:
            for perturb in result["perturbations"]:
                disc_type = perturb["type"]
                type_counts[disc_type]["total"] += 1
                type_counts[disc_type]["severity_sum"] += perturb["severity"]

        # Calculate average severity
        type_metrics = {}
        for disc_type, counts in type_counts.items():
            type_metrics[disc_type] = {
                "count": counts["total"],
                "avg_severity": counts["severity_sum"] / counts["total"] if counts["total"] > 0 else 0.0
            }

        return type_metrics

    def generate_report(
        self,
        output_path: Optional[Path] = None,
        include_details: bool = True
    ) -> Path:
        """
        Generate a comprehensive JSON report of benchmark results.

        Args:
            output_path: Path for the output file (auto-generated if None)
            include_details: Whether to include detailed per-document results

        Returns:
            Path to the generated report file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"benchmark_report_{timestamp}.json"

        report = {
            "benchmark_info": {
                "run_start": self.run_start_time.isoformat() if self.run_start_time else None,
                "run_end": self.run_end_time.isoformat() if self.run_end_time else None,
                "duration_seconds": (
                    (self.run_end_time - self.run_start_time).total_seconds()
                    if self.run_start_time and self.run_end_time
                    else None
                ),
                "total_documents": len(self.documents),
                "total_results": len(self.results)
            },
            "aggregate_metrics": self.aggregate_metrics,
        }

        if include_details:
            report["detailed_results"] = self.results
            report["documents"] = [
                {
                    "doc_id": doc["doc_id"],
                    "category": doc["category"],
                    "text_length": len(doc["text"]),
                    "metadata": doc.get("metadata", {})
                }
                for doc in self.documents
            ]

        # Write report
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n[Benchmark Runner] Report saved to: {output_path}")
        return output_path

    def _print_summary(self) -> None:
        """Print a summary of benchmark results to console."""
        if not self.aggregate_metrics:
            print("No metrics available.")
            return

        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)
        print(f"Total Documents: {self.aggregate_metrics['total_documents']}")
        print(f"Total Perturbations: {self.aggregate_metrics['total_perturbations']}")
        print(f"Total Predictions: {self.aggregate_metrics['total_predictions']}")
        print("\nAggregate Metrics:")
        print(f"  Mean Precision:  {self.aggregate_metrics['mean_precision']:.3f}")
        print(f"  Mean Recall:     {self.aggregate_metrics['mean_recall']:.3f}")
        print(f"  Mean F1 Score:   {self.aggregate_metrics['mean_f1']:.3f}")
        print(f"  Span Accuracy:   {self.aggregate_metrics['mean_span_accuracy']:.3f}")
        print("\nConfusion Matrix:")
        print(f"  True Positives:  {self.aggregate_metrics['total_true_positives']}")
        print(f"  False Positives: {self.aggregate_metrics['total_false_positives']}")
        print(f"  False Negatives: {self.aggregate_metrics['total_false_negatives']}")
        print("\nPer-Category Performance:")
        for category, metrics in self.aggregate_metrics.get("per_category", {}).items():
            print(f"  {category.capitalize()}:")
            print(f"    Documents: {metrics['count']}")
            print(f"    F1 Score:  {metrics['mean_f1']:.3f}")
        print("\nPer-Discrepancy-Type Counts:")
        for disc_type, metrics in self.aggregate_metrics.get("per_discrepancy_type", {}).items():
            print(f"  {disc_type}: {metrics['count']} (avg severity: {metrics['avg_severity']:.1f})")
        print("=" * 70)

    def _round_metrics(self, metrics: Dict[str, Any], decimals: int = 3) -> Dict[str, Any]:
        """Recursively round float values in metrics dictionary."""
        rounded = {}
        for key, value in metrics.items():
            if isinstance(value, float):
                rounded[key] = round(value, decimals)
            elif isinstance(value, dict):
                rounded[key] = self._round_metrics(value, decimals)
            else:
                rounded[key] = value
        return rounded

    def export_ground_truth(self, output_path: Path) -> None:
        """
        Export ground truth perturbations to a file for external evaluation.

        Args:
            output_path: Path for the output JSON file
        """
        ground_truth_data = []

        for doc, result in zip(self.documents, self.results):
            ground_truth_data.append({
                "doc_id": doc["doc_id"],
                "category": doc["category"],
                "perturbations": result["perturbations"]
            })

        with open(output_path, "w") as f:
            json.dump(ground_truth_data, f, indent=2)

        print(f"[Benchmark Runner] Ground truth exported to: {output_path}")

    def clear_results(self) -> None:
        """Clear all stored results and metrics."""
        self.results = []
        self.aggregate_metrics = {}
        self.run_start_time = None
        self.run_end_time = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_default_detection_function() -> Callable[[str, List[DiscrepancyInstance]], List[Tuple[int, int, str]]]:
    """
    Create a simple baseline detection function for testing.

    This is a naive implementation that randomly detects some perturbations.
    Replace with actual detection system for real benchmarking.

    Returns:
        Detection function that takes (document, ground_truth) and returns predictions
    """
    import random

    def baseline_detector(
        document: str,
        ground_truth: List[DiscrepancyInstance]
    ) -> List[Tuple[int, int, str]]:
        """Baseline detector that finds ~50% of perturbations randomly."""
        predictions = []

        for gt in ground_truth:
            # 50% chance of detection
            if random.random() < 0.5:
                # Add some noise to spans
                noise = random.randint(-5, 5)
                pred_start = max(0, gt.span_start + noise)
                pred_end = min(len(document), gt.span_end + noise)
                predictions.append((pred_start, pred_end, gt.discrepancy_type))

        return predictions

    return baseline_detector


def run_sample_benchmark() -> None:
    """Run a sample benchmark with synthetic documents."""
    print("Running sample benchmark...\n")

    # Create runner
    runner = BenchmarkRunner()

    # Add sample documents
    categories = ["parenting", "property", "general"]
    for i, category in enumerate(categories):
        doc_text = create_sample_document(category)
        runner.add_document(
            document_text=doc_text,
            category=category,
            doc_id=f"sample_{category}_{i}",
            metadata={"source": "synthetic", "sample": True}
        )

    # Run benchmark with baseline detector
    detection_func = create_default_detection_function()
    results = runner.run_benchmark(
        detection_function=detection_func,
        num_perturbations_per_doc=5,
        verbose=True
    )

    # Generate report
    report_path = runner.generate_report()
    print(f"\nBenchmark complete! Report saved to: {report_path}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Command-line interface for benchmark runner."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Family Law Discrepancy Detection Benchmark"
    )
    parser.add_argument(
        "--mode",
        choices=["sample", "custom"],
        default="sample",
        help="Run mode: 'sample' for demo, 'custom' for custom documents"
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to JSON file with documents (for custom mode)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/benchmark_results"),
        help="Output directory for results"
    )
    parser.add_argument(
        "--perturbations",
        type=int,
        default=5,
        help="Number of perturbations per document"
    )

    args = parser.parse_args()

    if args.mode == "sample":
        run_sample_benchmark()
    elif args.mode == "custom":
        if not args.input or not args.input.exists():
            print(f"Error: Input file not found: {args.input}")
            return

        # Load custom documents
        with open(args.input, "r") as f:
            documents = json.load(f)

        # Create runner
        runner = BenchmarkRunner(output_dir=args.output_dir)
        runner.add_documents_from_list(documents)

        # Run benchmark
        detection_func = create_default_detection_function()
        runner.run_benchmark(
            detection_function=detection_func,
            num_perturbations_per_doc=args.perturbations,
            verbose=True
        )

        # Generate report
        runner.generate_report()


if __name__ == "__main__":
    main()
