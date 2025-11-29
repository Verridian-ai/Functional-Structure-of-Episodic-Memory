#!/usr/bin/env python3
"""
Run All Integration Tests
==========================

Convenience script to run all integration tests for the Verridian AI system.

Usage:
    python run_all_tests.py
"""
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('=' * 70)

    result = subprocess.run(cmd, cwd=Path(__file__).parent)

    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        return True
    else:
        print(f"❌ {description} - FAILED")
        return False

def main():
    """Run all test suites."""
    print("\n" + "=" * 70)
    print("VERRIDIAN AI - COMPREHENSIVE TEST SUITE")
    print("=" * 70)

    tests = [
        (
            ["python", "-m", "pytest", "tests/test_integration.py", "-v"],
            "Legal GSW Pipeline Integration Tests"
        ),
        (
            ["python", "tests/test_integration.py"],
            "Standalone Integration Tests"
        ),
    ]

    results = []
    for cmd, desc in tests:
        success = run_command(cmd, desc)
        results.append((desc, success))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    failed = sum(1 for _, success in results if not success)

    for desc, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {desc}")

    print(f"\nTotal: {passed} passed, {failed} failed out of {len(results)} test suites")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {failed} test suite(s) failed. Review output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
