# Backend: Evaluation Module

The **Evaluation Module** provides multi-judge evaluation using multiple LLM models (GPT-4o, Claude, Gemini) to assess AI-generated responses with consensus-based scoring.

## Overview

**Location**: `src/evaluation/`

```
┌──────────────────────────────────────────────────────┐
│          MULTI-JUDGE EVALUATOR                        │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────────────────────────────────────┐     │
│  │         MultiJudgeEvaluator                │     │
│  │                                            │     │
│  │  Query + Response + Context ──────┐       │     │
│  │                                    │       │     │
│  │                                    ▼       │     │
│  │     ┌──────────────────────────────────┐  │     │
│  │     │   Parallel Judge Evaluation      │  │     │
│  │     │                                  │  │     │
│  │     │  ┌──────────┐  ┌──────────┐    │  │     │
│  │     │  │  GPT-4o  │  │  Claude  │    │  │     │
│  │     │  │  Judge   │  │  Judge   │    │  │     │
│  │     │  └────┬─────┘  └────┬─────┘    │  │     │
│  │     │       │             │           │  │     │
│  │     │       │  ┌──────────┐           │  │     │
│  │     │       └──│  Gemini  │           │  │     │
│  │     │          │  Judge   │           │  │     │
│  │     │          └────┬─────┘           │  │     │
│  │     └───────────────┼──────────────────┘  │     │
│  │                     ▼                     │     │
│  │     ┌──────────────────────────────────┐  │     │
│  │     │   Aggregate Results              │  │     │
│  │     │                                  │  │     │
│  │     │   • Mean Score                   │  │     │
│  │     │   • Median Score                 │  │     │
│  │     │   • Consensus Level (0-1)        │  │     │
│  │     │   • Combined Issues/Strengths    │  │     │
│  │     └──────────────────────────────────┘  │     │
│  └────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘
```

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `multi_judge.py` | Multi-judge evaluation system | ~373 |
| `example_usage.py` | Usage examples and demos | ~139 |
| `evaluation.py` | Batch evaluation utilities | ~109 |

---

## JudgeModel Options

The module supports three judge models via OpenRouter:

| Model | Enum Value | Description |
|-------|------------|-------------|
| **GPT-4o** | `JudgeModel.GPT4O` | OpenAI's GPT-4o (strong reasoning) |
| **Claude** | `JudgeModel.CLAUDE` | Anthropic Claude 3 Sonnet (balanced) |
| **Gemini** | `JudgeModel.GEMINI` | Google Gemini 2.0 Flash (fast, efficient) |

```python
from src.evaluation.multi_judge import JudgeModel

# Available judges
all_judges = [
    JudgeModel.GPT4O,    # "openai/gpt-4o"
    JudgeModel.CLAUDE,   # "anthropic/claude-3-sonnet"
    JudgeModel.GEMINI    # "google/gemini-2.0-flash"
]
```

---

## MultiJudgeEvaluator Class

**File**: `src/evaluation/multi_judge.py`

### Initialization

```python
from src.evaluation.multi_judge import MultiJudgeEvaluator, JudgeModel

# Option 1: Use all available judges (default)
evaluator = MultiJudgeEvaluator()

# Option 2: Use specific judges only
evaluator = MultiJudgeEvaluator(
    judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE]
)

# Option 3: Provide API key explicitly
evaluator = MultiJudgeEvaluator(
    api_key="your-openrouter-api-key"
)

# Otherwise, uses OPENROUTER_API_KEY environment variable
```

### Core Method: `evaluate_response()`

```python
async def evaluate_response(
    self,
    query: str,
    response: str,
    context: str
) -> AggregatedEvaluation:
    """
    Evaluate a response using multiple judge models.

    Args:
        query: The original user query
        response: The AI-generated response to evaluate
        context: The context or documents used to generate the response

    Returns:
        AggregatedEvaluation with scores and feedback from all judges
    """
```

### Basic Usage Example

