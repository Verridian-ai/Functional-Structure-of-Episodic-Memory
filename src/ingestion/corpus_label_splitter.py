"""
Corpus Label Splitter - Split corpus by existing labels (type, jurisdiction, source)
Uses the built-in metadata from the Open Australian Legal Corpus
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, Set
from contextlib import contextmanager


class LabelFileManager:
    """Manages output files for each label combination."""

    def __init__(self, output_dir: Path, split_by: str = "type"):
        self.output_dir = output_dir
        self.split_by = split_by
        self.files: Dict[str, object] = {}
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for f in self.files.values():
            f.close()

    def _get_file(self, label: str):
        """Get or create file handle for a label."""
        if label not in self.files:
            safe_name = label.replace("/", "_").replace(" ", "_").lower()
            filepath = self.output_dir / f"{safe_name}.jsonl"
            self.files[label] = open(filepath, 'w', encoding='utf-8')
        return self.files[label]

    def write(self, label: str, doc: dict):
        """Write document to appropriate file."""
        f = self._get_file(label)
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')


def split_corpus(input_path: Path, output_dir: Path, split_by: str = "type",
                 progress_interval: int = 10000):
    """
    Split corpus by existing labels.

    Args:
        input_path: Path to corpus.jsonl
        output_dir: Output directory for split files
        split_by: Field to split by - "type", "jurisdiction", "source", or "type_jurisdiction"
        progress_interval: How often to report progress
    """

    counts = defaultdict(int)
    total = 0
    start_time = datetime.now()

    print(f"[Splitter] Input: {input_path}")
    print(f"[Splitter] Output: {output_dir}")
    print(f"[Splitter] Split by: {split_by}")
    print("-" * 60)

    with open(input_path, 'r', encoding='utf-8') as f_in:
        with LabelFileManager(output_dir, split_by) as manager:
            for line in f_in:
                if not line.strip():
                    continue

                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue

                total += 1

                # Determine label based on split_by
                if split_by == "type":
                    label = doc.get("type", "unknown")
                elif split_by == "jurisdiction":
                    label = doc.get("jurisdiction", "unknown")
                elif split_by == "source":
                    label = doc.get("source", "unknown")
                elif split_by == "type_jurisdiction":
                    doc_type = doc.get("type", "unknown")
                    jurisdiction = doc.get("jurisdiction", "unknown")
                    label = f"{doc_type}_{jurisdiction}"
                else:
                    label = doc.get(split_by, "unknown")

                counts[label] += 1
                manager.write(label, doc)

                # Progress reporting
                if total % progress_interval == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = total / elapsed if elapsed > 0 else 0

                    # Show top 5 labels
                    top_labels = sorted(counts.items(), key=lambda x: -x[1])[:5]
                    label_str = " | ".join([f"{k}:{v}" for k, v in top_labels])
                    print(f"[Progress] {total:,} docs | {rate:.0f}/sec | {label_str}")

    # Final stats
    elapsed = datetime.now() - start_time
    print(f"\n[Complete] Processed {total:,} documents in {elapsed}")

    # Save statistics
    stats = {
        "total_documents": total,
        "split_by": split_by,
        "started_at": start_time.isoformat(),
        "completed_at": datetime.now().isoformat(),
        "label_counts": dict(counts)
    }

    stats_path = output_dir / "split_statistics.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

    print(f"[Stats] Saved to {stats_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("LABEL DISTRIBUTION:")
    print("=" * 60)
    for label, count in sorted(counts.items(), key=lambda x: -x[1]):
        pct = (count / total) * 100
        print(f"  {label}: {count:,} ({pct:.1f}%)")

    return counts


def main():
    parser = argparse.ArgumentParser(description="Split corpus by existing labels")
    parser.add_argument("--input", required=True, help="Path to corpus.jsonl")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--split-by", default="type",
                        choices=["type", "jurisdiction", "source", "type_jurisdiction"],
                        help="Field to split by")
    parser.add_argument("--progress", type=int, default=10000, help="Progress interval")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    split_corpus(input_path, output_dir, args.split_by, args.progress)


if __name__ == "__main__":
    main()
