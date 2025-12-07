"""
Pytest Configuration and Shared Fixtures for Classification Tests

This file contains shared fixtures and configuration used across all test files.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "benchmark: marks tests as benchmarks"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# ============================================================================
# SHARED FIXTURES
# ============================================================================

@pytest.fixture(scope='session')
def project_root():
    """Return project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope='session')
def test_data_dir():
    """Return test data directory."""
    data_dir = PROJECT_ROOT / 'tests' / 'test_data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope='module')
def classifier():
    """
    Create a shared classifier instance for module.

    This fixture is module-scoped so the classifier is created once per
    test module, improving test performance.
    """
    from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier
    return EnhancedDomainClassifier()


@pytest.fixture
def sample_case_citation():
    """Sample case law citation."""
    return '[2020] HCA 1'


@pytest.fixture
def sample_legislation_citation():
    """Sample legislation citation."""
    return 'Fair Work Act 2009 (Cth)'


@pytest.fixture
def sample_authorized_report():
    """Sample authorized report citation."""
    return '(2020) 271 CLR 657'


# ============================================================================
# SHARED TEST DATA
# ============================================================================

@pytest.fixture
def court_codes_list():
    """Return list of all court codes for testing."""
    from src.ingestion.court_hierarchy import COURT_CODES
    return list(COURT_CODES.keys())


@pytest.fixture
def federal_courts():
    """Return list of federal court codes."""
    return ['HCA', 'FCAFC', 'FCA', 'FamCA', 'FamCAFC', 'FedCFamC', 'FCCA']


@pytest.fixture
def state_supreme_courts():
    """Return list of state supreme court codes."""
    return ['NSWSC', 'VSC', 'QSC', 'WASC', 'SASC', 'TASSC', 'ACTSC', 'NTSC']


@pytest.fixture
def state_appellate_courts():
    """Return list of state appellate court codes."""
    return ['NSWCA', 'VSCA', 'QCA', 'WASCA', 'SASCFC', 'TASFC', 'ACTCA', 'NTCA']


@pytest.fixture
def tribunals():
    """Return list of tribunal codes."""
    return ['AATA', 'AAT', 'NCAT', 'VCAT', 'QCAT', 'SAT', 'SACAT', 'TasCAT', 'ACAT', 'NTCAT']


# ============================================================================
# DOCUMENT FIXTURES
# ============================================================================

@pytest.fixture
def minimal_case_document():
    """Minimal case law document for testing."""
    return {
        'id': 'test_minimal',
        'citation': '[2020] NSWSC 100',
        'type': 'case_law',
        'text': 'This is a legal matter before the Court.'
    }


@pytest.fixture
def comprehensive_case_document():
    """Comprehensive case law document with all fields."""
    return {
        'id': 'test_comprehensive',
        'citation': '[2020] FamCA 100',
        'type': 'case_law',
        'jurisdiction': 'family',
        'text': '''
        FAMILY LAW - PROPERTY SETTLEMENT

        The parties were married for 15 years and have two children aged 12 and 10.
        The applicant wife seeks property settlement pursuant to s 79 of the
        Family Law Act 1975 (Cth).

        The property pool consists of the family home valued at $900,000,
        superannuation totaling $400,000, and savings of $75,000.

        Section 79 requires the Court to consider:
        1. The financial contributions of each party
        2. The non-financial contributions of each party
        3. The future needs of the parties under s 75(2)

        Cases cited:
        Stanford v Stanford (2012) 247 CLR 108

        Order: The property be divided 60% to the wife and 40% to the husband.
        ''',
        'date': '2020-06-15',
        'parties': ['Applicant Wife', 'Respondent Husband']
    }


@pytest.fixture
def legislation_document():
    """Legislation document for testing."""
    return {
        'id': 'test_legislation',
        'citation': 'Test Legislation Act 2020 (Cth)',
        'type': 'primary_legislation',
        'text': '''
        Test Legislation Act 2020

        An Act to provide for the regulation of test matters.

        Part 1 - Preliminary

        Section 1 - Short title
        This Act may be cited as the Test Legislation Act 2020.

        Section 2 - Commencement
        This Act commences on the day after it receives Royal Assent.

        Section 3 - Definitions
        In this Act:
        "prescribed" means prescribed by the regulations
        "the Minister" means the Minister administering this Act
        '''
    }


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def benchmark_timer():
    """Simple benchmark timer fixture."""
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return 0

    return Timer()


# ============================================================================
# PYTEST HOOKS
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark benchmark tests
        if "benchmark" in item.nodeid:
            item.add_marker(pytest.mark.benchmark)
            item.add_marker(pytest.mark.slow)

        # Mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Mark unit tests (by exclusion)
        if "integration" not in item.nodeid and "benchmark" not in item.nodeid:
            item.add_marker(pytest.mark.unit)


def pytest_report_header(config):
    """Add custom header to pytest output."""
    return [
        "Australian Legal Corpus Classification System - Test Suite",
        f"Project root: {PROJECT_ROOT}",
    ]
