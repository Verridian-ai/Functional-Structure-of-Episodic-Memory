"""
Heuristic TEM Factorizer
========================

Implements the heuristic fallback for Micro-TEM (Case Structure Analysis).
Extracts a `CaseStructure` from a GSW `GlobalWorkspace` or `ChunkExtraction`
using rule-based logic (Phase 1B, Task T1.8).

This component provides immediate value while the neural Macro-TEM model trains.
"""

import re
from typing import Union, Dict, List, Optional
from collections import Counter

from src.logic.gsw_schema import GlobalWorkspace, ChunkExtraction, Actor, State, ActorType
from src.tem.structures import CaseArchetype, CaseStructure, ARCHETYPE_DESCRIPTIONS

class HeuristicTEMFactorizer:
    """
    Analyzes extracted legal facts to determine the case archetype.
    """
    
    def factorize(self, data: Union[GlobalWorkspace, ChunkExtraction]) -> CaseStructure:
        """
        Main entry point. Determines structure from GSW data.
        """
        # Consolidate data into lists of entities for analysis
        actors = data.actors if isinstance(data, ChunkExtraction) else list(data.actors.values())
        states = []
        if isinstance(data, GlobalWorkspace):
            states = list(data.states.values())
        else:
            # ChunkExtraction structures actors differently, gather states from actors
            for actor in actors:
                states.extend(actor.states)
                
        # Feature Extraction
        features = self._extract_features(actors, states)
        
        # Archetype Classification
        archetype, confidence, reasoning = self._classify_archetype(features)
        
        return CaseStructure(
            archetype=archetype,
            confidence=confidence,
            features=features,
            reasoning=reasoning
        )

    def _extract_features(self, actors: List[Actor], states: List[State]) -> Dict[str, float]:
        """
        Extracts numerical/boolean features from entities.
        """
        features = {
            "has_children": 0.0,
            "has_property": 0.0,
            "has_violence": 0.0,
            "relationship_duration_years": 0.0,
            "financial_disparity": 0.0,
            "relocation_intent": 0.0,
            "high_conflict": 0.0
        }
        
        # 1. Actor Analysis
        for actor in actors:
            # Check for children
            if actor.actor_type == ActorType.PERSON:
                name_lower = actor.name.lower()
                roles_lower = [r.lower() for r in actor.roles]
                if "child" in roles_lower or "minor" in roles_lower:
                    features["has_children"] = 1.0
                if "child" in name_lower and "representative" not in name_lower: # avoid ICL
                    features["has_children"] = 1.0
            
            # Check for assets
            if actor.actor_type == ActorType.ASSET:
                features["has_property"] = 1.0
                
        # 2. State Analysis
        for state in states:
            name_lower = state.name.lower()
            value_lower = state.value.lower()
            
            # Violence
            if "violence" in name_lower or "abuse" in name_lower or "safety" in name_lower:
                features["has_violence"] = 1.0
            if "violence" in value_lower or "abuse" in value_lower:
                features["has_violence"] = 1.0
                
            # Relationship Duration (Rough heuristic)
            if "relationship" in name_lower or "marriage" in name_lower:
                if state.start_date and state.end_date:
                    try:
                        # extremely simplified year parsing
                        start_year = int(re.search(r'\d{4}', state.start_date).group())
                        end_year = int(re.search(r'\d{4}', state.end_date).group())
                        duration = end_year - start_year
                        features["relationship_duration_years"] = float(duration)
                    except (AttributeError, ValueError):
                        pass
                        
            # Financial Disparity
            if "income" in name_lower or "earning" in name_lower:
                # If we see explicit states about disparity
                if "high" in value_lower and "disparity" in value_lower:
                    features["financial_disparity"] = 1.0
                    
            # Relocation
            if "residence" in name_lower or "location" in name_lower:
                if "relocat" in value_lower or "move" in value_lower:
                    features["relocation_intent"] = 1.0

        return features

    def _classify_archetype(self, features: Dict[str, float]) -> tuple[CaseArchetype, float, str]:
        """
        Rules engine to determine archetype based on features.
        """
        # 1. Violence Override (Safety is paramount)
        if features["has_violence"] > 0:
            return (
                CaseArchetype.VIOLENCE_FAMILY_VIOLENCE, 
                0.9, 
                "Detected explicit references to family violence or safety concerns."
            )
            
        # 2. Parenting Cases
        if features["has_children"] > 0:
            if features["relocation_intent"] > 0:
                return (
                    CaseArchetype.PARENTING_RELOCATION,
                    0.8,
                    "Involves children and an intent to relocate."
                )
            
            # Default to substantial time if no other indicators
            return (
                CaseArchetype.PARENTING_SUBSTANTIAL_TIME,
                0.6,
                "Parenting matter detected. Defaulting to Substantial Time assessment."
            )
            
        # 3. Property Cases
        if features["has_property"] > 0 or features["financial_disparity"] > 0:
            if features["relationship_duration_years"] > 15:
                return (
                    CaseArchetype.PROPERTY_LONG_MARRIAGE,
                    0.85,
                    f"Long relationship detected ({features['relationship_duration_years']} years)."
                )
            if features["relationship_duration_years"] > 0 and features["relationship_duration_years"] < 5:
                return (
                    CaseArchetype.PROPERTY_SHORT_MARRIAGE,
                    0.8,
                    f"Short relationship detected ({features['relationship_duration_years']} years)."
                )
            if features["financial_disparity"] > 0:
                return (
                    CaseArchetype.PROPERTY_HIGH_DISPARITY,
                    0.7,
                    "Significant financial disparity detected between parties."
                )
                
            return (
                CaseArchetype.PROPERTY_HIGH_WEALTH,
                0.5,
                "Property matter detected."
            )
            
        return (CaseArchetype.UNKNOWN, 0.0, "Insufficient features to classify.")

