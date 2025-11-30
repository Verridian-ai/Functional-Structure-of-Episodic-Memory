import json
import re
from collections import Counter

# Comprehensive keyword extraction
all_keywords = {
    'contract': Counter(),
    'consumer': Counter(),
    'corporations': Counter(),
    'insolvency': Counter(),
    'ip': Counter(),
    'competition': Counter(),
    'banking': Counter(),
    'securities': Counter(),
    'franchise': Counter(),
    'partnership': Counter()
}

# Extended patterns for each category
keyword_patterns = {
    'contract': [
        r'\b(contract\w*|agreement\w*|breach\w*|deed|covenant|undertaking|warranty|guarantee|indemnit\w*|settlement|memorandum|MOU|tender|bid|quotation|acceptance|offer|consideration|rescission|repudiation|frustration|specific performance|damages|liquidated damages|penalty clause|retention|novation|assignment|subcontract|privity|estoppel|unconscionable|undue influence|duress|misrepresentation|non-disclosure|confidentiality|restraint|exclusivity|termination|renewal|dispute resolution|arbitration|mediation)\b'
    ],
    'consumer': [
        r'\b(consumer|ACL|Australian Consumer Law|misleading|deceptive|unfair|refund|product safety|unconscionable|guarantee|warranty|acceptable quality|fit for purpose|lemon law|cooling-off|door-to-door|unsolicited|pyramid scheme|referral selling|bait advertising|two-price|price discrimination|lay-by|gift card|voucher|recall|product liability|defect|merchantable|fitness|caveat emptor|class action)\b'
    ],
    'corporations': [
        r'\b(ASIC|corporation\w*|director\w*|officer\w*|shareholder\w*|dividend|company|companies|proprietary|limited|PTY|LTD|PLC|AGM|board meeting|fiduciary|constitution|replaceable rules|members|resolution|ordinary resolution|special resolution|meeting|quorum|proxy|voting|share capital|shares|equity|preference shares|ordinary shares|partly paid|fully paid|register|transfer|transmission|pre-emptive rights|buy-back|capital reduction|dividend|distribution|solvency|statutory declaration|directors duties|care and diligence|good faith|proper purpose|conflict of interest|disclosure|related party|associate|controller|ultimate holding company|subsidiary|holding company|managed investment|responsible entity|custody|derivative|financial product|securities)\b'
    ],
    'insolvency': [
        r'\b(insolvency|insolvent|bankrupt\w*|liquidat\w*|administrat\w*|receiver\w*|voluntary administration|deed of company arrangement|DOCA|winding up|wind up|creditor\w*|debtor\w*|insolvent trading|voidable transaction|preference|unfair preference|uncommercial transaction|unreasonable director-related transaction|proof of debt|dividend|priority|secured creditor|unsecured creditor|priority creditor|employee entitlement|retention of title|PMSI|personal guarantee|phoenix activity|antecedent transaction|clawback|ipso facto|moratorium|safe harbour|small business restructure|simplified liquidation|sequestration|petition|arrangement|composition|trustee in bankruptcy|bankrupt estate|provable debt)\b'
    ],
    'ip': [
        r'\b(intellectual property|IP|patent\w*|trademark\w*|trade mark|copyright|trade secret|confidential information|industrial design|design right|passing off|infringement|misappropriation|piracy|counterfeiting|parallel import|grey import|moral rights|attribution|integrity|false attribution|registered design|invention|innovation|novelty|inventive step|utility model|patent pending|opposition|examination|grant|renewal|assignment|licence|exclusive licence|non-exclusive licence|compulsory licence|Crown use|experimental use|prior art|prior use|anticipation|obviousness|claim|specification|provisional|complete|divisional|PCT|Paris Convention|TRIPS|copyright subsistence|original work|literary work|artistic work|musical work|dramatic work|cinematograph|sound recording|broadcast|fair dealing|fair use|parody|satire|criticism|review|news reporting|educational use|statutory licence|collecting society|APRA|PPCA|CAL|registered trademark|certification mark|collective mark|defensive mark|series mark|well-known mark|deceptively similar|likelihood of confusion|descriptive|generic|distinctiveness|acquired distinctiveness|disclaimers|use requirement|genuine use|dilution|blurring|tarnishment)\b'
    ],
    'competition': [
        r'\b(ACCC|Australian Competition and Consumer Commission|competition|anti-competitive|cartel|price fixing|market sharing|bid rigging|output restriction|collective boycott|exclusive dealing|resale price maintenance|RPM|third line forcing|misuse of market power|substantial degree of market power|take advantage|predatory pricing|margin squeeze|refusal to deal|secondary boycott|merger|acquisition|control|substantial lessening of competition|SLC|market definition|barriers to entry|countervailing power|concentration|coordinated effects|unilateral effects|vertical integration|conglomerate|creeping acquisition|authorisation|notification|immunity|leniency|private enforcement|follow-on action|public benefit|competition notice|divestiture|undertaking|pecuniary penalty|treble damages|cease and desist|injunction|restraint of trade|unconscionable|monopoly|monopsony|oligopoly|market dominance)\b'
    ],
    'banking': [
        r'\b(banking|finance|financial|loan\w*|mortgage\w*|credit|security interest|PPSA|Personal Property Securities|guarantee|letter of credit|facility agreement|term loan|revolving facility|overdraft|line of credit|secured loan|unsecured loan|syndicated loan|bilateral loan|club deal|underwriting|arranger|agent|security trustee|intercreditor|subordination|pari passu|waterfall|cash sweep|prepayment|mandatory prepayment|break costs|default interest|event of default|cross-default|material adverse change|MAC|representations|warranties|covenants|affirmative covenant|negative covenant|financial covenant|leverage ratio|interest cover|debt service|gearing|LVR|loan-to-value|drawdown|utilisation|commitment|availability|accordion|all monies|guarantee and indemnity|GSA|general security agreement|specific security|fixed charge|floating charge|crystallisation|priority|perfection|registration|PPSR|attachment|circulating asset|proceeds|inventory|receivables|chattel mortgage|hire purchase|lease|finance lease|operating lease|novation|debt trading|securitisation|SPV|originator|servicer|note|tranche|senior|mezzanine|junior|subordinated|waterfall|swap|hedge|derivative|ISDA|master agreement|netting|collateral|margin|variation margin|initial margin|close-out|prudential|APRA|ADI|authorised deposit-taking institution|Basel|capital adequacy|liquidity|responsible lending|hardship|default notice|possession|foreclosure|mortgagee sale|caveat|discharge|refinance)\b'
    ],
    'securities': [
        r'\b(securities|security|investment\w*|share\w*|stock|prospectus|disclosure document|product disclosure statement|PDS|insider trading|continuous disclosure|financial services|managed fund|responsible entity|custodian|trustee|unit trust|managed investment scheme|MIS|collective investment|equity|debt|hybrid|convertible note|option|warrant|futures|derivative|financial product|debenture|bond|note|commercial paper|treasury bill|repo|reverse repo|equity swap|total return swap|CFD|contract for difference|forex|foreign exchange|spot|forward|swap|futures contract|cleared derivative|OTC|over-the-counter|ASX|securities exchange|licensed market|clearing house|settlement|CHESS|SRN|HIN|broker|dealer|adviser|financial adviser|AFS|AFSL|Australian Financial Services Licence|authorised representative|wholesale client|retail client|sophisticated investor|professional investor|experienced investor|suitability|best interests duty|safe harbour|fee disclosure|opt-in|FDS|conflicted remuneration|volume-based|soft dollar|research|placement|bookbuild|underwriting|firm underwriting|best efforts|rights issue|entitlement offer|pro rata|non-renounceable|renounceable|shortfall|institutional investor|cornerstone|lock-up|escrow|IPO|initial public offering|listing|admission|quotation|prospectus|pathfinder|roadshow|price discovery|retail offer|priority offer|takeover|scheme of arrangement|substantial holding|relevant interest|association|voting power|control|compulsory acquisition|squeeze-out|sell-out|bidder statement|target statement|independent expert|VWAP|volume weighted average price|disclosure notice|tracing notice|mandatory bid|creep|3%|20%|90%|off-market|market bid|conditional|unconditional|defeating condition|material adverse change|minimum acceptance|cash alternative|scrip|mix and match)\b'
    ],
    'franchise': [
        r'\b(franchise\w*|franchisee|franchisor|disclosure document|franchise agreement|territory|exclusive territory|area|development agreement|master franchise|sub-franchise|multi-unit|conversion|renewal|transfer|assignment|cooling-off|franchise code|franchising code of conduct|intellectual property|trade mark|brand|system|operations manual|know-how|trade secret|royalty|franchise fee|ongoing fee|marketing levy|advertising fund|fit-out|refurbishment|approved supplier|restraint|non-compete|confidentiality|training|support|quality control|brand standards|termination|breach|cure period|mediation|good faith|unconscionable|undue influence|significant capital expenditure|key money|relocation|site selection|lease|sublease|guarantee|renewal notice|failure to renew|exit strategy|buyback|first right of refusal)\b'
    ],
    'partnership': [
        r'\b(partnership|partner\w*|general partner|limited partner|silent partner|sleeping partner|junior partner|senior partner|equity partner|salaried partner|managing partner|joint venture|JV|joint venturer|consortium|alliance|collaboration|profit sharing|loss sharing|capital contribution|capital account|drawings|distribution|dissolution|retirement|expulsion|admission|goodwill|incoming partner|outgoing partner|partnership agreement|partnership deed|articles of partnership|fiduciary duty|duty of good faith|duty of loyalty|duty to account|duty of disclosure|partnership property|partnership asset|partnership liability|joint and several|indemnity|contribution|partnership by estoppel|partnership at will|fixed term partnership|professional partnership|trading partnership|investment partnership|limited partnership|incorporated limited partnership|ILP|limited liability partnership|LLP|unincorporated joint venture|incorporated joint venture|shareholders agreement|unanimous|supermajority|deadlock|buy-sell|shotgun|drag-along|tag-along|pre-emptive right|first right of refusal|good leaver|bad leaver|vesting|cliff|earn-out|non-solicitation|non-compete)\b'
    ]
}

# Process first 10000 lines for comprehensive analysis
count = 0
print("Processing corpus.jsonl for commercial law keywords...")
with open('corpus.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if count >= 10000:
            break
        try:
            data = json.loads(line)
            text = data.get('text', '').lower()

            for category, patterns in keyword_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        all_keywords[category][match.lower()] += 1
            count += 1
            if count % 1000 == 0:
                print(f"Processed {count} lines...")
        except:
            continue

print(f"\nTotal lines processed: {count}")

# Print comprehensive results
for category in all_keywords:
    print(f'\n{"="*80}')
    print(f'{category.upper()} - Top 100 Keywords/Phrases')
    print(f'{"="*80}')
    sorted_keywords = all_keywords[category].most_common(100)
    for i, (keyword, freq) in enumerate(sorted_keywords, 1):
        print(f'{i:3d}. {keyword:40s} (frequency: {freq:5d})')
