# Auto-Trigger GSW Extraction System

## Overview

The Auto-Trigger GSW Extraction system automatically queues high-authority legal documents for Global Semantic Workspace (GSW) extraction during the classification stage. This enables intelligent, priority-based processing of the most important cases first.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIFIED PIPELINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐      ┌─────────────────┐     ┌────────────┐ │
│  │ Classification│─────▶│ GSW Extraction  │────▶│   Graph    │ │
│  │   + Queue     │      │ (Priority-based)│     │  Building  │ │
│  └───────┬───────┘      └─────────────────┘     └────────────┘ │
│          │                                                       │
│          ▼                                                       │
│  ┌─────────────────┐                                           │
│  │ Priority Queue  │                                           │
│  │ (Authority-     │                                           │
│  │  based)         │                                           │
│  └─────────────────┘                                           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Components

1. **GSWExtractionQueue** (`src/ingestion/auto_gsw_trigger.py`)
   - Priority queue based on authority score
   - Checkpoint/resume capability
   - Smart filtering by court hierarchy

2. **SmartSampler** (`src/ingestion/auto_gsw_trigger.py`)
   - Court-level sampling strategies
   - Domain-based prioritization
   - Reference-based boosting

3. **CorpusDomainExtractor** (modified)
   - Integrated auto-queueing
   - Real-time priority calculation
   - Statistics tracking

4. **UnifiedPipeline** (`scripts/run_unified_pipeline.py`)
   - End-to-end orchestration
   - Batch processing
   - Progress monitoring

## Authority Thresholds

The system uses a hierarchical authority scoring system based on the Australian court hierarchy:

### Court Levels and Default Thresholds

| Court Level | Authority Score | Threshold | Sampling Strategy |
|------------|----------------|-----------|-------------------|
| **Apex** (HCA, Full Courts) | 90-100 | 90+ | All documents |
| **Appellate** (Courts of Appeal) | 70-89 | 70+ | With case references |
| **Trial** (District/Magistrates) | 50-69 | 50+ | Selective (high-priority domains) |
| **Tribunal** (AAT, etc.) | 30-49 | N/A | Skip |

### Priority Boosting

Priority scores are boosted based on:

- **Court level**: +10 for apex courts
- **Case references**: +1 per reference (max +10)
- **Legislation references**: +1 per reference (max +5)

## Usage

### Basic Usage

```bash
# Run with defaults (authority threshold 60)
python scripts/run_unified_pipeline.py

# Run with higher threshold (apex/appellate only)
python scripts/run_unified_pipeline.py --authority-threshold 80 --limit 1000

# Skip GSW extraction (classification only)
python scripts/run_unified_pipeline.py --no-gsw

# Resume from checkpoint
python scripts/run_unified_pipeline.py --resume
```

### Advanced Usage

```bash
# Custom configuration
python scripts/run_unified_pipeline.py \
  --corpus data/corpus.jsonl \
  --output data/processed/domains \
  --workspace-dir data/workspaces \
  --graph-dir data/processed/graph \
  --authority-threshold 70 \
  --limit 5000
```

### Programmatic Usage

```python
from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
from src.ingestion.auto_gsw_trigger import GSWExtractionQueue

# Initialize queue
queue = GSWExtractionQueue(min_authority=60)

# Initialize extractor with auto-queueing
extractor = CorpusDomainExtractor(
    input_path="data/corpus.jsonl",
    output_dir="data/processed/domains",
    enable_auto_gsw=True,
    gsw_queue=queue,
    gsw_min_authority=60
)

# Run classification (auto-queues high-authority docs)
stats = extractor.extract_all(limit=1000)

# Check queue
print(f"Documents queued: {queue.qsize()}")
```

## Testing

### Validation Suite

Run the comprehensive test suite:

```bash
python scripts/test_auto_gsw_trigger.py --limit 1000 --authority-threshold 80
```

The test suite validates:

1. **Queue Filtering**: Verifies only docs above threshold are queued
2. **Checkpoint Resume**: Tests save/load functionality
3. **Smart Sampling**: Validates court-level strategies

### Expected Output

