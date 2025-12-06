"""
Pipeline Package - End-to-End Corpus Processing Orchestration

This package provides the unified pipeline orchestration system that runs
the entire corpus processing pipeline from raw documents to query-ready system.

Components:
- config.py: Pipeline configuration with checkpointing
- orchestrator.py: Main pipeline orchestrator with stage execution
- run_full_pipeline.py: CLI script for pipeline execution
"""

from .config import PipelineConfig, PipelineStage
from .orchestrator import FullPipeline, PipelineState

__all__ = [
    "PipelineConfig",
    "PipelineStage",
    "FullPipeline",
    "PipelineState",
]
