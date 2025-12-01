import json
from collections import Counter, defaultdict
import re

# Patterns to track
category_counts = Counter()
citation_patterns = defaultdict(list)
text_keywords = Counter()
url_patterns = Counter()
court_patterns = Counter()
all_categories_seen = Counter()

# Keywords to extract from text
admin_keywords = [
    # Immigration & Visa
    'visa', 'migration', 'refugee', 'asylum', 'deportation', 'immigration', 'citizenship',
    'temporary entry', 'permanent residency', 'skilled migration',

    # Social Security & Centrelink
    'centrelink', 'social security', 'disability support', 'pension', 'welfare',
    'family tax benefit', 'jobseeker', 'newstart', 'austudy', 'abstudy',
    'carer payment', 'age pension', 'parenting payment',

    # Freedom of Information
    'freedom of information', 'foi', 'access to information', 'information commissioner',
    'privacy', 'public records', 'government information',

    # Judicial Review
    'judicial review', 'administrative decisions', 'reviewable decision',
    'natural justice', 'procedural fairness', 'ultra vires', 'jurisdictional error',

    # Tribunal Proceedings
    'aat', 'administrative appeals tribunal', 'vcat', 'ncat', 'qcat', 'sat', 'acat',
    'tribunal', 'merits review', 'tribunal proceeding',

    # Government Decisions
    'ministerial decision', 'government decision', 'executive decision',
    'administrative decision', 'public authority', 'statutory decision',

    # Regulatory Compliance
    'regulatory', 'compliance', 'licensing', 'permit', 'approval',
    'registration', 'accreditation', 'certification',

    # Planning & Land Use
    'planning', 'land use', 'development approval', 'rezoning', 'planning permit',
    'building permit', 'local government',

    # Professional Regulation
    'professional conduct', 'disciplinary', 'professional standards',
    'medical board', 'legal services', 'professional registration',

    # General Administrative
    'proclamation', 'regulation', 'administrative law', 'ombudsman',
    'statutory interpretation', 'discretionary power'
]

def extract_keywords_from_text(text):
    """Extract matching keywords from text"""
    text_lower = text.lower()
    found = []
    for keyword in admin_keywords:
        if keyword in text_lower:
            found.append(keyword)
    return found

def extract_domain_indicators(doc):
    """Extract indicators that might suggest non-admin classification"""
    text_lower = doc.get('text', '').lower()

    indicators = []

    # Criminal indicators
    if any(word in text_lower for word in ['murder', 'assault', 'robbery', 'theft', 'drug', 'criminal', 'sentence', 'bail', 'accused', 'defendant']):
        indicators.append('Criminal')

    # Commercial indicators
    if any(word in text_lower for word in ['contract', 'breach', 'commercial', 'business', 'sale of goods', 'trade practices', 'corporation']):
        indicators.append('Commercial')

    # Property indicators
    if any(word in text_lower for word in ['property', 'real estate', 'lease', 'landlord', 'tenant', 'mortgage', 'conveyancing']):
        indicators.append('Property')

    # Family indicators
    if any(word in text_lower for word in ['divorce', 'custody', 'child support', 'matrimonial', 'family law', 'parenting']):
        indicators.append('Family')

    # Employment indicators
    if any(word in text_lower for word in ['employment', 'unfair dismissal', 'workplace', 'industrial relations', 'fair work']):
        indicators.append('Employment')

    # Tax indicators
    if any(word in text_lower for word in ['tax', 'income tax', 'gst', 'taxation', 'tax assessment', 'tax appeal']):
        indicators.append('Tax')

    # Tort indicators
    if any(word in text_lower for word in ['negligence', 'personal injury', 'defamation', 'nuisance', 'trespass', 'tort']):
        indicators.append('Torts')

    return indicators

# Track potential misclassifications
potential_misclass = []

