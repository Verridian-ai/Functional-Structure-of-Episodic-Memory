"""
Legislative Temporal Schema for Temporal Tracker Agent
======================================================

This module defines the complete temporal tracking schema for Australian legislation.
Based on: docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md

Usage:
    from src.agents.legislative_temporal_schema import LegislativeDocument, TemporalTracker

    tracker = TemporalTracker()
    doc = LegislativeDocument(
        document_id="FLA_2024_045",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Amendment Act 2024",
        year=2024,
        number=45,
        current_state=LegislativeState.IN_FORCE
    )
"""

from enum import Enum
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# ENUMERATIONS
# ============================================================================

class LegislationType(str, Enum):
    """Type of legislative document"""
    BILL = "bill"
    ACT = "act"
    REGULATION = "regulation"
    RULE = "rule"
    DETERMINATION = "determination"
    PROCLAMATION = "proclamation"
    ORDINANCE = "ordinance"


class Jurisdiction(str, Enum):
    """Australian jurisdiction"""
    COMMONWEALTH = "commonwealth"
    NSW = "nsw"
    VICTORIA = "vic"
    QUEENSLAND = "qld"
    SOUTH_AUSTRALIA = "sa"
    WESTERN_AUSTRALIA = "wa"
    TASMANIA = "tas"
    ACT = "act"
    NORTHERN_TERRITORY = "nt"


class LegislativeState(str, Enum):
    """
    Complete state machine for Australian legislation.
    See docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md for state diagram.
    """
    # Bills (pre-assent)
    DRAFTED = "drafted"
    INTRODUCED = "introduced"
    DEBATED = "debated"
    IN_COMMITTEE = "in_committee"
    UNDER_AMENDMENT = "under_amendment"
    PASSED_HOUSE = "passed_house"
    IN_SENATE = "in_senate"
    SENATE_AMENDED = "senate_amended"
    RETURNED_TO_HOUSE = "returned_to_house"
    PASSED_SENATE = "passed_senate"
    PASSED_BOTH_HOUSES = "passed_both_houses"
    REJECTED = "rejected"
    LAPSED = "lapsed"
    WITHDRAWN = "withdrawn"

    # Acts (post-assent)
    ASSENTED = "assented"
    PENDING_28_DAY = "pending_28_day"
    AWAITING_PROCLAMATION = "awaiting_proclamation"
    PROCLAIMED = "proclaimed"
    SCHEDULED = "scheduled"
    AWAITING_TRIGGER = "awaiting_trigger"
    TRIGGERED = "triggered"
    IN_FORCE = "in_force"
    PARTIALLY_IN_FORCE = "partially_in_force"
    SUSPENDED = "suspended"
    SPENT = "spent"
    SUNSET_PENDING = "sunset_pending"
    SUPERSEDED = "superseded"
    REPEALED = "repealed"
    SUNSETTED = "sunsetted"
    DISALLOWED = "disallowed"

    # Regulations
    REGISTERED = "registered"
    TABLED = "tabled"
    IN_DISALLOWANCE_PERIOD = "in_disallowance_period"
    REMADE = "remade"


class CommencementMethod(str, Enum):
    """How an Act commences (Section 2 patterns)"""
    ON_ASSENT = "on_assent"
    AUTOMATIC_28_DAYS = "28_days"
    PROCLAMATION = "proclamation"
    FIXED_DATE = "fixed_date"
    RETROSPECTIVE = "retrospective"
    EVENT_TRIGGERED = "event_triggered"
    PARTIAL = "partial"


class AmendmentType(str, Enum):
    """Types of amendments to legislation"""
    OMIT = "omit"
    SUBSTITUTE = "substitute"
    INSERT = "insert"
    REPEAL = "repeal"
    RENUMBER = "renumber"
    RELOCATE = "relocate"


class RepealType(str, Enum):
    """How legislation was repealed"""
    EXPRESS = "express"
    IMPLIED = "implied"
    SUNSET = "sunset"
    DISALLOWANCE = "disallowance"


