# Benchmarking Framework

Comprehensive benchmarking and continuous monitoring for LAW OS system accuracy.

## Overview

This framework provides continuous monitoring and evaluation using a 6-metric scoring system, integrated with the existing retrieval scorer and CLAUSE framework for legal discrepancy detection.

## Components

### 1. Continuous Monitor (`continuous_monitor.py`)

Real-time monitoring of query-response pairs with comprehensive accuracy scoring.

```python
from src.benchmarking import ContinuousMonitor

# Initialize monitor
monitor = ContinuousMonitor(Path("data/benchmarks"))

# Monitor a query
scores = monitor.monitor_query(
    query="What are my property rights after separation?",
    response={
        'retrieved_entities': entities,
        'response_text': text,
        'validation': vsa_results
    },
    ground_truth=optional_ground_truth
)

print(f"Composite Score: {scores['composite_score']:.3f}")
print(f"Meets Target: {scores['meets_target']}")
```

**Features:**
- Real-time query monitoring
- 6-metric scoring integration
- Supervised and unsupervised evaluation
- JSONL logging for continuous tracking
- VSA validation confidence tracking
- Session statistics

### 2. Accuracy Tracker (`accuracy_tracker.py`)

SQLite-based persistent storage for historical benchmark tracking.

```python
from src.benchmarking import AccuracyTracker

# Initialize tracker
tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Record benchmark results
tracker.record_benchmark("retrieval", {
    'composite_score': 0.87,
    'entity_relevance': 0.90,
    'legal_precision': 0.85
})

# Get historical data
history = tracker.get_metric_history("composite_score", days=30)

# Analyze trends
trend = tracker.get_trend_analysis("entity_relevance", days=7)
print(f"Trend: {trend['trend']}")  # 'improving', 'stable', or 'declining'

# Get alerts
alerts = tracker.get_alerts(threshold=0.80)
for alert in alerts:
    print(f"{alert['severity']}: {alert['metric']} = {alert['score']:.3f}")
```

**Features:**
- Persistent SQLite storage
- Historical metric queries
- Trend analysis
- Alert generation
- CSV export capabilities
- Suite run tracking

### 3. Benchmark Suite (`scripts/run_benchmark_suite.py`)

Comprehensive benchmark suite running 5 major benchmarks:

1. **Classification Accuracy** - Document categorization
2. **GSW Extraction Quality** - Entity extraction evaluation
3. **Retrieval Precision** - 6-metric retrieval scoring
4. **VSA Validation Accuracy** - Hallucination detection
5. **End-to-End Pipeline** - Complete workflow testing

```bash
# Run full benchmark suite
python scripts/run_benchmark_suite.py

# Run specific stage
python scripts/run_benchmark_suite.py --stage retrieval

# Custom output directory
python scripts/run_benchmark_suite.py --output-dir results/benchmarks
```

## 6-Metric Scoring System

All benchmarks use the comprehensive 6-metric scoring system:

| Metric | Weight | Description | Target |
|--------|--------|-------------|--------|
| **Entity Relevance** | 25% | Accuracy of retrieved entities | 0.90+ |
| **Structural Accuracy** | 20% | Graph structure coherence | 0.85+ |
| **Temporal Coherence** | 15% | Chronological consistency | 0.85+ |
| **Legal Precision** | 20% | Citation and legal accuracy | 0.80+ |
| **Answer Completeness** | 20% | Response quality | 0.85+ |
| **Composite Score** | - | Weighted average | **0.85+** |

### Additional Metrics

- **Citation Accuracy** - Statutory reference correctness
- **Role Binding Accuracy** - Entity-role assignment accuracy
- **VSA Confidence** - Validation confidence score (target: 0.95+)
- **Hallucination Risk** - 1.0 - VSA confidence

## CLAUSE Framework Integration

Integration with CLAUSE paper (arXiv:2412.12120) for legal discrepancy detection:

### 10 Discrepancy Categories

**Legal Discrepancies (5):**
1. Payment arrangements
2. Parenting orders
3. Maintenance obligations
4. Child support
5. Consent orders

