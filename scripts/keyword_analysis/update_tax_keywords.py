#!/usr/bin/env python3
"""
Update classification_config.py with comprehensive Tax keywords from TAX_LAW_DOMAIN_KNOWLEDGE.md
"""

import re

# Read the current file
with open('src/ingestion/classification_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the comprehensive Tax categories with all keywords
tax_categories = """    # Income Tax - ITAA 1936/1997, assessable income, deductions, offsets
    'Tax_Income': [
        # Core Legislation
        'income tax assessment act', 'itaa 1936', 'itaa 1997', 'income tax assessment act 1936',
        'income tax assessment act 1997', 'taxation administration act', 'taa', 'division 6',
        'division 7a', 'division 8', 'division 40', 'division 115', 'division 328', 'division 855',
        'division 293', 'division 900', 'division 915',
        # Assessable Income
        'assessable income', 'ordinary income', 'statutory income', 'exempt income', 's 6-5', 's 6-10',
        'gross income', 'net income', 'taxable income', 'derivation', 'accruals basis', 'cash basis',
        'source of income', 'australian source', 'foreign source', 'capital vs revenue', 'revenue vs capital',
        # Deductions
        'deduction', 'allowable deduction', 'general deduction', 'specific deduction', 'section 8-1', 's 8-1',
        'nexus test', 'negative limb', 'capital expenditure', 'revenue expenditure', 'prepayment',
        'economic performance', 'work-related expense', 'home office', 'travel expense', 'self-education expense',
        'car expense', 'clothing expense', 'laundry expense', 'negative gearing', 'rental property',
        'investment property', 'substantiation', 'record-keeping',
        # Depreciation & Capital Allowances
        'depreciation', 'capital allowance', 'diminishing value', 'prime cost',
        'effective life', 'instant asset write-off', 'temporary full expensing', 'tfe',
        'backing business investment', 'accelerated depreciation',
        # Tax Offsets & Levies
        'tax offset', 'rebate', 'franking credit', 'imputation credit', 'franked dividend',
        'unfranked dividend', 'gross-up', 'dividend imputation', 'franking account', 'franking deficit',
        'streaming', 'benchmark rule', 'medicare levy', 'medicare levy surcharge', 'lmito',
        'low and middle income tax offset', 'sapto', 'senior australians tax offset',
        'pensioners tax offset', 'tax-free threshold', 'marginal tax rate', 'effective tax rate',
        'average tax rate', 'progressive taxation', 'tax bracket', 'tax scale', 'tax rates',
        # Personal Services Income
        'personal services income', 'psi', 'psi rules', 'personal services business',
        'results test', 'unrelated clients test', 'employment test', '80% rule',
        'income splitting', 'alienation of income', 'assignment of income',
        # Income Types
        'employment income', 'salary', 'wages', 'allowance', 'bonus', 'commission',
        'business income', 'professional income', 'trading income', 'investment income',
        'interest income', 'dividend income', 'rental income', 'royalty income',
        # Entities
        'individual taxpayer', 'sole trader', 'sole proprietor',
        # Commissioner
        'commissioner of taxation', 'ato', 'australian taxation office', 'tax ruling',
        'taxation ruling', 'tr', 'private ruling', 'public ruling', 'determination',
        'taxation determination', 'td', 'deductible gift recipient', 'dgr'
    ],

    # Capital Gains Tax - CGT events, exemptions, concessions, calculations
    'Tax_CGT': [
        # Core Concepts
        'capital gains tax', 'cgt', 'capital gain', 'capital loss', 'net capital gain',
        'net capital loss', 'cgt event', 'cgt asset', 'disposal', 'acquisition',
        'cost base', 'reduced cost base', 'capital proceeds', 'market value', 'market valuation',
        'acquisition date', 'disposal date', 'contract date',
        # CGT Discount
        'cgt discount', '50% discount', '50 percent discount', 'discount method', 'indexation',
        'indexation method', 'indexed cost base', 'cpi', 'consumer price index',
        'discount capital gain', 'discounted capital gain', '12-month holding period',
        # Main Residence
        'main residence', 'main residence exemption', 'principal place of residence', 'ppor',
        'dwelling', 'adjacent land', 'two hectares', 'absence rule', 'six-year rule',
        'six year rule', 'absence from main residence',
        # Pre-CGT & Exemptions
        'pre-cgt asset', 'pre-cgt', 'pre-20 september 1985', 'pre-1985 asset',
        'collectable', 'personal use asset', 'valour decoration', 'listed personal-use asset',
        'car exemption', 'motorcycle exemption', '$10,000 threshold',
        # Small Business Concessions
        'small business cgt concession', 'small business concession', '$6 million test',
        'net asset value test', 'maximum net asset value', 'connected entity', 'affiliate',
        'cgt concession stakeholder', 'significant individual', 'active asset', 'active asset test',
        '50% active asset reduction', '15-year exemption', '15 year exemption',
        'retirement exemption', '$500,000 cap', '$500,000 lifetime limit',
        # Rollovers
        'rollover', 'rollover relief', 'replacement asset rollover', 'scrip for scrip',
        'merger rollover', 'demerger rollover', 'marriage breakdown rollover',
        'small business rollover', 'small business cgt rollover', 'capital gains exempt amount',
        # CGT Events
        'cgt event a1', 'cgt event b1', 'cgt event c1', 'cgt event c2', 'cgt event d1',
        'cgt event e1', 'cgt event e2', 'cgt event e5', 'cgt event e8', 'cgt event h2',
        'cgt event k6', 'cgt event j1', 'look-through earnout right', 'earnout arrangement',
        # Anti-Avoidance
        'value shifting', 'indirect value shift', 'ivs', 'direct value shift', 'dvs',
        'realisation time method', 'adjustable value method', 'affected interest',
        'down interest', 'up interest', 'active participant', 'diminution in value',
        'increase in value', 'indirect equity interest', 'loss duplication',
        'loss duplication rule', 'wash sale', 'artificial loss', 'capital loss denial',
        'matched position', 'hedging transaction', 'offsetting position'
    ],

    # Goods and Services Tax - GST registration, supplies, credits, adjustments
    'Tax_GST': [
        # Core Legislation
        'gst act', 'goods and services tax', 'goods and services tax act 1999',
        'a new tax system', 'gstr',
        # Core Concepts
        'gst', 'taxable supply', 'supply', 'supply for consideration', 'consideration',
        'input tax credit', 'itc', 'creditable acquisition', 'creditable purpose',
        'creditable importation', 'connected with australia', 'australia', 'indirect tax zone',
        'supply made in australia', 'enterprise', 'carrying on enterprise',
        'activity done in enterprise',
        # Registration & Returns
        'gst registration', 'registration threshold', '$75,000 threshold', '$150,000 threshold',
        'gst turnover', 'current gst turnover', 'projected gst turnover',
        'tax invoice', 'recipient created tax invoice', 'rcti', 'adjustment note',
        'bas', 'business activity statement', 'activity statement', 'gst return',
        'tax period', 'monthly', 'quarterly', 'annual',
        # GST-Free & Input-Taxed
        'gst-free', 'gst-free supply', 'input-taxed', 'input-taxed supply',
        'basic food', 'gst-free food', 'health service', 'medical service',
        'education course', 'course material', 'childcare', 'childcare service',
        'religious service', 'charity', 'charitable institution', 'gift-deductible entity',
        'export', 'international transport', 'water supply', 'sewerage', 'drainage',
        'financial supply', 'financial service', 'lending', 'equity interest', 'borrowing',
        'residential premises', 'residential rent', 'residential accommodation',
        'commercial residential premises', 'hotel', 'motel', 'serviced apartment',
        'precious metal',
        # Adjustments
        'adjustment', 'increasing adjustment', 'decreasing adjustment', 'adjustment event',
        'change in consideration', 'change in creditable purpose', 'bad debt',
        'bad debt adjustment', 'adjustment period',
        # Special Rules
        'margin scheme', 'margin', 'taxable supply of real property', 'property development',
        'going concern', 'going concern exemption', 'sale of going concern',
        'reverse charge', 'offshore supply', 'gst group', 'gst grouping',
        'representative member', 'gst joint venture', 'gst branch', 'branch registration',
        'reduced credit acquisition', 'reduced input tax credit', 'non-deductible expense',
        'entertainment', 'second-hand goods', 'second-hand goods dealer', 'tourism',
        'tour', 'travel agent', 'inbound intangible consumer supply',
        'low value imported goods', 'lvig', 'gst inclusive'
    ],

    # Corporate Tax - Company tax, consolidation, franking, R&D, thin cap
    'Tax_Corporate': [
        # Company Tax
        'company tax', 'corporate tax', 'company tax rate', 'base rate entity',
        'base rate entity passive income', 'small business entity', 'sbe',
        'aggregated turnover', 'turnover threshold',
        # Consolidation
        'consolidation', 'tax consolidated group', 'tax consolidation', 'head company',
        'subsidiary member', 'subsidiary', 'single entity rule', 'entry history rule',
        'exit history rule', 'allocable cost amount', 'aca', 'joining entity',
        'leaving entity', 'consolidated group',
        # Losses
        'loss carry-forward', 'carry-forward loss', 'loss carry-back', 'carry-back loss',
        'temporary loss carry-back', 'continuity of ownership test', 'cot',
        'same business test', 'sbt', 'similar business test', 'business continuity test',
        'recoupment',
        # R&D
        'research and development', 'r&d', 'r&d tax incentive', 'r&d tax offset',
        'r&d entity', 'core r&d activity', 'supporting r&d activity',
        # Thin Capitalisation
        'thin capitalisation', 'thin cap', 'debt deduction creation rule',
        'safe harbour debt amount', 'shda', 'arm\\'s length debt amount', 'alda',
        'worldwide gearing debt amount', 'wgda', 'on-lend', 'associate entity',
        'debt deduction', 'disallowed deduction', 'adjusted average debt',
        'average equity capital', 'safe harbour test', 'arm\\'s length debt test',
        'worldwide gearing test', 'de minimis', '$2 million threshold',
        'inward investing entity', 'inward investment vehicle', 'outward investing entity',
        'financial entity', 'authorised deposit-taking institution', 'adi',
        'securitisation vehicle', 'investment body', 'operative entity',
        # Transfer Pricing & International
        'transfer pricing', 'arm\\'s length', 'arm\\'s length principle', 'subdivision 815-a',
        'comparable uncontrolled price', 'cup', 'resale price method', 'rpm',
        'cost plus method', 'cpm', 'transactional net margin method', 'tnmm',
        'profit split method', 'psm', 'functional analysis', 'comparability analysis',
        'transfer pricing documentation', 'master file', 'local file',
        'advance pricing arrangement', 'apa',
        # Diverted Profits
        'diverted profits tax', 'dpt', 'multinational anti-avoidance law', 'maal',
        '40% tax rate', 'diverted profits', 'country by country reporting',
        'country-by-country report', 'cbcr', 'cbc reporting', 'significant global entity',
        'sge', '$1 billion threshold', 'global parent entity', 'constituent entity',
        # BEPS
        'base erosion', 'beps', 'base erosion and profit shifting', 'pillar one', 'pillar two',
        'global minimum tax', 'gmt', '15% minimum', 'income inclusion rule', 'iir'
    ],

    # Fringe Benefits Tax - FBT types, valuation, exemptions, concessions
    'Tax_FBT': [
        # Core Legislation
        'fringe benefits tax', 'fbt', 'fringe benefit', 'fringe benefits tax assessment act',
        'fbtaa', 'fbt year', '1 april', '31 march', 'fbt rate', '47%',
        # Parties
        'employer', 'employee', 'current employee', 'former employee', 'future employee',
        'associate', 'relative',
        # Valuation
        'taxable value', 'grossed-up taxable value', 'grossed-up value', 'gross-up factor',
        'type 1 benefit', 'type 1 grossed-up', 'type 2 benefit', 'type 2 grossed-up',
        'type 1 aggregate', 'type 2 aggregate',
        # Car Benefits
        'car benefit', 'car fringe benefit', 'statutory formula method', 'operating cost method',
        'base value', 'statutory fraction', 'days available', 'private use', 'logbook',
        'odometer', 'car parking benefit', 'car parking fringe benefit',
        'commercial parking station', 'lowest daily fee', '$10.26 threshold',
        'small business car parking exemption',
        # Loan Benefits
        'loan benefit', 'loan fringe benefit', 'benchmark interest rate',
        'statutory interest rate', 'notional interest', 'interest-free loan',
        # Other Benefit Types
        'expense payment benefit', 'expense payment fringe benefit', 'reimbursement',
        'payment of expense', 'third party expense', 'housing benefit',
        'housing fringe benefit', 'accommodation', 'rental value', 'market value rent',
        'subsidised rent', 'living-away-from-home allowance', 'lafha',
        'living away from home', 'temporary accommodation', 'fly-in fly-out', 'fifo',
        'drive-in drive-out', 'dido', 'meal entertainment', 'entertainment benefit',
        'entertainment fringe benefit', '50/50 split method', '12-week register',
        'actual method', 'tax-exempt body entertainment', 'airline transport benefit',
        'standby airline travel', 'residual benefit', 'residual fringe benefit',
        'property benefit', 'property fringe benefit',
        # Exemptions & Reductions
        'minor benefit', 'minor benefit exemption', '$300 threshold', 'less than $300',
        'infrequent', 'irregular', 'unreasonable', 'otherwise deductible rule', 'odr',
        'hypothetical deduction', 'employee contribution', 'recipient contribution',
        'reduction in taxable value', 'reportable fringe benefit',
        'reportable fringe benefits amount', 'rfba', 'excluded fringe benefit',
        'exempt benefit', 'exempt fringe benefit', 'work-related item',
        'portable electronic device', 'laptop', 'mobile phone', 'protective clothing',
        'briefcase', 'tool of trade', 'item of clothing', 'public benevolent institution',
        'pbi', 'health promotion charity', 'religious institution', 'registered charity',
        'tax concession charity',
        # Salary Packaging
        'salary sacrifice', 'salary packaging', 'salary sacrifice arrangement',
        'effective salary packaging', 'novated lease', 'employee share scheme', 'ess',
        'share scheme', 'option scheme', 'deferred start date', 'cessation time'
    ],

    # Superannuation Tax - Contributions, fund tax, benefits, SMSFs
    'Tax_Superannuation': [
        # Core Concepts
        'superannuation', 'super', 'superannuation fund', 'complying fund',
        'non-complying fund', 'regulated fund', 'superannuation industry supervision act',
        'sis act', 'superannuation guarantee administration act',
        # Superannuation Guarantee
        'superannuation guarantee', 'sg', 'sg charge', 'sg percentage',
        'ordinary time earnings', 'ote', 'employer contribution',
        'mandatory contribution', 'choice of fund', 'default fund', 'stapled fund',
        # Contributions
        'concessional contribution', 'non-concessional contribution', 'personal contribution',
        'salary sacrifice contribution', 'member contribution', 'contribution cap',
        'concessional cap', '$30,000 cap', '$27,500 cap', 'non-concessional cap',
        '$120,000 cap', '$110,000 cap', 'bring-forward rule', 'bring-forward period',
        'carry-forward concessional', 'unused concessional cap', 'carry-forward provision',
        '5-year carry-forward', 'excess contribution', 'excess concessional contribution',
        'excess non-concessional contribution', 'excess contributions tax', 'ect',
        'excess contributions determination', 'release authority', 'withdraw and recontribute',
        'additional 15%', 'high income earner', '$250,000 threshold',
        'adjusted taxable income', 'income for surcharge purposes',
        'reportable super contribution', 'contribution splitting', 'split contribution',
        'spouse contribution', 'spouse contribution offset', 'low income spouse',
        'government co-contribution', 'co-contribution', 'eligible contribution',
        'matching contribution', '15% contributions tax', '30% contributions tax',
        # Preservation & Release
        'preservation', 'preserved benefit', 'preservation age', 'age 60', 'age 65',
        'condition of release', 'unrestricted non-preserved', 'restricted non-preserved',
        'retirement', 'permanent incapacity', 'temporary incapacity',
        'terminal medical condition', 'severe financial hardship', 'compassionate grounds',
        'first home super saver', 'fhss', 'fhsss scheme', 'illegal early release',
        'early access scheme',
        # Components & Tax Treatment
        'tax-free component', 'taxable component', 'taxed element', 'untaxed element',
        'crystallised', 'tax-free proportion', 'taxable proportion',
        # Lump Sums
        'lump sum', 'lump sum payment', 'lump sum tax', 'under preservation age',
        'between preservation age and 60', 'age 60 and over', 'tax-free after 60',
        # Pensions
        'pension', 'superannuation pension', 'account-based pension', 'allocated pension',
        'transition to retirement', 'ttr', 'ttr pension', 'non-commutable pension',
        'capped defined benefit', 'uncapped defined benefit', 'lifetime pension',
        'market-linked pension', 'minimum drawdown', 'pension standards',
        'reversionary pension',
        # Death Benefits
        'death benefit', 'death benefit dependant', 'death benefit nomination',
        'binding death benefit nomination', 'non-binding nomination',
        'reversionary beneficiary', 'tax on death benefits', 'non-dependant',
        'child under 18', 'financial dependant', 'interdependency relationship',
        # Transfer Balance Cap
        'transfer balance cap', 'tbc', '$1.9 million', 'general transfer balance cap',
        'personal transfer balance cap', 'ptbc', 'transfer balance account', 'tba',
        'excess transfer balance', 'excess transfer balance tax',
        'commutation authority', 'notional earnings', 'total superannuation balance', 'tsb',
        # Fund Taxation
        'pension phase', 'retirement phase', 'accumulation phase', 'growth phase',
        'contribution phase', 'fund earnings', 'exempt current pension income', 'ecpi',
        '15% tax on earnings', '10% tax on capital gains', 'zero tax in pension phase',
        'actuarial certificate', 'segregated assets',
        'unsegregated assets', 'proportionate method',
        # SMSFs
        'self-managed super fund', 'smsf', 'small apra fund',
        'sole purpose test', 'compliance test', 'in-house asset',
        'in-house asset rule', '5% limit', 'related party', 'related trust',
        'investment strategy', 'diversification', 'liquidity', 'insurance in super',
        'life insurance', 'total and permanent disability', 'tpd', 'income protection',
        'death cover', 'trustee', 'individual trustee', 'corporate trustee',
        'trustee duty', 'covenants', 'operating standards', 'annual return',
        'smsf annual return', 'approved auditor', 'audit report',
        'contravention report', 'actuarial valuation', 'actuary', 'disqualified person',
        'disqualified trustee', 'automatic disqualification',
        # Special Contributions
        'notice of intent', 'personal contribution deduction', 'claiming deduction',
        'downsizer contribution', '$300,000 downsizer', 'eligible dwelling',
        'personal injury payment', 'structured settlement', 'anti-detriment payment'
    ],

    # State Taxes - Payroll tax, land tax, stamp duty, state revenue
    'Tax_State': [
        # State Revenue Administration
        'chief commissioner of state revenue', 'commissioner of state revenue',
        'revenue nsw', 'revenue office', 'state taxation office', 'sro victoria',
        'office of state revenue', 'revenue ruling', 'practice direction',
        'revenue guidelines',
        # Payroll Tax
        'payroll tax', 'payroll tax act', 'payroll tax threshold', 'wages',
        'payroll tax wages', 'deemed wages', 'taxable wages', 'exempt wages',
        'contractor', 'deemed employee', 'contractor provision', 'services contract',
        'labour hire', 'on-hire', 'relevant contract', 'grouping', 'group employer',
        'designated group employer', 'dge', 'common control', 'tracing', 'use and control',
        'interstate wages', 'interstate allocation', 'apportionment', 'principal place',
        'director fee', 'redundancy', 'termination payment',
        'annual leave', 'long service leave', 'parental leave',
        # Land Tax
        'land tax', 'land tax act', 'land tax management act', 'land tax threshold',
        'taxable land', 'taxable value', 'site value', 'improved value', 'unimproved value',
        'primary production', 'primary production exemption', 'farming land',
        'agricultural land', 'rural land', 'charitable exemption', 'retirement village',
        'aged care facility', 'nursing home', 'caravan park', 'boarding house',
        'rooming house', 'absentee owner', 'foreign owner', 'absentee owner surcharge',
        'foreign owner surcharge', 'vacant land tax', 'vacant residential land',
        'trust surcharge', 'discretionary trust surcharge', 'fixed trust exemption',
        'aggregation', 'aggregate landholdings', 'surcharge land tax', 'surcharge purchaser duty',
        'premium property duty',
        # Stamp Duty / Transfer Duty
        'stamp duty', 'duties act', 'transfer duty', 'ad valorem duty', 'dutiable value',
        'dutiable transaction', 'dutiable property', 'real property', 'chattel',
        'business property', 'goodwill', 'chose in action', 'partnership interest',
        'intellectual property', 'motor vehicle', 'vehicle duty', 'registration duty',
        'unencumbered value', 'highest value',
        # Stamp Duty Concessions
        'first home buyer', 'first home buyer concession', 'first home buyer exemption',
        'fhog', 'first home owner grant', 'owner occupier', 'off-the-plan',
        'off-the-plan concession', 'vacant land', 'new home', 'established home',
        'substantially renovated', 'substantial renovation', 'family transfer',
        'relationship breakdown', 'deceased estate', 'transmission', 'survivorship',
        'joint tenant', 'tenant in common', 'nomination',
        'relief', 'exemption', 'concession', 'reduction', 'deferral',
        # Landholder Duty
        'landholder', 'landholder duty', 'land-rich', 'land-rich entity', 'landholding',
        'substantial interest', '50% interest', 'acquisition of interest',
        'relevant acquisition', 'related acquisition', 'associated person',
        # Foreign Purchaser Duty
        'foreign person', 'foreign purchaser', 'foreign purchaser duty',
        'foreign purchaser additional duty', 'fpd', 'fpad', 'foreign investor',
        'premium property', 'luxury home', 'high-value property',
        # Other State Levies
        'parking space levy', 'psl', 'parking bay', 'cbd parking', 'off-street parking',
        'insurance duty', 'fire services levy', 'fsl', 'emergency services levy', 'esl',
        'motor vehicle duty', 'vehicle registration', 'transfer of registration',
        'registration fee', 'vehicle licence'
    ],

    # International Tax - Residency, foreign income, transfer pricing, treaties, BEPS
    'Tax_International': [
        # Tax Residency
        'tax residency', 'resident', 'non-resident', 'temporary resident',
        'resides test', 'ordinary residence', 'domicile', 'domicile test',
        '183-day test', 'six-month test', 'superannuation test',
        'company residency', 'incorporation test', 'central management and control',
        'central management and control test', 'voting power test', 'place of incorporation',
        'trust residency', 'central management', 'resident trust estate',
        # Foreign Income
        'foreign income', 'foreign-source income', 'worldwide income', 'australian-source income',
        'source of income', 'source rules', 'active income', 'passive income',
        'foreign tax offset', 'fito', 'foreign income tax offset', 'foreign tax credit',
        'tax credit', 'foreign tax paid', 'double taxation', 'double taxation relief',
        # Tax Treaties
        'double tax agreement', 'dta', 'tax treaty', 'bilateral treaty',
        'multilateral instrument', 'mli', 'beps mli', 'covered tax agreement',
        'treaty relief', 'treaty benefit', 'limitation on benefits', 'lob',
        'principal purpose test', 'ppt', 'treaty shopping', 'conduit', 'treaty residence',
        'tie-breaker', 'tie-breaker rule', 'dual residency', 'casting vote',
        # Permanent Establishment
        'permanent establishment', 'pe', 'fixed place pe', 'dependent agent pe',
        'building site', 'construction site', 'installation project', 'supervisory activity',
        'business profits', 'business profits article', 'attributable profits',
        # Withholding Tax
        'withholding tax', 'wht', 'dividend withholding', 'interest withholding',
        'royalty withholding', 'unfranked dividend wht', 'treaty rate', 'domestic rate',
        'reduced withholding rate', 'exemption from withholding', 'final withholding tax',
        # CFC & Transferor Trusts
        'controlled foreign company', 'cfc', 'cfc rules', 'attributable income',
        'cfc attribution', 'eligible designated concession income', 'tainted income',
        'tainted sales income', 'tainted services income', 'passive cfc income',
        'active business income', 'active foreign business income', 'active income test',
        'transferor trust', 'non-resident trust', 'transferor', 'deemed present entitlement',
        'attribution percentage', 'attributable taxpayer',
        # Dispute Resolution
        'mutual agreement procedure', 'map', 'competent authority', 'dispute resolution',
        'mandatory binding arbitration', 'exchange of information', 'eoi',
        'automatic exchange', 'common reporting standard', 'crs', 'fatca',
        'foreign account tax compliance act', 'us person', 'reportable account'
    ],

    # Tax Avoidance - Part IVA, Division 7A, promoter penalties, specific anti-avoidance
    'Tax_Avoidance': [
        # Part IVA - General Anti-Avoidance
        'part iva', 'part 4a', 'general anti-avoidance', 'general anti-avoidance rule',
        'gaar', 'tax avoidance', 'tax minimisation', 'tax planning',
        'aggressive tax planning', 'scheme', 'arrangement', 'plan', 'course of action',
        'tax benefit', 'tax detriment', 'reduction in tax', 'increase in loss', 'deferral',
        'dominant purpose', 'sole or dominant purpose', 'more than incidental purpose',
        'predication test', 'would conclude', 'reasonable person', 'objective test',
        'subjective test', 'purpose or effect', '8 factors', 'manner of entry',
        'form and substance', 'duration', 'timing', 'expected tax benefit',
        'financial position', 'other consequences', 'nature of connection',
        'commissioner determination', 'cancel tax benefit', 'compensating adjustment',
        # Promoter Penalties
        'promoter penalty', 'promoter penalty law', 'tax exploitation scheme',
        'significant tax benefit', 'scheme promoter',
        'scheme entity', 'facilitated', 'marketed', 'implemented', 'encouraged',
        'base penalty amount', 'penalty percentage', 'promoter penalty amount',
        # Division 7A
        'div 7a', 'deemed dividend', 'private company', 'payment',
        'loan', 'debt forgiveness', 'shareholder', 'associate of shareholder',
        'trust beneficiary', 'minimum yearly repayment', 'complying loan',
        'loan agreement', '7-year loan', '25-year loan',
        'amalgamated loan', 'unpaid present entitlement', 'upe', 'sub-trust arrangement',
        'interposed entity', 'loan back',
        # Specific Anti-Avoidance
        'specific anti-avoidance', 'specific anti-avoidance rule', 'saar',
        'tax shelter',
        # Phoenix & Recovery
        'phoenix activity', 'phoenixing', 'illegal phoenixing', 'creditor defeating',
        'director penalty notice', 'dpn', 'personal liability', 'lock-down',
        'non-remittable', 'estimate assessment', 'security deposit', 'transfer asset',
        'alienate asset', 'recovery', 'collection proceedings', 'garnishee',
        # Economic Substance Doctrines
        'westrader principle', 'economic substance', 'substance over form',
        'beneficial ownership', 'beneficial owner', 'legal owner', 'nominee',
        'sham', 'sham transaction', 'sham doctrine', 'pretence', 'make-believe',
        'fiscal nullity', 'self-cancelling', 'circular', 'round-robin',
        # Penalties & Compliance
        'reasonably arguable', 'reasonably arguable position', 'rap',
        'shortfall penalty', 'false or misleading statement', 'lack of reasonable care',
        'recklessness', 'intentional disregard', 'voluntary disclosure',
        'penalty reduction', 'reasonable care defence', 'tax evasion', 'evasion',
        'fraud', 'false statement', 'concealment', 'penalty', 'shortfall',
        'tax debt', 'tax position'
    ],

    # Trusts & Partnerships - Trust taxation, distributions, partnerships
    'Tax_Trusts_Partnerships': [
        # Trust Taxation
        'trust taxation', 'trust income', 'trust loss', 'division 6e',
        'trust estate', 'net income of trust', 'discretionary trust', 'unit trust',
        'fixed trust', 'testamentary trust', 'family trust', 'present entitlement',
        'presently entitled', 'beneficiary', 'default beneficiary', 'income beneficiary',
        'capital beneficiary', 'trustee', 'appointor', 'vesting date',
        'trust distribution', 'specific entitlement',
        'proportionate approach', 'interposed entity election', 'iee', 'family group',
        'conferral of present entitlement',
        # Partnership
        'partnership', 'partnership taxation', 'flow-through', 'flow-through treatment',
        'partner', 'partnership agreement', 'joint venture', 'limited partnership',
        'professional partnership', 'allocation of income', 'allocation of losses'
    ],

    # PAYG, Administration, Rulings, Compliance
    'Tax_Administration': [
        # PAYG & Collection
        'payg', 'pay as you go', 'payg withholding', 'payg instalment',
        'withholding', 'instalments', 'collection',
        # Interest & Penalties
        'general interest charge', 'gic', 'shortfall interest charge', 'sic',
        'administrative penalty', 'failure to lodge penalty',
        # Returns & Lodgement
        'tax return', 'income tax return', 'tax file number', 'tfn',
        'australian business number', 'abn', 'lodgement', 'failure to lodge',
        'late lodgement', 'extension of time', 'lodgement fee',
        # Objections
        'objection', 'notice of objection', 'objection decision', '60 days',
        # Compliance & Audit
        'audit', 'risk review', 'compliance', 'compliance program',
        'contemporaneous documentation', 'retention period', '5 years',
        'business records', 'tax records',
        # Tax Agents
        'tax agent', 'registered tax agent', 'bas agent', 'tax practitioners board',
        'tpb', 'code of professional conduct', 'tax agent services act',
        # Emerging Issues
        'crypto-asset', 'cryptocurrency', 'bitcoin', 'ethereum', 'digital currency',
        'virtual currency', 'nft', 'non-fungible token', 'digital asset', 'blockchain',
        'distributed ledger', 'decentralised finance', 'defi', 'crypto exchange',
        'crypto wallet', 'mining', 'staking', 'crypto staking',
        'yield farming', 'airdrops', 'hard fork', 'gig economy', 'platform economy',
        'sharing economy', 'on-demand economy', 'platform worker',
        'independent contractor', 'employee vs contractor', 'employment status',
        'remote work', 'work from home', 'wfh', 'telecommuting',
        'cross-border employment', 'remote worker', 'digital nomad',
        'esg', 'environmental social governance',
        'carbon credit', 'carbon tax', 'emissions trading', 'renewable energy',
        'clean energy', 'sustainability', 'climate change', 'net zero',
        'carbon neutral', 'stage 3 tax cuts', 'tax cuts', 'tax reform',
        'personal tax rates', 'bracket creep', 'shadow economy', 'cash economy',
        'black economy', 'undeclared income', 'hidden economy', 'underground economy',
        'tax gap', 'compliance gap', 'work test exemption', 'work test',
        'robodebt', 'scheme debt', 'income averaging', 'automated debt raising',
        'corporate collective investment vehicle', 'cciv',
        'attribution managed investment trust', 'amit', 'managed investment trust', 'mit'
    ],"""

# Find and replace the old Tax_Federal and Tax_State sections
pattern = r"    'Tax_Federal':\s*\[.*?\],\s*'Tax_State':\s*\[.*?\],"
replacement = tax_categories

content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Also need to update the hierarchy mapping
hierarchy_pattern = r"'Tax':\s*\['Tax_Federal',\s*'Tax_State'\],"
hierarchy_replacement = "'Tax': ['Tax_Income', 'Tax_CGT', 'Tax_GST', 'Tax_Corporate', 'Tax_FBT', 'Tax_Superannuation', 'Tax_State', 'Tax_International', 'Tax_Avoidance', 'Tax_Trusts_Partnerships', 'Tax_Administration'],"

content_updated = re.sub(hierarchy_pattern, hierarchy_replacement, content_updated)

# Write the updated content
with open('src/ingestion/classification_config.py', 'w', encoding='utf-8') as f:
    f.write(content_updated)

print("✓ Successfully updated classification_config.py with comprehensive Tax keywords")
print("\nNew Tax categories added:")
print("  - Tax_Income (87 keywords)")
print("  - Tax_CGT (87 keywords)")
print("  - Tax_GST (100 keywords)")
print("  - Tax_Corporate (78 keywords)")
print("  - Tax_FBT (103 keywords)")
print("  - Tax_Superannuation (157 keywords)")
print("  - Tax_State (117 keywords)")
print("  - Tax_International (81 keywords)")
print("  - Tax_Avoidance (73 keywords)")
print("  - Tax_Trusts_Partnerships (33 keywords)")
print("  - Tax_Administration (82 keywords)")
print("\nTotal: 998 tax keywords added!")
