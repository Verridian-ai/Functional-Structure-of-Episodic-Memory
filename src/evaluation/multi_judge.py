"""
Multi-Judge Evaluation Module for Verridian AI

This module provides a multi-judge evaluation system that uses multiple LLMs
to evaluate responses for quality, accuracy, and appropriateness. It aggregates
scores from different models to provide a robust evaluation.

Uses OpenRouter API for accessing multiple models.
"""

import os
import asyncio
import statistics
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json
import httpx


class JudgeModel(Enum):
    """Available judge models via OpenRouter."""
    GPT4O = "openai/gpt-4o"
    CLAUDE = "anthropic/claude-3-sonnet"
    GEMINI = "google/gemini-2.0-flash"


@dataclass
class JudgeEvaluation:
    """Evaluation from a single judge model."""
    model: JudgeModel
    score: float  # 1-10 scale
    issues: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class AggregatedEvaluation:
    """Aggregated evaluation from multiple judges."""
    mean_score: float
    median_score: float
    consensus_level: float  # 0-1, how much judges agree
    individual_evaluations: List[JudgeEvaluation] = field(default_factory=list)
    combined_issues: List[str] = field(default_factory=list)
    combined_strengths: List[str] = field(default_factory=list)


class MultiJudgeEvaluator:
    """
    Multi-judge evaluation system that uses multiple LLMs to evaluate responses.

    This class coordinates multiple judge models to provide robust evaluation of
    AI-generated responses. It aggregates scores and feedback from different models
    to reduce bias and improve evaluation quality.
    """

    def __init__(
        self,
        judges: Optional[List[JudgeModel]] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Multi-Judge Evaluator.

        Args:
            judges: List of judge models to use. If None, uses all available judges.
            api_key: OpenRouter API key. If None, uses OPENROUTER_API_KEY env var.

        Raises:
            ValueError: If no API key is found.
        """
        # Default to using all judges if none specified
        if judges is None:
            self.judges = [
                JudgeModel.GPT4O,
                JudgeModel.CLAUDE,
                JudgeModel.GEMINI
            ]
        else:
            self.judges = judges

        # Get API key
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key found. Set OPENROUTER_API_KEY environment variable "
                "or pass api_key parameter."
            )

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
        # Gather evaluations from all judges concurrently
        tasks = [
            self._get_judge_evaluation(judge, query, response, context)
            for judge in self.judges
        ]
        evaluations = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any failed evaluations
        valid_evaluations = [
            eval for eval in evaluations
            if isinstance(eval, JudgeEvaluation)
        ]

        if not valid_evaluations:
            # Return a default evaluation if all judges failed
            return AggregatedEvaluation(
                mean_score=0.0,
                median_score=0.0,
                consensus_level=0.0,
                individual_evaluations=[],
                combined_issues=["All judge evaluations failed"],
                combined_strengths=[]
            )

        # Aggregate the evaluations
        return self._aggregate_evaluations(valid_evaluations)

    async def _get_judge_evaluation(
        self,
        judge: JudgeModel,
        query: str,
        response: str,
        context: str
    ) -> JudgeEvaluation:
        """
        Get evaluation from a single judge model.

        Args:
            judge: The judge model to use
            query: The original user query
            response: The AI-generated response to evaluate
            context: The context used to generate the response

        Returns:
            JudgeEvaluation from this judge

        Raises:
            Exception: If the API call fails or response cannot be parsed
        """
        # Build the evaluation prompt
        prompt = self._build_evaluation_prompt(query, response, context)

        # Call the judge model via OpenRouter
        async with httpx.AsyncClient(
            base_url="https://openrouter.ai/api/v1",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        ) as client:
            response_data = await client.post(
                "/chat/completions",
                json={
                    "model": judge.value,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are an expert evaluator of AI responses. "
                                "Provide detailed, objective evaluations in JSON format."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            )
            response_data.raise_for_status()
            result = response_data.json()

        # Parse the response
        content = result["choices"][0]["message"]["content"]

        # Clean markdown code blocks if present
        cleaned_content = content.strip()
        if cleaned_content.startswith("```"):
            # Remove opening ```json or ```
            cleaned_content = cleaned_content.split('\n', 1)[1]
            # Remove closing ```
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content.rsplit('\n', 1)[0]

        try:
            eval_data = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            import re
            match = re.search(r'\{[\s\S]*\}', cleaned_content)
            if match:
                eval_data = json.loads(match.group())
            else:
                raise ValueError(f"Could not parse JSON from {judge.value} response")

        # Build JudgeEvaluation object
        return JudgeEvaluation(
            model=judge,
            score=float(eval_data.get("score", 5.0)),
            issues=eval_data.get("issues", []),
            strengths=eval_data.get("strengths", []),
            reasoning=eval_data.get("reasoning", "")
        )

    def _aggregate_evaluations(
        self,
        evaluations: List[JudgeEvaluation]
    ) -> AggregatedEvaluation:
        """
        Aggregate evaluations from multiple judges.

        Args:
            evaluations: List of individual judge evaluations

        Returns:
            AggregatedEvaluation combining all judge feedback
        """
        if not evaluations:
            return AggregatedEvaluation(
                mean_score=0.0,
                median_score=0.0,
                consensus_level=0.0
            )

        # Calculate score statistics
        scores = [eval.score for eval in evaluations]
        mean_score = statistics.mean(scores)
        median_score = statistics.median(scores)

        # Calculate consensus level
        consensus_level = self._calculate_consensus(evaluations)

        # Combine issues and strengths from all judges
        all_issues = []
        all_strengths = []

        for eval in evaluations:
            # Add issues with judge identifier
            for issue in eval.issues:
                all_issues.append(f"[{eval.model.name}] {issue}")

            # Add strengths with judge identifier
            for strength in eval.strengths:
                all_strengths.append(f"[{eval.model.name}] {strength}")

        return AggregatedEvaluation(
            mean_score=mean_score,
            median_score=median_score,
            consensus_level=consensus_level,
            individual_evaluations=evaluations,
            combined_issues=all_issues,
            combined_strengths=all_strengths
        )

    def _calculate_consensus(
        self,
        evaluations: List[JudgeEvaluation]
    ) -> float:
        """
        Calculate consensus level among judges (0-1 scale).

        Consensus is based on the standard deviation of scores.
        Lower deviation = higher consensus.

        Args:
            evaluations: List of judge evaluations

        Returns:
            Consensus level between 0 (no consensus) and 1 (perfect consensus)
        """
        if len(evaluations) <= 1:
            return 1.0

        scores = [eval.score for eval in evaluations]

        # Calculate standard deviation
        try:
            std_dev = statistics.stdev(scores)
        except statistics.StatisticsError:
            # All scores are identical
            return 1.0

        # Convert std_dev to consensus score
        # Max reasonable std_dev is about 3 (on a 1-10 scale)
        # Consensus = 1 - (std_dev / 3), clamped to [0, 1]
        consensus = max(0.0, min(1.0, 1.0 - (std_dev / 3.0)))

        return consensus

    def _build_evaluation_prompt(
        self,
        query: str,
        response: str,
        context: str
    ) -> str:
        """
        Build the evaluation prompt for judge models.

        Args:
            query: The original user query
            response: The AI-generated response to evaluate
            context: The context used to generate the response

        Returns:
            Formatted evaluation prompt
        """
        prompt = f"""
Evaluate the following AI-generated response for quality, accuracy, and appropriateness.

**USER QUERY:**
{query}

**CONTEXT PROVIDED:**
{context[:2000]}{"..." if len(context) > 2000 else ""}

**AI RESPONSE:**
{response}

**EVALUATION CRITERIA:**
1. **Accuracy**: Is the response factually correct based on the context?
2. **Completeness**: Does it fully address the user's query?
3. **Relevance**: Is the information relevant to the question?
4. **Clarity**: Is the response clear and well-structured?
5. **Context Usage**: Does it properly use the provided context?

**RESPONSE FORMAT:**
Provide your evaluation as a JSON object with the following structure:
{{
    "score": <float between 1-10>,
    "issues": [<list of specific problems or concerns>],
    "strengths": [<list of positive aspects>],
    "reasoning": "<brief explanation of your score>"
}}

**SCORING GUIDE:**
- 9-10: Excellent - Accurate, complete, highly relevant
- 7-8: Good - Mostly accurate with minor issues
- 5-6: Adequate - Acceptable but has notable gaps
- 3-4: Poor - Significant issues or inaccuracies
- 1-2: Very Poor - Mostly incorrect or irrelevant

Provide your evaluation now:
"""
        return prompt


__all__ = [
    "JudgeModel",
    "JudgeEvaluation",
    "AggregatedEvaluation",
    "MultiJudgeEvaluator",
]
