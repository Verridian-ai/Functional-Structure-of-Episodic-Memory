import json
import re
from collections import Counter

# Extract case citations and procedural terms
case_citations = []
procedural_terms = Counter()
additional_keywords = {
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
        if count > 100:  # Sample first 100 for case citations
            break
        try:
            doc = json.loads(line)
            name = doc.get('name', '')
            text = doc.get('text', '')[:30000]

            # Extract case name patterns
            if ' v ' in name or ' v. ' in name:
                case_citations.append(name)

            full_text = (name + ' ' + text).lower()

            # Procedural and legal terms
            proc_terms = [
                'appeal', 'judicial review', 'certiorari', 'mandamus',
                'injunction', 'interlocutory', 'interim relief',
                'declaration', 'declaratory relief',
                'stay application', 'stay of proceedings',
                'summary dismissal', 'strike out', 'dismissal of application',
                'directions hearing', 'case management',
                'conciliation conference', 'compulsory conference',
                'mediation', 'arbitration', 'determination',
                'jurisdictional objection', 'preliminary objection',
                'costs application', 'security for costs',
                'discovery', 'interrogatories', 'particulars',
                'witness summons', 'subpoena',
                'evidence in chief', 'cross-examination',
                'submissions', 'closing submissions',
                'reserved decision', 'ex tempore', 'reasons for decision'
            ]
            for term in proc_terms:
                if term in full_text:
                    procedural_terms[term] += 1

            # More unfair dismissal terms
            ud_additional = [
                'abandonment of employment', 'job left voluntarily',
                'resignation under duress', 'forced resignation',
                'cooling off period', 'waiting period',
                'casual employees', 'probationary employees',
                'high income earner', 'high income threshold',
                'award/agreement free employee',
                'small business fair dismissal code',
                'code of practice', 'procedural requirements',
                'substantive requirements', 'valid reason requirement',
                'notified of reason', 'reasonable time to respond',
                'support person', 'representative',
                'warnings or counselling', 'previous warnings',
                'consistency of treatment', 'similar cases',
                'mitigation of loss', 'duty to mitigate',
                'compensation amount', 'compensation calculation',
                'loss and damage', 'economic loss'
            ]
            if any(t in full_text for t in ['unfair dismissal', 'termination', 'dismissal']):
                for term in ud_additional:
                    if term in full_text:
                        additional_keywords['unfair_dismissal'].add(term)

            # General protections additional
            gp_additional = [
                'workplace right definition', 'benefit under workplace law',
                'complaint or inquiry', 'able to make complaint',
                'proceeding under workplace law',
                'temporary absence', 'illness or injury',
                'parental leave rights', 'flexible work arrangements',
                'requests for flexible work',
                'industrial association membership', 'union membership',
                'non-membership', 'refusal to join',
                'industrial activity definition',
                'adverse action definition', 'coercion or undue influence',
                'threatening or taking action',
                'burden of proof', 'reverse burden',
                'circumstantial evidence', 'inference',
                'substantial and operative factor',
                'causation', 'but for test',
                'interim injunction', 'penalty provisions',
                'maximum penalty', 'contraventions'
            ]
            if any(t in full_text for t in ['general protection', 'adverse action']):
                for term in gp_additional:
                    if term in full_text:
                        additional_keywords['general_protections'].add(term)

            # Enterprise agreements additional
            ea_additional = [
                'enterprise agreement definition',
                'single interest employer', 'common interest employer',
                'single enterprise', 'multi enterprise',
                'approval process', 'section 186 requirements',
                'better off overall test', 'boot assessment',
                'nominal expiry date', 'post-nominal expiry',
                'variation of agreement', 'minor variation',
                'termination by agreement', 'termination by commission',
                'replacement agreement', 'zombie agreement',
                'agreement content requirements',
                'prohibited content', 'unlawful content',
                'model terms', 'consultation term',
                'dispute settlement term', 'flexibility term',
                'outworker term', 'shiftworker term',
                'undertakings to commission', 'technical errors',
                'access to agreement', 'notice of representational rights'
            ]
            if any(t in full_text for t in ['enterprise agreement', 'bargaining']):
                for term in ea_additional:
                    if term in full_text:
                        additional_keywords['enterprise_agreements'].add(term)

            # Fair Work additional
            fw_additional = [
                'national employment standards', 'nes entitlements',
                'maximum weekly hours', 'requests for flexible work',
                'parental leave entitlements', 'annual leave',
                'personal/carer leave', 'compassionate leave',
                'community service leave', 'long service leave',
                'public holidays', 'notice of termination',
                'redundancy pay', 'fair work information statement',
                'modern award coverage', 'award-free',
                'minimum wage', 'national minimum wage',
                'casual loading', 'casual conversion',
                'part-time employee', 'full-time employee',
                'fixed term contract', 'maximum term contract',
                'workplace determination', 'low-paid bargaining',
                'right of entry', 'permit holder',
                'frequency of entry', 'notice of entry',
                'compliance powers', 'investigation powers'
            ]
            if 'fair work' in full_text:
                for term in fw_additional:
                    if term in full_text:
                        additional_keywords['fair_work'].add(term)

            # Discrimination additional
            disc_additional = [
                'unlawful discrimination grounds',
                'age', 'disability', 'race', 'sex', 'pregnancy',
                'marital status', 'family responsibilities',
                'sexual orientation', 'gender identity',
                'intersex status', 'religious belief',
                'political opinion', 'national extraction',
                'direct discrimination', 'indirect discrimination',
                'comparator', 'less favourable treatment',
                'unreasonable requirement', 'condition or requirement',
                'inherent requirements', 'genuine occupational requirement',
                'reasonable adjustments', 'unjustifiable hardship',
                'special measures', 'affirmative action',
                'vicarious liability', 'employer liability',
                'sexual harassment definition', 'hostile environment',
                'anti-bullying provisions', 'stop bullying orders'
            ]
            if any(t in full_text for t in ['discrimination', 'harassment', 'bullying']):
                for term in disc_additional:
                    if term in full_text:
                        additional_keywords['discrimination'].add(term)

            # WHS additional
            whs_additional = [
                'duty of care pcbu', 'duty to workers',
                'duty to other persons', 'upstream duty',
                'downstream duty', 'officer duties',
                'reasonable steps', 'all reasonable steps',
                'resources and processes', 'information and understanding',
                'appropriate resources', 'verifying provisions',
                'health and safety matters', 'hazards and risks',
                'incident response', 'emergency procedures',
                'designated work groups', 'health and safety representative',
                'hsr functions', 'hsr powers',
                'issue resolution procedures', 'provisional improvement notice',
                'cease work direction', 'work cessation',
                'inspector appointment', 'powers of entry',
                'improvement notice', 'prohibition notice',
                'infringement notice', 'penalty notice',
                'prosecution offences', 'category 1 offence',
                'category 2 offence', 'category 3 offence',
                'reckless conduct', 'failure to comply'
            ]
            if any(t in full_text for t in ['whs', 'work health', 'safety']):
                for term in whs_additional:
                    if term in full_text:
                        additional_keywords['workplace_safety'].add(term)

            # Awards additional
            award_additional = [
                'modern awards objective', 'fair and relevant safety net',
                'relative living standards', 'needs of low paid',
                'award simplification', 'easy to understand',
                'stable and sustainable', 'performance and productivity',
                'award coverage', 'coverage determination',
                'industry coverage', 'occupational coverage',
                'geographical coverage', 'exclusion clause',
                'wage rates', 'pay points', 'incremental progression',
                'classification descriptors', 'duties and responsibilities',
                'minimum engagement', 'minimum payment',
                'span of ordinary hours', 'ordinary time',
                'penalty rates saturday', 'penalty rates sunday',
                'public holiday rates', 'overtime rates',
                'meal allowance', 'travel time', 'call back',
                'on call allowance', 'higher duties allowance'
            ]
            if 'award' in full_text:
                for term in award_additional:
                    if term in full_text:
                        additional_keywords['awards'].add(term)

            # Industrial disputes additional
            id_additional = [
                'protected action definition', 'employee claim action',
                'employer response action', 'lock out',
                'organising or engaging', 'threatening to organise',
                'notification requirements', 'notice of action',
                'written notice', 'three clear days',
                'ballot requirements', 'protected action ballot',
                'ballot agent', 'ballot questions',
                'suspension of action', 'termination of action',
                'significant harm', 'threatening harm',
                'endangering life', 'personal safety',
                'health or welfare', 'economy or part',
                'significant damage', 'suspension order',
                'termination order', 'bargaining related determination',
                'serious breach', 'pattern bargaining'
            ]
            if any(t in full_text for t in ['industrial action', 'dispute']):
                for term in id_additional:
                    if term in full_text:
                        additional_keywords['industrial_disputes'].add(term)

            # Redundancy additional
            red_additional = [
                'genuine redundancy', 'section 119',
                'job no longer required', 'operational reasons',
                'employer no longer requires', 'due to changes',
                'ordinary and customary turnover', 'normal turnover',
                'redeployment opportunities', 'suitable position',
                'acceptable to employee', 'within group',
                'unreasonable refusal', 'reasonable alternative',
                'redundancy pay entitlement', 'service calculation',
                'continuous service', 'broken service',
                'redundancy exclusions', 'casual employees',
                'fixed term', 'seasonal work',
                'transmission of business', 'transfer of employment',
                'consultation obligations', 'discuss changes',
                'reasons for redundancy', 'measures to avoid',
                'selection criteria', 'selection process'
            ]
            if 'redundancy' in full_text or 'redundant' in full_text:
                for term in red_additional:
                    if term in full_text:
                        additional_keywords['redundancy'].add(term)

            # Contractors additional
            con_additional = [
                'employee contractor distinction',
                'employment versus independent contractor',
                'common law tests', 'multi factorial test',
                'control and direction', 'level of control',
                'mode of remuneration', 'basis of payment',
                'provision of equipment', 'tools and equipment',
                'delegation or substitution', 'personal services',
                'commercial risk', 'financial risk',
                'goodwill or saleable asset',
                'integration test', 'business structure',
                'tax treatment', 'superannuation obligations',
                'workers compensation', 'insurance obligations',
                'sham contracting offence', 'misrepresentation',
                'reckless misrepresentation', 'knowingly false',
                'deemed employee provisions', 'statutory deeming',
                'labour hire worker', 'host arrangement'
            ]
            if any(t in full_text for t in ['contractor', 'independent contractor']):
                for term in con_additional:
                    if term in full_text:
                        additional_keywords['contractors'].add(term)

        except Exception as e:
            continue

print(f'Documents sampled: {count}')
print('\n' + '=' * 80)
print('\nSAMPLE CASE CITATIONS (First 20)')
print('=' * 80)
for i, case in enumerate(case_citations[:20]):
    print(f'{i+1:2d}. {case}')

print('\n' + '=' * 80)
print('\nPROCEDURAL/LEGAL TERMS (Top 30)')
print('=' * 80)
for term, freq in procedural_terms.most_common(30):
    print(f'{freq:4d}x  {term}')

print('\n' + '=' * 80)
print('\nADDITIONAL KEYWORDS BY CATEGORY')
print('=' * 80)

for category, terms in additional_keywords.items():
    if terms:
        print(f'\n{category.upper().replace("_", " ")} ({len(terms)} additional terms)')
        print('-' * 80)
        for term in sorted(terms):
            print(f'  - {term}')
