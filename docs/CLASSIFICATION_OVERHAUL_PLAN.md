# Classification System Overhaul - Implementation Plan

## Executive Summary

This document consolidates findings from 6 parallel research agents into a unified implementation plan for the Australian Legal Corpus Classification System overhaul.

**Goal**: 100% accurate primary domain assignment, complete multi-domain tagging, exact legislation citation extraction.

---

## Agent Findings Summary

### Agent 1: Legal Taxonomy Audit
- **Current State**: 22 domains, 95 subcategories, 16,407 keywords
- **Critical Gaps**:
  - Employment Law: 15-25% miss rate (missing Fair Work Act provisions, modern awards, enterprise agreements)
  - Administrative Law: Missing tribunal-specific procedures (SSAT, MRT, ART)
  - Criminal Law: State-specific codes incomplete (NSW Crimes Act vs Vic, QLD Criminal Code)
- **Recommended Additions**: 47 new subcategories, 2,300+ keywords

### Agent 2: Legislation Coverage
- **Current State**: 500+ Acts mapped to domains
- **Gaps Identified**:
  - Missing superseded legislation tracking (e.g., Workplace Relations Act 1996)
  - State legislation coverage varies (NSW: 85%, others: 40-60%)
  - Sub-legislation (Regulations, Rules) not systematically mapped
- **AGLC4 Citation Patterns**: Documented for extraction

### Agent 3: Court Codes & Citations
- **Current State**: 77 court codes in court_hierarchy.py
- **Enhanced Coverage**: 106 codes identified (29 missing)
- **Missing**:
  - Norfolk Island courts (NISC, NIFCA)
  - Specialist tribunals (SSAT, MRT, IPC, ACLEI)
  - Historical courts (CCA pre-2009)
- **Authority Scoring**: Complete hierarchy documented

### Agent 4: Legal Terminology
- **Current Dictionaries**: 5 files, 8,776+ lines
- **Critical Gaps**:
  - Latin terms: 91% missing (habeas corpus, certiorari, mandamus, etc.)
  - Old English: 89% missing (fee simple, chattels, seisin)
  - Layman explanations: 95% missing
- **Recommendation**: Create specialized dictionary files

### Agent 5: Architecture Design
- **Enhanced BOOST Scoring**: 10-factor system (vs current 5-factor)
- **MultiDomainClassification Dataclass**: Structured output format
- **Citation Pipeline**: Regex-based extraction with validation
- **Integration Points**: GSW, TOON, Graph, VSA