```
================================================================================
TEST 1: Queue Filtering by Authority Score
================================================================================
Corpus: data/corpus.jsonl
Limit: 1,000 documents
Authority threshold: 80

Running classification...
✓ Classification complete: 1,000 documents in 0:00:15

================================================================================
QUEUE ANALYSIS
================================================================================
Total documents processed: 1,000
Documents queued for GSW: 23
Queue acceptance rate: 2.30%

Documents by court level:
  apex: 12 (52.2%)
  intermediate: 8 (34.8%)
  trial: 3 (13.0%)

================================================================================
THRESHOLD VALIDATION
================================================================================
Sample of 10 queued documents:
  [ 1] ✓ [2023] HCA 1                        | HCA      | apex         | Authority: 95
  [ 2] ✓ [2023] HCA 2                        | HCA      | apex         | Authority: 92
  [ 3] ✓ [2023] FCAFC 50                     | FCAFC    | apex         | Authority: 90
  ...

✓ PASS: All sampled documents meet authority threshold
```

## Workflow

### Stage 1: Classification + Auto-Queue

```python
# For each document during classification:
1. Extract authority score from court hierarchy
2. Calculate priority (authority + boosts)
3. If priority >= threshold:
   - Add to priority queue
   - Track in checkpoint
4. Continue classification
```

### Stage 2: GSW Extraction

```python
# Process queue in batches:
while not queue.empty():
    batch = queue.process_batch(batch_size=10)

    for doc in batch:
        # Extract GSW
        extraction = operator.extract(doc['text'])

        # Save workspace
        workspace_mgr.save(workspace_file)

        # Mark processed
        queue.mark_processed(doc)

    # Checkpoint every N batches
    queue.save_checkpoint()
```

### Stage 3: Graph Building

```python
# Build citation network from all processed data
graph_builder = SPCNetBuilder(
    input_dir=output_dir,
    output_dir=graph_dir
)
graph_builder.build()
```

## Checkpointing

### Queue Checkpoint Format

```json
{
  "processed_ids": ["[2023] HCA 1", "[2023] HCA 2", ...],
  "total_processed": 50,
  "total_queued": 150,
  "last_updated": "2025-12-06T10:30:00",
  "authority_stats": {
    "apex": 20,
    "intermediate": 25,
    "trial": 5
  }
}
```

### Checkpoint Locations

- **Queue checkpoint**: `data/processed/gsw_queue_checkpoint.json`
- **Classification checkpoint**: `data/processed/extraction_state.json`

### Resume Behavior

```bash
# Resume classification from last checkpoint
python scripts/run_unified_pipeline.py --resume

# Automatic detection:
# - Loads processed_ids to skip duplicates
# - Continues from last line number
# - Preserves queue state
```

## Performance Considerations

### Throughput

- **Classification**: ~2,000-5,000 docs/sec (CPU-bound)
- **GSW Extraction**: ~5-10 docs/sec (API-bound)
- **Queue overhead**: <1% impact on classification

### Memory Usage

- **Queue size**: ~1KB per document
- **1,000 queued docs**: ~1MB memory
- **10,000 queued docs**: ~10MB memory

### Batch Processing

Optimal batch sizes:
- **Classification checkpoint**: 5,000 documents
- **GSW extraction**: 10 documents
- **Queue checkpoint**: 50 documents

## Smart Sampling Strategies

### Apex Courts (Authority 90+)

**Strategy**: Sample ALL documents

```python
def should_sample_apex(doc):
    authority = doc['_classification']['authority_score']
    return authority >= 90
```

**Rationale**: Apex courts set binding precedent for all lower courts. Every decision is potentially precedent-setting.

### Appellate Courts (Authority 70-89)

**Strategy**: Sample if has case references

```python
def should_sample_appellate(doc):
    authority = doc['_classification']['authority_score']
    case_refs = doc['_classification']['case_refs']

    return authority >= 70 and len(case_refs) > 0
```

**Rationale**: Appellate courts that cite other cases are more likely to be developing or applying precedent.

### Trial Courts (Authority 50-69)

**Strategy**: Selective sampling (high-priority domains + case references)

