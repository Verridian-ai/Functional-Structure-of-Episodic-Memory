"""
Tolman-Eichenbaum Machine (TEM) Model
=====================================

PyTorch implementation of the TEM architecture for legal graph navigation.
Based on Whittington et al. (2020).

Components:
1.  MEC (Structural Path Integration):
    - Updates grid cells (g) based on action (a).
    - g_t = f(g_{t-1}, a_t)
2.  LEC (Sensory Processing):
    - Encodes observation (x) into sensory embedding (p).
3.  Hippocampus (Associative Memory):
    - Attractor network binding (g) and (p).
    - Predicts x_{t+1} based on g_{t+1} and retrieved memory.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict

from src.tem.action_space import get_action_dim

class TransitionModule(nn.Module):
    """
    Models the transition in the abstract structural space (Grid Cells).
    Learns a transition matrix for each action.
    """
    def __init__(self, hidden_dim: int, action_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.action_dim = action_dim
        
        # Transition weights: [Action_Dim, Hidden, Hidden]
        # W_g[a] transforms g_{t-1} to g_t
        self.weights = nn.Parameter(torch.randn(action_dim, hidden_dim, hidden_dim) * 0.01)
        self.bias = nn.Parameter(torch.zeros(hidden_dim))
        
        # Recurrent nonlinearity
        self.activation = nn.Tanh()

    def forward(self, g_prev: torch.Tensor, action_indices: torch.Tensor) -> torch.Tensor:
        """
        g_prev: (Batch, Hidden)
        action_indices: (Batch,) - indices of actions taken
        """
        batch_size = g_prev.size(0)
        
        # Select transition matrices for the batch: (Batch, Hidden, Hidden)
        W_a = self.weights[action_indices]
        
        # Apply transition: g_t = W_a * g_{t-1}
        # (Batch, Hidden, Hidden) x (Batch, Hidden, 1) -> (Batch, Hidden, 1)
        g_next = torch.bmm(W_a, g_prev.unsqueeze(2)).squeeze(2)
        
        return self.activation(g_next + self.bias)

class SensoryModule(nn.Module):
    """
    Encodes sensory observations (Document Embeddings) into LEC state.
    Decodes LEC state back to observations (Prediction).
    """
    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, input_dim)
        )

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return self.encoder(x)

    def decode(self, p: torch.Tensor) -> torch.Tensor:
        return self.decoder(p)

class MemoryModule(nn.Module):
    """
    Associative Memory (Hippocampus).
    Binds structural (g) and sensory (p) representations.
    Uses Hebbian learning to update the memory matrix M.
    """
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # In a real TEM, M is dynamic per episode.
        # Here we define the learning rule logic, state is kept in the forward loop.

    def retrieve(self, g: torch.Tensor, M: torch.Tensor) -> torch.Tensor:
        """
        Retrieve sensory prediction p_hat from memory M given structure g.
        p_hat = M * g
        """
        # M: (Batch, Hidden_p, Hidden_g)
        # g: (Batch, Hidden_g)
        # result: (Batch, Hidden_p)
        return torch.bmm(M, g.unsqueeze(2)).squeeze(2)

    def update(self, M: torch.Tensor, g: torch.Tensor, p: torch.Tensor, eta: float = 0.1) -> torch.Tensor:
        """
        Hebbian Update: M_new = M + eta * (p * g^T)
        """
        # Outer product: (Batch, Hidden_p, 1) x (Batch, 1, Hidden_g) -> (Batch, Hidden_p, Hidden_g)
        update_term = torch.bmm(p.unsqueeze(2), g.unsqueeze(1))
        return M + eta * update_term

class TolmanEichenbaumMachine(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, action_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        self.mec = TransitionModule(hidden_dim, action_dim)
        self.lec = SensoryModule(input_dim, hidden_dim)
        self.memory = MemoryModule(hidden_dim)
        
        # Initial state parameters
        self.g_init = nn.Parameter(torch.randn(hidden_dim))

    def forward(self, observations: torch.Tensor, actions: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Runs TEM on a sequence of observations and actions.
        
        Args:
            observations: (Batch, Seq_Len, Input_Dim)
            actions: (Batch, Seq_Len) - Note: Action a_t leads to Obs x_{t+1}
                     Normally seq len of actions is 1 less than obs.
                     Here we assume aligned: Action[t] -> Obs[t+1]
        
        Returns:
            Dict containing:
            - 'predictions': Predicted observations (reconstructed)
            - 'accuracies': (if supervised)
        """
        batch_size, seq_len, _ = observations.size()
        
        # Initialize structural state g_0
        g = self.g_init.expand(batch_size, -1)
        
        # Initialize Memory Matrix M_0 (Batch, Hidden, Hidden)
        # M maps g (structure) -> p (sense)
        M = torch.zeros(batch_size, self.hidden_dim, self.hidden_dim, device=observations.device)
        
        predictions = []
        
        # Encoding first observation
        p = self.lec.encode(observations[:, 0])
        
        # Hebbian update for t=0
        M = self.memory.update(M, g, p)
        predictions.append(self.lec.decode(p)) # Trivial reconstruction for t=0
        
        for t in range(seq_len - 1):
            # 1. Path Integration: g_{t+1} = MEC(g_t, a_t)
            action = actions[:, t]
            g = self.mec(g, action)
            
            # 2. Pattern Completion / Retrieval: p_hat_{t+1} = Memory(g_{t+1})
            p_hat = self.memory.retrieve(g, M)
            
            # 3. Decode prediction: x_hat_{t+1}
            x_hat = self.lec.decode(p_hat)
            predictions.append(x_hat)
            
            # 4. Encode actual observation: p_{t+1}
            p_actual = self.lec.encode(observations[:, t+1])
            
            # 5. Update Memory with new reality: M_{t+1} = Hebbian(M_t, g_{t+1}, p_{t+1})
            M = self.memory.update(M, g, p_actual)
            
        return {
            'predictions': torch.stack(predictions, dim=1)
        }

