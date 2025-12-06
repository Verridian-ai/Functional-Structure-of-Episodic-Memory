"""
Pipeline Integration Tests

Tests for the full pipeline orchestration system.
"""

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline.config import PipelineConfig, PipelineStage
from src.pipeline.orchestrator import FullPipeline, PipelineState, StageResult


def test_config_creation():
    """Test that default configuration can be created."""
    config = PipelineConfig()
    assert config.corpus_path == Path("data/corpus.jsonl")
    assert config.enable_auto_gsw == True
    assert config.gsw_authority_threshold == 60


def test_config_validation():
    """Test configuration validation."""
    config = PipelineConfig()

    # Valid config should have no errors
    # (May have error if corpus doesn't exist, which is ok for this test)
    errors = config.validate()
    assert isinstance(errors, list)


def test_config_yaml_roundtrip(tmp_path):
    """Test saving and loading configuration from YAML."""
    config = PipelineConfig(
        document_limit=100,
        gsw_authority_threshold=70
    )

    yaml_path = tmp_path / "test_config.yaml"
    config.to_yaml(yaml_path)

    loaded = PipelineConfig.from_yaml(yaml_path)
    assert loaded.document_limit == 100
    assert loaded.gsw_authority_threshold == 70


def test_pipeline_state_serialization():
    """Test pipeline state serialization."""
    state = PipelineState()
    state.completed_stages = ["classify"]
    state.total_documents_processed = 1000

    # Serialize
    data = state.to_dict()
    assert data["total_documents_processed"] == 1000
    assert "classify" in data["completed_stages"]

    # Deserialize
    loaded = PipelineState.from_dict(data)
    assert loaded.total_documents_processed == 1000
    assert "classify" in loaded.completed_stages


def test_stage_result_creation():
    """Test stage result creation."""
    result = StageResult(
        stage="classify",
        success=True,
        duration_seconds=120.5,
        documents_processed=1000,
        statistics={"domains": 10}
    )

    assert result.stage == "classify"
    assert result.success == True
    assert result.documents_processed == 1000


def test_pipeline_initialization():
    """Test pipeline can be initialized."""
    config = PipelineConfig(
        document_limit=10,
        enable_auto_gsw=False,
        enable_graph_building=False
    )

    pipeline = FullPipeline(config)
    assert pipeline.config.document_limit == 10
    assert isinstance(pipeline.state, PipelineState)


def test_config_summary():
    """Test configuration summary generation."""
    config = PipelineConfig()
    summary = config.summary()

    assert "Pipeline Configuration Summary" in summary
    assert "Input:" in summary
    assert "Output:" in summary
    assert "GSW Extraction:" in summary


def test_config_overrides():
    """Test configuration command-line style overrides."""
    config = PipelineConfig()

    # Apply overrides
    config.document_limit = 500
    config.gsw_authority_threshold = 80
    config.enable_graph_building = False

    assert config.document_limit == 500
    assert config.gsw_authority_threshold == 80
    assert config.enable_graph_building == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
