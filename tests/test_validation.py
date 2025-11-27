"""
Comprehensive Tests for the Validation Module
==============================================

Tests for the statutory validation system, including:
- StatutoryReference creation
- ValidationResult creation
- CorpusLoader.load_corpus()
- CorpusLoader.search_by_keyword()
- StatutoryRAGValidator.validate_extraction()

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import pytest
import json
import tempfile
from pathlib import Path
from typing import Dict, List

from src.validation.statutory_rag import (
    StatutoryReference,
    ValidationResult,
    StatutoryRAGValidator
)
from src.validation.corpus_loader import CorpusLoader


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_corpus_data():
    """Fixture providing sample statutory corpus data."""
    return {
        "act": {
            "name": "Family Law Act 1975",
            "citation": "FLA 1975",
            "url": "https://legislation.gov.au/fla1975"
        },
        "sections": [
            {
                "section": "60CC",
                "title": "Best interests of the child",
                "summary": "The court must regard the best interests of the child as the paramount consideration.",
                "legal_test": "Best interests test",
                "keywords": ["best interests", "child", "paramount", "consideration"],
                "required_elements": [
                    {
                        "element": "Child's views",
                        "keywords": ["child", "views", "wishes"]
                    },
                    {
                        "element": "Relationship with parents",
                        "keywords": ["relationship", "parent", "bond"]
                    }
                ],
                "minimum_elements": 2,
                "threshold": 0.5
            },
            {
                "section": "79",
                "title": "Property division",
                "summary": "The court may make orders for property division considering contributions and future needs.",
                "legal_test": "Property division test",
                "keywords": ["property", "division", "contributions", "future needs"],
                "required_elements": [
                    {
                        "element": "Asset pool",
                        "keywords": ["asset", "pool", "property"]
                    },
                    {
                        "element": "Contributions",
                        "keywords": ["contributions", "financial", "non-financial"]
                    }
                ],
                "minimum_elements": 2
            }
        ]
    }


@pytest.fixture
def temp_corpus_dir(tmp_path, sample_corpus_data):
    """Fixture creating a temporary corpus directory with test data."""
    corpus_dir = tmp_path / "statutory_corpus"
    corpus_dir.mkdir()

    # Write sample corpus file
    corpus_file = corpus_dir / "family_law_act_1975.json"
    with open(corpus_file, "w") as f:
        json.dump(sample_corpus_data, f, indent=2)

    return str(corpus_dir)


@pytest.fixture
def corpus_loader(temp_corpus_dir):
    """Fixture providing a CorpusLoader with test data."""
    return CorpusLoader(temp_corpus_dir)


@pytest.fixture
def validator(temp_corpus_dir):
    """Fixture providing a StatutoryRAGValidator with test data."""
    return StatutoryRAGValidator(temp_corpus_dir)


@pytest.fixture
def sample_extraction():
    """Fixture providing a sample legal extraction."""
    return {
        "text": "The court considered the best interests of the child.",
        "legal_test": "Best interests test",
        "requirements": [
            "Consider child's views",
            "Assess relationship with parents"
        ],
        "findings": [
            "Child expressed preference to live with mother",
            "Strong bond with both parents observed"
        ]
    }


@pytest.fixture
def invalid_extraction():
    """Fixture providing an extraction that should fail validation."""
    return {
        "text": "Property should be divided.",
        "legal_test": "Property division test",
        "findings": [
            "No asset pool defined",
            "No contributions assessed"
        ]
    }


# ============================================================================
# STATUTORY REFERENCE TESTS
# ============================================================================

class TestStatutoryReference:
    """Tests for StatutoryReference dataclass."""

    def test_create_statutory_reference_basic(self):
        """Test creating a basic StatutoryReference."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC",
            content="Best interests of child"
        )

        assert ref.act_name == "Family Law Act 1975"
        assert ref.section == "60CC"
        assert ref.content == "Best interests of child"
        assert ref.subsection is None
        assert ref.url == ""

    def test_create_statutory_reference_with_subsection(self):
        """Test creating a StatutoryReference with subsection."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC",
            subsection="2",
            content="Best interests factors"
        )

        assert ref.subsection == "2"

    def test_create_statutory_reference_with_url(self):
        """Test creating a StatutoryReference with URL."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="79",
            url="https://legislation.gov.au/fla1975/s79"
        )

        assert ref.url == "https://legislation.gov.au/fla1975/s79"

    def test_statutory_reference_str_without_subsection(self):
        """Test string representation without subsection."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC"
        )

        assert str(ref) == "Family Law Act 1975 s60CC"

    def test_statutory_reference_str_with_subsection(self):
        """Test string representation with subsection."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC",
            subsection="2"
        )

        assert str(ref) == "Family Law Act 1975 s60CC(2)"

    def test_statutory_reference_equality(self):
        """Test equality comparison of StatutoryReferences."""
        ref1 = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC"
        )
        ref2 = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC"
        )

        assert ref1 == ref2