### Agent 6: Code Quality Audit
- **Overall Score**: B
- **Critical Issues**:
  - Dead `ToonFileManager` class (lines 455-523 never used)
  - Markdown artifacts in keywords (```python, ##, etc.)
  - Silent error handling (no logging)
  - 631KB classification_config.py needs splitting
- **Refactoring Priority**: High

---

## Implementation Phases

### Phase 1: Critical Bug Fixes (Immediate)
**Priority**: P0 - Must fix before any other changes

1. **Remove Dead Code**
   - Delete unused `ToonFileManager` class (lines 455-523)
   - Clean up duplicate class definitions

2. **Fix Keyword Contamination**
   - Remove markdown artifacts from CLASSIFICATION_MAP
   - Validate all 16,407 keywords for format issues

3. **Add Error Logging**
   - Replace silent exception handling with proper logging
   - Add classification failure tracking

### Phase 2: Enhanced Classification Architecture
**Priority**: P1 - Core system improvements

1. **Implement MultiDomainClassification**
   ```python
   @dataclass
   class MultiDomainClassification:
       document_id: str
       primary_domain: str
       primary_confidence: float
       secondary_domains: List[Tuple[str, float]]
       document_type: str
       citation_type: str
       legislation_refs: List[LegislationRef]
       case_refs: List[CaseRef]
       court_info: Optional[CourtInfo]
       authority_score: int
       binding_status: str
       boost_breakdown: Dict[str, int]
   ```

2. **Implement 10-Factor BOOST Scoring**
   - BOOST 1: Citation match (+10)
   - BOOST 2: Jurisdiction alignment (+15-20)
   - BOOST 3: Court domain hint (+25)
   - BOOST 4: Legislation reference (+15)
   - BOOST 5: Case law reference (+10)
   - BOOST 6: Case title patterns (+15-20)
   - NEW BOOST 7: Multi-domain confidence (+5-10)
   - NEW BOOST 8: Legislation status (current vs superseded) (+10/-5)
   - NEW BOOST 9: Common law vs statute distinction (+5)
   - NEW BOOST 10: Document type weighting (+5-15)

3. **Citation Extraction Pipeline**
   - Medium neutral: `[YYYY] COURT NUM`
   - Authorized reports: `(YYYY) VOL REPORT PAGE`
   - Legislation citations: `Act Name YYYY (Jurisdiction) s X`
   - Sub-section extraction: `s 51(xxvi)`, `reg 4.12`

### Phase 3: Taxonomy Expansion
**Priority**: P2 - Coverage improvements

1. **Employment Law Expansion**
   - Add Fair Work Act 2009 provisions (Pt 2-1, 3-1, 3-2, 3-3, 3-4)
   - Modern Awards keywords (120+ awards)
   - Enterprise Agreement terminology
   - WorkCover/SafeWork variations by state

2. **Administrative Law Expansion**
   - Tribunal-specific subcategories (AAT, SSAT, MRT, ART)
   - Procedural keywords (merits review, judicial review, privative clause)
   - Migration-specific subdivisions (visa classes, protection claims)

3. **Criminal Law Expansion**
   - State-specific offence categories
   - Code vs common law jurisdiction mapping
   - Sentencing terminology by jurisdiction

4. **New Domain Coverage**
   - Environmental/Native Title Law (split from Property)
   - International Law (treaties, extradition)
   - Succession/Probate Law (wills, estates)

### Phase 4: Court & Citation Enhancements
**Priority**: P2 - Reference data improvements

1. **Add Missing Court Codes (29)**
   ```python
   # Norfolk Island
   'NISC': {'name': 'Norfolk Island Supreme Court', ...},
   'NIFCA': {'name': 'Norfolk Island Federal Court Appeal', ...},

   # Specialist Tribunals
   'SSAT': {'name': 'Social Security Appeals Tribunal', ...},
   'MRT': {'name': 'Migration Review Tribunal', ...},
   'IPC': {'name': 'Information and Privacy Commission', ...},
   ```

2. **Report Series Expansion**
   - Add 15 missing report series
   - Include domain hints for specialized reports

3. **Binding Precedent Logic**
   - Implement `get_binding_authority()` with full hierarchy
   - Cross-jurisdiction persuasive authority scoring

### Phase 5: Dictionary Enhancements
**Priority**: P3 - Terminology improvements

1. **Create Latin Legal Terms Dictionary**
   - 200+ terms with definitions
   - Usage context indicators

2. **Create Historical Terms Dictionary**
   - Old English property terms
   - Historical procedural terminology

3. **Create Layman's Dictionary**
   - Plain English explanations
   - Cross-references to technical terms

### Phase 6: Integration & Testing
**Priority**: P1 - Validation

1. **Downstream Pipeline Verification**
   - GSW extraction accuracy
   - TOON encoding compatibility
   - Graph building integrity
   - Search/retrieval relevance

2. **Benchmark Suite**
   - 100 manually-labeled test documents
   - Domain classification accuracy metrics
   - Multi-domain detection rates
   - Citation extraction precision/recall

---

## File Structure Changes

### Files to Modify
1. `src/ingestion/corpus_domain_extractor.py`
   - Remove dead ToonFileManager class
   - Implement 10-factor BOOST
   - Add MultiDomainClassification output

2. `src/ingestion/classification_config.py`
   - Clean keyword contamination
   - Split into domain-specific modules

3. `src/ingestion/court_hierarchy.py`
   - Add 29 missing court codes
   - Implement binding precedent logic

4. `src/ingestion/legislation_patterns.py`
   - Add superseded legislation tracking
   - Expand sub-legislation patterns

5. `src/ingestion/case_patterns.py`
   - Add 50+ missing landmark cases
   - Expand citation extraction patterns

### New Files to Create
1. `src/ingestion/domains/employment.py` - Employment Law keywords
2. `src/ingestion/domains/administrative.py` - Admin Law keywords
3. `src/ingestion/domains/criminal.py` - Criminal Law keywords
4. `src/ingestion/dictionaries/latin_terms.py` - Latin legal terms
5. `src/ingestion/dictionaries/historical_terms.py` - Historical terms
6. `src/ingestion/multi_domain_classifier.py` - Enhanced classifier

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Primary domain accuracy | ~85% | 98%+ |
| Multi-domain detection | ~60% | 95%+ |
| Employment Law accuracy | 75-85% | 98%+ |
| Citation extraction precision | ~80% | 99%+ |
| Legislation reference recall | ~70% | 95%+ |
| Court code coverage | 77 codes | 106 codes |
| Keyword quality (no contamination) | ~95% | 100% |

---

## Implementation Order

1. **Day 1**: Phase 1 (Bug Fixes) - Clean dead code, fix keywords
2. **Day 2-3**: Phase 2 (Architecture) - MultiDomainClassification, 10-factor BOOST
3. **Day 4-5**: Phase 3 (Taxonomy) - Employment, Admin, Criminal expansion
4. **Day 6**: Phase 4 (Courts) - Add missing codes, binding logic
5. **Day 7**: Phase 5 (Dictionaries) - Latin, historical terms
6. **Day 8**: Phase 6 (Testing) - Integration validation, benchmarks

---

## Risk Mitigation

1. **Backward Compatibility**: All changes maintain existing API signatures
2. **Incremental Deployment**: Each phase can be deployed independently
3. **Rollback Plan**: Git branches per phase for easy reversion
4. **Performance**: Maintain streaming capability for 8.8GB+ corpus

---

## Approval Checkpoints

- [ ] Phase 1 complete: Dead code removed, keywords cleaned
- [ ] Phase 2 complete: Enhanced classification architecture deployed
- [ ] Phase 3 complete: Taxonomy expanded for priority domains
- [ ] Phase 4 complete: Court codes and citations enhanced
- [ ] Phase 5 complete: Dictionaries created
- [ ] Phase 6 complete: All tests passing, benchmarks met
