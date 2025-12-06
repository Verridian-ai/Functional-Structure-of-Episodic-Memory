# Benchmarking Framework - Quick Start Guide

Get started with continuous monitoring and benchmarking in 5 minutes.

## Installation

No additional dependencies required. The framework uses:
- `sqlite3` (Python standard library)
- `json` (Python standard library)
- Existing `src.observability.retrieval_scorer`

## Quick Start

### 1. Monitor a Single Query

```python
from pathlib import Path
from src.benchmarking import ContinuousMonitor

# Initialize monitor
monitor = ContinuousMonitor(Path("data/benchmarks"))

# Monitor a query
scores = monitor.monitor_query(
    query="What are my property rights?",
    response={
        'retrieved_entities': [...],  # Your retrieved entities
        'response_text': "...",       # Generated response
        'validation': {...}            # Optional VSA results
    }
)

# Check results
print(f"Composite Score: {scores['composite_score']:.3f}")
print(f"Meets Target: {scores['meets_target']}")
```

### 2. Track Benchmarks Over Time

```python
from pathlib import Path
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
for entry in history[-5:]:  # Last 5 entries
    print(f"{entry['timestamp']}: {entry['score']:.3f}")

# Analyze trends
trend = tracker.get_trend_analysis("composite_score", days=7)
print(f"Trend: {trend['trend']}")  # 'improving', 'stable', or 'declining'

tracker.close()
```

### 3. Run Full Benchmark Suite

```bash
# Run all benchmarks
python scripts/run_benchmark_suite.py

# Run specific stage
python scripts/run_benchmark_suite.py --stage retrieval

# Custom output directory
python scripts/run_benchmark_suite.py --output-dir results/benchmarks

# Quiet mode (minimal output)
python scripts/run_benchmark_suite.py --quiet
```

### 4. Generate Dashboard Metrics

```python
from pathlib import Path
from src.benchmarking import AccuracyTracker

tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Generate dashboard JSON
dashboard = {
    'current_accuracy': {},
    'trends': {},
    'alerts': tracker.get_alerts(threshold=0.80)
}

# Get current metrics
for metric in ['composite_score', 'entity_relevance', 'legal_precision']:
    history = tracker.get_metric_history(metric, days=1)
    if history:
        dashboard['current_accuracy'][metric] = history[-1]['score']

# Get trends
for metric in dashboard['current_accuracy'].keys():
    trend = tracker.get_trend_analysis(metric, days=7)
    dashboard['trends'][metric] = {
        'direction': trend['trend'],
        'current': trend['current_value']
    }

# Save
import json
with open('data/benchmarks/dashboard.json', 'w') as f:
    json.dump(dashboard, f, indent=2)

tracker.close()
```

## Common Use Cases

### Monitor Production Queries

```python
from src.benchmarking import ContinuousMonitor

monitor = ContinuousMonitor(Path("data/benchmarks/production"))

def handle_user_query(query: str):
    # Your existing query processing
    response = your_query_processor(query)

    # Monitor quality
    scores = monitor.monitor_query(query, response)

    # Alert if below threshold
    if scores['composite_score'] < 0.80:
        send_alert(f"Low quality response: {scores['composite_score']:.3f}")

    return response
```

### Daily Benchmark Automation

```python
import schedule
from pathlib import Path
from src.benchmarking import AccuracyTracker

def run_daily_benchmark():
    # Run your benchmark
    results = run_your_benchmark()

    # Track results
    tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))
    tracker.record_benchmark("daily", results)

    # Check for regressions
    trend = tracker.get_trend_analysis("composite_score", days=7)
    if trend['trend'] == 'declining':
        send_alert(f"Performance declining: {trend['change_percent']:.1f}%")

    tracker.close()

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(run_daily_benchmark)
```

### Batch Query Analysis

```python
from src.benchmarking import ContinuousMonitor

monitor = ContinuousMonitor(Path("data/benchmarks"))

# Process batch
queries = load_test_queries()
responses = [process_query(q) for q in queries]
ground_truths = load_ground_truths()

# Monitor batch
batch_stats = monitor.monitor_batch(queries, responses, ground_truths)

print(f"Batch size: {batch_stats['batch_size']}")
print(f"Avg score: {batch_stats['avg_composite_score']:.3f}")
print(f"Target met: {batch_stats['target_met_percentage']:.1f}%")
```

### Alert on Performance Issues

```python
from src.benchmarking import AccuracyTracker

tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))

# Get active alerts
alerts = tracker.get_alerts(threshold=0.80)

for alert in alerts:
    severity = alert['severity']  # 'high' or 'medium'
    metric = alert['metric']
    score = alert['score']

    if severity == 'high':  # Score < 0.70
        send_urgent_alert(f"CRITICAL: {metric} = {score:.3f}")
    else:  # Score < 0.80
        send_warning(f"Warning: {metric} = {score:.3f}")

tracker.close()
```

## File Structure

After running benchmarks, you'll have:

