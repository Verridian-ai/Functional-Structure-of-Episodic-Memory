
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import json
import shutil
from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
from src.graph.spcnet_builder import SPCNetBuilder
from src.tem.legal_graph_builder import LegalGraphBuilder
from src.utils.toon import ToonDecoder

# Optimized paths
TEST_DIR = Path("tmp/verify_pipeline")
INPUT_FILE = TEST_DIR / "corpus.jsonl"
OUTPUT_DIR = TEST_DIR / "processed"
GRAPH_DIR = TEST_DIR / "graph"

def setup_test_data():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)
    
    docs = [
        # Legislation
        {
            "type": "primary_legislation",
            "citation": "Corporations Act 2001",
            "jurisdiction": "Commonwealth",
            "text": "An Act to make provision in relation to corporations...",
            "date": "2001-01-01"
        },
        # Case Law (Commercial)
        {
            "type": "decision",
            "citation": "[2023] HCA 1",
            "name": "Testing v Commissioner",
            "jurisdiction": "Commonwealth",
            "text": "The High Court held that per s 180 of the Corporations Act 2001...",
            "date": "2023-01-01"
        },
        # Case Law (Family)
        {
            "type": "decision",
            "citation": "[2022] FamCA 50",
            "name": "P vs D",
            "jurisdiction": "Commonwealth",
            "text": "In this family law matter regarding s 79 property settlement...",
            "date": "2022-06-01"
        }
    ]
    
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(json.dumps(doc) + '\n')

def verify_extractor():
    print("\n--- Running Extractor ---")
    extractor = CorpusDomainExtractor(INPUT_FILE, OUTPUT_DIR)
    extractor.extract_all(progress_interval=1)
    
    # Check Legislation
    leg_path = OUTPUT_DIR / "legislation" / "acts.toon"
    if leg_path.exists():
        print("[Pass] Legislation file created")
        with open(leg_path, 'r') as f:
            print(f"Content preview:\n{f.read(200)}...")
    else:
        print("[Fail] Legislation file missing")
        return False

    # Check Cases
    # Commercial domain should exist due to Corporations Act reference/classification
    case_path = OUTPUT_DIR / "cases" / "Commercial" / "Commercial.toon"
    if case_path.exists():
         print("[Pass] Commercial case file created")
    else:
         print(f"[Fail] Commercial case file missing. Found: {list(OUTPUT_DIR.glob('cases/*'))}")

    return True

def verify_graph():
    print("\n--- Running SPCNetBuilder ---")
    builder = SPCNetBuilder(OUTPUT_DIR, GRAPH_DIR)
    builder.build()
    
    nodes_path = GRAPH_DIR / "spcnet_nodes.toon"
    edges_path = GRAPH_DIR / "spcnet_edges.toon"
    
    if nodes_path.exists() and edges_path.exists():
        print("[Pass] Graph files created")
        with open(nodes_path, 'r') as f:
            print(f"Nodes preview:\n{f.read(200)}...")
        return True
    else:
        print("[Fail] Graph files missing")
        return False

def verify_tem_load():
    print("\n--- Running TEM LegalGraphBuilder ---")
    try:
        gb = LegalGraphBuilder(GRAPH_DIR)
        print(f"[Pass] Graph loaded. Nodes: {len(gb.nodes)}")
        path, actions = gb.random_walk(gb.node_ids[0], 5)
        print(f"Random walk: {path}")
        return True
    except Exception as e:
        print(f"[Fail] TEM load failed: {e}")
        return False

if __name__ == "__main__":
    setup_test_data()
    if verify_extractor():
        if verify_graph():
            verify_tem_load()
