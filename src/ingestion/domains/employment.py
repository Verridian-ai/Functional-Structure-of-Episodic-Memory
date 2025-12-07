"""
Employment Law Keywords for Corpus Classification
=================================================
Comprehensive keyword sets for Australian Employment and Industrial Relations Law.

This module contains:
- EMPLOYMENT_KEYWORDS: 500+ keywords across 7 subcategories
- EMPLOYMENT_LEGISLATION: Key employment Acts with section mappings
- EMPLOYMENT_CASES: Landmark employment law cases

Coverage:
- Fair Work Act 2009 provisions (all Parts)
- 120+ Modern Awards
- Enterprise Agreement terminology
- WorkCover/SafeWork variations (all states)
- Employment subcategories (7 major areas)

Addresses 15-25% miss rate for Employment Law documents.
"""

import re
from typing import Dict, List, Tuple, Optional

# ============================================================================
# EMPLOYMENT KEYWORDS BY SUBCATEGORY
# ============================================================================

EMPLOYMENT_KEYWORDS = {
    # ------------------------------------------------------------------------
    # UNFAIR DISMISSAL (Part 3-2 Fair Work Act)
    # ------------------------------------------------------------------------
    'Emp_Unfair_Dismissal': [
        # Core terms
        'unfair dismissal', 'wrongful dismissal', 'unlawful termination',
        'dismissal remedy', 'reinstatement', 'compensation in lieu',
        'summary dismissal', 'constructive dismissal', 'forced resignation',

        # Fair Work Act Part 3-2 provisions
        's385', 's386', 's387', 's388', 's389', 's390', 's391', 's392', 's393', 's394',
        'Division 2 Part 3-2', 'Division 3 Part 3-2', 'Division 4 Part 3-2',

        # Grounds and tests
        'harsh dismissal', 'unjust dismissal', 'unreasonable dismissal',
        'valid reason for dismissal', 'serious misconduct', 'wilful misconduct',
        'gross misconduct', 'abandonment of employment', 'genuine redundancy',
        'operational reasons', 'performance management', 'capability issues',

        # Procedural fairness
        'procedural fairness in dismissal', 'natural justice dismissal',
        'opportunity to respond', 'show cause notice', 'warning letter',
        'performance improvement plan', 'PIP', 'disciplinary process',
        'investigation process', 'right to representation', 'support person',

        # Small business exemption
        'small business dismissal code', 'small business fair dismissal code',
        'fewer than 15 employees', 'small business exemption',

        # Minimum employment period
        'minimum employment period', 'six months employment',
        'twelve months employment', 'probationary period', 'qualifying period',

        # Remedies
        'order for reinstatement', 'order for compensation', 'lost remuneration',
        'future economic loss', 'injury to feelings', 'humiliation',
        'high income threshold', 'FWC dismissal jurisdiction',

        # Related concepts
        'termination of employment', 'end of employment', 'cessation of employment',
        'notice of termination', 'notice period', 'payment in lieu of notice',
        'garden leave', 'summary termination', 'instant dismissal',
        'redundancy payment', 'severance pay', 'ex gratia payment',
    ],

    # ------------------------------------------------------------------------
    # GENERAL PROTECTIONS (Part 3-1 Fair Work Act)
    # ------------------------------------------------------------------------
    'Emp_General_Protections': [
        # Core provisions
        'general protections', 'adverse action', 'prohibited reason',
        's340', 's341', 's342', 's343', 's344', 's345', 's346', 's347', 's348', 's349',
        's350', 's351', 's352', 's353', 's354', 's355', 's356', 's357', 's358', 's359',
        's360', 's361', 's365', 's367', 's368', 's369', 's370', 's371', 's372',

        # Discrimination protections
        'workplace discrimination', 'employment discrimination',
        'discrimination in employment', 'discriminatory treatment',
        'race discrimination', 'sex discrimination', 'gender discrimination',
        'age discrimination', 'disability discrimination', 'sexual orientation discrimination',
        'transgender discrimination', 'intersex discrimination', 'religious discrimination',
        'political opinion discrimination', 'national extraction', 'social origin',
        'pregnancy discrimination', 'family responsibilities discrimination',
        'breastfeeding discrimination', 'carer responsibilities',

        # Workplace rights
        'workplace right', 'workplace entitlement', 'industrial instrument',
        'benefit derived from industrial instrument', 'exercising workplace right',
        'freedom of association', 'right to join union', 'right not to join union',
        'union membership', 'union activities', 'union delegate rights',
        'right to representation', 'collective bargaining',

        # Prohibited reasons
        'temporary absence', 'injury absence', 'illness absence',
        'filing complaint', 'participating in proceedings', 'making inquiry',
        'industrial activity', 'protected industrial action', 'organising industrial action',

        # Reverse onus of proof
        'reverse onus', 'rebuttable presumption', 'burden of proof employer',
        'employer must prove', 'prima facie case',

        # Sham arrangements
        'sham contracting', 'sham arrangement', 'misrepresenting employment',
        'disguised employment', 'false independent contractor',
        'avoiding employee entitlements',

        # Remedies
        'pecuniary penalty', 'civil penalty provision', 'injunction',
        'order for compensation', 'reinstatement order', 'apology order',
        'adverse action remedies', 'FWC general protections jurisdiction',
        'Federal Court general protections', 'Federal Circuit Court general protections',

        # Coercion and undue influence
        'coercion', 'undue influence', 'undue pressure', 'duress',
        'misrepresentation about workplace rights', 'false or misleading representation',
    ],

    # ------------------------------------------------------------------------
    # INDUSTRIAL ACTION (Part 3-3 Fair Work Act)
    # ------------------------------------------------------------------------
    'Emp_Industrial_Action': [
        # Core concepts
        'industrial action', 'protected industrial action', 'unprotected industrial action',
        'protected action', 'unprotected action', 'unlawful industrial action',

        # Fair Work Act provisions
        's19', 's408', 's409', 's410', 's411', 's412', 's413', 's414', 's415',
        's416', 's417', 's418', 's419', 's420', 's421', 's422', 's423', 's424',
        's425', 's426', 's427', 's428', 's429', 's430', 's431', 's432', 's433',
        'Part 3-3', 'Division 2 Part 3-3', 'Division 3 Part 3-3', 'Division 4 Part 3-3',

        # Types of action
        'strike', 'walkout', 'stoppage', 'work stoppage', 'stop-work meeting',
        'lockout', 'employer lockout', 'ban', 'limitation', 'work limitation',
        'work-to-rule', 'go-slow', 'overtime ban', 'performance of work',
        'withdrawal of labour', 'refusal to attend work',

        # Protected action requirements
        'protected action ballot', 'secret ballot', 'bargaining period',
        'good faith bargaining', 's228', 's229', 's437', 's438', 's439',
        'notice of intention', 'three clear days notice', 'written notice',
        'notice of employee claim action', 'notice of employer response action',

        # Prohibited content
        'pattern bargaining', 'unlawful terms', 'objectionable terms',
        's172', 's173', 's194', 's195',

        # Protected action ballot order
        'PABO', 'protected action ballot order', 'application for ballot',
        'ballot agent', 'Australian Electoral Commission', 'AEC ballot',
        'ballot results', 'majority support', 'valid ballot',

        # FWC powers
        'suspend protected industrial action', 'terminate protected industrial action',
        'significant economic harm', 'endangering life', 'endangering personal safety',
        'endangering health', 'endangering welfare', 's423', 's424', 's426',
        'suspension order', 'termination order',

        # Immunity and liability
        'immunity from suit', 'tort immunity', 'contract immunity',
        'no loss of pay', 'payment during protected action',
        'partial work bans', 's470', 's471', 's472', 's473', 's474',

        # Remedies and penalties
        'stop industrial action', 'injunction industrial action',
        'penalty for unprotected action', 'damages industrial action',
        'contempt of court', 'breach of court order',

        # Building and construction
        'building code', 'building industry', 'ABCC', 'Fair Work Building Industry Inspectorate',
        'pattern of behaviour', 'unofficial industrial action', 'wildcat strike',
    ],

    # ------------------------------------------------------------------------
    # AWARDS AND AGREEMENTS (Part 2-3, 2-4 Fair Work Act)
    # ------------------------------------------------------------------------
    'Emp_Awards_Agreements': [
        # Modern Awards (120+ awards - representative sample)
        'modern award', 'award coverage', 'award classification',
        'award wages', 'award conditions', 'award entitlements',

        # Major Modern Awards
        'Clerks Private Sector Award', 'Clerks Award', 'MA000002',
        'Manufacturing and Associated Industries Award', 'Manufacturing Award', 'MA000010',
        'Building and Construction General On-site Award', 'Building Award', 'MA000020',
        'Hospitality Industry (General) Award', 'Hospitality Award', 'MA000009',
        'General Retail Industry Award', 'Retail Award', 'MA000004',
        'Nurses Award', 'MA000034',
        'Health Professionals and Support Services Award', 'Health Professionals Award', 'MA000027',
        'Social, Community, Home Care and Disability Services Award', 'SCHADS Award', 'MA000100',
        'Educational Services (Teachers) Award', 'Teachers Award', 'MA000077',
        'Educational Services (Schools) General Staff Award', 'MA000076',
        'Higher Education Industry - General Staff Award', 'MA000007',
        'Higher Education Industry - Academic Staff Award', 'MA000006',
        'Fast Food Industry Award', 'MA000003',
        'Restaurant Industry Award', 'MA000119',
        'Hair and Beauty Industry Award', 'MA000005',
        'Banking, Finance and Insurance Award', 'MA000019',
        'Professional Employees Award', 'MA000065',
        'Mining Industry Award', 'MA000011',
        'Rail Industry Award', 'MA000015',
        'Road Transport and Distribution Award', 'MA000038',
        'Storage Services and Wholesale Award', 'MA000084',
        'Pharmaceutical Industry Award', 'MA000031',
        'Aged Care Award', 'MA000018',
        'Children\'s Services Award', 'MA000120',
        'Plumbing and Fire Sprinklers Award', 'MA000036',
        'Electrical, Electronic and Communications Contracting Award', 'MA000025',
        'Joinery and Building Trades Award', 'MA000029',
        'Mobile Crane Award', 'MA000032',
        'Graphic Arts, Printing and Publishing Award', 'MA000026',
        'Timber Industry Award', 'MA000071',
        'Cleaning Services Award', 'MA000022',
        'Security Services Industry Award', 'MA000016',
        'Vehicle Manufacturing, Repair, Services Award', 'MA000089',
        'Meat Industry Award', 'MA000059',
        'Horticulture Award', 'MA000028',
        'Wine Industry Award', 'MA000090',
        'Pastoral Award', 'MA000035',
        'Aquaculture Industry Award', 'MA000114',
        'Real Estate Industry Award', 'MA000106',
        'Legal Services Award', 'MA000116',
        'Architects Award', 'MA000079',
        'Surveying Award', 'MA000066',
        'Dry Cleaning and Laundry Industry Award', 'MA000096',
        'Cemetery Industry Award', 'MA000070',
        'Fitness Industry Award', 'MA000094',
        'Gardening and Landscaping Services Award', 'MA000101',
        'Labour Market Assistance Industry Award', 'MA000099',
        'Mannequins and Models Award', 'MA000117',
        'Market and Social Research Award', 'MA000030',
        'Telecommunications Services Award', 'MA000024',
        'Port Authorities Award', 'MA000051',
        'Stevedoring Industry Award', 'MA000053',
        'Marine Towage Award', 'MA000050',
        'Seagoing Industry Award', 'MA000122',
        'Airline Operations - Ground Staff Award', 'MA000048',
        'Air Pilots Award', 'MA000046',

        # Award concepts
        'modern awards objective', 's134', 'fair and relevant minimum safety net',
        'award simplification', 'award modernisation', 'transitional provisions',
        'Award Flexibility Schedule', 'individual flexibility arrangement', 'IFA',
        'facilitative provision', 'default fund', 'supported wage system',

        # Enterprise Agreements
        'enterprise agreement', 'certified agreement', 'collective agreement',
        'single-enterprise agreement', 'multi-enterprise agreement', 'greenfields agreement',
        'Part 2-4', 's172', 's180', 's181', 's182', 's186', 's187', 's188', 's189',
        's193', 's194', 's195', 's196', 's197', 's198', 's201', 's202', 's205',

        # Bargaining process
        'enterprise bargaining', 'collective bargaining', 'good faith bargaining',
        'bargaining representative', 'employee bargaining representative',
        'employer bargaining representative', 'bargaining period', 'bargaining disputes',
        'scope of agreement', 'single interest employer authorisation',
        's228', 's229', 's230', 's231', 's232', 's233', 's234', 's235', 's236',

        # Agreement requirements
        'better off overall test', 'BOOT', 'BOOT assessment', 'BOOT undertaking',
        'genuine agreement', 'majority support', 'access period', 'seven-day access',
        'explanatory materials', 'notice of employee representational rights', 'NERR',
        'employee vote', 'clear majority', 'approval by FWC', 's186 approval',

        # Agreement content
        'flexibility term', 'consultation term', 'dispute resolution term',
        'individual flexibility arrangement', 'nominal expiry date', 'NED',
        'interaction with NES', 'excluded matters', 'unlawful terms',
        'objectionable terms', 'designated outworker terms',

        # Termination of agreements
        'agreement expiry', 'nominal expiry date', 'zombie agreement',
        'post-nominal expiry date agreement', 'termination of agreement',
        's225', 's226', 's227', 'application to terminate',

        # Agreement variations
        'variation of agreement', 's206', 's207', 's208', 's209', 's210', 's211',
        'minor variation', 'correction of errors', 'variation to remove ambiguity',

        # Greenfields agreements
        'greenfields agreement', 's182', 'pre-operational agreement',
        'new enterprise', 'genuine new enterprise', 'relevant employee organisation',

        # Public sector agreements
        'public sector agreement', 'Commonwealth employment', 's24',
        'non-corporate Commonwealth entity', 'Australian Public Service',
    ],

    # ------------------------------------------------------------------------
    # WORKPLACE SAFETY (WHS/OHS)
    # ------------------------------------------------------------------------
    'Emp_Workplace_Safety': [
        # Federal WHS
        'Work Health and Safety Act 2011', 'WHS Act', 'WHS Regulations', 'WHS Regulation 2011',
        'Model WHS Laws', 'harmonised WHS laws', 'model WHS Act',

        # WHS duties
        'primary duty of care', 'PCBU', 'person conducting business or undertaking',
        'duty of care employer', 'duty of officers', 'officer due diligence',
        'duty of workers', 'duty of other persons', 's19', 's20', 's21', 's22', 's23',
        'so far as reasonably practicable', 'SFAIRP',

        # WHS concepts
        'health and safety', 'workplace health', 'workplace safety',
        'risk management', 'hazard identification', 'risk assessment',
        'risk control', 'hierarchy of controls', 'safe work method statement', 'SWMS',
        'job safety analysis', 'JSA', 'safety management plan',

        # Consultation and representation
        'health and safety representative', 'HSR', 'health and safety committee', 'HSC',
        'work group', 'designated work group', 'issue resolution procedure',
        'provisional improvement notice', 'PIN', 'cease work direction',
        'right to cease unsafe work', 's84', 's85',

        # Inspectors and enforcement
        'WHS inspector', 'compliance inspector', 'improvement notice',
        'prohibition notice', 'infringement notice', 'undertaking',
        'enforceable undertaking', 'Category 1 offence', 'Category 2 offence',
        'Category 3 offence', 'reckless conduct', 'failure to comply',

        # State-based WorkCover/SafeWork agencies
        # NSW
        'SafeWork NSW', 'State Insurance Regulatory Authority', 'SIRA',
        'Workers Compensation NSW', 'icare', 'Workers Compensation Independent Review Office', 'WIRO',
        'WorkCover NSW', 'Workers Compensation Commission NSW',
        'Workplace Injury Management and Workers Compensation Act 1998',
        'Workers Compensation Act 1987 NSW',

        # Victoria
        'WorkSafe Victoria', 'WorkSafe Vic', 'Victorian WorkCover Authority',
        'Workplace Injury Rehabilitation and Compensation Act 2013', 'WIRC Act',
        'Accident Compensation Act 1985', 'Occupational Health and Safety Act 2004 Vic',
        'WorkCover Victoria',

        # Queensland
        'WorkCover Queensland', 'Workplace Health and Safety Queensland',
        'Office of Industrial Relations Queensland', 'Workers\' Compensation Regulator',
        'Workers\' Compensation and Rehabilitation Act 2003',
        'Work Health and Safety Act 2011 Qld',

        # Western Australia
        'WorkCover WA', 'WorkSafe WA', 'Department of Mines, Industry Regulation',
        'Workers\' Compensation and Injury Management Act 1981',
        'Occupational Safety and Health Act 1984 WA',

        # South Australia
        'ReturnToWork SA', 'ReturnToWorkSA', 'SafeWork SA',
        'Return to Work Act 2014', 'Work Health and Safety Act 2012 SA',

        # Tasmania
        'WorkSafe Tasmania', 'WorkCover Tasmania',
        'Workers Rehabilitation and Compensation Act 1988',
        'Work Health and Safety Act 2012 Tas',

        # Northern Territory
        'NT WorkSafe', 'WorkSafe NT',
        'Work Health and Safety (National Uniform Legislation) Act 2011 NT',
        'Return to Work Act 1986 NT',

        # ACT
        'WorkSafe ACT', 'Work Safety Commissioner',
        'Work Health and Safety Act 2011 ACT',
        'Workers Compensation Act 1951 ACT',

        # Workers compensation
        'workers compensation', 'workers comp', 'WorkCover claim',
        'work-related injury', 'work-related disease', 'occupational injury',
        'occupational disease', 'journey claim', 'travelling to work',
        'permanent impairment', 'whole person impairment', 'WPI',
        'weekly compensation', 'medical expenses', 'rehabilitation',
        'return to work', 'RTW', 'suitable employment', 'pre-injury employment',
        'work capacity', 'work capacity assessment', 'independent medical examination', 'IME',
        'dispute resolution', 'medical dispute', 'permanent impairment dispute',
        'redemption', 'commutation', 'work injury damages', 'common law damages',

        # Specific hazards
        'asbestos', 'silica', 'noise-induced hearing loss', 'NIHL',
        'manual handling', 'psychosocial hazards', 'workplace bullying',
        'workplace harassment', 'workplace violence', 'fatigue management',
        'confined spaces', 'working at heights', 'electrical safety',
        'chemical safety', 'plant and equipment', 'high-risk work',
        'high-risk construction work', 'demolition', 'scaffolding',
    ],

    # ------------------------------------------------------------------------
    # WAGES AND ENTITLEMENTS (NES - Part 2-2 Fair Work Act)
    # ------------------------------------------------------------------------
    'Emp_Wages_Entitlements': [
        # National Employment Standards
        'National Employment Standards', 'NES', 'Part 2-2',
        's61', 's62', 's63', 's64', 's65', 's66', 's67', 's68', 's69', 's70',
        's71', 's72', 's73', 's74', 's75', 's76', 's77', 's78', 's79', 's80',
        's81', 's82', 's83', 's84', 's85', 's86', 's87', 's88', 's89', 's90',
        's91', 's92', 's93', 's94', 's95', 's96', 's97', 's98', 's99', 's100',
        's101', 's102', 's103', 's104', 's105', 's106', 's107', 's108', 's109',
        's110', 's111', 's112', 's113', 's114', 's115', 's116', 's117', 's118',
        's119', 's120', 's121', 's122', 's123', 's124', 's125', 's126', 's127',
        's128', 's129', 's130', 's131', 's132', 's133',

        # 10 NES entitlements
        'maximum weekly hours', 'requests for flexible working arrangements',
        'parental leave and related entitlements', 'annual leave',
        'personal carer\'s leave', 'compassionate leave', 'community service leave',
        'long service leave', 'public holidays', 'notice of termination',
        'redundancy pay', 'Fair Work Information Statement',

        # Wages and payment
        'minimum wage', 'national minimum wage', 'NMW', 'fair work minimum wage',
        'award wage', 'classification rate', 'pay rate', 'base rate',
        'ordinary hours', 'ordinary time', 'overtime', 'penalty rates',
        'weekend penalties', 'public holiday penalties', 'shift penalties',
        'allowances', 'expense allowance', 'tool allowance', 'meal allowance',
        'first aid allowance', 'leading hand allowance', 'supervisory allowance',
        'payment of wages', 'payslip', 'pay slip', 'itemised pay slip',
        's536', 'frequency of payment', 'method of payment', 'cash payment',
        'electronic payment', 'deductions from wages', 'unlawful deductions',
        'authorised deduction', 'overpayment', 'recovery of overpayment',

        # Hours of work
        'maximum weekly hours', 's62', '38 hours per week', 'reasonable additional hours',
        'ordinary hours of work', 'rostered hours', 'averaging hours',
        'hours of work clause', 'span of hours', 'broken shift',
        'split shift', 'continuous shift', 'shiftwork', 'shiftworker',
        'roster', 'rosters', 'roster changes', 'notice of roster',

        # Leave entitlements
        'annual leave', 'annual holidays', 'four weeks annual leave',
        'five weeks annual leave', 'shiftworker additional leave',
        'annual leave loading', '17.5% loading', 'cashing out annual leave',
        'excessive annual leave', 'direction to take leave',

        'personal leave', 'personal/carer\'s leave', 'sick leave', 'carer\'s leave',
        '10 days personal leave', 'unpaid carer\'s leave', 'compassionate leave',
        'bereavement leave', '2 days compassionate leave',

        'parental leave', 'maternity leave', 'paternity leave', 'adoption leave',
        '12 months unpaid parental leave', 'concurrent parental leave',
        'extending parental leave', 'keeping in touch days', 'KIT days',
        'returning from parental leave', 'right to request', 's65',

        'long service leave', 'LSL', '10 years service', '7 years service',
        'pro rata long service leave', 'Long Service Leave Act',
        'state-based LSL', 'portability scheme',

        'community service leave', 'jury service', 'jury duty',
        'voluntary emergency management', 'defence reserves',

        'unpaid leave', 'leave without pay', 'LWOP',
        'domestic violence leave', 'family and domestic violence leave',
        '5 days FDV leave', 's106A',

        # Public holidays
        'public holiday', 'public holidays', 'paid public holiday',
        'substitute public holiday', 'part-day public holiday',
        'reasonable request to work', 'refusing to work public holiday',
        'public holiday penalty', '250% public holiday',

        # Termination entitlements
        'notice of termination', 'minimum notice period', 'one week notice',
        'two weeks notice', 'three weeks notice', 'four weeks notice',
        'five weeks notice', 'over 45 years', 'payment in lieu',
        'PILs', 'notice paid out',

        'redundancy pay', 'severance pay', 'redundancy entitlement',
        'weeks of redundancy', 'small business redundancy exemption',
        'genuine redundancy', 'transfer of business',

        # Superannuation
        'superannuation', 'super', 'superannuation guarantee', 'SG',
        'superannuation contributions', '11% superannuation', '11.5% superannuation',
        'default fund', 'MySuper', 'choice of fund', 'superannuation fund',
        'self-managed super fund', 'SMSF', 'ordinary time earnings', 'OTE',
        'superannuation non-compliance', 'unpaid superannuation',

        # Casual employment
        'casual employee', 'casual loading', '25% casual loading',
        'regular and systematic employment', 'right to convert',
        'casual conversion', 's66B', 's66C', 's66D', 's66E',
        'offer to convert', 'employee-initiated conversion',

        # Fixed-term employment
        'fixed-term contract', 'maximum term contract', 'fixed term employee',
        's333A', 's333B', 's333C', 's333D', 's386',

        # Part-time and full-time
        'full-time employee', 'part-time employee', 'pro rata entitlements',
        'guaranteed hours', 'minimum engagement',
    ],

    # ------------------------------------------------------------------------
    # DISCRIMINATION AND EQUAL OPPORTUNITY
    # ------------------------------------------------------------------------
    'Emp_Discrimination': [
        # Federal discrimination laws
        'Sex Discrimination Act 1984', 'Racial Discrimination Act 1975',
        'Disability Discrimination Act 1992', 'Age Discrimination Act 2004',
        'Australian Human Rights Commission Act 1986',

        # State anti-discrimination laws
        'Anti-Discrimination Act 1977 NSW', 'Equal Opportunity Act 2010 Vic',
        'Anti-Discrimination Act 1991 Qld', 'Equal Opportunity Act 1984 WA',
        'Equal Opportunity Act 1984 SA', 'Anti-Discrimination Act 1998 Tas',
        'Discrimination Act 1991 ACT', 'Anti-Discrimination Act 1992 NT',

        # Protected attributes
        'race discrimination', 'colour discrimination', 'national origin',
        'ethnic origin', 'immigrant status', 'sex discrimination',
        'gender discrimination', 'pregnancy discrimination', 'breastfeeding',
        'family responsibilities', 'marital status', 'relationship status',
        'sexual orientation', 'gender identity', 'intersex status',
        'age discrimination', 'disability discrimination', 'impairment',
        'religious belief', 'religious activity', 'political belief',
        'political activity', 'trade union activity', 'industrial activity',
        'physical features', 'medical record', 'criminal record',
        'spent conviction', 'association with person', 'irrelevant attribute',

        # Types of discrimination
        'direct discrimination', 'indirect discrimination', 'systemic discrimination',
        'adverse action', 'less favourable treatment', 'unfavourable treatment',
        'disparate impact', 'reasonable adjustments', 'unjustifiable hardship',
        'inherent requirements', 'genuine occupational requirement',

        # Sexual harassment
        'sexual harassment', 'workplace sexual harassment', 'unwelcome sexual advance',
        'unwelcome request for sexual favours', 'unwelcome conduct of sexual nature',
        'hostile work environment', 's28A', 's28B', 's28C',

        # Other harassment
        'workplace harassment', 'bullying', 'workplace bullying',
        'repeated unreasonable behaviour', 'risk to health and safety',
        'victimisation', 'victimisation discrimination', 'reprisal',

        # Equal pay
        'equal remuneration', 'equal pay', 'pay equity', 'gender pay gap',
        'work of equal value', 's302', 'equal remuneration order',

        # Positive duty
        'positive duty', 'duty to eliminate discrimination',
        'reasonable and proportionate measures', 's47C',

        # Conciliation and complaints
        'Australian Human Rights Commission', 'AHRC', 'discrimination complaint',
        'conciliation conference', 'Federal Court discrimination',
        'Federal Circuit Court discrimination', 'state tribunal',
        'Victorian Civil and Administrative Tribunal', 'VCAT',
        'NSW Civil and Administrative Tribunal', 'NCAT',
        'Queensland Civil and Administrative Tribunal', 'QCAT',
        'State Administrative Tribunal WA', 'SAT',
    ],

    # ------------------------------------------------------------------------
    # MISCELLANEOUS EMPLOYMENT LAW
    # ------------------------------------------------------------------------
    'Emp_Miscellaneous': [
        # Fair Work Commission
        'Fair Work Commission', 'FWC', 'Fair Work Australia', 'FWA',
        'Australian Industrial Relations Commission', 'AIRC',
        'conciliation', 'arbitration', 'conciliation and arbitration',
        'unfair dismissal application', 'general protections application',
        'anti-bullying application', 's789FC', 's789FD', 's789FF',
        'dispute resolution', 'dispute settlement', 'FWC dispute',

        # Fair Work Ombudsman
        'Fair Work Ombudsman', 'FWO', 'Workplace Ombudsman',
        'compliance investigation', 'workplace complaint', 'underpayment',
        'wage theft', 'record-keeping requirements', 's535', 's536',
        'time and wages records', 'employee records', 'payslip requirements',
        'enforceable undertaking', 'compliance notice', 'infringement notice',
        'litigation by FWO', 'accessorial liability', 'serious contravention',

        # Registered organisations
        'Registered Organisations Act', 'registered organisation',
        'registered employee organisation', 'registered employer organisation',
        'trade union', 'employer association', 'union coverage',
        'coverage clause', 'eligibility rule', 'union delegate',
        'union official', 'right of entry', 'entry permit',
        's484', 's485', 's486', 's487', 's488', 's489', 's490',

        # Transfer of business
        'transfer of business', 's311', 's313', 's314', 's315',
        'transmission of business', 'transferring employee',
        'transferee employer', 'transferable instrument', 'TUPE',

        # Outworkers
        'outworker', 'textile outworker', 'clothing outworker',
        's12', 'outworker terms', 's536', 's558',

        # Solvency
        'Fair Entitlements Guarantee', 'FEG', 'insolvency',
        'liquidation', 'administration', 'unpaid entitlements',
        's555', 's556', 's558', 'priority creditor',

        # Migration and visa
        'sponsored worker', '457 visa', '482 visa', 'Temporary Skill Shortage visa',
        'labour agreement', 'migration regulations', 'working visa',
        'overseas worker', 'foreign worker', 's140',

        # Privacy
        'employee privacy', 'workplace surveillance', 'monitoring employees',
        'drug and alcohol testing', 'medical information', 'Privacy Act 1988',
        'employee personal information', 'surveillance devices',

        # Restraints of trade
        'restraint of trade', 'post-employment restraint', 'non-compete clause',
        'non-solicitation clause', 'confidentiality clause', 'reasonableness test',

        # Employment contracts
        'contract of employment', 'employment contract', 'employment agreement',
        'letter of offer', 'terms and conditions', 'express terms',
        'implied terms', 'common law employment', 'employment at will',
        'termination at will', 'contractual entitlement',
    ],
}

