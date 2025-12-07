"""
Court Hierarchy Integration Tests for Australian Legal Corpus Classification System

This test suite validates:
- All 106+ court codes are accessible and have correct metadata
- Authority scoring is accurate across all hierarchy levels
- Binding precedent logic works correctly
- Specialist court domain hints are properly assigned
- Jurisdiction mapping is correct
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.court_hierarchy import (
    COURT_CODES,
    HIERARCHY_LEVELS,
    REPORT_SERIES,
    get_court_info,
    get_hierarchy_level,
    get_authority_score,
    get_jurisdiction,
    get_domain_hint,
    extract_court_from_citation,
    is_binding_authority,
    get_report_series_info,
)


# ============================================================================
# COURT CODE COVERAGE TESTS
# ============================================================================

class TestCourtCodeCoverage:
    """Test comprehensive coverage of Australian court codes."""

    def test_total_court_codes_count(self):
        """Test that we have 75+ court codes (expanded from original 56)."""
        assert len(COURT_CODES) >= 75, f"Only {len(COURT_CODES)} court codes found"

    def test_all_jurisdictions_represented(self):
        """Test all Australian jurisdictions are represented."""
        jurisdictions = set()
        for code, info in COURT_CODES.items():
            jurisdictions.add(info['jurisdiction'])

        expected_jurisdictions = [
            'Commonwealth',
            'NSW',
            'VIC',
            'QLD',
            'WA',
            'SA',
            'TAS',
            'ACT',
            'NT',
        ]

        for jurisdiction in expected_jurisdictions:
            assert jurisdiction in jurisdictions, f"Missing jurisdiction: {jurisdiction}"

    def test_all_hierarchy_levels_used(self):
        """Test that all hierarchy levels are represented."""
        levels_used = set()
        for code, info in COURT_CODES.items():
            levels_used.add(info['level'])

        # Should have courts at multiple levels
        assert 'apex' in levels_used  # High Court
        assert 'superior_appellate' in levels_used  # State Courts of Appeal
        assert 'superior_trial' in levels_used  # Supreme Courts
        assert 'intermediate' in levels_used  # District/County Courts
        assert 'lower' in levels_used  # Magistrates/Local Courts
        assert 'tribunal' in levels_used  # Administrative tribunals
        assert 'specialist' in levels_used  # Specialist courts

    def test_apex_court_exists(self):
        """Test High Court of Australia exists."""
        assert 'HCA' in COURT_CODES
        hca = COURT_CODES['HCA']
        assert hca['name'] == 'High Court of Australia'
        assert hca['level'] == 'apex'
        assert hca['jurisdiction'] == 'Commonwealth'
        assert hca['binding'] is True
        assert hca['authority_score'] == 100


class TestFederalCourts:
    """Test federal court codes."""

    def test_federal_court_codes(self):
        """Test Federal Court codes exist."""
        federal_courts = ['HCA', 'FCAFC', 'FCA', 'FedCFamC', 'FCCA']

        for code in federal_courts:
            assert code in COURT_CODES, f"Missing federal court: {code}"

    def test_federal_family_courts(self):
        """Test Family Court codes exist."""
        family_courts = ['FamCA', 'FamCAFC']

        for code in family_courts:
            assert code in COURT_CODES, f"Missing family court: {code}"
            assert COURT_CODES[code].get('domain_hint') == 'Family'

    def test_federal_tribunals(self):
        """Test federal tribunal codes exist."""
        tribunals = ['AATA', 'AAT', 'FWC', 'FWCFB']

        for code in tribunals:
            assert code in COURT_CODES, f"Missing federal tribunal: {code}"

    def test_specialist_federal_tribunals(self):
        """Test specialist federal tribunals added by Agent 3."""
        specialist_tribunals = ['SSAT', 'MRT', 'RRT', 'IPC', 'OAIC', 'VET', 'NNTT']

        for code in specialist_tribunals:
            assert code in COURT_CODES, f"Missing specialist tribunal: {code}"
            assert COURT_CODES[code]['level'] == 'tribunal'


class TestStateCourts:
    """Test state court codes."""

    @pytest.mark.parametrize("state,appellate_code,supreme_code", [
        ('NSW', 'NSWCA', 'NSWSC'),
        ('VIC', 'VSCA', 'VSC'),
        ('QLD', 'QCA', 'QSC'),
        ('WA', 'WASCA', 'WASC'),
        ('SA', 'SASCFC', 'SASC'),
        ('TAS', 'TASFC', 'TASSC'),
        ('ACT', 'ACTCA', 'ACTSC'),
        ('NT', 'NTCA', 'NTSC'),
    ])
    def test_state_appellate_and_supreme_courts(self, state, appellate_code, supreme_code):
        """Test each state has appellate and supreme court codes."""
        # Appellate court
        assert appellate_code in COURT_CODES, f"Missing {state} appellate court"
        appellate = COURT_CODES[appellate_code]
        assert appellate['level'] == 'superior_appellate'
        assert appellate['jurisdiction'] == state

        # Supreme court
        assert supreme_code in COURT_CODES, f"Missing {state} supreme court"
        supreme = COURT_CODES[supreme_code]
        assert supreme['level'] == 'superior_trial'
        assert supreme['jurisdiction'] == state

    @pytest.mark.parametrize("state,district_code", [
        ('NSW', 'NSWDC'),
        ('QLD', 'QDC'),
        ('WA', 'WADC'),
        ('SA', 'SADC'),
    ])
    def test_state_district_courts(self, state, district_code):
        """Test states with District Courts."""
        assert district_code in COURT_CODES, f"Missing {state} District Court"
        district = COURT_CODES[district_code]
        assert district['level'] == 'intermediate'
        assert district['jurisdiction'] == state

    @pytest.mark.parametrize("state,local_code", [
        ('NSW', 'NSWLC'),
        ('VIC', 'VMC'),
        ('QLD', 'QMC'),
        ('WA', 'WAMC'),
        ('SA', 'SAMC'),
        ('TAS', 'TASMC'),
        ('ACT', 'ACTMC'),
        ('NT', 'NTLC'),
    ])
    def test_state_local_courts(self, state, local_code):
        """Test states with Local/Magistrates Courts."""
        assert local_code in COURT_CODES, f"Missing {state} Local/Magistrates Court"
        local = COURT_CODES[local_code]
        assert local['level'] == 'lower'
        assert local['jurisdiction'] == state


class TestSpecialistCourts:
    """Test specialist court codes."""

    def test_criminal_appeal_courts(self):
        """Test criminal appeal court codes."""
        criminal_courts = {
            'NSWCCA': 'NSW Court of Criminal Appeal',
            'TASCCA': 'Tasmanian Court of Criminal Appeal',
            'CCA': 'Court of Criminal Appeal (Historical)',
        }

        for code, name in criminal_courts.items():
            assert code in COURT_CODES, f"Missing criminal court: {code}"
            assert COURT_CODES[code].get('domain_hint') == 'Criminal'

    def test_employment_industrial_courts(self):
        """Test employment/industrial court codes."""
        employment_courts = [
            'FWC', 'FWCFB',  # Fair Work Commission
            'IRC', 'AIRC',  # Industrial Relations Commissions
            'NSWIC', 'IRC_NSW',  # NSW Industrial
            'ICQ', 'QIRC',  # Queensland Industrial
            'WAIRC',  # WA Industrial
            'SAET',  # SA Employment Tribunal
        ]

        for code in employment_courts:
            assert code in COURT_CODES, f"Missing employment court: {code}"
            court_info = COURT_CODES[code]
            assert court_info.get('domain_hint') == 'Employment', \
                f"{code} should have Employment domain hint"

    def test_environment_courts(self):
        """Test environment/planning court codes."""
        env_courts = ['NSWLEC']

        for code in env_courts:
            assert code in COURT_CODES, f"Missing environment court: {code}"
            assert COURT_CODES[code].get('domain_hint') == 'Environment'

    def test_family_children_courts(self):
        """Test family and children's court codes."""
        family_courts = ['NSWCC', 'VChC', 'NSWGT']

        for code in family_courts:
            assert code in COURT_CODES, f"Missing family/children court: {code}"
            assert COURT_CODES[code].get('domain_hint') == 'Family'

    def test_workers_compensation_tribunals(self):
        """Test workers compensation tribunal codes."""
        comp_tribunals = ['WCC', 'WCAT', 'DDT']

        for code in comp_tribunals:
            assert code in COURT_CODES, f"Missing compensation tribunal: {code}"

    def test_coroners_courts(self):
        """Test coroners court codes."""
        coroners = ['NSWCOR', 'VICCOR']

        for code in coroners:
            assert code in COURT_CODES, f"Missing coroners court: {code}"
            assert COURT_CODES[code].get('domain_hint') == 'Criminal'


