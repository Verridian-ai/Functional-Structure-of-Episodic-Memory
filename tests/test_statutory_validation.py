"""
Test Script for Statutory RAG Validation Module
================================================

Demonstrates the usage of the statutory validation module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from validation import StatutoryRAGValidator, StatutoryReference, ValidationResult


def test_basic_validation():
    """Test basic validation functionality."""
    print("=" * 80)
    print("STATUTORY RAG VALIDATION TEST")
    print("=" * 80)
    print()

    # Initialize validator
    print("Initializing validator...")
    validator = StatutoryRAGValidator(corpus_path="data/statutory_corpus")
    print()

    # Test Case 1: Valid extraction with good compliance
    print("-" * 80)
    print("TEST CASE 1: Valid Child Best Interests Extraction")
    print("-" * 80)

    extraction1 = {
        "legal_test": "Best Interests of the Child",
        "elements": {
            "safety": "The court must consider the safety of the child from harm",
            "meaningful_relationship": "Benefit of meaningful relationship with both parents",
            "views_of_child": "The child's views were expressed and considered"
        },
        "findings": [
            "The court found that safety from family violence is paramount",
            "The child benefits from spending time with both parents",
            "The child, aged 12, expressed clear views about living arrangements"
        ],
        "conclusion": "Orders made in the best interests of the child per s60CC"
    }

    result1 = validator.validate_extraction(extraction1)
    print_result(result1)

    # Test Case 2: Extraction with missing elements
    print("\n" + "-" * 80)
    print("TEST CASE 2: Incomplete Property Settlement Extraction")
    print("-" * 80)

    extraction2 = {
        "legal_test": "Property Settlement",
        "elements": {
            "financial_contributions": "Husband contributed $200,000 deposit"
        },
        "findings": [
            "Husband made initial financial contribution to property purchase"
        ],
        "conclusion": "Property to be divided 70/30 in favor of husband"
    }

    result2 = validator.validate_extraction(extraction2)
    print_result(result2)

    # Test Case 3: Complex parenting case
    print("\n" + "-" * 80)
    print("TEST CASE 3: Parenting Orders with Family Violence")
    print("-" * 80)

    extraction3 = {
        "legal_test": "Parenting Orders in Context of Family Violence",
        "elements": {
            "safety": "Family violence by father toward mother documented",
            "family_violence": "History of coercive and controlling behavior",
            "child_safety": "Risk assessment indicates ongoing risk to child"
        },
        "findings": [
            "Court finds family violence occurred as defined in s4AB",
            "Child's safety is the paramount consideration per s60CC",
            "No meaningful relationship can be facilitated while safety concerns exist"
        ],
        "conclusion": "Mother granted sole parental responsibility; supervised contact only"
    }

    result3 = validator.validate_extraction(extraction3)
    print_result(result3)

    # Test Case 4: Empty extraction
    print("\n" + "-" * 80)
    print("TEST CASE 4: Empty/Invalid Extraction")
    print("-" * 80)

    extraction4 = {}

    result4 = validator.validate_extraction(extraction4)
    print_result(result4)

    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)


def print_result(result: ValidationResult):
    """Pretty print validation result."""
    print()
    print(f"  Status: {'✓ VALID' if result.is_valid else '✗ INVALID'}")
    print(f"  Compliance Score: {result.compliance_score:.2%}")
    print()

    if result.supporting_citations:
        print(f"  Supporting Citations ({len(result.supporting_citations)}):")
        for i, citation in enumerate(result.supporting_citations[:5], 1):
            print(f"    {i}. {citation}")
        if len(result.supporting_citations) > 5:
            print(f"    ... and {len(result.supporting_citations) - 5} more")
        print()

    if result.conflicts:
        print(f"  Conflicts ({len(result.conflicts)}):")
        for i, conflict in enumerate(result.conflicts, 1):
            print(f"    {i}. {conflict}")
        print()

    if result.recommendations:
        print(f"  Recommendations ({len(result.recommendations)}):")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"    {i}. {rec}")
        print()


def test_corpus_loader():
    """Test corpus loader functionality."""
    print("\n" + "=" * 80)
    print("CORPUS LOADER TEST")
    print("=" * 80)
    print()

    from validation import CorpusLoader

    loader = CorpusLoader("data/statutory_corpus")

    # Test section retrieval
    print("Testing section retrieval...")
    section = loader.get_section("60CC")
    if section:
        print(f"  Retrieved: {section.get('title')}")
        print(f"  Act: {section.get('act_name')}")
        print(f"  Summary: {section.get('summary', '')[:100]}...")
    print()

    # Test keyword search
    print("Testing keyword search for 'best interests'...")
    results = loader.search_by_keyword("best interests", top_k=3)
    print(f"  Found {len(results)} sections:")
    for i, result in enumerate(results, 1):
        print(f"    {i}. s{result.get('section')}: {result.get('title')}")
    print()

    # Test text search
    print("Testing text search for 'family violence and safety'...")
    results = loader.search_by_text("family violence and safety", top_k=3)
    print(f"  Found {len(results)} sections:")
    for i, result in enumerate(results, 1):
        print(f"    {i}. s{result.get('section')}: {result.get('title')} "
              f"(relevance: {result.get('relevance_score', 0):.2f})")
    print()

    # Test related provisions
    print("Testing related provisions for s60CC...")
    related = loader.get_related_provisions("60CC")
    print(f"  Found {len(related)} related sections:")
    for i, rel in enumerate(related[:5], 1):
        print(f"    {i}. s{rel.get('section')}: {rel.get('title')}")
    print()


if __name__ == "__main__":
    try:
        test_basic_validation()
        test_corpus_loader()
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