```python
import asyncio
from src.evaluation.multi_judge import MultiJudgeEvaluator

async def evaluate_example():
    # Initialize evaluator
    evaluator = MultiJudgeEvaluator()

    # Define evaluation inputs
    query = "What is the best interests test in Australian family law?"

    context = """
    The Family Law Act 1975 s60CC sets out the best interests test
    for parenting matters. Primary considerations include the benefit
    of a meaningful relationship with both parents and protection
    from harm. Additional considerations cover 14 specific factors.
    """

    response = """
    The best interests test under s60CC of the Family Law Act 1975
    is the paramount consideration in parenting matters. It includes
    two primary considerations: the benefit of the child having a
    meaningful relationship with both parents, and the need to protect
    the child from harm. The court also considers 14 additional factors.
    """

    # Evaluate
    result = await evaluator.evaluate_response(
        query=query,
        response=response,
        context=context
    )

    # Display results
    print(f"Mean Score: {result.mean_score:.2f}/10")
    print(f"Median Score: {result.median_score:.2f}/10")
    print(f"Consensus: {result.consensus_level:.2%}")

    print(f"\nJudge Scores:")
    for eval in result.individual_evaluations:
        print(f"  {eval.model.name}: {eval.score:.2f}/10")

# Run
asyncio.run(evaluate_example())
```

---

## Data Structures

### JudgeEvaluation

```python
@dataclass
class JudgeEvaluation:
    """Evaluation from a single judge model."""
    model: JudgeModel           # Which judge provided this
    score: float                # 1-10 scale
    issues: List[str]          # Identified problems
    strengths: List[str]       # Positive aspects
    reasoning: str             # Judge's explanation
```

### AggregatedEvaluation

```python
@dataclass
class AggregatedEvaluation:
    """Aggregated evaluation from multiple judges."""
    mean_score: float                           # Average score
    median_score: float                         # Median score
    consensus_level: float                      # 0-1 (agreement level)
    individual_evaluations: List[JudgeEvaluation]  # All judge evals
    combined_issues: List[str]                  # All issues found
    combined_strengths: List[str]               # All strengths found
```

---

## Consensus Calculation

The consensus level measures how much judges agree (0.0 to 1.0):

```python
def _calculate_consensus(evaluations: List[JudgeEvaluation]) -> float:
    """
    Calculate consensus based on standard deviation of scores.

    Formula:
        std_dev = standard_deviation(scores)
        consensus = 1.0 - (std_dev / 3.0)
        consensus = clamp(consensus, 0.0, 1.0)

    Interpretation:
        1.0: Perfect agreement (all judges gave same score)
        0.8+: Strong consensus
        0.6-0.8: Moderate consensus
        0.4-0.6: Weak consensus
        <0.4: Disagreement
    """
```

### Example Consensus Scenarios

```python
# Scenario 1: Perfect Consensus
# Judges: [8.5, 8.5, 8.5]
# Std Dev: 0.0
# Consensus: 1.0 (100%)

# Scenario 2: Strong Consensus
# Judges: [8.0, 8.5, 9.0]
# Std Dev: 0.5
# Consensus: 0.83 (83%)

# Scenario 3: Moderate Consensus
# Judges: [7.0, 8.5, 9.5]
# Std Dev: 1.25
# Consensus: 0.58 (58%)

# Scenario 4: Disagreement
# Judges: [4.0, 7.0, 9.5]
# Std Dev: 2.8
# Consensus: 0.07 (7%)
```

---

## Async Usage Examples

### Single Evaluation

```python
import asyncio
from src.evaluation.multi_judge import MultiJudgeEvaluator

async def single_evaluation():
    evaluator = MultiJudgeEvaluator()

    result = await evaluator.evaluate_response(
        query="Explain property settlement",
        response="Property is divided under s79...",
        context="Family Law Act provisions..."
    )

    print(f"Score: {result.mean_score:.2f}/10")
    return result

# Run
result = asyncio.run(single_evaluation())
```

### Batch Evaluation