# Read and analyze
print("Analyzing administrative.jsonl...")
with open('C:\\Users\\Danie\\Desktop\\Fuctional Structure of Episodic Memory\\data\\domains\\administrative.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i % 5000 == 0:
            print(f"Processed {i} documents...")

        doc = json.loads(line)

        # Get classification
        classif = doc.get('_classification', {})
        primary_cat = classif.get('primary_category', 'Unknown')
        all_matches = classif.get('all_matches', [])

        category_counts[primary_cat] += 1

        # Track all categories that matched
        for match in all_matches:
            if len(match) >= 1:
                all_categories_seen[match[0]] += 1

        # Get source patterns
        source = doc.get('source', 'Unknown')
        court = doc.get('court', 'Unknown')
        doc_type = doc.get('type', 'Unknown')

        url_patterns[source] += 1
        court_patterns[court] += 1

        # Extract keywords from text
        text = doc.get('text', '')
        found_keywords = extract_keywords_from_text(text)
        for kw in found_keywords:
            text_keywords[kw] += 1

        # Check for potential misclassifications
        other_domain_indicators = extract_domain_indicators(doc)
        if other_domain_indicators and len(text) > 500:  # Only flag substantive documents
            potential_misclass.append({
                'version_id': doc.get('version_id', 'Unknown'),
                'citation': doc.get('citation', 'Unknown')[:100],
                'primary_category': primary_cat,
                'suggested_domains': other_domain_indicators,
                'keywords_found': found_keywords[:5],
                'text_preview': text[:200]
            })

print(f"\nTotal documents analyzed: {sum(category_counts.values())}")

# Print results
print("\n" + "="*80)
print("ADMINISTRATIVE LAW CATEGORY BREAKDOWN")
print("="*80)
for cat, count in category_counts.most_common():
    pct = (count / sum(category_counts.values())) * 100
    print(f"{cat:30} {count:8,} ({pct:5.1f}%)")

print("\n" + "="*80)
print("ALL CATEGORIES THAT MATCHED (including secondary matches)")
print("="*80)
for cat, count in all_categories_seen.most_common():
    print(f"{cat:30} {count:8,}")

print("\n" + "="*80)
print("TOP KEYWORDS FOUND IN ADMINISTRATIVE DOCUMENTS")
print("="*80)
for keyword, count in text_keywords.most_common(40):
    pct = (count / sum(category_counts.values())) * 100
    print(f"{keyword:30} {count:8,} ({pct:5.1f}%)")

print("\n" + "="*80)
print("SOURCE DISTRIBUTION")
print("="*80)
for source, count in url_patterns.most_common(20):
    print(f"{source:40} {count:8,}")

print("\n" + "="*80)
print("COURT DISTRIBUTION")
print("="*80)
for court, count in court_patterns.most_common(20):
    print(f"{court:40} {count:8,}")

print("\n" + "="*80)
print("POTENTIAL MISCLASSIFICATIONS (first 50)")
print("="*80)
print("Documents classified as Administrative but showing strong indicators of other domains:\n")

for i, doc in enumerate(potential_misclass[:50]):
    print(f"\n{i+1}. {doc['citation']}")
    print(f"   Current: {doc['primary_category']}")
    print(f"   Suggested: {', '.join(doc['suggested_domains'])}")
    print(f"   Keywords: {', '.join(doc['keywords_found'])}")
    print(f"   Preview: {doc['text_preview']}...")

print(f"\n\nTotal potential misclassifications found: {len(potential_misclass)}")

# Save detailed results
with open('C:\\Users\\Danie\\Desktop\\Fuctional Structure of Episodic Memory\\admin_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_documents': sum(category_counts.values()),
        'category_breakdown': dict(category_counts),
        'all_matches': dict(all_categories_seen),
        'keyword_frequencies': dict(text_keywords.most_common(100)),
        'source_distribution': dict(url_patterns),
        'court_distribution': dict(court_patterns),
        'potential_misclassifications_count': len(potential_misclass),
        'sample_misclassifications': potential_misclass[:100]
    }, f, indent=2)

print("\n\nDetailed results saved to: admin_analysis_results.json")
