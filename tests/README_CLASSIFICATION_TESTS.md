# Australian Legal Corpus Classification System - Test Suite

Comprehensive integration test suite for validating the classification pipeline, domain coverage, court hierarchy, citation extraction, and performance benchmarks.

## Test Files Overview

### 1. test_classification_integration.py
**Purpose**: End-to-end integration tests for the full classification pipeline

**Coverage**:
- Complete classification flow from raw documents to structured output
- Multi-domain detection with confidence scoring
- All 10 BOOST factors validation
- Citation extraction integration
- Real Australian legal document samples (Family Law, Criminal Law, Migration, Employment)
- Edge case handling

**Key Test Classes**:
- `TestFullClassificationPipeline`: Complete pipeline validation
- `TestBOOSTScoring`: Individual BOOST factor tests (1-10)
- `TestCitationIntegration`: Citation extraction with classification
- `TestSerializationAndOutput`: Output format validation
- `TestEdgeCases`: Error handling and edge cases

**Sample Documents Include**:
- Family law property settlement decisions
- Criminal appeal decisions (R v cases)
- Migration/administrative tribunal decisions
- Employment/Fair Work Commission decisions
- Multi-domain cases spanning multiple areas of law

### 2. test_domain_coverage.py
**Purpose**: Validate classification accuracy across all major legal domains

**Coverage**:
- Employment Law classification
- Administrative Law classification
- Criminal Law classification
- Family Law classification
- Commercial/Corporate Law classification
- Property Law classification
- Constitutional Law classification
- Taxation Law classification
- Environmental Law classification
- Intellectual Property Law classification
- Torts Law classification

**Key Test Classes**:
- One test class per major domain (11 classes)
- `TestDomainCoverageCompleteness`: Overall coverage validation

**Features**:
- Real Australian case samples for each domain
- Legislation extraction validation
- Court code and domain hint verification
- Confidence score validation
- Ensures no major domains are missing

### 3. test_court_hierarchy_integration.py
**Purpose**: Validate all 80 court codes and hierarchy relationships

**Coverage**:
- All Australian court codes (Federal, State, Territory)
- Authority scoring across hierarchy levels
- Binding precedent logic
- Specialist court domain hints
- Jurisdiction mapping
- Citation extraction from court codes

**Key Test Classes**:
- `TestCourtCodeCoverage`: 75+ court codes validation
- `TestFederalCourts`: Federal court system
- `TestStateCourts`: All state/territory courts
- `TestSpecialistCourts`: Specialist courts (Family, Employment, Criminal, etc.)
- `TestStateTribunals`: Civil and Administrative Tribunals
- `TestAuthorityScoring`: Authority score validation
- `TestHierarchyLevels`: Hierarchy level assignment
- `TestBindingPrecedent`: Binding precedent logic
- `TestDomainHints`: Domain hint assignment
- `TestReportSeries`: Authorized report series metadata

**Court Coverage**:
- High Court of Australia (HCA)
- Federal Courts (FCA, FCAFC, FamCA, etc.)
- State Courts of Appeal (8 jurisdictions)
- State Supreme Courts (8 jurisdictions)
- District/County Courts (4 states)
- Local/Magistrates Courts (8 jurisdictions)
- Specialist Courts (Family, Employment, Criminal Appeal, Environment, etc.)
- Federal and State Tribunals (AAT, NCAT, VCAT, etc.)

### 4. test_citation_extraction.py
**Purpose**: Comprehensive citation extraction and parsing tests

**Coverage**:
- Medium neutral citation extraction ([2020] HCA 1)
- Authorized report citation extraction ((2020) 271 CLR 657)
- Legislation citation extraction (Fair Work Act 2009 (Cth))
- Section/subsection parsing (s 79, s 51(xxvi), s 79(1)(a))
- Citation type detection
- Edge cases and malformed citations
- Performance with large documents

**Key Test Classes**:
- `TestMediumNeutralExtraction`: [YYYY] COURT NUM format
- `TestAuthorizedReportExtraction`: (YEAR) VOL REPORT PAGE format
- `TestLegislationExtraction`: Act/Regulation/Rules extraction
- `TestSectionParsing`: Section and subsection parsing
- `TestCitationTypeDetection`: Automatic type detection
- `TestEdgeCasesAndMalformed`: Error handling
- `TestCitationClassificationIntegration`: Integration with classifier
- `TestCitationExtractionPerformance`: Performance tests

**Citation Formats Tested**:
- Medium Neutral: [2020] HCA 1, [2021] NSWCA 50
- Authorized Reports: (2020) 271 CLR 657, (2012) 247 CLR 108
- Legislation: Fair Work Act 2009 (Cth), Crimes Act 1900 (NSW)
- Sections: s 79, s 51(xxvi), s 79(1)(a), reg 4.12

### 5. benchmarks/classification_benchmark.py
**Purpose**: Performance benchmarking and scalability testing

**Coverage**:
- Classification speed (documents per second)
- Memory usage during classification
- Throughput under load
- Performance across document types
- Consistency and variance testing
- Scalability validation

**Key Test Classes**:
- `TestClassificationSpeed`: Speed tests for different document lengths
- `TestClassificationThroughput`: Batch processing throughput
- `TestClassificationConsistency`: Performance consistency
- `TestMemoryUsage`: Memory profiling (requires memory_profiler)

