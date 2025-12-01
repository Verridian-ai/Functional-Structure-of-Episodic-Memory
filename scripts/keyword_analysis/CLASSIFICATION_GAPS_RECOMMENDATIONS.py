# CLASSIFICATION_CONFIG.PY GAP ANALYSIS - RECOMMENDED ADDITIONS
# Generated: 2025-11-29
# Target file: src/ingestion/classification_config.py

# ============================================================================
# ADMINISTRATIVE LAW - ENHANCED KEYWORDS
# ============================================================================

ADMIN_MIGRATION_ENHANCED = [
    # EXISTING (keep all current keywords)
    'migration act', 'protection visa', 'visa cancellation', 'section 501',
    'refugee review tribunal', 'immigration assessment authority', 'minister for immigration',
    'deportation', 'skilled migration', 'detention', 'bridging visa', 'student visa',
    'partner visa', 'character test', 'character cancellation', 'protection claim',
    'refugee status', 'asylum seeker', 'immigration detention', 'immigration review',
    'migration agent', 'onshore protection', 'offshore protection', 'complementary protection',
    's501', 's501ca', 'ministerial intervention', 'ministerial direction', 'removal',

    # NEW ADDITIONS - Visa subclasses
    'subclass 820', 'subclass 801', 'subclass 188', 'subclass 888', 'subclass 457',
    'subclass 482', 'subclass 186', 'subclass 189', 'subclass 190', 'subclass 491',
    'subclass 100', 'subclass 143', 'subclass 866', 'subclass 202', 'subclass 785',

    # NEW ADDITIONS - Cancellation terminology
    'substantial criminal record', 'behaviour concern', 'another reason', 's501ca revocation',
    'compelling circumstances', 'best interests of the child', 'direction 90', 'direction 99',
    'strength duration ties', 'expectations of australian community',

    # NEW ADDITIONS - Tribunal divisions and procedure
    'migration and refugee division', 'mrd', 'migration review tribunal', 'mrt',
    'refugee review tribunal', 'rrt', 'tribunal act 2015', 'part 5 review',
    'part 7 review', 'fast track', 'iaa review',

    # NEW ADDITIONS - Protection grounds
    'refugees convention', 'sur place claim', 'political opinion', 'membership of particular social group',
    'race', 'religion', 'nationality', 'effective protection', 'relocation principle',
    'complementary protection criterion', 'significant harm', 'torture', 'cruel inhuman degrading',
    'arbitrary deprivation of life', 'death penalty',

    # NEW ADDITIONS - Procedural terms
    'pam3', 'procedural advice manual', 'ministerial direction 65', 'ministerial direction 79',
    'direction 65', 'direction 79', 'direction 80', 'merits review', 'code of procedure',
    'schedule 1 criteria', 'schedule 2 criteria', 'schedule 3 criteria',
    'public interest criterion 4020', 'pic 4020', 'sch3 waiver',
    'compelling and compassionate circumstances'
]

ADMIN_SOCIAL_SECURITY_ENHANCED = [
    # EXISTING (keep all current keywords)
    'social security act', 'disability support pension', 'centrelink',
    'administrative appeals tribunal', 'aat', 'ndis act', 'national disability insurance',
    'robodebt', 'jobseeker', 'dsp', 'age pension', 'carer payment', 'parenting payment',
    'family tax benefit', 'newstart', 'austudy', 'abstudy', 'youth allowance',
    'social security appeal', 'overpayment', 'debt recovery', 'waiver', 'special circumstances',
    'ndis participant', 'ndis plan', 'support needs', 'reasonable and necessary',

    # NEW ADDITIONS - NDIS specific
    'ndia', 'national disability insurance agency', 'ndis provider', 'ndis support',
    'plan manager', 'support coordinator', 'core supports', 'capacity building',
    'capital supports', 'stated supports', 'plan reviewer', 'internal review ndis',
    'aat review ndis', 'supports in kind', 'reasonable necessary supports',

    # NEW ADDITIONS - Social security tests
    'continuing inability to work', 'severely impaired', 'impairment table',
    '20 point rating', '15 hours per week', 'participation requirement',
    'mutual obligation', 'job plan', 'compliance failure', 'reconnection requirement',
    'payment suspension', 'rate of payment', 'income test', 'assets test',

    # NEW ADDITIONS - Debt procedures
    'social security debt', 'debt notice', 's1223', 's1224aa', 'debt waiver',
    'recovery fee', 'small debt', 'statute barred debt', 'departure prohibition order',
    'garnishee notice', 'debt write off',

    # NEW ADDITIONS - Other payments
    'mobility allowance', 'pharmaceutical allowance', 'rent assistance', 'remote area allowance',
    'pension supplement', 'clean energy supplement', 'telephone allowance',

    # NEW ADDITIONS - Social Services Division
    'social services and child support division', 'sscs division', 'child support appeal'
]

