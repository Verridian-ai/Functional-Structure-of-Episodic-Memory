"""
Active Inference POMDP Specification (Phase 3.1)
================================================

Defines the Partially Observable Markov Decision Process (POMDP)
for the Active Inference Legal Research Agent.

States (S):
- Case Knowledge: {Incomplete, Partial, Comprehensive}
- Legal Issue: {Unresolved, Ambiguous, Settled}
- Evidence Status: {Missing, Weak, Strong}

Observations (O):
- Search Results: {Relevant, Irrelevant, Novel}
- Document Content: {Supports, Contradicts, Neutral}
- User Feedback: {Positive, Negative, None}

Policies (Pi):
- Actions defined in Phase 1 (Navigational Action Space)
"""

from enum import Enum, auto

class HiddenState(Enum):
    """Hidden States (S) of the generative model."""
    # Knowledge States
    KNOWLEDGE_LOW = auto()
    KNOWLEDGE_MEDIUM = auto()
    KNOWLEDGE_HIGH = auto()
    
    # Goal States
    GOAL_UNMET = auto()
    GOAL_MET = auto()

class Observation(Enum):
    """Observations (O) received from the environment."""
    # Search Outcomes
    FINDING_RELEVANT = auto()
    FINDING_IRRELEVANT = auto()
    FINDING_NOVEL = auto()
    
    # Goal Signals
    GOAL_SIGNAL_OFF = auto()
    GOAL_SIGNAL_ON = auto() # "Success"

class Action(Enum):
    """Active Inference Policies / Actions."""
    # Epistemic Actions (Exploration)
    SEARCH_BROAD = auto()
    SEARCH_SPECIFIC = auto()
    READ_DOCUMENT = auto()
    
    # Pragmatic Actions (Exploitation)
    DRAFT_ANSWER = auto()
    CITE_AUTHORITY = auto()
    STOP = auto()

# Dimensions
NUM_STATES = [len(HiddenState)] # Simple factorized state space for now
NUM_OBS = [len(Observation)]
NUM_ACTIONS = len(Action)

