# GSW Rebuild Verification Report

**Date:** 2025-11-28
**Working Directory:** `C:\Users\Danie\Desktop\Fuctional Structure of Episodic Memory`

---

## 1. Source Data Status

**Location:** `data/domains/family.jsonl`
**Size:** 6.1 MB
**Total Documents:** 170

### Document Breakdown:
- **Decisions:** 56
- **Primary Legislation:** 52
- **Secondary Legislation:** 53
- **Bills:** 9

### Categories:
- Family_Child_Support: 45
- Family_Adoption: 27
- Family_Violence: 23
- Family_ADR: 17
- Family_Financial: 15
- Family_Property: 11
- Family_Child_Protection: 10
- Family_Enforcement: 9
- Family_General: 8
- Other categories: 4

---

## 2. Rebuild Script Verification

**Script:** `src/agents/family_law_knowledge.py`
**Status:** ✓ Verified working
**Dependencies:** ✓ All imports successful
**Test Build:** ✓ Successfully processed 100 docs in 0.12s (~820 docs/sec)

### Test Results (100 documents):
- **Actors:** 224 (2.24 per doc)
- **Questions:** 500 (5.0 per doc)
- **Spatio-temporal Links:** 8 (0.08 per doc)

---

## 3. Correct Rebuild Command

```bash
python src/agents/family_law_knowledge.py \
  --input data/domains/family.jsonl \
  --output data/domains/family_law_gsw.json \
  --progress 20
```

**Note:** The plan mentioned `--rebuild` flag, but the script uses `--input` and `--output` parameters instead.

### Command Line Options:
- `--input`: Path to family.jsonl (required)
- `--output`: Output workspace path (required)
- `--max-docs`: Limit number of documents to process (optional)
- `--progress`: Progress reporting interval in documents (default: 100)

---

## 4. Expected vs Target Metrics

### Expected Output (from 170 documents):
- **Actors:** ~380
- **Questions:** ~850
- **Spatio-temporal Links:** ~13

### Target Metrics (from plan):
- **Actors:** > 10,000 (was 5,170)
- **Questions:** > 15,000 (was 7,615)
- **Spatio-temporal Links:** > 1,500 (was 646)

### Shortfall Analysis:
- Need **~26x more actors** than current dataset will produce
- Need **~18x more questions** than current dataset will produce
- Need **~115x more links** than current dataset will produce

**To reach 10,000 actors:** ~4,500 documents needed (at 2.24 actors/doc)

---

## 5. Critical Finding

**⚠ INSUFFICIENT SOURCE DATA**

The current `family.jsonl` contains only 170 documents, which is far below what's needed to meet the target metrics outlined in the plan.

### Root Cause:
According to `data/domains/extraction_statistics.json`:
- Only 134 Family documents were extracted during the initial classification
- Many Family Law documents (2,818) were classified as Administrative due to overlapping keywords
- The extraction process needs different thresholds or multi-domain handling

### Evidence from extraction_statistics.json:
```
"Family": {
  "document_count": 134,
  "by_category": {
    "Family_General": 64,
    "Family_Parenting": 39,
    "Family_Violence": 21,
    ...
  }
}

"overlap_stats": {
  "('Administrative', 'Family')": 2818
}
```

---

## 6. Prerequisites (All Met ✓)

- [x] Python 3.13.9 installed
- [x] Required packages available:
  - `sentence-transformers`
  - `pydantic`
  - `torch`
  - `jsonlines`
- [x] GSW schema files present (`src/logic/gsw_schema.py`)
- [x] TOON encoder/decoder available (`src/utils/toon.py`)
- [x] WorkspaceManager functional (`src/gsw/workspace.py`)

---

## 7. Rebuild Process Details

The `family_law_knowledge.py` script performs the following steps:

### A. Document Parsing (FamilyLawExtractor)
- Extracts party names from citations and text
- Identifies judges/magistrates
- Determines case type using keyword matching:
  - Parenting (children, custody, relocation)
  - Property (asset pool, contributions, s.79)
  - Divorce, Child Support, Spousal Maintenance
  - Contravention
- Parses catchwords section
- Extracts court and jurisdiction

### B. GSW Construction (FamilyLawGSWBuilder)
- **Creates Actors:**
  - Party actors (Applicant, Respondent, Mother, Father)
  - Judge actors
  - Court/organization actors
  - Temporal actors (decision dates)
- **Generates Questions:**
  - 5 predictive questions per document
  - Based on case type (parenting vs property)
  - Question types: WHO, WHAT, WHEN, WHERE, WHY, HOW_MUCH
- **Creates Links:**
  - SpatioTemporalLink entities connecting parties to dates
  - Tracks relationships via chunk IDs