class BillType(str, Enum):
    """Type of bill"""
    GOVERNMENT = "government"
    PRIVATE_MEMBER = "private_member"
    PRIVATE_SENATOR = "private_senator"


class HouseOfOrigin(str, Enum):
    """Which house bill originated in"""
    HOUSE_OF_REPRESENTATIVES = "house_of_representatives"
    SENATE = "senate"
    LEGISLATIVE_ASSEMBLY = "legislative_assembly"  # State lower house
    LEGISLATIVE_COUNCIL = "legislative_council"     # State upper house


# ============================================================================
# MODELS
# ============================================================================

class TemporalAnchor(BaseModel):
    """
    Key date in legislative lifecycle.
    Represents a significant temporal event (e.g., assent, commencement, repeal).
    """
    date: date
    event_type: str = Field(..., description="Type of event (e.g., 'royal_assent', 'commencement', 'repeal')")
    description: str = Field(..., description="Human-readable description of event")
    source_document: Optional[str] = Field(None, description="Reference to source (e.g., Gazette notice)")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StateTransition(BaseModel):
    """Record of state transition"""
    from_state: LegislativeState
    to_state: LegislativeState
    transition_date: date
    reason: str
    triggered_by: Optional[str] = Field(None, description="What triggered transition (e.g., Act ID, event)")


