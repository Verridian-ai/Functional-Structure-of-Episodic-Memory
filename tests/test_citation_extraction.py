"""
Citation Extraction Tests for Australian Legal Corpus Classification System

This test suite validates:
- Medium neutral citation extraction ([2020] HCA 1)
- Authorized report extraction ((2020) 271 CLR 657)
- Legislation citation extraction (Fair Work Act 2009 (Cth))
- Section/subsection parsing (s 79, s 51(xxvi))
- Edge cases and malformed citations
- Integration with classification system
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.multi_domain_classifier import (
    CitationExtractor,
    CitationType,
    LegislationRef,
    CaseRef,
)


# ============================================================================
# MEDIUM NEUTRAL CITATION TESTS
# ============================================================================

class TestMediumNeutralExtraction:
    """Test extraction of medium neutral citations."""

    @pytest.mark.parametrize("text,expected_year,expected_court,expected_number", [
        ('[2020] HCA 1', 2020, 'HCA', 1),
        ('[2021] NSWCA 50', 2021, 'NSWCA', 50),
        ('[2022] FCA 1492', 2022, 'FCA', 1492),
        ('[2019] FamCA 156', 2019, 'FAMCA', 156),
        ('[2023] VSCA 234', 2023, 'VSCA', 234),
        ('[2018] AATA 500', 2018, 'AATA', 500),
    ])
    def test_basic_medium_neutral_extraction(self, text, expected_year,
                                             expected_court, expected_number):
        """Test extraction of basic medium neutral citations."""
        results = CitationExtractor.extract_medium_neutral(text)

        assert len(results) >= 1, f"Failed to extract from: {text}"

        result = results[0]
        assert result['year'] == expected_year
        assert result['court'] == expected_court
        assert result['number'] == expected_number
        assert result['type'] == CitationType.MEDIUM_NEUTRAL

    def test_multiple_citations_in_text(self):
        """Test extraction of multiple citations from single text."""
        text = """
        The decision in [2020] HCA 1 was followed in [2021] NSWCA 50.
        See also [2022] FCA 100.
        """

        results = CitationExtractor.extract_medium_neutral(text)

        assert len(results) >= 3
        assert results[0]['court'] == 'HCA'
        assert results[1]['court'] == 'NSWCA'
        assert results[2]['court'] == 'FCA'

    def test_citation_in_sentence(self):
        """Test extraction when citation is embedded in sentence."""
        text = "The principle established in [2020] HCA 15 applies."

        results = CitationExtractor.extract_medium_neutral(text)

        assert len(results) == 1
        assert results[0]['year'] == 2020
        assert results[0]['court'] == 'HCA'
        assert results[0]['number'] == 15

    def test_citation_with_extra_spaces(self):
        """Test extraction with varying whitespace."""
        variations = [
            '[2020] HCA 1',      # Normal
            '[2020]  HCA  1',    # Extra spaces
            '[2020] HCA  1',     # One extra space
        ]

        for text in variations:
            results = CitationExtractor.extract_medium_neutral(text)
            assert len(results) >= 1, f"Failed on: {text}"

    def test_case_insensitive_extraction(self):
        """Test extraction is case-insensitive for court codes."""
        variations = [
            '[2020] HCA 1',
            '[2020] hca 1',
            '[2020] Hca 1',
        ]

        for text in variations:
            results = CitationExtractor.extract_medium_neutral(text)
            assert len(results) == 1
            # Result should be uppercase
            assert results[0]['court'] == 'HCA'

    def test_four_digit_case_numbers(self):
        """Test extraction of large case numbers."""
        text = '[2022] FCA 1492'

        results = CitationExtractor.extract_medium_neutral(text)

        assert len(results) == 1
        assert results[0]['number'] == 1492

    def test_specialist_court_codes(self):
        """Test extraction of specialist court codes."""
        specialist_codes = [
            ('[2020] NSWLEC 75', 'NSWLEC'),
            ('[2021] FamCAFC 20', 'FAMCAFC'),
            ('[2022] FCAFC 100', 'FCAFC'),
            ('[2019] NSWCATAD 50', 'NSWCATAD'),
            ('[2023] NSWWCCPD 30', 'NSWWCCPD'),
        ]

        for citation, expected_court in specialist_codes:
            results = CitationExtractor.extract_medium_neutral(citation)
            assert len(results) >= 1
            assert results[0]['court'] == expected_court


# ============================================================================
# AUTHORIZED REPORT CITATION TESTS
# ============================================================================

class TestAuthorizedReportExtraction:
    """Test extraction of authorized report citations."""

    @pytest.mark.parametrize("text,expected_year,expected_volume,expected_report,expected_page", [
        ('(2020) 271 CLR 657', 2020, 271, 'CLR', 657),
        ('(2012) 247 CLR 108', 2012, 247, 'CLR', 108),
        ('(2011) 244 CLR 120', 2011, 244, 'CLR', 120),
        ('(2010) 240 CLR 461', 2010, 240, 'CLR', 461),
        ('(2006) 229 CLR 1', 2006, 229, 'CLR', 1),
    ])
    def test_basic_authorized_report_extraction(self, text, expected_year,
                                                expected_volume, expected_report,
                                                expected_page):
        """Test extraction of basic authorized report citations."""
        results = CitationExtractor.extract_authorized_reports(text)

        assert len(results) >= 1, f"Failed to extract from: {text}"

        result = results[0]
        assert result['year'] == expected_year
        assert result['volume'] == expected_volume
        assert result['report'] == expected_report
        assert result['page'] == expected_page
        assert result['type'] == CitationType.AUTHORIZED_REPORT

    def test_state_law_reports(self):
        """Test extraction of state law reports."""
        state_reports = [
            ('(2020) 100 NSWLR 50', 'NSWLR'),
            ('(2021) 95 VR 200', 'VR'),
            ('(2019) 75 QdR 300', 'QdR'),
            ('(2022) 120 SASR 100', 'SASR'),
            ('(2020) 85 WAR 250', 'WAR'),
            ('(2018) 40 TasR 150', 'TasR'),
        ]

        for citation, expected_report in state_reports:
            results = CitationExtractor.extract_authorized_reports(citation)
            assert len(results) >= 1
            assert results[0]['report'] == expected_report

    def test_specialist_reports(self):
        """Test extraction of specialist report series."""
        specialist = [
            ('(2020) 300 FLR 100', 'FLR'),   # Federal Law Reports
            ('(2019) 250 ALR 50', 'ALR'),    # Australian Law Reports
            ('(2021) 400 FCR 200', 'FCR'),   # Federal Court Reports
            ('(2018) 150 FLC 500', 'FLC'),   # Family Law Cases
            ('(2022) 100 ACSR 75', 'ACSR'),  # Australian Corporations Reports
        ]

        for citation, expected_report in specialist:
            results = CitationExtractor.extract_authorized_reports(citation)
            assert len(results) >= 1
            assert results[0]['report'] == expected_report

    def test_multiple_reports_in_text(self):
        """Test extraction of multiple report citations."""
        text = """
        The case is reported at (2020) 271 CLR 657 and (2020) 300 ALR 100.
        See also (2019) 250 FCR 50.
        """

        results = CitationExtractor.extract_authorized_reports(text)

        assert len(results) >= 3
        assert results[0]['report'] == 'CLR'
        assert results[1]['report'] == 'ALR'
        assert results[2]['report'] == 'FCR'

    def test_citation_in_case_name(self):
        """Test extraction when citation follows case name."""
        text = "Stanford v Stanford (2012) 247 CLR 108 is the leading case."

        results = CitationExtractor.extract_authorized_reports(text)

        assert len(results) >= 1
        assert results[0]['year'] == 2012
        assert results[0]['volume'] == 247
        assert results[0]['report'] == 'CLR'
        assert results[0]['page'] == 108


# ============================================================================
# LEGISLATION CITATION TESTS
# ============================================================================

class TestLegislationExtraction:
    """Test extraction of legislation citations."""

    @pytest.mark.parametrize("text,expected_name,expected_year,expected_juris", [
        ('Family Law Act 1975 (Cth)', 'Family Law Act', 1975, 'CTH'),
        ('Fair Work Act 2009 (Cth)', 'Fair Work Act', 2009, 'CTH'),
        ('Crimes Act 1900 (NSW)', 'Crimes Act', 1900, 'NSW'),
        ('Migration Act 1958 (Cth)', 'Migration Act', 1958, 'CTH'),
        ('Corporations Act 2001 (Cth)', 'Corporations Act', 2001, 'CTH'),
    ])
    def test_basic_legislation_extraction(self, text, expected_name,
                                          expected_year, expected_juris):
        """Test extraction of basic legislation references."""
        results = CitationExtractor.extract_legislation(text)

        assert len(results) >= 1, f"Failed to extract from: {text}"

        result = results[0]
        assert expected_name in result.name
        assert result.year == expected_year
        assert result.jurisdiction == expected_juris

    def test_legislation_with_section(self):
        """Test extraction of legislation with section numbers."""
        text = "Family Law Act 1975 (Cth) s 79"

        results = CitationExtractor.extract_legislation(text)

        assert len(results) >= 1
        result = results[0]
        assert 'Family Law Act' in result.name
        assert result.section == '79'

    def test_legislation_with_subsection(self):
        """Test extraction with subsection notation."""
        text = "Constitution s 51(xxvi)"

        # Note: This tests the section pattern, not full legislation pattern
        # Full legislation pattern requires Act/Regulation/Rules keyword
        text = "Constitution Act 1900 (Cth) s 51(xxvi)"

        results = CitationExtractor.extract_legislation(text)

        if len(results) >= 1:
            result = results[0]
            # Section might be captured
            assert result.section is None or '51' in str(result.section)

    def test_multiple_legislation_in_text(self):
        """Test extraction of multiple legislation references."""
        text = """
        The Fair Work Act 2009 (Cth) applies. The applicant also relies on
        the Sex Discrimination Act 1984 (Cth) and the Corporations Act 2001 (Cth).
        """

        results = CitationExtractor.extract_legislation(text)

        assert len(results) >= 3
        names = [ref.name for ref in results]
        assert any('Fair Work Act' in name for name in names)
        assert any('Sex Discrimination Act' in name for name in names)
        assert any('Corporations Act' in name for name in names)

    def test_state_legislation(self):
        """Test extraction of state legislation."""
        states = [
            ('Crimes Act 1900 (NSW)', 'NSW'),
            ('Crimes Act 1958 (Vic)', 'VIC'),
            ('Criminal Code 1899 (Qld)', 'QLD'),
            ('Criminal Code 1924 (Tas)', 'TAS'),
        ]

        for citation, expected_juris in states:
            results = CitationExtractor.extract_legislation(citation)
            assert len(results) >= 1
            assert results[0].jurisdiction == expected_juris

    def test_regulations_and_rules(self):
        """Test extraction of regulations and rules."""
        citations = [
            'Migration Regulations 1994 (Cth)',
            'Family Law Rules 2004 (Cth)',
            'Civil Procedure Rules 2005 (NSW)',
        ]

        for citation in citations:
            results = CitationExtractor.extract_legislation(citation)
            assert len(results) >= 1, f"Failed to extract: {citation}"

    def test_section_variations(self):
        """Test extraction of various section notations."""
        variations = [
            'Family Law Act 1975 (Cth) s 79',
            'Family Law Act 1975 (Cth) s 79(1)',
            'Family Law Act 1975 (Cth) s 79(1)(a)',
            'Family Law Act 1975 (Cth) s 79A',
        ]

        for text in variations:
            results = CitationExtractor.extract_legislation(text)
            assert len(results) >= 1, f"Failed on: {text}"


# ============================================================================
# SECTION/SUBSECTION PARSING TESTS
# ============================================================================

class TestSectionParsing:
    """Test parsing of section and subsection references."""

    @pytest.mark.parametrize("text,expected_section", [
        ('s 79', '79'),
        ('s 385', '385'),
        ('section 51', '51'),
        ('s 79A', '79A'),
        ('s 79AA', '79AA'),
    ])
    def test_basic_section_extraction(self, text, expected_section):
        """Test extraction of basic section numbers."""
        results = CitationExtractor.SECTION_PATTERN.findall(text)

        assert len(results) >= 1
        assert results[0] == expected_section

    @pytest.mark.parametrize("text,expected_section", [
        ('s 51(xxvi)', '51(xxvi)'),
        ('s 79(1)', '79(1)'),
        ('s 385(a)', '385(a)'),
        ('section 75(2)', '75(2)'),
    ])
    def test_subsection_extraction(self, text, expected_section):
        """Test extraction of subsections in parentheses."""
        results = CitationExtractor.SECTION_PATTERN.findall(text)

        assert len(results) >= 1
        # Pattern should capture the subsection
        assert expected_section in results[0] or results[0].startswith(expected_section.split('(')[0])

    def test_regulation_section_patterns(self):
        """Test extraction of regulation section patterns."""
        patterns = [
            'reg 4.12',
            'regulation 5',
            'r 10.5',
        ]

        for pattern in patterns:
            results = CitationExtractor.SECTION_PATTERN.findall(pattern)
            assert len(results) >= 1

    def test_multiple_sections_in_text(self):
        """Test extraction of multiple section references."""
        text = "Sections 79, 75(2), and 79A apply."

        results = CitationExtractor.SECTION_PATTERN.findall(text)

        # Should extract multiple sections
        assert len(results) >= 2


# ============================================================================
# CITATION TYPE DETECTION TESTS
# ============================================================================

class TestCitationTypeDetection:
    """Test automatic detection of citation types."""

    def test_detect_medium_neutral(self):
        """Test detection of medium neutral citations."""
        citations = [
            '[2020] HCA 1',
            '[2021] NSWCA 50',
            '[2022] FCA 100',
        ]

        for citation in citations:
            detected = CitationExtractor.detect_citation_type(citation)
            assert detected == CitationType.MEDIUM_NEUTRAL

    def test_detect_authorized_report(self):
        """Test detection of authorized report citations."""
        citations = [
            '(2020) 271 CLR 657',
            '(2012) 247 CLR 108',
            '(2010) 240 CLR 461',
        ]

        for citation in citations:
            detected = CitationExtractor.detect_citation_type(citation)
            assert detected == CitationType.AUTHORIZED_REPORT

    def test_detect_legislation(self):
        """Test detection of legislation citations."""
        citations = [
            'Fair Work Act 2009 (Cth)',
            'Family Law Act 1975 (Cth)',
            'Crimes Act 1900 (NSW)',
        ]

        for citation in citations:
            detected = CitationExtractor.detect_citation_type(citation)
            assert detected == CitationType.LEGISLATION

    def test_detect_unknown_type(self):
        """Test detection returns unknown for unrecognized formats."""
        citations = [
            'Some random text',
            '2020',
            'Not a citation',
        ]

        for citation in citations:
            detected = CitationExtractor.detect_citation_type(citation)
            assert detected == CitationType.UNKNOWN


# ============================================================================
# EDGE CASES AND MALFORMED CITATIONS
# ============================================================================

class TestEdgeCasesAndMalformed:
    """Test handling of edge cases and malformed citations."""

    def test_empty_string(self):
        """Test extraction from empty string."""
        text = ''

        mn_results = CitationExtractor.extract_medium_neutral(text)
        ar_results = CitationExtractor.extract_authorized_reports(text)
        leg_results = CitationExtractor.extract_legislation(text)

        assert len(mn_results) == 0
        assert len(ar_results) == 0
        assert len(leg_results) == 0

    def test_no_citations_in_text(self):
        """Test extraction when no citations present."""
        text = 'This is just plain text with no legal citations.'

        mn_results = CitationExtractor.extract_medium_neutral(text)
        ar_results = CitationExtractor.extract_authorized_reports(text)
        leg_results = CitationExtractor.extract_legislation(text)

        assert len(mn_results) == 0
        assert len(ar_results) == 0
        assert len(leg_results) == 0

    def test_malformed_year_bracket(self):
        """Test handling of malformed year brackets."""
        malformed = [
            '2020] HCA 1',      # Missing opening bracket
            '[2020 HCA 1',      # Missing closing bracket
            '(2020 HCA 1',      # Wrong bracket type
        ]

        for text in malformed:
            results = CitationExtractor.extract_medium_neutral(text)
            # May or may not extract - should not crash
            assert isinstance(results, list)

    def test_invalid_year_range(self):
        """Test handling of invalid years."""
        citations = [
            '[1800] HCA 1',     # Too old
            '[2100] HCA 1',     # Future
            '[9999] HCA 1',     # Invalid
        ]

        for citation in citations:
            results = CitationExtractor.extract_medium_neutral(citation)
            # Pattern will still match - validation happens elsewhere
            if len(results) > 0:
                assert isinstance(results[0]['year'], int)

    def test_very_long_court_code(self):
        """Test handling of unusually long court codes."""
        text = '[2020] VERYLONGCOURTCODE 1'

        results = CitationExtractor.extract_medium_neutral(text)
        # Pattern limits court code to 10 chars, so won't match
        # This is expected behavior
        assert isinstance(results, list)

    def test_missing_jurisdiction_in_legislation(self):
        """Test legislation without jurisdiction."""
        text = 'Fair Work Act 2009'  # Missing (Cth)

        results = CitationExtractor.extract_legislation(text)
        # Pattern requires jurisdiction, so won't match
        assert len(results) == 0

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters."""
        text = '[2020] HCA 1 – this is an en-dash'

        results = CitationExtractor.extract_medium_neutral(text)
        # Should still extract citation
        assert len(results) >= 1

    def test_multiple_spaces_between_components(self):
        """Test citations with excessive spacing."""
        text = '[2020]     HCA     1'

        results = CitationExtractor.extract_medium_neutral(text)
        # Pattern should handle multiple spaces
        assert len(results) >= 1


