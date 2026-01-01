"""
Tests for the Active Inference Agency Module
=============================================

Tests the POMDP specification, generative model, and agent logic
for the Legal Research Agent.
"""

from unittest.mock import patch

import numpy as np
import pytest

from src.agency.agent import LegalResearchAgent
from src.agency.generative_model import build_generative_model
from src.agency.pomdp import NUM_ACTIONS, NUM_OBS, NUM_STATES, Action, HiddenState, Observation
from src.utils.math_utils import entropy, kl_divergence, normalize, softmax

# =============================================================================
# POMDP Tests
# =============================================================================

class TestPOMDPSpec:
    """Test POMDP specification and enumerations."""

    def test_hidden_states_exist(self):
        """Test that all hidden states are defined."""
        assert HiddenState.KNOWLEDGE_LOW is not None
        assert HiddenState.KNOWLEDGE_MEDIUM is not None
        assert HiddenState.KNOWLEDGE_HIGH is not None
        assert HiddenState.GOAL_UNMET is not None
        assert HiddenState.GOAL_MET is not None

    def test_observations_exist(self):
        """Test that all observations are defined."""
        assert Observation.FINDING_RELEVANT is not None
        assert Observation.FINDING_IRRELEVANT is not None
        assert Observation.FINDING_NOVEL is not None
        assert Observation.GOAL_SIGNAL_OFF is not None
        assert Observation.GOAL_SIGNAL_ON is not None

    def test_actions_exist(self):
        """Test that all actions are defined."""
        assert Action.SEARCH_BROAD is not None
        assert Action.SEARCH_SPECIFIC is not None
        assert Action.READ_DOCUMENT is not None
        assert Action.DRAFT_ANSWER is not None
        assert Action.CITE_AUTHORITY is not None
        assert Action.STOP is not None

    def test_state_count(self):
        """Test that NUM_STATES matches HiddenState count."""
        assert NUM_STATES[0] == len(HiddenState)

    def test_observation_count(self):
        """Test that NUM_OBS matches Observation count."""
        assert NUM_OBS[0] == len(Observation)

    def test_action_count(self):
        """Test that NUM_ACTIONS matches Action count."""
        assert len(Action) == NUM_ACTIONS

    def test_enum_values_are_sequential(self):
        """Test that enum values are sequential (1-indexed from auto())."""
        states = [s.value for s in HiddenState]
        assert states == list(range(1, len(HiddenState) + 1))

        obs = [o.value for o in Observation]
        assert obs == list(range(1, len(Observation) + 1))

        actions = [a.value for a in Action]
        assert actions == list(range(1, len(Action) + 1))


# =============================================================================
# Generative Model Tests
# =============================================================================

class TestGenerativeModel:
    """Test generative model matrix construction."""

    @pytest.fixture
    def model(self):
        """Build generative model matrices."""
        return build_generative_model()

    def test_model_returns_four_matrices(self, model):
        """Test that build_generative_model returns A, B, C, D."""
        A, B, C, D = model
        assert A is not None
        assert B is not None
        assert C is not None
        assert D is not None

    def test_a_matrix_shape(self, model):
        """Test A matrix (likelihood) has correct shape."""
        A, B, C, D = model
        n_obs = len(Observation)
        n_states = len(HiddenState)
        assert A.shape == (n_obs, n_states)

    def test_b_matrix_shape(self, model):
        """Test B matrix (transition) has correct shape."""
        A, B, C, D = model
        n_states = len(HiddenState)
        n_actions = len(Action)
        assert B.shape == (n_states, n_states, n_actions)

    def test_c_matrix_shape(self, model):
        """Test C matrix (preferences) has correct shape."""
        A, B, C, D = model
        n_obs = len(Observation)
        assert C.shape == (n_obs,)

    def test_d_matrix_shape(self, model):
        """Test D matrix (prior) has correct shape."""
        A, B, C, D = model
        n_states = len(HiddenState)
        assert D.shape == (n_states,)

    def test_a_matrix_is_normalized(self, model):
        """Test that A matrix columns sum to 1 (probability distribution)."""
        A, B, C, D = model
        column_sums = np.sum(A, axis=0)
        np.testing.assert_array_almost_equal(column_sums, np.ones(A.shape[1]))

    def test_d_prior_starts_with_low_knowledge(self, model):
        """Test that prior D starts in KNOWLEDGE_LOW state."""
        A, B, C, D = model
        low_idx = HiddenState.KNOWLEDGE_LOW.value - 1
        assert D[low_idx] == 1.0

    def test_c_prefers_goal_signal(self, model):
        """Test that C matrix prefers GOAL_SIGNAL_ON observation."""
        A, B, C, D = model
        goal_idx = Observation.GOAL_SIGNAL_ON.value - 1
        irrelevant_idx = Observation.FINDING_IRRELEVANT.value - 1
        assert C[goal_idx] > C[irrelevant_idx]

    def test_b_goal_met_is_absorbing(self, model):
        """Test that GOAL_MET state is absorbing (stays in GOAL_MET)."""
        A, B, C, D = model
        goal_met_idx = HiddenState.GOAL_MET.value - 1
        for action in range(B.shape[2]):
            # Probability of staying in GOAL_MET should be 1
            assert B[goal_met_idx, goal_met_idx, action] == 1.0

    def test_specific_search_more_effective_than_broad(self, model):
        """Test that SEARCH_SPECIFIC is more effective than SEARCH_BROAD."""
        A, B, C, D = model
        low_idx = HiddenState.KNOWLEDGE_LOW.value - 1
        med_idx = HiddenState.KNOWLEDGE_MEDIUM.value - 1

        broad_idx = Action.SEARCH_BROAD.value - 1
        specific_idx = Action.SEARCH_SPECIFIC.value - 1

        # Probability of LOW -> MEDIUM transition
        prob_broad = B[med_idx, low_idx, broad_idx]
        prob_specific = B[med_idx, low_idx, specific_idx]

        assert prob_specific > prob_broad, "Specific search should be more effective"