class SectionCommencement(BaseModel):
    """
    Commencement details for specific sections/schedules.
    Used when Act has partial commencement (different sections commence differently).
    """
    section_range: str = Field(..., description="e.g., '1-3', 'Schedule 1', 'Part 2'")
    commencement_method: CommencementMethod
    commencement_date: Optional[date] = None
    proclamation_reference: Optional[str] = Field(None, description="Gazette reference if by proclamation")
    trigger_event: Optional[str] = Field(None, description="Event description if event-triggered")
    status: LegislativeState
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Amendment(BaseModel):
    """
    Amendment made by an Amending Act to a Principal Act.
    Tracks individual items in amendment schedules.
    """
    amendment_id: str = Field(..., description="Unique ID for this amendment")
    amending_act_id: str = Field(..., description="ID of the Act making this amendment")
    item_number: int = Field(..., description="Item number in amendment schedule")
    target_section: str = Field(..., description="Section/provision being amended")
    amendment_type: AmendmentType
    old_text: Optional[str] = Field(None, description="Text being replaced (for OMIT/SUBSTITUTE)")
    new_text: Optional[str] = Field(None, description="Replacement text (for SUBSTITUTE/INSERT)")
    effective_date: Optional[date] = Field(None, description="When amendment takes effect")
    status: LegislativeState
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Compilation(BaseModel):
    """
    Compiled version of Act showing all amendments up to a date.
    Published on Federal Register of Legislation.
    """
    compilation_number: int
    as_at_date: date = Field(..., description="Date compilation reflects amendments up to")
    registered_date: date = Field(..., description="Date compilation was registered")
    incorporates_amendments: List[str] = Field(default_factory=list, description="List of amending Act IDs included")
    compilation_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SavingsTransitionalProvisions(BaseModel):
    """
    Savings and transitional provisions when legislation changes.
    Manages rights/obligations during transition.
    """
    has_savings: bool = False
    has_transitional: bool = False
    transition_end_date: Optional[date] = None
    provisions_text: Optional[str] = Field(None, description="Full text of provisions")
    location: Optional[str] = Field(None, description="Where provisions are located (e.g., 'Schedule 2')")
    affected_rights: List[str] = Field(default_factory=list, description="Rights/obligations affected")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LegislativeDocument(BaseModel):
    """
    Complete legislative document with full temporal tracking.

    This model represents any Australian legislative document (Bill, Act, Regulation)
    and tracks its complete lifecycle from introduction through termination.
    """

    # ========== IDENTITY ==========
    document_id: str = Field(..., description="Unique identifier (e.g., 'FLA_2024_045')")
    jurisdiction: Jurisdiction
    document_type: LegislationType
    title: str
    short_title: Optional[str] = None
    year: int
    number: Optional[int] = Field(None, description="Act/Bill number (e.g., 45 for 'No. 45 of 2024')")

    # ========== CURRENT STATE ==========
    current_state: LegislativeState
    state_history: List[StateTransition] = Field(default_factory=list)

    # ========== BILL STAGE (if applicable) ==========
    bill_type: Optional[BillType] = None
    house_of_origin: Optional[HouseOfOrigin] = None
    introduced_date: Optional[date] = None
    introduced_by: Optional[str] = Field(None, description="Minister or Member who introduced")

    # Reading dates
    first_reading_date: Optional[date] = None
    second_reading_date: Optional[date] = None
    third_reading_date: Optional[date] = None

    # Committee stage
    committee_referral_date: Optional[date] = None
    committee_name: Optional[str] = None
    committee_report_date: Optional[date] = None

    # Passage through houses
    passed_house_date: Optional[date] = None
    passed_senate_date: Optional[date] = None

    # Constitutional restrictions
    is_money_bill: bool = False
    is_appropriation_bill: bool = False

    # ========== ACT CREATION (if applicable) ==========
    assent_date: Optional[date] = None
    assent_by: Optional[str] = Field(None, description="Governor-General or State Governor")

    # Commencement
    commencement_method: Optional[CommencementMethod] = None
    commencement_date: Optional[date] = None
    section_commencements: List[SectionCommencement] = Field(default_factory=list)

    # Proclamation (if applicable)
    proclamation_date: Optional[date] = None
    proclamation_reference: Optional[str] = Field(None, description="Gazette reference")
    proclaimed_commencement_date: Optional[date] = None

    # Event-triggered (if applicable)
    trigger_event: Optional[str] = None
    trigger_date: Optional[date] = None

    # ========== AMENDMENTS (if this is Amending Act) ==========
    is_amending_act: bool = False
    amends_act_id: Optional[str] = Field(None, description="ID of Principal Act being amended")
    amendments: List[Amendment] = Field(default_factory=list)

    # ========== AMENDMENTS (if this is Principal Act) ==========
    is_principal_act: bool = False
    amended_by: List[str] = Field(default_factory=list, description="List of amending Act IDs")
    compilations: List[Compilation] = Field(default_factory=list)
    current_compilation: Optional[Compilation] = None

    # ========== TERMINATION ==========
    is_repealed: bool = False
    repeal_date: Optional[date] = None
    repealed_by_act_id: Optional[str] = None
    repeal_type: Optional[RepealType] = None

    is_spent: bool = False
    spent_reason: Optional[str] = None
    spent_determination_date: Optional[date] = None

    # Savings and transitional
    savings_transitional: Optional[SavingsTransitionalProvisions] = None

    # ========== SUBORDINATE LEGISLATION (if applicable) ==========
    enabling_act_id: Optional[str] = Field(None, description="ID of Act authorizing this regulation")
    enabling_section: Optional[str] = Field(None, description="Section of enabling Act")
    rule_maker: Optional[str] = Field(None, description="e.g., 'Governor-General', 'Minister for X'")

    # Registration and sunsetting
    registration_date: Optional[date] = None
    federal_register_id: Optional[str] = None
    sunset_date: Optional[date] = None
    sunset_exempt: bool = False
    sunset_exemption_reason: Optional[str] = None

    # Disallowance
    tabled_date_house: Optional[date] = None
    tabled_date_senate: Optional[date] = None
    disallowance_period_ends: Optional[date] = None
    disallowance_exempt: bool = False
    disallowed_date: Optional[date] = None

    # ========== TEMPORAL ANCHORS ==========
    temporal_anchors: List[TemporalAnchor] = Field(default_factory=list)

    # ========== METADATA ==========
    source_url: Optional[str] = Field(None, description="URL on Federal Register or Parliament website")
    explanatory_memorandum_url: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # ========== METHODS ==========

    def add_state_change(
        self,
        new_state: LegislativeState,
        reason: str,
        triggered_by: Optional[str] = None
    ) -> None:
        """Record state transition"""
        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            transition_date=date.today(),
            reason=reason,
            triggered_by=triggered_by
        )
        self.state_history.append(transition)
        self.current_state = new_state
        self.last_updated = datetime.now()

    def calculate_28_day_commencement(self) -> Optional[date]:
        """
        Calculate automatic commencement date (Acts Interpretation Act 1901 s 3A).
        Returns assent_date + 28 days.
        """
        if self.assent_date:
            return self.assent_date + timedelta(days=28)
        return None

    def calculate_sunset_date(self) -> Optional[date]:
        """
        Calculate sunset date for subordinate legislation (Legislation Act 2003 s 50).
        Returns 10 years from registration, nearest 1 April or 1 October.
        """
        if not self.registration_date:
            return None

        if self.document_type not in [
            LegislationType.REGULATION,
            LegislationType.RULE,
            LegislationType.DETERMINATION
        ]:
            return None

        # 10 years from registration
        ten_years = self.registration_date.replace(year=self.registration_date.year + 10)

        # Find nearest 1 Apr or 1 Oct
        april_1 = date(ten_years.year, 4, 1)
        oct_1 = date(ten_years.year, 10, 1)

        if ten_years <= april_1:
            return april_1
        elif ten_years <= oct_1:
            return oct_1
        else:
            return date(ten_years.year + 1, 4, 1)

    def is_in_force_on(self, check_date: date) -> bool:
        """
        Check if Act/regulation was in force on a specific date.

        Args:
            check_date: Date to check

        Returns:
            True if document was in force on that date
        """
        # Must be commenced
        if not self.commencement_date or check_date < self.commencement_date:
            return False

        # Must not be repealed (or check date is before repeal)
        if self.is_repealed and self.repeal_date and check_date >= self.repeal_date:
            return False

        # Must not be sunsetted
        if self.sunset_date and check_date >= self.sunset_date:
            return False

        return True

    def get_state_on_date(self, check_date: date) -> Optional[LegislativeState]:
        """
        Get the state of the document on a specific historical date.

        Args:
            check_date: Date to check

        Returns:
            LegislativeState on that date, or None if no history
        """
        # Start with earliest state (before any transitions)
        if not self.state_history:
            return self.current_state if check_date >= date.today() else None

        # Find last transition on or before check_date
        current_state = None
        for transition in sorted(self.state_history, key=lambda t: t.transition_date):
            if transition.transition_date <= check_date:
                current_state = transition.to_state
            else:
                break

        return current_state

    def get_compilation_on_date(self, check_date: date) -> Optional[Compilation]:
        """
        Get the compiled version that was current on a specific date.

        Args:
            check_date: Date to check

        Returns:
            Compilation current on that date, or None
        """
        # Find latest compilation on or before check_date
        valid_compilations = [
            c for c in self.compilations
            if c.as_at_date <= check_date
        ]

        if not valid_compilations:
            return None

        return max(valid_compilations, key=lambda c: c.as_at_date)

    def add_temporal_anchor(
        self,
        event_date: date,
        event_type: str,
        description: str,
        source_document: Optional[str] = None
    ) -> None:
        """Add a temporal anchor (key event)"""
        anchor = TemporalAnchor(
            date=event_date,
            event_type=event_type,
            description=description,
            source_document=source_document
        )
        self.temporal_anchors.append(anchor)

        # Sort anchors by date
        self.temporal_anchors.sort(key=lambda a: a.date)


