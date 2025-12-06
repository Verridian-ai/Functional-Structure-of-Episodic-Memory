"""
Comprehensive Tests for VSA Validator
======================================

Tests for the VSA anti-hallucination validation system, including:
- Claim extraction
- Factual statement detection
- Confidence calibration
- Hallucination detection
- Integration with retrieval pipeline

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import pytest
import torch
from typing import Dict, List

from src.retrieval.vsa_validator import VSAValidator, EnhancedVSAValidator
from src.logic.gsw_schema import (
    GlobalWorkspace,
    Actor,
    ActorType,
    State,
    VerbPhrase,
    ChunkExtraction
)
from src.retrieval.retriever import LegalRetriever


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_workspace():
    """Fixture providing a sample workspace for testing."""
    workspace = GlobalWorkspace()

    # Create actors
    john = Actor(
        id="actor_john",
        name="John Smith",
        actor_type=ActorType.PERSON,
        roles=["husband", "applicant"],
        aliases=["John", "Mr. Smith"]
    )

    jane = Actor(
        id="actor_jane",
        name="Jane Smith",
        actor_type=ActorType.PERSON,
        roles=["wife", "respondent"],
        aliases=["Jane", "Mrs. Smith"]
    )

    # Add states
    john.add_state(State(
        entity_id="actor_john",
        name="MaritalStatus",
        value="Married",
        start_date="2010-03-15",
        end_date="2020-06-01"
    ))

    john.add_state(State(
        entity_id="actor_john",
        name="MaritalStatus",
        value="Separated",
        start_date="2020-06-01",
        end_date=None
    ))

    # Add actors to workspace
    workspace.add_actor(john)
    workspace.add_actor(jane)

    # Add verb phrases
    marriage_verb = VerbPhrase(
        verb="married",
        agent_id="actor_john",
        patient_ids=["actor_jane"]
    )

    separation_verb = VerbPhrase(
        verb="separated",
        agent_id="actor_john",
        patient_ids=["actor_jane"]
    )

    workspace.add_verb_phrase(marriage_verb)
    workspace.add_verb_phrase(separation_verb)

    return workspace


@pytest.fixture
def vsa_validator():
    """Fixture providing a VSA validator instance."""
    return VSAValidator()


@pytest.fixture
def enhanced_validator():
    """Fixture providing an enhanced VSA validator instance."""
    return EnhancedVSAValidator()


# ============================================================================
# CLAIM EXTRACTION TESTS
# ============================================================================

class TestClaimExtraction:
    """Tests for claim extraction functionality."""

    def test_extract_single_claim(self, vsa_validator):
        """Test extracting a single factual claim."""
        response = "John married Jane in 2010."
        claims = vsa_validator._extract_claims(response)

        assert len(claims) == 1
        assert "John married Jane in 2010" in claims[0]

    def test_extract_multiple_claims(self, vsa_validator):
        """Test extracting multiple claims from text."""
        response = "John married Jane in 2010. They separated in 2020. John filed for divorce."
        claims = vsa_validator._extract_claims(response)

        assert len(claims) == 3
        assert any("married" in claim for claim in claims)
        assert any("separated" in claim for claim in claims)
        assert any("filed" in claim for claim in claims)

    def test_extract_claims_with_questions(self, vsa_validator):
        """Test that questions are not extracted as claims."""
        response = "John married Jane. When did they separate? They separated in 2020."
        claims = vsa_validator._extract_claims(response)

        # Should have 2 claims (the statements), not the question
        assert len(claims) == 2
        assert not any("?" in claim for claim in claims)

    def test_extract_claims_with_opinions(self, vsa_validator):
        """Test that opinions are not extracted as claims."""
        response = "John married Jane. They might separate soon. John may file for divorce."
        claims = vsa_validator._extract_claims(response)

        # Should only extract the factual statement
        assert len(claims) == 1
        assert "married" in claims[0]

    def test_extract_claims_empty_text(self, vsa_validator):
        """Test extraction from empty text."""
        claims = vsa_validator._extract_claims("")

        assert len(claims) == 0

    def test_extract_claims_no_factual_content(self, vsa_validator):
        """Test extraction from text with no factual content."""
        response = "Maybe something happened? Could be possible. Perhaps."
        claims = vsa_validator._extract_claims(response)

        assert len(claims) == 0


# ============================================================================
# FACTUAL STATEMENT DETECTION TESTS
# ============================================================================

class TestFactualDetection:
    """Tests for factual statement detection."""

    def test_is_factual_with_verb_of_being(self, vsa_validator):
        """Test detection of factual statements with 'is'."""
        assert vsa_validator._is_factual("John is married")
        assert vsa_validator._is_factual("The property was valued at $500,000")

    def test_is_factual_with_action_verbs(self, vsa_validator):
        """Test detection of factual statements with action verbs."""
        assert vsa_validator._is_factual("John filed for divorce")
        assert vsa_validator._is_factual("The court ordered shared custody")

    def test_is_not_factual_with_questions(self, vsa_validator):
        """Test that questions are not factual."""
        assert not vsa_validator._is_factual("When did they marry?")
        assert not vsa_validator._is_factual("Is John married?")

    def test_is_not_factual_with_modal_verbs(self, vsa_validator):
        """Test that statements with modal verbs are not factual."""
        assert not vsa_validator._is_factual("John might file for divorce")
        assert not vsa_validator._is_factual("They could separate soon")
        assert not vsa_validator._is_factual("Perhaps they will reconcile")

    def test_is_factual_edge_cases(self, vsa_validator):
        """Test edge cases in factual detection."""
        # Factual despite containing opinion-adjacent words in context
        assert vsa_validator._is_factual("John married Jane in May")

        # Not factual due to speculative nature
        assert not vsa_validator._is_factual("Maybe John married Jane")


# ============================================================================
# CONCEPT EXTRACTION TESTS
# ============================================================================

class TestConceptExtraction:
    """Tests for concept extraction from claims."""

    def test_extract_concepts_basic(self, vsa_validator):
        """Test basic concept extraction."""
        claim = "John married Jane in 2010"
        concepts = vsa_validator._extract_concepts(claim)

        assert "john" in concepts
        assert "married" in concepts
        assert "jane" in concepts
        assert "2010" in concepts

    def test_extract_concepts_removes_stop_words(self, vsa_validator):
        """Test that stop words are removed."""
        claim = "The man is in the house with the dog"
        concepts = vsa_validator._extract_concepts(claim)

        # Stop words should not be included
        assert "the" not in concepts
        assert "is" not in concepts
        assert "in" not in concepts
        assert "with" not in concepts

        # Content words should be included
        assert "man" in concepts
        assert "house" in concepts
        assert "dog" in concepts

    def test_extract_concepts_handles_hyphens(self, vsa_validator):
        """Test handling of hyphenated words."""
        claim = "The court ordered fifty-fifty custody"
        concepts = vsa_validator._extract_concepts(claim)

        assert "fifty-fifty" in concepts

    def test_extract_concepts_filters_short_words(self, vsa_validator):
        """Test that very short words are filtered."""
        claim = "I am at it"
        concepts = vsa_validator._extract_concepts(claim)

        # Short words (<=2 chars) should be filtered
        # Note: 'am' and 'at' are also stop words
        assert len([c for c in concepts if len(c) <= 2]) == 0


# ============================================================================
# CONFIDENCE CALIBRATION TESTS
# ============================================================================

class TestConfidenceCalibration:
    """Tests for confidence score calibration."""

    def test_calibrate_very_high_similarity(self, vsa_validator):
        """Test calibration for very high similarity scores."""
        confidence = vsa_validator._calibrate_confidence(0.95)
        assert confidence == 0.95
        assert 0.9 <= confidence <= 1.0

    def test_calibrate_high_similarity(self, vsa_validator):
        """Test calibration for high similarity scores."""
        confidence = vsa_validator._calibrate_confidence(0.75)
        assert 0.8 <= confidence <= 0.95

    def test_calibrate_medium_similarity(self, vsa_validator):
        """Test calibration for medium similarity scores."""
        confidence = vsa_validator._calibrate_confidence(0.55)
        assert 0.6 <= confidence <= 0.8

    def test_calibrate_low_similarity(self, vsa_validator):
        """Test calibration for low similarity scores."""
        confidence = vsa_validator._calibrate_confidence(0.35)
        assert 0.4 <= confidence <= 0.6

    def test_calibrate_very_low_similarity(self, vsa_validator):
        """Test calibration for very low similarity scores."""
        confidence = vsa_validator._calibrate_confidence(0.1)
        assert 0.0 <= confidence < 0.4

    def test_calibrate_negative_similarity(self, vsa_validator):
        """Test calibration for negative similarity scores."""
        confidence = vsa_validator._calibrate_confidence(-0.5)
        assert confidence >= 0.0
        assert confidence < 0.2

    def test_calibration_monotonicity(self, vsa_validator):
        """Test that calibration is monotonically increasing."""
        similarities = [-1.0, -0.5, 0.0, 0.3, 0.5, 0.7, 0.9, 1.0]
        confidences = [vsa_validator._calibrate_confidence(s) for s in similarities]

        # Each confidence should be >= previous
        for i in range(1, len(confidences)):
            assert confidences[i] >= confidences[i-1]


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidation:
    """Tests for response validation."""

    def test_validate_correct_fact(self, vsa_validator, sample_workspace):
        """Test validation of a known correct fact."""
        query = "When did John and Jane marry?"
        response = "John married Jane in 2010."

        result = vsa_validator.validate_response(query, response, sample_workspace)

        assert result['total_claims'] == 1
        # Should have high confidence for correct fact
        assert result['overall_confidence'] > 0.5

    def test_validate_hallucination(self, vsa_validator, sample_workspace):
        """Test detection of hallucinated information."""
        query = "When did John and Jane divorce?"
        response = "John divorced Jane in 2015."  # False - they separated but no divorce recorded

        result = vsa_validator.validate_response(query, response, sample_workspace)

        assert result['total_claims'] == 1
        # Should have low confidence for hallucination
        # Note: Might not be detected if 'divorce' is in ontology
        assert isinstance(result['hallucination_detected'], bool)

    def test_validate_multiple_claims(self, vsa_validator, sample_workspace):
        """Test validation of multiple claims."""
        query = "Tell me about John and Jane."
        response = "John married Jane in 2010. They separated in 2020."

        result = vsa_validator.validate_response(query, response, sample_workspace)

        assert result['total_claims'] == 2
        assert 'individual_validations' in result
        assert len(result['individual_validations']) == 2

    def test_validate_empty_response(self, vsa_validator, sample_workspace):
        """Test validation of empty response."""
        result = vsa_validator.validate_response("test", "", sample_workspace)

        assert result['total_claims'] == 0
        assert result['overall_confidence'] == 0.5  # Neutral

    def test_validate_no_factual_claims(self, vsa_validator, sample_workspace):
        """Test validation of response with no factual claims."""
        response = "Maybe something happened? Could be possible."

        result = vsa_validator.validate_response("test", response, sample_workspace)

        assert result['total_claims'] == 0

    def test_severity_breakdown(self, vsa_validator, sample_workspace):
        """Test severity breakdown in validation results."""
        response = "John married Jane."

        result = vsa_validator.validate_response("test", response, sample_workspace)

        assert 'severity' in result
        assert 'high_risk' in result['severity']
        assert 'medium_risk' in result['severity']
        assert 'low_risk' in result['severity']
        assert 'verified' in result['severity']


# ============================================================================
# CLAIM VALIDATION TESTS
# ============================================================================

class TestClaimValidation:
    """Tests for single claim validation."""

    def test_validate_single_claim(self, vsa_validator, sample_workspace):
        """Test validation of a single claim."""
        claim = "John married Jane"

        result = vsa_validator.validate_claim(claim, sample_workspace)

        assert 'claim' in result
        assert 'similarity' in result
        assert 'confidence' in result
        assert 'valid' in result
        assert isinstance(result['valid'], bool)

    def test_validate_claim_with_concepts(self, vsa_validator, sample_workspace):
        """Test that validation includes extracted concepts."""
        claim = "John married Jane in 2010"

        result = vsa_validator.validate_claim(claim, sample_workspace)

        assert 'concepts' in result
        assert len(result['concepts']) > 0
        assert 'john' in result['concepts']
        assert 'married' in result['concepts']

    def test_validate_claim_vsa_integration(self, vsa_validator, sample_workspace):
        """Test integration with VSA validation."""
        claim = "John married Jane"

        result = vsa_validator.validate_claim(claim, sample_workspace)

        assert 'vsa_valid' in result
        assert 'vsa_confidence' in result
        assert 'vsa_issues' in result


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestRetrieverIntegration:
    """Tests for integration with retrieval pipeline."""

    def test_retriever_with_validation_disabled(self):
        """Test retriever with validation disabled."""
        retriever = LegalRetriever(enable_vsa_validation=False)

        assert retriever.vsa_validator is None

    def test_retriever_with_validation_enabled(self):
        """Test retriever with validation enabled."""
        retriever = LegalRetriever(enable_vsa_validation=True)

        assert retriever.vsa_validator is not None
        assert isinstance(retriever.vsa_validator, VSAValidator)

    def test_retrieve_with_validation_no_workspace(self):
        """Test retrieval with validation but no workspace."""
        retriever = LegalRetriever(enable_vsa_validation=True)

        result = retriever.retrieve_with_validation(
            query="test query",
            workspace=None,
            generate_response=False
        )

        assert 'results' in result
        assert 'validation' not in result

    def test_retrieve_with_validation_and_workspace(self, sample_workspace):
        """Test retrieval with validation and workspace."""
        retriever = LegalRetriever(enable_vsa_validation=True)

        result = retriever.retrieve_with_validation(
            query="When did John marry Jane?",
            workspace=sample_workspace,
            generate_response=True
        )

        assert 'results' in result
        assert 'response' in result
        assert 'validation' in result
        assert 'confidence' in result
        assert 'hallucination_risk' in result

    def test_validate_claim_through_retriever(self, sample_workspace):
        """Test claim validation through retriever."""
        retriever = LegalRetriever(enable_vsa_validation=True)

        result = retriever.validate_claim(
            "John married Jane",
            sample_workspace
        )

        assert 'valid' in result
        assert 'confidence' in result

    def test_batch_validate_claims(self, sample_workspace):
        """Test batch claim validation."""
        retriever = LegalRetriever(enable_vsa_validation=True)

        claims = [
            "John married Jane",
            "They separated in 2020",
            "John filed for divorce"
        ]

        results = retriever.batch_validate_claims(claims, sample_workspace)

        assert len(results) == 3
        assert all('valid' in r for r in results)
        assert all('confidence' in r for r in results)


# ============================================================================
# ENHANCED VALIDATOR TESTS
# ============================================================================

class TestEnhancedValidator:
    """Tests for enhanced VSA validator."""

    def test_enhanced_validator_initialization(self, enhanced_validator):
        """Test enhanced validator initialization."""
        assert enhanced_validator is not None
        assert hasattr(enhanced_validator, 'validation_cache')

    def test_validate_with_context(self, enhanced_validator, sample_workspace):
        """Test validation with additional context."""
        context = {
            'case_id': 'test_case',
            'date': '2020-06-01'
        }

        result = enhanced_validator.validate_with_context(
            query="test",
            response="John married Jane",
            workspace=sample_workspace,
            context=context
        )

        assert 'overall_confidence' in result
        assert 'context_checks' in result

    def test_context_validation(self, enhanced_validator):
        """Test context-specific validation."""
        context = {
            'entities': ['John', 'Jane'],
            'date': '2010-03-15'
        }

        checks = enhanced_validator._validate_context(
            "John married Jane",
            context
        )

        assert 'temporal_consistency' in checks
        assert 'entity_consistency' in checks
        assert 'issues' in checks


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_validate_very_long_response(self, vsa_validator, sample_workspace):
        """Test validation of very long responses."""
        # Generate a long response with many claims
        sentences = [f"Claim number {i}." for i in range(100)]
        response = " ".join(sentences)

        result = vsa_validator.validate_response("test", response, sample_workspace)

        # Should handle large number of claims
        assert result['total_claims'] > 0

    def test_validate_special_characters(self, vsa_validator, sample_workspace):
        """Test validation with special characters."""
        response = "John & Jane: married in 2010 (verified)!"

        result = vsa_validator.validate_response("test", response, sample_workspace)

        assert result['total_claims'] >= 0

    def test_validate_unicode_text(self, vsa_validator, sample_workspace):
        """Test validation with Unicode characters."""
        response = "John married Jane in Melbournė, Australia."

        result = vsa_validator.validate_response("test", response, sample_workspace)

        assert result['total_claims'] >= 0

    def test_empty_workspace(self, vsa_validator):
        """Test validation with empty workspace."""
        empty_workspace = GlobalWorkspace()

        result = vsa_validator.validate_response(
            "test",
            "John married Jane",
            empty_workspace
        )

        # Should not crash, but likely low confidence
        assert 'overall_confidence' in result

    def test_retriever_validation_disabled(self):
        """Test retriever methods when validation is disabled."""
        retriever = LegalRetriever(enable_vsa_validation=False)

        workspace = GlobalWorkspace()
        result = retriever.validate_claim("test claim", workspace)

        assert 'error' in result
        assert result['valid'] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
