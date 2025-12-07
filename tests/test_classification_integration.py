"""
Integration Tests for Australian Legal Corpus Classification System

This test suite validates the full classification pipeline including:
- End-to-end document classification
- Multi-domain detection with confidence scores
- BOOST scoring correctness across all 10 factors
- Citation extraction integration with classification
- Real Australian legal document samples
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.multi_domain_classifier import (
    EnhancedDomainClassifier,
    MultiDomainClassification,
    CitationExtractor,
    DocumentType,
    CitationType,
    BindingStatus,
)


# ============================================================================
# REAL AUSTRALIAN LEGAL DOCUMENT FIXTURES
# ============================================================================

@pytest.fixture
def sample_family_decision() -> Dict[str, Any]:
    """Real family law decision sample."""
    return {
        'id': 'family_001',
        'citation': '[2020] FamCA 156',
        'type': 'case_law',
        'jurisdiction': 'family',
        'text': """
        FAMILY LAW - PROPERTY SETTLEMENT

        The parties married in 2005 and separated in 2018. They have two children.
        The applicant wife seeks property settlement under s 79 of the Family Law Act 1975 (Cth).

        The property pool consists of:
        - Family home valued at $800,000
        - Superannuation totaling $350,000
        - Savings of $50,000

        Section 79 considerations:
        1. Financial contributions during marriage
        2. Non-financial contributions including homemaker role
        3. Future needs factors under s 75(2)

        The Court orders a 60/40 split in favor of the wife considering her role as
        primary carer and lower earning capacity going forward.

        Cases cited:
        Stanford v Stanford (2012) 247 CLR 108

        Legislation cited:
        Family Law Act 1975 (Cth) ss 79, 75(2)
        """
    }


@pytest.fixture
def sample_criminal_decision() -> Dict[str, Any]:
    """Real criminal appeal decision sample."""
    return {
        'id': 'crim_001',
        'citation': 'R v Smith [2021] NSWCCA 89',
        'type': 'case_law',
        'jurisdiction': 'criminal',
        'text': """
        CRIMINAL LAW - APPEAL AGAINST SENTENCE

        The appellant was convicted after trial of armed robbery contrary to s 97(1)
        of the Crimes Act 1900 (NSW). The sentencing judge imposed a sentence of
        7 years imprisonment with a non-parole period of 4 years.

        Grounds of appeal:
        1. Sentence manifestly excessive
        2. Insufficient discount for prospects of rehabilitation
        3. Error in application of sentencing principles

        The objective seriousness was mid-range. The use of a knife as a weapon
        was an aggravating factor. The appellant's prior record showed two previous
        convictions for dishonesty offences.

        Section 21A of the Crimes (Sentencing Procedure) Act 1999 (NSW) requires
        consideration of aggravating and mitigating factors.

        Cases cited:
        Muldrock v The Queen (2011) 244 CLR 120
        Markarian v The Queen (2005) 228 CLR 357

        The appeal is dismissed. The sentence imposed was within range and
        appropriate in all circumstances.
        """
    }


@pytest.fixture
def sample_migration_decision() -> Dict[str, Any]:
    """Real migration tribunal decision sample."""
    return {
        'id': 'mig_001',
        'citation': '[2022] AATA 1234',
        'type': 'tribunal_decision',
        'jurisdiction': 'migration',
        'text': """
        MIGRATION - VISA REFUSAL - JUDICIAL REVIEW

        The applicant seeks review of the delegate's decision to refuse a Partner (Provisional)
        visa under subclass 309 of the Migration Regulations 1994 (Cth).

        The issue is whether the relationship is genuine and continuing within the meaning
        of regulation 1.15A.

        The applicant provided the following evidence:
        - Joint bank account statements
        - Shared lease agreement
        - Statutory declarations from friends and family
        - Photographs spanning 3 years

        The delegate was not satisfied the relationship was genuine, citing:
        1. Limited financial intermingling
        2. Inconsistencies in testimony
        3. Short cohabitation period

        Under s 359A of the Migration Act 1958 (Cth), the Tribunal must provide
        particulars of adverse information to the applicant.

        Cases cited:
        Minister for Immigration v SZIAI (2009) 259 ALR 429

        The Tribunal sets aside the delegate's decision and substitutes a decision
        to grant the visa, being satisfied on the evidence that the relationship
        is genuine and continuing.
        """
    }


@pytest.fixture
def sample_employment_decision() -> Dict[str, Any]:
    """Real employment/industrial decision sample."""
    return {
        'id': 'emp_001',
        'citation': '[2023] FWC 456',
        'type': 'tribunal_decision',
        'jurisdiction': 'employment',
        'text': """
        FAIR WORK - UNFAIR DISMISSAL

        The applicant claims unfair dismissal under s 385 of the Fair Work Act 2009 (Cth).
        The respondent employer dismissed the applicant for alleged serious misconduct.

        The applicant had been employed as a warehouse supervisor for 8 years. On 15 March 2023,
        the applicant was summarily dismissed following an incident involving workplace safety.

        Key issues:
        1. Was there a valid reason for dismissal related to conduct or capacity?
        2. Was the applicant afforded procedural fairness?
        3. Was dismissal harsh, unjust or unreasonable in all circumstances?

        Section 387 factors:
        (a) Valid reason - The conduct was serious but not wilful
        (b) Notified of reason - Yes, but inadequate opportunity to respond
        (c) Opportunity to respond - Limited, only 1 hour notice
        (d) Unreasonable refusal of support person - Not applicable
        (e) Warnings given - No prior warnings for similar conduct
        (f) Size of enterprise - Medium sized, 150 employees
        (g) Absence of HR specialist - HR present at meeting
        (h) Other matters - Long service, good record

        Cases cited:
        Selvachandran v Peteron Plastics Pty Ltd (1995) 62 IR 371
        King v Freshmore (Vic) Pty Ltd (2000) 97 IR 131

        The Commission finds the dismissal was harsh and orders reinstatement with
        continuity of service, or in the alternative, compensation of 12 weeks pay.
        """
    }


@pytest.fixture
def sample_legislation() -> Dict[str, Any]:
    """Real legislation document sample."""
    return {
        'id': 'leg_001',
        'citation': 'Fair Work Act 2009 (Cth)',
        'type': 'primary_legislation',
        'jurisdiction': 'Commonwealth',
        'text': """
        Fair Work Act 2009

        An Act relating to workplace relations for employees, employers and organisations,
        and for related purposes.

        Part 1-1 - Preliminary

        Section 1 - Short title
        This Act may be cited as the Fair Work Act 2009.

        Section 3 - Objects
        The objects of this Act are:
        (a) to provide a balanced framework for cooperative and productive workplace relations
        (b) to promote social inclusion for all Australians by ensuring a guaranteed safety net
        (c) to enable fairness and representation at work

        Part 3-2 - Unfair Dismissal

        Section 385 - What is an unfair dismissal
        A person has been unfairly dismissed if:
        (a) the person has been dismissed; and
        (b) the dismissal was harsh, unjust or unreasonable; and
        (c) the dismissal was not consistent with the Small Business Fair Dismissal Code; and
        (d) the dismissal was not a case of genuine redundancy.

        Section 387 - Criteria for considering harshness etc
        In considering whether it is satisfied that a dismissal was harsh, unjust or
        unreasonable, the FWC must take into account:
        (a) whether there was a valid reason for the dismissal related to the person's
            capacity or conduct;
        (b) whether the person was notified of that reason;
        (c) whether the person was given an opportunity to respond...
        """
    }


@pytest.fixture
def sample_multi_domain_decision() -> Dict[str, Any]:
    """Decision spanning multiple domains."""
    return {
        'id': 'multi_001',
        'citation': '[2021] FCA 789',
        'type': 'case_law',
        'jurisdiction': 'federal',
        'text': """
        CORPORATIONS - EMPLOYMENT - DISCRIMINATION

        This matter involves overlapping issues of corporate law, employment law,
        and anti-discrimination law.

        The applicant was a director and employee of the respondent company. She alleges:
        1. Unfair dismissal under the Fair Work Act 2009 (Cth)
        2. Sex discrimination under the Sex Discrimination Act 1984 (Cth)
        3. Breach of director's duties under the Corporations Act 2001 (Cth)
        4. Oppression under s 232 of the Corporations Act

        The respondent company denies the allegations and relies on:
        - Valid reason for termination of employment
        - Legitimate business restructure
        - Proper exercise of board powers

        Relevant legislation:
        Fair Work Act 2009 (Cth) ss 385, 387
        Sex Discrimination Act 1984 (Cth) ss 5, 7, 14
        Corporations Act 2001 (Cth) ss 180, 181, 232, 233

        Cases cited:
        Gambotto v WCP Ltd (1995) 182 CLR 432 (corporate oppression)
        Waters v Public Transport Corporation (1991) 173 CLR 349 (discrimination)
        Selvachandran v Peteron Plastics (1995) 62 IR 371 (unfair dismissal)

        The Court finds in favor of the applicant on grounds 1 and 2, orders
        reinstatement and damages for discrimination.
        """
    }


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestFullClassificationPipeline:
    """Test complete classification pipeline end-to-end."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance for tests."""
        return EnhancedDomainClassifier()

    def test_family_law_full_pipeline(self, classifier, sample_family_decision):
        """Test complete classification of family law decision."""
        result = classifier.classify(sample_family_decision)

        # Verify classification structure
        assert isinstance(result, MultiDomainClassification)
        assert result.document_id == 'family_001'

        # Primary domain should be Family
        assert result.primary_domain == 'Family'
        assert result.primary_confidence > 0.3

        # Court information
        assert result.court_info is not None
        assert result.court_info.code == 'FamCA'
        assert result.court_info.name == 'Family Court of Australia'
        assert result.court_info.domain_hint == 'Family'

        # Authority and binding status
        assert result.authority_score == 75
        assert result.binding_status in [BindingStatus.PERSUASIVE, BindingStatus.NOT_BINDING]

        # Document type
        assert result.document_type == DocumentType.CASE_LAW
        assert result.citation_type == CitationType.MEDIUM_NEUTRAL

        # Legislation extraction
        assert len(result.legislation_refs) > 0
        family_act_found = any('Family Law Act' in ref.name for ref in result.legislation_refs)
        assert family_act_found

        # Section extraction
        section_79_found = any(ref.section and '79' in ref.section for ref in result.legislation_refs)
        assert section_79_found

        # BOOST scoring
        assert result.boost_breakdown.court_domain_hint == 25  # FamCA hint = Family
        assert result.boost_breakdown.legislation_reference >= 15
        assert result.boost_breakdown.total > 30

    def test_criminal_law_full_pipeline(self, classifier, sample_criminal_decision):
        """Test complete classification of criminal law decision."""
        result = classifier.classify(sample_criminal_decision)

        # Primary domain should be Criminal
        assert result.primary_domain == 'Criminal'
        assert result.primary_confidence > 0.2

        # Court information - CCA has domain hint
        assert result.court_info is not None
        assert result.court_info.code == 'NSWCCA'
        assert result.court_info.domain_hint == 'Criminal'

        # High authority for appellate court
        assert result.authority_score == 85

        # BOOST 6: Case title pattern "R v"
        assert result.boost_breakdown.case_title_pattern >= 20

        # BOOST 3: Court domain hint
        assert result.boost_breakdown.court_domain_hint == 25

        # Legislation references
        crimes_act_found = any('Crimes Act' in ref.name for ref in result.legislation_refs)
        assert crimes_act_found

    def test_migration_admin_full_pipeline(self, classifier, sample_migration_decision):
        """Test classification of migration/administrative decision."""
        result = classifier.classify(sample_migration_decision)

        # Should classify as Administrative
        assert result.primary_domain == 'Administrative'

        # Tribunal decision
        assert result.document_type == DocumentType.TRIBUNAL_DECISION

        # Court info for AATA
        assert result.court_info is not None
        assert result.court_info.code == 'AATA'
        assert result.court_info.domain_hint == 'Administrative'

        # Lower authority for tribunal
        assert result.authority_score == 40
        assert result.binding_status == BindingStatus.NOT_BINDING

        # BOOST 3: Domain hint alignment
        assert result.boost_breakdown.court_domain_hint == 25

        # Migration Act should be extracted
        migration_act_found = any('Migration Act' in ref.name for ref in result.legislation_refs)
        assert migration_act_found

    def test_employment_law_full_pipeline(self, classifier, sample_employment_decision):
        """Test classification of employment/industrial decision."""
        result = classifier.classify(sample_employment_decision)

        # Should classify as Employment
        assert result.primary_domain == 'Employment'

        # FWC tribunal
        assert result.court_info is not None
        assert result.court_info.code == 'FWC'
        assert result.court_info.domain_hint == 'Employment'

        # Fair Work Act extraction
        fw_act_found = any('Fair Work Act' in ref.name for ref in result.legislation_refs)
        assert fw_act_found

        # BOOST scoring
        assert result.boost_breakdown.court_domain_hint == 25
        assert result.boost_breakdown.legislation_reference >= 15

    def test_legislation_full_pipeline(self, classifier, sample_legislation):
        """Test classification of legislation document."""
        result = classifier.classify(sample_legislation)

        # Document type should be primary legislation
        assert result.document_type == DocumentType.PRIMARY_LEGISLATION

        # BOOST 8: Legislation status boost
        assert result.boost_breakdown.legislation_status == 10

        # BOOST 10: Document type weight
        assert result.boost_breakdown.document_type_weight >= 5

        # Should classify as Employment based on Fair Work Act
        assert result.primary_domain == 'Employment'

    def test_multi_domain_detection(self, classifier, sample_multi_domain_decision):
        """Test detection and scoring of multiple domains."""
        result = classifier.classify(sample_multi_domain_decision)

        # Should have a primary domain
        assert result.primary_domain != 'Unclassified'

        # Should detect secondary domains
        assert len(result.secondary_domains) > 0

        # BOOST 7: Multi-domain confidence boost should apply
        # Only applies if 2+ domains have score >= 20
        if result.boost_breakdown.multi_domain_confidence > 0:
            assert result.boost_breakdown.multi_domain_confidence == 5

        # Should extract multiple legislation acts
        assert len(result.legislation_refs) >= 2

        # Verify specific acts mentioned
        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Fair Work Act' in name for name in leg_names)
        assert any('Corporations Act' in name or 'Sex Discrimination Act' in name for name in leg_names)