# ============================================================================
# TEMPORAL TRACKER
# ============================================================================

class TemporalTracker:
    """
    Manages legislative documents and their temporal state transitions.

    This is the main interface for tracking Australian legislation lifecycle.
    """

    def __init__(self):
        self.documents: Dict[str, LegislativeDocument] = {}

    def add_document(self, doc: LegislativeDocument) -> None:
        """Add document to tracker"""
        self.documents[doc.document_id] = doc

    def get_document(self, document_id: str) -> Optional[LegislativeDocument]:
        """Retrieve document by ID"""
        return self.documents.get(document_id)

    def transition_bill_to_assented(
        self,
        bill_id: str,
        assent_date: date,
        assent_by: str = "Governor-General"
    ) -> LegislativeDocument:
        """
        Transition bill to Act upon Royal Assent.

        Args:
            bill_id: ID of bill
            assent_date: Date of Royal Assent
            assent_by: Who granted assent (default: Governor-General)

        Returns:
            Updated document

        Raises:
            ValueError: If bill not in correct state
        """
        doc = self.documents[bill_id]

        if doc.current_state != LegislativeState.PASSED_BOTH_HOUSES:
            raise ValueError(
                f"Bill must be in 'passed_both_houses' state, currently: {doc.current_state}"
            )

        # Update to Act
        doc.assent_date = assent_date
        doc.assent_by = assent_by
        doc.document_type = LegislationType.ACT
        doc.add_state_change(
            LegislativeState.ASSENTED,
            "Royal Assent received",
            triggered_by=assent_by
        )

        # Add temporal anchor
        doc.add_temporal_anchor(
            event_date=assent_date,
            event_type="royal_assent",
            description=f"Royal Assent by {assent_by}"
        )

        return doc

    def determine_commencement_state(self, act_id: str) -> LegislativeDocument:
        """
        Determine commencement state after assent based on Section 2.

        Args:
            act_id: ID of Act

        Returns:
            Updated document

        Raises:
            ValueError: If Act not assented
        """
        doc = self.documents[act_id]

        if doc.current_state != LegislativeState.ASSENTED:
            raise ValueError(f"Act must be assented, currently: {doc.current_state}")

        # Determine based on commencement method
        if doc.commencement_method == CommencementMethod.ON_ASSENT:
            doc.commencement_date = doc.assent_date
            doc.add_state_change(
                LegislativeState.IN_FORCE,
                "Commenced on assent (Section 2)"
            )

        elif doc.commencement_method == CommencementMethod.AUTOMATIC_28_DAYS:
            doc.commencement_date = doc.calculate_28_day_commencement()
            doc.add_state_change(
                LegislativeState.PENDING_28_DAY,
                f"Awaiting automatic commencement on {doc.commencement_date}"
            )

        elif doc.commencement_method == CommencementMethod.PROCLAMATION:
            doc.add_state_change(
                LegislativeState.AWAITING_PROCLAMATION,
                "Awaiting proclamation (Section 2)"
            )

        elif doc.commencement_method == CommencementMethod.FIXED_DATE:
            doc.add_state_change(
                LegislativeState.SCHEDULED,
                f"Scheduled to commence on {doc.commencement_date}"
            )

        elif doc.commencement_method == CommencementMethod.EVENT_TRIGGERED:
            doc.add_state_change(
                LegislativeState.AWAITING_TRIGGER,
                f"Awaiting trigger event: {doc.trigger_event}"
            )

        elif doc.commencement_method == CommencementMethod.PARTIAL:
            doc.add_state_change(
                LegislativeState.PARTIALLY_IN_FORCE,
                "Partial commencement (see section_commencements)"
            )

        return doc

    def record_proclamation(
        self,
        act_id: str,
        proclamation_date: date,
        proclaimed_commencement_date: date,
        gazette_reference: str
    ) -> LegislativeDocument:
        """
        Record proclamation of commencement.

        Args:
            act_id: ID of Act
            proclamation_date: Date proclamation issued
            proclaimed_commencement_date: Date Act will commence
            gazette_reference: Gazette reference (e.g., "C2024G00156")

        Returns:
            Updated document
        """
        doc = self.documents[act_id]

        if doc.current_state != LegislativeState.AWAITING_PROCLAMATION:
            raise ValueError(
                f"Act must be awaiting proclamation, currently: {doc.current_state}"
            )

        doc.proclamation_date = proclamation_date
        doc.proclaimed_commencement_date = proclaimed_commencement_date
        doc.proclamation_reference = gazette_reference
        doc.commencement_date = proclaimed_commencement_date

        doc.add_state_change(
            LegislativeState.PROCLAIMED,
            f"Proclaimed to commence {proclaimed_commencement_date}"
        )

        doc.add_temporal_anchor(
            event_date=proclamation_date,
            event_type="proclamation",
            description=f"Proclamation issued: {gazette_reference}",
            source_document=gazette_reference
        )

        # If commencement is immediate or in past, transition to IN_FORCE
        if proclaimed_commencement_date <= date.today():
            doc.add_state_change(
                LegislativeState.IN_FORCE,
                "Commenced by proclamation"
            )

        return doc

    def record_amendment(
        self,
        principal_act_id: str,
        amending_act: LegislativeDocument
    ) -> LegislativeDocument:
        """
        Record amendment to principal Act.

        Args:
            principal_act_id: ID of Act being amended
            amending_act: The amending Act

        Returns:
            Updated principal Act
        """
        principal = self.documents[principal_act_id]

        # Add to principal's amendment list
        if amending_act.document_id not in principal.amended_by:
            principal.amended_by.append(amending_act.document_id)

        # Create new compilation
        compilation = Compilation(
            compilation_number=len(principal.compilations) + 1,
            as_at_date=amending_act.commencement_date or date.today(),
            registered_date=date.today(),
            incorporates_amendments=principal.amended_by.copy()
        )
        principal.compilations.append(compilation)
        principal.current_compilation = compilation
        principal.last_updated = datetime.now()

        return principal

    def record_repeal(
        self,
        act_id: str,
        repeal_date: date,
        repealing_act_id: str,
        repeal_type: RepealType
    ) -> LegislativeDocument:
        """
        Record repeal of Act.

        Args:
            act_id: ID of Act being repealed
            repeal_date: Date repeal takes effect
            repealing_act_id: ID of Act causing repeal
            repeal_type: How it was repealed

        Returns:
            Updated document
        """
        doc = self.documents[act_id]

        doc.is_repealed = True
        doc.repeal_date = repeal_date
        doc.repealed_by_act_id = repealing_act_id
        doc.repeal_type = repeal_type

        doc.add_state_change(
            LegislativeState.REPEALED,
            f"Repealed by {repealing_act_id} ({repeal_type.value})",
            triggered_by=repealing_act_id
        )

        doc.add_temporal_anchor(
            event_date=repeal_date,
            event_type="repeal",
            description=f"Repealed ({repeal_type.value})"
        )

        return doc

    def check_sunset(
        self,
        regulation_id: str,
        current_date: Optional[date] = None
    ) -> LegislativeDocument:
        """
        Check if regulation should sunset.

        Args:
            regulation_id: ID of regulation
            current_date: Date to check (default: today)

        Returns:
            Updated document
        """
        if current_date is None:
            current_date = date.today()

        doc = self.documents[regulation_id]

        # Only applies to subordinate legislation
        if doc.document_type not in [
            LegislationType.REGULATION,
            LegislationType.RULE,
            LegislationType.DETERMINATION
        ]:
            return doc

        # Skip if exempt
        if doc.sunset_exempt:
            return doc

        # Calculate sunset date if not set
        if not doc.sunset_date:
            doc.sunset_date = doc.calculate_sunset_date()

        if not doc.sunset_date:
            return doc

        # Check if approaching sunset (18 months = 547 days)
        sunset_warning = doc.sunset_date - timedelta(days=547)
        if sunset_warning <= current_date < doc.sunset_date:
            if doc.current_state != LegislativeState.SUNSET_PENDING:
                doc.add_state_change(
                    LegislativeState.SUNSET_PENDING,
                    f"Approaching sunset on {doc.sunset_date}"
                )

        # Check if sunset date reached
        if current_date >= doc.sunset_date:
            doc.add_state_change(
                LegislativeState.SUNSETTED,
                "Automatically sunsetted (Legislation Act 2003 s 50)"
            )
            doc.is_repealed = True
            doc.repeal_date = doc.sunset_date
            doc.repeal_type = RepealType.SUNSET

        return doc