ADMIN_VETERANS_ENHANCED = [
    # EXISTING (keep all current keywords)
    'veterans entitlements', 'military rehabilitation', 'mrca', 'war widow pension', 'dva',
    'veterans review board', 'vrb', 'statement of principles', 'sop', 'reasonable hypothesis',
    'service injury', 'accepted condition', 'war service', 'peacekeeping service',
    'special rate pension', 'totally and permanently incapacitated', 'tpi',
    'intermediate rate', 'extreme disablement adjustment',

    # NEW ADDITIONS - VEA terminology
    'vea', 'veterans entitlements act', 'defence service', 'operational service',
    'peacetime service', 'eligible service', 'service pension', 'income support supplement',
    'gold card', 'white card', 'orange card', 'repatriation health card',

    # NEW ADDITIONS - SoP specific
    'treatment principles', 'reasonable hypothesis test', 'beyond reasonable doubt',
    'deledio', 'four step process', 'clinical onset', 'clinical worsening',
    'kind of injury disease or death', 'kidd', 'factor', 'sop factor'
]

ADMIN_JUDICIAL_REVIEW_ENHANCED = [
    # EXISTING (keep all current keywords)
    'adjr act', 'judicial review', 'jurisdictional error', 'wednesbury unreasonableness',
    'legal unreasonableness', 'natural justice', 'procedural fairness', 'bias',
    'apprehended bias', 'hearing rule', 'relevant consideration', 'irrelevant consideration',
    'improper purpose', 'fettering discretion', 'ultra vires', 'mandamus', 'certiorari',
    'prohibition', 'prerogative writ', 'constitutional writ', 'section 39b', 's39b',
    'jurisdictional fact', 'no evidence', 'illogical', 'irrational', 'unreasonable decision',

    # NEW ADDITIONS - Migration Act specific
    'section 476', 's476', 'section 476a', 's476a', 'privative clause', 'section 474',
    'plaintiff s157', 'constructive failure to exercise jurisdiction',
    'ask wrong question', 'disregard relevant consideration', 'legal error',

    # NEW ADDITIONS - State tribunal appeals
    'ncat appeal panel', 'appeal on question of law', 'kirk v industrial relations',
    'wednesbury principles', 'associated provincial picture houses'
]

# ============================================================================
# TAX LAW - ENHANCED KEYWORDS
# ============================================================================