**In-Text Discrepancies (5):**
1. Date inconsistencies
2. Party name errors
3. Numerical discrepancies
4. Legal reference errors
5. Order contradictions

```python
def benchmark_with_clause_framework():
    """Run CLAUSE framework benchmark."""
    benchmark = FamilyLawBenchmark()

    # Test across all 10 categories
    results = {
        'accuracy': 0.0,
        'legal_discrepancies': {},
        'text_discrepancies': {},
        'target_met': False  # Target: 95% accuracy
    }

    return results
```

## Benchmark Stages

### 1. Classification Accuracy

Tests document classification into categories:
- Parenting orders
- Property settlement
- Child support
- General family law

**Metrics:**
- Accuracy, Precision, Recall, F1
- Per-category F1 scores
- Composite score

### 2. GSW Extraction Quality

Tests extraction of:
- Actors (parties, judges, witnesses)
- States (legal states, property states)
- Verb phrases (actions, orders)
- Spatio-temporal links

**Metrics:**
- Per-component F1 scores
- Entity relevance
- Structural accuracy
- Temporal coherence

### 3. Retrieval Precision

Tests graph retrieval using full 6-metric system:

```python
scorer = RetrievalScorer()
metrics = scorer.score_retrieval(
    query=query,
    retrieved_entities=entities,
    expected_entities=ground_truth,
    response_text=response
)
```

### 4. VSA Validation Accuracy

Tests validation capabilities:
- Hallucination detection
- Citation verification
- Logical consistency
- Temporal consistency
- Entity grounding

**Target:** 95% validation confidence (CLAUSE paper standard)

### 5. End-to-End Pipeline

Tests complete workflow:
1. Document ingestion
2. Classification
3. GSW extraction
4. Graph construction
5. Query processing
6. Response generation
7. VSA validation

**Metrics:** All 6 core metrics plus pipeline success rate

## Dashboard Metrics

The framework generates real-time dashboard metrics in JSON format:

```json
{
  "generated_at": "2025-01-15T10:30:00",
  "current_accuracy": {
    "composite_score": 0.87,
    "entity_relevance": 0.89,
    "legal_precision": 0.84
  },
  "trends": {
    "composite_score": {
      "direction": "improving",
      "current": 0.87,
      "mean": 0.85,
      "change_percent": 2.3
    }
  },
  "alerts": [
    {
      "metric": "legal_precision",
      "score": 0.78,
      "severity": "medium",
      "threshold": 0.80
    }
  ],
  "stage_summaries": {
    "retrieval": {
      "metrics": {...}
    }
  }
}
```

## Usage Examples

### Monitor Production Queries

```python
from src.benchmarking import ContinuousMonitor

monitor = ContinuousMonitor(Path("data/benchmarks"))

# In your query handler
def handle_query(query: str) -> Dict:
    # Process query
    response = process_query(query)

    # Monitor quality
    scores = monitor.monitor_query(query, response)

    # Check if meets target
    if not scores['meets_target']:
        logger.warning(f"Query below target: {scores['composite_score']:.3f}")

    return response
```

### Track Benchmark History

```python
from src.benchmarking import AccuracyTracker

tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Record daily benchmark
metrics = run_daily_benchmark()
tracker.record_benchmark("daily", metrics)

# Analyze trends
trend = tracker.get_trend_analysis("composite_score", days=30)

if trend['trend'] == 'declining':
    send_alert(f"Composite score declining: {trend['change_percent']:.1f}%")
```

### Run Continuous Monitoring

```python
from datetime import datetime
from src.benchmarking import ContinuousMonitor, AccuracyTracker

# Initialize
monitor = ContinuousMonitor(Path("data/benchmarks"))
tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Monitor batch of queries
batch_scores = monitor.monitor_batch(queries, responses, ground_truths)

# Record in tracker
tracker.record_benchmark(
    stage="production",
    metrics=batch_scores,
    metadata={'batch_size': len(queries)}
)

# Generate dashboard
dashboard = generate_dashboard_metrics(tracker, Path("data/benchmarks/dashboard.json"))
```

## Performance Targets

Based on arXiv:2511.07587 (Functional Structure) and arXiv:2412.12120 (CLAUSE):

