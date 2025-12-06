"""
Pipeline Configuration - Settings for Full Corpus Processing

This module defines the configuration for the complete pipeline orchestration.
It supports YAML-based configuration files and command-line overrides.

Configuration includes:
- Input/output paths
- Classification settings
- GSW extraction settings
- Graph building options
- Processing limits and checkpointing
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class PipelineStage(str, Enum):
    """Available pipeline stages."""
    CLASSIFY = "classify"
    GSW = "gsw"
    GRAPH = "graph"
    INDEX = "index"


@dataclass
class PipelineConfig:
    """Configuration for full corpus processing pipeline."""

    # ========================================================================
    # INPUT/OUTPUT PATHS
    # ========================================================================

    corpus_path: Path = Path("data/corpus.jsonl")
    output_dir: Path = Path("data/processed")
    workspace_dir: Path = Path("data/workspaces")
    graph_dir: Path = Path("data/processed/graph")
    checkpoint_dir: Path = Path("data/checkpoints")

    # ========================================================================
    # CLASSIFICATION SETTINGS
    # ========================================================================

    classification_batch_size: int = 100
    classification_progress_interval: int = 5000
    classification_resume: bool = True

    # ========================================================================
    # GSW EXTRACTION SETTINGS
    # ========================================================================

    enable_auto_gsw: bool = True
    gsw_authority_threshold: int = 60  # Only process high-authority cases
    gsw_batch_size: int = 10
    gsw_model: str = "google/gemini-2.5-flash"
    gsw_fallback_models: List[str] = field(default_factory=lambda: [
        "google/gemini-2.5-flash",
        "deepseek/deepseek-chat",
        "meta-llama/llama-3.3-70b-instruct"
    ])
    gsw_delay: float = 0.5  # API rate limiting delay in seconds
    gsw_max_retries: int = 3
    gsw_use_toon: bool = True  # Use TOON format for context (~40% token reduction)

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    enable_graph_building: bool = True
    graph_include_legislation: bool = True
    graph_min_citation_confidence: float = 0.7

    # ========================================================================
    # FORMAT SETTINGS
    # ========================================================================

    use_toon: bool = True
    toon_workspace_storage: bool = True
    toon_batch_size: int = 100

    # ========================================================================
    # PROCESSING LIMITS
    # ========================================================================

    document_limit: Optional[int] = None  # None = process all documents
    max_text_length: int = 30000  # Maximum text length for GSW extraction
    skip_existing: bool = True  # Skip already processed documents

    # ========================================================================
    # CHECKPOINTING
    # ========================================================================

    enable_checkpoints: bool = True
    checkpoint_interval: int = 10000  # Save checkpoint every N documents
    checkpoint_compress: bool = True

    # ========================================================================
    # LOGGING
    # ========================================================================

    log_level: str = "INFO"
    log_file: Optional[Path] = None
    verbose: bool = False

    # ========================================================================
    # PARALLEL PROCESSING
    # ========================================================================

    parallel_workers: int = 1  # Number of parallel workers (future)
    use_multiprocessing: bool = False  # Enable multiprocessing (future)

    def __post_init__(self):
        """Convert string paths to Path objects."""
        self.corpus_path = Path(self.corpus_path)
        self.output_dir = Path(self.output_dir)
        self.workspace_dir = Path(self.workspace_dir)
        self.graph_dir = Path(self.graph_dir)
        self.checkpoint_dir = Path(self.checkpoint_dir)
        if self.log_file:
            self.log_file = Path(self.log_file)

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "PipelineConfig":
        """Load configuration from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Convert nested dicts to proper types
        if data is None:
            data = {}

        return cls(**data)

    def to_yaml(self, yaml_path: Path) -> None:
        """Save configuration to YAML file."""
        yaml_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict and handle Path objects
        data = asdict(self)

        # Convert Path objects to strings for YAML serialization
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)
            elif isinstance(value, list) and value and isinstance(value[0], Path):
                data[key] = [str(p) for p in value]

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        # Convert Path objects to strings
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)
        return data

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []

        # Check input file exists
        if not self.corpus_path.exists():
            errors.append(f"Corpus file not found: {self.corpus_path}")

        # Check output directories are writable
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory: {e}")

        # Validate GSW settings
        if self.enable_auto_gsw:
            if self.gsw_authority_threshold < 0 or self.gsw_authority_threshold > 100:
                errors.append(f"Invalid authority threshold: {self.gsw_authority_threshold}")

            if not self.gsw_model:
                errors.append("GSW model not specified")

        # Validate limits
        if self.document_limit is not None and self.document_limit < 1:
            errors.append(f"Invalid document limit: {self.document_limit}")

        if self.max_text_length < 1000:
            errors.append(f"max_text_length too small: {self.max_text_length}")

        return errors

    def summary(self) -> str:
        """Return a human-readable summary of the configuration."""
        lines = [
            "Pipeline Configuration Summary",
            "=" * 60,
            f"Input: {self.corpus_path}",
            f"Output: {self.output_dir}",
            f"Workspaces: {self.workspace_dir}",
            f"Graph: {self.graph_dir}",
            "",
            "Processing:",
            f"  - Document limit: {self.document_limit or 'None (all)'}",
            f"  - Use TOON format: {self.use_toon}",
            f"  - Checkpointing: {self.enable_checkpoints}",
            "",
            "Classification:",
            f"  - Progress interval: {self.classification_progress_interval}",
            f"  - Resume from checkpoint: {self.classification_resume}",
            "",
            "GSW Extraction:",
            f"  - Enabled: {self.enable_auto_gsw}",
            f"  - Authority threshold: {self.gsw_authority_threshold}",
            f"  - Model: {self.gsw_model}",
            f"  - Fallback models: {len(self.gsw_fallback_models)}",
            f"  - Batch size: {self.gsw_batch_size}",
            f"  - Rate limit delay: {self.gsw_delay}s",
            "",
            "Graph Building:",
            f"  - Enabled: {self.enable_graph_building}",
            f"  - Include legislation: {self.graph_include_legislation}",
            "=" * 60,
        ]
        return "\n".join(lines)