TAX_INCOME_ENHANCED = [
    # EXISTING (keep all current keywords)
    'income tax assessment act', 'commissioner of taxation', 'tax benefit', 'part iva',
    'assessable income', 'ordinary income', 'statutory income', 'exempt income',
    'deduction', 'allowable deduction', 'work-related expense', 'depreciation',
    'capital allowance', 'self-education expense', 'home office', 'travel expense',
    'negative gearing', 'prepaid expense', 'accrued expense', 'ato', 'tax agent',
    'personal services income', 'psi', 'income splitting', 'alienation of income',
    'dividend', 'franking credit', 'imputation credit', 'unfranked dividend',

    # NEW ADDITIONS - Division 7A
    'division 7a', 'div 7a', 's109', 'deemed dividend', 'private company',
    'shareholder loan', 'complying loan', 'benchmark interest rate', 'minimum yearly repayment',
    'loan agreement', 'unpaid present entitlement', 'upe',

    # NEW ADDITIONS - Trust taxation
    'trust income', 'net income of trust', 'division 6', 'division 6e',
    'present entitlement', 'beneficiary income', 'trust distribution',
    'reimbursement agreement', 'section 100a', 's100a', 'ordinary family dealing',
    'trustee assessment', 'excepted trust income',

    # NEW ADDITIONS - Specific deduction provisions
    'section 8-1', 's8-1', 'general deduction', 'business expense', 'nexus test',
    'positive limbs', 'negative limbs', 'capital outgoing', 'private purpose',
    'section 25-25', 'borrowing expense', 'section 40-880', 'blackhole expenditure',

    # NEW ADDITIONS - Timing
    'section 15-2', 's15-2', 'trading stock', 'prepayment rule', 'section 82kzm',
    '12 month rule', 'expenditure incurred',

    # NEW ADDITIONS - Income characterization
    'ordinary concepts', 'receipts on revenue account', 'receipts on capital account',
    'profit-making undertaking', 'isolated transaction', 'mere realization',

    # NEW ADDITIONS - Residence
    'tax resident', 'foreign resident', 'resides test', 'domicile test',
    '183 day test', 'superannuation test', 'ordinary concepts residence'
]

TAX_CGT_ENHANCED = [
    # EXISTING (keep all current keywords)
    'capital gains tax', 'cgt', 'capital gain', 'capital loss', 'cost base',
    'reduced cost base', 'cgt discount', '50 percent discount', 'cgt event',
    'cgt asset', 'main residence exemption', 'small business cgt concession',
    'active asset', 'rollover relief', 'scrip for scrip', 'market value',
    'acquisition date', 'disposal', 'capital proceeds', 'indexation',

    # NEW ADDITIONS - CGT events
    'cgt event a1', 'cgt event b1', 'cgt event c1', 'cgt event c2', 'cgt event c3',
    'cgt event d1', 'cgt event e1', 'cgt event g1', 'cgt event h2', 'cgt event i1',
    'cgt event j1', 'cgt event k1', 'cgt event k3', 'cgt event k4', 'cgt event k6',

    # NEW ADDITIONS - Small business concessions
    '15 year exemption', 'retirement exemption', '50 percent active asset reduction',
    'small business rollover', 'maximum net asset value test', 'mnavt', '$6 million test',
    'active asset test', '80 percent test', 'significant individual',
    'affiliated entity', 'connected entity', 'cgt concession stakeholder',

    # NEW ADDITIONS - Main residence
    'dwelling', 'adjacent land', '2 hectare test',
    'use for income producing purposes', 'absence rule', '6 year rule',
    'first use to produce income', 'partial exemption formula',

    # NEW ADDITIONS - Pre-CGT
    'pre-cgt asset', '20 september 1985', 'acquired before cgt', 'grandfathered'
]

TAX_GST_ENHANCED = [
    # EXISTING (keep all current keywords)
    'gst act', 'goods and services tax', 'taxable supply', 'input tax credit',
    'gst-free', 'input taxed', 'tax invoice', 'adjustment', 'bas',
    'business activity statement', 'gst registration', 'gst group',
    'going concern', 'margin scheme', 'reverse charge', 'gst inclusive',
    'financial supply', 'residential premises', 'commercial residential premises',

    # NEW ADDITIONS - Supplies
    'enterprise', 'carrying on enterprise', 'continuous or regular', 'business of enterprise',
    'consideration', 'supply for consideration', 'monetary consideration',

    # NEW ADDITIONS - Financial supplies
    'division 40', 'regulation 40-5.09', 'input taxed supply',
    'borrowing', 'provision of credit', 'dealing in money', 'provision of interest',
    'financial acquisition threshold', 'reduced input tax credit', 'reduced credit acquisition',

    # NEW ADDITIONS - GST-free
    'division 38', 'gst-free supply', 'food', 'health', 'medical service',
    'education', 'course of study', 'child care', 'exports', 'international transport',
    'precious metal', 'farm land',

    # NEW ADDITIONS - Adjustments
    'division 129', 'division 135', 'increasing adjustment', 'decreasing adjustment',
    'change in extent of creditable purpose', 'adjustment period',

    # NEW ADDITIONS - Reverse charge
    'division 83', 'recipients obligation', 'non-resident',
    'connected with indirect tax zone', 'connected with australia'
]

