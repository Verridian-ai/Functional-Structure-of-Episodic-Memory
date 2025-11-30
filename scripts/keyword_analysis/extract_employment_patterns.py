import json
import re
from collections import defaultdict

# More comprehensive search patterns
new_keywords = {
    'unfair_dismissal': set(),
    'general_protections': set(),
    'enterprise_agreements': set(),
    'fair_work': set(),
    'discrimination': set(),
    'workplace_safety': set(),
    'awards': set(),
    'industrial_disputes': set(),
    'redundancy': set(),
    'contractors': set()
}

count = 0
with open('data/domains/industrial.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        count += 1
        try:
            doc = json.loads(line)
            name = doc.get('name', '')
            text = doc.get('text', '')[:15000]
            full_text = (name + ' ' + text).lower()

            # UNFAIR DISMISSAL - expanded search
            patterns_ud = [
                'performance management', 'performance issue', 'disciplinary action',
                'warning letter', 'show cause', 'termination letter',
                'notice of dismissal', 'dismissal without notice', 'payment in lieu',
                'unfair dismissal application', 's.394', 's394', 's.385', 's385',
                'high income threshold', 'small business fair dismissal code',
                'probationary period', 'probation', 'trial period',
                'abandonment of employment', 'job abandonment',
                'capacity', 'incapacity', 'inability to perform',
                'wilful misconduct', 'gross misconduct',
                'repudiation', 'fundamental breach'
            ]
            for p in patterns_ud:
                if p in full_text:
                    new_keywords['unfair_dismissal'].add(p)

            # GENERAL PROTECTIONS - expanded
            patterns_gp = [
                'general protections claim', 's.340', 's340', 's.351', 's351',
                'freedom of association', 'right to organize',
                'parental leave', 'carer leave', 'compassionate leave',
                'jury service', 'discrimination', 'protected attribute',
                'temporary absence due to illness', 'absence from work',
                'filing a complaint', 'making an inquiry',
                'exercising a workplace right', 'assert a workplace right',
                'whistleblower', 'public interest disclosure',
                'subjective intention', 'substantial and operative reason'
            ]
            for p in patterns_gp:
                if p in full_text:
                    new_keywords['general_protections'].add(p)

            # ENTERPRISE AGREEMENTS - expanded
            patterns_ea = [
                'enterprise bargaining', 'ea', 'approval of agreement',
                'variation', 'termination of agreement', 'agreement expiry',
                'undertaking', 'model term', 'flexibility term',
                'individual flexibility arrangement', 'ifa',
                'dispute resolution', 'dispute settlement', 'grievance procedure',
                'consultation clause', 'redundancy clause',
                'scope of agreement', 'coverage', 'nominal expiry',
                'better off overall', 'no disadvantage',
                'protected action ballot', 'bargaining period',
                'good faith bargaining obligations', 'bargaining representative',
                'majority support determination', 'scope order',
                'multi-enterprise agreement', 'mea'
            ]
            for p in patterns_ea:
                if p in full_text:
                    new_keywords['enterprise_agreements'].add(p)

            # FAIR WORK - expanded
            patterns_fw = [
                'fair work ombudsman', 'fwo', 'inspector',
                'compliance notice', 'infringement notice',
                'underpayment', 'unpaid wages', 'wage theft',
                'record keeping', 'pay slip', 'time and wages records',
                'sham contracting', 'phoenixing',
                'accessorial liability', 'involved in contravention',
                'civil penalty', 'pecuniary penalty',
                'contraventions', 'breach',
                'national system employer', 'constitutional corporation',
                'transitional provisions', 'modern awards objective',
                'registered agreement', 'approval', 'undertakings'
            ]
            for p in patterns_fw:
                if p in full_text:
                    new_keywords['fair_work'].add(p)

            # DISCRIMINATION - expanded
            patterns_disc = [
                'sex discrimination act', 'age discrimination act',
                'disability discrimination act', 'racial discrimination act',
                'ahrc', 'human rights commission',
                'protected attribute', 'inherent requirement',
                'direct discrimination', 'indirect discrimination',
                'reasonable adjustment', 'accommodation',
                'sexual harassment policy', 'anti-bullying policy',
                'victimisation', 'retaliation',
                'positive duty', 'proactive duty',
                'gender pay gap', 'pay equity',
                'unconscious bias', 'systemic discrimination',
                'disparate impact', 'adverse impact'
            ]
            for p in patterns_disc:
                if p in full_text:
                    new_keywords['discrimination'].add(p)

            # WORKPLACE SAFETY - expanded
            patterns_whs = [
                'safework', 'work safe', 'worksafe',
                'safety management system', 'sms',
                'risk assessment', 'hazard identification',
                'safe work method statement', 'swms', 'jsea',
                'emergency procedures', 'evacuation',
                'personal protective equipment', 'ppe',
                'training and instruction', 'induction',
                'workplace inspection', 'safety audit',
                'incident investigation', 'root cause analysis',
                'improvement notice', 'prohibition notice',
                'prosecution', 'category 1 offence', 'category 2 offence',
                'reckless conduct', 'due diligence',
                'officer duties', 'senior management',
                'mental health', 'stress', 'fatigue management'
            ]
            for p in patterns_whs:
                if p in full_text:
                    new_keywords['workplace_safety'].add(p)

            # AWARDS - expanded
            patterns_awards = [
                'award wage', 'minimum wage order',
                'ordinary hours', 'span of hours',
                'rostering', 'roster', 'shift pattern',
                'casual employment', 'part-time', 'full-time',
                'shiftwork', 'weekend work', 'public holiday',
                'meal break', 'rest break', 'tea break',
                'on-call', 'standby', 'availability',
                'higher duties', 'mixed functions',
                'apprentice', 'trainee', 'junior rates',
                'uniform', 'tool allowance', 'travel allowance',
                'annualised salary', 'salary packaging',
                'pay increment', 'progression'
            ]
            for p in patterns_awards:
                if p in full_text:
                    new_keywords['awards'].add(p)

            # INDUSTRIAL DISPUTES - expanded
            patterns_id = [
                'protected action ballot order', 'pabo',
                'notification of industrial action',
                'suspension of industrial action', 'interim injunction',
                'pattern bargaining', 'common claim',
                'bargaining order', 's.230', 's230',
                'serious breach declaration',
                'cooling off period', 'suspension order',
                'dispute notification', 'dispute resolution clause',
                'mediation', 'facilitation',
                'compulsory conference', 'conciliation conference',
                'appeal', 'judicial review',
                'interlocutory application', 'stay application'
            ]
            for p in patterns_id:
                if p in full_text:
                    new_keywords['industrial_disputes'].add(p)

            # REDUNDANCY - expanded
            patterns_red = [
                'operational requirements', 'business restructure',
                'downsizing', 'workforce reduction',
                'transfer of business', 'sale of business',
                'suitable alternative employment', 'alternative position',
                'trial period', 'retraining',
                's.119', 's119', 'genuine redundancy exemption',
                'small business exemption',
                'redundancy consultation', 'consultation period',
                'redundancy selection', 'selection criteria',
                'volunteers for redundancy', 'voluntary redundancy'
            ]
            for p in patterns_red:
                if p in full_text:
                    new_keywords['redundancy'].add(p)

            # CONTRACTORS - expanded
            patterns_con = [
                'contractor', 'subcontractor', 'consultant',
                'abn', 'australian business number',
                'contract for services', 'contract of service',
                'control and direction', 'supervision',
                'right to delegate', 'delegation',
                'provision of equipment', 'tools of trade',
                'commercial risk', 'profit and loss',
                'integration test', 'business on own account',
                'superannuation guarantee', 'super obligation',
                'workers comp insurance', 'public liability',
                'casual conversion', 'pathway to permanency',
                'on-demand worker', 'platform worker'
            ]
            for p in patterns_con:
                if p in full_text:
                    new_keywords['contractors'].add(p)

        except Exception as e:
            continue

print(f'Total documents processed: {count}')
print('=' * 80)

for category, terms in new_keywords.items():
    if terms:
        print(f'\n{category.upper().replace("_", " ")}')
        print(f'Keywords found: {len(terms)}')
        for term in sorted(terms):
            print(f'  - {term}')