```
data/benchmarks/
├── accuracy.db                      # SQLite database with all history
├── metrics_log.jsonl                # Line-by-line query logs
├── dashboard.json                   # Real-time dashboard metrics
└── benchmark_report_<run_id>.json   # Detailed benchmark reports
```

## Metrics Explained

### 6 Core Metrics

1. **Entity Relevance** (0.0-1.0) - How relevant retrieved entities are
2. **Structural Accuracy** (0.0-1.0) - Graph structure coherence
3. **Temporal Coherence** (0.0-1.0) - Chronological consistency
4. **Legal Precision** (0.0-1.0) - Citation and legal accuracy
5. **Answer Completeness** (0.0-1.0) - Response quality and coverage
6. **Composite Score** (0.0-1.0) - Weighted average of all metrics

### Performance Targets

- **Composite Score**: 0.85+ (85% F1)
- **VSA Confidence**: 0.95+ (95% accuracy)
- **Individual Metrics**: 0.80+ minimum
- **Critical Threshold**: 0.70 (triggers high-priority alerts)

### Trend Indicators

- **Improving**: Recent average > historical average by 2%+
- **Declining**: Recent average < historical average by 2%+
- **Stable**: Within 2% of historical average

## Integration Examples

### With Retrieval Scorer

```python
from src.observability.retrieval_scorer import RetrievalScorer
from src.benchmarking import ContinuousMonitor

scorer = RetrievalScorer()
monitor = ContinuousMonitor(Path("data/benchmarks"))

# Score and monitor in one pass
metrics = scorer.score_retrieval(
    query=query,
    retrieved_entities=retrieved,
    expected_entities=expected,
    response_text=response
)

# Metrics object has to_dict() method
monitor._log_metrics(metrics.to_dict())
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
    'validation': {
        'overall_confidence': validation.confidence,
        'checks_passed': validation.checks_passed,
        'checks_total': validation.total_checks
    }
})
```

## Testing

Run the test suite to verify everything works:

```bash
python scripts/test_benchmarking.py
```

Expected output:
```
======================================================================
ALL TESTS PASSED
======================================================================

Generated Test Files:
  data/benchmarks/test/metrics_log.jsonl
  data/benchmarks/test/accuracy_test.db
  data/benchmarks/test/dashboard.json
```

## Troubleshooting

### Issue: "No module named 'src.benchmarking'"

**Solution**: Ensure you're running from project root:
```bash
cd /path/to/project
python scripts/run_benchmark_suite.py
```

### Issue: Database locked

**Solution**: Close all tracker instances when done:
```python
tracker = AccuracyTracker(db_path)
# ... use tracker ...
tracker.close()

# Or use context manager
with AccuracyTracker(db_path) as tracker:
    # ... use tracker ...
# Automatically closed
```

### Issue: Empty metrics log

**Solution**: Ensure output directory exists:
```python
from pathlib import Path

output_dir = Path("data/benchmarks")
output_dir.mkdir(parents=True, exist_ok=True)

monitor = ContinuousMonitor(output_dir)
```

### Issue: Trends show "insufficient_data"

**Solution**: Record more data points:
```python
# Need at least 10 data points for trends
tracker = AccuracyTracker(db_path)

for i in range(15):  # Record at least 10
    tracker.record_benchmark("test", {'composite_score': 0.8 + i*0.01})

trend = tracker.get_trend_analysis("composite_score")
# Now shows trend direction
```

## Next Steps

1. **Read the full README**: `src/benchmarking/README.md`
2. **Review sample report**: `data/benchmarks/SAMPLE_BENCHMARK_REPORT.md`
3. **Integrate with your pipeline**: Add monitoring to query handlers
4. **Set up daily benchmarks**: Schedule automated benchmark runs
5. **Create dashboard**: Build UI consuming `dashboard.json`

## Support

For questions or issues:
1. Check `src/benchmarking/README.md` for detailed documentation
2. Review test examples in `scripts/test_benchmarking.py`
3. Examine sample reports in `data/benchmarks/`

## Quick Reference

### Essential Commands

```bash
# Run full benchmark suite
python scripts/run_benchmark_suite.py

# Test framework
python scripts/test_benchmarking.py

# Run specific stage
python scripts/run_benchmark_suite.py --stage retrieval
```

### Essential Code

```python
# Monitor query
from src.benchmarking import ContinuousMonitor
monitor = ContinuousMonitor(Path("data/benchmarks"))
scores = monitor.monitor_query(query, response)

# Track over time
from src.benchmarking import AccuracyTracker
tracker = AccuracyTracker(Path("data/benchmarks/accuracy.db"))
tracker.record_benchmark("stage", metrics)
history = tracker.get_metric_history("composite_score", days=30)
tracker.close()

# Get alerts
alerts = tracker.get_alerts(threshold=0.80)
```

### Key Files

- `src/benchmarking/continuous_monitor.py` - Real-time monitoring
- `src/benchmarking/accuracy_tracker.py` - Historical tracking
- `scripts/run_benchmark_suite.py` - Full benchmark suite
- `scripts/test_benchmarking.py` - Test suite

That's it! You're ready to start monitoring and benchmarking your LAW OS system.
