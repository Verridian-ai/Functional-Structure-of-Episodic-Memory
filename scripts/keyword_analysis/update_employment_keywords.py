"""
Script to add all missing employment law keywords to classification_config.py
Based on EMPLOYMENT_LAW_DOMAIN_KNOWLEDGE.md analysis
"""

import re

# Read the current file
with open(r'C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\classification_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define all the new keywords to add to each category
new_keywords = {
    'Emp_Unfair_Dismissal': [
        'wrongful dismissal', 'constructive dismissal', 'termination of employment',
        'forced redundancy', 'severance pay', 'warning letter', 'show cause notice',
        'suspension from employment', 'disciplinary action', 'performance management',
        'harsh dismissal', 'unjust dismissal', 'unreasonable dismissal',
        'small business exemption', 'jurisdictional eligibility', 'dismissal application',
        'conciliation conference', 'arbitration hearing', 'costs order',
        'sound defensible reason', 'well-founded reason', 'opportunity to respond',
        'investigation process', 'notice without pay', 'termination without notice',
        'part 3-2', 'section 394', 'fair work act 2009', 'unfair dismissal remedy',
        'position elimination', 'operational requirements', 'capacity dismissal',
        'conduct dismissal', 'termination process', 'natural justice',
        'notification of termination', 'dismissal decision', 'employer termination',
        'redundancy selection', 'redeployment', 'consultation requirements'
    ],

    'Emp_General_Protections': [
        'general protections claim', 'adverse action claim', 'workplace right',
        'protected industrial action participation', 'trade union membership',
        'trade union activities', 'stop bullying application', 'jury service protection',
        'parental leave protection', 'flexible work protection', 'whistleblower protection',
        'protected attribute discrimination', 'reverse onus provision',
        'substantial and operative factor', 'temporal proximity', 'circumstantial evidence',
        'multiple reasons', 'prohibited reason', 'discrimination protection',
        'temporary absence protection', 'illness protection', 'injury protection',
        'part 3-1 fair work act', 'section 340', 'section 341', 'section 342',
        'section 343', 'section 344', 'section 345', 'section 346',
        'general protections remedy', 'pecuniary penalty', 'compensation remedy',
        'unlawful dismissal', 'discriminatory dismissal', 'protected activity'
    ],

    'Emp_Contract': [
        'contract formation', 'written employment agreement', 'oral employment agreement',
        'restraint clause', 'restraint period', 'restraint geographic scope',
        'confidentiality agreement', 'intellectual property clause', 'ip clause',
        'termination clause', 'probation period', 'probationary employment',
        'fixed-term employment', 'successive fixed-term', 'casual arrangement',
        'part-time arrangement', 'job sharing', 'contractor arrangement',
        'contractor vs employee', 'employment relationship', 'multi-factor employment test',
        'control test', 'integration test', 'sham arrangement', 'misrepresentation of status',
        'casual conversion rights', 'conversion to permanent', 'regular and systematic',
        'independent contractors act', 'employment status determination',
        'written contract', 'express contract terms', 'implied contract terms',
        'common law employment', 'employment at will', 'employment agreement',
        'employment conditions', 'contractual terms', 'breach of employment contract'
    ],

    'Emp_Enterprise_Agreement': [
        'enterprise bargaining', 'collective agreement', 'part 2-4', 'section 186',
        'better off overall', 'boot test', 'boot assessment', 'nominal expiry date',
        'post-nominal expiry', 'bargaining good faith', 'good faith requirements',
        'protected action', 'protected action during bargaining', 'bargaining representative',
        'employee bargaining representative', 'employer bargaining representative',
        'agreement coverage', 'agreement scope', 'greenfield agreement',
        'greenfield site', 'multi-enterprise bargaining', 'pattern bargaining claim',
        'agreement approval process', 'agreement lodgment', 'fwc approval',
        'better off assessment', 'dispute resolution procedure', 'dispute clause',
        'flexibility arrangement', 'individual flexibility arrangement', 'ifa',
        'consultation clause', 'consultation requirements', 'agreement variation',
        'variation application', 'agreement termination', 'termination application',
        'agreement content', 'permitted matters', 'unlawful terms',
        'majority support', 'employee vote', 'voting requirements',
        'access period', 'notice of representational rights', 'norr'
    ],

    'Emp_Awards': [
        'award interpretation', 'award application', 'award modernisation',
        'modern award system', 'industry award', 'occupation award',
        'award classification structure', 'classification level', 'pay scale',
        'minimum pay rate', 'base rate', 'all-purpose rate', 'penalty rate',
        'weekend penalty', 'public holiday penalty', 'overtime rate',
        'overtime payment', 'time and a half', 'double time', 'ordinary hours of work',
        'maximum ordinary hours', 'shift penalty', 'shift loading', 'allowance',
        'tool allowance', 'uniform allowance', 'meal allowance', 'travel allowance',
        'casual loading rate', 'casual conversion right', 'regular casual',
        'annual leave entitlement', 'annual leave loading', 'leave accrual',
        'personal leave entitlement', 'paid personal leave', 'unpaid personal leave',
        'sick leave entitlement', 'carer leave entitlement', 'compassionate leave entitlement',
        'parental leave entitlement', 'maternity leave entitlement', 'paternity leave entitlement',
        'adoption leave', 'long service leave entitlement', 'lsl',
        'public holiday entitlement', 'public holiday payment', 'substitute public holiday',
        'notice of termination requirement', 'notice period requirement',
        'redundancy payment', 'redundancy entitlement', 'service credit',
        'rostering requirement', 'roster change', 'minimum shift', 'broken shift',
        'split shift', 'sleepover', 'on-call', 'recall to work',
        'meal break', 'rest break', 'unpaid break', 'tea break',
        'award flexibility', 'individual flexibility arrangement',
        'national employment standard', 'nes interaction', 'award coverage determination',
        'transitional provision', 'award review', '4 yearly review'
    ],

    'Emp_Industrial_Action': [
        'strike action', 'work ban', 'work limitation', 'stoppage of work',
        'stopwork meeting', 'walkout', 'lockout action', 'employer lockout',
        'protected industrial action', 'protected action requirements',
        'protected action notice', 'protected action ballot order', 'ballot order',
        'ballot requirements', 'secret ballot', 'ballot agent',
        'bargaining period commencement', 'bargaining period termination',
        'pattern bargaining allegation', 'multi-employer bargaining',
        'secondary boycott prohibition', 'competition and consumer act',
        'suspension order', 'termination order', 'cooling off order',
        'ministerial direction', 'ministerial declaration', 'serious harm',
        'stand down provision', 'section 524', 'section 526', 'stoppage beyond control',
        'industrial dispute', 'dispute notification', 'conciliation of dispute',
        'arbitration of dispute', 'unprotected industrial action',
        'unlawful industrial action', 'damages for industrial action',
        'injunction industrial action', 'penalties for unprotected action',
        'right to take action', 'notice of action', 'action suspension',
        'action termination', 'emergency powers', 'public interest'
    ],

    'Emp_Discrimination': [
        'protected characteristic', 'less favorable treatment', 'less favourable treatment',
        'comparator', 'comparator analysis', 'because of attribute',
        'direct discrimination claim', 'indirect discrimination claim',
        'unreasonable requirement', 'disadvantage to group', 'neutral requirement',
        'sexual harassment claim', 'unwelcome conduct', 'sexual nature',
        'reasonable person test', 'hostile environment', 'quid pro quo',
        'workplace bullying claim', 'repeated behavior', 'unreasonable behavior',
        'risk to health and safety', 'stop bullying order application',
        'victimisation claim', 'less favourable treatment complainant',
        'vilification claim', 'public vilification', 'incitement of hatred',
        'reasonable adjustment', 'adjustment for disability', 'accommodation',
        'unjustifiable hardship', 'inherent requirement of position',
        'genuine occupational requirement', 'special measure', 'affirmative action',
        'positive duty obligation', 'proactive duty', 'elimination of discrimination',
        'disability discrimination claim', 'age discrimination claim',
        'sex discrimination claim', 'pregnancy discrimination claim',
        'race discrimination claim', 'racial discrimination claim',
        'family responsibility discrimination', 'carer discrimination',
        'sex discrimination act 1984', 'disability discrimination act 1992',
        'age discrimination act 2004', 'racial discrimination act 1975',
        'anti-discrimination act', 'equal opportunity act', 'discrimination complaint',
        'ahrc complaint', 'human rights complaint', 'tribunal complaint',
        'conciliation process', 'tribunal hearing', 'burden of proof',
        'prima facie case', 'respondent defense', 'exemption application',
        'temporary exemption', 'permanent exemption', 'discrimination remedy',
        'apology order', 'policy change order', 'training order',
        'sex discrimination commissioner', 'disability discrimination commissioner',
        'age discrimination commissioner', 'race discrimination commissioner',
        'australian human rights commission', 'ahrc', 'respect at work'
    ],

    'Emp_WHS': [
        'work health safety', 'workplace health safety', 'occupational safety',
        'whs act', 'whs regulation', 'model whs laws', 'harmonised whs laws',
        'pcbu duty', 'business undertaking', 'primary duty holder',
        'officer duty', 'officer diligence', 'due diligence obligation',
        'active steps', 'verifiable action', 'primary duty requirement',
        'reasonably practicable measures', 'reasonable practicability',
        'hierarchy of control', 'eliminate risk', 'minimize risk',
        'risk control measure', 'health safety representative', 'hsr election',
        'hsr powers', 'hsr training', 'work group', 'designated work group',
        'provisional improvement notice power', 'pin issue', 'pin compliance',
        'improvement notice issue', 'prohibition notice issue',
        'compliance direction', 'inspector powers', 'whs inspector',
        'whs prosecution offence', 'category 1 offence', 'category 2 offence',
        'category 3 offence', 'industrial manslaughter offence',
        'reckless conduct', 'gross negligence', 'notifiable incident report',
        'death notification', 'serious injury notification', 'dangerous incident notification',
        'incident investigation', 'incident response', 'serious injury definition',
        'dangerous incident definition', 'workplace death', 'fatality investigation',
        'psychosocial hazard', 'psychological risk', 'mental health risk',
        'work-related stress', 'bullying hazard', 'violence hazard',
        'fatigue hazard', 'workload hazard', 'trauma hazard',
        'risk assessment process', 'hazard identification', 'risk evaluation',
        'risk control', 'swms', 'safe work procedure', 'work method statement',
        'safe operating procedure', 'sop', 'control hierarchy',
        'elimination control', 'substitution control', 'engineering control',
        'administrative control', 'ppe control', 'personal protective equipment',
        'safe work system', 'system of work', 'work safety system',
        'consultation duty', 'worker consultation', 'hsr consultation',
        'safety committee', 'health and safety committee', 'hsc',
        'issue resolution', 'whs issue', 'cease work', 'unsafe work',
        'right to refuse', 'safework australia', 'work safety regulator',
        'worksafe', 'safework nsw', 'worksafe victoria', 'workplace health and safety queensland'
    ],

    'Emp_Workers_Comp': [
        'workers comp claim', 'work injury claim', 'injury claim',
        'workplace injury claim', 'work-related injury claim', 'injury at work',
        'arising out of employment', 'in the course of employment',
        'employment connection', 'injury causation', 'journey to work',
        'journey from work', 'journey claim requirement', 'substantial connection',
        'gradual process', 'disease claim', 'occupational disease claim',
        'dust disease', 'asbestos disease', 'noise-induced hearing loss',
        'repetitive strain injury', 'work-related disease',
        'psychological injury claim', 'psychiatric injury claim',
        'mental injury', 'stress claim', 'ptsd claim', 'depression claim',
        'anxiety claim', 'psychological injury exclusion', 'reasonable action',
        'performance management exclusion', 'weekly compensation entitlement',
        'weekly payment', 'weekly benefit', 'pre-injury average weekly earnings',
        'piawe', 'current weekly earnings', 'compensation rate',
        'medical expense', 'treatment expense', 'medical treatment',
        'approved treatment', 'treatment approval', 'treatment dispute',
        'whole person impairment assessment', 'wpi assessment', 'wpi percentage',
        'impairment assessor', 'ams', 'approved medical specialist',
        'permanent impairment assessment', 'permanent impairment lump sum',
        'pain and suffering', 'work capacity decision', 'work capacity assessment',
        'current work capacity', 'work capacity certificate',
        'suitable duties offer', 'suitable employment offer',
        'pre-injury duties', 'alternative duties', 'modified duties',
        'return to work program', 'return to work plan', 'rtw plan',
        'rehabilitation program', 'vocational rehabilitation', 'work trial',
        'common law claim', 'common law proceedings', 'work injury damages',
        'negligence claim', 'breach of duty', 'whole person impairment threshold',
        'section 66 lump sum', 'section 67 lump sum', 's66 claim', 's67 claim',
        'pain and suffering award', 'section 39 liability dispute',
        's39 dispute resolution', 'dispute referral', 'teleconference',
        'workcover claim nsw', 'worksafe claim vic', 'workcover claim qld',
        'workcover wa claim', 'return to work sa', 'worksafe tas',
        'comcare claim', 'workers compensation commission nsw',
        'workers compensation regulator', 'claims management', 'insurer',
        'scheme agent', 'icare nsw', 'worksafe victoria',
        'employer excess', 'claims cost', 'premium impact',
        'injury notification', 'injury report', 'first certificate of capacity',
        'certificate of capacity', 'medical certificate', 'treating doctor',
        'independent medical examination', 'ime', 'medical assessment',
        'death benefit', 'dependency claim', 'funeral expenses',
        'dependency payment', 'lump sum death', 'weekly death benefit'
    ],

    'Emp_Union': [
        'union official', 'union organiser', 'union representative',
        'shop steward', 'workplace delegate', 'union member rights',
        'union activity', 'union participation', 'right of entry provision',
        'section 484', 'section 485', 'section 486', 'entry notice',
        'entry permit holder', 'permit requirements', 'federal safety official',
        'state safety official', 'right to inspect', 'right to investigate',
        'suspected contravention', 'safety inspection', 'interview workers',
        'freedom of association right', 'associational freedom',
        'registered union', 'registered organisation', 'federal registration',
        'state registration', 'industrial organisation', 'employer organisation',
        'bargaining representative appointment', 'default bargaining representative',
        'employee organisation', 'union coverage', 'union rules',
        'union constitution', 'enterprise bargaining representative',
        'collective bargaining representative', 'union membership fee',
        'union subscription', 'union dues', 'payroll deduction',
        'union access', 'union notification', 'union meeting',
        'workplace meeting', 'delegate training', 'union training leave',
        'paid union leave', 'union official facilities', 'union notice board',
        'fair work registered organisations', 'roc', 'registered organisations commission',
        'union election', 'union democracy', 'union governance'
    ],

    'Emp_Underpayment': [
        'underpayment of wages', 'wage underpayment', 'unpaid wages claim',
        'unpaid salary', 'wage recovery', 'entitlement underpayment',
        'unpaid entitlements claim', 'entitlement recovery', 'wage theft offence',
        'wage theft criminal', 'deliberate underpayment', 'intentional underpayment',
        'dishonest underpayment', 'unpaid overtime claim', 'overtime underpayment',
        'penalty rates underpayment', 'unpaid penalty rates',
        'unpaid superannuation claim', 'super underpayment', 'superannuation shortfall',
        'superannuation guarantee charge', 'sgc', 'superannuation non-compliance',
        'unpaid super penalty', 'payroll tax obligation', 'payroll tax compliance',
        'payslip requirement', 'pay slip provision', 'payslip content',
        'time and wages record', 'employee records', 'employment records',
        'record keeping requirement', 'record keeping breach',
        'annualised salary arrangement', 'annualisation', 'salary offset',
        'loaded rate arrangement', 'all-purpose loading', 'setoff arrangement',
        'set-off clause', 'offset agreement', 'civil remedy breach',
        'civil penalty provision', 'civil penalty proceeding',
        'pecuniary penalty order', 'financial penalty', 'maximum penalty',
        'penalty calculation', 'serious contravention', 'compliance notice issue',
        'infringement notice', 'compliance action', 'enforcement action',
        'accessorial liability provision', 'accessory liability', 'involved in contravention',
        'knowingly concerned', 'aided and abetted', 'director liability',
        'back pay', 'unpaid leave', 'leave entitlement underpayment',
        'allowance underpayment', 'incorrect classification', 'misclassification',
        'award coverage error', 'agreement coverage error', 'incorrect pay rate',
        'fair work ombudsman investigation', 'fwo audit', 'compliance audit',
        'self-audit', 'voluntary disclosure', 'enforceable undertaking',
        'court-enforceable undertaking', 'proactive compliance deed',
        'small business assistance', 'my account', 'pay and conditions tool'
    ],

    'Emp_FWC': [
        'fair work commission decision', 'fwc decision', 'fwc application',
        'fwc jurisdiction', 'fwc powers', 'fwc orders', 'fwc directions',
        'fair work act 2009', 'fwa 2009', 'fair work legislation',
        'fair work ombudsman enforcement', 'fwo investigation', 'fwo compliance',
        'fair work information statement requirement', 'fwis', 'employment information',
        'commissioner decision', 'deputy president decision', 'vice president decision',
        'senior deputy president', 'fwc member', 'presidential member',
        'full bench hearing', 'full bench decision', 'full bench appeal',
        'permission to appeal', 'appeal grounds', 'appeal decision',
        'minimum wage review', 'annual wage review', 'minimum wage determination',
        'minimum wage panel decision', 'expert panel', 'wage setting',
        'modern awards objective test', 's134', 'section 134',
        'minimum wages objective test', 's284', 'section 284',
        'award variation', 'award review', 'award modernisation',
        '4-yearly review', 'four yearly review', 'award variation application',
        'common issue', 'test case', 'model term', 'model clause',
        'fwc procedure', 'fwc rules', 'fair work commission rules',
        'conciliation by fwc', 'mediation by fwc', 'arbitration by fwc',
        'fwc conference', 'directions hearing', 'mention hearing',
        'substantive hearing', 'final hearing', 'fwc evidence',
        'witness statement', 'witness examination', 'expert evidence fwc',
        'fwc costs', 'costs order fwc', 'unreasonable conduct',
        'fwc remedy', 'fwc compensation', 'fwc reinstatement',
        'transfer of business', 'transferring employee', 'transmission of business'
    ]
}

# Function to add keywords to a category
def add_keywords_to_category(content, category_name, new_kw_list):
    # Find the category pattern - must handle both ],\n and ] at end of list
    pattern = rf"('{category_name}':\s*\[)(.*?)(\s*\],)"

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Warning: Could not find category {category_name}")
        return content

    # Get existing keywords
    existing_keywords_str = match.group(2)

    # Extract existing keywords (strip quotes and whitespace)
    existing_keywords = set()
    for line in existing_keywords_str.split(','):
        cleaned = line.strip().strip("'").strip('"')
        if cleaned:
            existing_keywords.add(cleaned.lower())

    # Find truly new keywords
    truly_new = []
    for kw in new_kw_list:
        if kw.lower() not in existing_keywords:
            truly_new.append(kw)

    if not truly_new:
        print(f"{category_name}: No new keywords to add")
        return content

    # Format new keywords
    formatted_new = ",\n        ".join([f"'{kw}'" for kw in truly_new])

    # Add comma after existing content if needed
    existing_with_comma = existing_keywords_str.rstrip()
    if not existing_with_comma.endswith(','):
        existing_with_comma += ','

    # Build replacement
    replacement = f"{match.group(1)}{existing_with_comma}\n        {formatted_new}{match.group(3)}"

    # Replace in content
    content = content[:match.start()] + replacement + content[match.end():]

    print(f"{category_name}: Added {len(truly_new)} new keywords")
    return content

# Process all categories
print("Adding missing employment law keywords...\n")
for category, keywords in new_keywords.items():
    content = add_keywords_to_category(content, category, keywords)

# Write back to file
with open(r'C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\classification_config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll missing keywords have been added to classification_config.py")
