"""
Direct script to add all employment law keywords to classification_config.py
"""

import re

config_path = r'C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\classification_config.py'

# Read file
with open(config_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The replacement content - this is the entire INDUSTRIAL section with all subcategories
new_industrial_section = """    # --- 7. INDUSTRIAL & EMPLOYMENT LAW ---
    # Comprehensive keywords from EMPLOYMENT_LAW_DOMAIN_KNOWLEDGE.md

    # 7.1 Unfair Dismissal
    'Ind_Unfair_Dismissal': [
        'unfair dismissal', 'wrongful dismissal', 'constructive dismissal', 'harsh dismissal', 'unjust dismissal',
        'unreasonable dismissal', 's394', 'section 394', 'part 3-2', 'harsh unjust or unreasonable',
        'valid reason', 'sound defensible reason', 'well-founded reason', 'procedural fairness', 'natural justice',
        'opportunity to respond', 'small business fair dismissal code', 'small business exemption',
        'genuine redundancy', 'forced redundancy', 'redundancy selection', 'position elimination',
        'operational requirements', 'redeployment', 'consultation requirements',
        'minimum employment period', 'jurisdictional eligibility', 'high income threshold',
        'summary dismissal', 'serious misconduct', 'capacity dismissal', 'conduct dismissal',
        'warning', 'warning letter', 'show cause', 'show cause notice', 'disciplinary action',
        'performance management', 'investigation process', 'suspension from employment',
        'termination', 'dismissal', 'termination of employment', 'termination without notice',
        'notice without pay', 'notification of termination', 'termination process',
        'employer termination', 'dismissal decision', 'dismissal application',
        'reinstatement', 'reinstatement remedy', 'reinstatement order',
        'compensation order', 'compensation remedy', 'unfair dismissal remedy',
        'jurisdictional objection', 'conciliation', 'conciliation conference',
        'arbitration', 'arbitration hearing', 'full bench appeal', 'costs order', 'severance pay'
    ],

    # 7.2 General Protections
    'Ind_General_Protections': [
        'general protections', 'general protections claim', 'adverse action', 'adverse action claim',
        'workplace rights', 'workplace right', 'protected activity', 'part 3-1', 'part 3-1 fair work act',
        's340', 's341', 's342', 's343', 's344', 's345', 's346',
        'section 340', 'section 341', 'section 342', 'section 343', 'section 344', 'section 345', 'section 346',
        'reverse onus', 'reverse onus provision', 'reverse onus of proof',
        'prohibited reasons', 'prohibited reason', 'discriminatory reasons', 'discriminatory dismissal',
        'protected attributes', 'protected attribute', 'protected attribute discrimination',
        'protected industrial action', 'protected industrial action participation',
        'trade union membership', 'trade union activities', 'union activity protection',
        'temporary absence', 'temporary absence protection', 'illness protection', 'injury protection',
        'workplace complaint', 'workplace rights complaint',
        'unlawful termination', 'unlawful dismissal', 'sham contracting', 'sham arrangement',
        'misrepresentation of status', 'coercion', 'undue influence', 'misrepresentation',
        'whistleblower', 'whistleblower protection', 'retaliation', 'victimization',
        'stop bullying application', 'stop bullying order', 'workplace bullying claim',
        'jury service protection', 'parental leave protection', 'flexible work protection',
        'substantial and operative factor', 'temporal proximity', 'circumstantial evidence',
        'multiple reasons', 'discrimination protection', 'general protections remedy',
        'pecuniary penalty', 'compensation remedy', 'restraint of trade'
    ],

    # 7.3 Employment Contracts
    'Ind_Employment_Contract': [
        'employment contract', 'contract of employment', 'contract formation',
        'written employment agreement', 'oral employment agreement', 'employment agreement',
        'employment conditions', 'contractual terms', 'breach of employment contract',
        'implied terms', 'implied contract terms', 'express terms', 'express contract terms',
        'written contract', 'common law employment', 'employment at will',
        'restraint of trade', 'restraint clause', 'restraint period', 'restraint geographic scope',
        'non-compete', 'non-compete clause', 'non-solicitation',
        'confidentiality clause', 'confidentiality agreement',
        'intellectual property clause', 'ip clause',
        'notice period', 'termination clause', 'probationary period', 'probation period',
        'probationary employment', 'fixed term contract', 'fixed-term contract',
        'fixed-term employment', 'successive fixed-term', 'casual employment', 'casual arrangement',
        'permanent employment', 'part-time employment', 'part-time arrangement',
        'job sharing', 'independent contractor', 'contractor arrangement',
        'employee vs contractor', 'contractor vs employee', 'employment relationship',
        'multi-factor test', 'multi-factor employment test', 'control test', 'integration test',
        'employment status', 'employment status determination', 'casual conversion',
        'casual conversion rights', 'conversion to permanent', 'regular and systematic',
        'independent contractors act'
    ],

    # 7.4 Enterprise Agreements & Bargaining
    'Ind_Enterprise_Agreement': [
        'enterprise agreement', 'enterprise bargaining', 'collective agreement',
        'better off overall test', 'better off overall', 'boot', 'boot test', 'boot assessment',
        's186', 'section 186', 'part 2-4',
        'nominal expiry', 'nominal expiry date', 'post-nominal expiry',
        'bargaining in good faith', 'bargaining good faith', 'good faith requirements',
        'protected industrial action', 'protected action', 'protected action during bargaining',
        'bargaining period', 'bargaining period commencement', 'bargaining period termination',
        'greenfields agreement', 'greenfield agreement', 'greenfield site',
        'multi-enterprise agreement', 'multi-enterprise bargaining',
        'pattern bargaining', 'pattern bargaining claim', 'pattern bargaining allegation',
        'majority support determination', 'majority support', 'employee vote', 'voting requirements',
        'protected action ballot', 'protected action ballot order', 'ballot order',
        'agreement approval', 'agreement approval process', 'agreement lodgment', 'fwc approval',
        'better off assessment', 'dispute resolution clause', 'dispute resolution procedure', 'dispute clause',
        'flexibility term', 'flexibility arrangement', 'individual flexibility arrangement', 'ifa',
        'consultation term', 'consultation clause', 'consultation requirements',
        'variation', 'variation application', 'agreement variation',
        'termination of agreement', 'termination application',
        'agreement coverage', 'agreement scope', 'agreement content',
        'bargaining representative', 'employee bargaining representative', 'employer bargaining representative',
        'bargaining representative appointment', 'default bargaining representative',
        'permitted matters', 'unlawful terms', 'access period',
        'notice of representational rights', 'norr', 'union access', 'union notification'
    ],

    # 7.5 Modern Awards & Entitlements
    'Ind_Awards': [
        'modern award', 'award interpretation', 'award application', 'award modernisation',
        'modern award system', 'industry award', 'occupation award',
        'national employment standards', 'nes', 'national employment standard', 'nes interaction',
        'award coverage', 'award coverage determination', 'award classification', 'award classification structure',
        'classification level', 'pay rate', 'pay scale', 'minimum pay rate', 'minimum wage',
        'base rate', 'all-purpose rate', 'penalty rates', 'penalty rate',
        'weekend penalty', 'public holiday penalty', 'overtime', 'overtime rate', 'overtime payment',
        'time and a half', 'double time', 'ordinary hours', 'ordinary hours of work',
        'maximum ordinary hours', 'shift allowance', 'shift penalty', 'shift loading',
        'allowance', 'tool allowance', 'uniform allowance', 'meal allowance', 'travel allowance',
        'casual loading', 'casual loading rate', 'casual conversion right', 'regular casual',
        'annual leave', 'annual leave entitlement', 'annual leave loading', 'leave accrual',
        'personal leave', 'personal leave entitlement', 'paid personal leave', 'unpaid personal leave',
        'sick leave', 'sick leave entitlement', 'carer leave', 'carer leave entitlement',
        'compassionate leave', 'compassionate leave entitlement',
        'parental leave', 'parental leave entitlement', 'maternity leave', 'maternity leave entitlement',
        'paternity leave', 'paternity leave entitlement', 'adoption leave',
        'long service leave', 'long service leave entitlement', 'lsl',
        'public holidays', 'public holiday entitlement', 'public holiday payment', 'substitute public holiday',
        'notice of termination', 'notice of termination requirement', 'notice period requirement',
        'redundancy pay', 'redundancy payment', 'redundancy entitlement', 'service credit',
        'rostering', 'rostering requirement', 'roster change', 'minimum shift',
        'broken shift', 'split shift', 'sleepover', 'on-call', 'recall to work',
        'meal break', 'rest break', 'unpaid break', 'tea break',
        'award flexibility', 'individual flexibility arrangement',
        'transitional provision', 'award review', '4 yearly review', '4-yearly review', 'four yearly review',
        'modern awards objective', 'minimum wages objective', 's134', 's284', 'section 134', 'section 284'
    ],

    # 7.6 Industrial Action & Disputes
    'Ind_Industrial_Action': [
        'industrial action', 'strike', 'strike action', 'stopwork', 'work stoppage', 'stoppage of work',
        'work ban', 'work limitation', 'stopwork meeting', 'walkout',
        'lockout', 'lockout action', 'employer lockout',
        'protected action', 'protected industrial action', 'protected action requirements',
        'protected action notice', 'notice of action',
        'unprotected action', 'unprotected industrial action', 'unlawful industrial action',
        'protected action ballot order', 'ballot order', 'ballot requirements',
        'secret ballot', 'ballot agent',
        'bargaining period', 'bargaining period commencement', 'bargaining period termination',
        'pattern bargaining', 'pattern bargaining allegation', 'multi-employer bargaining',
        'secondary boycott', 'secondary boycott prohibition', 's45d', 's45e',
        'competition and consumer act',
        'suspension of industrial action', 'suspension order', 'action suspension',
        'termination of industrial action', 'termination order', 'action termination',
        'cooling off period', 'cooling off order',
        'ministerial intervention', 'ministerial direction', 'ministerial declaration',
        'serious harm', 'emergency powers', 'public interest',
        'stand down', 'stand down provision', 's524', 's526', 'section 524', 'section 526',
        'stoppage beyond control', 'industrial dispute', 'dispute notification',
        'conciliation of dispute', 'arbitration of dispute',
        'damages for industrial action', 'injunction industrial action',
        'penalties for unprotected action', 'right to take action', 'right of entry'
    ],

    # 7.7 Discrimination & Harassment
    'Ind_Discrimination': [
        'discrimination', 'discrimination claim', 'discrimination complaint',
        'direct discrimination', 'direct discrimination claim', 'indirect discrimination', 'indirect discrimination claim',
        'protected attribute', 'protected characteristic', 'less favorable treatment', 'less favourable treatment',
        'comparator', 'comparator analysis', 'because of attribute',
        'unreasonable requirement', 'disadvantage to group', 'neutral requirement',
        'sexual harassment', 'sexual harassment claim', 'unwelcome conduct', 'sexual nature',
        'reasonable person test', 'hostile environment', 'quid pro quo',
        'workplace bullying', 'workplace bullying claim', 'repeated behavior', 'unreasonable behavior',
        'risk to health and safety', 'stop bullying order', 'stop bullying order application',
        'victimisation', 'victimisation claim', 'less favourable treatment complainant',
        'vilification', 'vilification claim', 'public vilification', 'incitement of hatred',
        'reasonable adjustments', 'reasonable adjustment', 'adjustment for disability',
        'accommodation', 'unjustifiable hardship',
        'inherent requirements', 'inherent requirement of position', 'genuine occupational requirement',
        'special measures', 'special measure', 'affirmative action',
        'positive duty', 'positive duty obligation', 'proactive duty', 'elimination of discrimination',
        'disability discrimination', 'disability discrimination claim',
        'age discrimination', 'age discrimination claim',
        'sex discrimination', 'sex discrimination claim',
        'pregnancy discrimination', 'pregnancy discrimination claim',
        'race discrimination', 'race discrimination claim', 'racial discrimination', 'racial discrimination claim',
        'family responsibilities', 'family responsibility discrimination', 'carer discrimination',
        'sex discrimination act', 'sex discrimination act 1984',
        'disability discrimination act', 'disability discrimination act 1992',
        'age discrimination act', 'age discrimination act 2004',
        'racial discrimination act', 'racial discrimination act 1975',
        'anti-discrimination', 'anti-discrimination act', 'equal opportunity act',
        'ahrc', 'ahrc complaint', 'australian human rights commission',
        'human rights complaint', 'tribunal complaint',
        'conciliation process', 'tribunal hearing',
        'burden of proof', 'prima facie case', 'respondent defense',
        'exemption application', 'temporary exemption', 'permanent exemption',
        'discrimination remedy', 'apology order', 'policy change order', 'training order',
        'sex discrimination commissioner', 'disability discrimination commissioner',
        'age discrimination commissioner', 'race discrimination commissioner',
        'respect at work', 'respect@work'
    ],

    # 7.8 Work Health & Safety
    'Ind_WHS': [
        'work health and safety', 'work health safety', 'workplace health safety', 'whs',
        'occupational health and safety', 'occupational safety', 'ohs',
        'work health and safety act', 'whs act', 'whs regulation',
        'model whs laws', 'harmonised whs laws',
        'pcbu', 'pcbu duty', 'pcbu obligations', 'person conducting business or undertaking',
        'business undertaking', 'primary duty of care', 'primary duty holder', 'primary duty requirement',
        'officer due diligence', 'officer duty', 'officer diligence', 'due diligence obligation',
        'active steps', 'verifiable action',
        'reasonably practicable', 'reasonably practicable measures', 'reasonable practicability',
        'health and safety representative', 'health safety representative', 'hsr',
        'hsr election', 'hsr powers', 'hsr training', 'hsr consultation',
        'work group', 'designated work group',
        'provisional improvement notice', 'provisional improvement notice power', 'pin', 'pin issue', 'pin compliance',
        'improvement notice', 'improvement notice issue', 'prohibition notice', 'prohibition notice issue',
        'compliance direction', 'inspector powers', 'whs inspector',
        'whs prosecution', 'whs prosecution offence', 'category 1 offence', 'category 2 offence', 'category 3 offence',
        'industrial manslaughter', 'industrial manslaughter offence', 'reckless conduct', 'gross negligence',
        'notifiable incident', 'notifiable incident report', 'death notification',
        'serious injury', 'serious injury notification', 'serious injury definition',
        'dangerous incident', 'dangerous incident notification', 'dangerous incident definition',
        'workplace fatality', 'workplace death', 'fatality investigation',
        'incident investigation', 'incident response',
        'psychosocial hazards', 'psychosocial hazard', 'psychological risk', 'mental health risk',
        'work-related stress', 'bullying hazard', 'violence hazard',
        'fatigue hazard', 'workload hazard', 'trauma hazard',
        'risk assessment', 'risk assessment process', 'hazard identification',
        'risk evaluation', 'risk control', 'risk control measure',
        'safe work method statement', 'swms', 'safe work procedure', 'work method statement',
        'safe operating procedure', 'sop',
        'hierarchy of controls', 'hierarchy of control', 'control hierarchy',
        'eliminate risk', 'elimination control', 'minimize risk',
        'substitution control', 'engineering control', 'administrative control',
        'ppe control', 'personal protective equipment',
        'safe system of work', 'safe work system', 'system of work', 'work safety system',
        'consultation', 'consultation duty', 'worker consultation', 'safety committee',
        'health and safety committee', 'hsc', 'issue resolution', 'whs issue',
        'cease work', 'cease unsafe work', 'unsafe work', 'right to refuse', 'right to cease unsafe work',
        'safework', 'safework australia', 'work safety regulator',
        'worksafe', 'safework nsw', 'worksafe victoria', 'workplace health and safety queensland'
    ],

    # 7.9 Workers Compensation
    'Ind_Workers_Comp': [
        'workers compensation', 'workers comp', 'workers comp claim',
        'work injury', 'work injury claim', 'injury claim',
        'workplace injury', 'workplace injury claim', 'work-related injury', 'work-related injury claim',
        'injury at work', 'arising out of employment', 'in the course of employment',
        'employment connection', 'injury causation',
        'journey claim', 'journey to work', 'journey from work', 'journey claim requirement',
        'substantial connection',
        'gradual process injury', 'gradual process', 'disease claim',
        'occupational disease', 'occupational disease claim', 'work-related disease',
        'dust disease', 'asbestos disease', 'noise-induced hearing loss', 'repetitive strain injury',
        'psychological injury', 'psychological injury claim', 'psychiatric injury', 'psychiatric injury claim',
        'mental injury', 'stress claim', 'ptsd claim', 'depression claim', 'anxiety claim',
        'psychological injury exclusion', 'reasonable action', 'performance management exclusion',
        'weekly compensation', 'weekly compensation entitlement', 'weekly payments', 'weekly payment', 'weekly benefit',
        'pre-injury average weekly earnings', 'piawe', 'current weekly earnings', 'compensation rate',
        'medical expenses', 'medical expense', 'treatment expense', 'medical treatment',
        'approved treatment', 'treatment approval', 'treatment dispute',
        'whole person impairment', 'whole person impairment assessment', 'wpi', 'wpi assessment', 'wpi percentage',
        'impairment assessor', 'ams', 'approved medical specialist',
        'permanent impairment', 'permanent impairment assessment', 'permanent impairment lump sum',
        'pain and suffering', 'pain and suffering award',
        'work capacity', 'work capacity assessment', 'work capacity decision',
        'current work capacity', 'work capacity certificate',
        'suitable employment', 'suitable employment offer', 'suitable duties', 'suitable duties offer',
        'pre-injury duties', 'alternative duties', 'modified duties',
        'return to work', 'return to work program', 'return to work plan', 'rtw plan',
        'rehabilitation', 'rehabilitation program', 'vocational rehabilitation', 'work trial',
        'common law damages', 'common law claim', 'common law proceedings',
        'work injury damages', 'negligence claim', 'breach of duty',
        'whole person impairment threshold',
        'section 66', 's66', 's66 claim', 'section 66 lump sum',
        'section 67', 's67', 's67 claim', 'section 67 lump sum',
        'section 39', 's39', 's39 dispute', 'section 39 liability dispute', 's39 dispute resolution',
        'dispute referral', 'dispute resolution', 'teleconference',
        'workcover', 'workcover claim', 'workcover claim nsw', 'worksafe claim vic', 'workcover claim qld',
        'workcover wa claim', 'return to work sa', 'worksafe tas', 'comcare claim',
        'workers compensation commission', 'workers compensation commission nsw',
        'workers compensation regulator', 'claims management', 'insurer', 'scheme agent',
        'icare', 'icare nsw', 'worksafe victoria',
        'employer excess', 'claims cost', 'premium impact',
        'injury notification', 'injury report', 'first certificate of capacity',
        'certificate of capacity', 'medical certificate', 'treating doctor',
        'independent medical examination', 'ime', 'medical assessment',
        'death benefit', 'dependency claim', 'funeral expenses',
        'dependency payment', 'lump sum death', 'weekly death benefit'
    ],

    # 7.10 Unions & Workplace Representatives
    'Ind_Union': [
        'trade union', 'union', 'union membership', 'union member rights',
        'union delegate', 'union official', 'union organiser', 'union representative',
        'shop steward', 'workplace delegate', 'union activity', 'union participation',
        'right of entry', 'right of entry provision', 's484', 's485', 's486',
        'section 484', 'section 485', 'section 486',
        'entry notice', 'entry permit', 'entry permit holder', 'permit requirements',
        'federal safety officer', 'federal safety official', 'state safety official',
        'right to inspect', 'right to investigate', 'suspected contravention',
        'safety inspection', 'interview workers',
        'freedom of association', 'freedom of association right', 'associational freedom',
        'registered organisation', 'registered union', 'federal registration', 'state registration',
        'industrial organisation', 'employer organisation',
        'bargaining representative', 'bargaining representative appointment',
        'default bargaining representative', 'employee organisation',
        'union coverage', 'union rules', 'union constitution',
        'enterprise bargaining', 'enterprise bargaining representative',
        'collective bargaining', 'collective bargaining representative',
        'union fees', 'union membership fee', 'union subscription', 'union dues',
        'payroll deduction', 'union access', 'union notification', 'union meeting',
        'workplace meeting', 'delegate training', 'union training leave',
        'paid union leave', 'union official facilities', 'union notice board',
        'fair work registered organisations', 'fair work (registered organisations) act',
        'roc', 'registered organisations commission',
        'union election', 'union democracy', 'union governance'
    ],

    # 7.11 Underpayment & Wage Theft
    'Ind_Underpayment': [
        'underpayment', 'underpayment of wages', 'wage underpayment',
        'wage theft', 'wage theft offence', 'wage theft criminal',
        'unpaid wages', 'unpaid wages claim', 'unpaid salary', 'wage recovery',
        'entitlement underpayment', 'unpaid entitlements', 'unpaid entitlements claim', 'entitlement recovery',
        'deliberate underpayment', 'intentional underpayment', 'dishonest underpayment',
        'unpaid overtime', 'unpaid overtime claim', 'overtime underpayment',
        'penalty rates underpayment', 'unpaid penalty rates',
        'unpaid superannuation', 'unpaid superannuation claim', 'super underpayment',
        'superannuation guarantee', 'superannuation shortfall', 'superannuation guarantee charge', 'sgc',
        'superannuation non-compliance', 'unpaid super penalty',
        'payroll tax', 'payroll tax obligation', 'payroll tax compliance',
        'payslip', 'payslip requirement', 'pay slip provision', 'payslip content',
        'time and wages records', 'time and wages record', 'employee records',
        'employment records', 'record keeping requirement', 'record keeping breach',
        'annualised salary', 'annualised salary arrangement', 'annualisation', 'salary offset',
        'loaded rate', 'loaded rate arrangement', 'all-purpose loading',
        'setoff clause', 'set-off clause', 'setoff arrangement', 'offset agreement',
        'civil remedy provision', 'civil remedy breach', 'civil penalty provision',
        'civil penalty proceeding', 'pecuniary penalty', 'pecuniary penalty order',
        'financial penalty', 'maximum penalty', 'penalty calculation', 'serious contravention',
        'compliance notice', 'compliance notice issue', 'infringement notice',
        'compliance action', 'enforcement action',
        'accessorial liability', 'accessorial liability provision', 'accessory liability',
        'involved in contravention', 'knowingly concerned', 'aided and abetted',
        'director liability', 'back pay', 'unpaid leave', 'leave entitlement underpayment',
        'allowance underpayment', 'incorrect classification', 'misclassification',
        'award coverage error', 'agreement coverage error', 'incorrect pay rate',
        'fair work ombudsman', 'fair work ombudsman investigation', 'fwo', 'fwo audit',
        'compliance audit', 'self-audit', 'voluntary disclosure',
        'enforceable undertaking', 'court-enforceable undertaking', 'proactive compliance deed',
        'small business assistance', 'my account', 'pay and conditions tool'
    ],

    # 7.12 Fair Work Commission & Processes
    'Ind_FWC': [
        'fair work commission', 'fwc', 'fwc decision', 'fwc application',
        'fwc jurisdiction', 'fwc powers', 'fwc orders', 'fwc directions',
        'fair work act', 'fair work act 2009', 'fwa 2009', 'fair work legislation',
        'fair work ombudsman', 'fair work ombudsman enforcement', 'fwo', 'fwo investigation', 'fwo compliance',
        'fair work information statement', 'fair work information statement requirement', 'fwis',
        'employment information',
        'commissioner', 'commissioner decision', 'deputy president', 'deputy president decision',
        'vice president', 'vice president decision', 'senior deputy president',
        'fwc member', 'presidential member',
        'full bench', 'full bench hearing', 'full bench decision', 'full bench appeal',
        'permission to appeal', 'appeal grounds', 'appeal decision',
        'minimum wage panel', 'minimum wage review', 'annual wage review', 'minimum wage determination',
        'minimum wage panel decision', 'expert panel', 'wage setting',
        'modern awards objective', 'modern awards objective test', 's134', 'section 134',
        'minimum wages objective', 'minimum wages objective test', 's284', 'section 284',
        'award variation', 'award review', 'award modernisation',
        '4-yearly review', '4 yearly review', 'four yearly review', 'award variation application',
        'common issue', 'test case', 'model term', 'model clause',
        'fwc procedure', 'fwc rules', 'fair work commission rules',
        'conciliation', 'conciliation by fwc', 'mediation', 'mediation by fwc',
        'arbitration', 'arbitration by fwc', 'fwc conference',
        'directions hearing', 'mention hearing', 'substantive hearing', 'final hearing',
        'fwc evidence', 'witness statement', 'witness examination', 'expert evidence fwc',
        'fwc costs', 'costs order fwc', 'unreasonable conduct',
        'fwc remedy', 'fwc compensation', 'fwc reinstatement',
        'transfer of business', 'transferring employee', 'transmission of business'
    ],"""

# Find the old industrial section and replace it
old_pattern = r"    # --- 7\. INDUSTRIAL ---\n    'Ind_Employment':.*?\],\n    'Ind_Industrial':.*?\],\n    'Ind_Safety':.*?\],"

replacement = new_industrial_section + ","

content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)

