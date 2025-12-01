"""
Cost Tracker for GSW Pipeline
==============================

Tracks token usage and costs for OpenRouter API calls.

Pricing (Gemini 2.5 Flash):
- Input: $0.30 per 1M tokens
- Output: $2.50 per 1M tokens
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime
import json


# Model pricing per 1M tokens
MODEL_PRICING = {
    "google/gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "google/gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "google/gemini-2.0-flash-exp:free": {"input": 0.00, "output": 0.00},
    "deepseek/deepseek-r1-distill-llama-70b:free": {"input": 0.00, "output": 0.00},
    "meta-llama/llama-3.3-70b-instruct:free": {"input": 0.00, "output": 0.00},
    "mistralai/mistral-7b-instruct:free": {"input": 0.00, "output": 0.00},
    "microsoft/phi-3-medium-128k-instruct:free": {"input": 0.00, "output": 0.00},
    "huggingfaceh4/zephyr-7b-beta:free": {"input": 0.00, "output": 0.00},
    "deepseek/deepseek-r1-0528:free": {"input": 0.00, "output": 0.00},
    "moonshotai/kimi-k2:free": {"input": 0.00, "output": 0.00},
    "moonshotai/kimi-k2": {"input": 0.456, "output": 1.84},
}


@dataclass
class CostTracker:
    """Tracks token usage and costs across the pipeline."""

    model: str = "google/gemini-2.5-flash"
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_requests: int = 0

    # Per-component tracking
    operator_input: int = 0
    operator_output: int = 0
    reconciler_input: int = 0
    reconciler_output: int = 0
    spacetime_input: int = 0
    spacetime_output: int = 0
    summary_input: int = 0
    summary_output: int = 0

    start_time: Optional[datetime] = None

    def __post_init__(self):
        self.start_time = datetime.now()

    def add_usage(self, component: str, input_tokens: int, output_tokens: int):
        """Add token usage from an API call."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_requests += 1

        if component == "operator":
            self.operator_input += input_tokens
            self.operator_output += output_tokens
        elif component == "reconciler":
            self.reconciler_input += input_tokens
            self.reconciler_output += output_tokens
        elif component == "spacetime":
            self.spacetime_input += input_tokens
            self.spacetime_output += output_tokens
        elif component == "summary":
            self.summary_input += input_tokens
            self.summary_output += output_tokens

    def get_pricing(self) -> Dict[str, float]:
        """Get pricing for current model."""
        return MODEL_PRICING.get(self.model, {"input": 0.30, "output": 2.50})

    @property
    def input_cost(self) -> float:
        """Calculate input token cost in dollars."""
        pricing = self.get_pricing()
        return (self.total_input_tokens / 1_000_000) * pricing["input"]

    @property
    def output_cost(self) -> float:
        """Calculate output token cost in dollars."""
        pricing = self.get_pricing()
        return (self.total_output_tokens / 1_000_000) * pricing["output"]

    @property
    def total_cost(self) -> float:
        """Calculate total cost in dollars."""
        return self.input_cost + self.output_cost

    def get_summary(self) -> str:
        """Get a formatted summary string."""
        pricing = self.get_pricing()
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0

        return f"""
================================================================================
                           GSW PIPELINE COST REPORT
================================================================================
Model: {self.model}
Pricing: ${pricing['input']:.2f}/1M input, ${pricing['output']:.2f}/1M output

TOKEN USAGE:
  Total Requests:    {self.total_requests:,}
  Input Tokens:      {self.total_input_tokens:,}
  Output Tokens:     {self.total_output_tokens:,}
  Total Tokens:      {self.total_input_tokens + self.total_output_tokens:,}

COST BREAKDOWN:
  Input Cost:        ${self.input_cost:.4f}
  Output Cost:       ${self.output_cost:.4f}
  -----------------------------
  TOTAL COST:        ${self.total_cost:.4f}

PER-COMPONENT USAGE:
  Operator:          {self.operator_input:,} in / {self.operator_output:,} out
  Reconciler:        {self.reconciler_input:,} in / {self.reconciler_output:,} out
  Spacetime:         {self.spacetime_input:,} in / {self.spacetime_output:,} out
  Summary:           {self.summary_input:,} in / {self.summary_output:,} out

PERFORMANCE:
  Elapsed Time:      {elapsed:.1f}s
  Tokens/Second:     {(self.total_input_tokens + self.total_output_tokens) / max(elapsed, 1):.1f}
================================================================================
"""

    def print_progress(self, docs_processed: int, total_docs: int = 0):
        """Print a progress line with current costs."""
        pct = f" ({100*docs_processed/total_docs:.1f}%)" if total_docs > 0 else ""
        print(f"  Docs: {docs_processed}{pct} | "
              f"Tokens: {self.total_input_tokens + self.total_output_tokens:,} | "
              f"Cost: ${self.total_cost:.4f}", end='\r')

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "model": self.model,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_requests": self.total_requests,
            "input_cost": self.input_cost,
            "output_cost": self.output_cost,
            "total_cost": self.total_cost,
            "components": {
                "operator": {"input": self.operator_input, "output": self.operator_output},
                "reconciler": {"input": self.reconciler_input, "output": self.reconciler_output},
                "spacetime": {"input": self.spacetime_input, "output": self.spacetime_output},
                "summary": {"input": self.summary_input, "output": self.summary_output},
            }
        }

    def save(self, filepath: str):
        """Save cost report to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


# Global instance for easy access
_cost_tracker: Optional[CostTracker] = None


def get_cost_tracker(model: str = "google/gemini-2.5-flash") -> CostTracker:
    """Get or create the global cost tracker."""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker(model=model)
    return _cost_tracker


def reset_cost_tracker(model: str = "google/gemini-2.5-flash") -> CostTracker:
    """Reset and return a new cost tracker."""
    global _cost_tracker
    _cost_tracker = CostTracker(model=model)
    return _cost_tracker
