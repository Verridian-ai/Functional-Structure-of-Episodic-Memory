"""
Comprehensive Benchmarking (Phase 5.2)
======================================

Runs the LegalCognitiveSystem against the Gold Standard dataset.
Evaluates:
1. Success Rate (Did the agent produce an answer?)
2. Logic Validation (Did VSA correctly flag invalid premises?)
3. Efficiency (Average steps to solution)
"""

import json
import time
import numpy as np
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from src.integration.cognitive_system import LegalCognitiveSystem
from src.vsa.legal_vsa import get_vsa_service

class Benchmarker:
    def __init__(self, benchmark_file: str = 'data/benchmarks/gold_standard.json'):
        self.benchmark_file = benchmark_file
        self.system = LegalCognitiveSystem()
        self.vsa = get_vsa_service()
        
    def load_benchmarks(self) -> List[Dict]:
        with open(self.benchmark_file, 'r') as f:
            return json.load(f)
            
    def run(self):
        print(f"Starting Benchmark on {datetime.now()}...")
        tests = self.load_benchmarks()
        
        results = {
            "total": len(tests),
            "passed": 0,
            "logic_checks_correct": 0,
            "avg_steps": 0,
            "details": []
        }
        
        total_steps = 0
        
        for test in tests:
            print(f"\nRunning Test {test['id']}: {test['query']}")
            
            # 1. Run System
            start_time = time.time()
            # Mocking the gathered facts for specific logic tests since we don't have a real retriever yet
            # In a real benchmark, the system would find these itself.
            # Here we inject the test's "required_concepts" into the VSA check during the run.
            
            # To make the simulation meaningful, we override the VSA check in the system temporarily 
            # or reliance on the system's mock random walk finding the right things.
            # Let's rely on the system's agent loop but inject the concepts into the `gathered_facts` 
            # manually before the DRAFT_ANSWER step if the agent decides to draft.
            # This simulates "perfect retrieval" to test the Logic/Agency layer specifically.
            
            # We need to hook into the system process or subclass it.
            # For simplicity, we'll assume the system finds the required concepts if it searches enough.
            
            # Actually, let's just run it. The system mock "finds" "DIVORCE" and "MARRIAGE" by default in the demo.
            # We should update the System to accept "mock_findings" for deterministic testing.
            
            # Run (using the demo logic for now, which is hardcoded to be 'valid' usually)
            # To test INVALID cases, we need the system to find the INVALID concepts.
            
            # Inject mock behavior
            if "logic_validation" in str(test.get("expected_logic_validation")):
                # Force system to 'find' the required concepts
                pass 

            # Let's modify the logic check in the system on the fly for testing?
            # Or better, let's assume the 'gathered_facts' will contain `required_concepts`.
            
            # Override the random walk extraction in the system instance
            original_vsa_check = self.system.vsa.verify_no_hallucination
            
            def mock_verify(concepts):
                # Use the test's required concepts instead of the hardcoded demo ones
                return original_vsa_check(test["required_concepts"])
                
            # Monkey patch
            self.system.vsa.verify_no_hallucination = mock_verify
            
            # Execute
            output = self.system.process_query(test['query'], max_steps=5)
            
            # Restore
            self.system.vsa.verify_no_hallucination = original_vsa_check
            
            duration = time.time() - start_time
            steps = len(output['history'])
            total_steps += steps
            
            # Evaluate
            # 1. Did it finish?
            success = output['status'] == 'success'
            
            # 2. Logic Check:
            # If expected_logic_validation is FALSE, we expect the system to FAIL/RETRY or report failure.
            # Our current system retries on failure. So if it times out or fails validation, that matches "False".
            # If expected is TRUE, we expect "success".
            
            logic_correct = False
            if test['expected_logic_validation']:
                if success: logic_correct = True
            else:
                if not success or (output['status'] == 'success' and "Validation FAILED" in str(output)): 
                    # In our current implementation, if validation fails, it retries.
                    # If it eventually succeeds (by correcting), that's good.
                    # But if the premise is fundamentally flawed (Divorce without Marriage), it should never succeed.
                    # So if expected=False, result should NOT be success (or should be success with a correction).
                    if output['status'] != 'success': logic_correct = True
                    
            # Record
            res = {
                "id": test['id'],
                "success": success,
                "steps": steps,
                "duration": duration,
                "logic_correct": logic_correct
            }
            results['details'].append(res)
            
            if logic_correct: results['logic_checks_correct'] += 1
            if success and test['expected_logic_validation']: results['passed'] += 1
            elif not success and not test['expected_logic_validation']: results['passed'] += 1 # Passed the negative test
            
        results['avg_steps'] = total_steps / len(tests)
        
        print("\n=== Benchmark Summary ===")
        print(f"Total Tests: {results['total']}")
        print(f"Passed: {results['passed']}")
        print(f"Logic Accuracy: {results['logic_checks_correct']}/{results['total']}")
        print(f"Avg Steps: {results['avg_steps']:.2f}")
        
        # Write report
        with open('data/benchmarks/report.json', 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    Path('data/benchmarks').mkdir(parents=True, exist_ok=True)
    bench = Benchmarker()
    bench.run()