### C. Workspace Serialization
- Saves to JSON with metadata
- Includes TOON format support for LLM context
- Captures statistics and document counts

---

## 8. Dependencies Verification

All required modules import successfully:

```python
from src.logic.gsw_schema import (
    GlobalWorkspace, Actor, State, VerbPhrase, PredictiveQuestion,
    SpatioTemporalLink, ActorType, QuestionType, LinkType
)
from src.gsw.workspace import WorkspaceManager
from src.utils.toon import ToonEncoder, ToonDecoder
```

No missing dependencies or import errors detected.

---

## 9. Test Build Results

**Test Command:**
```bash
python src/agents/family_law_knowledge.py \
  --input data/domains/family.jsonl \
  --output data/domains/family_law_gsw_test.json \
  --progress 5
```

**Performance:**
- Processed 100 documents in 0.12 seconds
- Throughput: ~820 documents/second
- Memory: Low overhead (streaming parser)

**Output Statistics:**
- Documents: 100
- Actors: 224
- Questions: 500
- Spatio-temporal Links: 8
- Case Types:
  - General: 26
  - Parenting: 31
  - Property: 17
  - Contravention: 23
  - Divorce: 1
  - Child Support: 2

**Quality Indicators:**
- All documents successfully parsed
- No critical errors
- TOON format preview generated correctly
- WorkspaceManager saved JSON successfully

---

## 10. Recommendation

**DO NOT REBUILD GSW YET**

The current source data is insufficient to meet the target metrics.

### Action Plan:

#### Option 1: Re-extract Family Domain (Recommended)
1. Review `src/ingestion/corpus_domain_extractor.py`
2. Adjust classification thresholds for Family Law
3. Re-run extraction with multi-domain support
4. Target: Extract 4,000-5,000 Family Law documents
5. Then rebuild GSW

#### Option 2: Wait for Complete Extraction
1. Monitor the ongoing extraction process
2. Verify extraction_state.json shows completion
3. Check if family.jsonl grows to target size
4. Then rebuild GSW

#### Option 3: Use Multi-Domain Source
1. Combine family.jsonl with overlapping Administrative docs (2,818)
2. Filter for Family Law keywords in combined set
3. This could provide the needed document volume
4. Rebuild GSW from filtered dataset

### When Ready to Rebuild:

**Full Rebuild Command:**
```bash
python src/agents/family_law_knowledge.py \
  --input data/domains/family.jsonl \
  --output data/domains/family_law_gsw.json \
  --progress 100
```

**Estimated Time:** ~5-6 seconds for 4,500 documents (at 820 docs/sec)

**Expected Output:**
- Actors: ~10,080
- Questions: ~22,500
- Links: ~360
- Workspace file: ~50-100 MB JSON

---

## 11. Known Issues

### Issue 1: Insufficient Source Documents
- **Impact:** Cannot meet target metrics
- **Status:** Awaiting extraction completion
- **Resolution:** Re-run extraction or wait for completion

### Issue 2: Link Generation Rate Low
- **Observation:** Only 0.08 links per document
- **Target:** Need 0.33 links per document to reach 1,500 links
- **Note:** May need to enhance link extraction logic in builder

### Issue 3: No Previous GSW File
- **Location Expected:** `data/domains/family_law_gsw.json`
- **Status:** File does not exist
- **Impact:** Cannot compare with previous version
- **Note:** This appears to be the first GSW build for Family Law

---

## 12. Files Involved

| File | Purpose | Status |
|------|---------|--------|
| `data/domains/family.jsonl` | Source data | ✓ Present (170 docs) |
| `src/agents/family_law_knowledge.py` | Rebuild script | ✓ Verified |
| `src/logic/gsw_schema.py` | GSW data structures | ✓ Working |
| `src/gsw/workspace.py` | Workspace manager | ✓ Working |
| `src/utils/toon.py` | TOON serialization | ✓ Working |
| `data/domains/family_law_gsw.json` | Output workspace | ⚠ Will be created |
| `data/processed/extraction_state.json` | Extraction progress | ✓ Present |
| `data/domains/extraction_statistics.json` | Domain stats | ✓ Present |

---

## Conclusion

The GSW rebuild process is **fully functional and ready to execute**, but should **not be run yet** due to insufficient source data. The current 170 documents in `family.jsonl` will produce only ~380 actors, falling far short of the 10,000+ target.

**Next Steps:**
1. Investigate why only 170 Family Law documents were extracted
2. Re-run extraction with adjusted parameters
3. Aim for 4,000-5,000 documents in family.jsonl
4. Then execute rebuild command

The rebuild itself will be fast (~5 seconds) and reliable once adequate source data is available.
