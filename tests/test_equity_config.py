"""Test equity configuration in classification_config.py"""
import sys
sys.path.insert(0, 'src/ingestion')
import classification_config

# Find all Equity categories
equity_cats = [k for k in classification_config.CLASSIFICATION_MAP.keys() if k.startswith('Equity_')]

print('=' * 70)
print('EQUITY CONFIGURATION TEST')
print('=' * 70)
print()
print('SUCCESS: File imports correctly!')
print()
print(f'Equity categories found: {len(equity_cats)}')
print('Categories:', equity_cats)
print()

# Count total keywords
total = sum([len(v) for k, v in classification_config.CLASSIFICATION_MAP.items() if k.startswith('Equity_')])
print(f'Total Equity keywords: {total}')
print()

# Show domain mapping
print('Domain mapping for Equity:')
for cat in classification_config.DOMAIN_MAPPING.get('Equity', []):
    count = len(classification_config.CLASSIFICATION_MAP.get(cat, []))
    print(f'  - {cat}: {count} keywords')

print()
print('=' * 70)
print('VERIFICATION COMPLETE')
print('=' * 70)