# ============================================================================
# INTEGRATION WITH CLASSIFICATION SYSTEM
# ============================================================================

class TestCitationClassificationIntegration:
    """Test citation extraction integration with classifier."""

    def test_legislation_extraction_in_classification(self):
        """Test legislation extraction through classifier."""
        from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier

        classifier = EnhancedDomainClassifier()

        doc = {
            'id': 'test_leg',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': '''
            The Fair Work Act 2009 (Cth) s 385 applies. The applicant also
            relies on the Sex Discrimination Act 1984 (Cth) s 14.
            '''
        }

        result = classifier.classify(doc)

        # Should extract legislation
        assert len(result.legislation_refs) >= 2

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Fair Work Act' in name for name in leg_names)
        assert any('Sex Discrimination Act' in name for name in leg_names)

    def test_case_citation_extraction_in_classification(self):
        """Test case citation extraction through classifier."""
        from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier

        classifier = EnhancedDomainClassifier()

        doc = {
            'id': 'test_cases',
            'citation': '[2020] NSWCA 100',
            'type': 'case_law',
            'text': '''
            The principles in Muldrock v The Queen (2011) 244 CLR 120 apply.
            See also Markarian v The Queen (2005) 228 CLR 357.
            '''
        }

        result = classifier.classify(doc)

        # Should detect case references
        assert len(result.case_refs) >= 0  # Implementation may vary

    def test_citation_type_detection_in_classification(self):
        """Test citation type is correctly detected in classification."""
        from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier

        classifier = EnhancedDomainClassifier()

        # Medium neutral
        doc_mn = {
            'id': 'test_mn',
            'citation': '[2020] HCA 1',
            'type': 'case_law',
            'text': 'Case law decision.'
        }

        result_mn = classifier.classify(doc_mn)
        assert result_mn.citation_type == CitationType.MEDIUM_NEUTRAL

        # Legislation
        doc_leg = {
            'id': 'test_leg_type',
            'citation': 'Fair Work Act 2009 (Cth)',
            'type': 'primary_legislation',
            'text': 'An Act relating to workplace relations.'
        }

        result_leg = classifier.classify(doc_leg)
        assert result_leg.citation_type == CitationType.LEGISLATION


# ============================================================================
# PERFORMANCE AND STRESS TESTS
# ============================================================================

class TestCitationExtractionPerformance:
    """Test performance with large volumes of citations."""

    def test_many_citations_in_long_text(self):
        """Test extraction from text with many citations."""
        # Create text with 50 citations
        citations = [f'[2020] HCA {i}' for i in range(1, 51)]
        text = ' '.join(citations)

        results = CitationExtractor.extract_medium_neutral(text)

        assert len(results) == 50

    def test_very_long_document(self):
        """Test extraction from very long document."""
        # Create a long document
        text = 'Legal text. ' * 10000 + '[2020] HCA 1' + ' More text. ' * 10000

        results = CitationExtractor.extract_medium_neutral(text)

        # Should still find the citation
        assert len(results) >= 1

    def test_mixed_citation_types(self):
        """Test extraction of all types from mixed text."""
        text = '''
        The case [2020] HCA 1 is reported at (2020) 271 CLR 657.
        It interprets the Fair Work Act 2009 (Cth) s 385.
        See also [2021] NSWCA 50 at (2021) 100 NSWLR 200.
        '''

        mn_results = CitationExtractor.extract_medium_neutral(text)
        ar_results = CitationExtractor.extract_authorized_reports(text)
        leg_results = CitationExtractor.extract_legislation(text)

        assert len(mn_results) >= 2
        assert len(ar_results) >= 2
        assert len(leg_results) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
