from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

# --- Universal GSW Primitives ---


class TemporalEntity(BaseModel):
    """Base class for anything that has a lifespan or occurrence time."""

    start_date: str | None = None  # Relaxed from date
    end_date: str | None = None  # Relaxed from date
    is_ongoing: bool = False


# --- Entities ---


class Entity(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None
    # Track which Case IDs this entity appears in
    involved_cases: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def ensure_id(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        return self


class Person(Entity):
    dob: str | None = None
    role_in_case: str | None = None


class Object(Entity):
    type: str


# --- Narrative Nodes ---


class State(TemporalEntity):
    entity_id: str | None = None
    name: str
    value: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Event(BaseModel):
    id: str | None = None
    date: str | None = None  # Relaxed
    type: str
    description: str
    participant_ids: list[str] = Field(default_factory=list)
    object_ids: list[str] = Field(default_factory=list)
    triggered_state_ids: list[str] = Field(
        default_factory=list, alias="triggered_states"
    )  # Alias to handle model output

    @model_validator(mode="after")
    def ensure_id(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        return self


# --- Legal Outcomes ---

# OutcomeType Enum removed for flexibility
# We will normalize strings like "Application" -> "Procedural" in a later phase.


class LegalOutcome(BaseModel):
    id: str | None = None
    type: str = (
        "Other"  # Now a string to accept any raw label (e.g. "Application", "Interim Order")
    )
    description: str
    orders: list[str] = Field(default_factory=list)
    granted_to_ids: list[str] = Field(default_factory=list)
    related_object_ids: list[str] = Field(default_factory=list)

    @field_validator("orders", mode="before")
    @classmethod
    def normalize_orders(cls, v):
        """Flatten structured orders (dicts) to strings if the model gets too creative."""
        if isinstance(v, list):
            new_orders = []
            for item in v:
                if isinstance(item, dict):
                    # Extract 'text' or 'description' or just dump it
                    new_orders.append(item.get("text") or item.get("description") or str(item))
                else:
                    new_orders.append(str(item))
            return new_orders
        return v

    @model_validator(mode="after")
    def ensure_id(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        return self


# --- The Case Container ---


class LegalCase(BaseModel):
    case_id: str | None = None
    title: str | None = None

    # Changed to Lists for robustness
    persons: list[Person] = Field(default_factory=list)
    objects: list[Object] = Field(default_factory=list)

    timeline: list[Event] = Field(default_factory=list)
    states: list[State] = Field(default_factory=list)
    outcomes: list[LegalOutcome] = Field(default_factory=list)

    @model_validator(mode="after")
    def ensure_case_id(self):
        if not self.case_id:
            self.case_id = str(uuid.uuid4())
        return self

    def get_entity_states(self, entity_id: str) -> list[State]:
        return [s for s in self.states if s.entity_id == entity_id]