# =============================================================================
# Agent Tests
# =============================================================================

class TestLegalResearchAgent:
    """Test the Legal Research Agent."""

    @pytest.fixture
    def agent(self):
        """Create a fresh agent."""
        return LegalResearchAgent()

    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.A is not None
        assert agent.B is not None
        assert agent.C is not None
        assert agent.D is not None
        assert agent.t == 0
        assert len(agent.action_history) == 0
        assert len(agent.obs_history) == 0

    def test_initial_belief_matches_prior(self, agent):
        """Test that initial belief state matches prior D."""
        np.testing.assert_array_equal(agent.qs, agent.D)

    def test_infer_states_updates_belief(self, agent):
        """Test that infer_states updates the belief state."""
        initial_qs = agent.qs.copy()
        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)

        # Belief should have changed
        assert not np.array_equal(agent.qs, initial_qs)

    def test_infer_states_updates_history(self, agent):
        """Test that infer_states updates observation history."""
        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)
        assert len(agent.obs_history) == 1
        assert agent.obs_history[0] == obs_idx

    def test_infer_policies_returns_valid_action(self, agent):
        """Test that infer_policies returns a valid action index."""
        # First observe something
        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)

        action_idx = agent.infer_policies()
        assert 0 <= action_idx < len(Action)

    def test_infer_policies_updates_time(self, agent):
        """Test that infer_policies increments time."""
        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)

        initial_t = agent.t
        agent.infer_policies()
        assert agent.t == initial_t + 1

    def test_infer_policies_updates_action_history(self, agent):
        """Test that infer_policies updates action history."""
        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)
        agent.infer_policies()

        assert len(agent.action_history) == 1

    def test_step_returns_action_enum(self, agent):
        """Test that step method returns an Action enum."""
        observation = Observation.FINDING_RELEVANT
        action = agent.step(observation)

        assert isinstance(action, Action)

    def test_multiple_steps(self, agent):
        """Test agent can perform multiple steps."""
        observations = [
            Observation.FINDING_IRRELEVANT,
            Observation.FINDING_RELEVANT,
            Observation.FINDING_NOVEL,
        ]

        for obs in observations:
            action = agent.step(obs)
            assert isinstance(action, Action)

        assert agent.t == 3
        assert len(agent.action_history) == 3
        assert len(agent.obs_history) == 3

    def test_belief_convergence_with_consistent_observations(self, agent):
        """Test that beliefs converge with consistent observations."""
        # Repeatedly observe relevant findings
        for _ in range(10):
            agent.step(Observation.FINDING_RELEVANT)

        # Agent should have high belief in KNOWLEDGE states
        # (not necessarily converged, but should have shifted)
        low_idx = HiddenState.KNOWLEDGE_LOW.value - 1
        assert agent.qs[low_idx] < 0.5, "Belief should shift away from LOW knowledge"

    @patch('numpy.random.choice')
    def test_action_selection_is_stochastic(self, mock_choice, agent):
        """Test that action selection uses stochastic sampling."""
        mock_choice.return_value = 0

        obs_idx = Observation.FINDING_RELEVANT.value - 1
        agent.infer_states(obs_idx)
        agent.infer_policies()

        mock_choice.assert_called_once()


# =============================================================================
# Math Utilities Tests
# =============================================================================