TAX_CORPORATE_ENHANCED = [
    # EXISTING (keep all current keywords)
    'corporate tax', 'company tax rate', 'base rate entity', 'small business entity',
    'aggregated turnover', 'franking account', 'dividend imputation', 'consolidation',
    'tax consolidated group', 'head company', 'subsidiary', 'single entity rule',
    'thin capitalisation', 'transfer pricing', 'arm\'s length', 'diverted profits tax',
    'multinational anti-avoidance law', 'country by country reporting',

    # NEW ADDITIONS - Consolidation
    'division 701', 'division 705', 'division 711', 'entry history rule',
    'allocable cost amount', 'aca', 'tax cost setting', 'reset cost base',
    'joining entity', 'leaving entity', 'membership interest', 'linked entity',

    # NEW ADDITIONS - International
    'controlled foreign company', 'cfc', 'attributable income', 'active income',
    'passive income', 'cfc attribution', 'division 820',
    'safe harbour test', 'arm\'s length debt test', 'worldwide gearing test',
    'division 815', 'reconstruct', 'arm\'s length consideration',

    # NEW ADDITIONS - Diverted profits
    'dpt', 'maal', 'principal purpose test', 'significant global entity',

    # NEW ADDITIONS - Imputation
    'franking debit', 'franking account balance', 'benchmark rule',
    'streaming', 'qualified person', 'holding period rule', '45 day rule',
    'related payment rule', 'dividend stripping'
]

TAX_FBT_ENHANCED = [
    # EXISTING (keep all current keywords)
    'fringe benefits tax', 'fbt', 'fringe benefit', 'car fringe benefit',
    'expense payment fringe benefit', 'property fringe benefit', 'grossed up',
    'otherwise deductible rule', 'exempt benefit', 'minor benefit', 'employee',
    'associate', 'employer', 'reportable fringe benefit', 'fbt year',

    # NEW ADDITIONS
    'car parking fringe benefit', 'meal entertainment', 'entertainment facility',
    'in-house fringe benefit', 'residual fringe benefit', 'living-away-from-home allowance',
    'lafha', 'fly-in fly-out', 'fifo', 'otherwise deductible test'
]

TAX_STATE_ENHANCED = [
    # EXISTING (keep all current keywords)
    'payroll tax', 'land tax management act', 'duties act', 'stamp duty',
    'transfer duty', 'parking space levy', 'chief commissioner of state revenue',
    'land tax', 'surcharge purchaser duty', 'surcharge land tax', 'foreign investor',
    'premium property duty', 'landholder duty', 'insurance duty', 'motor vehicle duty',
    'first home buyer exemption', 'principal place of residence', 'land rich',

    # NEW ADDITIONS - Payroll tax
    'payroll tax act', 'wages', 'grouping provisions', 'common control',
    'tracing interest', '50 percent interest', 'related corporations',
    'contractor payments', 'relevant contract', 'ordinary wages',

    # NEW ADDITIONS - Duties
    'dutiable transaction', 'dutiable property', 'landholder', 'landholding',
    'significant interest', '50 percent interest test', 'associated persons',
    'marketable securities', 'call option', 'put option', 'option duty',

    # NEW ADDITIONS - Foreign purchaser
    'foreign person', 'foreign corporation', 'foreign trust', 'trustee beneficiary',
    'surcharge purchaser', 'absentee owner', 'vacancy fee',
    'vacant residential land tax', 'principal place of residence test',

    # NEW ADDITIONS - State-specific
    'state revenue office victoria', 'sro', 'taxation administration act victoria',
    'queensland revenue office', 'qro', 'transfer duty qld',

    # NEW ADDITIONS - Land tax
    'land value', 'taxable land', 'exempt land', 'principal place of residence exemption',
    'threshold', 'land tax threshold', 'aggregation'
]

