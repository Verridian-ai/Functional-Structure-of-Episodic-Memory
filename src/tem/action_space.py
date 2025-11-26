"""
TEM Navigational Action Space
=============================

Defines the discrete set of relational actions (A) available to the TEM agent
for navigating the Hier-SPCNet.

Each action represents a directed edge type between two legal documents (nodes).
The agent predicts the next action (a_t) along with the next sensory state (x_t).
"""

from enum import Enum, auto
from typing import List, Dict

class LegalAction(Enum):
    """
    Discrete actions for traversing the legal citation graph.
    """
    # Neutral / General
    CITE = auto()          # General citation (default)
    CONSIDER = auto()      # Discussed but not pivotal
    MENTION = auto()       # Brief mention

    # Positive Treatment
    FOLLOW = auto()        # Applies precedent directly
    AFFIRM = auto()        # Upheld on appeal
    APPROVE = auto()       # Higher court approves lower court reasoning
    APPLY = auto()         # Applies principle to new facts

    # Negative Treatment
    DISTINGUISH = auto()   # Cites but differentiates facts (blocks application)
    OVERRULE = auto()      # Invalidates previous precedent
    REVERSE = auto()       # Overturns lower court decision on appeal
    DISAPPROVE = auto()    # Disagrees with reasoning
    NOT_FOLLOW = auto()    # Explicitly declines to follow

    # Procedural
    APPEAL_FROM = auto()   # Edge from Appellate -> Lower Court judgment
    RELATED_TO = auto()    # Same proceedings, different judgment

    @classmethod
    def list_all(cls) -> List[str]:
        return [a.name for a in cls]

    @classmethod
    def positive_actions(cls) -> List['LegalAction']:
        return [cls.FOLLOW, cls.AFFIRM, cls.APPROVE, cls.APPLY]

    @classmethod
    def negative_actions(cls) -> List['LegalAction']:
        return [cls.DISTINGUISH, cls.OVERRULE, cls.REVERSE, cls.DISAPPROVE, cls.NOT_FOLLOW]

# Mapping of integer IDs to Actions for the Neural Network (Output Layer)
ACTION_TO_ID: Dict[LegalAction, int] = {action: i for i, action in enumerate(LegalAction)}
ID_TO_ACTION: Dict[int, LegalAction] = {i: action for action, i in ACTION_TO_ID.items()}

def get_action_dim() -> int:
    """Returns the size of the action space."""
    return len(LegalAction)

