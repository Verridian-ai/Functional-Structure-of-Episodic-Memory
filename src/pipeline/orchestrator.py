"""
Full Pipeline Orchestrator - End-to-End Corpus Processing

This module orchestrates the complete pipeline from raw corpus to query-ready system.

Pipeline Stages:
1. Classification: Classify documents into legal domains
2. GSW: Extract structured GSW from high-authority cases
3. Graph: Build citation network (Hier-SPCNet)
4. Index: Create search indices (future)

Features:
- Stage-by-stage execution
- Checkpointing and resume capability
- Progress tracking and statistics
- Error handling and recovery
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from .config import PipelineConfig, PipelineStage


# ============================================================================
# PIPELINE STATE
# ============================================================================

@dataclass
class StageResult:
    """Result of a pipeline stage execution."""
    stage: str
    success: bool
    duration_seconds: float
    documents_processed: int = 0
    errors: List[str] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PipelineState:
    """
    Overall pipeline execution state.

    Tracks progress, completed stages, and statistics.
    """
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_stages: List[str] = field(default_factory=list)
    stage_results: Dict[str, StageResult] = field(default_factory=dict)
    total_documents_processed: int = 0
    gsw_queue_size: int = 0
    graph_node_count: int = 0
    graph_edge_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "started_at": self.started_at,
            "last_updated": self.last_updated,
            "completed_stages": self.completed_stages,
            "stage_results": {
                stage: {
                    "stage": result.stage,
                    "success": result.success,
                    "duration_seconds": result.duration_seconds,
                    "documents_processed": result.documents_processed,
                    "errors": result.errors,
                    "statistics": result.statistics,
                    "timestamp": result.timestamp
                }
                for stage, result in self.stage_results.items()
            },
            "total_documents_processed": self.total_documents_processed,
            "gsw_queue_size": self.gsw_queue_size,
            "graph_node_count": self.graph_node_count,
            "graph_edge_count": self.graph_edge_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PipelineState":
        """Load from dictionary."""
        state = cls(
            started_at=data.get("started_at", datetime.now().isoformat()),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            completed_stages=data.get("completed_stages", []),
            total_documents_processed=data.get("total_documents_processed", 0),
            gsw_queue_size=data.get("gsw_queue_size", 0),
            graph_node_count=data.get("graph_node_count", 0),
            graph_edge_count=data.get("graph_edge_count", 0)
        )

        # Reconstruct stage results
        for stage, result_data in data.get("stage_results", {}).items():
            state.stage_results[stage] = StageResult(
                stage=result_data["stage"],
                success=result_data["success"],
                duration_seconds=result_data["duration_seconds"],
                documents_processed=result_data.get("documents_processed", 0),
                errors=result_data.get("errors", []),
                statistics=result_data.get("statistics", {}),
                timestamp=result_data.get("timestamp", "")
            )

        return state


# ============================================================================
# FULL PIPELINE ORCHESTRATOR
# ============================================================================

class FullPipeline:
    """
    Orchestrates end-to-end corpus processing pipeline.

    This is the main entry point for running the complete pipeline
    from raw corpus to query-ready system.
    """

    def __init__(self, config: PipelineConfig):
        """
        Initialize the pipeline orchestrator.

        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.state = PipelineState()
        self.state_path = config.checkpoint_dir / "pipeline_state.json"

        # GSW queue (populated during classification)
        self.gsw_queue = None

    def run(self, stages: Optional[List[str]] = None, resume: bool = False) -> PipelineState:
        """
        Run pipeline stages.

        Args:
            stages: List of stages to run (None = all)
            resume: Whether to resume from checkpoint

        Returns:
            Final pipeline state
        """
        # Default to all stages
        if stages is None:
            stages = ["classify", "gsw", "graph", "index"]

        # Load checkpoint if resuming
        if resume:
            self._load_checkpoint()

        print(f"\n{'='*70}")
        print(f"  LEGAL CORPUS PROCESSING PIPELINE")
        print(f"{'='*70}\n")
        print(self.config.summary())
        print()

        # Validate configuration
        errors = self.config.validate()
        if errors:
            print("[Error] Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            return self.state

        # Run each stage
        for stage in stages:
            # Skip if already completed (unless forced)
            if stage in self.state.completed_stages and resume:
                print(f"\n[Skip] Stage '{stage}' already completed")
                continue

            print(f"\n{'='*70}")
            print(f"  STAGE: {stage.upper()}")
            print(f"{'='*70}\n")

            start_time = time.time()
            result = None

            try:
                if stage == "classify":
                    result = self._run_classification()
                elif stage == "gsw":
                    result = self._run_gsw_extraction()
                elif stage == "graph":
                    result = self._run_graph_building()
                elif stage == "index":
                    result = self._run_indexing()
                else:
                    print(f"[Warning] Unknown stage: {stage}")
                    continue

                # Record result
                if result:
                    result.duration_seconds = time.time() - start_time
                    self.state.stage_results[stage] = result

                    if result.success:
                        self.state.completed_stages.append(stage)
                        print(f"\n[Success] Stage '{stage}' completed in {result.duration_seconds:.1f}s")
                    else:
                        print(f"\n[Failed] Stage '{stage}' failed after {result.duration_seconds:.1f}s")
                        if result.errors:
                            for error in result.errors:
                                print(f"  - {error}")

                # Save checkpoint
                self._save_checkpoint()

            except Exception as e:
                print(f"\n[Error] Stage '{stage}' crashed: {e}")
                import traceback
                traceback.print_exc()

                # Record failure
                result = StageResult(
                    stage=stage,
                    success=False,
                    duration_seconds=time.time() - start_time,
                    errors=[str(e)]
                )
                self.state.stage_results[stage] = result
                self._save_checkpoint()

                # Stop pipeline on error
                break

        # Final summary
        self._print_final_summary()

        return self.state

    def _run_classification(self) -> StageResult:
        """
        Stage 1: Classify corpus into legal domains.

        This stage:
        - Streams corpus.jsonl
        - Classifies each document using multi-dimensional scoring
        - Writes to domain-specific TOON files
        - Optionally queues high-authority docs for GSW extraction
        """
        from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
        from src.ingestion.auto_gsw_trigger import GSWExtractionQueue

        print(f"[Classification] Input: {self.config.corpus_path}")
        print(f"[Classification] Output: {self.config.output_dir}")
        print(f"[Classification] Document limit: {self.config.document_limit or 'None (all)'}")

        # Create GSW queue if auto-extraction enabled
        if self.config.enable_auto_gsw:
            self.gsw_queue = GSWExtractionQueue(
                min_authority=self.config.gsw_authority_threshold,
                checkpoint_path=self.config.checkpoint_dir / "gsw_queue.json"
            )
            print(f"[Classification] GSW auto-queue enabled (threshold={self.config.gsw_authority_threshold})")

        # Create extractor
        extractor = CorpusDomainExtractor(
            input_path=self.config.corpus_path,
            output_dir=self.config.output_dir,
            state_path=self.config.checkpoint_dir / "extraction_state.json"
        )

        # Run classification
        try:
            stats = extractor.extract_all(
                progress_interval=self.config.classification_progress_interval,
                resume=self.config.classification_resume,
                limit=self.config.document_limit
            )

            # Queue high-authority documents for GSW
            if self.gsw_queue and self.config.enable_auto_gsw:
                # Re-scan classified files to populate queue
                print(f"\n[Classification] Scanning for high-authority documents...")
                self._populate_gsw_queue(stats)

            # Calculate totals
            total_docs = sum(s.document_count for s in stats.values())
            self.state.total_documents_processed = total_docs
            if self.gsw_queue:
                self.state.gsw_queue_size = self.gsw_queue.qsize()

            # Build statistics
            statistics = {
                "total_documents": total_docs,
                "domains": {domain: s.document_count for domain, s in stats.items()},
                "gsw_queue_size": self.state.gsw_queue_size if self.gsw_queue else 0
            }

            return StageResult(
                stage="classify",
                success=True,
                duration_seconds=0,  # Will be set by caller
                documents_processed=total_docs,
                statistics=statistics
            )

        except Exception as e:
            return StageResult(
                stage="classify",
                success=False,
                duration_seconds=0,
                errors=[str(e)]
            )

    def _populate_gsw_queue(self, stats: Dict[str, Any]) -> None:
        """
        Populate GSW queue by scanning classified domain files.

        Args:
            stats: Classification statistics
        """
        from src.utils.toon import ToonDecoder

        scanned = 0
        queued = 0

        # Scan all domain files
        domain_files = list((self.config.output_dir / "cases").rglob("*.toon"))

        for domain_file in domain_files:
            try:
                with open(domain_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                tables = ToonDecoder.decode(content)

                for table_name, rows in tables.items():
                    for row in rows:
                        scanned += 1

                        # Check authority score
                        authority = row.get('score', 0)  # 'score' is authority_score in TOON
                        if authority >= self.config.gsw_authority_threshold:
                            # Reconstruct doc for queue
                            doc = {
                                'citation': row.get('citation', ''),
                                'text': row.get('text', ''),
                                'type': row.get('type', ''),
                                'jurisdiction': row.get('jurisdiction', ''),
                                '_classification': {
                                    'primary_domain': row.get('domain', ''),
                                    'authority_score': authority,
                                    'court': row.get('court', ''),
                                    'court_level': row.get('court_level', ''),
                                    'case_refs': row.get('case_refs', '').split('|') if row.get('case_refs') else [],
                                    'legislation_refs': row.get('leg_refs', '').split('|') if row.get('leg_refs') else []
                                }
                            }

                            if self.gsw_queue.add(doc):
                                queued += 1

            except Exception as e:
                print(f"[Warning] Error scanning {domain_file}: {e}")
                continue

        print(f"[Classification] Scanned {scanned} documents, queued {queued} for GSW extraction")

    def _run_gsw_extraction(self) -> StageResult:
        """
        Stage 2: Extract GSW from high-priority documents.

        This stage:
        - Processes documents from GSW queue
        - Runs Legal Operator extraction
        - Merges into domain workspaces
        - Saves workspace files (JSON or TOON)
        """
        if not self.config.enable_auto_gsw:
            print("[GSW] Skipped (disabled in config)")
            return StageResult(
                stage="gsw",
                success=True,
                duration_seconds=0,
                statistics={"skipped": True}
            )

        # Load queue if not already populated
        if not self.gsw_queue:
            from src.ingestion.auto_gsw_trigger import GSWExtractionQueue
            self.gsw_queue = GSWExtractionQueue(
                min_authority=self.config.gsw_authority_threshold,
                checkpoint_path=self.config.checkpoint_dir / "gsw_queue.json"
            )

        if self.gsw_queue.empty():
            print("[GSW] No documents in queue")
            return StageResult(
                stage="gsw",
                success=True,
                duration_seconds=0,
                statistics={"documents_processed": 0}
            )

        print(f"[GSW] Processing {self.gsw_queue.qsize()} high-priority documents")
        print(f"[GSW] Model: {self.config.gsw_model}")
        print(f"[GSW] Fallback models: {len(self.config.gsw_fallback_models)}")

        from src.gsw.legal_operator import LegalOperator
        from src.gsw.workspace import WorkspaceManager
        from src.logic.gsw_schema import GlobalWorkspace

        # Initialize operator with model rotation
        operator = LegalOperator(
            model=self.config.gsw_fallback_models,  # Pass list for rotation
            use_toon=self.config.gsw_use_toon
        )

        # Track workspaces per domain
        domain_workspaces: Dict[str, WorkspaceManager] = {}

        processed = 0
        errors = []

        try:
            while not self.gsw_queue.empty():
                batch = self.gsw_queue.process_batch(self.config.gsw_batch_size)

                for doc in batch:
                    try:
                        domain = doc['_classification']['primary_domain']
                        citation = doc.get('citation', 'Unknown')

                        print(f"[GSW] Extracting: {citation} (domain={domain})")

                        # Extract
                        extraction = operator.extract(
                            text=doc.get('text', '')[:self.config.max_text_length],
                            situation=f"Legal case: {citation}",
                            document_id=doc.get('version_id', citation)
                        )

                        # Get or create workspace for domain
                        if domain not in domain_workspaces:
                            workspace_path = self.config.workspace_dir / f"{domain}_workspace.json"
                            if workspace_path.exists():
                                manager = WorkspaceManager.load(workspace_path)
                            else:
                                workspace = GlobalWorkspace(domain=domain)
                                manager = WorkspaceManager(workspace=workspace, storage_path=workspace_path)
                            domain_workspaces[domain] = manager

                        # Merge extraction into workspace
                        domain_workspaces[domain].workspace.merge_extraction(extraction)

                        # Mark as processed
                        self.gsw_queue.mark_processed(doc)
                        processed += 1

                        # Rate limiting
                        time.sleep(self.config.gsw_delay)

                    except Exception as e:
                        error_msg = f"Error processing {doc.get('citation', 'unknown')}: {str(e)[:100]}"
                        print(f"[GSW Error] {error_msg}")
                        errors.append(error_msg)
                        continue

                # Checkpoint every batch
                if processed % (self.config.gsw_batch_size * 10) == 0:
                    print(f"[GSW] Checkpoint: {processed} documents processed")
                    self.gsw_queue.save_checkpoint()
                    self._save_workspaces(domain_workspaces)

            # Save final workspaces
            self._save_workspaces(domain_workspaces)
            self.gsw_queue.save_checkpoint()

            # Statistics
            stats = {
                "documents_processed": processed,
                "domains": len(domain_workspaces),
                "errors": len(errors),
                "model_used": operator.model
            }

            # Add workspace stats
            for domain, manager in domain_workspaces.items():
                workspace_stats = manager.get_statistics()
                stats[f"workspace_{domain}"] = workspace_stats

            return StageResult(
                stage="gsw",
                success=True,
                duration_seconds=0,
                documents_processed=processed,
                errors=errors[:10],  # Limit error list
                statistics=stats
            )

        except Exception as e:
            return StageResult(
                stage="gsw",
                success=False,
                duration_seconds=0,
                documents_processed=processed,
                errors=[str(e)]
            )

    def _save_workspaces(self, domain_workspaces: Dict[str, Any]) -> None:
        """Save all domain workspaces."""
        from src.utils.toon import ToonEncoder

        for domain, manager in domain_workspaces.items():
            # Save as JSON
            json_path = self.config.workspace_dir / f"{domain}_workspace.json"
            manager.save(json_path)

            # Optionally save as TOON
            if self.config.toon_workspace_storage:
                # TOON workspace export would require custom serialization
                # For now, we just save JSON
                pass

    def _run_graph_building(self) -> StageResult:
        """
        Stage 3: Build citation network (Hier-SPCNet).

        This stage:
        - Scans domain files for cases
        - Extracts citations from text
        - Builds node and edge lists
        - Saves as TOON files
        """
        if not self.config.enable_graph_building:
            print("[Graph] Skipped (disabled in config)")
            return StageResult(
                stage="graph",
                success=True,
                duration_seconds=0,
                statistics={"skipped": True}
            )

        from src.graph.spcnet_builder import SPCNetBuilder

        print(f"[Graph] Building citation network...")
        print(f"[Graph] Input: {self.config.output_dir / 'cases'}")
        print(f"[Graph] Output: {self.config.graph_dir}")

        try:
            # Create builder
            builder = SPCNetBuilder(
                input_dir=self.config.output_dir / "cases",
                output_dir=self.config.graph_dir
            )

            # Build graph
            builder._index_nodes()
            builder._extract_edges()

            # Save as TOON
            nodes_path = self.config.graph_dir / "spcnet_nodes.toon"
            edges_path = self.config.graph_dir / "spcnet_edges.toon"

            builder._export()

            # Update state
            self.state.graph_node_count = len(builder.nodes)
            self.state.graph_edge_count = len(builder.edges)

            print(f"[Graph] Nodes: {len(builder.nodes)}")
            print(f"[Graph] Edges: {len(builder.edges)}")
            print(f"[Graph] Saved to: {self.config.graph_dir}")

            return StageResult(
                stage="graph",
                success=True,
                duration_seconds=0,
                statistics={
                    "nodes": len(builder.nodes),
                    "edges": len(builder.edges),
                    "nodes_file": str(nodes_path),
                    "edges_file": str(edges_path)
                }
            )

        except Exception as e:
            return StageResult(
                stage="graph",
                success=False,
                duration_seconds=0,
                errors=[str(e)]
            )

    def _run_indexing(self) -> StageResult:
        """
        Stage 4: Create search indices.

        This stage is a placeholder for future indexing work.
        """
        print("[Index] Creating search indices...")
        print("[Index] (Not yet implemented)")

        return StageResult(
            stage="index",
            success=True,
            duration_seconds=0,
            statistics={"skipped": True, "reason": "Not implemented"}
        )

    def _save_checkpoint(self) -> None:
        """Save pipeline state to checkpoint file."""
        if not self.config.enable_checkpoints:
            return

        self.state.last_updated = datetime.now().isoformat()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state.to_dict(), f, indent=2)

        print(f"[Checkpoint] Saved to {self.state_path}")

    def _load_checkpoint(self) -> None:
        """Load pipeline state from checkpoint file."""
        if not self.state_path.exists():
            print(f"[Checkpoint] No existing checkpoint found")
            return

        try:
            with open(self.state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.state = PipelineState.from_dict(data)
            print(f"[Checkpoint] Loaded: {len(self.state.completed_stages)} stages completed")

        except Exception as e:
            print(f"[Checkpoint Warning] Could not load checkpoint: {e}")

    def _print_final_summary(self) -> None:
        """Print final pipeline summary."""
        print(f"\n{'='*70}")
        print(f"  PIPELINE SUMMARY")
        print(f"{'='*70}\n")

        # Overall status
        total_stages = len(self.state.stage_results)
        successful_stages = sum(1 for r in self.state.stage_results.values() if r.success)

        print(f"Stages completed: {successful_stages}/{total_stages}")
        print(f"Total documents: {self.state.total_documents_processed}")
        print(f"GSW queue size: {self.state.gsw_queue_size}")
        print(f"Graph nodes: {self.state.graph_node_count}")
        print(f"Graph edges: {self.state.graph_edge_count}")

        # Stage-by-stage results
        print("\nStage Results:")
        for stage, result in self.state.stage_results.items():
            status = "SUCCESS" if result.success else "FAILED"
            print(f"  [{status}] {stage.upper()}: {result.duration_seconds:.1f}s, {result.documents_processed} docs")
            if result.errors:
                print(f"    Errors: {len(result.errors)}")

        print(f"\n{'='*70}\n")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def run_pipeline(
    config: Optional[PipelineConfig] = None,
    stages: Optional[List[str]] = None,
    resume: bool = False
) -> PipelineState:
    """
    Convenience function to run the pipeline.

    Args:
        config: Pipeline configuration (None = default)
        stages: Stages to run (None = all)
        resume: Resume from checkpoint

    Returns:
        Final pipeline state
    """
    if config is None:
        config = PipelineConfig()

    pipeline = FullPipeline(config)
    return pipeline.run(stages=stages, resume=resume)
