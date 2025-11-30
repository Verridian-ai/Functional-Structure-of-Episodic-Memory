import json
import re

# Comprehensive keyword extraction
keywords = {
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

# Sample documents
sample_docs = {cat: [] for cat in keywords.keys()}

with open('data/domains/industrial.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            doc = json.loads(line)
            name = doc.get('name', '')
            text = doc.get('text', '')[:10000]
            full_text = (name + ' ' + text).lower()

            # Extract terms using regex patterns

            # Unfair dismissal patterns
            if re.search(r'(unfair|unlawful|wrongful|harsh|unjust) (dismissal|termination)', full_text):
                keywords['unfair_dismissal'].add('unfair dismissal')
                if len(sample_docs['unfair_dismissal']) < 3:
                    sample_docs['unfair_dismissal'].append(name[:150])

            if re.search(r'(summary|instant) dismissal', full_text):
                keywords['unfair_dismissal'].add('summary dismissal')

            if 'termination of employment' in full_text:
                keywords['unfair_dismissal'].add('termination of employment')

            if re.search(r'(procedural|substantive) fairness', full_text):
                keywords['unfair_dismissal'].add('procedural fairness')
                keywords['unfair_dismissal'].add('substantive fairness')

            if 'constructive dismissal' in full_text:
                keywords['unfair_dismissal'].add('constructive dismissal')

            if 'misconduct' in full_text:
                keywords['unfair_dismissal'].add('misconduct')

            if 'serious misconduct' in full_text:
                keywords['unfair_dismissal'].add('serious misconduct')

            if 'valid reason' in full_text:
                keywords['unfair_dismissal'].add('valid reason')

            if 'reinstatement' in full_text:
                keywords['unfair_dismissal'].add('reinstatement')

            if 'compensation' in full_text:
                keywords['unfair_dismissal'].add('compensation')

            # General protections
            if 'adverse action' in full_text:
                keywords['general_protections'].add('adverse action')
                if len(sample_docs['general_protections']) < 3:
                    sample_docs['general_protections'].append(name[:150])

            if 'workplace right' in full_text:
                keywords['general_protections'].add('workplace rights')

            if 'victimisation' in full_text or 'victimization' in full_text:
                keywords['general_protections'].add('victimisation')

            if re.search(r'prohibited reason', full_text):
                keywords['general_protections'].add('prohibited reason')

            if 'reverse onus' in full_text:
                keywords['general_protections'].add('reverse onus')

            if 'temporary absence' in full_text:
                keywords['general_protections'].add('temporary absence')

            if 'trade union' in full_text:
                keywords['general_protections'].add('trade union membership')

            if 'industrial activity' in full_text:
                keywords['general_protections'].add('industrial activity')

            # Enterprise agreements
            if 'enterprise agreement' in full_text:
                keywords['enterprise_agreements'].add('enterprise agreement')
                if len(sample_docs['enterprise_agreements']) < 3:
                    sample_docs['enterprise_agreements'].append(name[:150])

            if re.search(r'collective (bargaining|agreement)', full_text):
                keywords['enterprise_agreements'].add('collective bargaining')

            if 'better off overall test' in full_text or 'boot' in full_text:
                keywords['enterprise_agreements'].add('better off overall test (BOOT)')

            if re.search(r'(multi-employer|single-employer)', full_text):
                keywords['enterprise_agreements'].add('multi-employer bargaining')
                keywords['enterprise_agreements'].add('single-employer agreement')

            if 'greenfields agreement' in full_text:
                keywords['enterprise_agreements'].add('greenfields agreement')

            if 'bargaining in good faith' in full_text:
                keywords['enterprise_agreements'].add('good faith bargaining')

            if 'nominal expiry' in full_text:
                keywords['enterprise_agreements'].add('nominal expiry date')

            if 'variation of agreement' in full_text or 'vary agreement' in full_text:
                keywords['enterprise_agreements'].add('variation of agreement')

            # Fair Work
            if 'fair work commission' in full_text or 'fwc' in full_text:
                keywords['fair_work'].add('Fair Work Commission (FWC)')
                if len(sample_docs['fair_work']) < 3:
                    sample_docs['fair_work'].append(name[:150])

            if 'fair work act' in full_text:
                keywords['fair_work'].add('Fair Work Act 2009')

            if 'national employment standards' in full_text or re.search(r'\bnes\b', full_text):
                keywords['fair_work'].add('National Employment Standards (NES)')

            if 'minimum wage' in full_text:
                keywords['fair_work'].add('minimum wage')

            if 'annual wage review' in full_text:
                keywords['fair_work'].add('annual wage review')

            if 'registered organisation' in full_text:
                keywords['fair_work'].add('registered organisations')

            if 'workplace laws' in full_text:
                keywords['fair_work'].add('workplace laws')

            # Discrimination
            if re.search(r'(unlawful|workplace) discrimination', full_text):
                keywords['discrimination'].add('unlawful discrimination')
                if len(sample_docs['discrimination']) < 3:
                    sample_docs['discrimination'].append(name[:150])

            if 'sexual harassment' in full_text:
                keywords['discrimination'].add('sexual harassment')

            if 'bullying' in full_text:
                keywords['discrimination'].add('workplace bullying')

            if re.search(r'(age|race|sex|disability|pregnancy) discrimination', full_text):
                keywords['discrimination'].add('age discrimination')
                keywords['discrimination'].add('race discrimination')
                keywords['discrimination'].add('sex discrimination')
                keywords['discrimination'].add('disability discrimination')
                keywords['discrimination'].add('pregnancy discrimination')

            if 'equal remuneration' in full_text:
                keywords['discrimination'].add('equal remuneration')

            if 'hostile work environment' in full_text:
                keywords['discrimination'].add('hostile work environment')

            if 'gender equality' in full_text:
                keywords['discrimination'].add('gender equality')

            # WHS
            if 'work health and safety' in full_text or re.search(r'\bwhs\b', full_text):
                keywords['workplace_safety'].add('Work Health and Safety (WHS)')
                if len(sample_docs['workplace_safety']) < 3:
                    sample_docs['workplace_safety'].append(name[:150])

            if 'occupational health' in full_text or re.search(r'\bohs\b', full_text):
                keywords['workplace_safety'].add('Occupational Health and Safety (OHS)')

            if 'duty of care' in full_text:
                keywords['workplace_safety'].add('duty of care')

            if 'psychosocial hazard' in full_text:
                keywords['workplace_safety'].add('psychosocial hazards')

            if 'workers compensation' in full_text:
                keywords['workplace_safety'].add('workers compensation')

            if 'safety officer' in full_text or 'health and safety representative' in full_text:
                keywords['workplace_safety'].add('health and safety representatives')

            if 'notifiable incident' in full_text:
                keywords['workplace_safety'].add('notifiable incidents')

            if 'provisional improvement notice' in full_text:
                keywords['workplace_safety'].add('provisional improvement notices')

            if 'reasonably practicable' in full_text:
                keywords['workplace_safety'].add('reasonably practicable')

            if 'pcbu' in full_text or 'person conducting a business' in full_text:
                keywords['workplace_safety'].add('PCBU (Person Conducting Business or Undertaking)')

            # Awards
            if 'modern award' in full_text:
                keywords['awards'].add('modern awards')
                if len(sample_docs['awards']) < 3:
                    sample_docs['awards'].append(name[:150])

            if 'award interpretation' in full_text:
                keywords['awards'].add('award interpretation')

            if 'award coverage' in full_text:
                keywords['awards'].add('award coverage')

            if 'penalty rates' in full_text or 'penalty rate' in full_text:
                keywords['awards'].add('penalty rates')

            if 'overtime' in full_text:
                keywords['awards'].add('overtime')

            if 'allowances' in full_text or 'allowance' in full_text:
                keywords['awards'].add('allowances')

            if 'classification' in full_text:
                keywords['awards'].add('classification')

            if 'minimum rates' in full_text or 'minimum rate' in full_text:
                keywords['awards'].add('minimum rates of pay')

            if 'casual loading' in full_text:
                keywords['awards'].add('casual loading')

            if 'shift work' in full_text:
                keywords['awards'].add('shift work')

            # Industrial disputes
            if 'industrial action' in full_text:
                keywords['industrial_disputes'].add('industrial action')
                if len(sample_docs['industrial_disputes']) < 3:
                    sample_docs['industrial_disputes'].append(name[:150])

            if re.search(r'protected (action|industrial action)', full_text):
                keywords['industrial_disputes'].add('protected industrial action')

            if 'unprotected action' in full_text:
                keywords['industrial_disputes'].add('unprotected action')

            if re.search(r'\bstrike\b', full_text):
                keywords['industrial_disputes'].add('strikes')

            if 'work stoppage' in full_text or 'stoppage' in full_text:
                keywords['industrial_disputes'].add('work stoppages')

            if 'work ban' in full_text or 'bans' in full_text:
                keywords['industrial_disputes'].add('work bans')

            if 'conciliation' in full_text:
                keywords['industrial_disputes'].add('conciliation')

            if 'arbitration' in full_text:
                keywords['industrial_disputes'].add('arbitration')

            if 'picketing' in full_text:
                keywords['industrial_disputes'].add('picketing')

            if 'lockout' in full_text:
                keywords['industrial_disputes'].add('lockouts')

            if 'ballot' in full_text:
                keywords['industrial_disputes'].add('ballot for protected action')

            # Redundancy
            if 'redundancy' in full_text:
                keywords['redundancy'].add('redundancy')
                if len(sample_docs['redundancy']) < 3:
                    sample_docs['redundancy'].append(name[:150])

            if 'genuine redundancy' in full_text:
                keywords['redundancy'].add('genuine redundancy')

            if 'severance pay' in full_text:
                keywords['redundancy'].add('severance pay')

            if 'redeployment' in full_text:
                keywords['redundancy'].add('redeployment')

            if 'consultation' in full_text:
                keywords['redundancy'].add('consultation obligations')

            if 'notice period' in full_text or 'notice of termination' in full_text:
                keywords['redundancy'].add('notice of termination')

            if 'redundancy pay' in full_text:
                keywords['redundancy'].add('redundancy pay')

            if 'position redundant' in full_text or 'role redundant' in full_text:
                keywords['redundancy'].add('position made redundant')

            # Contractors
            if re.search(r'independent contractor', full_text):
                keywords['contractors'].add('independent contractors')
                if len(sample_docs['contractors']) < 3:
                    sample_docs['contractors'].append(name[:150])

            if 'sham contract' in full_text:
                keywords['contractors'].add('sham contracting')

            if re.search(r'(employee|worker) (status|classification)', full_text):
                keywords['contractors'].add('employment status')

            if 'common law test' in full_text:
                keywords['contractors'].add('common law tests')

            if 'control test' in full_text:
                keywords['contractors'].add('control test')

            if 'principal and agent' in full_text:
                keywords['contractors'].add('principal and agent')

            if 'gig economy' in full_text or 'gig worker' in full_text:
                keywords['contractors'].add('gig economy workers')

            if 'labour hire' in full_text or 'labor hire' in full_text:
                keywords['contractors'].add('labour hire')

            if 'deemed employee' in full_text:
                keywords['contractors'].add('deemed employees')

        except Exception as e:
            continue

# Print results
for category, terms in keywords.items():
    print(f'\n\n=== {category.upper().replace("_", " ")} ===')
    print(f'Unique keywords found: {len(terms)}')
    print('\nKeywords:')
    for term in sorted(terms):
        print(f'  - {term}')
    if sample_docs[category]:
        print('\nSample cases:')
        for doc in sample_docs[category]:
            print(f'  * {doc}')