# ============================================================================
# DEFAULT CONFIGURATIONS
# ============================================================================

def get_default_config() -> PipelineConfig:
    """Get default pipeline configuration."""
    return PipelineConfig()


def get_test_config() -> PipelineConfig:
    """Get configuration optimized for testing."""
    return PipelineConfig(
        document_limit=100,
        classification_progress_interval=10,
        gsw_batch_size=5,
        enable_graph_building=False,
        checkpoint_interval=50,
    )


def get_production_config() -> PipelineConfig:
    """Get configuration optimized for production."""
    return PipelineConfig(
        document_limit=None,  # Process all
        classification_progress_interval=10000,
        gsw_authority_threshold=70,  # Higher threshold for production
        gsw_batch_size=20,
        enable_checkpoints=True,
        checkpoint_interval=50000,
        checkpoint_compress=True,
    )


# ============================================================================
# CLI HELPER
# ============================================================================

def create_example_config(output_path: Path) -> None:
    """Create an example configuration file."""
    config = get_default_config()
    config.to_yaml(output_path)
    print(f"Created example configuration: {output_path}")


if __name__ == "__main__":
    # Test configuration
    print("Testing PipelineConfig...")

    config = get_default_config()
    print(config.summary())

    # Test YAML serialization
    test_path = Path("test_config.yaml")
    config.to_yaml(test_path)
    print(f"\nSaved test config to: {test_path}")

    # Test loading
    loaded = PipelineConfig.from_yaml(test_path)
    print(f"\nLoaded config: {loaded.corpus_path}")

    # Cleanup
    test_path.unlink()
    print("\nTest complete!")
