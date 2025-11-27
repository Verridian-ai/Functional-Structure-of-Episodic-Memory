# Benchmarks Module

A comprehensive benchmarking system for evaluating discrepancy detection in family law documents.

## Overview

This module provides tools for:
- Generating synthetic discrepancies in legal documents
- Evaluating detection system performance
- Running comprehensive benchmarks across document sets
- Generating detailed performance reports

## Module Structure

```
src/benchmarks/
├── __init__.py                    # Module exports
├── family_law_discrepancy.py      # Discrepancy generation and evaluation
└── benchmark_runner.py            # Benchmark orchestration and reporting
```

## Components

### 1. Enums

#### LegalDiscrepancyType
Legal-domain discrepancies:
- `PROPERTY_POOL` - Property division without asset pool
- `PARENTING_ORDER` - Parenting orders without children
- `SPOUSAL_MAINTENANCE` - Maintenance without legal basis
- `CHILD_SUPPORT` - Child support without children
- `CONSENT_ORDER` - Consent order without consent

#### InTextDiscrepancyType
In-text inconsistencies:
- `DATE_INCONSISTENCY` - Conflicting dates
- `PARTY_MISMATCH` - Party name changes
- `ASSET_REFERENCE` - Asset value/description conflicts
- `NUMERICAL` - Number mismatches
- `ORDER_REFERENCE` - Order ID/type conflicts

### 2. DiscrepancyInstance Dataclass

Represents a single discrepancy with fields:
- `original_text` - Original correct text
- `perturbed_text` - Modified text with discrepancy
- `discrepancy_type` - Type of discrepancy
- `span_start` - Character index where discrepancy starts
- `span_end` - Character index where discrepancy ends
- `explanation` - Human-readable explanation
- `severity` - Severity rating (1-5)
- `metadata` - Additional metadata dictionary

### 3. FamilyLawBenchmark Class

Main class for generating and evaluating discrepancies.

#### Methods:
- `generate_perturbations(document, category, num_perturbations)` - Generate discrepancies
- `evaluate_detection(predictions, ground_truth)` - Evaluate detection performance
- `generate_legal_discrepancies(document, case_type)` - Generate legal-domain discrepancies
- `apply_perturbations(document, perturbations)` - Apply perturbations to document

#### Helper Methods:
- `_generate_date_perturbations()` - Generate date inconsistencies
- `_generate_party_perturbations()` - Generate party name mismatches
- `_generate_asset_perturbations()` - Generate asset value conflicts
- `_generate_numerical_perturbations()` - Generate numerical inconsistencies
- `_generate_order_perturbations()` - Generate order reference conflicts

### 4. BenchmarkRunner Class

Orchestrates benchmark evaluation across multiple documents.

#### Methods:
- `add_document(text, category, doc_id, metadata)` - Add single document
- `add_documents_from_list(documents)` - Add multiple documents
- `run_benchmark(detection_function, num_perturbations, verbose)` - Run full benchmark
- `calculate_metrics()` - Calculate aggregate metrics
- `generate_report(output_path, include_details)` - Generate JSON report
- `export_ground_truth(output_path)` - Export ground truth data
- `clear_results()` - Clear stored results

## Usage Examples

### Example 1: Basic Perturbation Generation

```python
from src.benchmarks import FamilyLawBenchmark
from src.benchmarks.family_law_discrepancy import create_sample_document

# Create benchmark
benchmark = FamilyLawBenchmark(seed=42)

# Create sample document
document = create_sample_document("parenting")

# Generate perturbations
perturbations = benchmark.generate_perturbations(
    document, 
    "parenting", 
    num_perturbations=5
)

for perturb in perturbations:
    print(f"Type: {perturb.discrepancy_type}")
    print(f"Original: {perturb.original_text}")
    print(f"Modified: {perturb.perturbed_text}")
    print(f"Severity: {perturb.severity}/5\n")
```

### Example 2: Evaluate Detection

```python
from src.benchmarks import FamilyLawBenchmark

benchmark = FamilyLawBenchmark()
document = "..."  # Your document
ground_truth = benchmark.generate_perturbations(document, "parenting")

# Your detection system returns: [(start, end, type), ...]
predictions = your_detection_system(document)

# Evaluate
metrics = benchmark.evaluate_detection(predictions, ground_truth)
print(f"Precision: {metrics['precision']:.3f}")
print(f"Recall: {metrics['recall']:.3f}")
print(f"F1 Score: {metrics['f1_score']:.3f}")
```

### Example 3: Full Benchmark Run

```python
from src.benchmarks import BenchmarkRunner
from src.benchmarks.family_law_discrepancy import create_sample_document

# Create runner
runner = BenchmarkRunner()

# Add documents
for category in ["parenting", "property", "general"]:
    doc = create_sample_document(category)
    runner.add_document(doc, category)

# Define detection function
def my_detector(document, ground_truth):
    # Your detection logic here
    predictions = []  # List of (start, end, type) tuples
    return predictions

# Run benchmark
results = runner.run_benchmark(
    detection_function=my_detector,
    num_perturbations_per_doc=5,
    verbose=True
)

# Generate report
runner.generate_report("results/benchmark_report.json")
```

### Example 4: CLI Usage

Run as standalone script:

```bash
# Run sample benchmark
python -m src.benchmarks.benchmark_runner --mode sample --perturbations 5

# Run with custom documents
python -m src.benchmarks.benchmark_runner \
    --mode custom \
    --input documents.json \
    --output-dir results/ \
    --perturbations 10
```

## Metrics

The benchmark calculates the following metrics:

### Detection Metrics
- **Precision**: Proportion of predictions that are correct
- **Recall**: Proportion of ground truth items detected
- **F1 Score**: Harmonic mean of precision and recall
- **Span Accuracy**: Proportion of detections with exact spans

### Counts
- **True Positives**: Correct detections
- **False Positives**: Incorrect detections
- **False Negatives**: Missed discrepancies

### Aggregate Metrics
- Mean/Median/StdDev for all metrics
- Per-category breakdown
- Per-discrepancy-type breakdown
- Timing information

## Report Format

Generated reports are JSON files with structure:

```json
{
  "benchmark_info": {
    "run_start": "2025-11-27T05:35:00",
    "run_end": "2025-11-27T05:35:10",
    "duration_seconds": 10.5,
    "total_documents": 10
  },
  "aggregate_metrics": {
    "mean_precision": 0.850,
    "mean_recall": 0.750,
    "mean_f1": 0.797,
    "per_category": {...},
    "per_discrepancy_type": {...}
  },
  "detailed_results": [...]
}
```

## Integration with Existing Code

This module integrates with:
- `src.logic.gsw_schema` - Uses GSW data structures
- `src.observability.evaluation` - Can feed into evaluation pipeline
- `src.integration.cognitive_system` - Can benchmark full system

## Testing

Run tests:

```bash
# Basic functionality test
python -c "from src.benchmarks import *; print('✓ Module loads successfully')"

# Full pipeline test
python examples/benchmark_usage_example.py
```

## Future Enhancements

Potential improvements:
- Additional perturbation types (entity references, legal citations)
- Multi-document consistency checking
- Temporal reasoning discrepancies
- Integration with VSA contradiction detection
- Support for custom perturbation generators
- Hierarchical evaluation (document → section → sentence level)

## References

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory

## License

Part of the Verridian AI project.
