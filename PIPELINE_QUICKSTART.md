# Pipeline Quick Start Guide

## Overview

The unified pipeline orchestrator runs the complete legal corpus processing pipeline from raw documents to query-ready system.

## 5-Minute Quick Start

### 1. Test with Small Sample

```bash
# Quick test with 100 documents (classification only)
python scripts/run_full_pipeline.py --limit 100 --stages classify

# Expected output:
# - Domain-specific TOON files in data/processed/cases/
# - Statistics in data/processed/extraction_statistics.json
# - Takes ~2-3 minutes
```

### 2. Test GSW Extraction

```bash
# Extract GSW from 10 high-authority cases
python scripts/run_full_pipeline.py --limit 100 --stages classify gsw --authority-threshold 80

# Expected output:
# - Domain workspaces in data/workspaces/
# - Takes ~5-10 minutes (depending on API speed)
```

### 3. Run Full Pipeline

```bash
# Process 1000 documents through all stages
python scripts/run_full_pipeline.py --limit 1000

# Expected output:
# - Classified documents in data/processed/
# - GSW workspaces in data/workspaces/
# - Citation graph in data/processed/graph/
# - Takes ~15-30 minutes
```

## Common Commands

### Configuration

```bash
# Show current configuration
python scripts/run_full_pipeline.py --show-config

# Validate configuration
python scripts/run_full_pipeline.py --validate-config

# Use custom config file
python scripts/run_full_pipeline.py --config configs/test.yaml

# Create example config
python scripts/run_full_pipeline.py --create-example-config my_config.yaml
```

### Stage Control

```bash
# Run specific stages
python scripts/run_full_pipeline.py --stages classify
python scripts/run_full_pipeline.py --stages gsw
python scripts/run_full_pipeline.py --stages graph

# Run multiple stages
python scripts/run_full_pipeline.py --stages classify gsw
```

### Resume and Checkpointing

```bash
# Resume from checkpoint
python scripts/run_full_pipeline.py --resume

# Clear checkpoints (start fresh)
rm -rf data/checkpoints/
```

### Tuning

```bash
# Adjust authority threshold (60=intermediate+, 70=appellate+, 90=apex)
python scripts/run_full_pipeline.py --authority-threshold 70

# Disable specific stages
python scripts/run_full_pipeline.py --disable-gsw
python scripts/run_full_pipeline.py --disable-graph

# Change GSW model
python scripts/run_full_pipeline.py --gsw-model deepseek/deepseek-chat

# Adjust rate limiting
python scripts/run_full_pipeline.py --gsw-delay 1.0
```

## Pre-Built Configurations

### Test Configuration (configs/test.yaml)

```bash
python scripts/run_full_pipeline.py --config configs/test.yaml

# Settings:
# - Document limit: 100
# - Authority threshold: 70 (appellate+)
# - GSW batch size: 5
# - Graph building: disabled
# - Verbose logging: enabled
```

### Production Configuration (configs/production.yaml)

```bash
python scripts/run_full_pipeline.py --config configs/production.yaml

# Settings:
# - Document limit: None (all documents)
# - Authority threshold: 70
# - GSW batch size: 20
# - Graph building: enabled
# - Checkpoint interval: 50,000
```

## Expected Outputs

### After Classification

```
data/processed/
├── cases/
│   ├── Family/Family.toon
│   ├── Criminal/Criminal.toon
│   ├── Tax/Tax.toon
│   └── ...
├── legislation/acts.toon
└── extraction_statistics.json
```

### After GSW Extraction

```
data/workspaces/
├── Family_workspace.json
├── Criminal_workspace.json
├── Tax_workspace.json
└── ...
```

### After Graph Building

```
data/processed/graph/
├── spcnet_nodes.toon
└── spcnet_edges.toon
```

### Checkpoints

```
data/checkpoints/
├── pipeline_state.json
├── extraction_state.json
└── gsw_queue.json
```

## Troubleshooting

### Issue: "Corpus file not found"

```bash
# Check corpus path
ls data/corpus.jsonl

# If missing, download from source or update path
python scripts/run_full_pipeline.py --corpus /path/to/corpus.jsonl
```

### Issue: API rate limits

```bash
# Increase delay between calls
python scripts/run_full_pipeline.py --gsw-delay 1.0

# Reduce batch size
python scripts/run_full_pipeline.py --gsw-batch-size 5
```

### Issue: Out of memory

```bash
# Use smaller batch size
python scripts/run_full_pipeline.py --gsw-batch-size 3

# Process fewer documents
python scripts/run_full_pipeline.py --limit 500
```

### Issue: Pipeline interrupted

```bash
# Resume from last checkpoint
python scripts/run_full_pipeline.py --resume

# If checkpoint corrupted, clear and restart
rm -rf data/checkpoints/
python scripts/run_full_pipeline.py
```

## Performance Tips

### For Speed

```bash
# Higher authority threshold = fewer GSW extractions
python scripts/run_full_pipeline.py --authority-threshold 80

# Skip graph building
python scripts/run_full_pipeline.py --disable-graph

# Use faster model
python scripts/run_full_pipeline.py --gsw-model google/gemini-2.5-flash
```

### For Quality

```bash
# Lower threshold = more GSW extractions
python scripts/run_full_pipeline.py --authority-threshold 50

# Enable all stages
python scripts/run_full_pipeline.py --stages classify gsw graph

# Use higher quality model
python scripts/run_full_pipeline.py --gsw-model anthropic/claude-3.5-sonnet
```

### For Cost Optimization

```bash
# High threshold + fast model
python scripts/run_full_pipeline.py \
  --authority-threshold 90 \
  --gsw-model google/gemini-2.5-flash

# Enable TOON format (40% token reduction)
# Already enabled by default!
```

## Next Steps

1. **Review outputs**: Check `data/processed/` and `data/workspaces/`
2. **Inspect statistics**: Open `data/processed/extraction_statistics.json`
3. **Query workspaces**: Use workspace manager to query GSW data
4. **Build applications**: Use classified data and workspaces for downstream tasks

## Full Documentation

See `docs/PIPELINE_GUIDE.md` for complete documentation.

## Environment Setup

Required environment variables:

```bash
# For OpenRouter (recommended)
export OPENROUTER_API_KEY=your_key_here

# For Google API (alternative)
export GOOGLE_API_KEY=your_key_here
```

## Testing

```bash
# Run unit tests
python -m pytest tests/test_pipeline.py -v

# Run integration test
python scripts/run_full_pipeline.py --config configs/test.yaml
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `docs/PIPELINE_GUIDE.md`
3. Check checkpoint files for error messages
4. Review logs in `logs/` directory
