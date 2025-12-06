# Full Pipeline Orchestration Guide

## Overview

The unified pipeline orchestrator runs the entire corpus processing pipeline from raw documents to query-ready system. It coordinates four main stages:

1. **Classification**: Multi-dimensional legal domain classification
2. **GSW Extraction**: Structured semantic extraction from high-authority cases
3. **Graph Building**: Citation network construction (Hier-SPCNet)
4. **Indexing**: Search index creation (future)

## Quick Start

### Basic Usage

```bash
# Run full pipeline with default settings
python scripts/run_full_pipeline.py

# Run with document limit (testing)
python scripts/run_full_pipeline.py --limit 100

# Run specific stages only
python scripts/run_full_pipeline.py --stages classify gsw

# Resume from checkpoint
python scripts/run_full_pipeline.py --resume
```

### Using Configuration Files

```bash
# Run with test configuration
python scripts/run_full_pipeline.py --config configs/test.yaml

# Run with production configuration
python scripts/run_full_pipeline.py --config configs/production.yaml

# Create custom configuration
python scripts/run_full_pipeline.py --create-example-config my_config.yaml
```

## Pipeline Stages

### Stage 1: Classification

Classifies documents into 37+ legal domains using multi-dimensional scoring:

- **Keyword patterns**: 10,500+ legal terms across 111 categories
- **Legislation references**: 500+ Acts mapped to domains
- **Landmark cases**: 150+ precedent-setting cases
- **Court hierarchy**: 50+ courts with authority scores

**Output**: Domain-specific TOON files in `data/processed/cases/`

**Configuration**:
```yaml
classification_batch_size: 100
classification_progress_interval: 5000
classification_resume: true
```

### Stage 2: GSW Extraction

Extracts structured Global Semantic Workspace from high-authority documents:

- **Authority-based queueing**: Only processes documents above threshold
- **Smart sampling**: Prioritizes apex and appellate courts
- **Model rotation**: Automatic fallback on API errors
- **TOON format**: ~40% token reduction for context

**Output**: Domain workspaces in `data/workspaces/`

**Configuration**:
```yaml
enable_auto_gsw: true
gsw_authority_threshold: 60  # 60=intermediate+, 70=appellate+, 90=apex only
gsw_batch_size: 10
gsw_model: google/gemini-2.5-flash
gsw_fallback_models:
  - google/gemini-2.5-flash
  - deepseek/deepseek-chat
  - meta-llama/llama-3.3-70b-instruct
```

### Stage 3: Graph Building

Builds citation network from classified documents:

- **Node indexing**: Extract all case citations as nodes
- **Edge extraction**: Parse citations from case text
- **TOON export**: Nodes and edges in compact format

**Output**: Graph files in `data/processed/graph/`

**Configuration**:
```yaml
enable_graph_building: true
graph_include_legislation: true
graph_min_citation_confidence: 0.7
```

### Stage 4: Indexing

*(Future implementation)*

## Configuration

### Configuration File Structure

```yaml
# Input/Output
corpus_path: data/corpus.jsonl
output_dir: data/processed
workspace_dir: data/workspaces
graph_dir: data/processed/graph

# Classification
classification_progress_interval: 5000

# GSW Extraction
enable_auto_gsw: true
gsw_authority_threshold: 60
gsw_model: google/gemini-2.5-flash

# Graph Building
enable_graph_building: true

# Processing Limits
document_limit: null  # null = all documents
max_text_length: 30000

# Checkpointing
enable_checkpoints: true
checkpoint_interval: 10000
```

### Command-Line Overrides

All configuration options can be overridden via command line:

```bash
# Override document limit
python scripts/run_full_pipeline.py --limit 1000

# Override authority threshold
python scripts/run_full_pipeline.py --authority-threshold 70

# Disable specific stages
python scripts/run_full_pipeline.py --disable-gsw --disable-graph

# Override GSW model
python scripts/run_full_pipeline.py --gsw-model deepseek/deepseek-chat

# Custom paths
python scripts/run_full_pipeline.py \
  --corpus data/my_corpus.jsonl \
  --output data/my_output \
  --workspaces data/my_workspaces
```

## Checkpointing and Resume

The pipeline automatically saves checkpoints for resume capability:

### Checkpoint Files

- `data/checkpoints/pipeline_state.json` - Overall pipeline state
- `data/checkpoints/extraction_state.json` - Classification progress
- `data/checkpoints/gsw_queue.json` - GSW extraction queue

### Resume from Checkpoint

```bash
# Resume full pipeline
python scripts/run_full_pipeline.py --resume

# Resume specific stage
python scripts/run_full_pipeline.py --resume --stages gsw
```

### Manual Checkpoint Management

```bash
# Clear all checkpoints (start fresh)
rm -rf data/checkpoints/

# Clear only GSW queue
rm data/checkpoints/gsw_queue.json
```

