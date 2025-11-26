"""
Generative Model Matrices (Phase 3.2)
=====================================

Defines the A, B, C, D matrices for the Active Inference agent.
Based on `pymdp` conventions.

Matrices:
- A (Likelihood): P(O|S) - Mapping states to observations.
- B (Transition): P(S_{t+1}|S_t, U) - Dynamics of state change.
- C (Preferences): P(O) - Prior preferences (Goal states).
- D (Priors): P(S_0) - Initial state belief.
"""

import numpy as np
from src.agency.pomdp import HiddenState, Observation, Action, NUM_STATES, NUM_OBS, NUM_ACTIONS
from src.utils.math_utils import normalize, softmax

def build_generative_model():
    """
    Constructs the generative model matrices.
    Returns: A, B, C, D
    """
    n_states = len(HiddenState)
    n_obs = len(Observation)
    n_actions = len(Action)

    # =========================================================================
    # A Matrix: Likelihood P(O|S)
    # Shape: (n_obs, n_states)
    # =========================================================================
    A = np.zeros((n_obs, n_states))
    
    # State: KNOWLEDGE_LOW
    # Likely to see Irrelevant results or nothing
    A[Observation.FINDING_IRRELEVANT.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1] = 0.8
    A[Observation.FINDING_RELEVANT.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1] = 0.2
    
    # State: KNOWLEDGE_MEDIUM
    # Mixed results
    A[Observation.FINDING_RELEVANT.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1] = 0.6
    A[Observation.FINDING_NOVEL.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1] = 0.3
    A[Observation.FINDING_IRRELEVANT.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1] = 0.1
    
    # State: KNOWLEDGE_HIGH
    # Mostly Relevant/Novel
    A[Observation.FINDING_RELEVANT.value - 1, HiddenState.KNOWLEDGE_HIGH.value - 1] = 0.5
    A[Observation.FINDING_NOVEL.value - 1, HiddenState.KNOWLEDGE_HIGH.value - 1] = 0.4
    A[Observation.GOAL_SIGNAL_ON.value - 1, HiddenState.KNOWLEDGE_HIGH.value - 1] = 0.1 # Small chance of spontaneous success
    
    # State: GOAL_MET
    # Should see Goal Signal
    A[Observation.GOAL_SIGNAL_ON.value - 1, HiddenState.GOAL_MET.value - 1] = 1.0
    
    # Handle GOAL_UNMET (Overlaps with knowledge states in this simplified view)
    # In a full factorized model, these would be separate factors.
    # For this simple model, let's normalize columns.
    A = normalize(A)

    # =========================================================================
    # B Matrix: Transition P(S'|S, U)
    # Shape: (n_states, n_states, n_actions)
    # =========================================================================
    B = np.zeros((n_states, n_states, n_actions))
    
    # Default: Identity (States persist unless acted upon)
    for u in range(n_actions):
        np.fill_diagonal(B[:, :, u], 1.0)
        
    # Action: SEARCH_BROAD (Increases Low -> Medium)
    # OPTIMIZED for OALC: Broad search is noisy (1.4B tokens), low probability of rapid knowledge gain
    u_sb = Action.SEARCH_BROAD.value - 1
    B[:, :, u_sb] = 0 # Reset
    B[HiddenState.KNOWLEDGE_MEDIUM.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1, u_sb] = 0.1 # Hard (10%)
    B[HiddenState.KNOWLEDGE_LOW.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1, u_sb] = 0.9 # Likely stay low
    # Med -> High
    B[HiddenState.KNOWLEDGE_HIGH.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1, u_sb] = 0.2
    B[HiddenState.KNOWLEDGE_MEDIUM.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1, u_sb] = 0.8
    
    # Action: SEARCH_SPECIFIC (Increases Med -> High)
    # OPTIMIZED for OALC: Specific search (citations/keywords) is effective
    u_ss = Action.SEARCH_SPECIFIC.value - 1
    B[:, :, u_ss] = 0
    B[HiddenState.KNOWLEDGE_MEDIUM.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1, u_ss] = 0.6 # Good chance (60%)
    B[HiddenState.KNOWLEDGE_LOW.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1, u_ss] = 0.4
    # Med -> High
    B[HiddenState.KNOWLEDGE_HIGH.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1, u_ss] = 0.8 # Very effective when narrowed
    B[HiddenState.KNOWLEDGE_MEDIUM.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1, u_ss] = 0.2
    
    # Action: DRAFT_ANSWER (Attempts to go to GOAL_MET)
    u_da = Action.DRAFT_ANSWER.value - 1
    B[:, :, u_da] = 0
    # Only works if Knowledge is High
    B[HiddenState.GOAL_MET.value - 1, HiddenState.KNOWLEDGE_HIGH.value - 1, u_da] = 0.9
    B[HiddenState.KNOWLEDGE_HIGH.value - 1, HiddenState.KNOWLEDGE_HIGH.value - 1, u_da] = 0.1
    # Fails if Knowledge Low/Med
    B[HiddenState.KNOWLEDGE_LOW.value - 1, HiddenState.KNOWLEDGE_LOW.value - 1, u_da] = 1.0
    B[HiddenState.KNOWLEDGE_MEDIUM.value - 1, HiddenState.KNOWLEDGE_MEDIUM.value - 1, u_da] = 1.0
    
    # Ensure persistence for Goal Met
    for u in range(n_actions):
        B[HiddenState.GOAL_MET.value - 1, HiddenState.GOAL_MET.value - 1, u] = 1.0

    # =========================================================================
    # C Matrix: Preferences P(O)
    # Shape: (n_obs,)
    # =========================================================================
    C = np.zeros(n_obs)
    # We strongly prefer the GOAL_SIGNAL_ON observation
    # C values are log-probabilities (or relative utilities)
    C[Observation.GOAL_SIGNAL_ON.value - 1] = 4.0  # High utility
    C[Observation.FINDING_RELEVANT.value - 1] = 1.0 # Epistemic value implicitly handled, but slight pref for relevance
    C[Observation.FINDING_IRRELEVANT.value - 1] = -2.0 # Dislike irrelevant
    
    # =========================================================================
    # D Matrix: Priors P(S_0)
    # Shape: (n_states,)
    # =========================================================================
    D = np.zeros(n_states)
    D[HiddenState.KNOWLEDGE_LOW.value - 1] = 1.0 # Start knowing nothing
    
    return A, B, C, D