```python
import asyncio
from src.evaluation.multi_judge import MultiJudgeEvaluator

async def batch_evaluation():
    evaluator = MultiJudgeEvaluator()

    # Multiple queries to evaluate
    test_cases = [
        {
            "query": "What is property settlement?",
            "response": "Property settlement is...",
            "context": "FLA s79..."
        },
        {
            "query": "How is child custody determined?",
            "response": "Custody is determined by...",
            "context": "FLA s60CC..."
        },
        # ... more cases
    ]

    # Evaluate all concurrently
    tasks = [
        evaluator.evaluate_response(
            query=case["query"],
            response=case["response"],
            context=case["context"]
        )
        for case in test_cases
    ]

    results = await asyncio.gather(*tasks)

    # Aggregate metrics
    mean_scores = [r.mean_score for r in results]
    avg_score = sum(mean_scores) / len(mean_scores)

    print(f"Average score across {len(results)} cases: {avg_score:.2f}/10")
    return results

# Run
results = asyncio.run(batch_evaluation())
```

### With Custom Judges

```python
import asyncio
from src.evaluation.multi_judge import MultiJudgeEvaluator, JudgeModel

async def custom_judges_evaluation():
    # Use only GPT-4o and Claude (skip Gemini)
    evaluator = MultiJudgeEvaluator(
        judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE]
    )

    result = await evaluator.evaluate_response(
        query="What is the four-step process?",
        response="The four-step process involves...",
        context="Stanford v Stanford (2012)..."
    )

    print(f"Judges used: {[e.model.name for e in result.individual_evaluations]}")
    print(f"Consensus: {result.consensus_level:.2%}")

    return result

# Run
result = asyncio.run(custom_judges_evaluation())
```

---

## Evaluation Criteria

Each judge evaluates responses on 5 criteria:

### 1. Accuracy (Factual Correctness)

```
✅ Is the response factually correct based on context?
✅ Are legal citations accurate?
✅ Are numbers and dates correct?
```

### 2. Completeness (Addresses Query)

```
✅ Does it fully address the user's question?
✅ Are all aspects covered?
✅ Is important information missing?
```

### 3. Relevance (On Topic)

```
✅ Is the information relevant to the question?
✅ Does it stay focused on the query?
✅ Is there unnecessary information?
```

### 4. Clarity (Well-Structured)

```
✅ Is the response clear and easy to understand?
✅ Is it well-organized?
✅ Is the language appropriate?
```

### 5. Context Usage (Proper Citations)

```
✅ Does it properly use the provided context?
✅ Are sources cited appropriately?
✅ Is context being ignored or misused?
```

---

## Scoring Guide

| Score | Rating | Description |
|-------|--------|-------------|
| 9-10 | Excellent | Accurate, complete, highly relevant, well-structured |
| 7-8 | Good | Mostly accurate with only minor issues |
| 5-6 | Adequate | Acceptable but has notable gaps or errors |
| 3-4 | Poor | Significant issues or inaccuracies |
| 1-2 | Very Poor | Mostly incorrect or irrelevant |

---

## Complete Example with Error Handling

