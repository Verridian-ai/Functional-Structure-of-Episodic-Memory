"""Compare equity keywords between MD and config files."""

# Keywords from EQUITY_LAW_DOMAIN_KNOWLEDGE.md Section 6.1
md_keywords = [
    'trust', 'trustee', 'beneficiary', 'cestui que trust', 'settlor', 'trust property',
    'trust fund', 'breach of trust', 'express trust', 'resulting trust', 'constructive trust',
    'discretionary trust', 'charitable trust', 'purpose trust', 'unit trust', 'bare trust',
    'Quistclose trust', 'secret trust', 'mutual wills', 'trust deed', 'fiduciary',
    'fiduciary duty', 'breach of fiduciary duty', 'duty of loyalty', 'duty of care',
    'duty not to profit', 'no conflict rule', 'no profit rule', 'account of profits',
    'disgorgement', 'secret commission', 'bribe', 'conflict of interest', 'duty of good faith',
    'duty of confidence', 'duty to account', 'informed consent', "director's duty",
    "partner's duty", "agent's duty", 'specific performance', 'injunction',
    'prohibitory injunction', 'mandatory injunction', 'interlocutory injunction',
    'Mareva injunction', 'Anton Piller order', 'rescission', 'rectification',
    'equitable compensation', 'tracing', 'following', 'subrogation', 'equitable lien',
    'equitable set-off', 'estoppel', 'promissory estoppel', 'proprietary estoppel',
    'estoppel by convention', 'unconscionable conduct', 'special disadvantage',
    'undue influence', 'presumed undue influence', 'actual undue influence', 'clean hands',
    'laches', 'acquiescence', 'election', 'fraud on a power', 'Amadio principle',
    'equitable interest', 'beneficial interest', 'equitable owner', 'legal title',
    'equitable title', 'equity of redemption', 'equitable mortgage', 'equitable assignment',
    'mere equity', 'caveatable interest', 'restitutio in integrum', 'in personam',
    'in rem', 'cy-pres', 'advancement (presumption of)', 'satisfaction', 'ademption',
    'conversion (doctrine of)', 'marshalling', 'contribution (equity)', 'exoneration',
    'performance (equitable)', 'reconversion'
]

# Keywords from classification_config.py (extracted)
config_keywords = [
    'accessory liability', 'account of profits', 'acquiescence', 'actual notice',
    'actual undue influence', 'ademption', 'affirmation', 'agent duty', 'amadio principle',
    'anton piller order', 'asset freezing order', 'automatic resulting trust', 'bar to relief',
    'bare trust', 'barnes v addy', 'beneficial interest', 'beneficial owner', 'beneficiary',
    'bona fide purchaser', 'breach of fiduciary duty', 'breach of trust', 'bribe',
    'caveatable interest', 'certainty of intention', 'certainty of objects',
    'certainty of subject matter', 'cestui que trust', 'charitable trust', 'clean hands',
    'coming to equity', 'common intention constructive trust', 'conflict of interest',
    'constructive notice', 'constructive trust', 'contribution', 'conversion doctrine',
    'corporate opportunity', 'cy-pres', 'delay defeats equity', 'director duty',
    'discretionary trust', 'disgorgement', 'dishonest assistance', 'duty not to profit',
    'duty of care', 'duty of confidence', 'duty of good faith', 'duty of loyalty',
    'duty to account', 'election', 'equitable assignment', 'equitable charge',
    'equitable compensation', 'equitable defence', 'equitable estate', 'equitable interest',
    'equitable lien', 'equitable mortgage', 'equitable owner', 'equitable set-off',
    'equitable title', 'equity acts in personam', 'equity follows the law',
    'equity is equality', 'equity of redemption',
    'equity regards as done that which ought to be done', 'estoppel', 'estoppel by convention',
    'express trust', 'family trust', 'fiduciary', 'fiduciary duty', 'fixed trust',
    'following', 'fraud on a power', 'garcia principle', 'hardship', 'impossibility',
    'imputed notice', 'informed consent', 'injunction', 'institutional constructive trust',
    'interlocutory injunction', 'knowing assistance', 'knowing receipt', 'laches',
    'legal owner', 'legal title', 'mandatory injunction', 'mareva injunction',
    'marshalling', 'mere equity', 'mutual wills', 'no conflict rule', 'no profit rule',
    'notice doctrine', 'partner duty', 'performance doctrine', 'perpetual injunction',
    'presumed resulting trust', 'presumed undue influence', 'principal agent',
    'prohibitory injunction', 'promissory estoppel', 'proprietary estoppel',
    'purchaser for value', 'purpose trust', 'quia timet injunction', 'quistclose trust',
    'reconversion', 'rectification', 'remedial constructive trust', 'rescission',
    'restitutio in integrum', 'resulting trust', 'satisfaction', 'search order',
    'secret commission', 'secret trust', 'settlor', 'solicitor client fiduciary',
    'special disadvantage', 'specific performance', 'subrogation', 'superannuation trust',
    'testamentary trust', 'third party rights', 'three certainties', 'tracing', 'trust',
    'trust deed', 'trust fund', 'trust property', 'trustee', 'trustee beneficiary',
    'unauthorized profit', 'unconscionable conduct', 'undue influence', 'unit trust',
    'volunteer', 'want of mutuality'
]

# Normalize for comparison
md_keywords_lower = set([k.lower() for k in md_keywords])
config_keywords_lower = set([k.lower() for k in config_keywords])

# Find missing keywords
missing = []
for md_kw in md_keywords:
    normalized = md_kw.lower()
    # Check exact match
    if normalized in config_keywords_lower:
        continue
    # Check for variations (e.g., "director's duty" vs "director duty")
    normalized_stripped = normalized.replace("'s", '').replace('(', '').replace(')', '').replace(' of', '').replace(' the', '')
    found = False
    for config_kw in config_keywords_lower:
        config_stripped = config_kw.replace("'s", '').replace('(', '').replace(')', '').replace(' of', '').replace(' the', '')
        if normalized_stripped == config_stripped:
            found = True
            break
        # Check if core words match
        normalized_words = set(normalized_stripped.split())
        config_words = set(config_stripped.split())
        if len(normalized_words & config_words) >= 2 and len(normalized_words - config_words) == 0:
            found = True
            break
    if not found:
        missing.append(md_kw)

print('=== MISSING KEYWORDS FROM CLASSIFICATION_CONFIG.PY ===')
print(f'Total missing: {len(missing)}')
for m in sorted(missing, key=str.lower):
    print(f'  - {m}')

print()
print('=== COVERAGE ANALYSIS ===')
total_md = len(md_keywords)
total_config = len(config_keywords_lower)
total_missing = len(missing)
coverage = ((total_md - total_missing) / total_md) * 100
print(f'MD Keywords: {total_md}')
print(f'Config Keywords: {total_config}')
print(f'Missing: {total_missing}')
print(f'Coverage: {coverage:.1f}%')