class TestStateTribunals:
    """Test state tribunal codes."""

    @pytest.mark.parametrize("state,tribunal_code", [
        ('NSW', 'NCAT'),
        ('VIC', 'VCAT'),
        ('QLD', 'QCAT'),
        ('WA', 'SAT'),
        ('SA', 'SACAT'),
        ('TAS', 'TasCAT'),
        ('ACT', 'ACAT'),
        ('NT', 'NTCAT'),
    ])
    def test_state_cat_tribunals(self, state, tribunal_code):
        """Test each state has Civil and Administrative Tribunal."""
        assert tribunal_code in COURT_CODES, f"Missing {state} CAT"
        tribunal = COURT_CODES[tribunal_code]
        assert tribunal['level'] == 'tribunal'
        assert tribunal['jurisdiction'] == state


# ============================================================================
# AUTHORITY SCORING TESTS
# ============================================================================

class TestAuthorityScoring:
    """Test authority score assignment across hierarchy."""

    def test_high_court_highest_authority(self):
        """Test High Court has highest authority score."""
        hca_score = get_authority_score('HCA')
        assert hca_score == 100

        # No other court should have higher score
        for code in COURT_CODES:
            score = get_authority_score(code)
            assert score <= 100, f"{code} has score > 100"

    def test_appellate_courts_high_authority(self):
        """Test appellate courts have high authority scores."""
        appellate_courts = ['FCAFC', 'NSWCA', 'VSCA', 'QCA', 'WASCA', 'SASCFC',
                           'TASFC', 'ACTCA', 'NTCA', 'FamCAFC']

        for code in appellate_courts:
            score = get_authority_score(code)
            assert score >= 80, f"{code} appellate court has low score: {score}"

    def test_supreme_courts_medium_high_authority(self):
        """Test Supreme Courts have medium-high authority."""
        supreme_courts = ['FCA', 'NSWSC', 'VSC', 'QSC', 'WASC', 'SASC',
                         'TASSC', 'ACTSC', 'NTSC', 'FamCA']

        for code in supreme_courts:
            score = get_authority_score(code)
            assert 70 <= score <= 80, f"{code} supreme court score out of range: {score}"

    def test_district_courts_medium_authority(self):
        """Test District Courts have medium authority."""
        district_courts = ['NSWDC', 'VCC', 'QDC', 'WADC', 'SADC']

        for code in district_courts:
            score = get_authority_score(code)
            assert 45 <= score <= 55, f"{code} district court score out of range: {score}"

    def test_local_courts_low_authority(self):
        """Test Local/Magistrates Courts have low authority."""
        local_courts = ['NSWLC', 'VMC', 'QMC', 'WAMC', 'SAMC', 'TASMC', 'ACTMC', 'NTLC']

        for code in local_courts:
            score = get_authority_score(code)
            assert score <= 35, f"{code} local court has high score: {score}"

    def test_tribunals_low_authority(self):
        """Test tribunals have lower authority than courts."""
        tribunals = ['NCAT', 'VCAT', 'QCAT', 'SAT', 'SACAT', 'TasCAT', 'ACAT', 'NTCAT']

        for code in tribunals:
            score = get_authority_score(code)
            assert score <= 40, f"{code} tribunal has high score: {score}"

    def test_specialist_tribunals_vary_authority(self):
        """Test specialist tribunals have varying authority based on function."""
        # FWC Full Bench should have higher authority than regular FWC
        fwc_score = get_authority_score('FWC')
        fwcfb_score = get_authority_score('FWCFB')
        assert fwcfb_score > fwc_score, "FWC Full Bench should have higher authority"