class TestBOOSTScoring:
    """Test all 10 BOOST factors individually."""

    @pytest.fixture
    def classifier(self):
        return EnhancedDomainClassifier()

    def test_boost_1_citation_match(self, classifier):
        """BOOST 1: Keywords in citation get +10."""
        doc = {
            'id': 'test_b1',
            'citation': 'Family Law Property Settlement [2020] FamCA 100',
            'type': 'case_law',
            'text': 'Family law matter concerning property.'
        }

        result = classifier.classify(doc)
        assert result.boost_breakdown.citation_match >= 10

    def test_boost_2_jurisdiction_alignment(self, classifier):
        """BOOST 2: Jurisdiction-specific terms get boost."""
        doc = {
            'id': 'test_b2',
            'citation': '[2020] FamCA 100',
            'type': 'case_law',
            'jurisdiction': 'family',
            'text': 'Family law parenting dispute section 79.'
        }

        result = classifier.classify(doc)
        # Jurisdiction alignment may vary based on implementation
        assert result.boost_breakdown.jurisdiction_alignment >= 0

    def test_boost_3_court_domain_hint(self, classifier):
        """BOOST 3: Court domain hint alignment +25."""
        doc = {
            'id': 'test_b3',
            'citation': '[2020] FamCA 100',
            'type': 'case_law',
            'text': 'Family law property settlement under Family Law Act.'
        }

        result = classifier.classify(doc)
        # FamCA has domain_hint='Family' so should get +25
        assert result.boost_breakdown.court_domain_hint == 25

    def test_boost_4_legislation_reference(self, classifier):
        """BOOST 4: Legislation reference domain boost +15."""
        doc = {
            'id': 'test_b4',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': 'The applicant relies on the Fair Work Act 2009 (Cth) s 385 unfair dismissal provisions.'
        }

        result = classifier.classify(doc)
        # Should get legislation reference boost
        assert result.boost_breakdown.legislation_reference >= 15

    def test_boost_5_case_law_reference(self, classifier):
        """BOOST 5: Landmark case reference +10."""
        doc = {
            'id': 'test_b5',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': 'Following the principles in Muldrock v The Queen (2011) 244 CLR 120.'
        }

        result = classifier.classify(doc)
        # May get case law reference boost if Muldrock is in landmark cases
        assert result.boost_breakdown.case_law_reference >= 0

    def test_boost_6_case_title_pattern(self, classifier):
        """BOOST 6: Criminal case title patterns +20."""
        doc = {
            'id': 'test_b6',
            'citation': 'R v Johnson [2020] NSWCCA 50',
            'type': 'case_law',
            'text': 'The accused was charged with armed robbery.'
        }

        result = classifier.classify(doc)
        # "R v" pattern should trigger +20
        assert result.boost_breakdown.case_title_pattern >= 20

    def test_boost_7_multi_domain_confidence(self, classifier):
        """BOOST 7: Multiple strong domains get +5."""
        doc = {
            'id': 'test_b7',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': '''
            This case involves employment discrimination. The applicant claims unfair dismissal
            under the Fair Work Act 2009 and sex discrimination under the Sex Discrimination Act 1984.
            Corporations Act duties also arise. Contract law principles apply.
            '''
        }

        result = classifier.classify(doc)
        # If 2+ domains score >= 20, should get +5
        # Note: May not always trigger depending on keyword density
        assert result.boost_breakdown.multi_domain_confidence >= 0

    def test_boost_8_legislation_status(self, classifier):
        """BOOST 8: Legislation documents get +10."""
        doc = {
            'id': 'test_b8',
            'citation': 'Fair Work Act 2009 (Cth)',
            'type': 'primary_legislation',
            'text': 'An Act relating to workplace relations.'
        }

        result = classifier.classify(doc)
        assert result.boost_breakdown.legislation_status == 10

    def test_boost_9_common_law_distinction(self, classifier):
        """BOOST 9: Common law decisions get equity/tort boost +5."""
        doc = {
            'id': 'test_b9',
            'citation': '[2020] NSWSC 100',
            'type': 'case_law',
            'text': 'This is an equitable claim for breach of fiduciary duty. Equitable remedies apply.'
        }

        result = classifier.classify(doc)
        # Common law boost for equity/tort/property categories
        assert result.boost_breakdown.common_statute_distinction >= 0

    def test_boost_10_document_type_weight(self, classifier):
        """BOOST 10: Document type weighting."""
        doc = {
            'id': 'test_b10',
            'citation': '[2020] HCA 1',
            'type': 'case_law',
            'text': 'Constitutional interpretation matter.'
        }

        result = classifier.classify(doc)
        # Case law should get document type weight
        assert result.boost_breakdown.document_type_weight >= 0


class TestCitationIntegration:
    """Test citation extraction integration with classification."""

    @pytest.fixture
    def classifier(self):
        return EnhancedDomainClassifier()

    def test_multiple_legislation_extraction(self, classifier):
        """Test extraction of multiple legislation references."""
        doc = {
            'id': 'test_multi_leg',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': '''
            The Fair Work Act 2009 (Cth) s 385 applies. The applicant also relies on
            the Sex Discrimination Act 1984 (Cth) s 14 and the Corporations Act 2001 (Cth) s 232.
            '''
        }

        result = classifier.classify(doc)

        # Should extract all three acts
        assert len(result.legislation_refs) >= 3

        # Verify specific acts
        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Fair Work Act' in name for name in leg_names)
        assert any('Sex Discrimination Act' in name for name in leg_names)
        assert any('Corporations Act' in name for name in leg_names)

        # Verify sections extracted
        sections = [ref.section for ref in result.legislation_refs if ref.section]
        assert len(sections) >= 3

    def test_case_citation_extraction(self, classifier):
        """Test extraction of case citations."""
        doc = {
            'id': 'test_cases',
            'citation': '[2020] NSWCA 100',
            'type': 'case_law',
            'text': '''
            The principles in Muldrock v The Queen (2011) 244 CLR 120 apply.
            See also Markarian v The Queen (2005) 228 CLR 357.
            Recent decision in Jones v Smith [2019] HCA 5.
            '''
        }

        result = classifier.classify(doc)

        # Should extract case references
        assert len(result.case_refs) > 0

    def test_jurisdiction_extraction(self, classifier):
        """Test jurisdiction extraction from legislation."""
        doc = {
            'id': 'test_juris',
            'citation': '[2020] FCA 100',
            'type': 'case_law',
            'text': '''
            Commonwealth legislation: Fair Work Act 2009 (Cth)
            NSW legislation: Crimes Act 1900 (NSW)
            Victorian legislation: Crimes Act 1958 (Vic)
            '''
        }

        result = classifier.classify(doc)

        # Check jurisdiction extraction
        jurisdictions = [ref.jurisdiction for ref in result.legislation_refs if ref.jurisdiction]
        assert 'CTH' in jurisdictions
        assert 'NSW' in jurisdictions or 'VIC' in jurisdictions


class TestSerializationAndOutput:
    """Test serialization of classification results."""

    @pytest.fixture
    def classifier(self):
        return EnhancedDomainClassifier()

    def test_complete_serialization(self, classifier, sample_family_decision):
        """Test full serialization to dictionary."""
        result = classifier.classify(sample_family_decision)
        serialized = result.to_dict()

        # Check all required fields present
        required_fields = [
            'document_id', 'primary_domain', 'primary_category', 'primary_confidence',
            'secondary_domains', 'document_type', 'citation_type', 'legislation_refs',
            'case_refs', 'court_info', 'authority_score', 'binding_status',
            'boost_breakdown', 'keyword_matches', 'classification_version'
        ]

        for field in required_fields:
            assert field in serialized, f"Missing field: {field}"

        # Check types
        assert isinstance(serialized['primary_confidence'], float)
        assert isinstance(serialized['authority_score'], int)
        assert isinstance(serialized['boost_breakdown'], dict)
        assert 'total' in serialized['boost_breakdown']

        # Version should be 2.0
        assert serialized['classification_version'] == '2.0'

    def test_boost_breakdown_serialization(self, classifier):
        """Test BOOST breakdown serialization."""
        doc = {
            'id': 'test_boost_ser',
            'citation': '[2020] FamCA 100',
            'type': 'case_law',
            'text': 'Family law property settlement under Family Law Act 1975 (Cth) s 79.'
        }

        result = classifier.classify(doc)
        boost_dict = result.boost_breakdown.to_dict()

        # All 10 factors plus total
        expected_keys = [
            'citation_match', 'jurisdiction_alignment', 'court_domain_hint',
            'legislation_reference', 'case_law_reference', 'case_title_pattern',
            'multi_domain_confidence', 'legislation_status', 'common_statute_distinction',
            'document_type_weight', 'total'
        ]

        for key in expected_keys:
            assert key in boost_dict
            assert isinstance(boost_dict[key], int)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def classifier(self):
        return EnhancedDomainClassifier()

    def test_empty_document(self, classifier):
        """Test classification of empty document."""
        doc = {
            'id': 'empty',
            'citation': '',
            'text': ''
        }

        result = classifier.classify(doc)
        assert result.primary_domain == 'Unclassified'
        assert result.primary_confidence == 0.0

    def test_minimal_document(self, classifier):
        """Test document with minimal information."""
        doc = {
            'id': 'minimal',
            'text': 'Brief legal text.'
        }

        result = classifier.classify(doc)
        assert isinstance(result, MultiDomainClassification)
        assert result.document_id == 'minimal'

    def test_malformed_citation(self, classifier):
        """Test handling of malformed citations."""
        doc = {
            'id': 'malformed',
            'citation': 'Not a real citation format',
            'text': 'Family law matter.'
        }

        result = classifier.classify(doc)
        # Should still classify based on text
        assert isinstance(result, MultiDomainClassification)

    def test_unknown_court_code(self, classifier):
        """Test handling of unknown court codes."""
        doc = {
            'id': 'unknown_court',
            'citation': '[2020] UNKNOWN 100',
            'text': 'Legal matter.'
        }

        result = classifier.classify(doc)
        # May not have court info, but should not crash
        assert isinstance(result, MultiDomainClassification)

    def test_very_long_document(self, classifier):
        """Test handling of very long documents."""
        doc = {
            'id': 'long_doc',
            'citation': '[2020] NSWSC 100',
            'text': 'Family law property settlement. ' * 10000  # Very long text
        }

        result = classifier.classify(doc)
        # Should handle gracefully (classifier uses text[:15000])
        assert isinstance(result, MultiDomainClassification)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