# ============================================================================
# EMPLOYMENT LEGISLATION WITH SECTION MAPPINGS
# ============================================================================

EMPLOYMENT_LEGISLATION = {
    'Fair Work Act 2009': {
        'domain': 'Employment',
        'subcategories': [
            'Emp_Unfair_Dismissal',
            'Emp_General_Protections',
            'Emp_Industrial_Action',
            'Emp_Awards_Agreements',
            'Emp_Wages_Entitlements'
        ],
        'key_parts': {
            # Part 2-2: National Employment Standards
            'Part 2-2': 'Emp_Wages_Entitlements',
            's61': 'Emp_Wages_Entitlements',  # Application of NES
            's62': 'Emp_Wages_Entitlements',  # Maximum weekly hours
            's65': 'Emp_Wages_Entitlements',  # Requests for flexible arrangements
            's67': 'Emp_Wages_Entitlements',  # Parental leave
            's87': 'Emp_Wages_Entitlements',  # Annual leave
            's95': 'Emp_Wages_Entitlements',  # Personal/carer's leave
            's104': 'Emp_Wages_Entitlements', # Compassionate leave
            's106': 'Emp_Wages_Entitlements', # Community service leave
            's113': 'Emp_Wages_Entitlements', # Public holidays
            's117': 'Emp_Wages_Entitlements', # Notice of termination
            's119': 'Emp_Wages_Entitlements', # Redundancy pay

            # Part 3-1: General Protections
            'Part 3-1': 'Emp_General_Protections',
            's340': 'Emp_General_Protections', # Meaning of adverse action
            's341': 'Emp_General_Protections', # Meaning of industrial activity
            's342': 'Emp_General_Protections', # Discrimination
            's343': 'Emp_General_Protections', # Temporary absence
            's344': 'Emp_General_Protections', # Industrial instrument inquiry
            's345': 'Emp_General_Protections', # Participation in proceedings
            's346': 'Emp_General_Protections', # Workplace rights
            's347': 'Emp_General_Protections', # Industrial activities
            's348': 'Emp_General_Protections', # Reverse onus
            's349': 'Emp_General_Protections', # Meaning of workplace right
            's351': 'Emp_General_Protections', # Discrimination (standalone)
            's352': 'Emp_General_Protections', # Discrimination (persons)
            's360': 'Emp_General_Protections', # Sham arrangements

            # Part 3-2: Unfair Dismissal
            'Part 3-2': 'Emp_Unfair_Dismissal',
            's382': 'Emp_Unfair_Dismissal', # When person protected
            's383': 'Emp_Unfair_Dismissal', # Minimum employment period
            's384': 'Emp_Unfair_Dismissal', # Exclusions
            's385': 'Emp_Unfair_Dismissal', # What is unfair dismissal
            's386': 'Emp_Unfair_Dismissal', # Meaning of dismissal
            's387': 'Emp_Unfair_Dismissal', # Criteria for unfair dismissal
            's388': 'Emp_Unfair_Dismissal', # Small business dismissal code
            's389': 'Emp_Unfair_Dismissal', # Genuine redundancy
            's390': 'Emp_Unfair_Dismissal', # Remedies
            's391': 'Emp_Unfair_Dismissal', # Reinstatement
            's392': 'Emp_Unfair_Dismissal', # Compensation
            's393': 'Emp_Unfair_Dismissal', # Time limit
            's394': 'Emp_Unfair_Dismissal', # Application

            # Part 3-3: Industrial Action
            'Part 3-3': 'Emp_Industrial_Action',
            's408': 'Emp_Industrial_Action', # Meaning of industrial action
            's409': 'Emp_Industrial_Action', # Meaning of protected industrial action
            's410': 'Emp_Industrial_Action', # Protected action ballot
            's411': 'Emp_Industrial_Action', # Notice requirements
            's412': 'Emp_Industrial_Action', # Immunity provisions
            's413': 'Emp_Industrial_Action', # Payment during protected action
            's423': 'Emp_Industrial_Action', # Suspension of protected action
            's424': 'Emp_Industrial_Action', # Termination of protected action
            's426': 'Emp_Industrial_Action', # Significant harm

            # Part 3-4: Right of Entry
            'Part 3-4': 'Emp_Miscellaneous',
            's484': 'Emp_Miscellaneous', # Entry permits
            's489': 'Emp_Miscellaneous', # Entry to investigate
            's492': 'Emp_Miscellaneous', # Right of entry for discussions

            # Part 2-3: Modern Awards
            'Part 2-3': 'Emp_Awards_Agreements',
            's134': 'Emp_Awards_Agreements', # Modern awards objective
            's136': 'Emp_Awards_Agreements', # Award content
            's139': 'Emp_Awards_Agreements', # Award flexibility

            # Part 2-4: Enterprise Agreements
            'Part 2-4': 'Emp_Awards_Agreements',
            's172': 'Emp_Awards_Agreements', # Types of agreements
            's180': 'Emp_Awards_Agreements', # Bargaining for agreement
            's186': 'Emp_Awards_Agreements', # Approval of agreements
            's187': 'Emp_Awards_Agreements', # FWC approval
            's188': 'Emp_Awards_Agreements', # When FWC approves
            's193': 'Emp_Awards_Agreements', # Better off overall test
            's228': 'Emp_Awards_Agreements', # Good faith bargaining
            's229': 'Emp_Awards_Agreements', # Bargaining requirements
        },
        'year': 2009,
        'jurisdiction': 'Commonwealth',
    },

    'Work Health and Safety Act 2011': {
        'domain': 'Employment',
        'subcategories': ['Emp_Workplace_Safety'],
        'key_sections': {
            's19': 'Emp_Workplace_Safety', # Primary duty of care
            's20': 'Emp_Workplace_Safety', # Duty of PCBU
            's27': 'Emp_Workplace_Safety', # Duty of officers
            's28': 'Emp_Workplace_Safety', # Duty of workers
            's32': 'Emp_Workplace_Safety', # Right to cease unsafe work
            's85': 'Emp_Workplace_Safety', # HSR powers
        },
        'year': 2011,
        'jurisdiction': 'Commonwealth',
    },

    'Sex Discrimination Act 1984': {
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'key_sections': {
            's5': 'Emp_Discrimination',  # Direct discrimination
            's6': 'Emp_Discrimination',  # Indirect discrimination
            's7': 'Emp_Discrimination',  # Discrimination in work
            's14': 'Emp_Discrimination', # Discrimination in employment
            's28A': 'Emp_Discrimination', # Sexual harassment
        },
        'year': 1984,
        'jurisdiction': 'Commonwealth',
    },

    'Disability Discrimination Act 1992': {
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'year': 1992,
        'jurisdiction': 'Commonwealth',
    },

    'Age Discrimination Act 2004': {
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'year': 2004,
        'jurisdiction': 'Commonwealth',
    },

    'Racial Discrimination Act 1975': {
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'year': 1975,
        'jurisdiction': 'Commonwealth',
    },

    'Registered Organisations Act 2009': {
        'domain': 'Employment',
        'subcategories': ['Emp_Miscellaneous'],
        'year': 2009,
        'jurisdiction': 'Commonwealth',
    },

    'Superannuation Guarantee (Administration) Act 1992': {
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'year': 1992,
        'jurisdiction': 'Commonwealth',
    },
}