# ============================================================================
# VALIDATION RESULT TESTS
# ============================================================================

class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_create_validation_result_valid(self):
        """Test creating a valid ValidationResult."""
        ref = StatutoryReference(
            act_name="Family Law Act 1975",
            section="60CC"
        )

        result = ValidationResult(
            is_valid=True,
            compliance_score=0.85,
            supporting_citations=[ref],
            conflicts=[],
            recommendations=["Good compliance"]
        )

        assert result.is_valid is True
        assert result.compliance_score == 0.85
        assert len(result.supporting_citations) == 1
        assert len(result.conflicts) == 0
        assert len(result.recommendations) == 1

    def test_create_validation_result_invalid(self):
        """Test creating an invalid ValidationResult."""
        result = ValidationResult(
            is_valid=False,
            compliance_score=0.3,
            supporting_citations=[],
            conflicts=["Missing required element"],
            recommendations=["Add missing information"]
        )

        assert result.is_valid is False
        assert result.compliance_score == 0.3
        assert len(result.conflicts) == 1
        assert len(result.recommendations) == 1

    def test_validation_result_str_representation(self):
        """Test string representation of ValidationResult."""
        result = ValidationResult(
            is_valid=True,
            compliance_score=0.9
        )

        str_repr = str(result)
        assert "VALID" in str_repr
        assert "0.90" in str_repr

    def test_validation_result_default_fields(self):
        """Test ValidationResult with default field values."""
        result = ValidationResult(
            is_valid=True,
            compliance_score=0.8
        )

        assert result.supporting_citations == []
        assert result.conflicts == []
        assert result.recommendations == []


# ============================================================================
# CORPUS LOADER TESTS
# ============================================================================

class TestCorpusLoader:
    """Tests for CorpusLoader class."""

    def test_initialization(self, corpus_loader):
        """Test CorpusLoader initialization."""
        assert corpus_loader is not None
        assert len(corpus_loader.acts) > 0

    def test_load_corpus_success(self, temp_corpus_dir):
        """Test successful corpus loading."""
        loader = CorpusLoader(temp_corpus_dir)

        assert "Family Law Act 1975" in loader.acts
        assert len(loader.acts["Family Law Act 1975"]["sections"]) == 2

    def test_load_corpus_nonexistent_directory(self):
        """Test loading from nonexistent directory."""
        loader = CorpusLoader("/nonexistent/path")

        assert len(loader.acts) == 0

    def test_build_section_index(self, corpus_loader):
        """Test section index is built correctly."""
        assert "60CC" in corpus_loader.section_index
        assert "79" in corpus_loader.section_index

    def test_build_keyword_index(self, corpus_loader):
        """Test keyword index is built correctly."""
        assert "child" in corpus_loader.keyword_index
        assert "property" in corpus_loader.keyword_index
        assert "best interests" in corpus_loader.keyword_index

    def test_get_section_by_number(self, corpus_loader):
        """Test retrieving a section by number."""
        section = corpus_loader.get_section("60CC")

        assert section is not None
        assert section["section"] == "60CC"
        assert section["title"] == "Best interests of the child"

    def test_get_section_with_act_name(self, corpus_loader):
        """Test retrieving a section with specific act name."""
        section = corpus_loader.get_section("60CC", "Family Law Act 1975")

        assert section is not None
        assert section["act_name"] == "Family Law Act 1975"

    def test_get_section_nonexistent(self, corpus_loader):
        """Test retrieving nonexistent section."""
        section = corpus_loader.get_section("999")

        assert section is None

    def test_search_by_keyword_exact_match(self, corpus_loader):
        """Test keyword search with exact match."""
        results = corpus_loader.search_by_keyword("child")

        assert len(results) > 0
        assert any("child" in r.get("keywords", []) for r in results)

    def test_search_by_keyword_partial_match(self, corpus_loader):
        """Test keyword search with partial match."""
        results = corpus_loader.search_by_keyword("interest")

        assert len(results) > 0

    def test_search_by_keyword_top_k_limit(self, corpus_loader):
        """Test keyword search respects top_k limit."""
        results = corpus_loader.search_by_keyword("child", top_k=1)

        assert len(results) <= 1

    def test_search_by_keyword_no_results(self, corpus_loader):
        """Test keyword search with no matches."""
        results = corpus_loader.search_by_keyword("nonexistent_keyword_xyz")

        assert len(results) == 0

    def test_search_by_text(self, corpus_loader):
        """Test text search functionality."""
        results = corpus_loader.search_by_text("best interests of the child")

        assert len(results) > 0
        assert results[0]["section"] == "60CC"

    def test_search_by_text_relevance_scoring(self, corpus_loader):
        """Test that text search returns relevance scores."""
        results = corpus_loader.search_by_text("child interests")

        assert len(results) > 0
        assert "relevance_score" in results[0]
        assert results[0]["relevance_score"] > 0

    def test_search_by_text_top_k(self, corpus_loader):
        """Test text search respects top_k parameter."""
        results = corpus_loader.search_by_text("property", top_k=1)

        assert len(results) <= 1

    def test_get_related_provisions(self, corpus_loader):
        """Test getting related provisions."""
        related = corpus_loader.get_related_provisions("60CC")

        # Should find sections with overlapping keywords
        assert isinstance(related, list)

    def test_get_all_acts(self, corpus_loader):
        """Test retrieving all acts metadata."""
        acts = corpus_loader.get_all_acts()

        assert len(acts) > 0
        assert any(act["name"] == "Family Law Act 1975" for act in acts)

    def test_get_sections_by_legal_test(self, corpus_loader):
        """Test retrieving sections by legal test."""
        sections = corpus_loader.get_sections_by_legal_test("Best interests test")

        assert len(sections) > 0
        assert sections[0]["section"] == "60CC"

    def test_corpus_loader_with_multiple_acts(self, tmp_path):
        """Test CorpusLoader with multiple act files."""
        corpus_dir = tmp_path / "multi_corpus"
        corpus_dir.mkdir()

        # Create two act files
        for i, act_name in enumerate(["Act A", "Act B"]):
            act_data = {
                "act": {"name": act_name},
                "sections": [{"section": f"{i+1}", "title": f"Section {i+1}"}]
            }
            with open(corpus_dir / f"act_{i}.json", "w") as f:
                json.dump(act_data, f)

        loader = CorpusLoader(str(corpus_dir))

        assert len(loader.acts) == 2
        assert "Act A" in loader.acts
        assert "Act B" in loader.acts


