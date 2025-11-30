# Tax Law Keywords Update Report

## Summary
Successfully added **998 comprehensive tax keywords** from `TAX_LAW_DOMAIN_KNOWLEDGE.md` to `classification_config.py`

## Date
2025-11-29

## Changes Made

### Structure Change
- **Previous**: 2 broad categories (`Tax_Federal`, `Tax_State`) with ~19 keywords total
- **Updated**: 11 specialized categories with 998 keywords total
- **Coverage**: Increased from <1% to ~100% of domain knowledge

### New Tax Categories Created

#### 1. Tax_Income (87 keywords)
Income tax assessment, deductions, offsets, and personal services income
- Key additions: ITAA 1936/1997, division references, assessable income types, deduction categories
- Covers: Ordinary income, statutory income, general/specific deductions, capital allowances, tax offsets, Medicare levy, PSI rules

#### 2. Tax_CGT (87 keywords)
Capital gains tax events, exemptions, concessions, and calculations
- Key additions: CGT events (A1-K6), discount methods, main residence exemption, small business concessions
- Covers: Cost base, capital proceeds, pre-CGT assets, 15-year exemption, rollover relief, value shifting

#### 3. Tax_GST (100 keywords)
Goods and Services Tax registration, supplies, credits, and adjustments
- Key additions: GST-free/input-taxed supplies, BAS reporting, margin scheme, reverse charge
- Covers: Taxable supply, input tax credits, tax invoices, adjustments, going concern, financial supplies

#### 4. Tax_Corporate (78 keywords)
Company tax, consolidation, franking, R&D, and thin capitalisation
- Key additions: Base rate entity, tax consolidation, loss carry-back, R&D tax incentive, transfer pricing
- Covers: Franking credits, consolidation regime, thin cap rules, BEPS, diverted profits tax, MAAL

#### 5. Tax_FBT (103 keywords)
Fringe benefits tax types, valuation, exemptions, and salary packaging
- Key additions: Car/loan/housing benefits, otherwise deductible rule, minor benefits, salary sacrifice
- Covers: Grossed-up values, Type 1/2 benefits, FBT year, reportable fringe benefits, ESS

#### 6. Tax_Superannuation (157 keywords)
Superannuation contributions, fund taxation, benefits, and SMSFs
- Key additions: Concessional/non-concessional contributions, Division 293, preservation rules, transfer balance cap
- Covers: SG, contribution caps, excess contributions tax, pension phase, death benefits, SMSF compliance

#### 7. Tax_State (117 keywords)
State taxes including payroll tax, land tax, and stamp duty
- Key additions: Grouping provisions, landholder duty, foreign purchaser duty, first home buyer concessions
- Covers: Payroll tax wages, land tax exemptions, stamp duty concessions, premium property duty

#### 8. Tax_International (81 keywords)
Cross-border taxation, residency, treaties, and BEPS
- Key additions: Residency tests, DTAs, PE rules, CFC attribution, FATCA/CRS
- Covers: Tax residency, foreign income, withholding tax, transfer pricing documentation, MLI, Pillar One/Two

#### 9. Tax_Avoidance (73 keywords)
Part IVA, Division 7A, and anti-avoidance provisions
- Key additions: Dominant purpose test, deemed dividends, UPE, phoenix activity, DPN
- Covers: General anti-avoidance, scheme rules, Division 7A loans, economic substance, promoter penalties

#### 10. Tax_Trusts_Partnerships (33 keywords)
Trust and partnership taxation
- Key additions: Division 6/6E, present entitlement, streaming, flow-through treatment
- Covers: Trust distributions, beneficiary entitlements, partnership allocations, family trust elections

#### 11. Tax_Administration (82 keywords)
ATO administration, PAYG, rulings, compliance, and emerging issues
- Key additions: PAYG withholding/instalments, GIC/SIC, objections, crypto-assets, gig economy
- Covers: Tax returns, TFN/ABN, audits, tax agents, TPB, cryptocurrency, remote work, ESG

## Keywords Added by Topic

### Legislation & Acts
- Income Tax Assessment Act 1936/1997 (ITAA)
- GST Act 1999
- Fringe Benefits Tax Assessment Act (FBTAA)
- Taxation Administration Act (TAA)
- Superannuation Industry (Supervision) Act
- Superannuation Guarantee (Administration) Act
- State Duties Acts, Land Tax Acts, Payroll Tax Acts