```python
"""Production-ready evaluation with error handling."""
import asyncio
import os
from typing import List, Dict, Any
from src.evaluation.multi_judge import (
    MultiJudgeEvaluator,
    JudgeModel,
    AggregatedEvaluation
)

async def evaluate_with_retry(
    evaluator: MultiJudgeEvaluator,
    query: str,
    response: str,
    context: str,
    max_retries: int = 3
) -> AggregatedEvaluation:
    """Evaluate with retry logic."""
    for attempt in range(max_retries):
        try:
            result = await evaluator.evaluate_response(
                query=query,
                response=response,
                context=context
            )
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
            print(f"Attempt {attempt + 1} failed, retrying...")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

async def main():
    # Check API key
    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY not set")

    # Initialize
    evaluator = MultiJudgeEvaluator(
        judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE, JudgeModel.GEMINI]
    )

    # Test cases
    test_cases = [
        {
            "id": "test_001",
            "query": "What are the s60CC factors?",
            "response": "Section 60CC outlines 16 factors...",
            "context": "Family Law Act 1975 s60CC..."
        },
        {
            "id": "test_002",
            "query": "How is property divided?",
            "response": "Property division follows a 4-step process...",
            "context": "Stanford v Stanford (2012)..."
        }
    ]

    # Evaluate all cases
    print(f"Evaluating {len(test_cases)} test cases...")
    results: List[AggregatedEvaluation] = []

    for case in test_cases:
        print(f"\n{'='*60}")
        print(f"Evaluating: {case['id']}")
        print(f"Query: {case['query']}")

        try:
            result = await evaluate_with_retry(
                evaluator=evaluator,
                query=case["query"],
                response=case["response"],
                context=case["context"]
            )

            results.append(result)

            # Display results
            print(f"\nResults:")
            print(f"  Mean Score: {result.mean_score:.2f}/10")
            print(f"  Median Score: {result.median_score:.2f}/10")
            print(f"  Consensus: {result.consensus_level:.2%}")

            print(f"\n  Individual Scores:")
            for eval in result.individual_evaluations:
                print(f"    {eval.model.name:12} {eval.score:.2f}/10")

            if result.combined_issues:
                print(f"\n  Issues ({len(result.combined_issues)}):")
                for issue in result.combined_issues[:3]:  # Show top 3
                    print(f"    • {issue}")

        except Exception as e:
            print(f"  ❌ Evaluation failed: {e}")

    # Summary statistics
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")

    if results:
        avg_mean = sum(r.mean_score for r in results) / len(results)
        avg_consensus = sum(r.consensus_level for r in results) / len(results)

        print(f"Average Mean Score: {avg_mean:.2f}/10")
        print(f"Average Consensus: {avg_consensus:.2%}")
        print(f"Total Evaluations: {len(results)}")
        print(f"Success Rate: {len(results)}/{len(test_cases)} ({len(results)/len(test_cases):.1%})")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Integration with Testing Pipeline

### Pytest Example

```python
"""Test suite using multi-judge evaluation."""
import pytest
import asyncio
from src.evaluation.multi_judge import MultiJudgeEvaluator

@pytest.fixture
def evaluator():
    """Fixture providing evaluator instance."""
    return MultiJudgeEvaluator()

@pytest.mark.asyncio
async def test_response_quality(evaluator):
    """Test that responses meet minimum quality threshold."""
    result = await evaluator.evaluate_response(
        query="What is s60CC?",
        response="Section 60CC sets out the best interests test...",
        context="Family Law Act 1975..."
    )

    # Assert quality thresholds
    assert result.mean_score >= 7.0, "Response quality below threshold"
    assert result.consensus_level >= 0.6, "Low judge consensus"
    assert len(result.combined_issues) <= 2, "Too many issues identified"

@pytest.mark.asyncio
async def test_factual_accuracy(evaluator):
    """Test factual accuracy detection."""
    # Intentionally incorrect response
    result = await evaluator.evaluate_response(
        query="How many s60CC factors are there?",
        response="There are 20 factors in s60CC.",  # Wrong - there are 16
        context="Section 60CC lists 16 factors..."
    )

    # Should detect the error
    assert result.mean_score < 7.0, "Failed to detect factual error"
```

---

## Performance Considerations

### API Rate Limits

```python
# Batch with rate limiting
import asyncio
from asyncio import Semaphore

async def evaluate_with_rate_limit(
    evaluator: MultiJudgeEvaluator,
    test_cases: List[Dict],
    max_concurrent: int = 5
):
    """Evaluate with concurrency limit to respect rate limits."""
    semaphore = Semaphore(max_concurrent)

    async def eval_one(case):
        async with semaphore:
            return await evaluator.evaluate_response(
                query=case["query"],
                response=case["response"],
                context=case["context"]
            )

    tasks = [eval_one(case) for case in test_cases]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### Cost Estimation

```python
# Approximate token usage per evaluation:
# - Prompt: ~500-1000 tokens (query + response + context + instructions)
# - Response: ~300-500 tokens per judge

# Example:
# 3 judges × 800 tokens per judge = 2,400 tokens/evaluation
# At $0.50 per 1M tokens = $0.0012/evaluation
```

---

## Related Pages

- [Backend-Benchmarks-Module](Backend-Benchmarks-Module) - Benchmark evaluation
- [Backend-Validation-Module](Backend-Validation-Module) - Statutory validation
- [Backend-GSW-Module](Backend-GSW-Module) - Legal operator extraction
- [Backend-Span-Detector](Backend-Span-Detector) - Span-level detection
