"""
Legal Research Agent (Active Inference) - Phase 3.4
===================================================

Implements the Active Inference loop for the Legal Research Agent.
Minimizes Variational Free Energy (VFE) for perception.
Minimizes Expected Free Energy (EFE) for action selection.

References:
- Friston et al., "Active Inference: A Process Theory"
- pymdp: Python implementation of Active Inference
"""

import numpy as np
from typing import List, Tuple, Optional

from src.agency.pomdp import HiddenState, Observation, Action
from src.agency.generative_model import build_generative_model
from src.utils.math_utils import normalize, softmax, entropy, kl_divergence

class LegalResearchAgent:
    def __init__(self):
        # Load Generative Model
        self.A, self.B, self.C, self.D = build_generative_model()
        
        # Belief State (Posterior over hidden states)
        # Initialize with Prior D
        self.qs = self.D.copy()
        
        # Current Time
        self.t = 0
        
        # History
        self.action_history = []
        self.obs_history = []

    def infer_states(self, observation_idx: int):
        """
        Perception Step: Updates beliefs (qs) based on new observation (o).
        Minimizes Variational Free Energy (VFE).
        
        Update rule (approximate):
        qs = softmax( ln(A[o, :]) + ln(B[:, :, u] @ qs_prev) )
        """
        # 1. Get Prior from dynamics (Predictive Belief)
        # If t=0, prior is D. Else, propagate qs through B using last action.
        if self.t == 0:
            prior = self.D
        else:
            last_action = self.action_history[-1]
            prior = self.B[:, :, last_action] @ self.qs
            
        # 2. Get Likelihood from observation
        likelihood = self.A[observation_idx, :]
        
        # 3. Posterior Calculation (Bayes Rule)
        # qs ~ likelihood * prior
        posterior_unnorm = likelihood * prior + 1e-16 # Add epsilon
        self.qs = normalize(posterior_unnorm)
        
        self.obs_history.append(observation_idx)
        
    def infer_policies(self) -> int:
        """
        Action Selection Step: Selects action to minimize Expected Free Energy (G).
        G = Pragmatic Value + Epistemic Value
        """
        num_actions = self.B.shape[2]
        G = np.zeros(num_actions)
        
        # For each possible action u
        for u in range(num_actions):
            # 1. Predict Future State (qs_next)
            qs_next_pred = self.B[:, :, u] @ self.qs
            
            # 2. Predict Future Observation (qo_next)
            qo_next_pred = self.A @ qs_next_pred
            
            # 3. Calculate Pragmatic Value (Utility)
            # Distance to preferred observations (C)
            # Term: sum(qo * C) (since C is log-preference)
            pragmatic = np.dot(qo_next_pred, self.C)
            
            # 4. Calculate Epistemic Value (Information Gain)
            # Divergence between posterior (after seeing O) and prior (before O)
            # Expected Information Gain = H(A) - Expected H(A|s)
            # Simplification: Information Gain ~ Entropy of predicted observation (Novelty)
            # A more accurate form is D_KL[Q(o|s)||P(o)] or mutual information.
            # Here we use the Jensen-Shannon divergence form roughly:
            # H = - sum (qs_next * entropy(A[:, s])) + entropy(qo_next)
            
            # Let's use a simpler metric: State Uncertainty Reduction
            # If A is informative, H(A) is low.
            # Epistemic = sum_o P(o|u) * D_KL[Q(s|o,u) || Q(s|u)]
            
            epistemic = 0
            # Iterate over possible observations
            for o in range(len(qo_next_pred)):
                prob_o = qo_next_pred[o]
                if prob_o < 1e-6: continue
                
                # Posterior if we observed o
                post_s = normalize(self.A[o, :] * qs_next_pred)
                
                # KL between posterior and prior
                kl = kl_divergence(post_s, qs_next_pred)
                epistemic += prob_o * kl
                
            # G = - (Pragmatic + Epistemic)
            # We want to minimize G (Free Energy), so we maximize Value
            # Or standard pymdp convention: G is negative Expected Free Energy
            # Let's stick to: Select max (Pragmatic + Epistemic)
            
            G[u] = pragmatic + epistemic

        # Softmax over G to get policy distribution (stochastic selection)
        policy_prob = softmax(G)
        
        # Sample action
        action_idx = np.random.choice(num_actions, p=policy_prob)
        
        self.action_history.append(action_idx)
        self.t += 1
        
        return action_idx

    def step(self, observation: Observation) -> Action:
        """Main loop step."""
        self.infer_states(observation.value - 1)
        action_idx = self.infer_policies()
        return Action(action_idx + 1)

