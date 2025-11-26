"""
TEM Case Structures
===================

Defines the heuristic case structures for the Micro-TEM component.
These structures represent high-level "templates" or "archetypes" of legal cases,
particularly in Family Law, which the TEM agent can recognize to guide its reasoning.

Based on Task T1.7.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum, auto

class CaseArchetype(Enum):
    """
    Top-level heuristic case archetypes.
    """
    # Parenting
    PARENTING_EQUAL_TIME = auto()          # 50/50 shared care
    PARENTING_SUBSTANTIAL_TIME = auto()    # Significant time but not equal
    PARENTING_SUPERVISED_TIME = auto()     # Risk factors requiring supervision
    PARENTING_RELOCATION = auto()          # One parent moving away
    PARENTING_ALIENATION = auto()          # Allegations of parental alienation
    PARENTING_HIGH_CONFLICT = auto()       # Intractable conflict
    
    # Property
    PROPERTY_LONG_MARRIAGE = auto()        # Long duration (>15 years)
    PROPERTY_SHORT_MARRIAGE = auto()       # Short duration (<5 years)
    PROPERTY_HIGH_WEALTH = auto()          # High net worth
    PROPERTY_HIGH_DISPARITY = auto()       # Big difference in earning capacity
    PROPERTY_COMPLEX_STRUCTURE = auto()    # Trusts, businesses, etc.
    
    # Combined / Other
    VIOLENCE_FAMILY_VIOLENCE = auto()      # Presence of FV allegations
    PROCEDURAL_INTERIM = auto()            # Interim hearing
    PROCEDURAL_FINAL = auto()              # Final hearing
    UNKNOWN = auto()

@dataclass
class CaseStructure:
    """
    Represents the structural "skeleton" of a case.
    Extracted by the TEMFactorizer (Micro-TEM).
    """
    archetype: CaseArchetype
    confidence: float
    
    # Key structural features identified
    features: Dict[str, float] = field(default_factory=dict)
    
    # Explanation of why this structure was chosen
    reasoning: str = ""

    def to_dict(self) -> Dict:
        return {
            "archetype": self.archetype.name,
            "confidence": self.confidence,
            "features": self.features,
            "reasoning": self.reasoning
        }

# Descriptions for RAG/Context
ARCHETYPE_DESCRIPTIONS = {
    CaseArchetype.PARENTING_EQUAL_TIME: "Standard parenting case considering equal shared parental responsibility and time.",
    CaseArchetype.PARENTING_SUBSTANTIAL_TIME: "Parenting case where equal time is not appropriate, considering substantial and significant time.",
    CaseArchetype.PARENTING_SUPERVISED_TIME: "High-risk parenting case requiring supervised contact due to violence or abuse.",
    CaseArchetype.PARENTING_RELOCATION: "Dispute regarding one parent seeking to relocate with the children.",
    CaseArchetype.PROPERTY_LONG_MARRIAGE: "Property settlement following a long relationship; contributions often assessed as equal unless other factors apply.",
    CaseArchetype.PROPERTY_SHORT_MARRIAGE: "Property settlement for a short relationship; focus on direct financial contributions.",
    CaseArchetype.PROPERTY_HIGH_DISPARITY: "Property case with significant difference in future earning capacity, often leading to adjustment.",
    CaseArchetype.VIOLENCE_FAMILY_VIOLENCE: "Case involving allegations of family violence, impacting both parenting arrangements and property contributions.",
}