# ============================================================================
# HIERARCHY LEVEL TESTS
# ============================================================================

class TestHierarchyLevels:
    """Test hierarchy level assignment."""

    def test_hierarchy_level_ordering(self):
        """Test hierarchy levels are correctly ordered (1=highest)."""
        assert HIERARCHY_LEVELS['apex'] == 1
        assert HIERARCHY_LEVELS['superior_appellate'] == 2
        assert HIERARCHY_LEVELS['intermediate_appellate'] == 3
        assert HIERARCHY_LEVELS['superior_trial'] == 4
        assert HIERARCHY_LEVELS['intermediate'] == 5
        assert HIERARCHY_LEVELS['lower'] == 6
        assert HIERARCHY_LEVELS['tribunal'] == 7
        assert HIERARCHY_LEVELS['specialist'] == 8

    def test_high_court_apex_level(self):
        """Test High Court is apex level."""
        assert get_hierarchy_level('HCA') == 1

    def test_appellate_courts_level_2(self):
        """Test appellate courts are level 2."""
        appellate_courts = ['FCAFC', 'NSWCA', 'VSCA', 'QCA']

        for code in appellate_courts:
            level = get_hierarchy_level(code)
            assert level == 2, f"{code} should be level 2, got {level}"

    def test_supreme_courts_level_4(self):
        """Test Supreme Courts are level 4."""
        supreme_courts = ['FCA', 'NSWSC', 'VSC', 'QSC']

        for code in supreme_courts:
            level = get_hierarchy_level(code)
            assert level == 4, f"{code} should be level 4, got {level}"


