"""
Spiking-TEM (S-TEM) Research Module
===================================

R&D Module for Task T1.6.
Investigating Spiking Neural Networks (SNN) for the TEM architecture.

Objective:
Enable 'Phase Precession' for Legal Anticipation.
In biological grid cells, phase precession allows the brain to 'sweep' through
future possibilities within a theta cycle (5-10Hz).

Proposed Architecture:
1.  Replace Tanh activation in MEC with Leaky Integrate-and-Fire (LIF) neurons.
2.  Use Surrogate Gradient learning (e.g., SuperSpike) for backprop.
3.  Implement 'Theta Cycle' clock to synchronize spikes.

Implementation Plan:
- Class SpikingTransitionModule(nn.Module)
- Class SpikingMemoryModule(nn.Module)

References:
- "Phase precession in the human hippocampus" (Qasim et al., 2021)
- "Surrogate Gradient Learning in Spiking Neural Networks" (Neftci et al., 2019)
"""

import torch
import torch.nn as nn


class LIFNeuron(nn.Module):
    """
    Leaky Integrate-and-Fire Neuron with Surrogate Gradient.
    """

    def __init__(self, tau: float = 2.0, threshold: float = 1.0):
        super().__init__()
        self.tau = tau
        self.threshold = threshold
        self.act = SurrogateHeaviside.apply

    def forward(self, input_current: torch.Tensor, membrane_pot: torch.Tensor) -> torch.Tensor:
        # V[t] = V[t-1] * decay + I[t]
        membrane_pot = membrane_pot * (1 - 1 / self.tau) + input_current

        # Spike if V > Threshold
        spikes = self.act(membrane_pot - self.threshold)

        # Reset membrane potential (soft reset)
        membrane_pot = membrane_pot - spikes * self.threshold

        return spikes, membrane_pot


class SurrogateHeaviside(torch.autograd.Function):
    """
    Heaviside step function with surrogate gradient for backprop.
    Forward: 1 if x > 0 else 0
    Backward: Sigmoid derivative approximation
    """

    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return (input > 0).float()

    @staticmethod
    def backward(ctx, grad_output):
        (input,) = ctx.saved_tensors
        # Sigmoid derivative approximation: alpha * sigmoid(x) * (1 - sigmoid(x))
        alpha = 10.0
        sigmoid = torch.sigmoid(alpha * input)
        grad_input = grad_output * (alpha * sigmoid * (1 - sigmoid))
        return grad_input


