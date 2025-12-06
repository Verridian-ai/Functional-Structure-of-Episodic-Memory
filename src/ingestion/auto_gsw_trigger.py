"""
Auto-Trigger GSW Extraction - Priority Queue System
====================================================

Automatically triggers GSW extraction after classification based on authority score.
Uses a priority queue to process high-authority documents first.

Key Features:
- Authority-based priority queue (min_authority threshold)
- Smart sampling strategies (apex/appellate/trial courts)
- Progress tracking and checkpointing
- Batch processing for efficiency

Authority Thresholds:
- Apex courts (HCA, Full Courts): 90+
- Appellate courts (Court of Appeal): 70+
- Trial courts (selective): 50+

Usage:
    from src.ingestion.auto_gsw_trigger import GSWExtractionQueue

    queue = GSWExtractionQueue(min_authority=60)
    queue.add(doc, priority=85)
    batch = queue.process_batch(batch_size=10)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from queue import PriorityQueue
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


# ============================================================================
# AUTHORITY THRESHOLDS
# ============================================================================

# Court hierarchy thresholds for smart sampling
APEX_THRESHOLD = 90        # High Court of Australia, Full Courts
APPELLATE_THRESHOLD = 70   # Courts of Appeal, Federal Court
TRIAL_THRESHOLD = 50       # Trial courts (selective)

# Default minimum authority for GSW extraction
DEFAULT_MIN_AUTHORITY = 60


# ============================================================================
# CHECKPOINT STATE
# ============================================================================

@dataclass
class QueueCheckpoint:
    """Checkpoint state for GSW extraction queue."""
    processed_ids: Set[str] = field(default_factory=set)
    total_processed: int = 0
    total_queued: int = 0
    last_updated: str = ""
    authority_stats: Dict[str, int] = field(default_factory=dict)  # court_level -> count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "processed_ids": list(self.processed_ids),
            "total_processed": self.total_processed,
            "total_queued": self.total_queued,
            "last_updated": self.last_updated,
            "authority_stats": self.authority_stats
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueueCheckpoint":
        """Load from dictionary."""
        return cls(
            processed_ids=set(data.get("processed_ids", [])),
            total_processed=data.get("total_processed", 0),
            total_queued=data.get("total_queued", 0),
            last_updated=data.get("last_updated", ""),
            authority_stats=data.get("authority_stats", {})
        )


# ============================================================================
# GSW EXTRACTION QUEUE
# ============================================================================

class GSWExtractionQueue:
    """
    Priority queue for GSW extraction based on authority score.

    Higher authority documents are processed first to ensure
    precedent-setting cases are analyzed with highest fidelity.
    """

    def __init__(
        self,
        min_authority: int = DEFAULT_MIN_AUTHORITY,
        checkpoint_path: Optional[Path] = None
    ):
        """
        Initialize the GSW extraction queue.

        Args:
            min_authority: Minimum authority score to queue document (0-100)
            checkpoint_path: Path to checkpoint file for resume capability
        """
        self.queue = PriorityQueue()
        self.min_authority = min_authority
        self.checkpoint_path = checkpoint_path or Path("data/processed/gsw_queue_checkpoint.json")

        # Tracking
        self.checkpoint = QueueCheckpoint()

        # Load checkpoint if exists
        self._load_checkpoint()

    def add(self, doc: Dict[str, Any], priority: Optional[int] = None) -> bool:
        """
        Add document to queue if meets authority threshold.

        Args:
            doc: Document with _classification metadata
            priority: Optional override priority (default: use authority_score)

        Returns:
            True if document was queued, False if rejected
        """
        # Extract classification metadata
        classification = doc.get('_classification', {})
        authority = classification.get('authority_score', 0)

        # Use override priority or authority score
        effective_priority = priority if priority is not None else authority

        # Check threshold
        if effective_priority < self.min_authority:
            return False

        # Check if already processed
        doc_id = self._get_doc_id(doc)
        if doc_id in self.checkpoint.processed_ids:
            return False

        # Add to queue (negative for max-heap behavior)
        # PriorityQueue is min-heap, so negate for high-priority-first
        self.queue.put((-effective_priority, doc_id, doc))

        # Update stats
        self.checkpoint.total_queued += 1
        court_level = classification.get('court_level', 'unknown')
        self.checkpoint.authority_stats[court_level] = \
            self.checkpoint.authority_stats.get(court_level, 0) + 1

        return True

    def process_batch(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get next batch of high-priority documents.

        Args:
            batch_size: Number of documents to retrieve

        Returns:
            List of documents sorted by priority (highest first)
        """
        batch = []

        for _ in range(min(batch_size, self.queue.qsize())):
            if self.queue.empty():
                break

            _, doc_id, doc = self.queue.get()
            batch.append(doc)

        return batch

    def mark_processed(self, doc: Dict[str, Any]) -> None:
        """
        Mark document as processed in checkpoint.

        Args:
            doc: Document that was processed
        """
        doc_id = self._get_doc_id(doc)
        self.checkpoint.processed_ids.add(doc_id)
        self.checkpoint.total_processed += 1
        self.checkpoint.last_updated = datetime.now().isoformat()

    def is_processed(self, doc: Dict[str, Any]) -> bool:
        """
        Check if document has already been processed.

        Args:
            doc: Document to check

        Returns:
            True if already processed
        """
        doc_id = self._get_doc_id(doc)
        return doc_id in self.checkpoint.processed_ids

    def empty(self) -> bool:
        """Check if queue is empty."""
        return self.queue.empty()

    def qsize(self) -> int:
        """Get current queue size."""
        return self.queue.qsize()

    def get_statistics(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            "total_queued": self.checkpoint.total_queued,
            "total_processed": self.checkpoint.total_processed,
            "current_queue_size": self.qsize(),
            "min_authority": self.min_authority,
            "authority_stats": self.checkpoint.authority_stats,
            "last_updated": self.checkpoint.last_updated
        }

    def save_checkpoint(self) -> None:
        """Save checkpoint to file."""
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(self.checkpoint.to_dict(), f, indent=2)

        print(f"[Queue] Checkpoint saved: {self.checkpoint.total_processed} processed")

    def _load_checkpoint(self) -> None:
        """Load checkpoint from file if exists."""
        if not self.checkpoint_path.exists():
            return

        try:
            with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.checkpoint = QueueCheckpoint.from_dict(data)
            print(f"[Queue] Checkpoint loaded: {self.checkpoint.total_processed} previously processed")

        except Exception as e:
            print(f"[Queue Warning] Could not load checkpoint: {e}")

    def _get_doc_id(self, doc: Dict[str, Any]) -> str:
        """
        Get unique identifier for document.

        Uses citation as primary ID, falls back to combination of fields.
        """
        citation = doc.get('citation', '')
        if citation:
            return citation.strip()

        # Fallback: combine type + jurisdiction + snippet
        doc_type = doc.get('type', '')
        jurisdiction = doc.get('jurisdiction', '')
        text_snippet = doc.get('text', '')[:100] if doc.get('text') else ''

        return f"{doc_type}_{jurisdiction}_{hash(text_snippet)}"