TAX_AVOIDANCE_ENHANCED = [
    # EXISTING (keep all current keywords)
    'part iva', 'general anti-avoidance', 'tax benefit', 'scheme', 'dominant purpose',
    'promoter penalty', 'tax exploitation scheme', 'arrangement', 'tax position',
    'reasonably arguable position', 'shortfall', 'penalty', 'tax debt', 'garnishee',

    # NEW ADDITIONS - Part IVA detail
    'section 177c', 's177c', 'section 177d', 's177d', 'section 177f', 's177f',
    'obtained in connection with', 'scheme purpose',
    'sole or dominant purpose', 'eight factors', 's177d factors',
    'manner carried out', 'form and substance', 'time of entry',
    'result achieved', 'changes in financial position', 'changes in rights',
    'other consequences', 'nature of connection',

    # NEW ADDITIONS - Specific schemes
    'phoenix activity', 'wash sale', 'trust stripping',
    'round robin', 'circular arrangement',

    # NEW ADDITIONS - Objections and appeals
    'taxation objection', 'section 14zz', 's14zz', 'taxation administration act',
    'part ivc', 'appealable objection decision', 'federal court taxation jurisdiction',
    'aat taxation jurisdiction', 'taxation and commercial division',

    # NEW ADDITIONS - Private rulings
    'private ruling', 'public ruling', 'ruling application', 'oral ruling',
    'product ruling', 'class ruling', 'binding', 'non-binding',

    # NEW ADDITIONS - Penalties
    'administrative penalty', 'shortfall penalty', 'false or misleading statement',
    'lack of reasonable care', 'recklessness', 'intentional disregard',
    'shortfall interest charge', 'general interest charge',
    'voluntary disclosure', 'remission'
]

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
TO IMPLEMENT:

1. Open: src/ingestion/classification_config.py

2. Find each section and REPLACE the existing list with the ENHANCED version:

   'Admin_Migration': ADMIN_MIGRATION_ENHANCED,
   'Admin_Social_Security': ADMIN_SOCIAL_SECURITY_ENHANCED,
   'Admin_Veterans': ADMIN_VETERANS_ENHANCED,
   'Admin_Judicial_Review': ADMIN_JUDICIAL_REVIEW_ENHANCED,

   'Tax_Income': TAX_INCOME_ENHANCED,
   'Tax_CGT': TAX_CGT_ENHANCED,
   'Tax_GST': TAX_GST_ENHANCED,
   'Tax_Corporate': TAX_CORPORATE_ENHANCED,
   'Tax_FBT': TAX_FBT_ENHANCED,
   'Tax_State': TAX_STATE_ENHANCED,
   'Tax_Avoidance': TAX_AVOIDANCE_ENHANCED,

3. TEST by running classification on known test cases:
   - Migration Direction 90 case
   - Division 7A loan case
   - Part IVA scheme case
   - NDIS plan review case

4. MONITOR classification accuracy improvement via existing metrics

EXPECTED IMPACT:
- Admin_Migration: +30% coverage (Direction cases, visa subclass cases)
- Tax_Income: +25% coverage (Div 7A, s100A cases)
- Tax_Corporate: +35% coverage (Consolidation cases)
- Tax_Avoidance: +40% coverage (Part IVA, objection cases)
- Tax_State: +15% coverage (Grouping cases)

ESTIMATED TIME TO IMPLEMENT: 15 minutes
TESTING TIME: 30 minutes
TOTAL: 45 minutes
"""