class SpikingTransitionModule(nn.Module):
    """
    S-TEM MEC Module using LIF Neurons.

    Implements path integration in structural space using spiking neurons.
    Instead of continuous activations (Tanh), this module uses Leaky
    Integrate-and-Fire (LIF) neurons with surrogate gradients for training.

    The spike timing enables 'phase precession' where the relative timing
    of spikes within a theta cycle encodes the position/state in the
    abstract structural space.
    """

    def __init__(self, hidden_dim: int, action_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.action_dim = action_dim
        self.weights = nn.Parameter(torch.randn(action_dim, hidden_dim, hidden_dim) * 0.05)
        self.bias = nn.Parameter(torch.zeros(hidden_dim))
        self.neuron = LIFNeuron()

    def forward(
        self, spikes_prev: torch.Tensor, mem_prev: torch.Tensor, action_idx: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Apply spiking transition dynamics.

        Args:
            spikes_prev: Previous spike state (Batch, Hidden) - binary spike indicators
            mem_prev: Previous membrane potential (Batch, Hidden)
            action_idx: Action indices (Batch,) - which transition matrix to apply

        Returns:
            spikes_next: New spike output (Batch, Hidden)
            mem_next: Updated membrane potential (Batch, Hidden)
        """
        batch_size = spikes_prev.size(0)

        # Select transition matrices for the batch: (Batch, Hidden, Hidden)
        W_a = self.weights[action_idx]

        # Compute input current from previous spikes through transition matrix
        # This is analogous to: g_t = W_a * g_{t-1} in standard TEM
        # (Batch, Hidden, Hidden) x (Batch, Hidden, 1) -> (Batch, Hidden, 1)
        input_current = torch.bmm(W_a, spikes_prev.unsqueeze(2)).squeeze(2)
        input_current = input_current + self.bias

        # Apply LIF neuron dynamics
        spikes_next, mem_next = self.neuron(input_current, mem_prev)

        return spikes_next, mem_next

    def init_state(
        self, batch_size: int, device: torch.device = None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Initialize the spiking state for a new sequence.

        Args:
            batch_size: Number of sequences in batch
            device: Device to create tensors on

        Returns:
            spikes_init: Initial spike state (zeros)
            mem_init: Initial membrane potential (zeros)
        """
        if device is None:
            device = self.weights.device
        spikes_init = torch.zeros(batch_size, self.hidden_dim, device=device)
        mem_init = torch.zeros(batch_size, self.hidden_dim, device=device)
        return spikes_init, mem_init


class SpikingMemoryModule(nn.Module):
    """
    S-TEM Hippocampal Memory using spike-timing dependent plasticity (STDP).

    EXPERIMENTAL: This module extends the standard Hebbian memory with
    spike-timing considerations. The relative timing of pre and post
    synaptic spikes determines the strength and sign of plasticity.
    """

    def __init__(self, hidden_dim: int, tau_plus: float = 20.0, tau_minus: float = 20.0):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.tau_plus = tau_plus  # Time constant for potentiation
        self.tau_minus = tau_minus  # Time constant for depression

    def retrieve(self, spikes_g: torch.Tensor, M: torch.Tensor) -> torch.Tensor:
        """
        Retrieve sensory prediction from memory using spike pattern.

        Args:
            spikes_g: Structural spike pattern (Batch, Hidden_g)
            M: Memory matrix (Batch, Hidden_p, Hidden_g)

        Returns:
            p_hat: Retrieved sensory pattern (Batch, Hidden_p)
        """
        return torch.bmm(M, spikes_g.unsqueeze(2)).squeeze(2)

    def update_stdp(
        self,
        M: torch.Tensor,
        spikes_pre: torch.Tensor,
        spikes_post: torch.Tensor,
        trace_pre: torch.Tensor,
        trace_post: torch.Tensor,
        eta: float = 0.01,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        STDP-based memory update.

        Implements simplified STDP where:
        - Pre-before-post: Long-term potentiation (LTP)
        - Post-before-pre: Long-term depression (LTD)

        Args:
            M: Current memory matrix (Batch, Hidden_post, Hidden_pre)
            spikes_pre: Pre-synaptic spikes (structural, g)
            spikes_post: Post-synaptic spikes (sensory, p)
            trace_pre: Eligibility trace for pre-synaptic activity
            trace_post: Eligibility trace for post-synaptic activity
            eta: Learning rate

        Returns:
            M_new: Updated memory matrix
            trace_pre_new: Updated pre-synaptic trace
            trace_post_new: Updated post-synaptic trace
        """
        # Update eligibility traces (exponential decay + spike contribution)
        trace_pre_new = trace_pre * (1 - 1 / self.tau_plus) + spikes_pre
        trace_post_new = trace_post * (1 - 1 / self.tau_minus) + spikes_post

        # LTP: post spike when pre trace is active
        # (Batch, Hidden_post, 1) x (Batch, 1, Hidden_pre)
        ltp = torch.bmm(spikes_post.unsqueeze(2), trace_pre.unsqueeze(1))

        # LTD: pre spike when post trace is active
        ltd = torch.bmm(trace_post.unsqueeze(2), spikes_pre.unsqueeze(1))

        # Update memory: potentiation - depression
        M_new = M + eta * (ltp - 0.5 * ltd)

        return M_new, trace_pre_new, trace_post_new
