"""
Family Law Discrepancy Detection Benchmark
===========================================

Generates perturbations and discrepancies in family law documents to test
the system's ability to detect inconsistencies, errors, and contradictions.

This benchmark evaluates:
1. Detection of legal inconsistencies (e.g., property orders without asset pool)
2. Detection of in-text discrepancies (e.g., date mismatches, party name changes)
3. Span-level accuracy of error localization
4. Severity classification of discrepancies

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import re
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime, timedelta


# ============================================================================
# ENUMS - Discrepancy Classifications
# ============================================================================

class LegalDiscrepancyType(str, Enum):
    """Types of legal-domain discrepancies in family law documents."""
    PROPERTY_POOL = "property_pool"                    # Property division without asset pool
    PARENTING_ORDER = "parenting_order"                # Parenting orders without children
    SPOUSAL_MAINTENANCE = "spousal_maintenance"        # Maintenance without legal basis
    CHILD_SUPPORT = "child_support"                    # Child support without children
    CONSENT_ORDER = "consent_order"                    # Consent order without consent


class InTextDiscrepancyType(str, Enum):
    """Types of in-text inconsistencies that can be detected."""
    DATE_INCONSISTENCY = "date_inconsistency"          # Conflicting dates
    PARTY_MISMATCH = "party_mismatch"                  # Party name changes
    ASSET_REFERENCE = "asset_reference"                # Asset value/description conflicts
    NUMERICAL = "numerical"                            # Number mismatches
    ORDER_REFERENCE = "order_reference"                # Order ID/type conflicts


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class DiscrepancyInstance:
    """
    A single instance of a discrepancy in a document.

    Attributes:
        original_text: The original, correct text span
        perturbed_text: The modified text with the discrepancy
        discrepancy_type: Type of discrepancy (legal or in-text)
        span_start: Character index where discrepancy starts
        span_end: Character index where discrepancy ends
        explanation: Human-readable explanation of the discrepancy
        severity: Severity rating (1-5, with 5 being most severe)
    """
    original_text: str
    perturbed_text: str
    discrepancy_type: str  # LegalDiscrepancyType or InTextDiscrepancyType value
    span_start: int
    span_end: int
    explanation: str
    severity: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# FAMILY LAW BENCHMARK
# ============================================================================

class FamilyLawBenchmark:
    """
    Generates perturbations in family law documents to create a benchmark
    dataset for testing discrepancy detection capabilities.

    This class can:
    1. Generate various types of discrepancies (dates, parties, assets, etc.)
    2. Inject them into real or synthetic family law documents
    3. Evaluate detection performance against ground truth
    4. Calculate precision, recall, and F1 scores

    Example:
        >>> benchmark = FamilyLawBenchmark()
        >>> perturbations = benchmark.generate_perturbations(document, "parenting")
        >>> metrics = benchmark.evaluate_detection(predictions, perturbations)
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the benchmark generator.

        Args:
            seed: Random seed for reproducible perturbations
        """
        if seed is not None:
            random.seed(seed)

        # Common family law terms and patterns
        self.party_names = [
            "Mr Smith", "Mrs Smith", "Mr Jones", "Mrs Jones",
            "Mr Brown", "Ms Brown", "Mr Wilson", "Ms Wilson"
        ]

        self.asset_types = [
            "matrimonial home", "investment property", "superannuation",
            "motor vehicle", "bank account", "shares", "business interest"
        ]

        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def generate_perturbations(
        self,
        document: str,
        category: str,
        num_perturbations: int = 5
    ) -> List[DiscrepancyInstance]:
        """
        Generate perturbations for a given document.

        Args:
            document: The source document text
            category: Document category (e.g., "parenting", "property", "general")
            num_perturbations: Number of perturbations to generate

        Returns:
            List of DiscrepancyInstance objects representing the perturbations
        """
        perturbations = []

        # Select perturbation types based on document category
        if category == "parenting":
            perturbations.extend(self._generate_date_perturbations(document, max_count=2))
            perturbations.extend(self._generate_party_perturbations(document, max_count=2))
            perturbations.extend(self._generate_order_perturbations(document, max_count=1))
        elif category == "property":
            perturbations.extend(self._generate_asset_perturbations(document, max_count=2))
            perturbations.extend(self._generate_numerical_perturbations(document, max_count=2))
            perturbations.extend(self._generate_date_perturbations(document, max_count=1))
        else:
            # General perturbations
            perturbations.extend(self._generate_date_perturbations(document, max_count=2))
            perturbations.extend(self._generate_party_perturbations(document, max_count=1))
            perturbations.extend(self._generate_numerical_perturbations(document, max_count=2))

        # Limit to requested number
        return perturbations[:num_perturbations]

    def evaluate_detection(
        self,
        predictions: List[Tuple[int, int, str]],
        ground_truth: List[DiscrepancyInstance]
    ) -> Dict[str, Any]:
        """
        Evaluate detection performance against ground truth.

        Args:
            predictions: List of (start, end, type) tuples from the detection system
            ground_truth: List of DiscrepancyInstance objects (ground truth)

        Returns:
            Dictionary containing evaluation metrics:
            - precision: Proportion of predictions that are correct
            - recall: Proportion of ground truth items detected
            - f1_score: Harmonic mean of precision and recall
            - true_positives: Count of correct detections
            - false_positives: Count of incorrect detections
            - false_negatives: Count of missed discrepancies
            - span_accuracy: Proportion of detections with correct spans
        """
        if not ground_truth:
            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "true_positives": 0,
                "false_positives": len(predictions),
                "false_negatives": 0,
                "span_accuracy": 0.0,
                "details": []
            }

        # Match predictions to ground truth
        matched_predictions = set()
        matched_ground_truth = set()
        exact_span_matches = 0

        for i, pred in enumerate(predictions):
            pred_start, pred_end, pred_type = pred

            # Find overlapping ground truth
            for j, gt in enumerate(ground_truth):
                if self._spans_overlap(pred_start, pred_end, gt.span_start, gt.span_end):
                    # Check if types match (if type is provided)
                    if pred_type == "" or pred_type == gt.discrepancy_type:
                        matched_predictions.add(i)
                        matched_ground_truth.add(j)

                        # Check for exact span match
                        if pred_start == gt.span_start and pred_end == gt.span_end:
                            exact_span_matches += 1
                        break

        true_positives = len(matched_predictions)
        false_positives = len(predictions) - true_positives
        false_negatives = len(ground_truth) - len(matched_ground_truth)

        # Calculate metrics
        precision = true_positives / len(predictions) if predictions else 0.0
        recall = true_positives / len(ground_truth) if ground_truth else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        span_accuracy = exact_span_matches / len(predictions) if predictions else 0.0

        return {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1_score": round(f1_score, 3),
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "span_accuracy": round(span_accuracy, 3),
            "total_predictions": len(predictions),
            "total_ground_truth": len(ground_truth),
            "details": {
                "matched_predictions": list(matched_predictions),
                "matched_ground_truth": list(matched_ground_truth),
                "exact_span_matches": exact_span_matches
            }
        }

    # ========================================================================
    # HELPER METHODS - Perturbation Generation
    # ========================================================================

    def _generate_date_perturbations(
        self,
        document: str,
        max_count: int = 3
    ) -> List[DiscrepancyInstance]:
        """Generate date inconsistency perturbations."""
        perturbations = []

        # Find date patterns
        date_pattern = r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
        matches = list(re.finditer(date_pattern, document))

        if not matches or len(matches) < 2:
            return perturbations

        # Create date inconsistencies
        for _ in range(min(max_count, len(matches) // 2)):
            match = random.choice(matches)
            original_date = match.group(0)
            day, month, year = match.group(1), match.group(2), match.group(3)

            # Perturb the date
            new_day = str(random.randint(1, 28))
            perturbed_date = f"{new_day} {month} {year}"

            perturbations.append(DiscrepancyInstance(
                original_text=original_date,
                perturbed_text=perturbed_date,
                discrepancy_type=InTextDiscrepancyType.DATE_INCONSISTENCY.value,
                span_start=match.start(),
                span_end=match.end(),
                explanation=f"Date changed from '{original_date}' to '{perturbed_date}'",
                severity=3,
                metadata={"original_day": day, "new_day": new_day}
            ))

        return perturbations

    def _generate_party_perturbations(
        self,
        document: str,
        max_count: int = 2
    ) -> List[DiscrepancyInstance]:
        """Generate party name mismatch perturbations."""
        perturbations = []

        # Find party references (Mr/Mrs/Ms + Name)
        party_pattern = r'\b(Mr|Mrs|Ms|Dr)\s+([A-Z][a-z]+)\b'
        matches = list(re.finditer(party_pattern, document))

        if not matches:
            return perturbations

        # Create name mismatches
        for _ in range(min(max_count, len(matches))):
            match = random.choice(matches)
            original_name = match.group(0)
            title = match.group(1)
            surname = match.group(2)

            # Pick a different surname
            new_surname = random.choice([n.split()[-1] for n in self.party_names
                                        if n.split()[-1] != surname])
            perturbed_name = f"{title} {new_surname}"

            perturbations.append(DiscrepancyInstance(
                original_text=original_name,
                perturbed_text=perturbed_name,
                discrepancy_type=InTextDiscrepancyType.PARTY_MISMATCH.value,
                span_start=match.start(),
                span_end=match.end(),
                explanation=f"Party name changed from '{original_name}' to '{perturbed_name}'",
                severity=4,
                metadata={"original_surname": surname, "new_surname": new_surname}
            ))

        return perturbations

    def _generate_asset_perturbations(
        self,
        document: str,
        max_count: int = 2
    ) -> List[DiscrepancyInstance]:
        """Generate asset reference perturbations."""
        perturbations = []

        # Find asset value patterns (e.g., "$500,000")
        value_pattern = r'\$([0-9,]+)'
        matches = list(re.finditer(value_pattern, document))

        if not matches:
            return perturbations

        # Create value mismatches
        for _ in range(min(max_count, len(matches))):
            match = random.choice(matches)
            original_value = match.group(0)
            numeric_value = match.group(1).replace(',', '')

            try:
                value = int(numeric_value)
                # Perturb by 10-30%
                perturbation_factor = random.uniform(1.1, 1.3)
                new_value = int(value * perturbation_factor)
                perturbed_value = f"${new_value:,}"

                perturbations.append(DiscrepancyInstance(
                    original_text=original_value,
                    perturbed_text=perturbed_value,
                    discrepancy_type=InTextDiscrepancyType.ASSET_REFERENCE.value,
                    span_start=match.start(),
                    span_end=match.end(),
                    explanation=f"Asset value changed from '{original_value}' to '{perturbed_value}'",
                    severity=4,
                    metadata={"original_value": value, "new_value": new_value}
                ))
            except (ValueError, OverflowError):
                continue

        return perturbations

    def _generate_numerical_perturbations(
        self,
        document: str,
        max_count: int = 2
    ) -> List[DiscrepancyInstance]:
        """Generate numerical inconsistency perturbations."""
        perturbations = []

        # Find percentage patterns
        percentage_pattern = r'\b(\d+)%\b'
        matches = list(re.finditer(percentage_pattern, document))

        if not matches:
            return perturbations

        # Create percentage mismatches
        for _ in range(min(max_count, len(matches))):
            match = random.choice(matches)
            original_pct = match.group(0)
            value = int(match.group(1))

            # Perturb by ±5-15%
            delta = random.randint(5, 15)
            new_value = max(0, min(100, value + delta))
            perturbed_pct = f"{new_value}%"

            perturbations.append(DiscrepancyInstance(
                original_text=original_pct,
                perturbed_text=perturbed_pct,
                discrepancy_type=InTextDiscrepancyType.NUMERICAL.value,
                span_start=match.start(),
                span_end=match.end(),
                explanation=f"Percentage changed from '{original_pct}' to '{perturbed_pct}'",
                severity=3,
                metadata={"original_value": value, "new_value": new_value}
            ))

        return perturbations

    def _generate_order_perturbations(
        self,
        document: str,
        max_count: int = 1
    ) -> List[DiscrepancyInstance]:
        """Generate order reference perturbations."""
        perturbations = []

        # Find order references (e.g., "Order 1", "paragraph 5")
        order_pattern = r'\b(Order|Paragraph|Section)\s+(\d+)\b'
        matches = list(re.finditer(order_pattern, document, re.IGNORECASE))

        if not matches:
            return perturbations

        # Create order reference mismatches
        for _ in range(min(max_count, len(matches))):
            match = random.choice(matches)
            original_ref = match.group(0)
            prefix = match.group(1)
            number = int(match.group(2))

            # Change the number
            new_number = number + random.randint(1, 5)
            perturbed_ref = f"{prefix} {new_number}"

            perturbations.append(DiscrepancyInstance(
                original_text=original_ref,
                perturbed_text=perturbed_ref,
                discrepancy_type=InTextDiscrepancyType.ORDER_REFERENCE.value,
                span_start=match.start(),
                span_end=match.end(),
                explanation=f"Order reference changed from '{original_ref}' to '{perturbed_ref}'",
                severity=3,
                metadata={"original_number": number, "new_number": new_number}
            ))

        return perturbations

    def _spans_overlap(
        self,
        start1: int,
        end1: int,
        start2: int,
        end2: int
    ) -> bool:
        """Check if two character spans overlap."""
        return not (end1 <= start2 or end2 <= start1)

    # ========================================================================
    # LEGAL DISCREPANCY GENERATORS
    # ========================================================================

    def generate_legal_discrepancies(
        self,
        document: str,
        case_type: str
    ) -> List[DiscrepancyInstance]:
        """
        Generate legal-domain discrepancies (structural inconsistencies).

        Args:
            document: The source document text
            case_type: Type of case (parenting, property, etc.)

        Returns:
            List of legal discrepancy instances
        """
        discrepancies = []

        if case_type == "property":
            # Check for property division without asset pool mention
            if "property" in document.lower() and "divided" in document.lower():
                if "asset pool" not in document.lower() and "matrimonial property" not in document.lower():
                    discrepancies.append(DiscrepancyInstance(
                        original_text="property division discussed",
                        perturbed_text="property division without asset pool definition",
                        discrepancy_type=LegalDiscrepancyType.PROPERTY_POOL.value,
                        span_start=0,
                        span_end=len(document),
                        explanation="Property division ordered without defining the asset pool",
                        severity=5
                    ))

        elif case_type == "parenting":
            # Check for parenting orders without children
            if "parenting" in document.lower() and "order" in document.lower():
                if not any(child_ref in document.lower()
                          for child_ref in ["child", "children", "son", "daughter"]):
                    discrepancies.append(DiscrepancyInstance(
                        original_text="parenting orders discussed",
                        perturbed_text="parenting orders without children mentioned",
                        discrepancy_type=LegalDiscrepancyType.PARENTING_ORDER.value,
                        span_start=0,
                        span_end=len(document),
                        explanation="Parenting orders made without reference to children",
                        severity=5
                    ))

        return discrepancies

    def apply_perturbations(
        self,
        document: str,
        perturbations: List[DiscrepancyInstance]
    ) -> str:
        """
        Apply perturbations to a document.

        Args:
            document: Original document text
            perturbations: List of perturbations to apply

        Returns:
            Modified document with perturbations applied
        """
        # Sort by position (reverse order to maintain indices)
        sorted_perturbations = sorted(perturbations, key=lambda p: p.span_start, reverse=True)

        modified_doc = document
        for perturb in sorted_perturbations:
            # Replace the span
            modified_doc = (
                modified_doc[:perturb.span_start] +
                perturb.perturbed_text +
                modified_doc[perturb.span_end:]
            )

        return modified_doc


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_sample_document(category: str = "parenting") -> str:
    """
    Create a sample family law document for testing.

    Args:
        category: Type of document (parenting, property, general)

    Returns:
        Sample document text
    """
    if category == "parenting":
        return """
