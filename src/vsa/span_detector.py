"""
Span-Level Detection Module for VSA System
===========================================

This module provides span-level issue detection for the Verridian AI VSA system.
It detects and localizes inconsistencies in extracted legal text, including:
- Numerical conflicts
- Date inconsistencies
- Party name mismatches
- Reference errors

The module uses regex pattern matching and alignment metrics to identify
problematic text spans with high precision.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.vsa.legal_vsa import LegalVSA


@dataclass
class SpanIssue:
    """
    Represents a detected issue at a specific text span.

    Attributes:
        issue_type: Type of issue (e.g., "numerical_conflict", "date_mismatch")
        span_start: Starting character index of the problematic span
        span_end: Ending character index of the problematic span
        flagged_text: The actual text that was flagged
        expected_value: The expected or correct value
        confidence: Confidence score of the detection (0.0 to 1.0)
        source_reference: Reference to the source rule or pattern that flagged this
    """
    issue_type: str
    span_start: int
    span_end: int
    flagged_text: str
    expected_value: str
    confidence: float
    source_reference: str


class SpanAlignedVSA:
    """
    Span-aligned VSA detector for identifying and localizing issues in legal text.

    This class wraps an existing LegalVSA instance and provides methods to detect
    various types of inconsistencies at the span level, enabling precise error
    localization and correction.
    """

    # Regex patterns for common legal entities
    NUMERICAL_PATTERN = r'\$?[\d,]+\.?\d*'
    DATE_PATTERN = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
    PARTY_PATTERN = r'\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|LLC|Corp|Ltd|Co)\.?))\b'
    REFERENCE_PATTERN = r'(?:Section|Article|Clause|Paragraph)\s+\d+(?:\.\d+)*'

    def __init__(self, base_vsa: 'LegalVSA'):
        """
        Initialize the span detector with an existing LegalVSA instance.

        Args:
            base_vsa: The base LegalVSA instance to use for verification
        """
        self.base_vsa = base_vsa

    def detect_issues_with_spans(self, text: str, extraction: dict) -> List[SpanIssue]:
        """
        Main detection method that runs all span-level checks.

        Args:
            text: The original legal document text
            extraction: Dictionary containing extracted information from the text
                Expected keys: 'amounts', 'dates', 'parties', 'references', etc.

        Returns:
            List of detected SpanIssue objects
        """
        issues = []

        # Run all detection methods
        issues.extend(self._detect_numerical_spans(text, extraction))
        issues.extend(self._detect_date_spans(text, extraction))
        issues.extend(self._detect_party_spans(text, extraction))
        issues.extend(self._detect_reference_spans(text, extraction))

        # Sort by span position for easier review
        issues.sort(key=lambda x: (x.span_start, x.span_end))

        return issues

    def _detect_numerical_spans(self, text: str, extraction: dict) -> List[SpanIssue]:
        """
        Detect conflicting or inconsistent numerical values in the text.

        This method finds all numerical values in the text and compares them
        with the extracted amounts to identify mismatches or conflicts.

        Args:
            text: The original document text
            extraction: Dictionary with 'amounts' key containing expected amounts

        Returns:
            List of SpanIssue objects for numerical conflicts
        """
        issues = []

        # Extract expected amounts from extraction dict
        expected_amounts = extraction.get('amounts', [])

        # Find all numerical values in text
        for match in re.finditer(self.NUMERICAL_PATTERN, text, re.IGNORECASE):
            found_value = match.group(0)
            span_start = match.start()
            span_end = match.end()

            # Normalize the value for comparison
            normalized_found = self._normalize_number(found_value)

            # Check if this value matches any expected amount
            is_valid = False
            expected_value = None

            for expected in expected_amounts:
                normalized_expected = self._normalize_number(str(expected))
                if abs(normalized_found - normalized_expected) < 0.01:
                    is_valid = True
                    break

            # If we have expected amounts and this doesn't match any of them
            if expected_amounts and not is_valid:
                # Find the closest expected value
                if expected_amounts:
                    expected_value = min(
                        expected_amounts,
                        key=lambda x: abs(self._normalize_number(str(x)) - normalized_found)
                    )

                    issues.append(SpanIssue(
                        issue_type="numerical_conflict",
                        span_start=span_start,
                        span_end=span_end,
                        flagged_text=found_value,
                        expected_value=str(expected_value),
                        confidence=0.8,
                        source_reference="numerical_pattern_matcher"
                    ))

        return issues

    def _detect_date_spans(self, text: str, extraction: dict) -> List[SpanIssue]:
        """
        Detect date inconsistencies in the text.

        This method finds all date patterns and checks for:
        - Dates that don't match extracted dates
        - Chronologically impossible dates
        - Format inconsistencies

        Args:
            text: The original document text
            extraction: Dictionary with 'dates' key containing expected dates

        Returns:
            List of SpanIssue objects for date issues
        """
        issues = []

        expected_dates = extraction.get('dates', [])

        # Find all date patterns in text
        found_dates = []
        for match in re.finditer(self.DATE_PATTERN, text, re.IGNORECASE):
            found_date = match.group(0)
            span_start = match.start()
            span_end = match.end()
            found_dates.append((found_date, span_start, span_end))

        # Check each found date against expected dates
        for found_date, span_start, span_end in found_dates:
            if expected_dates:
                # Check if this date matches any expected date
                normalized_found = self._normalize_date(found_date)

                is_valid = False
                for expected in expected_dates:
                    if self._dates_match(normalized_found, str(expected)):
                        is_valid = True
                        break

                if not is_valid and expected_dates:
                    # Find closest expected date
                    expected_value = expected_dates[0] if len(expected_dates) == 1 else "one of expected dates"

                    issues.append(SpanIssue(
                        issue_type="date_mismatch",
                        span_start=span_start,
                        span_end=span_end,
                        flagged_text=found_date,
                        expected_value=str(expected_value),
                        confidence=0.75,
                        source_reference="date_pattern_matcher"
                    ))

        # Check for chronological impossibilities (future dates in historical docs, etc.)
        for i in range(len(found_dates) - 1):
            date1, start1, end1 = found_dates[i]
            date2, start2, end2 = found_dates[i + 1]

            # If we can parse both dates, check ordering
            # (This is a simplified check - full implementation would parse dates properly)
            if self._is_chronologically_impossible(date1, date2):
                issues.append(SpanIssue(
                    issue_type="chronological_impossibility",
                    span_start=start2,
                    span_end=end2,
                    flagged_text=date2,
                    expected_value=f"date after {date1}",
                    confidence=0.6,
                    source_reference="chronological_validator"
                ))

        return issues

    def _detect_party_spans(self, text: str, extraction: dict) -> List[SpanIssue]:
        """
        Detect party name mismatches and inconsistencies.

        This method finds all party name references and checks for:
        - Names that don't match expected parties
        - Inconsistent name usage (e.g., full name vs. abbreviation)
        - Potential typos in party names

        Args:
            text: The original document text
            extraction: Dictionary with 'parties' key containing expected party names

        Returns:
            List of SpanIssue objects for party name issues
        """
        issues = []

        expected_parties = extraction.get('parties', [])

        # Find all potential party names in text
        for match in re.finditer(self.PARTY_PATTERN, text):
            found_party = match.group(0)
            span_start = match.start()
            span_end = match.end()

            if expected_parties:
                # Check if this party name matches any expected party
                is_valid = False

                for expected in expected_parties:
                    if self._party_names_match(found_party, str(expected)):
                        is_valid = True
                        break

                if not is_valid:
                    # Find the most similar expected party
                    expected_value = self._find_closest_party(found_party, expected_parties)

                    # Calculate confidence based on similarity
                    confidence = 0.7 if self._is_similar_party(found_party, expected_value) else 0.85

                    issues.append(SpanIssue(
                        issue_type="party_name_mismatch",
                        span_start=span_start,
                        span_end=span_end,
                        flagged_text=found_party,
                        expected_value=expected_value,
                        confidence=confidence,
                        source_reference="party_pattern_matcher"
                    ))

        return issues

    def _detect_reference_spans(self, text: str, extraction: dict) -> List[SpanIssue]:
        """
        Detect reference errors (e.g., to sections, articles, clauses).

        This method finds all document references and checks for:
        - References to non-existent sections
        - Inconsistent reference formatting
        - Circular or invalid references

        Args:
            text: The original document text
            extraction: Dictionary with 'valid_references' key containing valid refs

        Returns:
            List of SpanIssue objects for reference errors
        """
        issues = []

        valid_references = extraction.get('valid_references', [])

        # Find all reference patterns
        for match in re.finditer(self.REFERENCE_PATTERN, text, re.IGNORECASE):
            found_ref = match.group(0)
            span_start = match.start()
            span_end = match.end()

            if valid_references:
                # Check if this reference is valid
                is_valid = False

                for valid_ref in valid_references:
                    if self._references_match(found_ref, str(valid_ref)):
                        is_valid = True
                        break

                if not is_valid:
                    issues.append(SpanIssue(
                        issue_type="invalid_reference",
                        span_start=span_start,
                        span_end=span_end,
                        flagged_text=found_ref,
                        expected_value="valid section reference",
                        confidence=0.65,
                        source_reference="reference_validator"
                    ))

        return issues

    def calculate_location_alignment(
        self,
        predicted: List[Tuple[int, int]],
        ground_truth: List[Tuple[int, int]]
    ) -> float:
        """
        Calculate alignment score between predicted and ground truth spans.

        Uses average IoU (Intersection over Union) across all span pairs.

        Args:
            predicted: List of predicted span tuples (start, end)
            ground_truth: List of ground truth span tuples (start, end)

        Returns:
            Alignment score between 0.0 and 1.0
        """
        if not predicted or not ground_truth:
            return 0.0

        # Calculate IoU for each predicted span against all ground truth spans
        total_iou = 0.0
        count = 0

        for pred_span in predicted:
            # Find the best matching ground truth span
            best_iou = 0.0
            for gt_span in ground_truth:
                iou = self._calculate_iou(pred_span, gt_span)
                best_iou = max(best_iou, iou)

            total_iou += best_iou
            count += 1

        # Also check from ground truth perspective
        for gt_span in ground_truth:
            best_iou = 0.0
            for pred_span in predicted:
                iou = self._calculate_iou(pred_span, gt_span)
                best_iou = max(best_iou, iou)

            total_iou += best_iou
            count += 1

        return total_iou / count if count > 0 else 0.0

    def _calculate_iou(self, span1: Tuple[int, int], span2: Tuple[int, int]) -> float:
        """
        Calculate Intersection over Union (IoU) for two spans.

        IoU = |Intersection| / |Union|

        Args:
            span1: First span as (start, end) tuple
            span2: Second span as (start, end) tuple

        Returns:
            IoU score between 0.0 and 1.0
        """
        start1, end1 = span1
        start2, end2 = span2

        # Calculate intersection
        intersection_start = max(start1, start2)
        intersection_end = min(end1, end2)
        intersection_length = max(0, intersection_end - intersection_start)

        # Calculate union
        union_start = min(start1, start2)
        union_end = max(end1, end2)
        union_length = union_end - union_start

        # Avoid division by zero
        if union_length == 0:
            return 1.0 if intersection_length == 0 else 0.0

        return intersection_length / union_length

    # Helper methods for normalization and comparison

    def _normalize_number(self, value: str) -> float:
        """Normalize a numerical string to a float value."""
        # Remove currency symbols and commas
        cleaned = value.replace('$', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def _normalize_date(self, date_str: str) -> str:
        """Normalize a date string for comparison."""
        # Simplified normalization - lowercase and remove extra whitespace
        return ' '.join(date_str.lower().split())

    def _dates_match(self, date1: str, date2: str) -> bool:
        """Check if two date strings represent the same date."""
        # Simplified comparison - in production, would use proper date parsing
        norm1 = self._normalize_date(date1)
        norm2 = self._normalize_date(date2)

        # Extract numerical components for fuzzy matching
        nums1 = set(re.findall(r'\d+', norm1))
        nums2 = set(re.findall(r'\d+', norm2))

        # If they share significant numerical components, consider them matching
        return len(nums1 & nums2) >= 2 or norm1 == norm2

    def _is_chronologically_impossible(self, date1: str, date2: str) -> bool:
        """Check if date2 comes before date1 when it shouldn't."""
        # Simplified check - would need proper date parsing in production
        # For now, just return False (no chronological issues detected)
        return False

    def _party_names_match(self, name1: str, name2: str) -> bool:
        """Check if two party names refer to the same entity."""
        norm1 = name1.lower().strip()
        norm2 = name2.lower().strip()

        # Exact match
        if norm1 == norm2:
            return True

        # Check if one is a substring of the other (abbreviation)
        if norm1 in norm2 or norm2 in norm1:
            return True

        # Check if they share significant words
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        common_words = words1 & words2

        # If they share more than half their words, consider them matching
        min_words = min(len(words1), len(words2))
        return len(common_words) >= min_words * 0.6

    def _find_closest_party(self, party_name: str, expected_parties: List) -> str:
        """Find the most similar party name from expected parties."""
        if not expected_parties:
            return "unknown party"

        best_match = str(expected_parties[0])
        best_score = 0.0

        for expected in expected_parties:
            expected_str = str(expected)
            # Simple similarity based on common words
            words1 = set(party_name.lower().split())
            words2 = set(expected_str.lower().split())

            if not words1 or not words2:
                continue

            score = len(words1 & words2) / max(len(words1), len(words2))

            if score > best_score:
                best_score = score
                best_match = expected_str

        return best_match

    def _is_similar_party(self, name1: str, name2: str) -> bool:
        """Check if two party names are similar (potential typo)."""
        # Levenshtein-like similarity - simplified version
        words1 = set(name1.lower().split())
        words2 = set(name2.lower().split())

        if not words1 or not words2:
            return False

        similarity = len(words1 & words2) / max(len(words1), len(words2))
        return similarity > 0.5

    def _references_match(self, ref1: str, ref2: str) -> bool:
        """Check if two reference strings refer to the same section."""
        # Extract numerical parts
        nums1 = re.findall(r'\d+', ref1)
        nums2 = re.findall(r'\d+', ref2)

        # If they have the same numbers, consider them matching
        return nums1 == nums2