class TestMathUtils:
    """Test mathematical utility functions."""

    def test_normalize_vector(self):
        """Test normalize function on a vector."""
        vec = np.array([1.0, 2.0, 3.0, 4.0])
        result = normalize(vec, axis=0)
        assert np.isclose(np.sum(result), 1.0)

    def test_normalize_matrix_columns(self):
        """Test normalize function on matrix columns."""
        mat = np.array([
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0]
        ])
        result = normalize(mat, axis=0)
        column_sums = np.sum(result, axis=0)
        np.testing.assert_array_almost_equal(column_sums, np.ones(2))

    def test_normalize_handles_zero_column(self):
        """Test normalize handles zero columns without division by zero."""
        mat = np.array([
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0]
        ])
        # Should not raise an error
        result = normalize(mat, axis=0)
        assert not np.any(np.isnan(result))

    def test_softmax_output_sums_to_one(self):
        """Test that softmax output sums to 1."""
        x = np.array([1.0, 2.0, 3.0])
        result = softmax(x)
        assert np.isclose(np.sum(result), 1.0)

    def test_softmax_preserves_ordering(self):
        """Test that softmax preserves the ordering of inputs."""
        x = np.array([1.0, 2.0, 3.0])
        result = softmax(x)
        assert result[2] > result[1] > result[0]

    def test_softmax_handles_large_values(self):
        """Test softmax numerical stability with large values."""
        x = np.array([1000.0, 1001.0, 1002.0])
        result = softmax(x)
        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))

    def test_kl_divergence_same_distribution(self):
        """Test KL divergence of a distribution with itself is 0."""
        P = np.array([0.25, 0.25, 0.25, 0.25])
        Q = P.copy()
        result = kl_divergence(P, Q)
        assert np.isclose(result, 0.0)

    def test_kl_divergence_different_distributions(self):
        """Test KL divergence of different distributions is positive."""
        P = np.array([0.9, 0.1])
        Q = np.array([0.1, 0.9])
        result = kl_divergence(P, Q)
        assert result > 0

    def test_kl_divergence_asymmetric(self):
        """Test that KL divergence is asymmetric."""
        P = np.array([0.9, 0.1])
        Q = np.array([0.5, 0.5])
        kl_pq = kl_divergence(P, Q)
        kl_qp = kl_divergence(Q, P)
        assert kl_pq != kl_qp

    def test_entropy_uniform_distribution(self):
        """Test entropy of uniform distribution."""
        P = np.array([0.25, 0.25, 0.25, 0.25])
        result = entropy(P)
        # Maximum entropy for 4 outcomes is log(4)
        assert np.isclose(result, np.log(4))

    def test_entropy_deterministic_distribution(self):
        """Test entropy of deterministic distribution is 0."""
        P = np.array([1.0, 0.0, 0.0, 0.0])
        result = entropy(P)
        assert np.isclose(result, 0.0, atol=1e-10)

    def test_entropy_non_negative(self):
        """Test that entropy is always non-negative."""
        P = np.array([0.7, 0.2, 0.1])
        result = entropy(P)
        assert result >= 0


# =============================================================================
# Integration Tests
# =============================================================================

class TestAgentIntegration:
    """Integration tests for the full agent workflow."""

    def test_agent_reaches_goal_with_good_observations(self):
        """Test that agent can reach goal state with appropriate observations."""
        agent = LegalResearchAgent()

        # Simulate a successful research session
        observations = [
            Observation.FINDING_RELEVANT,
            Observation.FINDING_NOVEL,
            Observation.FINDING_RELEVANT,
            Observation.GOAL_SIGNAL_ON,
        ]

        for obs in observations:
            agent.step(obs)

        # After seeing GOAL_SIGNAL_ON, belief should shift toward GOAL_MET
        goal_met_idx = HiddenState.GOAL_MET.value - 1
        assert agent.qs[goal_met_idx] > 0, "Should have some belief in GOAL_MET"

    def test_agent_action_variety(self):
        """Test that agent selects different actions over time."""
        agent = LegalResearchAgent()

        actions_taken = set()
        for _ in range(50):  # Run many steps
            obs = Observation.FINDING_RELEVANT
            action = agent.step(obs)
            actions_taken.add(action)

        # Should have selected more than one type of action
        assert len(actions_taken) > 1, "Agent should explore different actions"

    def test_agent_belief_state_is_valid_probability(self):
        """Test that agent belief state is always a valid probability distribution."""
        agent = LegalResearchAgent()

        for _ in range(20):
            obs = np.random.choice(list(Observation))
            agent.step(obs)

            # Check belief is a valid probability distribution
            assert np.all(agent.qs >= 0), "Belief must be non-negative"
            assert np.isclose(np.sum(agent.qs), 1.0), "Belief must sum to 1"
