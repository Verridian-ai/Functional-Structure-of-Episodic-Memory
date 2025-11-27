"""
Evaluation Module for Verridian AI

This module provides evaluation tools for assessing the quality of AI-generated
responses using multiple judge models.

Components:
-----------
- JudgeModel: Enum of available judge models
- JudgeEvaluation: Single judge evaluation result
- AggregatedEvaluation: Combined evaluation from multiple judges
- MultiJudgeEvaluator: Main evaluator class that coordinates multiple judges

Example Usage:
-------------
```python
import asyncio
from src.evaluation import MultiJudgeEvaluator, JudgeModel

async def evaluate_response():
    # Initialize evaluator with specific judges
    evaluator = MultiJudgeEvaluator(
        judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE]
    )

    # Evaluate a response
    result = await evaluator.evaluate_response(
        query="What are the key provisions of the Family Law Act?",
        response="The Family Law Act 1975 establishes...",
        context="[Legal document context...]"
    )

    print(f"Mean Score: {result.mean_score}")
    print(f"Consensus: {result.consensus_level}")
    print(f"Issues: {result.combined_issues}")

asyncio.run(evaluate_response())
```
"""

from .multi_judge import (
    JudgeModel,
    JudgeEvaluation,
    AggregatedEvaluation,
    MultiJudgeEvaluator,
)

__all__ = [
    "JudgeModel",
    "JudgeEvaluation",
    "AggregatedEvaluation",
    "MultiJudgeEvaluator",
]

__version__ = "0.1.0"