# ============================================================================
# SMART SAMPLING STRATEGIES
# ============================================================================

class SmartSampler:
    """
    Smart sampling strategies for different court levels.

    Helps prioritize which documents to extract based on court hierarchy
    and domain importance.
    """

    @staticmethod
    def should_sample_apex(doc: Dict[str, Any]) -> bool:
        """All apex court cases should be sampled."""
        authority = doc.get('_classification', {}).get('authority_score', 0)
        return authority >= APEX_THRESHOLD

    @staticmethod
    def should_sample_appellate(doc: Dict[str, Any]) -> bool:
        """Sample appellate cases selectively."""
        authority = doc.get('_classification', {}).get('authority_score', 0)

        if authority >= APPELLATE_THRESHOLD:
            # Additional filters for appellate
            # - Must have case references (precedent-setting)
            case_refs = doc.get('_classification', {}).get('case_refs', [])
            return len(case_refs) > 0

        return False

    @staticmethod
    def should_sample_trial(doc: Dict[str, Any]) -> bool:
        """Sample trial courts very selectively."""
        authority = doc.get('_classification', {}).get('authority_score', 0)

        if authority >= TRIAL_THRESHOLD:
            # Additional filters for trial courts
            # - Must be in high-priority domain
            domain = doc.get('_classification', {}).get('primary_domain', '')
            high_priority_domains = {
                'Family', 'Criminal', 'Constitutional',
                'Migration', 'Tax', 'Competition'
            }

            if domain in high_priority_domains:
                # And must have significant case references
                case_refs = doc.get('_classification', {}).get('case_refs', [])
                return len(case_refs) >= 2

        return False

    @staticmethod
    def get_sampling_priority(doc: Dict[str, Any]) -> int:
        """
        Calculate sampling priority for document.

        Returns priority score (0-100+):
        - 90+: Apex courts (must sample)
        - 70-89: Appellate courts (should sample)
        - 50-69: Trial courts (selective sample)
        - <50: Skip
        """
        authority = doc.get('_classification', {}).get('authority_score', 0)
        court_level = doc.get('_classification', {}).get('court_level', '')

        base_priority = authority

        # Boost apex courts
        if court_level == 'apex':
            base_priority += 10

        # Boost if has many case references (precedent-setting)
        case_refs = doc.get('_classification', {}).get('case_refs', [])
        base_priority += min(len(case_refs), 10)  # Up to +10 for case refs

        # Boost if has many legislation references
        leg_refs = doc.get('_classification', {}).get('legislation_refs', [])
        base_priority += min(len(leg_refs), 5)  # Up to +5 for leg refs

        return min(base_priority, 100)


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("Testing GSWExtractionQueue...\n")

    # Create test documents
    test_docs = [
        {
            'citation': '[2023] HCA 1',
            'type': 'decision',
            '_classification': {
                'authority_score': 95,
                'court_level': 'apex',
                'court': 'HCA',
                'case_refs': ['Mabo v Queensland'],
                'legislation_refs': ['Constitution Act 1901']
            }
        },
        {
            'citation': '[2023] NSWCA 100',
            'type': 'decision',
            '_classification': {
                'authority_score': 75,
                'court_level': 'intermediate',
                'court': 'NSWCA',
                'case_refs': ['Smith v Jones'],
                'legislation_refs': []
            }
        },
        {
            'citation': '[2023] NSWDC 200',
            'type': 'decision',
            '_classification': {
                'authority_score': 45,
                'court_level': 'trial',
                'court': 'NSWDC',
                'case_refs': [],
                'legislation_refs': []
            }
        }
    ]

    # Test queue
    queue = GSWExtractionQueue(min_authority=60)

    print("Adding documents to queue...")
    for doc in test_docs:
        added = queue.add(doc)
        citation = doc['citation']
        authority = doc['_classification']['authority_score']
        status = "QUEUED" if added else "REJECTED"
        print(f"  {citation} (authority={authority}): {status}")

    print(f"\nQueue size: {queue.qsize()}")

    # Test batch processing
    print("\nProcessing batch...")
    batch = queue.process_batch(batch_size=5)
    for doc in batch:
        citation = doc['citation']
        authority = doc['_classification']['authority_score']
        print(f"  Processing: {citation} (authority={authority})")
        queue.mark_processed(doc)

    # Test statistics
    print("\nQueue statistics:")
    stats = queue.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test checkpoint
    print("\nSaving checkpoint...")
    queue.save_checkpoint()

    # Test smart sampler
    print("\nTesting SmartSampler...")
    sampler = SmartSampler()
    for doc in test_docs:
        citation = doc['citation']
        priority = sampler.get_sampling_priority(doc)
        should_sample = priority >= 60
        action = "SAMPLE" if should_sample else "SKIP"
        print(f"  {citation}: priority={priority} {action}")

    print("\nTest complete!")
