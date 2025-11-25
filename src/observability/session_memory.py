"""
Episodic Session Memory Tracker for GSW
========================================

Tracks how the episodic memory (GlobalWorkspace) evolves during a user session.
Logs context window growth, entity activations, and memory state transitions.

This module integrates with LangFuse to provide visibility into:
- How context grows with follow-up questions
- Which entities are activated across turns
- Memory consolidation events
- Session-level patterns
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING
from enum import Enum
import json
import hashlib

if TYPE_CHECKING:
    from .langfuse_tracer import GSWTracer


class SessionEventType(str, Enum):
    """Types of events in an episodic session."""
    QUERY = "query"
    ENTITY_ACTIVATED = "entity_activated"
    ENTITY_ADDED = "entity_added"
    ENTITY_MERGED = "entity_merged"
    STATE_UPDATED = "state_updated"
    QUESTION_ANSWERED = "question_answered"
    QUESTION_GENERATED = "question_generated"
    CONTEXT_EXPANDED = "context_expanded"
    CONTEXT_PRUNED = "context_pruned"
    MEMORY_CONSOLIDATED = "memory_consolidated"
    SPATIO_TEMPORAL_LINK = "spatio_temporal_link"


@dataclass
class SessionEvent:
    """A single event in the session timeline."""
    event_type: SessionEventType
    timestamp: datetime
    data: Dict[str, Any]
    turn_number: int
    context_size_before: int
    context_size_after: int


@dataclass
class EntityActivation:
    """Tracks activation of an entity across session turns."""
    entity_id: str
    entity_type: str
    entity_name: Optional[str]
    first_activated_turn: int
    activation_count: int = 1
    last_activated_turn: int = 0
    relevance_scores: List[float] = field(default_factory=list)

    def record_activation(self, turn: int, relevance: float = 1.0):
        """Record another activation of this entity."""
        self.activation_count += 1
        self.last_activated_turn = turn
        self.relevance_scores.append(relevance)

    @property
    def avg_relevance(self) -> float:
        return sum(self.relevance_scores) / len(self.relevance_scores) if self.relevance_scores else 0.0

    @property
    def persistence(self) -> int:
        """How many turns this entity has persisted."""
        return self.last_activated_turn - self.first_activated_turn + 1


@dataclass
class ContextWindow:
    """Represents the current episodic memory context window."""
    actors: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    verb_phrases: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    questions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    spatio_temporal_links: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def total_entities(self) -> int:
        return (
            len(self.actors) +
            len(self.states) +
            len(self.verb_phrases) +
            len(self.questions) +
            len(self.spatio_temporal_links)
        )

    @property
    def size_breakdown(self) -> Dict[str, int]:
        return {
            "actors": len(self.actors),
            "states": len(self.states),
            "verb_phrases": len(self.verb_phrases),
            "questions": len(self.questions),
            "spatio_temporal_links": len(self.spatio_temporal_links),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_entities": self.total_entities,
            "breakdown": self.size_breakdown,
            "actors": list(self.actors.keys())[:20],
            "states": list(self.states.keys())[:20],
        }

    def compute_hash(self) -> str:
        """Compute a hash of the context state for change detection."""
        content = json.dumps({
            "actors": sorted(self.actors.keys()),
            "states": sorted(self.states.keys()),
            "verb_phrases": sorted(self.verb_phrases.keys()),
            "questions": sorted(self.questions.keys()),
            "links": sorted(self.spatio_temporal_links.keys()),
        }, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class SessionState:
    """Complete state of a session at a point in time."""
    turn_number: int
    timestamp: datetime
    query: str
    context: ContextWindow
    context_hash: str
    active_entity_ids: Set[str]
    newly_added_entities: Set[str]
    answered_questions: Set[str]
    pending_questions: Set[str]
    confidence_score: Optional[float] = None


class EpisodicSessionTracker:
    """
    Tracks episodic memory evolution during a user session.

    This provides visibility into:
    1. Context window growth over time
    2. Entity activation patterns
    3. Memory consolidation events
    4. Question answering progress

    Usage:
        tracker = EpisodicSessionTracker(session_id="user_123")

        # At each turn
        tracker.start_turn(query="What about the children?")
        tracker.record_entity_activation(entity_id="actor_1", ...)
        tracker.update_context(workspace)
        tracker.end_turn(response="Based on s60CC...")

        # Get analytics
        print(tracker.get_session_summary())
    """

    def __init__(
        self,
        session_id: str,
        tracer: Optional["GSWTracer"] = None,
        max_history: int = 100,
    ):
        """
        Initialize session tracker.

        Args:
            session_id: Unique session identifier
            tracer: Optional GSWTracer for LangFuse integration
            max_history: Maximum number of events to keep in memory
        """
        self.session_id = session_id
        self.tracer = tracer
        self.max_history = max_history

        # Session timeline
        self.events: List[SessionEvent] = []
        self.states: List[SessionState] = []
        self.current_turn: int = 0

        # Entity tracking
        self.entity_activations: Dict[str, EntityActivation] = {}
        self.entity_relationships: Dict[str, Set[str]] = {}  # entity_id -> related entity_ids

        # Current context
        self.current_context = ContextWindow()
        self.previous_context_hash: Optional[str] = None

        # Session metadata
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()

        # Analytics
        self.total_queries = 0
        self.total_entities_activated = 0
        self.questions_answered = 0
        self.questions_generated = 0

    # =========================================================================
    # TURN MANAGEMENT
    # =========================================================================

    def start_turn(self, query: str) -> int:
        """
        Start a new conversation turn.

        Args:
            query: The user's query

        Returns:
            Turn number
        """
        self.current_turn += 1
        self.total_queries += 1
        self.last_activity = datetime.utcnow()

        # Record query event
        self._record_event(
            SessionEventType.QUERY,
            {"query": query, "turn": self.current_turn},
        )

        # Log to LangFuse
        if self.tracer and self.tracer.enabled and self.tracer._current_trace:
            self.tracer._current_trace.event(
                name="session_turn_start",
                metadata={
                    "session_id": self.session_id,
                    "turn_number": self.current_turn,
                    "query_preview": query[:200],
                    "context_size": self.current_context.total_entities,
                },
            )

        return self.current_turn

    def end_turn(
        self,
        response: Optional[str] = None,
        confidence: Optional[float] = None,
    ):
        """
        End the current turn and record state.

        Args:
            response: The system's response
            confidence: Optional confidence score for the response
        """
        # Capture state snapshot
        state = SessionState(
            turn_number=self.current_turn,
            timestamp=datetime.utcnow(),
            query=self.events[-1].data.get("query", "") if self.events else "",
            context=self.current_context,
            context_hash=self.current_context.compute_hash(),
            active_entity_ids=set(self.entity_activations.keys()),
            newly_added_entities=self._get_newly_added_entities(),
            answered_questions=self._get_answered_questions(),
            pending_questions=self._get_pending_questions(),
            confidence_score=confidence,
        )

        self.states.append(state)

        # Detect context changes
        if self.previous_context_hash and state.context_hash != self.previous_context_hash:
            self._record_event(
                SessionEventType.CONTEXT_EXPANDED,
                {
                    "previous_size": len(self.states[-2].active_entity_ids) if len(self.states) > 1 else 0,
                    "new_size": len(state.active_entity_ids),
                    "new_entities": list(state.newly_added_entities)[:10],
                },
            )

        self.previous_context_hash = state.context_hash

        # Log to LangFuse
        if self.tracer and self.tracer.enabled and self.tracer._current_trace:
            self.tracer._current_trace.event(
                name="session_turn_end",
                metadata={
                    "session_id": self.session_id,
                    "turn_number": self.current_turn,
                    "context_size": self.current_context.total_entities,
                    "entities_activated_this_turn": self.total_entities_activated,
                    "confidence": confidence,
                    "response_preview": response[:200] if response else None,
                },
            )

            # Score if confidence provided
            if confidence is not None:
                self.tracer.score_retrieval(
                    name="turn_confidence",
                    score=confidence,
                    comment=f"Turn {self.current_turn} confidence",
                )

    # =========================================================================
    # ENTITY TRACKING
    # =========================================================================

    def record_entity_activation(
        self,
        entity_id: str,
        entity_type: str,
        entity_name: Optional[str] = None,
        relevance: float = 1.0,
        connected_entities: Optional[List[str]] = None,
    ):
        """
        Record that an entity was activated during retrieval.

        Args:
            entity_id: Unique entity identifier
            entity_type: Type (actor, state, verb_phrase, etc.)
            entity_name: Optional human-readable name
            relevance: Relevance score (0.0-1.0)
            connected_entities: IDs of related entities
        """
        if entity_id in self.entity_activations:
            self.entity_activations[entity_id].record_activation(self.current_turn, relevance)
        else:
            self.entity_activations[entity_id] = EntityActivation(
                entity_id=entity_id,
                entity_type=entity_type,
                entity_name=entity_name,
                first_activated_turn=self.current_turn,
                last_activated_turn=self.current_turn,
                relevance_scores=[relevance],
            )

        # Track relationships
        if connected_entities:
            if entity_id not in self.entity_relationships:
                self.entity_relationships[entity_id] = set()
            self.entity_relationships[entity_id].update(connected_entities)

        self.total_entities_activated += 1

        # Record event
        self._record_event(
            SessionEventType.ENTITY_ACTIVATED,
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "entity_name": entity_name,
                "relevance": relevance,
            },
        )

    def record_entity_added(
        self,
        entity_id: str,
        entity_type: str,
        entity_name: Optional[str] = None,
        source: str = "extraction",
    ):
        """Record that a new entity was added to the workspace."""
        self._record_event(
            SessionEventType.ENTITY_ADDED,
            {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "entity_name": entity_name,
                "source": source,
            },
        )

    def record_entity_merged(
        self,
        source_id: str,
        target_id: str,
        confidence: float,
    ):
        """Record that two entities were merged (reconciliation)."""
        self._record_event(
            SessionEventType.ENTITY_MERGED,
            {
                "source_id": source_id,
                "target_id": target_id,
                "merge_confidence": confidence,
            },
        )

    # =========================================================================
    # CONTEXT MANAGEMENT
    # =========================================================================

    def update_context(
        self,
        workspace: Optional[Any] = None,
        actors: Optional[Dict] = None,
        states: Optional[Dict] = None,
        verb_phrases: Optional[Dict] = None,
        questions: Optional[Dict] = None,
        spatio_temporal_links: Optional[Dict] = None,
    ):
        """
        Update the tracked context window.

        Can accept either a GlobalWorkspace object or individual dicts.

        Args:
            workspace: Optional GlobalWorkspace object
            actors: Dict of actor_id -> actor data
            states: Dict of state_id -> state data
            verb_phrases: Dict of verb_id -> verb data
            questions: Dict of question_id -> question data
            spatio_temporal_links: Dict of link_id -> link data
        """
        if workspace is not None:
            # Extract from GlobalWorkspace
            if hasattr(workspace, 'actors'):
                self.current_context.actors = {
                    k: self._entity_to_dict(v) for k, v in workspace.actors.items()
                }
            if hasattr(workspace, 'states'):
                self.current_context.states = {
                    k: self._entity_to_dict(v) for k, v in workspace.states.items()
                }
            if hasattr(workspace, 'verb_phrases'):
                self.current_context.verb_phrases = {
                    k: self._entity_to_dict(v) for k, v in workspace.verb_phrases.items()
                }
            if hasattr(workspace, 'questions'):
                self.current_context.questions = {
                    k: self._entity_to_dict(v) for k, v in workspace.questions.items()
                }
            if hasattr(workspace, 'spatio_temporal_links'):
                self.current_context.spatio_temporal_links = {
                    k: self._entity_to_dict(v) for k, v in workspace.spatio_temporal_links.items()
                }
        else:
            # Update from individual dicts
            if actors is not None:
                self.current_context.actors = actors
            if states is not None:
                self.current_context.states = states
            if verb_phrases is not None:
                self.current_context.verb_phrases = verb_phrases
            if questions is not None:
                self.current_context.questions = questions
            if spatio_temporal_links is not None:
                self.current_context.spatio_temporal_links = spatio_temporal_links

    def record_question_answered(self, question_id: str, answer: str):
        """Record that a predictive question was answered."""
        self.questions_answered += 1
        self._record_event(
            SessionEventType.QUESTION_ANSWERED,
            {"question_id": question_id, "answer_preview": answer[:100]},
        )

    def record_question_generated(self, question_id: str, question_text: str):
        """Record that a new predictive question was generated."""
        self.questions_generated += 1
        self._record_event(
            SessionEventType.QUESTION_GENERATED,
            {"question_id": question_id, "question_text": question_text[:200]},
        )

    def record_spatio_temporal_link(
        self,
        link_id: str,
        linked_entities: List[str],
        link_type: str,
        link_value: str,
    ):
        """Record a spatio-temporal linking event."""
        self._record_event(
            SessionEventType.SPATIO_TEMPORAL_LINK,
            {
                "link_id": link_id,
                "linked_entities": linked_entities,
                "link_type": link_type,
                "link_value": link_value,
            },
        )

    # =========================================================================
    # ANALYTICS & REPORTING
    # =========================================================================

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the session for analytics.

        Returns:
            Dict with session metrics and patterns
        """
        return {
            "session_id": self.session_id,
            "duration_minutes": (datetime.utcnow() - self.created_at).total_seconds() / 60,
            "total_turns": self.current_turn,
            "total_queries": self.total_queries,
            "metrics": {
                "entities_activated": len(self.entity_activations),
                "unique_entity_types": len(set(a.entity_type for a in self.entity_activations.values())),
                "questions_answered": self.questions_answered,
                "questions_generated": self.questions_generated,
                "context_growth": self._compute_context_growth(),
            },
            "context_window": self.current_context.to_dict(),
            "top_entities": self._get_top_entities(10),
            "entity_type_distribution": self._get_entity_type_distribution(),
            "context_evolution": self._get_context_evolution(),
        }

    def get_context_growth_chart_data(self) -> List[Dict[str, Any]]:
        """Get data suitable for plotting context growth over turns."""
        return [
            {
                "turn": state.turn_number,
                "total_entities": state.context.total_entities,
                **state.context.size_breakdown,
                "timestamp": state.timestamp.isoformat(),
            }
            for state in self.states
        ]

    def get_entity_activation_timeline(self) -> Dict[str, List[int]]:
        """Get which turns each entity was active in."""
        timeline = {}
        for entity_id, activation in self.entity_activations.items():
            timeline[entity_id] = list(range(
                activation.first_activated_turn,
                activation.last_activated_turn + 1
            ))
        return timeline

    def export_to_langfuse(self):
        """Export complete session data to LangFuse as a dataset item."""
        if not self.tracer or not self.tracer.enabled:
            return

        # Record session summary as trace metadata
        if self.tracer._current_trace:
            self.tracer._current_trace.update(
                metadata={
                    "session_summary": self.get_session_summary(),
                    "context_evolution": self.get_context_growth_chart_data(),
                },
            )

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _record_event(self, event_type: SessionEventType, data: Dict[str, Any]):
        """Record an event in the session timeline."""
        event = SessionEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            data=data,
            turn_number=self.current_turn,
            context_size_before=self.current_context.total_entities,
            context_size_after=self.current_context.total_entities,  # Updated after context change
        )

        self.events.append(event)

        # Prune old events if needed
        if len(self.events) > self.max_history:
            self.events = self.events[-self.max_history:]

    def _entity_to_dict(self, entity: Any) -> Dict[str, Any]:
        """Convert an entity object to a dict."""
        if hasattr(entity, "to_dict"):
            return entity.to_dict()
        if hasattr(entity, "__dict__"):
            return {k: v for k, v in entity.__dict__.items() if not k.startswith("_")}
        return {"value": str(entity)}

    def _get_newly_added_entities(self) -> Set[str]:
        """Get entities added in the current turn."""
        if len(self.states) < 2:
            return set(self.entity_activations.keys())

        previous_entities = self.states[-1].active_entity_ids if self.states else set()
        current_entities = set(self.entity_activations.keys())
        return current_entities - previous_entities

    def _get_answered_questions(self) -> Set[str]:
        """Get IDs of answered questions."""
        return {
            q_id for q_id, q_data in self.current_context.questions.items()
            if q_data.get("answer") or q_data.get("is_answered")
        }

    def _get_pending_questions(self) -> Set[str]:
        """Get IDs of unanswered questions."""
        answered = self._get_answered_questions()
        return set(self.current_context.questions.keys()) - answered

    def _compute_context_growth(self) -> Dict[str, Any]:
        """Compute context growth metrics."""
        if len(self.states) < 2:
            return {"growth_rate": 0, "total_change": 0}

        first_size = self.states[0].context.total_entities
        last_size = self.states[-1].context.total_entities

        return {
            "initial_size": first_size,
            "final_size": last_size,
            "total_change": last_size - first_size,
            "growth_rate": (last_size - first_size) / max(first_size, 1),
            "avg_growth_per_turn": (last_size - first_size) / max(len(self.states) - 1, 1),
        }

    def _get_top_entities(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N entities by activation count."""
        sorted_entities = sorted(
            self.entity_activations.values(),
            key=lambda a: (a.activation_count, a.avg_relevance),
            reverse=True,
        )

        return [
            {
                "entity_id": a.entity_id,
                "entity_type": a.entity_type,
                "entity_name": a.entity_name,
                "activation_count": a.activation_count,
                "avg_relevance": round(a.avg_relevance, 3),
                "persistence": a.persistence,
            }
            for a in sorted_entities[:n]
        ]

    def _get_entity_type_distribution(self) -> Dict[str, int]:
        """Get count of entities by type."""
        distribution: Dict[str, int] = {}
        for activation in self.entity_activations.values():
            distribution[activation.entity_type] = distribution.get(activation.entity_type, 0) + 1
        return distribution

    def _get_context_evolution(self) -> List[Dict[str, int]]:
        """Get context size evolution over turns."""
        return [
            {
                "turn": state.turn_number,
                "size": state.context.total_entities,
                **state.context.size_breakdown,
            }
            for state in self.states
        ]
