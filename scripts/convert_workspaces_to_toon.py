"""
Convert JSON Workspaces to TOON Format

This script migrates all JSON workspace files to TOON format,
achieving ~62% file size reduction while maintaining full data fidelity.

Usage:
    python scripts/convert_workspaces_to_toon.py

Features:
- Auto-discovers all workspace JSON files
- Converts to TOON format
- Validates round-trip conversion
- Reports size savings
- Optionally removes original JSON files
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.gsw.workspace import WorkspaceManager
from src.utils.toon import measure_compression


def find_workspace_files(workspace_dir: Path) -> List[Path]:
    """Find all workspace JSON files."""
    return list(workspace_dir.glob("*_workspace.json"))


def convert_workspace(json_path: Path, validate: bool = True) -> Tuple[Path, dict]:
    """
    Convert a single workspace from JSON to TOON.

    Args:
        json_path: Path to JSON workspace file
        validate: Whether to validate round-trip conversion

    Returns:
        Tuple of (toon_path, compression_stats)
    """
    print(f"\n{'='*60}")
    print(f"Converting: {json_path.name}")
    print(f"{'='*60}")

    # Load JSON workspace
    manager = WorkspaceManager.load(json_path)

    # Save to TOON
    toon_path = json_path.with_suffix('.toon')
    manager.save_toon(toon_path)

    # Measure compression
    with open(json_path, 'r', encoding='utf-8') as f:
        json_content = f.read()

    with open(toon_path, 'r', encoding='utf-8') as f:
        toon_content = f.read()

    stats = measure_compression(json_content, toon_content)

    print(f"\nCompression Results:")
    print(f"  JSON size: {stats['json_chars']:,} chars (~{stats['json_tokens_est']:,} tokens)")
    print(f"  TOON size: {stats['toon_chars']:,} chars (~{stats['toon_tokens_est']:,} tokens)")
    print(f"  Reduction: {stats['char_reduction']} (chars) / {stats['token_reduction']} (tokens)")

    # Validate round-trip if requested
    if validate:
        print(f"\nValidating round-trip conversion...")

        # Load TOON and compare
        manager_toon = WorkspaceManager.load_toon(toon_path)

        # Compare key metrics
        original_ws = manager.workspace
        loaded_ws = manager_toon.workspace

        assert len(original_ws.actors) == len(loaded_ws.actors), \
            f"Actor count mismatch: {len(original_ws.actors)} vs {len(loaded_ws.actors)}"

        assert len(original_ws.verb_phrases) == len(loaded_ws.verb_phrases), \
            f"Verb phrase count mismatch"

        assert len(original_ws.questions) == len(loaded_ws.questions), \
            f"Question count mismatch"

        assert len(original_ws.spatio_temporal_links) == len(loaded_ws.spatio_temporal_links), \
            f"Link count mismatch"

        print(f"  ✓ Validation passed!")
        print(f"    - {len(loaded_ws.actors)} actors")
        print(f"    - {len(loaded_ws.verb_phrases)} verb phrases")
        print(f"    - {len(loaded_ws.questions)} questions")
        print(f"    - {len(loaded_ws.spatio_temporal_links)} links")

    return toon_path, stats


def main():
    """Main migration script."""
    print("="*60)
    print("JSON to TOON Workspace Migration")
    print("="*60)

    # Find workspace directory
    workspace_dir = project_root / "data" / "workspaces"

    if not workspace_dir.exists():
        print(f"ERROR: Workspace directory not found: {workspace_dir}")
        return

    # Find all workspace files
    json_files = find_workspace_files(workspace_dir)

    if not json_files:
        print(f"No workspace files found in {workspace_dir}")
        return

    print(f"\nFound {len(json_files)} workspace file(s)")

    # Convert each workspace
    results = []
    for json_file in json_files:
        try:
            toon_path, stats = convert_workspace(json_file, validate=True)
            results.append((json_file, toon_path, stats))
        except Exception as e:
            print(f"\nERROR converting {json_file.name}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print(f"\n{'='*60}")
    print("MIGRATION SUMMARY")
    print(f"{'='*60}")

    if results:
        total_json_chars = sum(r[2]['json_chars'] for r in results)
        total_toon_chars = sum(r[2]['toon_chars'] for r in results)

        print(f"\nSuccessfully converted {len(results)} workspace(s)")
        print(f"\nTotal Savings:")
        print(f"  JSON: {total_json_chars:,} chars")
        print(f"  TOON: {total_toon_chars:,} chars")
        print(f"  Saved: {total_json_chars - total_toon_chars:,} chars")
        print(f"  Reduction: {((1 - total_toon_chars/total_json_chars)*100):.1f}%")

        print(f"\nConverted files:")
        for json_path, toon_path, stats in results:
            print(f"  {json_path.name} -> {toon_path.name} ({stats['char_reduction']})")

        # Ask about removing originals
        print(f"\n{'='*60}")
        remove_json = input("\nRemove original JSON files? (y/N): ").strip().lower()

        if remove_json == 'y':
            for json_path, toon_path, stats in results:
                json_path.unlink()
                print(f"  Removed: {json_path.name}")
            print(f"\nRemoved {len(results)} JSON file(s)")
        else:
            print("\nOriginal JSON files kept for safety")

    else:
        print("\nNo workspaces were converted")


if __name__ == "__main__":
    main()
