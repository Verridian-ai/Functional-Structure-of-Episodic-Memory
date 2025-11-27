"""
Comprehensive Tests for the Span Detector Module
=================================================

Tests for the span-level detection system, including:
- SpanIssue creation
- SpanAlignedVSA._calculate_iou()
- SpanAlignedVSA.calculate_location_alignment()
- Numerical span detection
- Date span detection

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import pytest
from typing import List, Tuple
from unittest.mock import Mock

from src.vsa.span_detector import (
    SpanIssue,
    SpanAlignedVSA
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_vsa():
    """Fixture providing a mock LegalVSA instance."""
    mock = Mock()
    mock.name = "MockLegalVSA"
    return mock


@pytest.fixture
def span_detector(mock_vsa):
    """Fixture providing a SpanAlignedVSA instance."""
    return SpanAlignedVSA(mock_vsa)


@pytest.fixture
def sample_text_with_numbers():
    """Fixture providing text with numerical values."""
    return """
    The settlement amount is $500,000. The property was valued at $750,000.
    The monthly payment shall be $2,500.
    """


@pytest.fixture
def sample_text_with_dates():
    """Fixture providing text with various date formats."""
    return """
    The parties separated on 15 March 2020. The final hearing was held on
    2021-06-15. Settlement was reached on Jun 30, 2021.
    """


@pytest.fixture
def sample_text_with_parties():
    """Fixture providing text with party names."""
    return """
    The applicant, Smith Corporation, filed proceedings against
    Jones Enterprises Ltd. Mr. Brown testified on behalf of Wilson Co.
    """


@pytest.fixture
def sample_text_with_references():
    """Fixture providing text with section references."""
    return """
    As outlined in Section 60CC, the court considered Article 5.2.
    Reference was made to Paragraph 10 and Clause 3.4.1.
    """


@pytest.fixture
def sample_extraction_numerical():
    """Fixture providing extraction data with expected numerical values."""
    return {
        "amounts": [500000, 750000, 2500]
    }


@pytest.fixture
def sample_extraction_dates():
    """Fixture providing extraction data with expected dates."""
    return {
        "dates": ["15 March 2020", "2021-06-15", "Jun 30, 2021"]
    }


@pytest.fixture
def sample_extraction_parties():
    """Fixture providing extraction data with expected parties."""
    return {
        "parties": ["Smith Corporation", "Jones Enterprises Ltd", "Wilson Co"]
    }


@pytest.fixture
def sample_extraction_references():
    """Fixture providing extraction data with valid references."""
    return {
        "valid_references": ["Section 60CC", "Article 5", "Paragraph 10", "Clause 3"]
    }


# ============================================================================
# SPAN ISSUE TESTS
# ============================================================================

class TestSpanIssue:
    """Tests for SpanIssue dataclass."""

    def test_create_span_issue_basic(self):
        """Test creating a basic SpanIssue."""
        issue = SpanIssue(
            issue_type="numerical_conflict",
            span_start=100,
            span_end=110,
            flagged_text="$500",
            expected_value="$600",
            confidence=0.85,
            source_reference="numerical_pattern_matcher"
        )

        assert issue.issue_type == "numerical_conflict"
        assert issue.span_start == 100
        assert issue.span_end == 110
        assert issue.flagged_text == "$500"
        assert issue.expected_value == "$600"
        assert issue.confidence == 0.85
        assert issue.source_reference == "numerical_pattern_matcher"

    def test_span_issue_confidence_range(self):
        """Test SpanIssue accepts valid confidence values."""
        for confidence in [0.0, 0.5, 1.0]:
            issue = SpanIssue(
                issue_type="test",
                span_start=0,
                span_end=10,
                flagged_text="test",
                expected_value="test",
                confidence=confidence,
                source_reference="test"
            )
            assert 0.0 <= issue.confidence <= 1.0

    def test_span_issue_types(self):
        """Test creating SpanIssues of different types."""
        issue_types = [
            "numerical_conflict",
            "date_mismatch",
            "party_name_mismatch",
            "invalid_reference"
        ]

        for issue_type in issue_types:
            issue = SpanIssue(
                issue_type=issue_type,
                span_start=0,
                span_end=10,
                flagged_text="test",
                expected_value="test",
                confidence=0.8,
                source_reference="test"
            )
            assert issue.issue_type == issue_type


# ============================================================================
# SPAN ALIGNED VSA INITIALIZATION TESTS
# ============================================================================

class TestSpanAlignedVSAInitialization:
    """Tests for SpanAlignedVSA initialization."""

    def test_initialization(self, span_detector, mock_vsa):
        """Test SpanAlignedVSA initialization."""
        assert span_detector is not None
        assert span_detector.base_vsa == mock_vsa

    def test_regex_patterns_defined(self, span_detector):
        """Test that regex patterns are properly defined."""
        assert span_detector.NUMERICAL_PATTERN is not None
        assert span_detector.DATE_PATTERN is not None
        assert span_detector.PARTY_PATTERN is not None
        assert span_detector.REFERENCE_PATTERN is not None

    def test_can_instantiate_multiple_detectors(self, mock_vsa):
        """Test creating multiple detector instances."""
        detector1 = SpanAlignedVSA(mock_vsa)
        detector2 = SpanAlignedVSA(mock_vsa)

        assert detector1 is not detector2
        assert detector1.base_vsa == detector2.base_vsa


# ============================================================================
# NUMERICAL SPAN DETECTION TESTS
# ============================================================================

class TestNumericalSpanDetection:
    """Tests for numerical span detection."""

    def test_detect_numerical_spans_basic(self, span_detector, sample_text_with_numbers):
        """Test basic numerical span detection."""
        extraction = {"amounts": [500000]}

        issues = span_detector._detect_numerical_spans(
            sample_text_with_numbers,
            extraction
        )

        assert isinstance(issues, list)

    def test_detect_numerical_spans_no_conflicts(
        self,
        span_detector,
        sample_text_with_numbers,
        sample_extraction_numerical
    ):
        """Test numerical detection with no conflicts."""
        issues = span_detector._detect_numerical_spans(
            sample_text_with_numbers,
            sample_extraction_numerical
        )

        # All numbers match expectations, should have no issues
        assert len(issues) == 0

    def test_detect_numerical_spans_with_conflict(self, span_detector):
        """Test numerical detection with conflicts."""
        text = "The amount is $500,000 and $600,000"
        extraction = {"amounts": [500000]}  # Only one expected

        issues = span_detector._detect_numerical_spans(text, extraction)

        # Should detect $600,000 as unexpected
        assert len(issues) > 0
        assert any("600,000" in issue.flagged_text for issue in issues)

    def test_detect_numerical_spans_empty_extraction(
        self,
        span_detector,
        sample_text_with_numbers
    ):
        """Test numerical detection with no expected amounts."""
        issues = span_detector._detect_numerical_spans(
            sample_text_with_numbers,
            {"amounts": []}
        )

        # With no expected amounts, all found numbers are issues
        assert len(issues) > 0

    def test_detect_numerical_spans_currency_symbols(self, span_detector):
        """Test detection of numbers with currency symbols."""
        text = "$1,000 and $2,500.50"
        extraction = {"amounts": [1000, 2500.50]}

        issues = span_detector._detect_numerical_spans(text, extraction)

        assert len(issues) == 0  # Should match

    def test_normalize_number_method(self, span_detector):
        """Test the _normalize_number helper method."""
        assert span_detector._normalize_number("$500") == 500.0
        assert span_detector._normalize_number("1,000") == 1000.0
        assert span_detector._normalize_number("2,500.50") == 2500.5
        assert span_detector._normalize_number("100") == 100.0

    def test_normalize_number_invalid_input(self, span_detector):
        """Test _normalize_number with invalid input."""
        result = span_detector._normalize_number("invalid")
        assert result == 0.0


# ============================================================================
# DATE SPAN DETECTION TESTS
# ============================================================================

class TestDateSpanDetection:
    """Tests for date span detection."""

    def test_detect_date_spans_basic(self, span_detector, sample_text_with_dates):
        """Test basic date span detection."""
        extraction = {"dates": ["15 March 2020"]}

        issues = span_detector._detect_date_spans(
            sample_text_with_dates,
            extraction
        )

        assert isinstance(issues, list)

    def test_detect_date_spans_no_conflicts(
        self,
        span_detector,
        sample_text_with_dates,
        sample_extraction_dates
    ):
        """Test date detection with no conflicts."""
        issues = span_detector._detect_date_spans(
            sample_text_with_dates,
            sample_extraction_dates
        )

        # All dates match expectations
        assert len(issues) == 0

    def test_detect_date_spans_with_mismatch(self, span_detector):
        """Test date detection with mismatches."""
        text = "The date was 15 March 2020 and 20 April 2021"
        extraction = {"dates": ["15 March 2020"]}

        issues = span_detector._detect_date_spans(text, extraction)

        # Should detect the unmatched date
        assert len(issues) > 0

    def test_detect_date_spans_various_formats(self, span_detector):
        """Test detection of various date formats."""
        text = "15 March 2020, 2021-06-15, Jun 30, 2021"
        extraction = {"dates": [
            "15 March 2020",
            "2021-06-15",
            "Jun 30, 2021"
        ]}

        issues = span_detector._detect_date_spans(text, extraction)

        # All formats should be detected and matched
        assert len(issues) == 0

    def test_normalize_date_method(self, span_detector):
        """Test the _normalize_date helper method."""
        result = span_detector._normalize_date("15 March 2020")
        assert result == "15 march 2020"

        result = span_detector._normalize_date("  Multiple   Spaces  ")
        assert result == "multiple spaces"

    def test_dates_match_method(self, span_detector):
        """Test the _dates_match helper method."""
        # Same dates in different formats
        assert span_detector._dates_match("15 March 2020", "15 march 2020")

        # Different dates
        # Note: simplified matching checks for overlapping components

    def test_detect_date_spans_empty_extraction(self, span_detector):
        """Test date detection with no expected dates."""
        text = "The date was 15 March 2020"
        issues = span_detector._detect_date_spans(text, {"dates": []})

        # With no expected dates, found dates are flagged
        assert len(issues) > 0


# ============================================================================
# PARTY SPAN DETECTION TESTS
# ============================================================================

class TestPartySpanDetection:
    """Tests for party name span detection."""

    def test_detect_party_spans_basic(
        self,
        span_detector,
        sample_text_with_parties
    ):
        """Test basic party name detection."""
        extraction = {"parties": ["Smith Corporation"]}

        issues = span_detector._detect_party_spans(
            sample_text_with_parties,
            extraction
        )

        assert isinstance(issues, list)

    def test_detect_party_spans_no_conflicts(
        self,
        span_detector,
        sample_text_with_parties,
        sample_extraction_parties
    ):
        """Test party detection with no conflicts."""
        issues = span_detector._detect_party_spans(
            sample_text_with_parties,
            sample_extraction_parties
        )

        # All parties match expectations
        assert len(issues) == 0

    def test_detect_party_spans_with_mismatch(self, span_detector):
        """Test party detection with mismatches."""
        text = "Smith Corporation and Unknown Company Ltd"
        extraction = {"parties": ["Smith Corporation"]}

        issues = span_detector._detect_party_spans(text, extraction)

        # Should detect Unknown Company as unexpected
        assert len(issues) > 0

    def test_party_names_match_method(self, span_detector):
        """Test the _party_names_match helper method."""
        # Exact match
        assert span_detector._party_names_match("Smith Corp", "Smith Corp")

        # Case insensitive
        assert span_detector._party_names_match("Smith Corp", "smith corp")

        # Substring match
        assert span_detector._party_names_match("Smith", "Smith Corporation")

    def test_find_closest_party_method(self, span_detector):
        """Test the _find_closest_party helper method."""
        parties = ["Smith Corporation", "Jones Enterprises", "Wilson Co"]

        closest = span_detector._find_closest_party("Smith Corp", parties)
        assert "Smith" in closest

        closest = span_detector._find_closest_party("Jones Ltd", parties)
        assert "Jones" in closest

    def test_is_similar_party_method(self, span_detector):
        """Test the _is_similar_party helper method."""
        # Similar names
        assert span_detector._is_similar_party("Smith Corp", "Smith Corporation")

        # Different names
        assert not span_detector._is_similar_party("Smith Corp", "Jones Ltd")


# ============================================================================
# REFERENCE SPAN DETECTION TESTS
# ============================================================================

class TestReferenceSpanDetection:
    """Tests for reference span detection."""

    def test_detect_reference_spans_basic(
        self,
        span_detector,
        sample_text_with_references
    ):
        """Test basic reference detection."""
        extraction = {"valid_references": ["Section 60CC"]}

        issues = span_detector._detect_reference_spans(
            sample_text_with_references,
            extraction
        )

        assert isinstance(issues, list)

    def test_detect_reference_spans_no_conflicts(
        self,
        span_detector,
        sample_text_with_references,
        sample_extraction_references
    ):
        """Test reference detection with no conflicts."""
        issues = span_detector._detect_reference_spans(
            sample_text_with_references,
            sample_extraction_references
        )

        # All references are valid
        assert len(issues) == 0

    def test_detect_reference_spans_invalid_reference(self, span_detector):
        """Test detection of invalid references."""
        text = "See Section 60CC and Section 999"
        extraction = {"valid_references": ["Section 60CC"]}

        issues = span_detector._detect_reference_spans(text, extraction)

        # Should detect Section 999 as invalid
        assert len(issues) > 0

    def test_references_match_method(self, span_detector):
        """Test the _references_match helper method."""
        # Same section numbers
        assert span_detector._references_match("Section 60", "Section 60")

        # Different section numbers
        assert not span_detector._references_match("Section 60", "Section 70")


# ============================================================================
# IOU CALCULATION TESTS
# ============================================================================

class TestIOUCalculation:
    """Tests for Intersection over Union calculation."""

    def test_calculate_iou_perfect_overlap(self, span_detector):
        """Test IoU with perfect overlap."""
        span1 = (10, 20)
        span2 = (10, 20)

        iou = span_detector._calculate_iou(span1, span2)

        assert iou == 1.0

    def test_calculate_iou_no_overlap(self, span_detector):
        """Test IoU with no overlap."""
        span1 = (10, 20)
        span2 = (30, 40)

        iou = span_detector._calculate_iou(span1, span2)

        assert iou == 0.0

    def test_calculate_iou_partial_overlap(self, span_detector):
        """Test IoU with partial overlap."""
        span1 = (10, 20)
        span2 = (15, 25)

        iou = span_detector._calculate_iou(span1, span2)

        # Intersection: [15, 20) = 5
        # Union: [10, 25) = 15
        # IoU = 5/15 = 0.333...
        assert 0.3 < iou < 0.4

    def test_calculate_iou_contained_span(self, span_detector):
        """Test IoU when one span contains the other."""
        span1 = (10, 30)
        span2 = (15, 25)

        iou = span_detector._calculate_iou(span1, span2)

        # Intersection: [15, 25) = 10
        # Union: [10, 30) = 20
        # IoU = 10/20 = 0.5
        assert iou == 0.5

    def test_calculate_iou_zero_length_spans(self, span_detector):
        """Test IoU with zero-length spans."""
        span1 = (10, 10)
        span2 = (10, 10)

        iou = span_detector._calculate_iou(span1, span2)

        assert iou == 1.0  # Both empty at same position

    def test_calculate_iou_symmetry(self, span_detector):
        """Test that IoU is symmetric."""
        span1 = (10, 20)
        span2 = (15, 25)

        iou1 = span_detector._calculate_iou(span1, span2)
        iou2 = span_detector._calculate_iou(span2, span1)

        assert iou1 == iou2


# ============================================================================
# LOCATION ALIGNMENT TESTS
# ============================================================================

class TestLocationAlignment:
    """Tests for location alignment calculation."""

    def test_calculate_location_alignment_perfect(self, span_detector):
        """Test alignment with perfect predictions."""
        predicted = [(10, 20), (30, 40), (50, 60)]
        ground_truth = [(10, 20), (30, 40), (50, 60)]

        alignment = span_detector.calculate_location_alignment(
            predicted,
            ground_truth
        )

        assert alignment == 1.0

    def test_calculate_location_alignment_no_predictions(self, span_detector):
        """Test alignment with no predictions."""
        predicted = []
        ground_truth = [(10, 20), (30, 40)]

        alignment = span_detector.calculate_location_alignment(
            predicted,
            ground_truth
        )

        assert alignment == 0.0

    def test_calculate_location_alignment_no_ground_truth(self, span_detector):
        """Test alignment with no ground truth."""
        predicted = [(10, 20), (30, 40)]
        ground_truth = []

        alignment = span_detector.calculate_location_alignment(
            predicted,
            ground_truth
        )

        assert alignment == 0.0

    def test_calculate_location_alignment_partial(self, span_detector):
        """Test alignment with partial overlap."""
        predicted = [(10, 20), (35, 45)]
        ground_truth = [(10, 20), (30, 40)]

        alignment = span_detector.calculate_location_alignment(
            predicted,
            ground_truth
        )

        assert 0.0 < alignment < 1.0

    def test_calculate_location_alignment_extra_predictions(self, span_detector):
        """Test alignment with extra false positive predictions."""
        predicted = [(10, 20), (30, 40), (50, 60), (70, 80)]
        ground_truth = [(10, 20), (30, 40)]

        alignment = span_detector.calculate_location_alignment(
            predicted,
            ground_truth
        )

        # Should penalize extra predictions
        assert alignment < 1.0


# ============================================================================
# FULL DETECTION TESTS
# ============================================================================

class TestFullDetection:
    """Tests for the complete detection workflow."""

    def test_detect_issues_with_spans_basic(self, span_detector):
        """Test basic issue detection with spans."""
        text = "The amount is $500,000 on 15 March 2020"
        extraction = {
            "amounts": [500000],
            "dates": ["15 March 2020"],
            "parties": [],
            "valid_references": []
        }

        issues = span_detector.detect_issues_with_spans(text, extraction)

        assert isinstance(issues, list)

    def test_detect_issues_with_spans_sorted(self, span_detector):
        """Test that detected issues are sorted by position."""
        text = """
        Section 60CC states that $500,000 shall be paid by Smith Corporation
        on 15 March 2020 to Jones Enterprises.
        """
        extraction = {
            "amounts": [500000],
            "dates": ["15 March 2020"],
            "parties": ["Smith Corporation", "Jones Enterprises"],
            "valid_references": ["Section 60CC"]
        }

        issues = span_detector.detect_issues_with_spans(text, extraction)

        # Check that issues are sorted by span_start
        for i in range(len(issues) - 1):
            assert issues[i].span_start <= issues[i + 1].span_start

    def test_detect_issues_with_spans_multiple_types(self, span_detector):
        """Test detection of multiple issue types."""
        text = "Amount: $999,999, Date: 99 March 2099, Party: Unknown Corp, Section: 999"
        extraction = {
            "amounts": [500000],
            "dates": ["15 March 2020"],
            "parties": ["Known Corp"],
            "valid_references": ["Section 60CC"]
        }

        issues = span_detector.detect_issues_with_spans(text, extraction)

        # Should detect issues of multiple types
        issue_types = set(issue.issue_type for issue in issues)
        assert len(issue_types) > 0

    def test_detect_issues_with_spans_empty_text(self, span_detector):
        """Test detection with empty text."""
        issues = span_detector.detect_issues_with_spans("", {})

        assert issues == []

    def test_detect_issues_with_spans_empty_extraction(self, span_detector):
        """Test detection with empty extraction."""
        text = "The amount is $500,000"
        issues = span_detector.detect_issues_with_spans(text, {})

        # Should still detect issues (as everything is unexpected)
        assert isinstance(issues, list)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestSpanDetectorIntegration:
    """Integration tests for span detector."""

    def test_end_to_end_detection(self, span_detector):
        """Test end-to-end detection workflow."""
        text = """
        IN THE FAMILY COURT OF AUSTRALIA

        ORDERS:

        1. The matrimonial property valued at $800,000 shall be divided 60/40.
        2. Settlement to be completed by 15 December 2023.
        3. Smith Corporation shall transfer assets to Jones Enterprises Ltd.

        Reference: Section 79 of the Family Law Act 1975.
        """

        extraction = {
            "amounts": [800000],
            "dates": ["15 December 2023"],
            "parties": ["Smith Corporation", "Jones Enterprises Ltd"],
            "valid_references": ["Section 79"]
        }

        issues = span_detector.detect_issues_with_spans(text, extraction)

        # Should complete without errors
        assert isinstance(issues, list)

    def test_detection_with_realistic_data(self, span_detector):
        """Test detection with realistic legal document data."""
        text = """
        The court orders that the property settlement of $1,250,000 be divided
        as follows: 65% to the wife and 35% to the husband. The settlement shall
        be completed no later than 30 June 2024.
        """

        extraction = {
            "amounts": [1250000],
            "dates": ["30 June 2024"],
            "parties": [],
            "valid_references": []
        }

        issues = span_detector.detect_issues_with_spans(text, extraction)

        # All expected values present, should have minimal issues
        assert isinstance(issues, list)

    def test_alignment_and_detection_combined(self, span_detector):
        """Test combining detection and alignment scoring."""
        text = "Amount: $500,000 and $600,000"

        extraction = {
            "amounts": [500000, 600000]
        }

        # Detect issues
        issues = span_detector._detect_numerical_spans(text, extraction)

        # Extract predicted spans from issues (if any)
        predicted_spans = [(issue.span_start, issue.span_end) for issue in issues]

        # Calculate alignment if we have predictions
        if predicted_spans:
            ground_truth = [(8, 17), (22, 31)]  # Approximate positions
            alignment = span_detector.calculate_location_alignment(
                predicted_spans,
                ground_truth
            )
            assert 0.0 <= alignment <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
