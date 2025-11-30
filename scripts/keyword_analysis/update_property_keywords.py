#!/usr/bin/env python3
"""
Script to update Property Law keywords in classification_config.py
Adds all missing keywords from PROPERTY_LAW_DOMAIN_KNOWLEDGE.md
"""

import re

# Read the current file
config_path = r"C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory\src\ingestion\classification_config.py"

with open(config_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new Property Law sections with comprehensive keywords
new_prop_torrens = """    # --- 4. PROPERTY LAW (KK) ---
    # 4.1 REAL PROPERTY - Enhanced from PROPERTY_LAW_DOMAIN_KNOWLEDGE.md (100% coverage verified 2025-11-29)
    'Prop_Torrens': [
        'real property act', 'conveyancing act', 'caveat', 'indefeasibility',
        'fraud exception', 'priority dispute', 'torrens title', 'transfer of land act',
        'registered proprietor', 'certificate of title', 'folio', 'memorial', 'dealing',
        'mirror principle', 'curtain principle', 'insurance principle', 'assurance fund',
        'in personam exception', 'immediate indefeasibility', 'bona fide purchaser',
        'title by registration', 'paramount title', 'prior interest', 'subsequent interest',
        'competing interests', 'lodgment', 'registration', 'land registry', 'lrs',
        'electronic conveyancing', 'pexa', 'general law title', 'old system title',
        'folio of the register', 'instrument', 'deferred indefeasibility', 'actual notice',
        'constructive notice', 'statutory exception', 'first in time', 'possessory title',
        'qualified title', 'good title', 'marketable title', 'defect in title',
        'investigation of title', 'root of title', 'chain of title', 'historical title',
        'frazer v walker', 'breskvar v wall', 'bahr v nicolay', 'vassos v state bank',
        'pyramid building society', 'lapsing notice', 'withdrawal of caveat', 'priority notice',
        'caveator', 'caveatee', 'land title act', 'land titles act', 'registrar general',
        'land use victoria', 'landgate', 'land services sa', 'land tasmania', 'access canberra',
        'nswlrs', 'landata', 'titlesqld', 'title search', 'priority of interests',
        'priority by registration', 'void instrument', 'voidable instrument', 'section 42',
        'section 57', 'registration confers title', 'constitutive registration',
        'real property', 'land', 'title', 'deed', 'conveyance', 'transfer', 'sale of land',
        'estate', 'fee simple', 'leasehold', 'freehold', 'realty', 'immovable property',
        'interest in land', 'parcel', 'lot number', 'deposited plan', 'plan number',
        'proprietor', 'notice to registered proprietor', 'caveat priority', 'caveat lapse',
        'sustain caveat', 'court order caveat', 'registrar', 'land registry services',
        'queensland titles registry', 'titles office', 'department of lands',
        'contract for sale', 'contract of sale', 'exchange of contracts', 'vendor', 'purchaser',
        'cooling off period', 'rescission', 'deposit', 'stakeholder', 'special conditions',
        'section 32 statement', 'vendor disclosure', 'disclosure statement', 'form 1',
        'requisitions on title', 'completion', 'settlement', 'settlement date', 'time of the essence',
        'vacant possession', 'adjustments', 'apportionment', 'transfer document', 'discharge of mortgage',
        'stamp duty', 'transfer duty', 'land tax', 'foreign purchaser duty', 'pre-settlement search',
        'priority search', 'planning certificate', 'zoning certificate', 'building certificate',
        'compliance certificate', 'subject to finance', 'subject to sale', 'termination',
        'trust account', 'standard conditions', 'caveat emptor', 'objections', 'possession',
        'rates adjustment', 'stamping', 'conveyancer', 'solicitor', 'settlement agent',
        'electronic settlement', 'workspace', 'subscriber', 'verification of identity', 'voi',
        'voice verification', 'financial settlement', 'plan search', 'company search',
        'building and pest inspection', 'encumbrance', 'charge', 'lien', 'judgment', 'writ',
        'restriction', 'notification', 'license', 'profit', 'adverse interest',
        'vendor and purchaser', 'property law act', 'sale of land act', 'section 52a',
        'vendor warranties', 'section 66w', 'section 66', 'free from encumbrances',
        'statutory requirements', 'breach consequences', 'specific performance', 'damages',
        'compensation', 'waiver', 'legal advice certificate', 'auction sales', 'business day',
        'rescind', 'penalty', 'court power', 'set aside contract', 'vary contract',
        'unconscionable conduct', 'undue influence', 'inequality of bargaining power',
        'improvident transaction', 'unjust contract', 'cooling-off waiver', 'exchange date',
        'counterparts', 'deposit release', 'estate agent', 'stakeholder deposit', 'lodge caveat',
        'mortgage discharge', 'settlement statement', 'adjustment calculations', 'strata search',
        'survey', 'finance approval', 'legal advice', 'settlement documents', 'keys', 'chattels',
        'identity verification', 'authority to settle', 'discharge confirmation', 'pay stamp duty',
        'notify purchaser', 'forward title', 'arrange insurance', 'account to client',
        'final reporting', 'arnecc', 'electronic workspace', 'fixtures', 'fixtures vs chattels',
        'degree of annexation', 'purpose of annexation', 'holland v hodgson', 'reid v smith',
        'built-in wardrobes', 'hot water system', 'adverse possession', 'limitation act',
        'mulcahy v curramore', 'beneficial interest', 'equitable interest', 'purchase price'
    ],"""

# Pattern to match the old Prop_Torrens section
old_pattern = r"    # --- 4\. PROPERTY ---\s*\n\s*# 4\.1 REAL PROPERTY\s*\n\s*'Prop_Torrens': \[[^\]]+\],"

# Replace
content_new = re.sub(old_pattern, new_prop_torrens, content)

# Write back
with open(config_path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("Updated Prop_Torrens section with comprehensive keywords")
print(f"File written: {config_path}")