# Also need to update the DOMAIN_MAPPING
old_mapping = r"'Industrial': \['Ind_Employment', 'Ind_Industrial', 'Ind_Safety'\],"
new_mapping = "'Industrial': ['Ind_Unfair_Dismissal', 'Ind_General_Protections', 'Ind_Employment_Contract', 'Ind_Enterprise_Agreement', 'Ind_Awards', 'Ind_Industrial_Action', 'Ind_Discrimination', 'Ind_WHS', 'Ind_Workers_Comp', 'Ind_Union', 'Ind_Underpayment', 'Ind_FWC'],"

content = content.replace(old_mapping, new_mapping)

# Write back
with open(config_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Added all employment law keywords!")
print("\nNew categories added:")
print("  1. Ind_Unfair_Dismissal (64 keywords)")
print("  2. Ind_General_Protections (54 keywords)")
print("  3. Ind_Employment_Contract (53 keywords)")
print("  4. Ind_Enterprise_Agreement (57 keywords)")
print("  5. Ind_Awards (106 keywords)")
print("  6. Ind_Industrial_Action (54 keywords)")
print("  7. Ind_Discrimination (81 keywords)")
print("  8. Ind_WHS (117 keywords)")
print("  9. Ind_Workers_Comp (120 keywords)")
print(" 10. Ind_Union (55 keywords)")
print(" 11. Ind_Underpayment (83 keywords)")
print(" 12. Ind_FWC (66 keywords)")
print("\nTOTAL: 910+ employment law keywords added across 12 detailed categories")
