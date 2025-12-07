#!/usr/bin/env python3
"""
Test Runner for Australian Legal Corpus Classification System

This script provides a convenient way to run the classification test suite
with various options and configurations.

Usage:
    python run_classification_tests.py                    # Run all tests
    python run_classification_tests.py --quick            # Run quick tests only
    python run_classification_tests.py --benchmarks       # Run benchmarks only
    python run_classification_tests.py --coverage         # Run with coverage
    python run_classification_tests.py --verbose          # Verbose output
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd: list, description: str) -> int:
    """
    Run a command and display results.

    Args:
        cmd: Command to run as list
        description: Description of what's being run

    Returns:
        Return code from command
    """
    print("\n" + "=" * 80)
    print(f"Running: {description}")
    print("=" * 80)
    print(f"Command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="Run Australian Legal Corpus Classification Tests"
    )

    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick tests only (no benchmarks)'
    )

    parser.add_argument(
        '--benchmarks',
        action='store_true',
        help='Run benchmarks only'
    )

    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run integration tests only'
    )

    parser.add_argument(
        '--domain',
        action='store_true',
        help='Run domain coverage tests only'
    )

    parser.add_argument(
        '--courts',
        action='store_true',
        help='Run court hierarchy tests only'
    )

    parser.add_argument(
        '--citations',
        action='store_true',
        help='Run citation extraction tests only'
    )

    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run tests with coverage report'
    )

    parser.add_argument(
        '--html',
        action='store_true',
        help='Generate HTML test report'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--markers',
        action='store_true',
        help='Show available pytest markers'
    )

    parser.add_argument(
        '--failures-only',
        action='store_true',
        help='Show only failures (short traceback)'
    )

    args = parser.parse_args()

    # Get test directory
    test_dir = Path(__file__).parent

    # Build pytest command
    pytest_cmd = ['pytest']

    # Determine which tests to run
    if args.benchmarks:
        pytest_cmd.append(str(test_dir / 'benchmarks' / 'classification_benchmark.py'))
    elif args.integration:
        pytest_cmd.append(str(test_dir / 'test_classification_integration.py'))
    elif args.domain:
        pytest_cmd.append(str(test_dir / 'test_domain_coverage.py'))
    elif args.courts:
        pytest_cmd.append(str(test_dir / 'test_court_hierarchy_integration.py'))
    elif args.citations:
        pytest_cmd.append(str(test_dir / 'test_citation_extraction.py'))
    elif args.quick:
        # Quick tests - exclude benchmarks
        pytest_cmd.extend([
            str(test_dir / 'test_classification_integration.py'),
            str(test_dir / 'test_domain_coverage.py'),
            str(test_dir / 'test_court_hierarchy_integration.py'),
            str(test_dir / 'test_citation_extraction.py'),
        ])
    else:
        # All tests including benchmarks
        pytest_cmd.append(str(test_dir))

    # Add verbosity
    if args.verbose:
        pytest_cmd.append('-v')
    else:
        pytest_cmd.append('-v')  # Always use some verbosity

    # Add coverage
    if args.coverage:
        pytest_cmd.extend([
            '--cov=src.ingestion',
            '--cov-report=term-missing',
            '--cov-report=html',
        ])

    # Add HTML report
    if args.html:
        pytest_cmd.extend([
            '--html=test_report.html',
            '--self-contained-html',
        ])

    # Show markers
    if args.markers:
        pytest_cmd.append('--markers')

    # Failures only
    if args.failures_only:
        pytest_cmd.append('--tb=short')
    else:
        pytest_cmd.append('--tb=auto')

    # Add color output
    pytest_cmd.append('--color=yes')

    # Run the tests
    return_code = run_command(pytest_cmd, "Classification Test Suite")

    # Print summary
    print("\n" + "=" * 80)
    if return_code == 0:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 80 + "\n")

    # Print additional info
    if args.coverage:
        print("Coverage report generated:")
        print(f"  HTML: {test_dir.parent / 'htmlcov' / 'index.html'}")
        print(f"  Terminal output above")

    if args.html:
        print(f"\nHTML test report: {test_dir / 'test_report.html'}")

    if args.benchmarks:
        print(f"\nBenchmark results: {test_dir / 'benchmarks' / 'benchmark_results.json'}")

    return return_code


if __name__ == '__main__':
    sys.exit(main())
