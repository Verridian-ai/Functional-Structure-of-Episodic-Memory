"""
Comprehensive Tests for the Evaluation Module
==============================================

Tests for the multi-judge evaluation system, including:
- JudgeModel enum values
- JudgeEvaluation creation
- AggregatedEvaluation creation
- MultiJudgeEvaluator._calculate_consensus()
- MultiJudgeEvaluator._aggregate_evaluations()

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import pytest
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import json

from src.evaluation.multi_judge import (
    JudgeModel,
    JudgeEvaluation,
    AggregatedEvaluation,
    MultiJudgeEvaluator
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_api_key():
    """Fixture providing a mock API key."""
    return "test_api_key_12345"


@pytest.fixture
def evaluator(mock_api_key):
    """Fixture providing a MultiJudgeEvaluator instance."""
    return MultiJudgeEvaluator(api_key=mock_api_key)


@pytest.fixture
def single_judge_evaluator(mock_api_key):
    """Fixture providing an evaluator with a single judge."""
    return MultiJudgeEvaluator(
        judges=[JudgeModel.GPT4O],
        api_key=mock_api_key
    )


@pytest.fixture
def sample_judge_evaluations():
    """Fixture providing sample judge evaluations."""
    return [
        JudgeEvaluation(
            model=JudgeModel.GPT4O,
            score=8.5,
            issues=["Minor clarity issue"],
            strengths=["Accurate", "Well-structured"],
            reasoning="Good response overall"
        ),
        JudgeEvaluation(
            model=JudgeModel.CLAUDE,
            score=8.0,
            issues=["Could be more concise"],
            strengths=["Correct information", "Good context usage"],
            reasoning="Solid response"
        ),
        JudgeEvaluation(
            model=JudgeModel.GEMINI,
            score=8.2,
            issues=[],
            strengths=["Clear", "Complete"],
            reasoning="Excellent response"
        )
    ]


@pytest.fixture
def sample_query():
    """Fixture providing a sample user query."""
    return "What are the requirements for parenting orders under the Family Law Act?"


@pytest.fixture
def sample_response():
    """Fixture providing a sample AI response."""
    return """
    Under the Family Law Act 1975, parenting orders must prioritize the best interests
    of the child. The court considers factors including the child's views, their
    relationship with each parent, and the capacity of each parent to provide for
    the child's needs.
    """


@pytest.fixture
def sample_context():
    """Fixture providing sample context."""
    return """
    Family Law Act 1975, Section 60CC outlines the best interests considerations
    for parenting orders. Key factors include the child's safety, their relationship
    with parents, and any family violence.
    """


# ============================================================================
# JUDGE MODEL ENUM TESTS
# ============================================================================

class TestJudgeModel:
    """Tests for JudgeModel enum."""

    def test_judge_model_values(self):
        """Test that all JudgeModel enum values are correctly defined."""
        assert JudgeModel.GPT4O.value == "openai/gpt-4o"
        assert JudgeModel.CLAUDE.value == "anthropic/claude-3-sonnet"
        assert JudgeModel.GEMINI.value == "google/gemini-2.0-flash"

    def test_judge_model_membership(self):
        """Test enum membership checks."""
        models = [JudgeModel.GPT4O, JudgeModel.CLAUDE, JudgeModel.GEMINI]
        assert len(models) == 3
        assert JudgeModel.GPT4O in models

    def test_judge_model_iteration(self):
        """Test iterating over judge models."""
        all_judges = list(JudgeModel)
        assert len(all_judges) == 3

    def test_judge_model_string_values(self):
        """Test that enum values are valid OpenRouter model IDs."""
        for model in JudgeModel:
            assert "/" in model.value  # Should have provider/model format
            assert isinstance(model.value, str)

    def test_judge_model_names(self):
        """Test judge model names."""
        assert JudgeModel.GPT4O.name == "GPT4O"
        assert JudgeModel.CLAUDE.name == "CLAUDE"
        assert JudgeModel.GEMINI.name == "GEMINI"


# ============================================================================
# JUDGE EVALUATION TESTS
# ============================================================================

class TestJudgeEvaluation:
    """Tests for JudgeEvaluation dataclass."""

    def test_create_judge_evaluation_basic(self):
        """Test creating a basic JudgeEvaluation."""
        eval = JudgeEvaluation(
            model=JudgeModel.GPT4O,
            score=7.5,
            issues=["Issue 1"],
            strengths=["Strength 1"],
            reasoning="Test reasoning"
        )

        assert eval.model == JudgeModel.GPT4O
        assert eval.score == 7.5
        assert len(eval.issues) == 1
        assert len(eval.strengths) == 1
        assert eval.reasoning == "Test reasoning"

    def test_judge_evaluation_default_fields(self):
        """Test JudgeEvaluation with default field values."""
        eval = JudgeEvaluation(
            model=JudgeModel.CLAUDE,
            score=8.0
        )

        assert eval.issues == []
        assert eval.strengths == []
        assert eval.reasoning == ""

    def test_judge_evaluation_score_range(self):
        """Test JudgeEvaluation accepts valid score range."""
        for score in [1.0, 5.0, 10.0]:
            eval = JudgeEvaluation(model=JudgeModel.GPT4O, score=score)
            assert eval.score == score

    def test_judge_evaluation_multiple_issues(self):
        """Test JudgeEvaluation with multiple issues."""
        issues = ["Issue 1", "Issue 2", "Issue 3"]
        eval = JudgeEvaluation(
            model=JudgeModel.GEMINI,
            score=6.0,
            issues=issues
        )

        assert len(eval.issues) == 3
        assert eval.issues == issues

    def test_judge_evaluation_multiple_strengths(self):
        """Test JudgeEvaluation with multiple strengths."""
        strengths = ["Strength 1", "Strength 2"]
        eval = JudgeEvaluation(
            model=JudgeModel.GPT4O,
            score=9.0,
            strengths=strengths
        )

        assert len(eval.strengths) == 2
        assert eval.strengths == strengths


# ============================================================================
# AGGREGATED EVALUATION TESTS
# ============================================================================

class TestAggregatedEvaluation:
    """Tests for AggregatedEvaluation dataclass."""

    def test_create_aggregated_evaluation(self, sample_judge_evaluations):
        """Test creating an AggregatedEvaluation."""
        agg_eval = AggregatedEvaluation(
            mean_score=8.2,
            median_score=8.2,
            consensus_level=0.9,
            individual_evaluations=sample_judge_evaluations,
            combined_issues=["Issue 1", "Issue 2"],
            combined_strengths=["Strength 1", "Strength 2"]
        )

        assert agg_eval.mean_score == 8.2
        assert agg_eval.median_score == 8.2
        assert agg_eval.consensus_level == 0.9
        assert len(agg_eval.individual_evaluations) == 3
        assert len(agg_eval.combined_issues) == 2
        assert len(agg_eval.combined_strengths) == 2

    def test_aggregated_evaluation_default_fields(self):
        """Test AggregatedEvaluation with default fields."""
        agg_eval = AggregatedEvaluation(
            mean_score=7.5,
            median_score=7.5,
            consensus_level=0.8
        )

        assert agg_eval.individual_evaluations == []
        assert agg_eval.combined_issues == []
        assert agg_eval.combined_strengths == []

    def test_aggregated_evaluation_consensus_range(self):
        """Test consensus_level is within valid range."""
        for consensus in [0.0, 0.5, 1.0]:
            agg_eval = AggregatedEvaluation(
                mean_score=8.0,
                median_score=8.0,
                consensus_level=consensus
            )
            assert 0.0 <= agg_eval.consensus_level <= 1.0


# ============================================================================
# MULTI-JUDGE EVALUATOR TESTS
# ============================================================================

class TestMultiJudgeEvaluator:
    """Tests for MultiJudgeEvaluator class."""

    def test_initialization_with_api_key(self, mock_api_key):
        """Test evaluator initialization with API key."""
        evaluator = MultiJudgeEvaluator(api_key=mock_api_key)

        assert evaluator.api_key == mock_api_key
        assert len(evaluator.judges) == 3  # Default: all judges

    def test_initialization_default_judges(self, mock_api_key):
        """Test that default judges are all available models."""
        evaluator = MultiJudgeEvaluator(api_key=mock_api_key)

        assert JudgeModel.GPT4O in evaluator.judges
        assert JudgeModel.CLAUDE in evaluator.judges
        assert JudgeModel.GEMINI in evaluator.judges

    def test_initialization_custom_judges(self, mock_api_key):
        """Test initialization with custom judge list."""
        custom_judges = [JudgeModel.GPT4O, JudgeModel.CLAUDE]
        evaluator = MultiJudgeEvaluator(
            judges=custom_judges,
            api_key=mock_api_key
        )

        assert len(evaluator.judges) == 2
        assert JudgeModel.GEMINI not in evaluator.judges

    def test_initialization_from_env_variable(self):
        """Test API key loaded from environment variable."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "env_key"}):
            evaluator = MultiJudgeEvaluator()
            assert evaluator.api_key == "env_key"

    def test_initialization_no_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="No API key found"):
                MultiJudgeEvaluator()

    def test_calculate_consensus_perfect(self, evaluator):
        """Test consensus calculation with identical scores."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=8.0),
            JudgeEvaluation(model=JudgeModel.CLAUDE, score=8.0),
            JudgeEvaluation(model=JudgeModel.GEMINI, score=8.0)
        ]

        consensus = evaluator._calculate_consensus(evaluations)

        assert consensus == 1.0  # Perfect consensus

    def test_calculate_consensus_high_agreement(self, evaluator):
        """Test consensus calculation with high agreement."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=8.0),
            JudgeEvaluation(model=JudgeModel.CLAUDE, score=8.2),
            JudgeEvaluation(model=JudgeModel.GEMINI, score=7.9)
        ]

        consensus = evaluator._calculate_consensus(evaluations)

        assert consensus > 0.8  # High consensus

    def test_calculate_consensus_low_agreement(self, evaluator):
        """Test consensus calculation with low agreement."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=3.0),
            JudgeEvaluation(model=JudgeModel.CLAUDE, score=7.0),
            JudgeEvaluation(model=JudgeModel.GEMINI, score=9.0)
        ]

        consensus = evaluator._calculate_consensus(evaluations)

        assert consensus < 0.5  # Low consensus

    def test_calculate_consensus_single_evaluation(self, evaluator):
        """Test consensus with only one evaluation."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=8.0)
        ]

        consensus = evaluator._calculate_consensus(evaluations)

        assert consensus == 1.0  # Perfect consensus with single judge

    def test_calculate_consensus_empty_list(self, evaluator):
        """Test consensus with empty evaluation list."""
        consensus = evaluator._calculate_consensus([])

        assert consensus == 1.0  # Default to perfect consensus

    def test_aggregate_evaluations_basic(self, evaluator, sample_judge_evaluations):
        """Test basic aggregation of evaluations."""
        agg_eval = evaluator._aggregate_evaluations(sample_judge_evaluations)

        assert isinstance(agg_eval, AggregatedEvaluation)
        assert agg_eval.mean_score > 0
        assert agg_eval.median_score > 0
        assert 0.0 <= agg_eval.consensus_level <= 1.0
        assert len(agg_eval.individual_evaluations) == 3

    def test_aggregate_evaluations_mean_calculation(self, evaluator):
        """Test mean score calculation in aggregation."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=6.0),
            JudgeEvaluation(model=JudgeModel.CLAUDE, score=8.0),
            JudgeEvaluation(model=JudgeModel.GEMINI, score=10.0)
        ]

        agg_eval = evaluator._aggregate_evaluations(evaluations)

        assert agg_eval.mean_score == 8.0  # (6 + 8 + 10) / 3

    def test_aggregate_evaluations_median_calculation(self, evaluator):
        """Test median score calculation in aggregation."""
        evaluations = [
            JudgeEvaluation(model=JudgeModel.GPT4O, score=6.0),
            JudgeEvaluation(model=JudgeModel.CLAUDE, score=8.0),
            JudgeEvaluation(model=JudgeModel.GEMINI, score=10.0)
        ]

        agg_eval = evaluator._aggregate_evaluations(evaluations)

        assert agg_eval.median_score == 8.0

    def test_aggregate_evaluations_combines_issues(self, evaluator):
        """Test that aggregation combines issues from all judges."""
        evaluations = [
            JudgeEvaluation(
                model=JudgeModel.GPT4O,
                score=7.0,
                issues=["Issue A"]
            ),
            JudgeEvaluation(
                model=JudgeModel.CLAUDE,
                score=7.0,
                issues=["Issue B"]
            )
        ]

        agg_eval = evaluator._aggregate_evaluations(evaluations)

        assert len(agg_eval.combined_issues) == 2
        assert any("GPT4O" in issue for issue in agg_eval.combined_issues)
        assert any("CLAUDE" in issue for issue in agg_eval.combined_issues)

    def test_aggregate_evaluations_combines_strengths(self, evaluator):
        """Test that aggregation combines strengths from all judges."""
        evaluations = [
            JudgeEvaluation(
                model=JudgeModel.GPT4O,
                score=8.0,
                strengths=["Strength A"]
            ),
            JudgeEvaluation(
                model=JudgeModel.CLAUDE,
                score=8.0,
                strengths=["Strength B"]
            )
        ]

        agg_eval = evaluator._aggregate_evaluations(evaluations)

        assert len(agg_eval.combined_strengths) == 2
        assert any("GPT4O" in strength for strength in agg_eval.combined_strengths)
        assert any("CLAUDE" in strength for strength in agg_eval.combined_strengths)

    def test_aggregate_evaluations_empty_list(self, evaluator):
        """Test aggregation with empty evaluation list."""
        agg_eval = evaluator._aggregate_evaluations([])

        assert agg_eval.mean_score == 0.0
        assert agg_eval.median_score == 0.0
        assert agg_eval.consensus_level == 0.0

    def test_build_evaluation_prompt(self, evaluator, sample_query, sample_response, sample_context):
        """Test evaluation prompt building."""
        prompt = evaluator._build_evaluation_prompt(
            sample_query,
            sample_response,
            sample_context
        )

        assert sample_query in prompt
        assert sample_response in prompt
        assert "EVALUATION CRITERIA" in prompt
        assert "JSON" in prompt
        assert "score" in prompt.lower()

    def test_build_evaluation_prompt_truncates_long_context(self, evaluator):
        """Test that long context is truncated in prompt."""
        long_context = "x" * 5000

        prompt = evaluator._build_evaluation_prompt(
            "Query",
            "Response",
            long_context
        )

        # Should be truncated to 2000 chars plus "..."
        assert len([c for c in prompt if c == 'x']) <= 2000

    @pytest.mark.asyncio
    async def test_evaluate_response_mock(self, evaluator, sample_query, sample_response, sample_context):
        """Test evaluate_response with mocked API calls."""
        # Mock the _get_judge_evaluation method
        mock_eval = JudgeEvaluation(
            model=JudgeModel.GPT4O,
            score=8.0,
            issues=["Test issue"],
            strengths=["Test strength"],
            reasoning="Test reasoning"
        )

        with patch.object(
            evaluator,
            '_get_judge_evaluation',
            new=AsyncMock(return_value=mock_eval)
        ):
            result = await evaluator.evaluate_response(
                sample_query,
                sample_response,
                sample_context
            )

            assert isinstance(result, AggregatedEvaluation)
            assert len(result.individual_evaluations) == 3  # All 3 judges

    @pytest.mark.asyncio
    async def test_evaluate_response_handles_failures(self, evaluator):
        """Test that evaluate_response handles judge failures gracefully."""
        # Mock some judges succeeding and some failing
        async def mock_judge_eval(judge, query, response, context):
            if judge == JudgeModel.GPT4O:
                return JudgeEvaluation(model=judge, score=8.0)
            else:
                raise Exception("API Error")

        with patch.object(
            evaluator,
            '_get_judge_evaluation',
            side_effect=mock_judge_eval
        ):
            result = await evaluator.evaluate_response(
                "Query",
                "Response",
                "Context"
            )

            # Should still return a result with the successful evaluations
            assert isinstance(result, AggregatedEvaluation)

    @pytest.mark.asyncio
    async def test_evaluate_response_all_failures(self, evaluator):
        """Test evaluate_response when all judges fail."""
        with patch.object(
            evaluator,
            '_get_judge_evaluation',
            new=AsyncMock(side_effect=Exception("API Error"))
        ):
            result = await evaluator.evaluate_response(
                "Query",
                "Response",
                "Context"
            )

            # Should return a default evaluation
            assert result.mean_score == 0.0
            assert "failed" in result.combined_issues[0].lower()

    @pytest.mark.asyncio
    async def test_get_judge_evaluation_mock_success(self, evaluator):
        """Test _get_judge_evaluation with successful API response."""
        mock_response_data = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "score": 8.5,
                        "issues": ["Minor issue"],
                        "strengths": ["Good accuracy"],
                        "reasoning": "Well done"
                    })
                }
            }]
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = Mock()

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )

            result = await evaluator._get_judge_evaluation(
                JudgeModel.GPT4O,
                "Query",
                "Response",
                "Context"
            )

            assert isinstance(result, JudgeEvaluation)
            assert result.score == 8.5
            assert len(result.issues) == 1
            assert len(result.strengths) == 1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestEvaluationIntegration:
    """Integration tests for the evaluation system."""

    def test_full_evaluation_workflow_mock(self, mock_api_key):
        """Test full evaluation workflow with mocked API."""
        evaluator = MultiJudgeEvaluator(api_key=mock_api_key)

        # Create mock evaluations
        mock_evals = [
            JudgeEvaluation(model=judge, score=8.0 + i * 0.1)
            for i, judge in enumerate(evaluator.judges)
        ]

        # Test aggregation
        result = evaluator._aggregate_evaluations(mock_evals)

        assert isinstance(result, AggregatedEvaluation)
        assert result.mean_score > 0
        assert len(result.individual_evaluations) == len(evaluator.judges)

    def test_consensus_calculation_workflow(self, evaluator):
        """Test consensus calculation in realistic scenario."""
        # Simulate judges with varying agreement
        scenarios = [
            # High consensus
            ([8.0, 8.1, 8.2], "high"),
            # Medium consensus
            ([7.0, 8.0, 9.0], "medium"),
            # Low consensus
            ([3.0, 7.0, 9.5], "low")
        ]

        for scores, expected in scenarios:
            evals = [
                JudgeEvaluation(model=judge, score=score)
                for judge, score in zip(evaluator.judges, scores)
            ]

            consensus = evaluator._calculate_consensus(evals)

            if expected == "high":
                assert consensus > 0.8
            elif expected == "medium":
                assert 0.4 < consensus < 0.8
            else:  # low
                assert consensus < 0.6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
