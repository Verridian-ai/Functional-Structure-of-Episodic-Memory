# Quick Start Guide - Classification Test Suite

## Installation

```bash
# Install required dependencies
pip install pytest pytest-cov

# Optional: for memory profiling
pip install memory-profiler
```

## Running Tests

### Option 1: Use the Test Runner (Recommended)

```bash
# Run all tests
python tests/run_classification_tests.py

# Run quick tests (no benchmarks)
python tests/run_classification_tests.py --quick

# Run with coverage
python tests/run_classification_tests.py --coverage

# Run specific suite
python tests/run_classification_tests.py --integration
python tests/run_classification_tests.py --domain
python tests/run_classification_tests.py --courts
python tests/run_classification_tests.py --citations
python tests/run_classification_tests.py --benchmarks
```

### Option 2: Use pytest directly

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_classification_integration.py -v
pytest tests/test_domain_coverage.py -v
pytest tests/test_court_hierarchy_integration.py -v
pytest tests/test_citation_extraction.py -v

# Specific test class
pytest tests/test_classification_integration.py::TestFullClassificationPipeline -v

# Specific test
pytest tests/test_classification_integration.py::TestFullClassificationPipeline::test_family_law_full_pipeline -v

# With coverage
pytest tests/ --cov=src.ingestion --cov-report=html
```

### Option 3: Run benchmarks standalone

```bash
# Comprehensive benchmarks (takes longer)
python tests/benchmarks/classification_benchmark.py

# Benchmark tests via pytest
pytest tests/benchmarks/classification_benchmark.py -v
```

## Understanding Test Results

### Success Output
```
==================== test session starts ====================
tests/test_classification_integration.py::TestFullClassificationPipeline::test_family_law_full_pipeline PASSED [100%]
==================== 200 passed in 45.2s ====================
```

### Failure Output
```
FAILED tests/test_classification_integration.py::TestFullClassificationPipeline::test_family_law_full_pipeline - AssertionError: Primary domain should be Family, got Unclassified
```

## Common Commands

```bash
# Quick validation (recommended for regular testing)
pytest tests/test_classification_integration.py -v --tb=short

# Full suite with coverage
pytest tests/ --cov=src.ingestion --cov-report=term-missing -v

# Only failed tests (after a failure)
pytest tests/ --lf -v

# Stop on first failure
pytest tests/ -x

# Run in parallel (requires pytest-xdist)
pytest tests/ -n auto

# Verbose with full output
pytest tests/ -vv -s
```

## Test Suite Structure

```
tests/
├── test_classification_integration.py   # Full pipeline tests (30KB, 50+ tests)
├── test_domain_coverage.py              # Domain-specific tests (32KB, 40+ tests)
├── test_court_hierarchy_integration.py  # Court codes & hierarchy (26KB, 60+ tests)
├── test_citation_extraction.py          # Citation parsing (25KB, 50+ tests)
├── benchmarks/
│   └── classification_benchmark.py      # Performance tests (25KB, 20+ tests)
├── conftest.py                          # Shared fixtures
├── run_classification_tests.py          # Test runner
├── README_CLASSIFICATION_TESTS.md       # Full documentation
├── TEST_SUITE_SUMMARY.md                # Overview
└── QUICK_START_GUIDE.md                 # This file
```

## What Each Test File Does

### test_classification_integration.py
Tests the **complete classification pipeline**:
- Full document classification flow
- All 10 BOOST factors
- Citation extraction integration
- Real legal document samples
- Edge cases and error handling

**Run when**: You want to validate the entire system works correctly.

### test_domain_coverage.py
Tests **domain classification accuracy**:
- 11 major legal domains
- Real case samples per domain
- Legislation extraction
- Court domain hints
- No domains overlooked

**Run when**: You want to verify all legal domains are correctly identified.

### test_court_hierarchy_integration.py
Tests **court codes and hierarchy**:
- 75+ court codes
- Authority scoring
- Binding precedent logic
- All jurisdictions
- Specialist courts

**Run when**: You want to verify court metadata and hierarchy relationships.

### test_citation_extraction.py
Tests **citation parsing**:
- Medium neutral citations
- Authorized reports
- Legislation references
- Section/subsection parsing
- Edge cases

**Run when**: You want to verify citation extraction works correctly.

### benchmarks/classification_benchmark.py
Tests **performance and speed**:
- Classification speed
- Memory usage
- Throughput under load
- Consistency
- Scalability

**Run when**: You want to measure system performance.

## Quick Troubleshooting

### Import Errors
```bash
# Ensure project root is in path
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
# Or on Windows:
set PYTHONPATH=%PYTHONPATH%;C:\path\to\project
```

### Slow Tests
```bash
# Run only fast tests
pytest tests/ -m "not slow" -v

# Skip benchmarks
python tests/run_classification_tests.py --quick
```

### Memory Profiler Not Found
```bash
# Install it (optional)
pip install memory-profiler

# Or skip memory tests (they auto-skip if not installed)
pytest tests/benchmarks/ -v
```

### Tests Taking Too Long
```bash
# Run in parallel (faster)
pip install pytest-xdist
pytest tests/ -n auto
```

## Expected Results

When everything works correctly:

```
======================== Test Summary ========================
test_classification_integration.py ... 50 passed
test_domain_coverage.py ............. 40 passed
test_court_hierarchy_integration.py . 60 passed
test_citation_extraction.py ......... 50 passed
======================== 200 passed in 45s ===================
```

## Performance Expectations

- **Total test time**: ~30-60 seconds (without benchmarks)
- **With benchmarks**: ~5-10 minutes
- **Individual tests**: <1 second each (usually <0.1s)
- **Classification speed**: >10 docs/sec for short documents

## Next Steps After Running Tests

1. **All tests pass**: Great! Your classification system is working correctly.

2. **Some tests fail**:
   - Read the error messages carefully
   - Check which domain/court/citation failed
   - Verify the classification_config.py is up to date
   - Review court_hierarchy.py has all court codes

3. **Performance below target**:
   - Run benchmarks to identify bottlenecks
   - Check if keyword cleaning is efficient
   - Consider optimizing regex patterns

4. **Coverage below 80%**:
   - Identify untested code paths
   - Add tests for edge cases
   - Test error handling

## Getting Help

1. **Read the full documentation**: README_CLASSIFICATION_TESTS.md
2. **Check test output**: Look for specific error messages
3. **Review fixtures**: Check conftest.py for shared test data
4. **Examine test code**: Tests are well-commented with docstrings

## Tips

- ✓ Run `--quick` mode during development
- ✓ Use `--coverage` to find gaps
- ✓ Run benchmarks after optimization
- ✓ Add `-v` for verbose output
- ✓ Use `--tb=short` for concise failures
- ✓ Run specific tests during debugging
- ✓ Check pytest.ini or setup.cfg for config

## One-Liners

```bash
# Most common: Quick validation
pytest tests/test_classification_integration.py -v

# Full validation with coverage
pytest tests/ --cov=src.ingestion --cov-report=html -v

# Performance check
python tests/benchmarks/classification_benchmark.py

# Everything
python tests/run_classification_tests.py --coverage --verbose
```

That's it! You're ready to test the Australian Legal Corpus Classification System.