**Benchmark Scenarios**:
- Short documents (~500 words): Target >10 docs/sec
- Medium documents (~2000 words): Target >5 docs/sec
- Long documents (~5000 words): Target >2 docs/sec
- Legislation documents: Target >10 docs/sec
- Mixed document batches
- Large batches (500+ documents)

**Output**:
- Detailed performance metrics
- JSON results file (benchmark_results.json)
- Timing statistics (avg, median, std dev)
- Memory usage reports

## Running the Tests

### Run All Tests
```bash
# From project root
pytest tests/test_classification_integration.py -v
pytest tests/test_domain_coverage.py -v
pytest tests/test_court_hierarchy_integration.py -v
pytest tests/test_citation_extraction.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_classification_integration.py::TestFullClassificationPipeline -v
pytest tests/test_domain_coverage.py::TestEmploymentLawClassification -v
pytest tests/test_court_hierarchy_integration.py::TestAuthorityScoring -v
pytest tests/test_citation_extraction.py::TestMediumNeutralExtraction -v
```

### Run Specific Test
```bash
pytest tests/test_classification_integration.py::TestFullClassificationPipeline::test_family_law_full_pipeline -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src.ingestion --cov-report=html
```

### Run Benchmarks
```bash
# As pytest tests (shorter version)
pytest tests/benchmarks/classification_benchmark.py -v

# Standalone comprehensive benchmarks (takes longer)
python tests/benchmarks/classification_benchmark.py
```

### Run All Classification Tests
```bash
# Quick test suite
pytest tests/test_*.py -v --tb=short

# With coverage
pytest tests/test_*.py --cov=src.ingestion --cov-report=term-missing
```

## Test Data and Fixtures

### Document Fixtures
Each test file includes realistic Australian legal document fixtures:
- Real case citations and court codes
- Actual legislation references
- Authentic legal reasoning and analysis
- Proper citation formatting
- Multi-domain documents

### Parametrized Tests
Many tests use `@pytest.mark.parametrize` for comprehensive coverage:
- All states/territories
- All court types
- Multiple citation formats
- Various document lengths

## Expected Performance Targets

### Classification Speed
- Short documents (~500 words): >10 docs/sec
- Medium documents (~2000 words): >5 docs/sec
- Long documents (~5000 words): >2 docs/sec
- Legislation: >10 docs/sec

### Accuracy Targets
- Primary domain classification: >90% accuracy on clear samples
- Confidence scores: >0.2 for domain-specific documents
- BOOST scoring: All factors correctly applied
- Citation extraction: >95% recall for standard formats

### Coverage Targets
- Court codes: 75+ courts covered
- Legal domains: 11+ major domains
- Citation formats: 3+ types (medium neutral, authorized reports, legislation)
- Test coverage: >80% code coverage for classification modules

## Dependencies

### Required
- pytest
- Python 3.8+
- src.ingestion modules (EnhancedDomainClassifier, CitationExtractor, etc.)

### Optional
- memory_profiler (for memory benchmarks)
- pytest-cov (for coverage reports)
- pytest-benchmark (alternative benchmarking)

Install optional dependencies:
```bash
pip install memory-profiler pytest-cov pytest-benchmark
```

## Continuous Integration

These tests are designed for CI/CD pipelines:
- Fast execution (most tests < 1 second)
- No external dependencies (uses fixtures)
- Clear pass/fail criteria
- Detailed error messages
- JSON output for results tracking

## Troubleshooting

### Import Errors
If you get import errors, ensure the project root is in your Python path:
```python
import sys
sys.path.insert(0, '/path/to/project/root')
```

### Slow Tests
If tests are slow:
- Run specific test classes instead of all tests
- Use `-n auto` with pytest-xdist for parallel execution
- Skip benchmark tests for quick validation

### Memory Profiler Not Available
If memory_profiler is not installed, memory tests will be skipped automatically.
Install with: `pip install memory-profiler`

### Classification Config Not Found
Ensure the classification_config.py file exists and contains:
- CLASSIFICATION_MAP dictionary
- DOMAIN_MAPPING dictionary
- HIERARCHY_MAP dictionary

## Test Maintenance

### Adding New Tests
1. Follow existing test structure and naming conventions
2. Use descriptive test names: `test_<what>_<scenario>`
3. Include docstrings explaining what is tested
4. Use realistic Australian legal examples
5. Add parametrization for multiple cases

### Updating Fixtures
When updating document fixtures:
- Maintain realistic legal content
- Use actual Australian legislation and cases
- Include proper citations and court codes
- Test both positive and negative cases

### Performance Baselines
Update performance targets in benchmarks when:
- Classification algorithm improves
- New optimizations are added
- Hardware capabilities change

## Metrics and Reporting

### Test Metrics
- Total tests: 200+ individual test cases
- Test files: 5 comprehensive suites
- Domain coverage: 11+ major legal domains
- Court codes tested: 75+
- Citation formats: 3+ types

### Reports Generated
- pytest HTML reports
- Coverage reports (HTML/terminal)
- Benchmark JSON results
- Performance metrics

## Contact and Support

For issues with tests:
1. Check test output for specific error messages
2. Verify classification_config.py is up to date
3. Ensure all required modules are importable
4. Check that court_hierarchy.py has 75+ court codes

## Version History

- v2.0: Comprehensive integration test suite created
  - 200+ test cases across 5 test files
  - Full BOOST scoring validation
  - Complete court hierarchy coverage
  - Citation extraction tests
  - Performance benchmarks
