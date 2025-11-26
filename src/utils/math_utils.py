"""
Math Utilities for Active Inference
===================================

Helper functions for matrix operations.
"""

import numpy as np

def normalize(A: np.ndarray, axis: int = 0) -> np.ndarray:
    """
    Normalizes a probability distribution/matrix.
    Ensures columns (or rows) sum to 1.
    """
    A_norm = A.copy()
    sums = np.sum(A, axis=axis, keepdims=True)
    # Avoid division by zero
    sums[sums == 0] = 1
    A_norm = A_norm / sums
    return A_norm

def softmax(x: np.ndarray) -> np.ndarray:
    """Softmax function."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def kl_divergence(P: np.ndarray, Q: np.ndarray) -> float:
    """KL Divergence D_KL(P || Q)."""
    # Clip to avoid log(0)
    P = np.clip(P, 1e-12, 1.0)
    Q = np.clip(Q, 1e-12, 1.0)
    return np.sum(P * np.log(P / Q))

def entropy(P: np.ndarray) -> float:
    """Shannon Entropy H(P)."""
    P = np.clip(P, 1e-12, 1.0)
    return -np.sum(P * np.log(P))

