"""
Temporal Tracker Agent - Usage Examples
========================================

This module demonstrates how to use the Legislative Temporal Schema
to track Australian legislation through its complete lifecycle.

See also:
- docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md (complete reference)
- src/agents/legislative_temporal_schema.py (schema definitions)
"""

from datetime import date, timedelta
from src.agents.legislative_temporal_schema import (
    LegislativeDocument,
    TemporalTracker,
    LegislationQuery,
    LegislationType,
    Jurisdiction,
    LegislativeState,
    CommencementMethod,
    BillType,
    HouseOfOrigin,
    AmendmentType,
    RepealType,
    SectionCommencement,
    Amendment,
)


def example_1_complete_bill_to_act_lifecycle():
    """
    Example 1: Track a bill from introduction through to Act in force.

    Demonstrates: Family Law Amendment Bill 2024 → Act
    """
    print("=" * 80)
    print("EXAMPLE 1: Complete Bill to Act Lifecycle")
    print("=" * 80)

    tracker = TemporalTracker()
    query = LegislationQuery(tracker)

    # === STAGE 1: Bill Introduction ===
    print("\n[1] Bill introduced to Parliament...")

    bill = LegislativeDocument(
        document_id="FLA_BILL_2024_045",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.BILL,
        title="Family Law Amendment Bill 2024",
        year=2024,
        number=45,
        current_state=LegislativeState.INTRODUCED,
        bill_type=BillType.GOVERNMENT,
        house_of_origin=HouseOfOrigin.HOUSE_OF_REPRESENTATIVES,
        introduced_date=date(2024, 4, 10),
        introduced_by="Attorney-General"
    )
    tracker.add_document(bill)

    bill.add_temporal_anchor(
        event_date=date(2024, 4, 10),
        event_type="introduction",
        description="First Reading - House of Representatives"
    )

    print(f"  Document ID: {bill.document_id}")
    print(f"  Current State: {bill.current_state}")
    print(f"  Introduced: {bill.introduced_date}")

    # === STAGE 2: Debate and Committee ===
    print("\n[2] Bill debated...")
    bill.second_reading_date = date(2024, 4, 15)
    bill.add_state_change(
        LegislativeState.DEBATED,
        "Second Reading debate commenced"
    )
    print(f"  Current State: {bill.current_state}")

    print("\n[3] Referred to committee...")
    bill.committee_referral_date = date(2024, 4, 22)
    bill.committee_name = "Legal and Constitutional Affairs Committee"
    bill.add_state_change(
        LegislativeState.IN_COMMITTEE,
        "Referred to committee"
    )
    print(f"  Current State: {bill.current_state}")

    # === STAGE 3: Passage ===
    print("\n[4] Bill passed House of Representatives...")
    bill.third_reading_date = date(2024, 5, 27)
    bill.passed_house_date = date(2024, 5, 27)
    bill.add_state_change(
        LegislativeState.PASSED_HOUSE,
        "Third Reading passed (78-52)"
    )
    print(f"  Current State: {bill.current_state}")

    print("\n[5] Bill passed Senate...")
    bill.passed_senate_date = date(2024, 6, 12)
    bill.add_state_change(
        LegislativeState.PASSED_BOTH_HOUSES,
        "Passed both houses"
    )
    print(f"  Current State: {bill.current_state}")

    # === STAGE 4: Royal Assent ===
    print("\n[6] Royal Assent granted...")
    tracker.transition_bill_to_assented(
        bill_id="FLA_BILL_2024_045",
        assent_date=date(2024, 6, 20),
        assent_by="Governor-General"
    )
    print(f"  Current State: {bill.current_state}")
    print(f"  Assent Date: {bill.assent_date}")
    print(f"  Document Type: {bill.document_type} (changed from BILL)")

    # === STAGE 5: Commencement (Partial) ===
    print("\n[7] Determining commencement...")

    # Set up partial commencement
    bill.commencement_method = CommencementMethod.PARTIAL
    bill.section_commencements = [
        SectionCommencement(
            section_range="1-3",
            commencement_method=CommencementMethod.ON_ASSENT,
            commencement_date=date(2024, 6, 20),
            status=LegislativeState.IN_FORCE
        ),
        SectionCommencement(
            section_range="Schedule 1",
            commencement_method=CommencementMethod.FIXED_DATE,
            commencement_date=date(2024, 7, 1),
            status=LegislativeState.SCHEDULED
        ),
        SectionCommencement(
            section_range="Schedule 2",
            commencement_method=CommencementMethod.PROCLAMATION,
            commencement_date=None,
            status=LegislativeState.AWAITING_PROCLAMATION
        ),
    ]

    tracker.determine_commencement_state("FLA_BILL_2024_045")
    print(f"  Current State: {bill.current_state}")
    print(f"  Sections 1-3: IN_FORCE (on assent)")
    print(f"  Schedule 1: SCHEDULED (1 July 2024)")
    print(f"  Schedule 2: AWAITING_PROCLAMATION")

    # === STAGE 6: Proclamation ===
    print("\n[8] Proclamation issued for Schedule 2...")

    # First update state to awaiting proclamation
    bill.add_state_change(
        LegislativeState.AWAITING_PROCLAMATION,
        "Schedule 2 awaiting proclamation"
    )

    tracker.record_proclamation(
        act_id="FLA_BILL_2024_045",
        proclamation_date=date(2024, 8, 15),
        proclaimed_commencement_date=date(2024, 9, 1),
        gazette_reference="C2024G00156"
    )

    # Update section commencements
    bill.section_commencements[2].commencement_date = date(2024, 9, 1)
    bill.section_commencements[2].status = LegislativeState.IN_FORCE
    bill.section_commencements[2].proclamation_reference = "C2024G00156"

    print(f"  Proclamation: {bill.proclamation_reference}")
    print(f"  Schedule 2 commences: {bill.proclaimed_commencement_date}")

    # Update to fully in force on Sept 1
    bill.add_state_change(
        LegislativeState.IN_FORCE,
        "All provisions now in force"
    )

    print(f"\n[9] Final State: {bill.current_state}")
    print(f"  Total Temporal Anchors: {len(bill.temporal_anchors)}")
    print(f"  State History Length: {len(bill.state_history)}")

    return tracker


