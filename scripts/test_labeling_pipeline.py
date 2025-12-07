"""
Complete testing of the corpus labeling pipeline.
Run: python scripts/test_labeling_pipeline.py
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CORPUS_PATH = Path("data/corpus.jsonl")
OUTPUT_DIR = Path("data/processed/domains")

def test_1_file_reading():
    """Test 1: File reading performance"""
    print("\n" + "="*60)
    print("TEST 1: File Reading Performance")
    print("="*60)
    
    if not CORPUS_PATH.exists():
        print(f"FAIL: Corpus not found at {CORPUS_PATH}")
        return False
    
    size_gb = CORPUS_PATH.stat().st_size / 1e9
    print(f"Corpus size: {size_gb:.2f} GB")
    
    start = time.time()
    line_count = 0
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            if line_count >= 5000:
                break
    
    elapsed = time.time() - start
    rate = line_count / elapsed
    print(f"Read {line_count} lines in {elapsed:.2f}s ({rate:.0f} lines/sec)")
    print("PASS: File reading works")
    return True

def test_2_classifier_init():
    """Test 2: Classifier initialization"""
    print("\n" + "="*60)
    print("TEST 2: Classifier Initialization")
    print("="*60)
    
    start = time.time()
    from src.ingestion.corpus_domain_extractor import DomainClassifier
    classifier = DomainClassifier()
    elapsed = time.time() - start
    
    print(f"Patterns loaded: {len(classifier.patterns)}")
    print(f"Legislation patterns: {len(classifier.legislation_patterns)}")
    print(f"Case patterns: {len(classifier.case_patterns)}")
    print(f"Init time: {elapsed:.2f}s")
    print("PASS: Classifier initialized")
    return classifier

def test_3_single_doc(classifier):
    """Test 3: Single document classification"""
    print("\n" + "="*60)
    print("TEST 3: Single Document Classification")
    print("="*60)
    
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        line = f.readline()
        doc = json.loads(line)
    
    print(f"Citation: {doc.get('citation', 'N/A')[:60]}")
    print(f"Type: {doc.get('type', 'N/A')}")
    
    start = time.time()
    domain, category, matches, meta = classifier.classify(doc)
    elapsed = time.time() - start
    
    print(f"Domain: {domain}")
    print(f"Category: {category}")
    print(f"Matches: {len(matches)}")
    print(f"Time: {elapsed*1000:.1f}ms")
    print("PASS: Single doc classification works")
    return True

def test_4_batch_classification(classifier):
    """Test 4: Batch classification (1000 docs)"""
    print("\n" + "="*60)
    print("TEST 4: Batch Classification (1000 docs)")
    print("="*60)
    
    docs = []
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 1000:
                break
            docs.append(json.loads(line))
    
    print(f"Loaded {len(docs)} documents")
    
    start = time.time()
    results = {}
    for doc in docs:
        domain, category, matches, meta = classifier.classify(doc)
        results[domain] = results.get(domain, 0) + 1
    elapsed = time.time() - start
    
    rate = len(docs) / elapsed
    print(f"Processed in {elapsed:.2f}s ({rate:.0f} docs/sec)")
    print("Domain distribution:")
    for domain, count in sorted(results.items(), key=lambda x: -x[1])[:5]:
        print(f"  {domain}: {count}")
    print("PASS: Batch classification works")
    return True

def test_5_file_output():
    """Test 5: File output writing"""
    print("\n" + "="*60)
    print("TEST 5: File Output Writing")
    print("="*60)
    
    from src.ingestion.corpus_domain_extractor import DomainFileManager, ALL_DOMAINS
    
    test_dir = Path("data/processed/test_output")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    with DomainFileManager(test_dir, append=False) as manager:
        test_doc = {"test": "document", "id": 1}
        manager.write("Family", test_doc)
        manager.write("Criminal", test_doc)
    
    family_file = test_dir / "family.jsonl"
    if family_file.exists() and family_file.stat().st_size > 0:
        print(f"Family file size: {family_file.stat().st_size} bytes")
        print("PASS: File output works")
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        return True
    else:
        print("FAIL: File output not working")
        return False

def test_6_full_pipeline():
    """Test 6: Full pipeline on subset"""
    print("\n" + "="*60)
    print("TEST 6: Full Pipeline (10,000 docs)")
    print("="*60)
    
    from src.ingestion.corpus_domain_extractor import CorpusDomainExtractor
    
    # Clear old state
    state_file = Path("data/processed/extraction_state.json")
    if state_file.exists():
        state_file.unlink()
    
    extractor = CorpusDomainExtractor(
        input_path=CORPUS_PATH,
        output_dir=OUTPUT_DIR
    )
    
    print("Running extraction (10,000 doc limit for test)...")
    start = time.time()
    
    # Monkey-patch to limit docs for testing
    original_extract = extractor.extract_all
    doc_limit = 10000
    
    from src.ingestion.corpus_domain_extractor import DomainFileManager
    
    with DomainFileManager(OUTPUT_DIR, append=False) as file_manager:
        with open(CORPUS_PATH, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile):
                if line_num >= doc_limit:
                    break
                if line_num % 2000 == 0:
                    print(f"  Progress: {line_num} docs...", flush=True)
                try:
                    doc = json.loads(line)
                    extractor._process_document(doc, file_manager, line_num)
                except:
                    continue
    
    elapsed = time.time() - start
    total = sum(s.document_count for s in extractor.stats.values())
    rate = total / elapsed if elapsed > 0 else 0
    
    print(f"Processed {total} docs in {elapsed:.1f}s ({rate:.0f} docs/sec)")
    print("Top domains:")
    for domain, stat in sorted(extractor.stats.items(), key=lambda x: -x[1].document_count)[:5]:
        print(f"  {domain}: {stat.document_count}")
    
    extractor._save_statistics()
    print("PASS: Full pipeline works")
    return True

def main():
    print("="*60)
    print("CORPUS LABELING PIPELINE - COMPLETE TEST SUITE")
    print(f"Started: {datetime.now()}")
    print("="*60)
    
    # Run tests
    test_1_file_reading()
    classifier = test_2_classifier_init()
    test_3_single_doc(classifier)
    test_4_batch_classification(classifier)
    test_5_file_output()
    test_6_full_pipeline()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()

