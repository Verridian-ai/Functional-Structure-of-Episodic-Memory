"""
Tests for GSW Observability Module
==================================

Run with: pytest tests/test_observability.py -v
"""

import pytest
import asyncio
import time
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import os

# Set test environment
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-test"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-test"
os.environ["LANGFUSE_HOST"] = "http://localhost:3001"

# Import modules under test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from observability.langfuse_tracer import (
    GSWTracer,
    GraphActivation,
    TraversalResult,
    LatencyBreakdown,
    OperationType,
    trace_gsw_operation,
    trace_graph_traversal,
    trace_llm_generation,
    _DummySpan,
)

from observability.session_memory import (
    EpisodicSessionTracker,
    SessionState,
    ContextWindow,
    SessionEventType,
)

from observability.scoring import (
    RetrievalScorer,
    AccuracyMetrics,
    ScoringWeights,
    ScoreCategory,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_langfuse():
    """Mock LangFuse client for testing without network calls."""
    with patch('observability.langfuse_tracer.LANGFUSE_AVAILABLE', True):
        with patch('observability.langfuse_tracer.Langfuse') as mock:
            mock_instance = MagicMock()
            mock_instance.trace.return_value = MagicMock()
            mock_instance.score.return_value = None
            mock.return_value = mock_instance
            yield mock_instance


@pytest.fixture
def tracer(mock_langfuse):
    """Create a tracer instance with mocked LangFuse."""
    # Reset singleton
    GSWTracer._instance = None
    t = GSWTracer(enabled=True, debug=True)
    return t


@pytest.fixture
def scorer():
    """Create a scorer instance."""
    return RetrievalScorer(target_score=0.95)


@pytest.fixture
def session_tracker():
    """Create a session tracker instance."""
    return EpisodicSessionTracker(
        session_id="test_session_123",
        tracer=None,
        max_history=100,
    )


# =============================================================================
# TRACER TESTS
# =============================================================================

class TestGSWTracer:
    """Tests for GSWTracer class."""

    def test_singleton_pattern(self, mock_langfuse):
        """Test that GSWTracer is a singleton."""
        GSWTracer._instance = None
        t1 = GSWTracer()
        t2 = GSWTracer()
        assert t1 is t2

    def test_tracer_initialization(self, tracer):
        """Test tracer initializes correctly."""
        assert tracer.enabled == True
        assert tracer.debug == True
        assert tracer._sessions == {}

    def test_start_and_end_trace(self, tracer):
        """Test starting and ending a trace."""
        trace = tracer.start_trace(
            name="test_trace",
            session_id="session_123",
            user_id="user_456",
            metadata={"test": True},
        )

        assert tracer._current_trace is not None

        tracer.end_trace(output={"result": "success"})
        assert tracer._current_trace is None

    def test_latency_timer(self, tracer):
        """Test latency timing."""
        tracer.start_timer("test_operation")
        time.sleep(0.1)  # Sleep 100ms
        elapsed = tracer.stop_timer("test_operation")

        assert elapsed >= 90  # At least 90ms (allow some variance)
        assert elapsed < 200  # But not too long

    def test_latency_breakdown_dict(self):
        """Test LatencyBreakdown to_dict method."""
        breakdown = LatencyBreakdown(
            total_ms=1000,
            graph_traversal_ms=400,
            vector_search_ms=100,
            llm_generation_ms=500,
        )

        d = breakdown.to_dict()
        assert d["total_ms"] == 1000
        assert d["graph_traversal_ms"] == 400
        assert d["llm_generation_ms"] == 500

    def test_latency_breakdown_percentages(self):
        """Test latency percentage calculation."""
        breakdown = LatencyBreakdown(
            total_ms=1000,
            graph_traversal_ms=400,
            llm_generation_ms=600,
        )

        percentages = breakdown.get_breakdown_percentages()
        assert percentages["graph_traversal_ms"] == 40.0
        assert percentages["llm_generation_ms"] == 60.0


class TestGraphActivation:
    """Tests for GraphActivation dataclass."""

    def test_activation_creation(self):
        """Test creating a graph activation."""
        activation = GraphActivation(
            entity_id="actor_123",
            entity_type="Actor",
            entity_name="John Smith",
            activation_score=0.95,
            traversal_depth=2,
            connected_entities=["state_456", "verb_789"],
        )

        assert activation.entity_id == "actor_123"
        assert activation.entity_type == "Actor"
        assert activation.activation_score == 0.95
        assert len(activation.connected_entities) == 2

    def test_activation_defaults(self):
        """Test default values."""
        activation = GraphActivation(
            entity_id="test",
            entity_type="State",
        )

        assert activation.entity_name is None
        assert activation.activation_score == 1.0
        assert activation.traversal_depth == 0
        assert activation.connected_entities == []


class TestTraversalResult:
    """Tests for TraversalResult dataclass."""

    def test_traversal_result_creation(self):
        """Test creating a traversal result."""
        activations = [
            GraphActivation("a1", "Actor", "Test", 0.9, 0, []),
            GraphActivation("a2", "State", "Active", 0.8, 1, ["a1"]),
        ]

        result = TraversalResult(
            query="test query",
            activated_nodes=activations,
            traversal_path=["a1", "a2"],
            total_nodes_scanned=100,
            nodes_activated=2,
            max_depth_reached=1,
            latency_ms=150.5,
        )

        assert result.query == "test query"
        assert len(result.activated_nodes) == 2
        assert result.nodes_activated == 2
        assert result.latency_ms == 150.5


# =============================================================================
# SESSION MEMORY TESTS
# =============================================================================

class TestEpisodicSessionTracker:
    """Tests for session memory tracking."""

    def test_session_initialization(self, session_tracker):
        """Test session tracker initializes correctly."""
        assert session_tracker.session_id == "test_session_123"
        assert session_tracker.current_turn == 0
        assert session_tracker.total_queries == 0

    def test_start_turn(self, session_tracker):
        """Test starting a conversation turn."""
        turn = session_tracker.start_turn("What are my rights?")

        assert turn == 1
        assert session_tracker.current_turn == 1
        assert session_tracker.total_queries == 1
        assert len(session_tracker.events) == 1
        assert session_tracker.events[0].event_type == SessionEventType.QUERY

    def test_record_entity_activation(self, session_tracker):
        """Test recording entity activations."""
        session_tracker.start_turn("Test query")

        session_tracker.record_entity_activation(
            entity_id="actor_1",
            entity_type="Actor",
            entity_name="The Wife",
            relevance=0.95,
            connected_entities=["state_1", "verb_1"],
        )

        assert "actor_1" in session_tracker.entity_activations
        activation = session_tracker.entity_activations["actor_1"]
        assert activation.entity_name == "The Wife"
        assert activation.activation_count == 1
        assert activation.avg_relevance == 0.95

    def test_multiple_activations_same_entity(self, session_tracker):
        """Test multiple activations of the same entity."""
        session_tracker.start_turn("Query 1")
        session_tracker.record_entity_activation("actor_1", "Actor", "Test", 0.9)

        session_tracker.start_turn("Query 2")
        session_tracker.record_entity_activation("actor_1", "Actor", "Test", 0.8)

        activation = session_tracker.entity_activations["actor_1"]
        assert activation.activation_count == 2
        assert abs(activation.avg_relevance - 0.85) < 0.001  # (0.9 + 0.8) / 2

    def test_context_window(self, session_tracker):
        """Test context window management."""
        session_tracker.update_context(
            actors={"a1": {"name": "Actor 1"}, "a2": {"name": "Actor 2"}},
            states={"s1": {"name": "State 1"}},
        )

        assert session_tracker.current_context.total_entities == 3
        breakdown = session_tracker.current_context.size_breakdown
        assert breakdown["actors"] == 2
        assert breakdown["states"] == 1

    def test_session_summary(self, session_tracker):
        """Test getting session summary."""
        session_tracker.start_turn("Query 1")
        session_tracker.record_entity_activation("a1", "Actor", "Test", 0.9)
        session_tracker.end_turn("Response 1", 0.85)

        summary = session_tracker.get_session_summary()

        assert summary["session_id"] == "test_session_123"
        assert summary["total_turns"] == 1
        assert summary["metrics"]["entities_activated"] == 1

    def test_context_growth_data(self, session_tracker):
        """Test context growth chart data."""
        session_tracker.start_turn("Query 1")
        session_tracker.update_context(actors={"a1": {}})
        session_tracker.end_turn()

        session_tracker.start_turn("Query 2")
        session_tracker.update_context(actors={"a1": {}, "a2": {}})
        session_tracker.end_turn()

        growth_data = session_tracker.get_context_growth_chart_data()

        assert len(growth_data) == 2
        assert growth_data[0]["turn"] == 1
        assert growth_data[1]["turn"] == 2


class TestContextWindow:
    """Tests for ContextWindow dataclass."""

    def test_total_entities(self):
        """Test total entity count."""
        window = ContextWindow(
            actors={"a1": {}, "a2": {}},
            states={"s1": {}},
            verb_phrases={"v1": {}},
        )

        assert window.total_entities == 4

    def test_context_hash(self):
        """Test context hashing for change detection."""
        window1 = ContextWindow(actors={"a1": {}, "a2": {}})
        window2 = ContextWindow(actors={"a1": {}, "a2": {}})
        window3 = ContextWindow(actors={"a1": {}, "a3": {}})

        assert window1.compute_hash() == window2.compute_hash()
        assert window1.compute_hash() != window3.compute_hash()


# =============================================================================
# SCORING TESTS
# =============================================================================

class TestScoringWeights:
    """Tests for scoring weight configuration."""

    def test_default_weights_validate(self):
        """Test default weights sum to 1.0."""
        weights = ScoringWeights()
        assert weights.validate() == True

    def test_custom_weights_invalid(self):
        """Test invalid custom weights."""
        weights = ScoringWeights(
            entity_relevance=0.5,
            structural_accuracy=0.5,
            # Other weights are 0.35 by default, so total > 1.0
        )
        assert weights.validate() == False


class TestAccuracyMetrics:
    """Tests for accuracy metrics."""

    def test_precision_calculation(self):
        """Test precision calculation."""
        metrics = AccuracyMetrics(
            true_positives=8,
            false_positives=2,
            false_negatives=3,
        )

        assert metrics.precision == 0.8  # 8 / (8 + 2)

    def test_recall_calculation(self):
        """Test recall calculation."""
        metrics = AccuracyMetrics(
            true_positives=8,
            false_positives=2,
            false_negatives=2,
        )

        assert metrics.recall == 0.8  # 8 / (8 + 2)

    def test_f1_score(self):
        """Test F1 score calculation."""
        metrics = AccuracyMetrics(
            true_positives=8,
            false_positives=2,
            false_negatives=2,
        )

        # precision = 0.8, recall = 0.8
        # f1 = 2 * (0.8 * 0.8) / (0.8 + 0.8) = 0.8
        assert abs(metrics.f1_score - 0.8) < 0.001

    def test_meets_target(self):
        """Test target threshold checking."""
        metrics = AccuracyMetrics(composite_score=0.96)
        assert metrics.meets_target(0.95) == True

        metrics.composite_score = 0.90
        assert metrics.meets_target(0.95) == False


class TestRetrievalScorer:
    """Tests for RetrievalScorer class."""

    def test_scorer_initialization(self, scorer):
        """Test scorer initializes correctly."""
        assert scorer.target_score == 0.95
        assert scorer.weights.validate() == True

    def test_entity_relevance_scoring(self, scorer):
        """Test entity relevance calculation."""
        retrieved = [
            {"id": "a1"},
            {"id": "a2"},
            {"id": "a3"},
        ]
        expected = [
            {"id": "a1"},
            {"id": "a2"},
            {"id": "a4"},
        ]

        score = scorer.score_entity_relevance(retrieved, expected)

        # Jaccard: intersection = {a1, a2} = 2, union = {a1, a2, a3, a4} = 4
        assert abs(score - 0.5) < 0.001

    def test_entity_relevance_perfect(self, scorer):
        """Test perfect entity relevance."""
        entities = [{"id": "a1"}, {"id": "a2"}]

        score = scorer.score_entity_relevance(entities, entities)
        assert score == 1.0

    def test_temporal_coherence_valid_dates(self, scorer):
        """Test temporal coherence with valid dates."""
        entities = [
            {"id": "s1", "type": "state", "start_date": "2020-01-15"},
            {"id": "s2", "type": "state", "start_date": "2021-06-20"},
        ]

        score = scorer.score_temporal_coherence(entities)
        assert score > 0.5  # Should be high for valid, ordered dates

    def test_legal_precision_with_citations(self, scorer):
        """Test legal precision scoring with citations."""
        response = """
        Under Section 79 of the Family Law Act 1975, property division
        follows the four-step process. See also Section 60CC for children's
        best interests. The case of Mallet v Mallet [1984] HCA 21 is relevant.
        """

        score = scorer.score_legal_precision(response)
        assert score > 0.7  # Good score for having citations

    def test_legal_precision_without_citations(self, scorer):
        """Test legal precision scoring without citations."""
        response = """
        Property is divided based on various factors including contributions
        and future needs. Both parties should consider their positions.
        """

        score = scorer.score_legal_precision(response)
        assert score <= 0.6  # Lower score without citations

    def test_citation_accuracy(self, scorer):
        """Test citation accuracy scoring."""
        response = """
        Under Section 79 and Section 60CC, the Court considers various factors.
        Section 999 is also relevant.
        """

        score = scorer.score_citation_accuracy(response)
        # 79 and 60CC are valid, 999 is not
        assert 0.5 <= score <= 0.8

    def test_role_binding_no_conflict(self, scorer):
        """Test role binding with no conflicts."""
        entities = [
            {"id": "a1", "roles": ["applicant"]},
            {"id": "a2", "roles": ["respondent"]},
        ]

        score = scorer.score_role_binding(entities)
        assert score == 1.0  # No conflicts

    def test_role_binding_with_conflict(self, scorer):
        """Test role binding with role conflict."""
        entities = [
            {"id": "a1", "roles": ["applicant", "respondent"]},  # Same entity both roles
        ]

        score = scorer.score_role_binding(entities)
        # Should handle gracefully
        assert score <= 1.0

    def test_comprehensive_scoring(self, scorer):
        """Test full retrieval scoring."""
        query = "What are my property rights after separation?"

        retrieved = [
            {"id": "a1", "type": "Actor", "name": "Applicant", "roles": ["applicant"]},
            {"id": "a2", "type": "Actor", "name": "Respondent", "roles": ["respondent"]},
            {"id": "s1", "type": "State", "name": "Separated", "start_date": "2023-01-15"},
        ]

        expected = [
            {"id": "a1"},
            {"id": "a2"},
            {"id": "s1"},
        ]

        response = """
        ## Property Division Under Section 79

        Under **Section 79** of the Family Law Act 1975, the Court follows
        a four-step process. See *Mallet v Mallet* [1984] HCA 21.
        """

        metrics = scorer.score_retrieval(
            query=query,
            retrieved_entities=retrieved,
            expected_entities=expected,
            response_text=response,
        )

        assert metrics.entity_relevance == 1.0  # Perfect match
        assert metrics.structural_accuracy > 0.5
        assert metrics.legal_precision > 0.7
        assert metrics.composite_score > 0.6


# =============================================================================
# DECORATOR TESTS
# =============================================================================

class TestDecorators:
    """Tests for tracing decorators."""

    def test_trace_gsw_operation_sync(self):
        """Test sync function decoration."""
        @trace_gsw_operation(OperationType.GRAPH_TRAVERSAL)
        def sync_function(x: int) -> int:
            return x * 2

        result = sync_function(5)
        assert result == 10

    def test_trace_gsw_operation_async(self):
        """Test async function decoration."""
        @trace_gsw_operation(OperationType.LLM_GENERATION)
        async def async_function(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 3

        result = asyncio.run(async_function(5))
        assert result == 15

    def test_trace_graph_traversal(self):
        """Test graph traversal decorator."""
        @trace_graph_traversal(name="test_traversal")
        def traverse(query: str) -> list:
            return [{"id": "a1"}, {"id": "a2"}]

        result = traverse("test query")
        assert len(result) == 2


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for the observability module."""

    def test_full_tracing_workflow(self, session_tracker):
        """Test complete tracing workflow."""
        # Start session
        session_tracker.start_turn("What are my property rights?")

        # Record activations
        session_tracker.record_entity_activation("a1", "Actor", "Wife", 0.95)
        session_tracker.record_entity_activation("a2", "Actor", "Husband", 0.92)
        session_tracker.record_entity_activation("s1", "State", "Separated", 0.98)

        # Update context
        session_tracker.update_context(
            actors={"a1": {"name": "Wife"}, "a2": {"name": "Husband"}},
            states={"s1": {"name": "Separated"}},
        )

        # End turn with score
        session_tracker.end_turn(
            response="Under Section 79...",
            confidence=0.92,
        )

        # Verify state
        assert session_tracker.current_turn == 1
        assert len(session_tracker.entity_activations) == 3
        assert session_tracker.current_context.total_entities == 3

        # Get summary
        summary = session_tracker.get_session_summary()
        assert summary["total_turns"] == 1
        assert summary["metrics"]["entities_activated"] == 3

    def test_multi_turn_conversation(self, session_tracker):
        """Test multi-turn conversation tracking."""
        # Turn 1
        session_tracker.start_turn("What about property?")
        session_tracker.record_entity_activation("a1", "Actor")
        session_tracker.update_context(actors={"a1": {}})
        session_tracker.end_turn()

        # Turn 2
        session_tracker.start_turn("What about children?")
        session_tracker.record_entity_activation("a2", "Actor")
        session_tracker.update_context(actors={"a1": {}, "a2": {}})
        session_tracker.end_turn()

        # Turn 3
        session_tracker.start_turn("Any precedents?")
        session_tracker.record_entity_activation("c1", "Case")
        session_tracker.update_context(
            actors={"a1": {}, "a2": {}},
            questions={"q1": {}},
        )
        session_tracker.end_turn()

        # Verify
        assert session_tracker.current_turn == 3
        assert len(session_tracker.states) == 3

        # Check growth - the chart data reflects the number of states recorded
        growth = session_tracker.get_context_growth_chart_data()
        assert len(growth) == 3
        # Each state reflects context at end of turn
        assert growth[0]["turn"] == 1
        assert growth[1]["turn"] == 2
        assert growth[2]["turn"] == 3


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