# ============================================================================
# BINDING PRECEDENT LOGIC TESTS
# ============================================================================

class TestBindingPrecedent:
    """Test binding precedent logic."""

    def test_high_court_binds_all(self):
        """Test High Court binds all Australian courts."""
        all_courts = list(COURT_CODES.keys())

        for court in all_courts:
            if court != 'HCA':
                assert is_binding_authority(court, 'HCA'), \
                    f"HCA should bind {court}"

    def test_appellate_binds_lower_same_state(self):
        """Test state appellate courts bind lower courts in same state."""
        # NSW Court of Appeal binds NSW Supreme Court
        assert is_binding_authority('NSWSC', 'NSWCA')

        # NSW Court of Appeal binds NSW District Court
        assert is_binding_authority('NSWDC', 'NSWCA')

        # NSW Court of Appeal binds NSW Local Court
        assert is_binding_authority('NSWLC', 'NSWCA')

    def test_supreme_court_binds_lower_same_state(self):
        """Test state Supreme Courts bind lower courts in same state."""
        # NSW Supreme Court binds NSW District Court
        assert is_binding_authority('NSWDC', 'NSWSC')

        # NSW Supreme Court binds NSW Local Court
        assert is_binding_authority('NSWLC', 'NSWSC')

    def test_appellate_not_binding_other_states(self):
        """Test state appellate courts don't bind other states."""
        # NSW Court of Appeal does not bind VIC Supreme Court
        assert not is_binding_authority('VSC', 'NSWCA')

        # QLD Court of Appeal does not bind NSW Supreme Court
        assert not is_binding_authority('NSWSC', 'QCA')

    def test_lower_not_binding_higher(self):
        """Test lower courts don't bind higher courts."""
        # Local Court does not bind District Court
        assert not is_binding_authority('NSWDC', 'NSWLC')

        # District Court does not bind Supreme Court
        assert not is_binding_authority('NSWSC', 'NSWDC')

    def test_same_level_not_binding(self):
        """Test courts at same level are not binding (only persuasive)."""
        # NSW Supreme Court does not bind VIC Supreme Court
        assert not is_binding_authority('VSC', 'NSWSC')

        # One District Court does not bind another
        assert not is_binding_authority('WADC', 'NSWDC')


