#!/usr/bin/env python3
"""Extract all tax keywords from domain knowledge file and compare with classification_config.py"""

import re
from pathlib import Path

def extract_keywords_from_domain_knowledge():
    """Extract all tax-related keywords from TAX_LAW_DOMAIN_KNOWLEDGE.md"""

    with open('TAX_LAW_DOMAIN_KNOWLEDGE.md', 'r', encoding='utf-8') as f:
        content = f.read()

    all_keywords = set()

    # Extract numbered keywords from section 6
    keywords_section = content[content.find('## 6. Classification Keywords'):content.find('## 7. Research and Analysis Framework')]
    for line in keywords_section.split('\n'):
        match = re.match(r'^\d+\.\s+(.+)$', line.strip())
        if match:
            keyword = match.group(1).strip()
            all_keywords.add(keyword.lower())

    # Extract legislation names and acts
    legislation_terms = [
        'itaa 1936', 'itaa 1997', 'income tax assessment act 1936', 'income tax assessment act 1997',
        'division 6', 'division 7a', 'division 8', 'division 40', 'division 115', 'division 328',
        'division 855', 'division 293', 'section 8-1', 's 8-1', 's 6-5', 's 6-10',
        'gst act', 'goods and services tax act 1999', 'a new tax system',
        'fringe benefits tax assessment act', 'fbtaa', 'taxation administration act', 'taa',
        'superannuation industry supervision act', 'sis act', 'superannuation guarantee administration act',
        'petroleum resource rent tax', 'prrt', 'excise act', 'customs act', 'tax agent services act',
        'duties act', 'land tax management act', 'payroll tax act', 'taxation ruling', 'tr',
        'gstr', 'td', 'taxation determination', 'pcg', 'practical compliance guideline',
        'ps la', 'law administration practice statement', 'ps ga', 'general administration practice statement',
        'taxpayer alert', 'ta', 'class ruling', 'product ruling', 'legislative instrument'
    ]

    # Tax administration and processes
    admin_terms = [
        'payg', 'pay as you go', 'payg withholding', 'payg instalment',
        'general interest charge', 'gic', 'shortfall interest charge', 'sic',
        'objection', 'appeal', 'amended assessment', 'self-assessment',
        'private ruling', 'public ruling', 'oral ruling', 'written advice',
        'advance pricing arrangement', 'apa', 'assessment', 'notice of assessment',
        'tax return', 'tax file number', 'tfn', 'australian business number', 'abn',
        'audit', 'record-keeping', 'substantiation', 'penalty', 'administrative penalty',
        'failure to lodge', 'garnishee', 'recovery', 'collection', 'lodgement fee',
        'objection decision', 'merit review', 'judicial review', 'special leave',
        'burden of proof', 'onus of proof', 'discovery', 'expert evidence',
        'contemporaneous documentation', 'alternative dispute resolution', 'adr',
        'settlement', 'mediation', 'test case', 'binding authority', 'persuasive authority',
        'tax agent', 'tax practitioners board', 'tpb', 'code of professional conduct',
        'legal professional privilege', 'conflict of interest', 'professional indemnity',
        'engagement letter', 'quality review', 'peer review', 'risk management',
        'client communication', 'file documentation', 'continuing professional education', 'cpe'
    ]

    # Income tax concepts
    income_tax_terms = [
        'assessable income', 'ordinary income', 'statutory income', 'exempt income',
        'taxable income', 'gross income', 'net income', 'derivation', 'accruals basis',
        'cash basis', 'source of income', 'australian source', 'foreign source',
        'capital vs revenue', 'revenue vs capital', 'deduction', 'allowable deduction',
        'general deduction', 'specific deduction', 'nexus test', 'negative limb',
        'capital expenditure', 'revenue expenditure', 'prepayment', 'economic performance',
        'negative gearing', 'work-related expense', 'home office', 'travel expense',
        'self-education expense', 'car expense', 'clothing expense', 'laundry expense',
        'depreciation', 'capital allowance', 'diminishing value', 'prime cost',
        'effective life', 'tax offset', 'rebate', 'franking credit', 'imputation credit',
        'franked dividend', 'unfranked dividend', 'gross-up', 'dividend imputation',
        'franking account', 'franking deficit', 'streaming', 'benchmark rule',
        'medicare levy', 'medicare levy surcharge', 'lmito', 'low and middle income tax offset',
        'sapto', 'senior australians tax offset', 'pensioners tax offset',
        'tax-free threshold', 'marginal tax rate', 'effective tax rate', 'average tax rate',
        'progressive taxation', 'tax bracket', 'tax scale', 'tax rates',
        'personal services income', 'psi', 'psi rules', 'personal services business',
        'results test', 'unrelated clients test', 'employment test', '80% rule',
        'income splitting', 'alienation of income', 'assignment of income',
        'employment income', 'salary', 'wages', 'allowance', 'bonus', 'commission',
        'business income', 'professional income', 'trading income',
        'investment income', 'interest income', 'dividend income', 'rental income',
        'royalty income', 'trust income', 'partnership income', 'estate income'
    ]

    # Company and trust taxation
    entity_tax_terms = [
        'company tax', 'corporate tax', 'company tax rate', 'base rate entity',
        'base rate entity passive income', 'small business entity', 'sbe',
        'aggregated turnover', 'turnover threshold', 'connected entity', 'affiliate',
        'consolidation', 'tax consolidated group', 'tax consolidation', 'head company',
        'subsidiary member', 'single entity rule', 'entry history rule', 'exit history rule',
        'allocable cost amount', 'aca', 'joining entity', 'leaving entity',
        'loss carry-forward', 'carry-forward loss', 'loss carry-back', 'carry-back loss',
        'continuity of ownership test', 'cot', 'same business test', 'sbt',
        'similar business test', 'business continuity test', 'recoupment',
        'research and development', 'r&d', 'r&d tax incentive', 'r&d tax offset',
        'r&d entity', 'core r&d activity', 'supporting r&d activity',
        'trust taxation', 'trust income', 'trust loss', 'discretionary trust',
        'unit trust', 'fixed trust', 'testamentary trust', 'family trust',
        'present entitlement', 'presently entitled', 'beneficiary',
        'default beneficiary', 'income beneficiary', 'capital beneficiary',
        'trustee', 'appointor', 'vesting date', 'trust distribution',
        'streaming', 'specific entitlement', 'proportionate approach',
        'family trust election', 'fte', 'interposed entity election', 'iee',
        'family group', 'conferral of present entitlement', 'division 6',
        'division 6e', 'trust estate', 'net income of trust',
        'partnership', 'partnership taxation', 'flow-through', 'flow-through treatment',
        'partner', 'partnership agreement', 'joint venture', 'limited partnership',
        'professional partnership', 'allocation of income', 'allocation of losses',
        'sole trader', 'sole proprietor', 'individual taxpayer'
    ]

    # CGT terms
    cgt_terms = [
        'capital gains tax', 'cgt', 'capital gain', 'capital loss', 'net capital gain',
        'net capital loss', 'cgt event', 'cgt asset', 'disposal', 'acquisition',
        'cost base', 'reduced cost base', 'capital proceeds', 'market value',
        'market valuation', 'acquisition date', 'disposal date', 'contract date',
        'cgt discount', '50% discount', '50 percent discount', 'discount method',
        'indexation', 'indexation method', 'indexed cost base', 'cpi', 'consumer price index',
        'discount capital gain', 'discounted capital gain', '12-month holding period',
        'main residence', 'main residence exemption', 'principal place of residence',
        'ppor', 'dwelling', 'adjacent land', 'two hectares', 'absence rule',
        'six-year rule', 'six year rule', 'absence from main residence',
        'pre-cgt asset', 'pre-cgt', 'pre-20 september 1985', 'pre-1985 asset',
        'collectable', 'personal use asset', 'valour decoration', 'listed personal-use asset',
        'car exemption', 'motorcycle exemption', '$10,000 threshold',
        'small business cgt concession', 'small business concession', '$6 million test',
        'net asset value test', 'maximum net asset value', 'connected entity',
        'affiliate', 'cgt concession stakeholder', 'significant individual',
        'active asset', 'active asset test', '50% active asset reduction',
        '15-year exemption', '15 year exemption', 'retirement exemption',
        '$500,000 cap', '$500,000 lifetime limit', 'rollover', 'rollover relief',
        'replacement asset rollover', 'scrip for scrip', 'merger rollover',
        'demerger rollover', 'marriage breakdown rollover', 'small business rollover',
        'cgt event a1', 'cgt event b1', 'cgt event c1', 'cgt event c2',
        'cgt event d1', 'cgt event e1', 'cgt event e2', 'cgt event e5',
        'cgt event e8', 'cgt event h2', 'cgt event k6', 'cgt event j1',
        'look-through earnout right', 'earnout arrangement', 'value shifting',
        'indirect value shift', 'direct value shift', 'loss duplication',
        'wash sale', 'artificial loss', 'capital loss denial'
    ]

    # GST terms
    gst_terms = [
        'gst', 'goods and services tax', 'taxable supply', 'input tax credit',
        'itc', 'creditable acquisition', 'creditable purpose', 'creditable importation',
        'gst-free', 'gst-free supply', 'input-taxed', 'input-taxed supply',
        'tax invoice', 'recipient created tax invoice', 'rcti', 'adjustment note',
        'bas', 'business activity statement', 'activity statement', 'gst return',
        'tax period', 'monthly', 'quarterly', 'annual', 'gst registration',
        'registration threshold', '$75,000 threshold', '$150,000 threshold',
        'gst turnover', 'current gst turnover', 'projected gst turnover',
        'enterprise', 'carrying on enterprise', 'activity done in enterprise',
        'consideration', 'supply', 'supply for consideration', 'connected with australia',
        'australia', 'indirect tax zone', 'supply made in australia',
        'adjustment', 'increasing adjustment', 'decreasing adjustment', 'adjustment event',
        'change in consideration', 'change in creditable purpose', 'bad debt',
        'bad debt adjustment', 'adjustment period', 'margin scheme', 'margin',
        'taxable supply of real property', 'property development', 'going concern',
        'going concern exemption', 'sale of going concern', 'financial supply',
        'financial service', 'lending', 'equity interest', 'borrowing',
        'residential premises', 'residential rent', 'residential accommodation',
        'commercial residential premises', 'hotel', 'motel', 'serviced apartment',
        'reverse charge', 'offshore supply', 'recipient created tax invoice',
        'gst group', 'gst grouping', 'representative member', 'gst joint venture',
        'gst branch', 'branch registration', 'reduced credit acquisition',
        'reduced input tax credit', 'non-deductible expense', 'entertainment',
        'basic food', 'gst-free food', 'health service', 'medical service',
        'education course', 'course material', 'childcare', 'childcare service',
        'religious service', 'charity', 'charitable institution', 'gift-deductible entity',
        'export', 'international transport', 'water supply', 'sewerage', 'drainage',
        'precious metal', 'second-hand goods', 'second-hand goods dealer',
        'tourism', 'tour', 'travel agent', 'inbound intangible consumer supply',
        'low value imported goods', 'lvig'
    ]

    # FBT terms
    fbt_terms = [
        'fringe benefits tax', 'fbt', 'fringe benefit', 'taxable value',
        'grossed-up taxable value', 'grossed-up value', 'gross-up factor',
        'type 1 benefit', 'type 1 grossed-up', 'type 2 benefit', 'type 2 grossed-up',
        'type 1 aggregate', 'type 2 aggregate', 'fbt rate', '47%', 'fbt year',
        '1 april', '31 march', 'employer', 'employee', 'current employee',
        'former employee', 'future employee', 'associate', 'relative',
        'car benefit', 'car fringe benefit', 'statutory formula method',
        'operating cost method', 'base value', 'statutory fraction',
        'days available', 'private use', 'logbook', 'odometer',
        'car parking benefit', 'car parking fringe benefit', 'commercial parking station',
        'lowest daily fee', '$10.26 threshold', 'small business car parking exemption',
        'loan benefit', 'loan fringe benefit', 'benchmark interest rate',
        'statutory interest rate', 'notional interest', 'interest-free loan',
        'expense payment benefit', 'expense payment fringe benefit',
        'reimbursement', 'payment of expense', 'third party expense',
        'housing benefit', 'housing fringe benefit', 'accommodation',
        'rental value', 'market value rent', 'subsidised rent',
        'living-away-from-home allowance', 'lafha', 'living away from home',
        'temporary accommodation', 'fly-in fly-out', 'fifo', 'drive-in drive-out', 'dido',
        'meal entertainment', 'entertainment benefit', 'entertainment fringe benefit',
        '50/50 split method', '12-week register', 'actual method',
        'tax-exempt body entertainment', 'minor benefit', 'minor benefit exemption',
        '$300 threshold', 'less than $300', 'infrequent', 'irregular', 'unreasonable',
        'otherwise deductible rule', 'odr', 'hypothetical deduction',
        'employee contribution', 'recipient contribution', 'reduction in taxable value',
        'reportable fringe benefit', 'reportable fringe benefits amount', 'rfba',
        'excluded fringe benefit', 'exempt benefit', 'exempt fringe benefit',
        'work-related item', 'portable electronic device', 'laptop', 'mobile phone',
        'protective clothing', 'briefcase', 'tool of trade', 'item of clothing',
        'public benevolent institution', 'pbi', 'health promotion charity',
        'religious institution', 'registered charity', 'tax concession charity',
        'salary sacrifice', 'salary packaging', 'salary sacrifice arrangement',
        'effective salary packaging', 'novated lease', 'employee share scheme',
        'ess', 'share scheme', 'option scheme', 'deferred start date', 'cessation time',
        'airline transport benefit', 'standby airline travel', 'residual benefit',
        'residual fringe benefit', 'property benefit', 'property fringe benefit'
    ]

    # Superannuation terms
    super_terms = [
        'superannuation', 'super', 'superannuation fund', 'complying fund',
        'non-complying fund', 'regulated fund', 'self-managed super fund',
        'smsf', 'small apra fund', 'large apra fund', 'public offer fund',
        'superannuation guarantee', 'sg', 'sg charge', 'sg percentage', '11%', '11.5%', '12%',
        'ordinary time earnings', 'ote', 'salary and wages', 'employer contribution',
        'mandatory contribution', 'choice of fund', 'default fund', 'stapled fund',
        'concessional contribution', 'non-concessional contribution', 'personal contribution',
        'salary sacrifice contribution', 'member contribution', 'employer contribution',
        'contribution cap', 'concessional cap', '$30,000 cap', '$27,500 cap',
        'non-concessional cap', '$120,000 cap', '$110,000 cap', 'bring-forward rule',
        'bring-forward period', 'carry-forward concessional', 'unused concessional cap',
        'carry-forward provision', '5-year carry-forward', 'total superannuation balance',
        'tsb', '$500,000 threshold', 'excess contribution', 'excess concessional contribution',
        'excess non-concessional contribution', 'excess contributions tax', 'ect',
        'excess contributions determination', 'release authority', 'withdraw and recontribute',
        'division 293 tax', 'additional 15%', 'high income earner', '$250,000 threshold',
        'adjusted taxable income', 'income for surcharge purposes', 'reportable super contribution',
        'contribution splitting', 'split contribution', 'spouse contribution',
        'spouse contribution offset', 'low income spouse', 'government co-contribution',
        'co-contribution', 'eligible contribution', 'matching contribution',
        'preservation', 'preserved benefit', 'preservation age', 'age 60', 'age 65',
        'condition of release', 'unrestricted non-preserved', 'restricted non-preserved',
        'retirement', 'permanent incapacity', 'temporary incapacity', 'terminal medical condition',
        'severe financial hardship', 'compassionate grounds', 'first home super saver',
        'fhss', 'fhsss scheme', 'illegal early release', 'early access scheme',
        'tax-free component', 'taxable component', 'taxed element', 'untaxed element',
        'crystallised', 'tax-free proportion', 'taxable proportion',
        'lump sum', 'lump sum payment', 'lump sum tax', 'under preservation age',
        'between preservation age and 60', 'age 60 and over', 'tax-free after 60',
        'pension', 'superannuation pension', 'account-based pension', 'allocated pension',
        'transition to retirement', 'ttr', 'ttr pension', 'non-commutable pension',
        'capped defined benefit', 'uncapped defined benefit', 'lifetime pension',
        'market-linked pension', 'minimum drawdown', 'pension standards', 'reversionary pension',
        'death benefit', 'death benefit dependant', 'death benefit nomination',
        'binding death benefit nomination', 'non-binding nomination', 'reversionary beneficiary',
        'tax on death benefits', 'non-dependant', 'child under 18', 'financial dependant',
        'interdependency relationship', 'transfer balance cap', 'tbc', '$1.9 million',
        'general transfer balance cap', 'personal transfer balance cap', 'ptbc',
        'transfer balance account', 'tba', 'credit', 'debit', 'excess transfer balance',
        'excess transfer balance tax', 'commutation authority', 'notional earnings',
        'pension phase', 'retirement phase', 'accumulation phase', 'growth phase',
        'contribution phase', 'fund earnings', 'exempt current pension income', 'ecpi',
        '15% tax on earnings', '10% tax on capital gains', 'zero tax in pension phase',
        '15% contributions tax', '30% contributions tax', 'actuarial certificate',
        'segregated assets', 'unsegregated assets', 'proportionate method',
        'sole purpose test', 'compliance test', 'in-house asset', 'in-house asset rule',
        '5% limit', 'related party', 'related trust', 'investment strategy',
        'diversification', 'liquidity', 'insurance in super', 'life insurance',
        'total and permanent disability', 'tpd', 'income protection', 'death cover',
        'trustee', 'individual trustee', 'corporate trustee', 'trustee duty',
        'covenants', 'operating standards', 'annual return', 'smsf annual return',
        'audit', 'approved auditor', 'audit report', 'contravention report',
        'actuarial certificate', 'actuarial valuation', 'actuary',
        'disqualified person', 'disqualified trustee', 'automatic disqualification',
        'notice of intent', 'personal contribution deduction', 'claiming deduction',
        'downsizer contribution', '$300,000 downsizer', 'eligible dwelling',
        'small business cgt rollover', 'capital gains exempt amount',
        'personal injury payment', 'structured settlement', 'anti-detriment payment'
    ]

    # State tax terms
    state_tax_terms = [
        'payroll tax', 'payroll tax act', 'payroll tax threshold', 'wages',
        'payroll tax wages', 'deemed wages', 'taxable wages', 'exempt wages',
        'contractor', 'deemed employee', 'contractor provision', 'services contract',
        'labour hire', 'on-hire', 'relevant contract', 'grouping', 'group employer',
        'designated group employer', 'dge', 'common control', 'tracing', 'use and control',
        'interstate wages', 'interstate allocation', 'apportionment', 'principal place',
        'allowance', 'bonus', 'commission', 'superannuation contribution',
        'shares', 'share scheme', 'fringe benefit', 'director fee', 'redundancy',
        'termination payment', 'annual leave', 'long service leave', 'parental leave',
        'land tax', 'land tax act', 'land tax threshold', 'taxable land', 'taxable value',
        'site value', 'improved value', 'unimproved value', 'principal place of residence',
        'ppor exemption', 'home exemption', 'primary production', 'primary production exemption',
        'farming land', 'agricultural land', 'rural land', 'charitable exemption',
        'retirement village', 'aged care facility', 'nursing home', 'caravan park',
        'boarding house', 'rooming house', 'absentee owner', 'foreign owner',
        'absentee owner surcharge', 'foreign owner surcharge', 'vacant land tax',
        'vacant residential land', 'trust surcharge', 'discretionary trust surcharge',
        'fixed trust exemption', 'aggregation', 'aggregate landholdings',
        'stamp duty', 'duties act', 'transfer duty', 'ad valorem duty', 'dutiable value',
        'dutiable transaction', 'dutiable property', 'real property', 'chattel',
        'business property', 'goodwill', 'chose in action', 'partnership interest',
        'intellectual property', 'motor vehicle', 'vehicle duty', 'registration duty',
        'consideration', 'market value', 'unencumbered value', 'highest value',
        'first home buyer', 'first home buyer concession', 'first home buyer exemption',
        'fhog', 'first home owner grant', 'owner occupier', 'principal place of residence',
        'off-the-plan', 'off-the-plan concession', 'vacant land', 'new home',
        'established home', 'substantially renovated', 'substantial renovation',
        'family transfer', 'relationship breakdown', 'deceased estate', 'transmission',
        'survivorship', 'joint tenant', 'tenant in common', 'nomination',
        'corporate reconstruction', 'corporate consolidation', 'corporate restructure',
        'relief', 'exemption', 'concession', 'reduction', 'deferral',
        'landholder', 'landholder duty', 'land-rich', 'land-rich entity',
        'landholding', 'substantial interest', '50% interest', 'acquisition of interest',
        'relevant acquisition', 'related acquisition', 'associated person',
        'foreign person', 'foreign purchaser', 'foreign purchaser duty',
        'foreign purchaser additional duty', 'fpd', 'fpad', 'surcharge purchaser duty',
        'premium property', 'premium property duty', 'luxury home', 'high-value property',
        'parking space levy', 'psl', 'parking bay', 'cbd parking', 'off-street parking',
        'insurance duty', 'fire services levy', 'fsl', 'emergency services levy', 'esl',
        'motor vehicle duty', 'vehicle registration', 'transfer of registration',
        'registration fee', 'vehicle licence', 'chief commissioner', 'state revenue',
        'chief commissioner of state revenue', 'commissioner of state revenue',
        'revenue nsw', 'revenue office', 'state taxation office', 'sro victoria',
        'office of state revenue', 'revenue ruling', 'practice direction',
        'revenue guidelines', 'private ruling', 'public ruling'
    ]

    # International tax terms
    international_tax_terms = [
        'international tax', 'cross-border', 'cross-border transaction', 'offshore',
        'tax residency', 'resident', 'non-resident', 'temporary resident',
        'resides test', 'ordinary residence', 'domicile', 'domicile test',
        '183-day test', 'six-month test', 'superannuation test', 'commonwealth superannuation',
        'company residency', 'incorporation test', 'central management and control',
        'central management and control test', 'voting power test', 'place of incorporation',
        'trust residency', 'central management', 'resident trust estate',
        'foreign income', 'foreign-source income', 'worldwide income', 'australian-source income',
        'source of income', 'source rules', 'active income', 'passive income',
        'foreign tax offset', 'fito', 'foreign income tax offset', 'foreign tax credit',
        'tax credit', 'foreign tax paid', 'double taxation', 'double taxation relief',
        'double tax agreement', 'dta', 'tax treaty', 'bilateral treaty',
        'multilateral instrument', 'mli', 'beps mli', 'covered tax agreement',
        'treaty relief', 'treaty benefit', 'limitation on benefits', 'lob',
        'principal purpose test', 'ppt', 'treaty shopping', 'conduit', 'treaty residence',
        'tie-breaker', 'tie-breaker rule', 'dual residency', 'casting vote',
        'permanent establishment', 'pe', 'fixed place pe', 'dependent agent pe',
        'building site', 'construction site', 'installation project', 'supervisory activity',
        'business profits', 'business profits article', 'attributable profits',
        'withholding tax', 'wht', 'dividend withholding', 'interest withholding',
        'royalty withholding', 'unfranked dividend wht', 'treaty rate', 'domestic rate',
        'reduced withholding rate', 'exemption from withholding', 'final withholding tax',
        'controlled foreign company', 'cfc', 'cfc rules', 'attributable income',
        'cfc attribution', 'eligible designated concession income', 'tainted income',
        'tainted sales income', 'tainted services income', 'passive cfc income',
        'active business income', 'active foreign business income', 'active income test',
        'transferor trust', 'non-resident trust', 'transferor', 'deemed present entitlement',
        'attribution percentage', 'attributable taxpayer', 'anti-avoidance provision',
        'transfer pricing', 'tp', 'arm\'s length', 'arm\'s length principle',
        'arm\'s length condition', 'subdivision 815-a', 'subdivision 815-b',
        'subdivision 815-c', 'subdivision 815-d', 'reconstruction', 'actual conditions',
        'comparable uncontrolled price', 'cup', 'resale price method', 'rpm',
        'cost plus method', 'cpm', 'transactional net margin method', 'tnmm',
        'profit split method', 'psm', 'comparable transaction', 'comparable company',
        'functional analysis', 'comparability analysis', 'economic analysis',
        'related party', 'associated enterprise', 'related party transaction',
        'intra-group transaction', 'intercompany pricing', 'royalty', 'management fee',
        'service fee', 'interest charge', 'guarantee fee', 'financing arrangement',
        'advance pricing arrangement', 'apa', 'unilateral apa', 'bilateral apa',
        'multilateral apa', 'rollback', 'renewal', 'critical assumption',
        'transfer pricing documentation', 'master file', 'local file',
        'country-by-country report', 'cbcr', 'cbc reporting', 'significant global entity',
        'sge', '$1 billion threshold', 'global parent entity', 'constituent entity',
        'thin capitalisation', 'thin cap', 'debt deduction creation rule',
        'safe harbour debt amount', 'shda', 'arm\'s length debt amount', 'alda',
        'worldwide gearing debt amount', 'wgda', 'on-lend', 'associate entity',
        'debt deduction', 'disallowed deduction', 'adjusted average debt',
        'average equity capital', 'safe harbour test', 'arm\'s length debt test',
        'worldwide gearing test', 'de minimis', '$2 million threshold',
        'inward investing entity', 'inward investment vehicle', 'outward investing entity',
        'financial entity', 'authorised deposit-taking institution', 'adi',
        'securitisation vehicle', 'investment body', 'operative entity',
        'diverted profits tax', 'dpt', 'multinational anti-avoidance law', 'maal',
        '40% tax rate', 'diverted profits', 'tax mismatch', 'foreign tax paid',
        'scheme', 'principal purpose', 'principal purpose test', 'significant global entity',
        'global revenue', '$1 billion', 'australian tax avoidance', 'diversion of profits',
        'profit allocation', 'profit shifting', 'base erosion', 'beps',
        'base erosion and profit shifting', 'action plan', 'oecd beps', 'g20 beps',
        'pillar one', 'pillar two', 'amount a', 'amount b', 'nexus', 'profit allocation',
        'digital services tax', 'dst', 'digital economy', 'remote supply',
        'global minimum tax', 'gmt', 'minimum tax rate', '15% minimum', 'globe rules',
        'income inclusion rule', 'iir', 'undertaxed profits rule', 'utpr',
        'qualified domestic minimum top-up tax', 'qdmtt', 'top-up tax',
        'mutual agreement procedure', 'map', 'competent authority', 'dispute resolution',
        'mandatory binding arbitration', 'exchange of information', 'eoi',
        'automatic exchange', 'common reporting standard', 'crs', 'fatca',
        'foreign account tax compliance act', 'us person', 'reportable account'
    ]

    # Anti-avoidance terms
    anti_avoidance_terms = [
        'part iva', 'part 4a', 'general anti-avoidance', 'general anti-avoidance rule', 'gaar',
        'tax avoidance', 'tax minimisation', 'tax planning', 'aggressive tax planning',
        'tax evasion', 'evasion', 'fraud', 'false statement', 'concealment',
        'scheme', 'arrangement', 'plan', 'course of action', 'tax benefit',
        'tax detriment', 'reduction in tax', 'increase in loss', 'deferral',
        'dominant purpose', 'sole or dominant purpose', 'more than incidental purpose',
        'predication test', 'would conclude', 'reasonable person', 'objective test',
        'subjective test', 'purpose or effect', '8 factors', 'manner of entry',
        'form and substance', 'duration', 'timing', 'expected tax benefit',
        'financial position', 'other consequences', 'nature of connection',
        'commissioner determination', 'cancel tax benefit', 'compensating adjustment',
        'promoter penalty', 'promoter penalty law', 'tax exploitation scheme',
        'significant global entity', 'significant tax benefit', 'scheme promoter',
        'scheme entity', 'facilitated', 'marketed', 'implemented', 'encouraged',
        'base penalty amount', 'penalty percentage', 'promoter penalty amount',
        'division 7a', 'div 7a', 'deemed dividend', 'private company',
        'payment', 'loan', 'debt forgiveness', 'shareholder', 'associate of shareholder',
        'trust beneficiary', 'minimum yearly repayment', 'complying loan',
        'loan agreement', 'benchmark interest rate', '7-year loan', '25-year loan',
        'amalgamated loan', 'unpaid present entitlement', 'upe',
        'sub-trust arrangement', 'interposed entity', 'loan back',
        'specific anti-avoidance', 'specific anti-avoidance rule', 'saar',
        'value shifting', 'indirect value shift', 'ivs', 'direct value shift', 'dvs',
        'realisation time method', 'adjustable value method', 'affected interest',
        'down interest', 'up interest', 'active participant', 'market value',
        'diminution in value', 'increase in value', 'indirect equity interest',
        'loss duplication', 'loss duplication rule', 'asset rollover',
        'pre-cgt status', 'original asset', 'replacement asset',
        'wash sale', 'artificial loss', 'capital loss denial', 'matched position',
        'hedging transaction', 'offsetting position', 'tax shelter',
        'phoenix activity', 'phoenixing', 'illegal phoenixing', 'creditor defeating',
        'director penalty notice', 'dpn', 'personal liability', 'lock-down',
        'non-remittable', 'estimate assessment', 'security deposit',
        'transfer asset', 'alienate asset', 'recovery', 'collection proceedings',
        'westrader principle', 'economic substance', 'substance over form',
        'beneficial ownership', 'beneficial owner', 'legal owner', 'nominee',
        'sham', 'sham transaction', 'sham doctrine', 'pretence', 'make-believe',
        'fiscal nullity', 'self-cancelling', 'circular', 'round-robin',
        'reasonably arguable', 'reasonably arguable position', 'rap',
        'shortfall penalty', 'false or misleading statement', 'lack of reasonable care',
        'recklessness', 'intentional disregard', 'voluntary disclosure',
        'safe harbour', 'penalty reduction', 'reasonable care defence'
    ]

    # Court and procedure terms
    court_procedure_terms = [
        'administrative appeals tribunal', 'aat', 'taxation division', 'small taxation claims',
        'merit review', 'tribunal', 'federal court', 'federal court of australia',
        'full federal court', 'full court', 'high court', 'high court of australia',
        'supreme court', 'state supreme court', 'ncat', 'vcat', 'qcat', 'sacat',
        'civil and administrative tribunal', 'revenue tribunal', 'state revenue tribunal',
        'jurisdiction', 'original jurisdiction', 'appellate jurisdiction',
        'subject matter jurisdiction', 'accrued jurisdiction', 'associated jurisdiction',
        'appeal', 'appeal on question of law', 'question of law', 'question of fact',
        'mixed question', 'leave to appeal', 'special leave', 'special leave application',
        'notice of appeal', 'grounds of appeal', 'appellate review', 'fresh evidence',
        'judicial review', 'constitutional writ', 'mandamus', 'prohibition', 'certiorari',
        'jurisdictional error', 'error of law', 'wednesbury unreasonableness',
        'natural justice', 'procedural fairness', 'hearing rule', 'bias rule',
        'standing', 'locus standi', 'party', 'applicant', 'respondent', 'appellant',
        'notice of objection', 'objection decision', '60 days', 'time limit',
        'extension of time', 'out of time', 'condonation', 'special circumstances',
        'burden of proof', 'onus of proof', 'evidentiary onus', 'legal burden',
        'standard of proof', 'balance of probabilities', 'beyond reasonable doubt',
        'presumption', 'rebuttable presumption', 'evidential presumption',
        'discovery', 'disclosure', 'interrogatories', 'inspection', 'list of documents',
        'privilege', 'legal professional privilege', 'without prejudice', 'settlement privilege',
        'litigation privilege', 'common interest privilege', 'public interest immunity',
        'evidence', 'admissible evidence', 'relevant evidence', 'hearsay', 'opinion evidence',
        'expert evidence', 'expert witness', 'expert report', 'concurrent evidence',
        'hot tub', 'factual witness', 'witness statement', 'affidavit', 'statutory declaration',
        'subpoena', 'notice to produce', 'summons', 'pleading', 'statement of claim',
        'defence', 'reply', 'particulars', 'amended pleading', 'strike out',
        'summary judgment', 'default judgment', 'interlocutory application',
        'case management', 'directions hearing', 'programming', 'timetable',
        'practice note', 'practice note tax 1', 'federal court rules', 'tribunal rules',
        'alternative dispute resolution', 'adr', 'mediation', 'conciliation',
        'neutral evaluation', 'settlement conference', 'without prejudice meeting',
        'settlement', 'compromise', 'consent order', 'terms of settlement',
        'deed of release', 'confidentiality', 'litigation funding', 'security for costs',
        'costs', 'party and party costs', 'solicitor and client costs', 'indemnity costs',
        'costs order', 'costs assessment', 'costs taxing', 'costs agreement',
        'test case', 'friendly litigation', 'lead case', 'representative proceeding',
        'class action', 'binding precedent', 'stare decisis', 'ratio decidendi',
        'obiter dictum', 'persuasive authority', 'judicial comity', 'disapprove',
        'overrule', 'distinguish', 'follow', 'apply', 'refuse to follow',
        'judgment', 'reasons for judgment', 'reserved judgment', 'extempore judgment',
        'orders', 'declaratory relief', 'injunction', 'stay', 'interlocutory injunction',
        'contemporaneous documentation', 'record-keeping', 'documentary evidence',
        'business records', 'tax records', '5 years', 'retention period'
    ]

    # Recent developments and emerging issues
    emerging_terms = [
        'crypto-asset', 'cryptocurrency', 'bitcoin', 'ethereum', 'digital currency',
        'virtual currency', 'nft', 'non-fungible token', 'digital asset',
        'blockchain', 'distributed ledger', 'decentralised finance', 'defi',
        'crypto exchange', 'crypto wallet', 'private key', 'mining',
        'staking', 'crypto staking', 'yield farming', 'airdrops', 'hard fork',
        'gig economy', 'platform economy', 'sharing economy', 'on-demand economy',
        'uber', 'deliveroo', 'airtasker', 'service provider', 'platform worker',
        'independent contractor', 'employee vs contractor', 'employment status',
        'remote work', 'work from home', 'wfh', 'telecommuting', 'cross-border employment',
        'remote worker', 'digital nomad', 'international remote work',
        'esg', 'environmental social governance', 'carbon credit', 'carbon tax',
        'emissions trading', 'renewable energy', 'clean energy', 'sustainability',
        'climate change', 'net zero', 'carbon neutral', 'stage 3 tax cuts',
        'tax cuts', 'tax reform', 'personal tax rates', 'bracket creep',
        'shadow economy', 'cash economy', 'black economy', 'undeclared income',
        'hidden economy', 'underground economy', 'tax gap', 'compliance gap',
        'illegal early release', 'early access', 'covid early release',
        'hardship release', 'compassionate release', 'work test exemption',
        'work test', 'contributions work test', '$300,000 downsizer',
        'royal commission', 'banking royal commission', 'hayne royal commission',
        'aged care royal commission', 'robodebt', 'scheme debt', 'income averaging',
        'automated debt raising', 'corporate collective investment vehicle', 'cciv',
        'attribution managed investment trust', 'amit', 'managed investment trust', 'mit',
        'sovereign immunity', 'foreign government', 'foreign sovereign',
        'patent box', 'intellectual property regime', 'ip regime',
        'loss carry-back', 'temporary loss carry-back', '2020-21', '2021-22',
        'instant asset write-off', 'temporary full expensing', 'tfe',
        'backing business investment', 'accelerated depreciation'
    ]

    # Legislative interpretation principles
    interpretation_terms = [
        'statutory interpretation', 'construction', 'literal approach', 'literal interpretation',
        'purposive approach', 'purposive interpretation', 'acts interpretation act',
        'interpretation act 1901', 'section 15aa', 'section 15ab', 'beneficial purpose',
        'mischief rule', 'golden rule', 'contextual approach', 'reading as a whole',
        'reading in context', 'extrinsic material', 'intrinsic material',
        'explanatory memorandum', 'em', 'second reading speech', 'hansard',
        'parliamentary debate', 'legislative history', 'amendment history',
        'parliamentary intent', 'legislative intent', 'policy', 'legislative policy',
        'ordinary meaning', 'technical meaning', 'legal meaning', 'trade meaning',
        'definition section', 'defined term', 'extended meaning', 'deeming provision',
        'exhaustive definition', 'inclusive definition', 'exclusive definition',
        'plain meaning', 'natural meaning', 'grammatical construction',
        'expressio unius', 'expressio unius est exclusio alterius',
        'ejusdem generis', 'noscitur a sociis', 'generalia specialibus non derogant',
        'presumption against retrospectivity', 'retrospective operation',
        'commencement', 'application provision', 'transitional provision',
        'savings provision', 'grandfathering', 'grandfather clause'
    ]

    # Combine all terms
    all_keywords.update([t.lower() for t in legislation_terms])
    all_keywords.update([t.lower() for t in admin_terms])
    all_keywords.update([t.lower() for t in income_tax_terms])
    all_keywords.update([t.lower() for t in entity_tax_terms])
    all_keywords.update([t.lower() for t in cgt_terms])
    all_keywords.update([t.lower() for t in gst_terms])
    all_keywords.update([t.lower() for t in fbt_terms])
    all_keywords.update([t.lower() for t in super_terms])
    all_keywords.update([t.lower() for t in state_tax_terms])
    all_keywords.update([t.lower() for t in international_tax_terms])
    all_keywords.update([t.lower() for t in anti_avoidance_terms])
    all_keywords.update([t.lower() for t in court_procedure_terms])
    all_keywords.update([t.lower() for t in emerging_terms])
    all_keywords.update([t.lower() for t in interpretation_terms])

    return all_keywords