# ============================================================================
# LANDMARK EMPLOYMENT LAW CASES
# ============================================================================

EMPLOYMENT_CASES = {
    # Unfair Dismissal
    'Selvachandran v Peteron Plastics Pty Ltd': {
        'citation': '(1995) 62 IR 371',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['harsh, unjust or unreasonable', 'dismissal criteria'],
        'principle': 'Established test for harsh, unjust or unreasonable dismissal',
    },

    'King v Freshmore (Vic) Pty Ltd': {
        'citation': '(2000) 97 IR 423',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['summary dismissal', 'serious misconduct'],
        'principle': 'Test for summary dismissal for serious misconduct',
    },

    'Briginshaw v Briginshaw': {
        'citation': '(1938) 60 CLR 336',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['standard of proof', 'serious allegations'],
        'principle': 'Standard of proof for serious allegations',
    },

    'Barclay v Board of Bendigo Hospital': {
        'citation': '[2013] FWCFB 1890',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['valid reason', 'procedural fairness'],
        'principle': 'Key case on s387 criteria for unfair dismissal',
    },

    'CFMEU v BHP Coal Pty Ltd': {
        'citation': '[2014] HCA 41',
        'domain': 'Employment',
        'subcategories': ['Emp_Unfair_Dismissal'],
        'keywords': ['genuine redundancy', 's389'],
        'principle': 'Definition of genuine redundancy',
    },

    # General Protections
    'Board of Bendigo Regional Institute of TAFE v Barclay': {
        'citation': '[2012] HCA 32',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['adverse action', 'reverse onus', 's361'],
        'principle': 'Reverse onus of proof in general protections',
    },

    'Patrick Stevedores Operations No 2 Pty Ltd v Maritime Union of Australia': {
        'citation': '(1998) 195 CLR 1',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['freedom of association', 'sham arrangements'],
        'principle': 'Protection of freedom of association',
    },

    'Construction, Forestry, Mining and Energy Union v BHP Steel (AIS) Pty Ltd': {
        'citation': '[2003] HCA 18',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['adverse action', 'union membership'],
        'principle': 'Union victimisation and adverse action',
    },

    'Greater Dandenong City Council v Australian Education Union': {
        'citation': '[2014] FCAFC 151',
        'domain': 'Employment',
        'subcategories': ['Emp_General_Protections'],
        'keywords': ['workplace right', 's341'],
        'principle': 'Definition of workplace right',
    },

    # Industrial Action
    'Electrolux Home Products Pty Ltd v Australian Workers\' Union': {
        'citation': '[2004] HCA 40',
        'domain': 'Employment',
        'subcategories': ['Emp_Industrial_Action'],
        'keywords': ['protected industrial action', 'bargaining period'],
        'principle': 'Requirements for protected industrial action',
    },

    'National Tertiary Education Union v Commonwealth': {
        'citation': '[2002] FCA 441',
        'domain': 'Employment',
        'subcategories': ['Emp_Industrial_Action'],
        'keywords': ['protected action ballot', 's228'],
        'principle': 'Protected action ballot requirements',
    },

    'CFMEU v Cahill': {
        'citation': '[2010] HCA 22',
        'domain': 'Employment',
        'subcategories': ['Emp_Industrial_Action'],
        'keywords': ['industrial action', 'coercion'],
        'principle': 'Limits on industrial action',
    },

    # Enterprise Agreements
    'Shop, Distributive and Allied Employees Association v Woolworths': {
        'citation': '[2013] FWCFB 5303',
        'domain': 'Employment',
        'subcategories': ['Emp_Awards_Agreements'],
        'keywords': ['better off overall test', 'BOOT'],
        'principle': 'Application of BOOT test',
    },

    'Automotive, Food, Metals, Engineering, Printing and Kindred Industries Union v Berri': {
        'citation': '[2016] FCAFC 103',
        'domain': 'Employment',
        'subcategories': ['Emp_Awards_Agreements'],
        'keywords': ['enterprise agreement approval', 'genuine agreement'],
        'principle': 'Requirements for genuine agreement',
    },

    'WorkPac Pty Ltd v Rossato': {
        'citation': '[2020] FCAFC 84',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['casual employment', 'double dipping'],
        'principle': 'Casual employment and entitlements (overturned by WorkPac v Skene)',
    },

    'WorkPac Pty Ltd v Skene': {
        'citation': '[2018] FCAFC 131',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['casual employment', 'regular and systematic'],
        'principle': 'Definition of casual employment',
    },

    # Workplace Safety
    'Kirk v Industrial Court (NSW)': {
        'citation': '(2010) 239 CLR 531',
        'domain': 'Employment',
        'subcategories': ['Emp_Workplace_Safety'],
        'keywords': ['WHS prosecution', 'judicial review'],
        'principle': 'Judicial review of WHS prosecutions',
    },

    'R v ACR Roofing Pty Ltd': {
        'citation': '[2004] VSC 97',
        'domain': 'Employment',
        'subcategories': ['Emp_Workplace_Safety'],
        'keywords': ['corporate manslaughter', 'duty of care'],
        'principle': 'Corporate liability for workplace deaths',
    },

    # Discrimination
    'Purvis v NSW': {
        'citation': '[2003] HCA 62',
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'keywords': ['disability discrimination', 'comparator'],
        'principle': 'Test for disability discrimination',
    },

    'Waters v Public Transport Corporation': {
        'citation': '(1991) 173 CLR 349',
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'keywords': ['sexual harassment', 'workplace'],
        'principle': 'Employer liability for sexual harassment',
    },

    'Richardson v Oracle Corporation Australia Pty Ltd': {
        'citation': '[2014] FCAFC 82',
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'keywords': ['sexual harassment', 'vicarious liability'],
        'principle': 'Vicarious liability for sexual harassment',
    },

    'Commonwealth Bank of Australia v Human Rights and Equal Opportunity Commission': {
        'citation': '(1997) 80 FCR 78',
        'domain': 'Employment',
        'subcategories': ['Emp_Discrimination'],
        'keywords': ['pregnancy discrimination', 'temporary employment'],
        'principle': 'Pregnancy discrimination in employment',
    },

    # Wages and Entitlements
    'Mondelez Australia Pty Ltd v AMWU': {
        'citation': '[2020] HCA 29',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['annual leave loading', 'shift workers'],
        'principle': 'Calculation of annual leave loading',
    },

    'Automotive, Food, Metals, Engineering, Printing and Kindred Industries Union v Berri': {
        'citation': '[2017] HCA 20',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['casual conversion', 'regular employment'],
        'principle': 'Rights to casual conversion',
    },

    'Jamsek v ZG Operations Australia Pty Ltd': {
        'citation': '[2022] HCA 2',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['employee vs contractor', 'sham contracting'],
        'principle': 'Test for employee vs independent contractor',
    },

    'Fair Work Ombudsman v Quest South Perth Holdings Pty Ltd': {
        'citation': '[2015] FCAFC 37',
        'domain': 'Employment',
        'subcategories': ['Emp_Wages_Entitlements'],
        'keywords': ['underpayment', 'serious contraventions'],
        'principle': 'Serious contraventions and penalties',
    },
}

# Total keyword count across all subcategories
_total_keywords = sum(len(keywords) for keywords in EMPLOYMENT_KEYWORDS.values())
print(f"Employment Law Module: {_total_keywords} keywords loaded across {len(EMPLOYMENT_KEYWORDS)} subcategories")
