import json
from collections import Counter

# Additional specific keywords to look for
additional_terms = Counter()

files = [
    'data/by_court/employment.jsonl',
    'data/by_court/industrial.jsonl',
    'data/by_court/occupational.jsonl'
]

# Search patterns for employment-specific terms we might have missed
search_terms = {
    'unfair_dismissal': [
        'dismissal on notice', 'instant dismissal', 'termination on notice',
        'dismissal for cause', 'without cause', 'with cause',
        'just cause', 'good cause', 'reasonable notice',
        'statutory notice', 'common law notice',
        'garden leave', 'stood down', 'standdown',
        'suspension', 'suspended', 'suspension pending',
        'final warning', 'first warning', 'written warning',
        'verbal warning', 'counselling', 'performance plan',
        'performance improvement', 'pip',
        'frustration of contract', 'frustration',
        'automatic termination', 'abandonment',
        'deemed resignation', 'end of fixed term',
        'contract expiry', 'non-renewal'
    ],
    'general_protections': [
        'discriminatory dismissal', 'unlawful dismissal',
        'pregnancy termination', 'maternity leave',
        'paternity leave', 'adoption leave',
        'flexible working', 'flexible work request',
        'part-time request', 'job share',
        'return from leave', 'return to work',
        'injured worker', 'workplace injury',
        'workers comp claim', 'compensation claim',
        'union delegate', 'union official', 'union rep',
        'collective action', 'union activity'
    ],
    'enterprise_agreements': [
        'certified agreement', 'workplace agreement',
        'collective agreement', 'industrial agreement',
        'consent award', 'award variation',
        'common rule', 'interim award',
        'bargaining fee', 'bargaining levy',
        'agreement coverage', 'covered by agreement',
        'agreement applies', 'transitional',
        'legacy agreement', 'pre-reform agreement'
    ],
    'discrimination': [
        'family violence', 'domestic violence',
        'family and domestic violence',
        'carers responsibilities', 'caring responsibilities',
        'breastfeeding', 'breast feeding',
        'transgender', 'gender transition',
        'same sex', 'de facto',
        'religious discrimination', 'belief discrimination',
        'political opinion discrimination',
        'social origin', 'national origin',
        'medical record', 'criminal record',
        'union affiliation', 'trade union affiliation',
        'sexual preference', 'gender reassignment',
        'reasonable accommodation', 'workplace adjustment',
        'disability support', 'assistance animal',
        'modified duties', 'light duties',
        'graduated return', 'phased return'
    ],
    'workplace_safety': [
        'safety officer', 'safety rep', 'safety representative',
        'work injury', 'workplace injury', 'work-related injury',
        'occupational disease', 'industrial disease',
        'noise induced', 'hearing loss',
        'asbestos', 'dust disease', 'silicosis',
        'repetitive strain', 'rsi',
        'manual handling', 'lifting injury',
        'slip and fall', 'trip and fall',
        'machinery accident', 'equipment failure',
        'electrical hazard', 'chemical exposure',
        'confined space', 'working at heights',
        'fall from height', 'scaffolding',
        'lockout tagout', 'isolation procedure',
        'permit to work', 'hot work permit',
        'safety induction', 'toolbox talk',
        'safety inspection', 'safety audit',
        'near miss', 'incident report',
        'accident investigation', 'root cause',
        'corrective action', 'preventative action',
        'safety culture', 'safety performance'
    ],
    'awards': [
        'base rate', 'base pay', 'minimum rate',
        'all purpose rate', 'safety net',
        'wage increase', 'pay rise',
        'enterprise bargaining agreement rate', 'eba rate',
        'over-award', 'above-award',
        'award free', 'common law contract',
        'piece rate', 'commission', 'piece work',
        'productivity bonus', 'performance bonus',
        'retention payment', 'sign-on bonus',
        'first aid allowance', 'leading hand',
        'shift loading', 'night shift',
        'weekend penalty', 'sunday penalty',
        'public holiday penalty', 'double time',
        'time and a half', 'overtime penalty',
        'meal penalty', 'broken shift',
        'split shift', 'sleepover', 'live-in',
        'residential', 'camp allowance',
        'district allowance', 'remote area'
    ],
    'industrial_disputes': [
        'go slow', 'work to rule', 'overtime ban',
        'rolling stoppages', 'rotating strikes',
        'sympathy strike', 'solidarity action',
        'general strike', 'industry-wide action',
        'demarcation dispute', 'demarcation',
        'right to work', 'scab', 'blackleg',
        'secondary boycott', 'secondary action',
        'primary boycott', 'consumer boycott',
        'closed shop', 'union shop',
        'preference clause', 'union security',
        'enterprise bargaining dispute',
        'bargaining impasse', 'deadlock',
        'final offer', 'last best offer',
        'return to work order', 'back to work'
    ],
    'redundancy': [
        'forced redundancy', 'compulsory redundancy',
        'voluntary separation', 'early retirement',
        'retirement package', 'separation package',
        'redundancy pool', 'expression of interest',
        'last in first out', 'lifo', 'fifo',
        'skills-based selection', 'merit-based',
        'bumping', 'displacement',
        'outplacement', 'career transition',
        'redundancy payout', 'ex gratia',
        'golden handshake', 'departure payment',
        'leave entitlements', 'accrued leave',
        'unused leave', 'leave loading',
        'taxation of redundancy', 'etp'
    ],
    'contractors': [
        'principal contractor', 'head contractor',
        'self-employed', 'sole trader',
        'partnership', 'trust', 'company structure',
        'personal services income', 'psi',
        'alienation of personal services',
        'results test', 'unrelated clients',
        'business premises', 'advertising',
        'invoicing', 'gst registered',
        'professional indemnity', 'pi insurance',
        'own abn', 'separate entity',
        'set own hours', 'own methods',
        'supply own materials', 'own uniform',
        'economic dependence', 'sole client',
        'exclusive services', 'non-compete',
        'restraint of trade', 'garden leave clause'
    ]
}

sample_count = 200
for filepath in files:
    try:
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if count >= sample_count:
                    break
                count += 1
                doc = json.loads(line)
                text = (doc.get('name', '') + ' ' + doc.get('text', '')[:10000]).lower()

                for category, terms in search_terms.items():
                    for term in terms:
                        if term.lower() in text:
                            additional_terms[f'{category}::{term}'] += 1
    except Exception as e:
        pass

# Print findings grouped by category
print('ADDITIONAL EMPLOYMENT KEYWORDS FOUND')
print('=' * 80)

for category in ['unfair_dismissal', 'general_protections', 'enterprise_agreements',
                 'discrimination', 'workplace_safety', 'awards',
                 'industrial_disputes', 'redundancy', 'contractors']:
    cat_terms = {k.split('::')[1]: v for k, v in additional_terms.items()
                 if k.startswith(category)}
    if cat_terms:
        print(f'\n{category.upper().replace("_", " ")}:')
        for term, count in sorted(cat_terms.items(), key=lambda x: -x[1])[:20]:
            print(f'  {count:3d}x  {term}')