def example_2_amendment_tracking():
    """
    Example 2: Track amendments to a Principal Act.

    Demonstrates: Family Law Act 1975 being amended
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Amendment Tracking")
    print("=" * 80)

    tracker = TemporalTracker()

    # === Create Principal Act ===
    print("\n[1] Principal Act: Family Law Act 1975")

    principal = LegislativeDocument(
        document_id="FLA_1975",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Act 1975",
        year=1975,
        number=53,
        current_state=LegislativeState.IN_FORCE,
        is_principal_act=True,
        assent_date=date(1975, 6, 12),
        commencement_date=date(1976, 1, 5),
    )
    tracker.add_document(principal)

    print(f"  Document ID: {principal.document_id}")
    print(f"  In force since: {principal.commencement_date}")

    # === Create Amending Act ===
    print("\n[2] Amending Act: Family Law Amendment Act 2024")

    amending_act = LegislativeDocument(
        document_id="FLA_2024_045",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Amendment Act 2024",
        year=2024,
        number=45,
        current_state=LegislativeState.IN_FORCE,
        is_amending_act=True,
        amends_act_id="FLA_1975",
        assent_date=date(2024, 6, 20),
        commencement_date=date(2024, 7, 1),
    )
    tracker.add_document(amending_act)

    # === Add Amendments ===
    print("\n[3] Recording amendments...")

    amendment_1 = Amendment(
        amendment_id="FLA_2024_045_ITEM_1",
        amending_act_id="FLA_2024_045",
        item_number=1,
        target_section="Section 79(4)(c)",
        amendment_type=AmendmentType.SUBSTITUTE,
        old_text="the financial resources of each of the parties",
        new_text="the financial resources available to each party, including earning capacity",
        effective_date=date(2024, 7, 1),
        status=LegislativeState.IN_FORCE
    )

    amendment_2 = Amendment(
        amendment_id="FLA_2024_045_ITEM_2",
        amending_act_id="FLA_2024_045",
        item_number=2,
        target_section="After section 60CC",
        amendment_type=AmendmentType.INSERT,
        new_text="60CCA Considerations for parenting orders - family violence\n(1) In making a parenting order...",
        effective_date=date(2024, 7, 1),
        status=LegislativeState.IN_FORCE
    )

    amending_act.amendments = [amendment_1, amendment_2]

    print(f"  Amendment 1: {amendment_1.target_section} - {amendment_1.amendment_type}")
    print(f"  Amendment 2: {amendment_2.target_section} - {amendment_2.amendment_type}")

    # === Record Amendment Relationship ===
    print("\n[4] Creating compilation...")

    tracker.record_amendment(
        principal_act_id="FLA_1975",
        amending_act=amending_act
    )

    print(f"  Principal Act amended by: {principal.amended_by}")
    print(f"  Current compilation: No. {principal.current_compilation.compilation_number}")
    print(f"  As at date: {principal.current_compilation.as_at_date}")

    # === Query Amendments ===
    print("\n[5] Querying amendments...")

    query = LegislationQuery(tracker)
    amendments = query.get_amendments_to_act("FLA_1975")

    print(f"  Total amendments to FLA 1975: {len(amendments)}")
    for amend in amendments:
        print(f"    - {amend.title} ({amend.year})")

    return tracker


def example_3_sunsetting_regulations():
    """
    Example 3: Track sunsetting of subordinate legislation.

    Demonstrates: 10-year sunset cycle for regulations
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Sunsetting of Regulations")
    print("=" * 80)

    tracker = TemporalTracker()

    # === Create Enabling Act ===
    print("\n[1] Enabling Act: Family Law Act 1975")

    enabling_act = LegislativeDocument(
        document_id="FLA_1975",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Act 1975",
        year=1975,
        current_state=LegislativeState.IN_FORCE,
    )
    tracker.add_document(enabling_act)

    # === Create Regulation ===
    print("\n[2] Regulation: Family Law Rules 2024")

    regulation = LegislativeDocument(
        document_id="FLR_2024",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.REGULATION,
        title="Family Law Rules 2024",
        year=2024,
        current_state=LegislativeState.IN_FORCE,
        enabling_act_id="FLA_1975",
        enabling_section="Section 123",
        rule_maker="Governor-General",
        registration_date=date(2024, 3, 15),
        federal_register_id="F2024L00234",
    )
    tracker.add_document(regulation)

    print(f"  Document ID: {regulation.document_id}")
    print(f"  Registered: {regulation.registration_date}")
    print(f"  Enabling Act: {regulation.enabling_act_id}")

    # === Calculate Sunset Date ===
    print("\n[3] Calculating sunset date...")

    sunset_date = regulation.calculate_sunset_date()
    regulation.sunset_date = sunset_date

    print(f"  Registration: {regulation.registration_date}")
    print(f"  Sunset Date: {sunset_date} (10 years later)")
    print(f"  Days until sunset: {(sunset_date - date.today()).days}")

    # === Check Sunset Status (Simulate Future) ===
    print("\n[4] Checking sunset status...")

    # Simulate checking 18 months before sunset
    check_date_1 = sunset_date - timedelta(days=600)
    print(f"\n  Checking on: {check_date_1}")
    tracker.check_sunset("FLR_2024", check_date_1)
    print(f"  State: {regulation.current_state}")

    # Simulate checking on sunset date
    check_date_2 = sunset_date
    print(f"\n  Checking on: {check_date_2}")
    tracker.check_sunset("FLR_2024", check_date_2)
    print(f"  State: {regulation.current_state}")
    print(f"  Is Repealed: {regulation.is_repealed}")
    print(f"  Repeal Type: {regulation.repeal_type}")

    # === Query Pending Sunsets ===
    print("\n[5] Finding regulations pending sunset...")

    # Create more regulations
    for i in range(3):
        reg = LegislativeDocument(
            document_id=f"REG_{2015 + i}",
            jurisdiction=Jurisdiction.COMMONWEALTH,
            document_type=LegislationType.REGULATION,
            title=f"Test Regulation {2015 + i}",
            year=2015 + i,
            current_state=LegislativeState.IN_FORCE,
            registration_date=date(2015 + i, 1, 1),
        )
        reg.sunset_date = reg.calculate_sunset_date()
        tracker.add_document(reg)

    query = LegislationQuery(tracker)
    pending = query.get_regulations_pending_sunset(months_ahead=120)

    print(f"  Regulations pending sunset (next 10 years): {len(pending)}")
    for reg in pending:
        print(f"    - {reg.title}: sunsets {reg.sunset_date}")

    return tracker