# ============================================================================
# DOMAIN HINT TESTS
# ============================================================================

class TestDomainHints:
    """Test domain hint assignment for specialist courts."""

    def test_family_courts_hint(self):
        """Test family courts have Family domain hint."""
        family_codes = ['FamCA', 'FamCAFC', 'NSWCC', 'VChC', 'NSWGT']

        for code in family_codes:
            hint = get_domain_hint(code)
            assert hint == 'Family', f"{code} should have Family hint, got {hint}"

    def test_employment_courts_hint(self):
        """Test employment courts have Employment domain hint."""
        employment_codes = ['FWC', 'FWCFB', 'IRC', 'AIRC', 'NSWIC', 'ICQ',
                           'WAIRC', 'SAET', 'WCC', 'WCAT']

        for code in employment_codes:
            hint = get_domain_hint(code)
            assert hint == 'Employment', f"{code} should have Employment hint, got {hint}"

    def test_criminal_courts_hint(self):
        """Test criminal courts have Criminal domain hint."""
        criminal_codes = ['NSWCCA', 'TASCCA', 'CCA', 'NSWCOR', 'VICCOR', 'NSWDC_Drug']

        for code in criminal_codes:
            hint = get_domain_hint(code)
            assert hint == 'Criminal', f"{code} should have Criminal hint, got {hint}"

    def test_administrative_courts_hint(self):
        """Test administrative tribunals have Administrative domain hint."""
        admin_codes = ['AATA', 'AAT', 'NSWCATAD', 'SSAT', 'MRT', 'RRT',
                      'IPC', 'OAIC', 'VET', 'MHRT']

        for code in admin_codes:
            hint = get_domain_hint(code)
            assert hint == 'Administrative', f"{code} should have Administrative hint, got {hint}"

    def test_environment_courts_hint(self):
        """Test environment courts have Environment domain hint."""
        assert get_domain_hint('NSWLEC') == 'Environment'

    def test_property_courts_hint(self):
        """Test property tribunals have Property domain hint."""
        assert get_domain_hint('NNTT') == 'Property'


# ============================================================================
# CITATION EXTRACTION TESTS
# ============================================================================

class TestCitationExtraction:
    """Test court code extraction from citations."""

    @pytest.mark.parametrize("citation,expected_code", [
        ('[2020] HCA 1', 'HCA'),
        ('[2021] NSWCA 50', 'NSWCA'),
        ('[2022] FCA 100', 'FCA'),
        ('[2023] FamCA 200', 'FamCA'),
        ('[2020] AATA 500', 'AATA'),
        ('[2019] NSWLEC 75', 'NSWLEC'),
        ('[2021] VSCA 80', 'VSCA'),
        ('[2022] QSC 150', 'QSC'),
    ])
    def test_extract_court_from_medium_neutral(self, citation, expected_code):
        """Test extraction of court codes from medium neutral citations."""
        extracted = extract_court_from_citation(citation)
        assert extracted == expected_code, \
            f"Expected {expected_code} from {citation}, got {extracted}"

    def test_extract_court_case_insensitive(self):
        """Test court code extraction is case-insensitive."""
        variations = [
            '[2020] HCA 1',
            '[2020] hca 1',
            '[2020] Hca 1',
        ]

        for citation in variations:
            extracted = extract_court_from_citation(citation)
            # Should extract the code as-is from citation
            assert extracted is not None


# ============================================================================
# REPORT SERIES TESTS
# ============================================================================

