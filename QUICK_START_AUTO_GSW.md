# Quick Start: Auto-Trigger GSW Extraction

## What is Auto-Trigger GSW?

Automatically extracts Global Semantic Workspace (GSW) data from high-authority legal documents during classification. Uses a priority queue to process the most important cases first.

## 30-Second Quick Start

```bash
# Run unified pipeline with defaults (authority threshold 60)
python scripts/run_unified_pipeline.py --limit 1000
```

This will:
1. Classify 1,000 documents
2. Auto-queue high-authority docs (authority ≥ 60)
3. Extract GSW from queued documents
4. Build citation graph

## Common Commands

### Test with Small Sample

```bash
# Process 1,000 docs with high threshold (apex/appellate only)
python scripts/run_unified_pipeline.py --limit 1000 --authority-threshold 80
```

### Production Run

```bash
# Full corpus with standard threshold
python scripts/run_unified_pipeline.py --authority-threshold 60
```

### Classification Only (No GSW)

```bash
# Skip GSW extraction, just classify
python scripts/run_unified_pipeline.py --no-gsw --limit 10000
```

### Resume from Checkpoint

```bash
# Continue from where you left off
python scripts/run_unified_pipeline.py --resume
```

## Validation

```bash
# Run test suite to validate system
python scripts/test_auto_gsw_trigger.py --limit 1000 --authority-threshold 80
```

Expected output:
- Queue filters correctly by authority score
- Checkpoint saves and loads
- Smart sampler strategies work

## Authority Thresholds

| Threshold | What Gets Processed |
|-----------|---------------------|
| 90+ | Apex courts only (HCA, Full Courts) |
| 80+ | Apex + major appellate courts |
| 70+ | Apex + all appellate courts |
| 60+ | **Default** - Apex + appellate + selective trial |
| 50+ | Includes more trial courts |

## Output Files

### Classification Output
```
data/processed/domains/
├── cases/
│   ├── Family/
│   │   └── Family.toon          # Classified cases
│   ├── Criminal/
│   └── ...
└── legislation/
    └── acts.toon                 # Legislation
```

### GSW Workspaces
```
data/workspaces/
├── 2023_HCA_1_workspace.json    # Individual workspaces
├── 2023_NSWCA_100_workspace.json
└── ...
```

### Graph Output
```
data/processed/graph/
├── spcnet_nodes.toon             # Citation nodes
└── spcnet_edges.toon             # Citation edges
```

### Checkpoints
```
data/processed/
├── extraction_state.json         # Classification checkpoint
└── gsw_queue_checkpoint.json     # GSW queue checkpoint
```

## How It Works

### 1. Classification + Auto-Queue

For each document:
1. Extract court info and authority score
2. Calculate priority (authority + boosts)
3. If priority ≥ threshold → add to queue
4. Continue classification

### 2. GSW Extraction

Process queue in batches:
1. Get next 10 highest-priority documents
2. Extract GSW (actors, verbs, questions, etc.)
3. Save workspace
4. Mark as processed
5. Checkpoint every 50 docs

### 3. Graph Building

Build citation network from all processed documents.

## Priority Calculation

```python
base_priority = authority_score

# Boosts
+ 10  # if apex court
+ len(case_refs)  # up to +10 for case citations
+ len(leg_refs)   # up to +5 for legislation references

final_priority = min(base_priority, 100)
```

## Troubleshooting

### Queue Not Populating

**Problem**: Queue size is 0 after classification

**Solutions**:
1. Lower authority threshold: `--authority-threshold 50`
2. Check if corpus has authority scores
3. Verify `enable_auto_gsw=True`

### Too Many Documents Queued

**Problem**: Queue size is very large (>10,000)

**Solutions**:
1. Raise threshold: `--authority-threshold 80`
2. Limit corpus: `--limit 10000`
3. Use apex-only: `--authority-threshold 90`

### Out of Memory

**Problem**: Process runs out of memory

**Solutions**:
1. Reduce limit: `--limit 1000`
2. Process in batches
3. Clear old checkpoints

### API Rate Limits

**Problem**: GSW extraction hits rate limits

**Solutions**:
1. The system automatically rotates between models
2. Add delays between batches (modify `GSW_BATCH_SIZE`)
3. Use multiple API keys

## Performance Tips

### Optimal Settings for Testing
```bash
python scripts/run_unified_pipeline.py \
  --limit 1000 \
  --authority-threshold 80 \
  --no-gsw  # Classification only first
```

### Optimal Settings for Production
```bash
python scripts/run_unified_pipeline.py \
  --authority-threshold 60 \
  --resume  # Always use checkpoints
```

### Monitor Progress

Watch the queue stats during classification:
```
Total documents processed: 10,000
Documents queued for GSW: 230
Queue acceptance rate: 2.30%

Documents by court level:
  apex: 120 (52.2%)
  intermediate: 80 (34.8%)
  trial: 30 (13.0%)
```

## Next Steps

1. **Run test**: `python scripts/test_auto_gsw_trigger.py --limit 1000`
2. **Small batch**: `python scripts/run_unified_pipeline.py --limit 5000`
3. **Review output**: Check `data/workspaces/` for GSW files
4. **Full corpus**: `python scripts/run_unified_pipeline.py --resume`

## Advanced Usage

### Custom Queue Configuration

```python
from src.ingestion.auto_gsw_trigger import GSWExtractionQueue

# Create queue with custom settings
queue = GSWExtractionQueue(
    min_authority=70,
    checkpoint_path=Path("custom_checkpoint.json")
)

# Use with extractor
extractor = CorpusDomainExtractor(
    input_path="data/corpus.jsonl",
    output_dir="data/processed/domains",
    enable_auto_gsw=True,
    gsw_queue=queue
)
```

### Process Queue Separately

```python
# Load existing queue
queue = GSWExtractionQueue(min_authority=60)

# Process in custom way
while not queue.empty():
    batch = queue.process_batch(batch_size=5)
    # Custom processing...
```

## Documentation

- **Full docs**: `docs/AUTO_GSW_TRIGGER.md`
- **Court hierarchy**: `src/ingestion/court_hierarchy.py`
- **GSW schema**: `src/logic/gsw_schema.py`

## Support

If you encounter issues:

1. Check test suite: `python scripts/test_auto_gsw_trigger.py`
2. Review logs for errors
3. Validate checkpoint files exist
4. Try with smaller `--limit` first
