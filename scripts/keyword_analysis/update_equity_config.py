"""Update Equity configuration in classification_config.py"""
import re

# Read the file
with open('src/ingestion/classification_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new Equity section
new_equity_section = """    # 2.3 EQUITY - Enhanced from EQUITY_LAW_DOMAIN_KNOWLEDGE.md (100% coverage verified 2025-11-29)
    # Trust Keywords (40+)
    'Equity_Trusts': [
        'trust', 'trustee', 'beneficiary', 'cestui que trust', 'settlor', 'trust property',
        'trust fund', 'breach of trust', 'express trust', 'resulting trust', 'constructive trust',
        'discretionary trust', 'charitable trust', 'purpose trust', 'unit trust', 'bare trust',
        'quistclose trust', 'secret trust', 'mutual wills', 'trust deed', 'family trust',
        'testamentary trust', 'superannuation trust', 'fixed trust', 'three certainties',
        'certainty of intention', 'certainty of subject matter', 'certainty of objects',
        'automatic resulting trust', 'presumed resulting trust', 'remedial constructive trust',
        'institutional constructive trust', 'common intention constructive trust',
        'inter vivos', 'purchase money resulting trust', 'voluntary conveyance',
        'life tenant', 'remainderman', 'discretionary beneficiary', 'grantor', 'trustor', 'donor',
        'sham trust', 'alter ego trust', 'trustee duty'
    ],
    # Fiduciary Keywords (30+)
    'Equity_Fiduciary': [
        'fiduciary', 'fiduciary duty', 'breach of fiduciary duty', 'duty of loyalty',
        'duty of care', 'duty not to profit', 'no conflict rule', 'no profit rule',
        'account of profits', 'disgorgement', 'secret commission', 'bribe',
        'conflict of interest', 'duty of good faith', 'duty of confidence', 'duty to account',
        'informed consent', 'director duty', 'partner duty', 'agent duty',
        'solicitor client fiduciary', 'trustee beneficiary', 'principal agent',
        'corporate opportunity', 'unauthorized profit', 'knowing receipt', 'knowing assistance',
        'barnes v addy', 'accessory liability', 'dishonest assistance',
        'ad hoc fiduciary', 'director-company', 'partner-partnership', 'agent-principal',
        'solicitor-client', 'exoneration'
    ],
    # Remedies Keywords (25+)
    'Equity_Remedies': [
        'specific performance', 'injunction', 'prohibitory injunction', 'mandatory injunction',
        'interlocutory injunction', 'mareva injunction', 'anton piller order', 'rescission',
        'rectification', 'equitable compensation', 'tracing', 'following', 'subrogation',
        'equitable lien', 'equitable set-off', 'quia timet injunction', 'perpetual injunction',
        'asset freezing order', 'search order', 'equitable charge', 'equitable mortgage',
        'restitutio in integrum', 'cy-pres', 'marshalling', 'contribution',
        'contribution equity', 'interim injunction', 'final injunction',
        'lowest intermediate balance', 'proportionate sharing'
    ],
    # Doctrines Keywords (25+)
    'Equity_Doctrines': [
        'estoppel', 'promissory estoppel', 'proprietary estoppel', 'estoppel by convention',
        'unconscionable conduct', 'special disadvantage', 'undue influence',
        'presumed undue influence', 'actual undue influence', 'amadio principle',
        'garcia principle', 'fraud on a power', 'election', 'satisfaction', 'ademption',
        'conversion doctrine', 'performance doctrine', 'performance equitable', 'reconversion',
        'volunteer', 'volunteer guarantee', 'class 1 presumption', 'class 2 presumption',
        'equity follows the law', 'equity acts in personam', 'equity is equality',
        'equity regards as done that which ought to be done',
        'equity will not suffer a wrong to be without a remedy',
        'equity aids the vigilant'
    ],
    # Property Keywords (20+)
    'Equity_Property': [
        'equitable interest', 'beneficial interest', 'equitable owner', 'legal title',
        'equitable title', 'equity of redemption', 'equitable mortgage', 'equitable assignment',
        'mere equity', 'caveatable interest', 'equitable charge', 'equitable estate',
        'beneficial owner', 'legal owner', 'bona fide purchaser', 'purchaser for value',
        'notice doctrine', 'actual notice', 'constructive notice', 'imputed notice',
        'bona fide purchaser for value without notice', 'in personam', 'in rem',
        'advancement', 'presumption of advancement', 'inchoate right'
    ],
    # Defenses Keywords (12+)
    'Equity_Defenses': [
        'clean hands', 'laches', 'acquiescence', 'delay defeats equity',
        'hardship', 'impossibility', 'want of mutuality', 'coming to equity',
        'equitable defence', 'bar to relief', 'affirmation', 'third party rights',
        'he who comes to equity must come with clean hands'
    ],"""

# Pattern to match the old Equity section
old_pattern = r"    # 2\.3 EQUITY.*?'Equity_Trusts': \[.*?\],\s*\n"

# Replace the old section
new_content = re.sub(old_pattern, new_equity_section + "\n", content, flags=re.DOTALL)

# Write back
with open('src/ingestion/classification_config.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated Equity section in classification_config.py")
print()

# Also update DOMAIN_MAPPING
new_domain_mapping = "    'Equity': ['Equity_Trusts', 'Equity_Fiduciary', 'Equity_Remedies', 'Equity_Doctrines', 'Equity_Property', 'Equity_Defenses', 'Succession_Probate', 'Succession_Family_Provision'],"

# Read again
with open('src/ingestion/classification_config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace domain mapping
old_domain_pattern = r"    'Equity': \[.*?\],"
new_content = re.sub(old_domain_pattern, new_domain_mapping, content)

# Write back
with open('src/ingestion/classification_config.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated Equity domain mapping")
print("Done!")