### Key Tax Concepts
**Income Tax**: Assessable income, deductions, capital allowances, franking credits, PSI, negative gearing
**CGT**: CGT events, cost base, main residence, small business concessions, rollovers, discount method
**GST**: Taxable supply, input tax credits, GST-free, input-taxed, margin scheme, going concern
**FBT**: Car benefits, loan benefits, otherwise deductible rule, minor benefits, salary packaging
**Superannuation**: Contributions (concessional/non-concessional), Division 293, preservation, TBC, SMSFs
**State Taxes**: Payroll tax grouping, land tax aggregation, stamp duty concessions, landholder duty
**International**: Tax residency, DTAs, withholding tax, CFC rules, transfer pricing, BEPS
**Anti-Avoidance**: Part IVA, Division 7A, deemed dividends, phoenix activity, economic substance

### ATO Guidance & Administration
- Taxation Rulings (TR), GSTR, Determinations (TD)
- Practice Statements (PS LA, PS GA)
- Practical Compliance Guidelines (PCG)
- Taxpayer Alerts (TA)
- Private/Public Rulings
- PAYG withholding/instalments
- GIC/SIC (interest charges)
- Objections and appeals

### Emerging Tax Issues
- Cryptocurrency & NFTs (crypto-assets, bitcoin, ethereum, blockchain, DeFi)
- Gig economy (platform workers, employee vs contractor)
- Remote work (cross-border employment, work from home)
- ESG (carbon credits, emissions trading, renewable energy)
- Tax reforms (Stage 3 tax cuts, bracket creep)
- Shadow economy (cash economy, tax gap)
- Digital economy (BEPS Pillar One/Two, global minimum tax)

## Coverage Analysis

### Before Update
- Tax_Federal: 12 keywords
- Tax_State: 7 keywords
- **Total: 19 keywords**
- Coverage: <1% of domain knowledge

### After Update
- Tax_Income: 87 keywords
- Tax_CGT: 87 keywords
- Tax_GST: 100 keywords
- Tax_Corporate: 78 keywords
- Tax_FBT: 103 keywords
- Tax_Superannuation: 157 keywords
- Tax_State: 117 keywords
- Tax_International: 81 keywords
- Tax_Avoidance: 73 keywords
- Tax_Trusts_Partnerships: 33 keywords
- Tax_Administration: 82 keywords
- **Total: 998 keywords**
- Coverage: ~100% of domain knowledge

## Impact on Classification

This comprehensive update enables:

1. **Precise Classification**: Documents can now be classified into specific tax subcategories
2. **Complete Coverage**: All major tax law domains are represented
3. **Modern Issues**: Covers emerging topics like crypto-assets, gig economy, remote work
4. **Legislative Depth**: Includes specific Division references, section numbers, and technical terms
5. **Practical Application**: Covers ATO guidance, compliance, administration, and litigation

## Files Modified

1. `src/ingestion/classification_config.py`
   - Added 11 new Tax categories
   - Added 998 keywords
   - Updated hierarchy mapping

## Files Created

1. `extract_tax_keywords.py` - Keyword extraction analysis script
2. `update_tax_keywords.py` - Update automation script
3. `missing_tax_keywords.txt` - List of missing keywords (pre-update)
4. `TAX_KEYWORDS_UPDATE_REPORT.md` - This report

## Verification

Run the following to verify the update:
```bash
cd "src/ingestion"
grep -c "'Tax_" classification_config.py  # Should show 12 (11 categories + 1 hierarchy)
```

## Next Steps

1. Test classification with tax law documents
2. Monitor classification accuracy
3. Add any additional emerging keywords as needed
4. Consider similar comprehensive updates for other law domains

## Notes

- All keywords are lowercase for consistent matching
- Keywords include abbreviations (e.g., 'cgt', 'gst', 'fbt', 'psi')
- Specific Division and section references included (e.g., 'division 7a', 's 8-1')
- Both full and abbreviated legislation names included
- Covers federal, state, and international taxation
- Includes both technical legal terms and practical administration concepts

---

**Update completed**: 2025-11-29
**Total keywords added**: 998
**Coverage**: 100% of TAX_LAW_DOMAIN_KNOWLEDGE.md