```python
def should_sample_trial(doc):
    authority = doc['_classification']['authority_score']
    domain = doc['_classification']['primary_domain']
    case_refs = doc['_classification']['case_refs']

    high_priority = {'Family', 'Criminal', 'Constitutional', ...}

    return (
        authority >= 50 and
        domain in high_priority and
        len(case_refs) >= 2
    )
```

**Rationale**: Trial courts rarely set precedent, so focus on important domains with significant case law engagement.

## Statistics and Monitoring

### Queue Statistics

```python
queue_stats = queue.get_statistics()

{
    'total_queued': 150,
    'total_processed': 50,
    'current_queue_size': 100,
    'min_authority': 60,
    'authority_stats': {
        'apex': 20,
        'intermediate': 25,
        'trial': 5
    },
    'last_updated': '2025-12-06T10:30:00'
}
```

### Classification Statistics

```python
# From extractor.stats
for domain, stat in stats.items():
    print(f"{domain}:")
    print(f"  Documents: {stat.document_count}")
    print(f"  Authority stats: {stat.authority_stats}")
    print(f"  By court level: {stat.by_court_level}")
```

## Error Handling

### Classification Errors

```python
try:
    doc = json.loads(line)
    extractor._process_document(doc, file_manager, line_num)
except json.JSONDecodeError:
    continue  # Skip malformed JSON
except Exception as e:
    print(f"Error on line {line_num}: {e}")
    continue  # Continue processing
```

### GSW Extraction Errors

```python
try:
    extraction = operator.extract(text)
    workspace_mgr.save(workspace_file)
    queue.mark_processed(doc)
except Exception as e:
    print(f"Error extracting {citation}: {e}")
    # Don't mark as processed - will retry on resume
    continue
```

## Best Practices

### 1. Start with High Threshold

```bash
# Test with high threshold first (apex/appellate only)
python scripts/run_unified_pipeline.py --authority-threshold 80 --limit 1000
```

### 2. Monitor Queue Growth

```python
# Check queue size periodically
if queue.qsize() > 10000:
    print("Warning: Large queue - consider raising threshold")
```

### 3. Use Checkpoints

```bash
# Always use resume for large corpora
python scripts/run_unified_pipeline.py --resume
```

### 4. Batch Processing

```bash
# Process in smaller batches for better control
python scripts/run_unified_pipeline.py --limit 10000
# Review results, then continue
python scripts/run_unified_pipeline.py --limit 20000 --resume
```

### 5. Validate Results

```bash
# Run validation suite after changes
python scripts/test_auto_gsw_trigger.py
```

## Troubleshooting

### Issue: Queue not populating

**Check**:
1. Authority threshold too high?
2. Court hierarchy configured correctly?
3. `enable_auto_gsw=True`?

### Issue: Too many documents queued

**Solution**:
1. Raise authority threshold
2. Enable stricter smart sampling
3. Filter by domain

### Issue: Checkpoint not resuming

**Check**:
1. Checkpoint file exists?
2. Correct checkpoint path?
3. File permissions?

## Future Enhancements

### Planned Features

1. **Domain-specific thresholds**
   ```python
   thresholds = {
       'Constitutional': 50,  # Lower threshold for important domain
       'Civil': 70,           # Higher threshold for common domain
   }
   ```

2. **Time-based prioritization**
   ```python
   # Prioritize recent decisions
   if doc['year'] >= 2020:
       priority += 10
   ```

3. **Multi-queue strategy**
   ```python
   # Separate queues for different priorities
   apex_queue = GSWExtractionQueue(min_authority=90)
   appellate_queue = GSWExtractionQueue(min_authority=70)
   ```

4. **Parallel processing**
   ```python
   # Process multiple documents simultaneously
   with ThreadPoolExecutor(max_workers=5) as executor:
       futures = [executor.submit(operator.extract, doc) for doc in batch]
   ```

## References

- **Court Hierarchy**: `src/ingestion/court_hierarchy.py`
- **Classification**: `src/ingestion/corpus_domain_extractor.py`
- **GSW Schema**: `src/logic/gsw_schema.py`
- **Legal Operator**: `src/gsw/legal_operator.py`