def extract_existing_keywords():
    """Extract existing keywords from classification_config.py"""

    with open('src/ingestion/classification_config.py', 'r', encoding='utf-8') as f:
        content = f.read()

    existing = {
        'Tax_Income': set(),
        'Tax_CGT': set(),
        'Tax_GST': set(),
        'Tax_Corporate': set(),
        'Tax_FBT': set(),
        'Tax_State': set(),
        'Tax_Avoidance': set()
    }

    # Extract each category
    for category in existing.keys():
        pattern = rf"'{category}':\s*\[(.*?)\]"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            keywords_text = match.group(1)
            # Extract quoted strings
            keywords = re.findall(r"'([^']+)'", keywords_text)
            existing[category] = set(k.lower() for k in keywords)

    return existing

def main():
    print("Extracting keywords from TAX_LAW_DOMAIN_KNOWLEDGE.md...")
    domain_keywords = extract_keywords_from_domain_knowledge()
    print(f"Found {len(domain_keywords)} unique keywords in domain knowledge file\n")

    print("Extracting existing keywords from classification_config.py...")
    existing_keywords = extract_existing_keywords()

    total_existing = sum(len(v) for v in existing_keywords.values())
    print(f"Found {total_existing} existing keywords across all Tax categories\n")

    # Combine all existing keywords
    all_existing = set()
    for keywords_set in existing_keywords.values():
        all_existing.update(keywords_set)

    # Find missing keywords
    missing = domain_keywords - all_existing

    print(f"\n{'='*80}")
    print(f"MISSING KEYWORDS: {len(missing)} keywords not in classification_config.py")
    print(f"{'='*80}\n")

    # Save to file for review
    with open('missing_tax_keywords.txt', 'w', encoding='utf-8') as f:
        f.write("MISSING TAX KEYWORDS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total missing: {len(missing)}\n\n")
        for i, kw in enumerate(sorted(missing), 1):
            f.write(f"{i}. {kw}\n")

    print("Analysis complete!")
    print(f"Missing keywords saved to: missing_tax_keywords.txt")
    print(f"\nSummary:")
    print(f"  Domain knowledge keywords: {len(domain_keywords)}")
    print(f"  Existing config keywords:  {total_existing}")
    print(f"  Missing keywords:          {len(missing)}")
    print(f"  Coverage:                  {(total_existing/len(domain_keywords)*100):.1f}%")

if __name__ == '__main__':
    main()