IN THE FAMILY COURT OF AUSTRALIA

BETWEEN: Mr Smith (Applicant)
AND: Mrs Smith (Respondent)

ORDERS:

1. The parties separated on 15 March 2020.

2. The children of the marriage are:
   - John Smith, born 5 January 2015
   - Mary Smith, born 12 June 2017

3. The children shall live with the mother, Mrs Smith.

4. The children shall spend time with the father as follows:
   - Alternate weekends from Friday 6pm to Sunday 6pm
   - Half of school holidays

5. Each party shall pay 50% of the children's educational expenses.

DATED: 20 September 2023
"""
    elif category == "property":
        return """
IN THE FAMILY COURT OF AUSTRALIA

PROPERTY SETTLEMENT

BETWEEN: Mr Jones (Husband)
AND: Mrs Jones (Wife)

ORDERS:

1. The parties separated on 10 July 2019.

2. The matrimonial asset pool is valued at $1,200,000 comprising:
   - Matrimonial home: $800,000
   - Superannuation (husband): $250,000
   - Superannuation (wife): $100,000
   - Motor vehicles: $50,000

3. The property shall be divided 60% to the wife and 40% to the husband.

4. The matrimonial home shall be transferred to the wife.

5. Each party shall retain their respective superannuation.

DATED: 5 November 2023
"""
    else:
        return """
IN THE FAMILY COURT OF AUSTRALIA

GENERAL ORDERS

BETWEEN: Mr Brown (Applicant)
AND: Ms Brown (Respondent)

ORDER:

1. The parties were in a de facto relationship from 1 January 2015 to 30 June 2021.

2. The applicant shall pay spousal maintenance to the respondent in the amount of
   $500 per week commencing 1 December 2023.

3. The maintenance order shall continue for a period of 2 years.

DATED: 15 October 2023
"""
