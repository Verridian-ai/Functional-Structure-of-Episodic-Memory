"""Quick test of corpus domain extractor."""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor

input_path = Path("data/corpus.jsonl")
output_dir = Path("data/processed/domains")

print(f"Input exists: {input_path.exists()}")
print(f"Input size: {input_path.stat().st_size / 1e9:.2f} GB")

# Fresh start - delete old state
state_file = Path("data/processed/extraction_state.json")
if state_file.exists():
    state_file.unlink()
    print("Deleted old state file")

extractor = CorpusDomainExtractor(
    input_path=input_path,
    output_dir=output_dir
)

print("Starting extraction...")
start = datetime.now()

try:
    stats = extractor.extract_all(progress_interval=5000, resume=False)
    print(f"\nCompleted in {datetime.now() - start}")
    for domain, stat in sorted(stats.items(), key=lambda x: x[1].document_count, reverse=True)[:10]:
        print(f"  {domain}: {stat.document_count}")
except KeyboardInterrupt:
    print("\nInterrupted by user")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

