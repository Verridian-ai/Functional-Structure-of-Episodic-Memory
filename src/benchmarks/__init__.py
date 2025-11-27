"""
Benchmarks Module for Verridian AI
===================================

Provides benchmarking and evaluation tools for testing the legal AI system's
ability to detect discrepancies, inconsistencies, and errors in family law
documents.

This module includes:
- Discrepancy generation for family law documents
- Benchmark runner for evaluating detection performance
- Metrics calculation and reporting

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

from src.benchmarks.family_law_discrepancy import (
    LegalDiscrepancyType,
    InTextDiscrepancyType,
    DiscrepancyInstance,
    FamilyLawBenchmark
)
from src.benchmarks.benchmark_runner import (
    BenchmarkRunner
)

__all__ = [
    "LegalDiscrepancyType",
    "InTextDiscrepancyType",
    "DiscrepancyInstance",
    "FamilyLawBenchmark",
    "BenchmarkRunner"
]
