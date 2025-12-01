import json
import re
from collections import Counter

# Extract legislation, case law, and organizations
legislation = Counter()
organizations = Counter()
case_patterns = Counter()
specific_terms = {
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
            text = doc.get('text', '')[:20000]
            full_text = (name + ' ' + text).lower()

            # Extract legislation references
            leg_patterns = [
                'fair work act 2009', 'fwa 2009', 'fair work act',
                'workplace relations act', 'wra', 'workplace relations act 1996',
                'work health and safety act', 'whs act',
                'safety, rehabilitation and compensation act', 'src act',
                'sex discrimination act 1984', 'age discrimination act 2004',
                'disability discrimination act 1992', 'racial discrimination act 1975',
                'human rights and equal opportunity commission act',
                'industrial relations act', 'ira',
                'workers compensation act', 'workers compensation and injury management act',
                'return to work act', 'workers compensation and rehabilitation act',
                'long service leave act', 'annual holidays act',
                'minimum wage act', 'equal opportunity act',
                'occupational health and safety act', 'ohs act',
                'public sector management act', 'public service act',
                'building and construction industry', 'bcii act',
                'registered organisations act', 'fair work (registered organisations) act'
            ]
            for leg in leg_patterns:
                if leg in full_text:
                    legislation[leg] += 1

            # Extract organizations
            org_patterns = [
                'fair work commission', 'fwc',
                'fair work ombudsman', 'fwo',
                'australian building and construction commission', 'abcc',
                'construction, forestry, mining and energy union', 'cfmeu',
                'australian workers union', 'awu',
                'shop, distributive and allied employees', 'sda',
                'united workers union', 'uwu',
                'australian services union', 'asu',
                'australian manufacturing workers union', 'amwu',
                'australian council of trade unions', 'actu',
                'australian industry group', 'ai group',
                'australian chamber of commerce and industry', 'acci',
                'master builders australia',
                'safework australia',
                'australian human rights commission', 'ahrc',
                'industrial relations commission',
                'australian industrial relations commission', 'airc'
            ]
            for org in org_patterns:
                if org in full_text:
                    organizations[org] += 1

            # Additional specific terms by category

            # Unfair dismissal specific
            if any(term in full_text for term in ['unfair dismissal', 'termination', 'dismissal']):
                ud_terms = [
                    'small business employer', 'genuine operational reasons',
                    'valid reason for dismissal', 'harsh, unjust or unreasonable',
                    's.387 considerations', 's.387',
                    'size of employer', 'degree of formality',
                    'opportunity to respond', 'unreasonable refusal',
                    'misconduct dismissal', 'serious and wilful',
                    'notice period', 'payment in lieu of notice',
                    'unfair dismissal remedy', 'compensation cap',
                    'reinstatement remedy', 'impracticability of reinstatement',
                    'application time limit', '21 days',
                    'minimum employment period', 'six months', 'twelve months'
                ]
                for term in ud_terms:
                    if term in full_text:
                        specific_terms['unfair_dismissal'].add(term)

            # General protections specific
            if any(term in full_text for term in ['general protection', 'adverse action']):
                gp_terms = [
                    'coercion', 'undue influence', 'undue pressure',
                    'proscribed reason', 'prohibited reason',
                    'workplace right includes', 'benefit under industrial instrument',
                    'role or responsibility under workplace law',
                    'initiating complaint', 'participating in proceeding',
                    'able to make complaint', 'eligible to make complaint',
                    'temporary absence illness', 'temporary absence injury',
                    'engaged in industrial activity', 'industrial association',
                    'not member of industrial association', 'refusal to join',
                    'discriminatory reason', 'protected attribute',
                    'reverse onus of proof', 'shifting evidentiary burden'
                ]
                for term in gp_terms:
                    if term in full_text:
                        specific_terms['general_protections'].add(term)

            # Enterprise agreements specific
            if any(term in full_text for term in ['enterprise agreement', 'bargaining', 'agreement']):
                ea_terms = [
                    'single enterprise agreement', 'multi-enterprise agreement',
                    'greenfields agreement', 'project agreement',
                    'approval requirements', 'better off overall test',
                    'model flexibility term', 'model consultation term',
                    'notice of employee representational rights', 'nerr',
                    'access period', 'seven day access period',
                    'good faith bargaining requirements', 'bargaining in good faith',
                    'surface bargaining', 'capricious bargaining',
                    'protected action ballot application', 'paba',
                    'scope order application', 'majority support determination',
                    'intractable bargaining', 'bargaining dispute',
                    'post-agreement commencement variation',
                    'agreement termination application',
                    'undertaking to fwc', 'approval undertaking'
                ]
                for term in ea_terms:
                    if term in full_text:
                        specific_terms['enterprise_agreements'].add(term)

            # Fair Work specific
            if 'fair work' in full_text:
                fw_terms = [
                    'national system', 'national workplace relations system',
                    'modern award system', 'safety net',
                    'annual wage review', 'minimum wages',
                    'compliance and enforcement', 'inspectorate powers',
                    'production of documents', 'entry to premises',
                    'civil remedy provisions', 'accessorial liability provisions',
                    'serious contraventions', 'multiple contraventions',
                    'court ordered penalties', 'enforceable undertaking',
                    'small claims procedure', 'small claims proceedings',
                    'anti-bullying jurisdiction', 'stop bullying order',
                    'transfer of business', 'transmission of business'
                ]
                for term in fw_terms:
                    if term in full_text:
                        specific_terms['fair_work'].add(term)

            # Workplace safety specific
            if any(term in full_text for term in ['whs', 'work health', 'safety', 'ohs']):
                whs_terms = [
                    'primary duty of care', 'so far as reasonably practicable',
                    'officer due diligence', 'officer obligations',
                    'worker obligations', 'other person obligations',
                    'consultation requirements', 'hsr election',
                    'designated work group', 'work group',
                    'issue resolution', 'issue resolution procedure',
                    'provisional improvement notice powers', 'pin',
                    'cease work powers', 'cease unsafe work',
                    'right to refuse unsafe work', 'right of refusal',
                    'notifiable incident', 'serious injury or illness',
                    'dangerous incident', 'death',
                    'regulator powers', 'inspector powers',
                    'compliance notices', 'improvement notices',
                    'prohibition notices', 'non-disturbance notices'
                ]
                for term in whs_terms:
                    if term in full_text:
                        specific_terms['workplace_safety'].add(term)

            # Awards specific
            if 'award' in full_text:
                award_terms = [
                    'award modernisation', 'modern award objective',
                    'award simplification', 'plain language',
                    'award coverage determination', 'coverage clause',
                    'classification structure', 'classification definitions',
                    'minimum engagement period', 'minimum payment period',
                    'ordinary hours of work', 'spread of hours',
                    'penalty rate provisions', 'overtime provisions',
                    'allowance provisions', 'expense-related allowances',
                    'casual conversion provisions', 'casual conversion clause',
                    'part-time provisions', 'regular pattern',
                    'consultation provisions', 'dispute resolution provisions',
                    'award variation application', '4-yearly review'
                ]
                for term in award_terms:
                    if term in full_text:
                        specific_terms['awards'].add(term)

            # Industrial disputes specific
            if any(term in full_text for term in ['industrial action', 'dispute', 'bargaining']):
                id_terms = [
                    'protected industrial action', 'unprotected industrial action',
                    'employee claim action', 'employer response action',
                    'notification requirements', 'three days notice',
                    'written notice of action', 'notice of intention',
                    'suspension of action order', 'suspension of protected action',
                    'termination of action order', 'bargaining related workplace determination',
                    'intractable bargaining declaration',
                    'significant harm to economy', 'endangering life',
                    'pattern bargaining orders', 'scope orders',
                    'good faith bargaining orders', 'serious breach orders',
                    'industrial action related workplace determination',
                    'cooling-off period', 'suspension period'
                ]
                for term in id_terms:
                    if term in full_text:
                        specific_terms['industrial_disputes'].add(term)

            # Redundancy specific
            if 'redundancy' in full_text or 'redundant' in full_text:
                red_terms = [
                    'genuine redundancy definition', 's.119 requirements',
                    'employer no longer requires job', 'job no longer required',
                    'reasonable redeployment', 'suitable alternative employment within',
                    'refusal of redeployment', 'unreasonable refusal',
                    'redundancy pay entitlement', 'redundancy pay calculation',
                    'service-based redundancy pay', 'years of service',
                    'redundancy pay exemptions', 'small business exemption',
                    'transfer of employment', 'acceptable alternative employment',
                    'consultation about redundancy', 'consultation requirements',
                    'redundancy discussion', 'advance notice',
                    'selection for redundancy', 'redundancy selection criteria'
                ]
                for term in red_terms:
                    if term in full_text:
                        specific_terms['redundancy'].add(term)

            # Contractors specific
            if any(term in full_text for term in ['contractor', 'independent contractor', 'contract']):
                con_terms = [
                    'employee or independent contractor', 'employment relationship',
                    'multi-factorial test', 'holistic assessment',
                    'control test factors', 'degree of control',
                    'integration into business', 'part and parcel',
                    'ability to delegate', 'personal service requirement',
                    'equipment provision', 'provision of own equipment',
                    'commercial independence', 'separate business entity',
                    'taxation treatment', 'abn holder',
                    'sham contracting prohibition', 'mischaracterisation',
                    'deemed employee provisions', 'statutory employee',
                    'labour hire arrangements', 'host employer',
                    'casual conversion rights', 'pathway to permanency',
                    'on-hire employee', 'triangular employment relationship'
                ]
                for term in con_terms:
                    if term in full_text:
                        specific_terms['contractors'].add(term)

        except Exception as e:
            continue

print(f'Documents processed: {count}')
print('\n' + '=' * 80)
print('\nLEGISLATION REFERENCES (Top 20)')
print('=' * 80)
for leg, freq in legislation.most_common(20):
    print(f'{freq:4d}x  {leg}')

print('\n' + '=' * 80)
print('\nORGANIZATIONS (Top 20)')
print('=' * 80)
for org, freq in organizations.most_common(20):
    print(f'{freq:4d}x  {org}')

print('\n' + '=' * 80)
print('\nADDITIONAL SPECIFIC TERMS BY CATEGORY')
print('=' * 80)

for category, terms in specific_terms.items():
    if terms:
        print(f'\n{category.upper().replace("_", " ")} ({len(terms)} terms)')
        print('-' * 80)
        for term in sorted(terms):
            print(f'  - {term}')