## Testing and Validation

### Test with Small Sample

```bash
# Quick test with 100 documents
python scripts/run_full_pipeline.py --limit 100 --stages classify

# Test GSW extraction only
python scripts/run_full_pipeline.py --limit 50 --stages gsw --authority-threshold 80
```

### Validate Configuration

```bash
# Check configuration validity
python scripts/run_full_pipeline.py --validate-config

# Show configuration summary
python scripts/run_full_pipeline.py --show-config

# Show configuration from file
python scripts/run_full_pipeline.py --config configs/production.yaml --show-config
```

## Performance Optimization

### Authority Threshold Tuning

The `gsw_authority_threshold` controls which documents get GSW extraction:

- **60**: Intermediate courts and above (~10-15% of corpus)
- **70**: Appellate courts and above (~5-8% of corpus)
- **90**: Apex courts only (~1-2% of corpus)

Higher thresholds = faster processing + lower cost, but less coverage.

### Batch Size Tuning

```yaml
# Larger batches = faster, but higher memory
gsw_batch_size: 20

# Smaller batches = slower, but safer
gsw_batch_size: 5
```

### Model Selection

```yaml
# Fast and cheap (recommended)
gsw_model: google/gemini-2.5-flash

# Higher quality but slower
gsw_model: anthropic/claude-3.5-sonnet

# Balanced
gsw_model: deepseek/deepseek-chat
```

## Monitoring Progress

### Real-Time Progress

The pipeline prints progress updates during execution:

```
[Progress] 5,000 docs | 150/sec | Family:1234 | Criminal:987 | Tax:654
[GSW] Extracting: [2023] HCA 1 (domain=Constitutional)
[Graph] Nodes: 45,234, Edges: 128,567
```

### Statistics Files

After completion, statistics are saved:

```
data/processed/extraction_statistics.json  # Classification stats
data/workspaces/{domain}_workspace.json    # GSW workspace stats
data/checkpoints/pipeline_state.json       # Overall pipeline state
```

## Error Handling

### Automatic Recovery

- **Model rotation**: Automatically switches to fallback models on API errors
- **Checkpointing**: Progress is saved every N documents
- **Error logging**: Failed documents are logged but don't stop pipeline

### Common Issues

**Issue**: API rate limits

```bash
# Increase delay between calls
python scripts/run_full_pipeline.py --gsw-delay 1.0
```

**Issue**: Out of memory

```bash
# Reduce batch size
python scripts/run_full_pipeline.py --gsw-batch-size 5
```

**Issue**: Corrupted checkpoint

```bash
# Clear checkpoints and restart
rm -rf data/checkpoints/
python scripts/run_full_pipeline.py
```

## Advanced Usage

### Stage-by-Stage Execution

Run stages independently for debugging:

```bash
# Stage 1 only
python scripts/run_full_pipeline.py --stages classify --limit 1000

# Stage 2 only (requires stage 1 complete)
python scripts/run_full_pipeline.py --stages gsw

# Stage 3 only
python scripts/run_full_pipeline.py --stages graph
```

### Custom Pipelines

Create domain-specific pipelines:

```bash
# Family law only
python scripts/run_full_pipeline.py \
  --limit 10000 \
  --authority-threshold 60 \
  --stages classify gsw

# High-authority cases only
python scripts/run_full_pipeline.py \
  --authority-threshold 90 \
  --stages gsw graph
```

### Parallel Processing (Future)

```yaml
# Enable multiprocessing (future feature)
parallel_workers: 4
use_multiprocessing: true
```

## Output Structure

After running the full pipeline:

```
data/
├── processed/
│   ├── cases/
│   │   ├── Family/
│   │   │   └── Family.toon
│   │   ├── Criminal/
│   │   │   └── Criminal.toon
│   │   └── ...
│   ├── legislation/
│   │   └── acts.toon
│   ├── graph/
│   │   ├── spcnet_nodes.toon
│   │   └── spcnet_edges.toon
│   └── extraction_statistics.json
├── workspaces/
│   ├── Family_workspace.json
│   ├── Criminal_workspace.json
│   └── ...
└── checkpoints/
    ├── pipeline_state.json
    ├── extraction_state.json
    └── gsw_queue.json
```

## API Keys

Required environment variables:

```bash
# For OpenRouter models
export OPENROUTER_API_KEY=your_key_here

# For Google models (if not using OpenRouter)
export GOOGLE_API_KEY=your_key_here
```

## See Also

- [GSW Extraction Guide](GSW_EXTRACTION_GUIDE.md)
- [Classification Guide](CLASSIFICATION_GUIDE.md)
- [Graph Building Guide](GRAPH_BUILDING_GUIDE.md)
- [TOON Format Specification](TOON_FORMAT.md)
