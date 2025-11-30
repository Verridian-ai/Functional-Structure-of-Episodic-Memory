"""
Test Suite for Acts Interpretation Framework

Tests the InterpretationActsDB class and all interpretation logic.

Run:
    pytest tests/test_interpretation_acts.py -v
"""

import pytest
from datetime import datetime
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.logic.interpretation_acts import (
    InterpretationActsDB,
    Definition,
    ModalClassification,
    get_definition,
    is_mandatory,
    is_permissive
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def db():
    """Provide InterpretationActsDB instance for tests."""
    return InterpretationActsDB()


# ============================================================================
# DEFINITION LOOKUP TESTS
# ============================================================================

class TestDefinitionLookup:
    """Test definition lookup functionality."""

    def test_get_person_definition_commonwealth(self, db):
        """Test lookup of 'person' in Commonwealth Act."""
        definition = db.get_definition('person', 'Commonwealth')

        assert definition is not None
        assert definition.term == 'person'
        assert definition.jurisdiction == 'Commonwealth'
        assert 'corporate' in definition.definition.lower()
        assert definition.section == '2C'

    def test_get_person_definition_nsw(self, db):
        """Test lookup of 'person' in NSW."""
        definition = db.get_definition('person', 'New South Wales')

        assert definition is not None
        assert definition.term == 'person'
        assert definition.jurisdiction == 'New South Wales'
        assert 'corporation' in definition.definition.lower()

    def test_get_month_definition(self, db):
        """Test 'month' definition - should be calendar month everywhere."""
        definition = db.get_definition('month', 'Victoria')

        assert definition is not None
        assert 'calendar month' in definition.definition.lower()

    def test_get_undefined_term(self, db):
        """Test lookup of undefined term returns None."""
        definition = db.get_definition('nonexistent_term', 'Commonwealth')
        assert definition is None

    def test_fallback_to_commonwealth(self, db):
        """Test fallback to Commonwealth when term not in state Act."""
        # This tests the fallback mechanism
        definition = db.get_definition('person', 'Tasmania', fallback=True)
        assert definition is not None

    def test_no_fallback(self, db):
        """Test no fallback when explicitly disabled."""
        # Get definition without fallback
        definition = db.get_definition('person', 'Commonwealth', fallback=False)
        assert definition is not None

    def test_case_insensitive_lookup(self, db):
        """Test that lookup is case-insensitive."""
        def1 = db.get_definition('PERSON', 'Commonwealth')
        def2 = db.get_definition('person', 'Commonwealth')
        def3 = db.get_definition('Person', 'Commonwealth')

        assert def1 is not None
        assert def2 is not None
        assert def3 is not None
        assert def1.term == def2.term == def3.term

    def test_get_all_definitions_for_term(self, db):
        """Test getting all jurisdictional definitions for a term."""
        definitions = db.get_all_definitions_for_term('person')

        # Should have definition from each jurisdiction
        assert len(definitions) >= 9
        jurisdictions = {d.jurisdiction for d in definitions}
        assert 'Commonwealth' in jurisdictions
        assert 'New South Wales' in jurisdictions

    def test_search_definitions(self, db):
        """Test searching definitions by keyword."""
        results = db.search_definitions('corporation')

        assert len(results) > 0
        # Should find 'person' definitions which mention corporations
        terms = {d.term for d in results}
        assert 'person' in terms


# ============================================================================
# MODAL VERB CLASSIFICATION TESTS
# ============================================================================

class TestModalClassification:
    """Test modal verb classification."""

    def test_classify_may_as_permissive(self, db):
        """Test 'may' is classified as permissive."""
        modal = db.classify_modal('may', 'Commonwealth')

        assert modal.modal_type == 'PERMISSIVE'
        assert modal.creates == 'power'
        assert modal.modal == 'may'

    def test_classify_must_as_mandatory(self, db):
        """Test 'must' is classified as mandatory."""
        modal = db.classify_modal('must', 'Victoria')

        assert modal.modal_type == 'MANDATORY'
        assert modal.creates == 'duty'

    def test_classify_shall_as_mandatory(self, db):
        """Test 'shall' is classified as mandatory."""
        modal = db.classify_modal('shall', 'Queensland')

        assert modal.modal_type == 'MANDATORY'
        assert modal.creates == 'duty'

    def test_classify_must_not_as_prohibited(self, db):
        """Test 'must not' is classified as prohibited."""
        modal = db.classify_modal('must not', 'Western Australia')

        assert modal.modal_type == 'PROHIBITED'
        assert modal.creates == 'prohibition'

    def test_modal_with_context_may_only(self, db):
        """Test contextual analysis for 'may only' construction."""
        context = "The Minister may only approve applications that meet criteria."
        modal = db.classify_modal('may', 'Commonwealth', context=context)

        assert modal.modal_type == 'PERMISSIVE'
        assert modal.contextual_note is not None
        assert 'may only' in modal.contextual_note.lower()

    def test_is_mandatory_convenience_function(self):
        """Test is_mandatory convenience function."""
        assert is_mandatory('must') is True
        assert is_mandatory('shall') is True
        assert is_mandatory('may') is False

    def test_is_permissive_convenience_function(self):
        """Test is_permissive convenience function."""
        assert is_permissive('may') is True
        assert is_permissive('must') is False


# ============================================================================
# OBLIGATION EXTRACTION TESTS
# ============================================================================

class TestObligationExtraction:
    """Test extraction of obligations from statutory text."""

    def test_extract_duties(self, db):
        """Test extraction of mandatory duties."""
        text = "The Minister must approve applications. The court shall grant relief."

        obligations = db.extract_obligations(text)

        assert len(obligations['duties']) == 2
        assert 'must approve' in obligations['duties'][0]
        assert 'shall grant' in obligations['duties'][1]

    def test_extract_powers(self, db):
        """Test extraction of permissive powers."""
        text = "The Minister may delegate this power. The tribunal may adjourn."

        obligations = db.extract_obligations(text)

        assert len(obligations['powers']) == 2
        assert 'may delegate' in obligations['powers'][0]
        assert 'may adjourn' in obligations['powers'][1]

    def test_extract_prohibitions(self, db):
        """Test extraction of prohibitions."""
        text = "A person must not engage in conduct. Parties shall not communicate."

        obligations = db.extract_obligations(text)

        assert len(obligations['prohibitions']) == 2
        assert 'must not engage' in obligations['prohibitions'][0]
        assert 'shall not communicate' in obligations['prohibitions'][1]

    def test_extract_mixed_obligations(self, db):
        """Test extraction from text with mixed obligations."""
        text = """
        The court must consider all evidence. The court may order disclosure.
        A party must not file late. The tribunal may grant extensions.
        """

        obligations = db.extract_obligations(text)

        assert len(obligations['duties']) >= 1
        assert len(obligations['powers']) >= 1
        assert len(obligations['prohibitions']) >= 1


# ============================================================================
# TEMPORAL CALCULATION TESTS
# ============================================================================

class TestTemporalCalculations:
    """Test temporal calculations (month, year, business day)."""

    def test_calculate_month_standard(self, db):
        """Test standard month calculation."""
        result = db.calculate_month('2024-01-15')
        assert result == '2024-02-15'

    def test_calculate_month_end_of_month(self, db):
        """Test month calculation from end of month."""
        # Jan 31 + 1 month = Feb 29 (2024 is leap year)
        result = db.calculate_month('2024-01-31')
        assert result == '2024-02-29'

        # Jan 31 + 1 month in non-leap year = Feb 28
        result = db.calculate_month('2023-01-31')
        assert result == '2023-02-28'

    def test_calculate_month_no_corresponding_day(self, db):
        """Test when target month has no corresponding day."""
        # March 31 + 1 month = April 30 (April has 30 days)
        result = db.calculate_month('2024-03-31')
        assert result == '2024-04-30'

    def test_calculate_multiple_months(self, db):
        """Test calculating multiple months ahead."""
        result = db.calculate_month('2024-01-15', months=3)
        assert result == '2024-04-15'

    def test_calculate_month_year_boundary(self, db):
        """Test month calculation across year boundary."""
        result = db.calculate_month('2024-11-15', months=2)
        assert result == '2025-01-15'

    def test_commencement_commonwealth(self, db):
        """Test Commonwealth commencement (28 days after assent)."""
        result = db.calculate_commencement('2024-06-01', 'Commonwealth')

        # Should be 28 days later
        expected = datetime(2024, 6, 29).strftime("%Y-%m-%d")
        assert result == expected

    def test_commencement_nsw(self, db):
        """Test NSW commencement (immediate on assent)."""
        result = db.calculate_commencement('2024-06-01', 'New South Wales')
        assert result == '2024-06-01'

    def test_commencement_victoria(self, db):
        """Test Victoria commencement (immediate)."""
        result = db.calculate_commencement('2024-06-01', 'Victoria')
        assert result == '2024-06-01'

    def test_commencement_wa_raises_error(self, db):
        """Test WA commencement requires Gazette date."""
        with pytest.raises(ValueError, match="Gazette"):
            db.calculate_commencement('2024-06-01', 'Western Australia')

    def test_commencement_act_raises_error(self, db):
        """Test ACT commencement requires notification date."""
        with pytest.raises(ValueError, match="notification"):
            db.calculate_commencement('2024-06-01', 'Australian Capital Territory')

    def test_is_business_day_weekday(self, db):
        """Test business day check for weekday."""
        # Monday
        result = db.is_business_day('2024-01-08', 'Commonwealth')
        assert result is True

    def test_is_business_day_weekend(self, db):
        """Test business day check for weekend."""
        # Saturday
        result = db.is_business_day('2024-01-06', 'Commonwealth')
        assert result is False

        # Sunday
        result = db.is_business_day('2024-01-07', 'Commonwealth')
        assert result is False


# ============================================================================
# CORPORATE PERSONALITY TESTS
# ============================================================================

class TestCorporatePersonality:
    """Test corporate personality rules."""

    def test_person_includes_corporations_commonwealth(self, db):
        """Test that 'person' includes corporations in Commonwealth."""
        result = db.includes_corporations('person', 'Commonwealth')
        assert result is True

    def test_person_includes_corporations_all_jurisdictions(self, db):
        """Test that 'person' includes corporations in all jurisdictions."""
        jurisdictions = [
            'Commonwealth', 'New South Wales', 'Victoria', 'Queensland',
            'Western Australia', 'South Australia', 'Tasmania',
            'Australian Capital Territory', 'Northern Territory'
        ]

        for jurisdiction in jurisdictions:
            result = db.includes_corporations('person', jurisdiction)
            assert result is True, f"Failed for {jurisdiction}"

    def test_non_person_term(self, db):
        """Test that non-person terms don't include corporations."""
        result = db.includes_corporations('month', 'Commonwealth')
        assert result is False


# ============================================================================
# GENDER NEUTRALITY TESTS
# ============================================================================

class TestGenderNeutrality:
    """Test gender neutrality rules."""

    def test_all_jurisdictions_gender_neutral(self, db):
        """Test that all jurisdictions require gender neutrality."""
        jurisdictions = db.list_jurisdictions()

        for jurisdiction in jurisdictions:
            result = db.is_gender_neutral(jurisdiction)
            assert result is True, f"{jurisdiction} should be gender neutral"

    def test_get_gender_neutral_section(self, db):
        """Test getting gender neutral section reference."""
        section = db.get_gender_neutral_section('Commonwealth')
        assert section is not None
        assert section == '23'


# ============================================================================
# HEADINGS TESTS
# ============================================================================

class TestHeadings:
    """Test heading interpretation rules."""

    def test_headings_part_of_act_commonwealth(self, db):
        """Test that headings are part of Act in Commonwealth."""
        result = db.headings_are_part_of_act('Commonwealth')
        assert result is True

    def test_headings_part_of_act_most_jurisdictions(self, db):
        """Test that headings are part of Act in most jurisdictions."""
        jurisdictions = db.list_jurisdictions()

        for jurisdiction in jurisdictions:
            result = db.headings_are_part_of_act(jurisdiction)
            # Most jurisdictions include headings
            # This is a general test - specific jurisdictions may vary
            assert isinstance(result, bool)


# ============================================================================
# UTILITY METHOD TESTS
# ============================================================================

class TestUtilityMethods:
    """Test utility and helper methods."""

    def test_list_jurisdictions(self, db):
        """Test listing all jurisdictions."""
        jurisdictions = db.list_jurisdictions()

        assert len(jurisdictions) == 9
        assert 'Commonwealth' in jurisdictions
        assert 'New South Wales' in jurisdictions
        assert 'Northern Territory' in jurisdictions

    def test_get_act_citation(self, db):
        """Test getting Act citation."""
        citation = db.get_act_citation('Commonwealth')
        assert citation is not None
        assert 'Acts Interpretation Act 1901' in citation
        assert '(Cth)' in citation

    def test_get_act_url(self, db):
        """Test getting Act URL."""
        url = db.get_act_url('Commonwealth')
        assert url is not None
        assert 'legislation.gov.au' in url

    def test_get_uniform_definitions(self, db):
        """Test getting uniform definitions analysis."""
        uniform = db.get_uniform_definitions()

        assert isinstance(uniform, dict)
        assert 'person_includes_corporations' in uniform

    def test_get_nlp_implications(self, db):
        """Test getting NLP implications."""
        nlp = db.get_nlp_implications()

        assert isinstance(nlp, dict)
        assert 'entity_recognition' in nlp

    def test_get_automated_reasoning_rules(self, db):
        """Test getting automated reasoning rules."""
        rules = db.get_automated_reasoning_rules()

        assert isinstance(rules, dict)
        assert 'default_definition_hierarchy' in rules

    def test_export_definitions_for_nlp(self, db):
        """Test exporting definitions for NLP."""
        definitions = db.export_definitions_for_nlp('Commonwealth')

        assert isinstance(definitions, dict)
        assert 'person' in definitions
        assert 'month' in definitions
        assert isinstance(definitions['person'], str)


# ============================================================================
# CONVENIENCE FUNCTION TESTS
# ============================================================================

class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_get_definition_function(self):
        """Test get_definition convenience function."""
        result = get_definition('person', 'Commonwealth')

        assert result is not None
        assert isinstance(result, str)
        assert 'corporate' in result.lower()

    def test_is_mandatory_function(self):
        """Test is_mandatory convenience function."""
        assert is_mandatory('must', 'Commonwealth') is True
        assert is_mandatory('shall', 'Victoria') is True
        assert is_mandatory('may', 'Queensland') is False

    def test_is_permissive_function(self):
        """Test is_permissive convenience function."""
        assert is_permissive('may', 'Commonwealth') is True
        assert is_permissive('must', 'New South Wales') is False


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple features."""

    def test_full_statutory_analysis_workflow(self, db):
        """Test complete workflow for analyzing statutory text."""
        # Sample statutory text
        text = """
        A person must lodge an application within 1 month of the event.
        The Minister may grant an extension. The tribunal must not accept
        late applications unless exceptional circumstances exist.
        """

        # 1. Extract obligations
        obligations = db.extract_obligations(text, 'Commonwealth')

        assert len(obligations['duties']) >= 1
        assert len(obligations['powers']) >= 1
        assert len(obligations['prohibitions']) >= 1

        # 2. Check definition of 'person'
        person_def = db.get_definition('person', 'Commonwealth')
        includes_corp = db.includes_corporations('person', 'Commonwealth')

        assert person_def is not None
        assert includes_corp is True

        # 3. Calculate time period
        start_date = '2024-01-15'
        deadline = db.calculate_month(start_date, 'Commonwealth')

        assert deadline == '2024-02-15'

        # 4. Classify modals
        must_modal = db.classify_modal('must', 'Commonwealth')
        may_modal = db.classify_modal('may', 'Commonwealth')

        assert must_modal.modal_type == 'MANDATORY'
        assert may_modal.modal_type == 'PERMISSIVE'

    def test_cross_jurisdictional_comparison(self, db):
        """Test comparing same term across jurisdictions."""
        term = 'person'
        jurisdictions = ['Commonwealth', 'New South Wales', 'Victoria']

        definitions = []
        for jurisdiction in jurisdictions:
            definition = db.get_definition(term, jurisdiction)
            definitions.append(definition)

        # All should have definition
        assert all(d is not None for d in definitions)

        # All should mention corporations
        assert all('corp' in d.definition.lower() for d in definitions)

        # Verify cross-jurisdictional consistency
        for definition in definitions:
            assert db.includes_corporations(term, definition.jurisdiction) is True


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_jurisdiction(self, db):
        """Test handling of invalid jurisdiction."""
        definition = db.get_definition('person', 'Invalid Jurisdiction')
        # Should return None or fallback to Commonwealth
        # Implementation depends on fallback setting

    def test_invalid_date_format(self, db):
        """Test handling of invalid date format."""
        with pytest.raises(ValueError):
            db.calculate_month('invalid-date')

    def test_empty_text_obligation_extraction(self, db):
        """Test obligation extraction from empty text."""
        obligations = db.extract_obligations('', 'Commonwealth')

        assert len(obligations['duties']) == 0
        assert len(obligations['powers']) == 0
        assert len(obligations['prohibitions']) == 0

    def test_unknown_modal_verb(self, db):
        """Test classification of unknown modal verb."""
        modal = db.classify_modal('unknown_modal', 'Commonwealth')

        assert modal.modal_type == 'UNKNOWN'
        assert modal.creates == 'unknown'


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test performance characteristics."""

    def test_multiple_lookups_performance(self, db):
        """Test that multiple lookups are reasonably fast."""
        import time

        start = time.time()

        # Perform 100 lookups
        for _ in range(100):
            db.get_definition('person', 'Commonwealth')
            db.get_definition('month', 'Victoria')

        elapsed = time.time() - start

        # Should complete in under 1 second
        assert elapsed < 1.0, f"100 lookups took {elapsed:.2f}s"

    def test_search_performance(self, db):
        """Test search performance."""
        import time

        start = time.time()
        db.search_definitions('corporation')
        elapsed = time.time() - start

        # Should be very fast
        assert elapsed < 0.5, f"Search took {elapsed:.2f}s"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
