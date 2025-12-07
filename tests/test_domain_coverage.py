"""
Domain Coverage Tests for Australian Legal Corpus Classification System

This test suite validates classification accuracy across all major legal domains:
- Employment Law
- Administrative Law
- Criminal Law
- Family Law
- Commercial/Corporate Law
- Property Law
- Constitutional Law
- Taxation Law
- Environmental Law
- Intellectual Property Law
- Torts Law

Ensures no major domains are missing from classification system.
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.multi_domain_classifier import (
    EnhancedDomainClassifier,
    DocumentType,
    CitationType,
)


# ============================================================================
# TEST FIXTURES - ONE FOR EACH MAJOR DOMAIN
# ============================================================================

@pytest.fixture
def classifier():
    """Create classifier instance."""
    return EnhancedDomainClassifier()


@pytest.fixture
def employment_sample() -> Dict[str, Any]:
    """Employment Law test document."""
    return {
        'id': 'employment_001',
        'citation': '[2023] FWC 234',
        'type': 'tribunal_decision',
        'text': '''
        UNFAIR DISMISSAL APPLICATION

        The applicant was employed as a warehouse manager for 6 years. On 15 January 2023,
        the respondent employer summarily dismissed the applicant for alleged misconduct.

        Section 385 of the Fair Work Act 2009 (Cth) provides that a person has been
        unfairly dismissed if the dismissal was harsh, unjust or unreasonable.

        Section 387 factors to consider:
        (a) Valid reason related to conduct or capacity
        (b) Person was notified of the reason
        (c) Opportunity to respond to allegations
        (d) Support person not unreasonably refused
        (e) Warnings about unsatisfactory performance
        (f) Size of the employer's enterprise
        (g) Degree of specialist HR expertise

        The applicant had an unblemished record and was given no prior warnings.
        The employer failed to afford procedural fairness.

        Cases cited:
        Selvachandran v Peteron Plastics Pty Ltd (1995) 62 IR 371
        King v Freshmore (Vic) Pty Ltd (2000) 97 IR 131

        Order: Reinstatement with continuity of service.
        '''
    }


@pytest.fixture
def administrative_sample() -> Dict[str, Any]:
    """Administrative Law test document."""
    return {
        'id': 'admin_001',
        'citation': '[2022] AATA 567',
        'type': 'tribunal_decision',
        'text': '''
        ADMINISTRATIVE LAW - JUDICIAL REVIEW - VISA CANCELLATION

        The applicant seeks review of the Minister's decision to cancel their visa
        under s 501 of the Migration Act 1958 (Cth) on character grounds.

        The applicant has a substantial criminal record including convictions for
        assault and drug offences. The Minister exercised discretion under s 501(2)
        to cancel the visa in the national interest.

        Relevant considerations under Direction No 90:
        1. Protection of the Australian community
        2. Best interests of minor children in Australia
        3. Expectations of the Australian community
        4. Extent of impediments if removed

        The applicant has three Australian citizen children and has lived in Australia
        since age 5. However, the serious criminal history and risk of reoffending
        weigh heavily against the applicant.

        Cases cited:
        Minister for Immigration v SZIAI (2009) 259 ALR 429
        Plaintiff M70/2011 v Minister for Immigration (2011) 244 CLR 144

        Decision: The Tribunal affirms the delegate's decision to cancel the visa.
        '''
    }


@pytest.fixture
def criminal_sample() -> Dict[str, Any]:
    """Criminal Law test document."""
    return {
        'id': 'criminal_001',
        'citation': 'R v Thompson [2024] NSWCCA 145',
        'type': 'case_law',
        'text': '''
        CRIMINAL LAW - APPEAL AGAINST CONVICTION - MURDER

        The appellant was convicted after jury trial of murder contrary to s 18
        of the Crimes Act 1900 (NSW). The Crown alleged the appellant intentionally
        killed the deceased by stabbing him multiple times.

        Grounds of appeal:
        1. Verdict unreasonable and cannot be supported by the evidence
        2. Misdirection to jury on intent
        3. Exclusion of evidence prejudiced the appellant

        The mens rea for murder requires proof beyond reasonable doubt that the accused:
        (a) intended to kill, or
        (b) intended to inflict grievous bodily harm, or
        (c) acted with reckless indifference to human life

        The trial judge directed the jury in accordance with Zecevic v DPP (1987) 162 CLR 645.

        Self-defence was raised under s 418 of the Crimes Act. The prosecution must
        disprove self-defence beyond reasonable doubt. The test is whether the accused
        believed on reasonable grounds that it was necessary to do what they did in
        self-defence: Zecevic principle.

        Cases cited:
        Zecevic v DPP (Vic) (1987) 162 CLR 645
        Royall v The Queen (1991) 172 CLR 378
        Crabbe v The Queen (1985) 156 CLR 464

        The appeal is dismissed. The conviction is sound.
        '''
    }


@pytest.fixture
def family_sample() -> Dict[str, Any]:
    """Family Law test document."""
    return {
        'id': 'family_001',
        'citation': '[2023] FamCA 678',
        'type': 'case_law',
        'text': '''
        FAMILY LAW - PARENTING ORDERS - RELOCATION

        The mother seeks to relocate with the two children (aged 8 and 6) from
        Sydney to Perth, a distance of 4000km. The father opposes the relocation.

        The paramount consideration is the best interests of the children pursuant
        to s 60CA of the Family Law Act 1975 (Cth).

        Primary considerations under s 60CC(2):
        (a) Benefit of meaningful relationship with both parents
        (b) Need to protect from harm, abuse, neglect or family violence

        Additional considerations under s 60CC(3):
        (a) Views expressed by the children
        (b) Nature of relationship with each parent
        (c) Likely effect of change in circumstances
        (d) Capacity of each parent to meet needs
        (e) Maturity, sex, lifestyle and background of child

        The mother has a genuine employment opportunity in Perth. The father has
        exercised time with the children every second weekend. The children have
        expressed a preference to stay in Sydney close to their school and friends.

        Cases cited:
        MRR v GR (2010) 240 CLR 461
        Goode & Goode (2006) FLC 93-286
        AMS v AIF (1999) FLC 92-825

        Order: Relocation not approved. Parenting orders to continue as is.
        '''
    }


@pytest.fixture
def commercial_sample() -> Dict[str, Any]:
    """Commercial/Corporate Law test document."""
    return {
        'id': 'commercial_001',
        'citation': '[2022] FCA 890',
        'type': 'case_law',
        'text': '''
        CORPORATIONS - DIRECTOR'S DUTIES - INSOLVENT TRADING

        The plaintiff ASIC alleges the defendant directors breached their duties under
        s 180 (care and diligence) and s 588G (insolvent trading) of the Corporations
        Act 2001 (Cth).

        The company continued to incur debts during the period January to June 2021
        when there were reasonable grounds to suspect insolvency. The directors failed
        to prevent the company from incurring those debts.

        Section 588G provides that a director contravenes if:
        (a) company incurs a debt
        (b) person is a director at the time
        (c) company is insolvent or becomes insolvent by incurring the debt
        (d) reasonable grounds for suspecting insolvency exist
        (e) director is aware of those grounds or a reasonable person would be aware

        Defences under s 588H:
        - Reasonable grounds to expect solvency
        - Relied on competent and reliable person
        - Illness or other good reason for not participating
        - Took all reasonable steps to prevent incurring debt

        The directors cannot establish any defence. They ignored warnings from the
        accountant and auditor about deteriorating financial position.

        Cases cited:
        ASIC v Healey (2011) 196 FCR 291
        ASIC v Plymin (2003) 46 ACSR 126
        Morley v ASIC (2010) 247 CLR 486

        Orders: Civil penalty of $200,000 per director. Disqualification for 5 years.
        '''
    }


@pytest.fixture
def property_sample() -> Dict[str, Any]:
    """Property Law test document."""
    return {
        'id': 'property_001',
        'citation': '[2023] NSWSC 456',
        'type': 'case_law',
        'text': '''
        PROPERTY - TORRENS TITLE - INDEFEASIBILITY - CAVEATS

        The plaintiff seeks removal of a caveat lodged by the defendant over the
        plaintiff's land. The defendant claims an equitable interest based on an
        alleged oral agreement to transfer the property.

        Under s 74F of the Real Property Act 1900 (NSW), a person claiming an interest
        in land may lodge a caveat. The caveat prevents registration of dealings
        inconsistent with the claimed interest.

        The plaintiff is a registered proprietor and prima facie has indefeasible title
        under s 42 of the Real Property Act. Indefeasibility means the registered
        proprietor's title cannot be challenged except in cases of fraud, prior
        registered interest, or statutory exception.

        The defendant must establish a serious question to be tried regarding the
        alleged equitable interest. Mere assertion is insufficient.

        The evidence shows:
        - No written agreement (Statute of Frauds issue)
        - No part performance sufficient to take out of statute
        - No constructive trust established
        - No proprietary estoppel made out

        Cases cited:
        Frazer v Walker [1967] 1 AC 569
        Breskvar v Wall (1971) 126 CLR 376
        Bahr v Nicolay (No 2) (1988) 164 CLR 604

        Order: Caveat to be removed. Costs against defendant.
        '''
    }


@pytest.fixture
def constitutional_sample() -> Dict[str, Any]:
    """Constitutional Law test document."""
    return {
        'id': 'constitutional_001',
        'citation': '[2024] HCA 8',
        'type': 'case_law',
        'text': '''
        CONSTITUTIONAL LAW - SECTION 51 - CORPORATIONS POWER

        The plaintiff challenges the validity of the Fair Work Act 2009 (Cth) provisions
        as beyond the corporations power in s 51(xx) of the Constitution.

        Section 51(xx) grants Parliament power to make laws with respect to:
        "foreign corporations, and trading or financial corporations formed within
        the limits of the Commonwealth"

        The question is whether the impugned provisions are reasonably appropriate
        and adapted to regulate the activities of constitutional corporations.

        The High Court in New South Wales v Commonwealth (Work Choices Case) (2006)
        229 CLR 1 held that the corporations power extends to:
        - Employment relationships of constitutional corporations
        - Terms and conditions of employment
        - Industrial relations systems

        The characterization test requires determining whether the law in substance
        relates to corporations or whether it regulates corporations merely incidentally.

        The principle in Actors and Announcers Equity Association v Fontana Films
        (1982) 150 CLR 169 applies: the power supports laws regulating the activities
        and operations of corporations.

        Cases cited:
        New South Wales v Commonwealth (2006) 229 CLR 1 (Work Choices)
        R v Trade Practices Tribunal; Ex parte Tasmanian Breweries (1970) 123 CLR 361
        Re Dingjan (1995) 183 CLR 323

        Held: The provisions are valid exercises of the corporations power.
        '''
    }


@pytest.fixture
def taxation_sample() -> Dict[str, Any]:
    """Taxation Law test document."""
    return {
        'id': 'tax_001',
        'citation': '[2022] FCA 234',
        'type': 'case_law',
        'text': '''
        TAXATION - INCOME TAX - CAPITAL GAINS TAX - MAIN RESIDENCE EXEMPTION

        The applicant appeals against an assessment by the Commissioner of Taxation
        disallowing the main residence exemption under s 118-110 of the Income Tax
        Assessment Act 1997 (Cth).

        The applicant sold a property in 2020 and claimed the capital gain was exempt
        as it was their main residence. The Commissioner contends the property was
        used for income-producing purposes and the exemption does not apply.

        Section 118-110 provides a complete exemption from CGT for a capital gain
        on a dwelling that is your main residence. The key requirement is that the
        dwelling was the taxpayer's main residence throughout the ownership period.

        Factors to determine main residence (Taxation Ruling TR 98/14):
        - Where the taxpayer's family resides
        - Place of employment and business
        - Where personal belongings are located
        - Address for mail and electoral roll
        - Social and living arrangements

        The property was rented out for 8 of the 10 years of ownership. The taxpayer
        lived in a different property during that time. The absence exceeds the
        6-year absence rule for previously occupied main residences.

        Cases cited:
        FC of T v Buckland (1987) 18 ATR 957
        Wakelin v FC of T (1997) 37 ATR 399
        Miller v FC of T (2006) 62 ATR 284

        Decision: Appeal dismissed. Assessment confirmed. Main residence exemption denied.
        '''
    }


@pytest.fixture
def environmental_sample() -> Dict[str, Any]:
    """Environmental Law test document."""
    return {
        'id': 'env_001',
        'citation': '[2023] NSWLEC 123',
        'type': 'case_law',
        'text': '''
        ENVIRONMENTAL LAW - DEVELOPMENT CONSENT - CLASS 4 PROCEEDINGS

        The applicant seeks judicial review of the consent authority's decision to
        grant development consent for a coal mine under s 89 of the Environmental
        Planning and Assessment Act 1979 (NSW).

        This is a Class 4 proceeding under s 20 of the Land and Environment Court
        Act 1979 (NSW) - judicial review of administrative decisions.

        Grounds of review:
        1. Failure to properly consider environmental impacts under s 79C
        2. Breach of principles of ecologically sustainable development
        3. Wednesbury unreasonableness
        4. Procedural unfairness in public consultation

        Section 79C requires consent authority to consider:
        (a) Environmental planning instruments
        (b) Likely impacts of development including environmental impacts
        (c) Suitability of the site
        (d) Public submissions
        (e) Public interest

        The development will impact threatened species habitat and increase greenhouse
        gas emissions significantly. The consent authority's reasons do not adequately
        address climate change impacts or cumulative effects.

        Cases cited:
        Gray v Minister for Planning (2006) 152 LGERA 258
        Gloucester Resources Limited v Minister for Planning (2019) 234 LGERA 257
        Walker v Minister for Planning (2007) 157 LGERA 124

        Order: Development consent quashed. Matter remitted for reconsideration.
        '''
    }


@pytest.fixture
def intellectual_property_sample() -> Dict[str, Any]:
    """Intellectual Property Law test document."""
    return {
        'id': 'ip_001',
        'citation': '[2023] FCA 567',
        'type': 'case_law',
        'text': '''
        INTELLECTUAL PROPERTY - COPYRIGHT - SUBSTANTIAL PART - INFRINGEMENT

        The applicant is a software company alleging copyright infringement of its
        computer program by the respondent under s 36 of the Copyright Act 1968 (Cth).

        Copyright subsists in original literary works including computer programs:
        s 32(1). The applicant must establish:
        (a) Copyright subsists in the work
        (b) Applicant owns the copyright
        (c) Respondent reproduced a substantial part without licence

        Section 36(1) provides that copyright includes the exclusive right to:
        - Reproduce the work in a material form
        - Publish the work
        - Communicate the work to the public

        Substantiality is assessed qualitatively not quantitatively. The test is
        whether a substantial part of the independent intellectual effort of the
        author has been taken: IceTV v Nine Network (2009) 239 CLR 458.

        The respondent copied 15% of the source code but this included the core
        algorithms and functionality. This constitutes reproduction of a substantial
        part despite the relatively small percentage.

        Defences under ss 40-43 (fair dealing) do not apply. The use was commercial
        and not for research, study, criticism or review.

        Cases cited:
        IceTV Pty Ltd v Nine Network Australia Pty Ltd (2009) 239 CLR 458
        SW Hart & Co v Edwards Hot Water Systems (1985) 159 CLR 466
        Telstra Corporation v Phone Directories Company (2010) 194 FCR 142

        Orders: Injunction granted. Damages or account of profits. Costs to applicant.
        '''
    }


@pytest.fixture
def torts_sample() -> Dict[str, Any]:
    """Torts Law test document."""
    return {
        'id': 'torts_001',
        'citation': '[2023] NSWSC 789',
        'type': 'case_law',
        'text': '''
        TORTS - NEGLIGENCE - DUTY OF CARE - BREACH - CAUSATION

        The plaintiff claims damages for personal injuries sustained when she slipped
        on a wet floor in the defendant's supermarket. The defendant denies liability.

        To establish negligence, the plaintiff must prove:
        (a) Defendant owed duty of care
        (b) Defendant breached that duty
        (c) Breach caused the plaintiff's injuries
        (d) Damages are not too remote

        Duty of care: An occupier owes a duty to take reasonable care to avoid
        foreseeable risk of injury to persons lawfully on the premises: Hackshaw v
        Shaw (1984) 155 CLR 614.

        Breach: The standard is that of a reasonable person in the defendant's position.
        Under s 5B of the Civil Liability Act 2002 (NSW), factors include:
        - Probability of harm if care not taken
        - Likely seriousness of harm
        - Burden of taking precautions
        - Social utility of the activity

        The floor had been wet for 30 minutes with no warning signs. No cleaning
        schedule was followed. A reasonable supermarket operator would have:
        - Implemented regular inspection regime
        - Placed warning signs
        - Cleaned spills immediately

        Causation: But for the wet floor, the plaintiff would not have fallen: s 5D.
        The breach was a necessary condition of the occurrence of harm.

        Cases cited:
        Hackshaw v Shaw (1984) 155 CLR 614
        Wyong Shire Council v Shirt (1980) 146 CLR 40
        Strong v Woolworths Ltd (2012) 246 CLR 182

        Judgment for plaintiff. Damages assessed at $250,000 plus costs.
        '''
    }


# ============================================================================
# DOMAIN COVERAGE TESTS
# ============================================================================

class TestEmploymentLawClassification:
    """Test Employment Law domain classification."""

    def test_employment_domain_detection(self, classifier, employment_sample):
        """Test detection of Employment Law domain."""
        result = classifier.classify(employment_sample)

        assert result.primary_domain == 'Employment'
        assert result.primary_confidence > 0.2

        # Fair Work Commission domain hint
        assert result.court_info is not None
        assert result.court_info.code == 'FWC'
        assert result.court_info.domain_hint == 'Employment'

    def test_employment_legislation_extraction(self, classifier, employment_sample):
        """Test extraction of Fair Work Act."""
        result = classifier.classify(employment_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Fair Work Act' in name for name in leg_names)


class TestAdministrativeLawClassification:
    """Test Administrative Law domain classification."""

    def test_administrative_domain_detection(self, classifier, administrative_sample):
        """Test detection of Administrative Law domain."""
        result = classifier.classify(administrative_sample)

        assert result.primary_domain == 'Administrative'
        assert result.primary_confidence > 0.2

    def test_migration_tribunal_detection(self, classifier, administrative_sample):
        """Test AATA tribunal detection."""
        result = classifier.classify(administrative_sample)

        assert result.court_info is not None
        assert result.court_info.code == 'AATA'
        assert result.court_info.domain_hint == 'Administrative'

    def test_migration_act_extraction(self, classifier, administrative_sample):
        """Test extraction of Migration Act."""
        result = classifier.classify(administrative_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Migration Act' in name for name in leg_names)


class TestCriminalLawClassification:
    """Test Criminal Law domain classification."""

    def test_criminal_domain_detection(self, classifier, criminal_sample):
        """Test detection of Criminal Law domain."""
        result = classifier.classify(criminal_sample)

        assert result.primary_domain == 'Criminal'
        assert result.primary_confidence > 0.2

    def test_criminal_court_detection(self, classifier, criminal_sample):
        """Test Court of Criminal Appeal detection."""
        result = classifier.classify(criminal_sample)

        assert result.court_info is not None
        assert result.court_info.code == 'NSWCCA'
        assert result.court_info.domain_hint == 'Criminal'

    def test_r_v_pattern_boost(self, classifier, criminal_sample):
        """Test R v pattern BOOST scoring."""
        result = classifier.classify(criminal_sample)

        # BOOST 6: Criminal case title pattern
        assert result.boost_breakdown.case_title_pattern >= 20

    def test_crimes_act_extraction(self, classifier, criminal_sample):
        """Test extraction of Crimes Act."""
        result = classifier.classify(criminal_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Crimes Act' in name for name in leg_names)


class TestFamilyLawClassification:
    """Test Family Law domain classification."""

    def test_family_domain_detection(self, classifier, family_sample):
        """Test detection of Family Law domain."""
        result = classifier.classify(family_sample)

        assert result.primary_domain == 'Family'
        assert result.primary_confidence > 0.2

    def test_family_court_detection(self, classifier, family_sample):
        """Test Family Court detection."""
        result = classifier.classify(family_sample)

        assert result.court_info is not None
        assert result.court_info.code == 'FamCA'
        assert result.court_info.domain_hint == 'Family'

    def test_family_law_act_extraction(self, classifier, family_sample):
        """Test extraction of Family Law Act."""
        result = classifier.classify(family_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Family Law Act' in name for name in leg_names)


class TestCommercialLawClassification:
    """Test Commercial/Corporate Law domain classification."""

    def test_commercial_domain_detection(self, classifier, commercial_sample):
        """Test detection of Commercial Law domain."""
        result = classifier.classify(commercial_sample)

        # Should classify as Commercial or Corporate
        assert result.primary_domain in ['Commercial', 'Corporate', 'Corporations']

    def test_corporations_act_extraction(self, classifier, commercial_sample):
        """Test extraction of Corporations Act."""
        result = classifier.classify(commercial_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Corporations Act' in name for name in leg_names)


class TestPropertyLawClassification:
    """Test Property Law domain classification."""

    def test_property_domain_detection(self, classifier, property_sample):
        """Test detection of Property Law domain."""
        result = classifier.classify(property_sample)

        assert result.primary_domain == 'Property'

    def test_real_property_act_extraction(self, classifier, property_sample):
        """Test extraction of Real Property Act."""
        result = classifier.classify(property_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Real Property Act' in name for name in leg_names)


class TestConstitutionalLawClassification:
    """Test Constitutional Law domain classification."""

    def test_constitutional_domain_detection(self, classifier, constitutional_sample):
        """Test detection of Constitutional Law domain."""
        result = classifier.classify(constitutional_sample)

        # Should classify as Constitutional
        assert result.primary_domain in ['Constitutional', 'Constitution']

    def test_high_court_detection(self, classifier, constitutional_sample):
        """Test High Court detection."""
        result = classifier.classify(constitutional_sample)

        assert result.court_info is not None
        assert result.court_info.code == 'HCA'
        assert result.authority_score == 100


class TestTaxationLawClassification:
    """Test Taxation Law domain classification."""

    def test_taxation_domain_detection(self, classifier, taxation_sample):
        """Test detection of Taxation Law domain."""
        result = classifier.classify(taxation_sample)

        assert result.primary_domain in ['Tax', 'Taxation']

    def test_income_tax_act_extraction(self, classifier, taxation_sample):
        """Test extraction of Income Tax Assessment Act."""
        result = classifier.classify(taxation_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Income Tax' in name for name in leg_names)


class TestEnvironmentalLawClassification:
    """Test Environmental Law domain classification."""

    def test_environmental_domain_detection(self, classifier, environmental_sample):
        """Test detection of Environmental Law domain."""
        result = classifier.classify(environmental_sample)

        assert result.primary_domain in ['Environment', 'Environmental']

    def test_land_environment_court_detection(self, classifier, environmental_sample):
        """Test Land and Environment Court detection."""
        result = classifier.classify(environmental_sample)

        assert result.court_info is not None
        assert result.court_info.code == 'NSWLEC'
        assert result.court_info.domain_hint == 'Environment'


class TestIntellectualPropertyLawClassification:
    """Test Intellectual Property Law domain classification."""

    def test_ip_domain_detection(self, classifier, intellectual_property_sample):
        """Test detection of IP Law domain."""
        result = classifier.classify(intellectual_property_sample)

        assert result.primary_domain in ['IP', 'Intellectual Property', 'IntellectualProperty']

    def test_copyright_act_extraction(self, classifier, intellectual_property_sample):
        """Test extraction of Copyright Act."""
        result = classifier.classify(intellectual_property_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Copyright Act' in name for name in leg_names)


class TestTortsLawClassification:
    """Test Torts Law domain classification."""

    def test_torts_domain_detection(self, classifier, torts_sample):
        """Test detection of Torts Law domain."""
        result = classifier.classify(torts_sample)

        assert result.primary_domain in ['Torts', 'Tort']

    def test_civil_liability_act_extraction(self, classifier, torts_sample):
        """Test extraction of Civil Liability Act."""
        result = classifier.classify(torts_sample)

        leg_names = [ref.name for ref in result.legislation_refs]
        assert any('Civil Liability Act' in name for name in leg_names)


# ============================================================================
# COMPREHENSIVE COVERAGE VALIDATION
# ============================================================================

class TestDomainCoverageCompleteness:
    """Validate comprehensive domain coverage."""

    def test_all_major_domains_covered(self, classifier):
        """Test that all major Australian legal domains are covered."""
        # Check that classification map includes all major domains
        from src.ingestion.classification_config import DOMAIN_MAPPING

        # Major domains that should be present
        expected_domains = [
            'Criminal',
            'Family',
            'Employment',
            'Administrative',
            'Commercial',
            'Property',
            'Constitutional',
            'Torts',
        ]

        # Check each expected domain exists in mapping
        for domain in expected_domains:
            assert domain in DOMAIN_MAPPING, f"Missing domain: {domain}"

    def test_no_unclassified_for_clear_samples(self, classifier,
                                                 employment_sample,
                                                 criminal_sample,
                                                 family_sample):
        """Test that clear domain samples don't result in Unclassified."""
        samples = [employment_sample, criminal_sample, family_sample]

        for sample in samples:
            result = classifier.classify(sample)
            assert result.primary_domain != 'Unclassified', \
                f"Sample {sample['id']} incorrectly classified as Unclassified"

    def test_confidence_scores_reasonable(self, classifier,
                                          employment_sample,
                                          criminal_sample,
                                          family_sample):
        """Test that confidence scores are in reasonable ranges."""
        samples = [employment_sample, criminal_sample, family_sample]

        for sample in samples:
            result = classifier.classify(sample)

            # Confidence should be between 0 and 1
            assert 0 <= result.primary_confidence <= 1, \
                f"Confidence out of range for {sample['id']}"

            # For clear domain samples, confidence should be > 0.2
            assert result.primary_confidence > 0.2, \
                f"Low confidence for clear sample {sample['id']}"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