# ============================================================================
# QUERY FUNCTIONS
# ============================================================================

class LegislationQuery:
    """Query legislative documents by temporal criteria"""

    def __init__(self, tracker: TemporalTracker):
        self.tracker = tracker

    def get_in_force_on_date(
        self,
        check_date: date,
        jurisdiction: Optional[Jurisdiction] = None,
        document_type: Optional[LegislationType] = None
    ) -> List[LegislativeDocument]:
        """Get all Acts/regulations in force on a specific date"""
        results = []
        for doc in self.tracker.documents.values():
            if jurisdiction and doc.jurisdiction != jurisdiction:
                continue
            if document_type and doc.document_type != document_type:
                continue
            if doc.is_in_force_on(check_date):
                results.append(doc)
        return results

    def get_amendments_to_act(
        self,
        principal_act_id: str
    ) -> List[LegislativeDocument]:
        """Get all amendments to a principal Act"""
        principal = self.tracker.documents.get(principal_act_id)
        if not principal:
            return []

        return [
            self.tracker.documents[aid]
            for aid in principal.amended_by
            if aid in self.tracker.documents
        ]

    def get_acts_repealed_by(
        self,
        repealing_act_id: str
    ) -> List[LegislativeDocument]:
        """Get all Acts repealed by a specific Act"""
        results = []
        for doc in self.tracker.documents.values():
            if doc.repealed_by_act_id == repealing_act_id:
                results.append(doc)
        return results

    def get_bills_in_parliament(
        self,
        jurisdiction: Jurisdiction
    ) -> List[LegislativeDocument]:
        """Get all bills currently in Parliament"""
        active_bill_states = [
            LegislativeState.INTRODUCED,
            LegislativeState.DEBATED,
            LegislativeState.IN_COMMITTEE,
            LegislativeState.UNDER_AMENDMENT,
            LegislativeState.PASSED_HOUSE,
            LegislativeState.IN_SENATE,
            LegislativeState.SENATE_AMENDED,
            LegislativeState.RETURNED_TO_HOUSE,
            LegislativeState.PASSED_SENATE,
            LegislativeState.PASSED_BOTH_HOUSES
        ]

        results = []
        for doc in self.tracker.documents.values():
            if (doc.jurisdiction == jurisdiction and
                doc.document_type == LegislationType.BILL and
                doc.current_state in active_bill_states):
                results.append(doc)
        return results

    def get_regulations_pending_sunset(
        self,
        months_ahead: int = 18
    ) -> List[LegislativeDocument]:
        """Get regulations approaching sunset"""
        cutoff = date.today() + timedelta(days=months_ahead * 30)

        results = []
        for doc in self.tracker.documents.values():
            if (doc.document_type in [
                    LegislationType.REGULATION,
                    LegislationType.RULE,
                    LegislationType.DETERMINATION
                ] and
                doc.sunset_date and
                doc.sunset_date <= cutoff and
                not doc.sunset_exempt and
                not doc.is_repealed):
                results.append(doc)
        return results

    def get_documents_by_state(
        self,
        state: LegislativeState,
        jurisdiction: Optional[Jurisdiction] = None
    ) -> List[LegislativeDocument]:
        """Get all documents in a specific state"""
        results = []
        for doc in self.tracker.documents.values():
            if jurisdiction and doc.jurisdiction != jurisdiction:
                continue
            if doc.current_state == state:
                results.append(doc)
        return results


__all__ = [
    # Enums
    "LegislationType",
    "Jurisdiction",
    "LegislativeState",
    "CommencementMethod",
    "AmendmentType",
    "RepealType",
    "BillType",
    "HouseOfOrigin",
    # Models
    "TemporalAnchor",
    "StateTransition",
    "SectionCommencement",
    "Amendment",
    "Compilation",
    "SavingsTransitionalProvisions",
    "LegislativeDocument",
    # Main classes
    "TemporalTracker",
    "LegislationQuery",
]