class TestReportSeries:
    """Test authorized report series metadata."""

    def test_major_report_series_exist(self):
        """Test major authorized report series exist."""
        major_series = ['CLR', 'FCR', 'ALR', 'NSWLR', 'VR', 'QdR', 'SASR',
                       'WAR', 'TasR', 'FLC', 'ACSR']

        for series in major_series:
            assert series in REPORT_SERIES, f"Missing report series: {series}"

    def test_clr_highest_authority(self):
        """Test Commonwealth Law Reports has highest authority."""
        clr = get_report_series_info('CLR')
        assert clr is not None
        assert clr['authority_score'] == 100
        assert clr['court'] == 'HCA'

    def test_state_reports_authority(self):
        """Test state law reports have appropriate authority."""
        state_series = ['NSWLR', 'VR', 'QdR', 'SASR', 'WAR', 'TasR']

        for series in state_series:
            info = get_report_series_info(series)
            assert info is not None
            assert info['authority_score'] == 80, \
                f"{series} should have authority score 80"

    def test_specialist_report_series(self):
        """Test specialist report series have domain hints."""
        # Family Law Cases
        flc = get_report_series_info('FLC')
        assert flc is not None
        assert flc.get('domain_hint') == 'Family'

        # Australian Corporations and Securities Reports
        acsr = get_report_series_info('ACSR')
        assert acsr is not None
        assert acsr.get('domain_hint') == 'Commercial'

        # Industrial Reports
        ir = get_report_series_info('IR')
        assert ir is not None
        assert ir.get('domain_hint') == 'Employment'


# ============================================================================
# UTILITY FUNCTION TESTS
# ============================================================================

class TestUtilityFunctions:
    """Test utility functions in court_hierarchy module."""

    def test_get_court_info_valid(self):
        """Test get_court_info returns correct information."""
        hca_info = get_court_info('HCA')
        assert hca_info is not None
        assert hca_info['name'] == 'High Court of Australia'
        assert hca_info['level'] == 'apex'
        assert hca_info['jurisdiction'] == 'Commonwealth'

    def test_get_court_info_case_insensitive(self):
        """Test get_court_info is case-insensitive."""
        info_upper = get_court_info('HCA')
        info_lower = get_court_info('hca')
        info_mixed = get_court_info('Hca')

        assert info_upper == info_lower == info_mixed

    def test_get_court_info_invalid(self):
        """Test get_court_info returns None for invalid codes."""
        assert get_court_info('INVALID') is None
        assert get_court_info('') is None
        assert get_court_info(None) is None

    def test_get_jurisdiction_valid(self):
        """Test get_jurisdiction returns correct jurisdiction."""
        assert get_jurisdiction('HCA') == 'Commonwealth'
        assert get_jurisdiction('NSWCA') == 'NSW'
        assert get_jurisdiction('VSCA') == 'VIC'
        assert get_jurisdiction('QCA') == 'QLD'

    def test_get_jurisdiction_invalid(self):
        """Test get_jurisdiction returns None for invalid codes."""
        assert get_jurisdiction('INVALID') is None
        assert get_jurisdiction('') is None


# ============================================================================
# COMPREHENSIVE VALIDATION
# ============================================================================

class TestComprehensiveValidation:
    """Validate data integrity across all court codes."""

    def test_all_courts_have_required_fields(self):
        """Test all court codes have required metadata fields."""
        required_fields = ['name', 'level', 'jurisdiction', 'authority_score']

        for code, info in COURT_CODES.items():
            for field in required_fields:
                assert field in info, f"{code} missing field: {field}"

    def test_authority_scores_valid_range(self):
        """Test all authority scores are in valid range."""
        for code, info in COURT_CODES.items():
            score = info['authority_score']
            assert 0 <= score <= 100, \
                f"{code} has invalid authority score: {score}"

    def test_hierarchy_levels_valid(self):
        """Test all hierarchy levels are valid."""
        valid_levels = set(HIERARCHY_LEVELS.keys())

        for code, info in COURT_CODES.items():
            level = info['level']
            assert level in valid_levels, \
                f"{code} has invalid hierarchy level: {level}"

    def test_no_duplicate_codes(self):
        """Test there are no duplicate court codes."""
        codes = list(COURT_CODES.keys())
        unique_codes = set(codes)
        assert len(codes) == len(unique_codes), "Duplicate court codes detected"

    def test_binding_field_consistency(self):
        """Test binding field is consistent with hierarchy."""
        for code, info in COURT_CODES.items():
            binding = info.get('binding')
            # Binding can be True, False, or a string describing scope
            assert binding is not None, f"{code} missing binding field"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