def example_4_repeal_and_savings():
    """
    Example 4: Track repeal with savings provisions.

    Demonstrates: Act repealed but with transitional provisions
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Repeal with Savings Provisions")
    print("=" * 80)

    tracker = TemporalTracker()

    # === Create Act to be Repealed ===
    print("\n[1] Original Act")

    old_act = LegislativeDocument(
        document_id="OLD_ACT_2010",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law (Old Provisions) Act 2010",
        year=2010,
        current_state=LegislativeState.IN_FORCE,
        assent_date=date(2010, 6, 15),
        commencement_date=date(2010, 7, 1),
    )
    tracker.add_document(old_act)

    print(f"  Document ID: {old_act.document_id}")
    print(f"  In force since: {old_act.commencement_date}")

    # === Create Repealing Act ===
    print("\n[2] Repealing Act")

    repealing_act = LegislativeDocument(
        document_id="REPEAL_ACT_2024",
        jurisdiction=Jurisdiction.COMMONWEALTH,
        document_type=LegislationType.ACT,
        title="Family Law Repeal and Transitional Provisions Act 2024",
        year=2024,
        current_state=LegislativeState.IN_FORCE,
        assent_date=date(2024, 6, 20),
        commencement_date=date(2024, 7, 1),
    )
    tracker.add_document(repealing_act)

    # === Add Savings and Transitional Provisions ===
    print("\n[3] Savings and Transitional Provisions")

    from src.agents.legislative_temporal_schema import SavingsTransitionalProvisions

    old_act.savings_transitional = SavingsTransitionalProvisions(
        has_savings=True,
        has_transitional=True,
        transition_end_date=date(2026, 6, 30),
        provisions_text="""
        Schedule 2 - Savings and Transitional Provisions

        1. Applications lodged before commencement
           Applications lodged under the repealed Act before 1 July 2024
           continue to be dealt with under the old law.

        2. Orders made under repealed Act
           Orders made under the repealed Act remain in force and may be
           varied or discharged under the new Act.

        3. Proceedings commenced before commencement
           Proceedings commenced before 1 July 2024 continue under the old law
           until final determination.
        """,
        location="Schedule 2 of Repeal Act",
        affected_rights=["pending_applications", "existing_orders", "current_proceedings"]
    )

    print(f"  Has savings provisions: {old_act.savings_transitional.has_savings}")
    print(f"  Has transitional provisions: {old_act.savings_transitional.has_transitional}")
    print(f"  Transition ends: {old_act.savings_transitional.transition_end_date}")

    # === Record Repeal ===
    print("\n[4] Recording repeal...")

    tracker.record_repeal(
        act_id="OLD_ACT_2010",
        repeal_date=date(2024, 7, 1),
        repealing_act_id="REPEAL_ACT_2024",
        repeal_type=RepealType.EXPRESS
    )

    print(f"  Current State: {old_act.current_state}")
    print(f"  Repealed by: {old_act.repealed_by_act_id}")
    print(f"  Repeal Date: {old_act.repeal_date}")

    # === Check In Force Status Over Time ===
    print("\n[5] Checking in-force status over time...")

    dates_to_check = [
        date(2015, 1, 1),  # Before repeal
        date(2024, 6, 30),  # Day before repeal
        date(2024, 7, 1),   # Day of repeal
        date(2025, 1, 1),   # After repeal
    ]

    for check_date in dates_to_check:
        in_force = old_act.is_in_force_on(check_date)
        print(f"  {check_date}: {'IN FORCE' if in_force else 'NOT IN FORCE'}")

    print(f"\n  Note: Despite repeal, transitional provisions apply until {old_act.savings_transitional.transition_end_date}")

    return tracker


def example_5_temporal_queries():
    """
    Example 5: Query documents by temporal criteria.

    Demonstrates: Complex queries across time
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Temporal Queries")
    print("=" * 80)

    # Build sample dataset
    tracker = TemporalTracker()

    # Add various documents
    docs_data = [
        ("ACT_2020", "Act 2020", date(2020, 1, 1), LegislativeState.IN_FORCE, None),
        ("ACT_2021", "Act 2021", date(2021, 1, 1), LegislativeState.IN_FORCE, None),
        ("ACT_2022", "Act 2022", date(2022, 1, 1), LegislativeState.IN_FORCE, date(2024, 1, 1)),
        ("BILL_2024", "Bill 2024", None, LegislativeState.DEBATED, None),
        ("REG_2023", "Regulation 2023", date(2023, 1, 1), LegislativeState.IN_FORCE, None),
    ]

    for doc_id, title, commence, state, repeal in docs_data:
        doc_type = LegislationType.REGULATION if "REG" in doc_id else (
            LegislationType.BILL if "BILL" in doc_id else LegislationType.ACT
        )

        doc = LegislativeDocument(
            document_id=doc_id,
            jurisdiction=Jurisdiction.COMMONWEALTH,
            document_type=doc_type,
            title=title,
            year=int(doc_id.split("_")[1]),
            current_state=state,
            commencement_date=commence,
            is_repealed=repeal is not None,
            repeal_date=repeal,
        )
        tracker.add_document(doc)

    query = LegislationQuery(tracker)

    # === Query 1: In force on specific date ===
    print("\n[1] Acts in force on 2022-06-01:")
    results = query.get_in_force_on_date(
        check_date=date(2022, 6, 1),
        document_type=LegislationType.ACT
    )
    for doc in results:
        print(f"  - {doc.title}")

    # === Query 2: Bills currently in Parliament ===
    print("\n[2] Bills currently in Parliament:")
    results = query.get_bills_in_parliament(Jurisdiction.COMMONWEALTH)
    for doc in results:
        print(f"  - {doc.title} ({doc.current_state})")

    # === Query 3: Documents by state ===
    print("\n[3] All documents currently IN_FORCE:")
    results = query.get_documents_by_state(
        LegislativeState.IN_FORCE,
        Jurisdiction.COMMONWEALTH
    )
    for doc in results:
        print(f"  - {doc.title} ({doc.document_type})")

    # === Query 4: Historical state check ===
    print("\n[4] State of ACT_2022 over time:")
    doc = tracker.get_document("ACT_2022")
    check_dates = [
        date(2021, 6, 1),
        date(2022, 6, 1),
        date(2024, 6, 1),
    ]
    for check_date in check_dates:
        in_force = doc.is_in_force_on(check_date)
        print(f"  {check_date}: {'IN FORCE' if in_force else 'NOT IN FORCE'}")

    return tracker


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("TEMPORAL TRACKER AGENT - USAGE EXAMPLES")
    print("Australian Legislative Lifecycle Tracking")
    print("=" * 80)

    # Run examples
    example_1_complete_bill_to_act_lifecycle()
    example_2_amendment_tracking()
    example_3_sunsetting_regulations()
    example_4_repeal_and_savings()
    example_5_temporal_queries()

    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nFor full documentation, see:")
    print("  - docs/AUSTRALIAN_LEGISLATIVE_LIFECYCLE.md")
    print("  - src/agents/legislative_temporal_schema.py")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