# ============================================================================
# STATUTORY RAG VALIDATOR TESTS
# ============================================================================

class TestStatutoryRAGValidator:
    """Tests for StatutoryRAGValidator class."""

    def test_initialization(self, validator):
        """Test StatutoryRAGValidator initialization."""
        assert validator is not None
        assert validator.corpus_loader is not None

    def test_validate_extraction_valid(self, validator, sample_extraction):
        """Test validation of a valid extraction."""
        result = validator.validate_extraction(sample_extraction)

        assert isinstance(result, ValidationResult)
        assert result.compliance_score > 0

    def test_validate_extraction_invalid(self, validator, invalid_extraction):
        """Test validation of an invalid extraction."""
        result = validator.validate_extraction(invalid_extraction)

        assert isinstance(result, ValidationResult)
        # Should have low compliance or conflicts
        assert result.compliance_score < 1.0 or len(result.conflicts) > 0

    def test_validate_extraction_no_corpus(self):
        """Test validation with no corpus loaded."""
        validator = StatutoryRAGValidator("/nonexistent/path")
        result = validator.validate_extraction({"text": "Test"})

        assert result.is_valid is False
        assert len(result.conflicts) > 0

    def test_validate_extraction_empty(self, validator):
        """Test validation of empty extraction."""
        result = validator.validate_extraction({})

        assert result.is_valid is False
        assert len(result.conflicts) > 0

    def test_extract_claims_from_dict(self, validator, sample_extraction):
        """Test claim extraction from dictionary."""
        claims = validator._extract_claims(sample_extraction)

        assert len(claims) > 0
        assert any("best interests" in claim.lower() for claim in claims)

    def test_extract_claims_from_nested_dict(self, validator):
        """Test claim extraction from nested dictionary."""
        extraction = {
            "main": {
                "text": "Main claim",
                "nested": {
                    "finding": "Nested finding"
                }
            }
        }

        claims = validator._extract_claims(extraction)

        assert "Main claim" in claims
        assert "Nested finding" in claims

    def test_extract_claims_from_list(self, validator):
        """Test claim extraction from list."""
        extraction = {
            "findings": [
                "First finding",
                "Second finding"
            ]
        }

        claims = validator._extract_claims(extraction)

        assert "First finding" in claims
        assert "Second finding" in claims

    def test_extract_claims_deduplication(self, validator):
        """Test that extracted claims are deduplicated."""
        extraction = {
            "text": "Duplicate claim",
            "summary": "Duplicate claim",
            "conclusion": "Duplicate claim"
        }

        claims = validator._extract_claims(extraction)

        # Should only have one instance of "Duplicate claim"
        assert claims.count("Duplicate claim") == 1

    def test_retrieve_statutes(self, validator):
        """Test statute retrieval for claims."""
        claims = ["best interests of the child", "parenting arrangement"]

        statutes = validator._retrieve_statutes(claims)

        assert len(statutes) > 0
        assert any(s.get("section") == "60CC" for s in statutes)

    def test_extract_keywords(self, validator):
        """Test keyword extraction from text."""
        text = "The court must consider the best interests of the child and their relationship with parents."

        keywords = validator._extract_keywords(text)

        assert len(keywords) > 0
        assert "court" in keywords
        assert "child" in keywords
        # Stop words should be removed
        assert "that" not in keywords
        assert "this" not in keywords

    def test_check_compliance_high_score(self, validator):
        """Test compliance checking with high overlap."""
        claims = [
            "The court must consider the best interests of the child",
            "The relationship with both parents is important"
        ]

        statutes = validator.corpus_loader.search_by_keyword("child", top_k=5)

        score = validator._check_compliance(claims, statutes)

        assert score > 0

    def test_check_compliance_no_statutes(self, validator):
        """Test compliance checking with no statutes."""
        claims = ["Some claim"]
        score = validator._check_compliance(claims, [])

        assert score == 0.0

    def test_detect_conflicts_missing_elements(self, validator):
        """Test conflict detection for missing required elements."""
        claims = ["Property division is ordered"]

        # Get property division statute
        statutes = [
            s for s in validator.corpus_loader.search_by_keyword("property")
            if s.get("section") == "79"
        ]

        conflicts = validator._detect_conflicts(claims, statutes)

        # Should detect missing required elements
        assert len(conflicts) > 0

    def test_detect_conflicts_no_issues(self, validator):
        """Test conflict detection with compliant extraction."""
        claims = [
            "The asset pool includes matrimonial property",
            "Financial contributions were assessed",
            "Non-financial contributions were considered"
        ]

        statutes = validator.corpus_loader.search_by_keyword("property")

        conflicts = validator._detect_conflicts(claims, statutes)

        # Should have fewer or no conflicts
        assert isinstance(conflicts, list)

    def test_generate_recommendations_no_conflicts(self, validator):
        """Test recommendation generation with no conflicts."""
        recommendations = validator._generate_recommendations([])

        assert len(recommendations) > 0
        assert any("compliant" in r.lower() for r in recommendations)

    def test_generate_recommendations_with_conflicts(self, validator):
        """Test recommendation generation with conflicts."""
        conflicts = [
            "Insufficient elements for Family Law Act 1975 s60CC: found 0/2"
        ]

        recommendations = validator._generate_recommendations(conflicts)

        assert len(recommendations) > 0
        assert any("element" in r.lower() for r in recommendations)

    def test_validation_result_supporting_citations(self, validator, sample_extraction):
        """Test that validation result includes supporting citations."""
        result = validator.validate_extraction(sample_extraction)

        assert isinstance(result.supporting_citations, list)
        # Should have at least one citation
        if len(result.supporting_citations) > 0:
            assert isinstance(result.supporting_citations[0], StatutoryReference)

    def test_validation_with_context(self, validator, sample_extraction):
        """Test validation with additional context."""
        context = "This is a parenting matter involving custody arrangements."

        result = validator.validate_extraction(sample_extraction, context=context)

        assert isinstance(result, ValidationResult)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestValidationIntegration:
    """Integration tests for the validation system."""

    def test_end_to_end_validation(self, temp_corpus_dir):
        """Test complete validation workflow."""
        # Create validator
        validator = StatutoryRAGValidator(temp_corpus_dir)

        # Create extraction
        extraction = {
            "text": "The court considered the best interests of the child.",
            "legal_test": "Best interests test",
            "findings": [
                "Child's views were obtained",
                "Relationship with parents assessed"
            ]
        }

        # Validate
        result = validator.validate_extraction(extraction)

        # Check result
        assert isinstance(result, ValidationResult)
        assert result.compliance_score >= 0
        assert result.compliance_score <= 1.0

    def test_corpus_loader_and_validator_integration(self, temp_corpus_dir):
        """Test integration between CorpusLoader and Validator."""
        # Create separate instances
        loader = CorpusLoader(temp_corpus_dir)
        validator = StatutoryRAGValidator(temp_corpus_dir)

        # Both should have loaded the same data
        assert len(loader.acts) == len(validator.corpus_loader.acts)

    def test_validation_with_multiple_extractions(self, validator):
        """Test validating multiple extractions."""
        extractions = [
            {
                "text": "Best interests of child considered",
                "legal_test": "Best interests test"
            },
            {
                "text": "Property division ordered",
                "legal_test": "Property division test"
            }
        ]

        results = [validator.validate_extraction(e) for e in extractions]

        assert len(results) == 2
        assert all(isinstance(r, ValidationResult) for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