| Component | Target | Benchmark |
|-----------|--------|-----------|
| Composite Score | 0.85+ | 85% F1 (Functional Structure) |
| VSA Confidence | 0.95+ | 95% accuracy (CLAUSE) |
| Entity Relevance | 0.90+ | 90% precision |
| Legal Precision | 0.80+ | 80% citation accuracy |
| Pipeline Success | 0.95+ | 95% completion rate |

## Integration Points

### With Retrieval Scorer

```python
from src.observability.retrieval_scorer import RetrievalScorer
from src.benchmarking import ContinuousMonitor

scorer = RetrievalScorer()
monitor = ContinuousMonitor(Path("data/benchmarks"))

# Scorer provides detailed metrics
metrics = scorer.score_retrieval(...)

# Monitor tracks over time
monitor._log_metrics(metrics.to_dict())
```

### With CLAUSE Framework

```python
from src.benchmarks.family_law_discrepancy import FamilyLawBenchmark
from src.benchmarking import AccuracyTracker

benchmark = FamilyLawBenchmark()
tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Run CLAUSE benchmark
results = benchmark_with_clause_framework()

# Track results
tracker.record_benchmark("clause_framework", {
    'accuracy': results['accuracy'],
    'target_met': results['target_met']
})
```

### With VSA Validation

```python
from src.validation.statutory_rag import StatutoryRAGValidator
from src.benchmarking import ContinuousMonitor

validator = StatutoryRAGValidator("data/statutory_corpus")
monitor = ContinuousMonitor(Path("data/benchmarks"))

# Validate and monitor
validation = validator.validate_extraction(extraction, source_text)
scores = monitor.monitor_query(query, response={
    'retrieved_entities': entities,
    'response_text': text,
    'validation': validation
})

# VSA metrics automatically included
print(f"VSA Confidence: {scores['vsa_confidence']:.3f}")
print(f"Hallucination Risk: {scores['hallucination_risk']:.3f}")
```

## Database Schema

### benchmark_runs table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | TEXT | ISO timestamp |
| stage | TEXT | Benchmark stage |
| metric_name | TEXT | Metric identifier |
| score | REAL | Metric value (0.0-1.0) |
| metadata | TEXT | JSON metadata |
| run_id | TEXT | Suite run identifier |

### benchmark_suite_runs table

| Column | Type | Description |
|--------|------|-------------|
| run_id | TEXT | Primary key |
| start_time | TEXT | Suite start time |
| end_time | TEXT | Suite end time |
| total_benchmarks | INTEGER | Number of benchmarks |
| benchmarks_passed | INTEGER | Benchmarks meeting target |
| overall_score | REAL | Average composite score |
| status | TEXT | completed/failed/partial |
| metadata | TEXT | JSON metadata |

## Files Generated

```
data/benchmarks/
├── accuracy.db                      # SQLite database
├── metrics_log.jsonl                # Continuous monitoring log
├── dashboard.json                   # Real-time dashboard metrics
└── benchmark_report_<run_id>.json   # Detailed benchmark reports
```

## Best Practices

1. **Continuous Monitoring**: Monitor all production queries in real-time
2. **Daily Benchmarks**: Run full benchmark suite daily to track trends
3. **Alert Thresholds**: Set appropriate thresholds (0.80 for warnings, 0.70 for critical)
4. **Trend Analysis**: Review 7-day and 30-day trends weekly
5. **Ground Truth**: Include ground truth when available for supervised evaluation
6. **VSA Integration**: Always include VSA validation results
7. **Dashboard Updates**: Regenerate dashboard metrics hourly in production

## References

- **Functional Structure of Episodic Memory** (arXiv:2511.07587) - 85% F1 target
- **CLAUSE: Legal Hallucination Benchmark** (arXiv:2412.12120) - 95% accuracy target
- **LAW OS Architecture** - 6-metric scoring system design

## Future Enhancements

- [ ] A/B testing framework integration
- [ ] Automated regression detection
- [ ] Machine learning trend prediction
- [ ] Real-time alerting via webhooks
- [ ] Integration with CI/CD pipelines
- [ ] Multi-model comparison benchmarks
