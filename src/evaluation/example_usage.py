"""
Example usage of the Multi-Judge Evaluation module.

This script demonstrates how to use the MultiJudgeEvaluator to evaluate
AI-generated responses using multiple judge models.

Requirements:
- httpx: pip install httpx
- OPENROUTER_API_KEY environment variable must be set
"""

import asyncio
import os
from multi_judge import (
    JudgeModel,
    JudgeEvaluation,
    AggregatedEvaluation,
    MultiJudgeEvaluator,
)


async def example_evaluation():
    """Example of evaluating an AI response with multiple judges."""

    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set it with: export OPENROUTER_API_KEY='your-key-here'")
        return

    # Sample data
    query = "What are the main provisions of the Australian Family Law Act regarding property division?"

    context = """
    The Family Law Act 1975 (Cth) establishes the framework for property division
    following marriage breakdown in Australia. Key provisions include:
    - Section 79: Court's power to alter property interests
    - Section 75(2): Factors to be considered in property settlements
    - The four-step process established in case law
    """

    response = """
    The Australian Family Law Act provides a comprehensive framework for property
    division after marriage breakdown. Under Section 79, the court has power to
    alter the property interests of parties to a marriage. The court considers
    factors outlined in Section 75(2), including the financial contributions of
    each party, non-financial contributions, and future needs. The process follows
    a well-established four-step approach for determining fair property division.
    """

    # Initialize evaluator with all judges
    print("Initializing Multi-Judge Evaluator...")
    evaluator = MultiJudgeEvaluator()

    # Or initialize with specific judges:
    # evaluator = MultiJudgeEvaluator(
    #     judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE]
    # )

    print(f"Using judges: {[j.name for j in evaluator.judges]}")
    print("\nEvaluating response...\n")

    # Evaluate the response
    try:
        result = await evaluator.evaluate_response(
            query=query,
            response=response,
            context=context
        )

        # Display results
        print("=" * 60)
        print("EVALUATION RESULTS")
        print("=" * 60)
        print(f"\nOverall Scores:")
        print(f"  Mean Score:      {result.mean_score:.2f}/10")
        print(f"  Median Score:    {result.median_score:.2f}/10")
        print(f"  Consensus Level: {result.consensus_level:.2%}")

        print(f"\nIndividual Judge Scores:")
        for eval in result.individual_evaluations:
            print(f"  {eval.model.name:12} {eval.score:.2f}/10")

        if result.combined_strengths:
            print(f"\nStrengths ({len(result.combined_strengths)}):")
            for strength in result.combined_strengths:
                print(f"  • {strength}")

        if result.combined_issues:
            print(f"\nIssues ({len(result.combined_issues)}):")
            for issue in result.combined_issues:
                print(f"  • {issue}")

        print("\nDetailed Reasoning:")
        for eval in result.individual_evaluations:
            print(f"\n{eval.model.name}:")
            print(f"  {eval.reasoning}")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()


async def example_custom_evaluation():
    """Example using only specific judges."""

    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set")
        return

    # Use only GPT-4o and Claude
    evaluator = MultiJudgeEvaluator(
        judges=[JudgeModel.GPT4O, JudgeModel.CLAUDE]
    )

    query = "Explain the concept of constructive trust in property law."
    context = "Constructive trust is an equitable remedy..."
    response = "A constructive trust arises when..."

    result = await evaluator.evaluate_response(query, response, context)

    print(f"Evaluation complete: {result.mean_score:.2f}/10")
    print(f"Judges used: {[e.model.name for e in result.individual_evaluations]}")


if __name__ == "__main__":
    print("Multi-Judge Evaluation Example\n")

    # Run the main example
    asyncio.run(example_evaluation())

    # Uncomment to run the custom evaluation example:
    # print("\n" + "=" * 60)
    # print("Custom Evaluation Example\n")
    # asyncio.run(example_custom_evaluation())
