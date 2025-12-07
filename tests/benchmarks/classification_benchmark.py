"""
Classification Benchmark Suite for Australian Legal Corpus Classification System

This benchmark suite measures:
- Classification speed (documents per second)
- Memory usage during classification
- Throughput under load
- Comparison between old and new classifier (if available)
- Performance across different document types
- Scalability with document length
"""

import pytest
import time
import sys
import json
import gc
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from statistics import mean, median, stdev

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.multi_domain_classifier import EnhancedDomainClassifier

# Try to import memory_profiler if available
try:
    from memory_profiler import memory_usage
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False
    print("Warning: memory_profiler not available. Install with: pip install memory-profiler")


# ============================================================================
# BENCHMARK DATA STRUCTURES
# ============================================================================

@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""
    name: str
    total_documents: int
    total_time: float
    docs_per_second: float
    avg_time_per_doc: float
    median_time_per_doc: float
    std_dev: float
    memory_mb: float = 0.0
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'total_documents': self.total_documents,
            'total_time_seconds': round(self.total_time, 3),
            'docs_per_second': round(self.docs_per_second, 2),
            'avg_time_per_doc_ms': round(self.avg_time_per_doc * 1000, 2),
            'median_time_per_doc_ms': round(self.median_time_per_doc * 1000, 2),
            'std_dev_ms': round(self.std_dev * 1000, 2),
            'memory_mb': round(self.memory_mb, 2),
            'metadata': self.metadata or {},
        }


# ============================================================================
# SAMPLE DOCUMENT GENERATORS
# ============================================================================

def generate_short_document(doc_id: int) -> Dict[str, Any]:
    """Generate a short legal document (~500 words)."""
    return {
        'id': f'short_{doc_id}',
        'citation': f'[2023] NSWSC {doc_id}',
        'type': 'case_law',
        'text': f'''
        SUPREME COURT - CIVIL PROCEDURE

        The plaintiff seeks summary judgment pursuant to r 13.1 of the
        Uniform Civil Procedure Rules 2005 (NSW).

        The defendant has failed to file a defence within the required time.
        Under r 16.2, the plaintiff may apply for default judgment.

        The claim is for breach of contract. The plaintiff alleges that the
        defendant failed to deliver goods pursuant to a written agreement
        dated 15 January 2023. The contract price was $50,000.

        The defendant was served with the statement of claim on 20 February 2023.
        No defence has been filed. The plaintiff has provided evidence of the
        contract and breach.

        Cases cited:
        General Steel Industries Inc v Commissioner for Railways (NSW) (1964) 112 CLR 125

        Order: Summary judgment for the plaintiff in the sum of $50,000 plus costs.
        '''
    }


def generate_medium_document(doc_id: int) -> Dict[str, Any]:
    """Generate a medium-length legal document (~2000 words)."""
    return {
        'id': f'medium_{doc_id}',
        'citation': f'R v Johnson [{2020 + (doc_id % 5)}] NSWCCA {doc_id}',
        'type': 'case_law',
        'text': f'''
        CRIMINAL LAW - APPEAL AGAINST SENTENCE - ARMED ROBBERY

        The appellant was convicted after trial of armed robbery contrary to
        s 97(1) of the Crimes Act 1900 (NSW). The sentencing judge imposed
        a sentence of 8 years imprisonment with a non-parole period of 5 years.

        GROUNDS OF APPEAL

        The appellant appeals on three grounds:
        1. The sentence was manifestly excessive
        2. The sentencing judge erred in finding limited prospects of rehabilitation
        3. Insufficient weight given to subjective factors

        FACTS

        On 15 March 2022, the appellant entered a convenience store armed with
        a knife. He demanded money from the cashier, threatening violence if
        his demands were not met. The cashier handed over approximately $800
        in cash. The appellant fled the scene but was arrested two hours later
        following a police pursuit.

        OBJECTIVE SERIOUSNESS

        Armed robbery is a serious offence. The maximum penalty is 20 years
        imprisonment. The use of a weapon significantly increases the objective
        seriousness. The sentencing judge found the offence to be in the
        mid-range of objective seriousness.

        The factors increasing seriousness were:
        - Use of a knife as a weapon
        - Significant threat of violence
        - Planning and premeditation
        - Commission while on bail for another offence

        SUBJECTIVE FACTORS

        The appellant was 28 years old at the time of the offence. He has a
        criminal record including:
        - 2018: Assault occasioning actual bodily harm - 12 months imprisonment
        - 2020: Larceny - 6 months imprisonment suspended
        - 2021: Drug possession - fine

        The appellant had a difficult childhood marked by domestic violence
        and substance abuse in the family home. He left school at age 15 and
        has had limited employment history. At the time of the offence, he was
        addicted to methamphetamine.

        SENTENCING PRINCIPLES

        Section 21A of the Crimes (Sentencing Procedure) Act 1999 (NSW) requires
        consideration of aggravating and mitigating factors.

        Aggravating factors under s 21A(2):
        (a) Actual violence threatened
        (c) Use of weapon
        (e) Offence committed while on conditional liberty (bail)
        (j) Record of previous convictions

        Mitigating factors under s 21A(3):
        (c) Injury, illness or disability of the offender
        (f) Plea of guilty (not applicable - convicted after trial)
        (g) Assistance to authorities (not applicable)

        CASE LAW

        The High Court in Muldrock v The Queen (2011) 244 CLR 120 held that
        the sentencing judge must not give undue emphasis to numerical
        guidelines but must have regard to all circumstances.

        In Markarian v The Queen (2005) 228 CLR 357, the High Court emphasized
        the importance of instinctive synthesis in sentencing.

        Recent decisions of this Court have indicated that sentences for armed
        robbery should reflect:
        - General deterrence
        - Personal deterrence
        - Protection of the community
        - Denunciation of the conduct

        REHABILITATION

        The sentencing judge found that the appellant had limited prospects
        of rehabilitation due to his ongoing drug addiction and criminal history.
        The appellant contests this finding, pointing to his recent engagement
        with drug treatment programs while in custody.

        The psychologist's report indicates that with appropriate treatment
        and support, the appellant could make progress towards rehabilitation.
        However, the report also notes the significant challenges given the
        long-standing nature of the addiction.

        ANALYSIS

        Ground 1: Manifest excess

        A sentence is manifestly excessive if it falls outside the range of
        sentences that could reasonably be imposed. The question is whether
        the sentence is unreasonable or plainly unjust.

        Comparable cases:
        - R v Smith [2020] NSWCCA 50: 7 years for similar armed robbery
        - R v Williams [2021] NSWCCA 89: 9 years for aggravated armed robbery
        - R v Brown [2019] NSWCCA 120: 6 years for armed robbery (guilty plea)

        The sentence of 8 years falls within the range for this type of offence.
        While at the higher end, it is not manifestly excessive given the
        aggravating factors, particularly the commission while on bail.

        Ground 2: Rehabilitation prospects

        The sentencing judge was entitled to be cautious about rehabilitation
        prospects given the criminal history and ongoing addiction. However,
        the judge should have given more weight to the recent engagement with
        treatment programs.

        Ground 3: Subjective factors

        The appellant's difficult background and addiction should be given
        appropriate weight. However, these factors do not outweigh the serious
        objective circumstances and the need for general deterrence.

        CONCLUSION

        While the sentence is stern, it is not outside the range that could
        reasonably be imposed. The sentencing judge properly applied the
        sentencing principles and gave appropriate weight to all factors.

        ORDER

        The appeal is dismissed. The sentence imposed is affirmed.
        ''' * (1 + doc_id % 2)  # Vary length slightly
    }


def generate_long_document(doc_id: int) -> Dict[str, Any]:
    """Generate a long legal document (~5000 words)."""
    medium = generate_medium_document(doc_id)
    # Extend the medium document
    medium['id'] = f'long_{doc_id}'
    medium['text'] = medium['text'] * 3  # Triple the length
    return medium


def generate_legislation_document(doc_id: int) -> Dict[str, Any]:
    """Generate a legislation document."""
    return {
        'id': f'legislation_{doc_id}',
        'citation': f'Test Act {2000 + doc_id} (Cth)',
        'type': 'primary_legislation',
        'text': f'''
        Test Act {2000 + doc_id}

        An Act relating to the regulation of legal matters and for related purposes.

        PART 1 - PRELIMINARY

        Section 1 - Short title
        This Act may be cited as the Test Act {2000 + doc_id}.

        Section 2 - Commencement
        This Act commences on the day after it receives Royal Assent.

        Section 3 - Objects
        The objects of this Act are:
        (a) to provide a framework for regulation
        (b) to promote compliance with legal standards
        (c) to protect the interests of affected persons

        Section 4 - Definitions
        In this Act:
        "affected person" means a person to whom this Act applies
        "authorised officer" means an officer authorised under section 20
        "Commonwealth" means the Commonwealth of Australia
        "regulations" means regulations made under this Act

        PART 2 - MAIN PROVISIONS

        Section 10 - Application of Act
        (1) This Act applies to all persons within Australia.
        (2) This Act applies to acts done outside Australia in specified circumstances.
        (3) The Minister may by legislative instrument exempt persons from this Act.

        Section 11 - General obligations
        (1) A person must not engage in prohibited conduct.
        (2) A person must comply with all requirements under this Act.
        (3) Failure to comply is an offence punishable by fine or imprisonment.

        Section 12 - Powers of authorised officers
        (1) An authorised officer may enter premises for compliance purposes.
        (2) An authorised officer may require production of documents.
        (3) An authorised officer may interview persons.

        PART 3 - ENFORCEMENT

        Section 20 - Penalties
        (1) A person who contravenes section 11 is liable to a fine not exceeding
            100 penalty units.
        (2) For serious contraventions, imprisonment for up to 2 years may be imposed.

        Section 21 - Civil penalties
        The Federal Court may order a person to pay a civil penalty for contraventions.
        ''' * (1 + doc_id % 2)
    }


# ============================================================================
# BENCHMARK RUNNERS
# ============================================================================

class ClassificationBenchmark:
    """Main benchmark runner."""

    def __init__(self):
        """Initialize benchmark."""
        self.classifier = None
        self.results: List[BenchmarkResult] = []

    def setup(self):
        """Set up classifier for benchmarking."""
        # Force garbage collection before starting
        gc.collect()

        # Initialize classifier
        self.classifier = EnhancedDomainClassifier()

    def teardown(self):
        """Clean up after benchmarking."""
        self.classifier = None
        gc.collect()

    def run_classification_batch(self, documents: List[Dict[str, Any]],
                                 name: str) -> BenchmarkResult:
        """
        Run classification on a batch of documents and measure performance.

        Args:
            documents: List of documents to classify
            name: Name of this benchmark run

        Returns:
            BenchmarkResult with timing and performance metrics
        """
        times = []
        memory_before = 0
        memory_after = 0

        # Measure memory if available
        if MEMORY_PROFILER_AVAILABLE:
            memory_before = memory_usage()[0]

        # Start timing
        start_time = time.time()

        # Classify each document
        for doc in documents:
            doc_start = time.time()
            _ = self.classifier.classify(doc)
            doc_end = time.time()
            times.append(doc_end - doc_start)

        # End timing
        end_time = time.time()

        # Measure memory after
        if MEMORY_PROFILER_AVAILABLE:
            memory_after = memory_usage()[0]
            memory_delta = memory_after - memory_before
        else:
            memory_delta = 0.0

        # Calculate metrics
        total_time = end_time - start_time
        total_docs = len(documents)
        docs_per_second = total_docs / total_time if total_time > 0 else 0
        avg_time = mean(times) if times else 0
        median_time = median(times) if times else 0
        std_dev_time = stdev(times) if len(times) > 1 else 0

        result = BenchmarkResult(
            name=name,
            total_documents=total_docs,
            total_time=total_time,
            docs_per_second=docs_per_second,
            avg_time_per_doc=avg_time,
            median_time_per_doc=median_time,
            std_dev=std_dev_time,
            memory_mb=memory_delta,
        )

        self.results.append(result)
        return result

    def print_results(self):
        """Print all benchmark results."""
        print("\n" + "=" * 80)
        print("CLASSIFICATION BENCHMARK RESULTS")
        print("=" * 80)

        for result in self.results:
            print(f"\n{result.name}")
            print("-" * 80)
            print(f"  Total documents:      {result.total_documents:,}")
            print(f"  Total time:           {result.total_time:.3f} seconds")
            print(f"  Throughput:           {result.docs_per_second:.2f} docs/sec")
            print(f"  Avg time per doc:     {result.avg_time_per_doc * 1000:.2f} ms")
            print(f"  Median time per doc:  {result.median_time_per_doc * 1000:.2f} ms")
            print(f"  Std deviation:        {result.std_dev * 1000:.2f} ms")
            if result.memory_mb > 0:
                print(f"  Memory delta:         {result.memory_mb:.2f} MB")

        print("\n" + "=" * 80)

    def save_results(self, filepath: Path):
        """Save results to JSON file."""
        results_data = {
            'benchmark_run': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': [r.to_dict() for r in self.results],
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)

        print(f"\nResults saved to: {filepath}")


# ============================================================================
# PYTEST BENCHMARK TESTS
# ============================================================================

@pytest.fixture(scope='module')
def benchmark_runner():
    """Create benchmark runner for tests."""
    runner = ClassificationBenchmark()
    runner.setup()
    yield runner
    runner.teardown()


class TestClassificationSpeed:
    """Test classification speed across different scenarios."""

    def test_short_documents_speed(self, benchmark_runner):
        """Benchmark classification of short documents."""
        docs = [generate_short_document(i) for i in range(100)]

        result = benchmark_runner.run_classification_batch(
            docs, "Short Documents (100 docs, ~500 words each)"
        )

        # Assertions - adjust based on expected performance
        assert result.docs_per_second > 10, "Classification too slow for short docs"
        assert result.avg_time_per_doc < 1.0, "Average time too high"

    def test_medium_documents_speed(self, benchmark_runner):
        """Benchmark classification of medium documents."""
        docs = [generate_medium_document(i) for i in range(50)]

        result = benchmark_runner.run_classification_batch(
            docs, "Medium Documents (50 docs, ~2000 words each)"
        )

        # Assertions
        assert result.docs_per_second > 5, "Classification too slow for medium docs"
        assert result.avg_time_per_doc < 2.0, "Average time too high"

    def test_long_documents_speed(self, benchmark_runner):
        """Benchmark classification of long documents."""
        docs = [generate_long_document(i) for i in range(20)]

        result = benchmark_runner.run_classification_batch(
            docs, "Long Documents (20 docs, ~5000 words each)"
        )

        # Assertions
        assert result.docs_per_second > 2, "Classification too slow for long docs"
        assert result.avg_time_per_doc < 5.0, "Average time too high"

    def test_legislation_documents_speed(self, benchmark_runner):
        """Benchmark classification of legislation documents."""
        docs = [generate_legislation_document(i) for i in range(50)]

        result = benchmark_runner.run_classification_batch(
            docs, "Legislation Documents (50 docs)"
        )

        # Assertions
        assert result.docs_per_second > 10, "Classification too slow for legislation"

    def test_mixed_documents_speed(self, benchmark_runner):
        """Benchmark classification of mixed document types."""
        docs = []
        for i in range(25):
            docs.append(generate_short_document(i))
            docs.append(generate_medium_document(i))

        result = benchmark_runner.run_classification_batch(
            docs, "Mixed Documents (50 docs, various lengths)"
        )

        # Assertions
        assert result.docs_per_second > 8, "Classification too slow for mixed docs"


class TestClassificationThroughput:
    """Test throughput under load."""

    def test_batch_100_documents(self, benchmark_runner):
        """Test throughput with 100 documents."""
        docs = [generate_short_document(i) for i in range(100)]

        result = benchmark_runner.run_classification_batch(
            docs, "Batch Throughput - 100 documents"
        )

        assert result.total_time < 30, "Batch processing too slow"

    def test_batch_500_documents(self, benchmark_runner):
        """Test throughput with 500 documents."""
        docs = [generate_short_document(i) for i in range(500)]

        result = benchmark_runner.run_classification_batch(
            docs, "Batch Throughput - 500 documents"
        )

        assert result.total_time < 150, "Large batch processing too slow"


class TestClassificationConsistency:
    """Test consistency of classification performance."""

    def test_repeated_classification_same_document(self, benchmark_runner):
        """Test performance is consistent when classifying same document repeatedly."""
        doc = generate_medium_document(1)
        docs = [doc] * 50  # Same document 50 times

        result = benchmark_runner.run_classification_batch(
            docs, "Repeated Classification - Same Document 50x"
        )

        # Standard deviation should be low for same document
        assert result.std_dev < result.avg_time_per_doc * 0.3, \
            "Performance too inconsistent"

    def test_variance_across_similar_documents(self, benchmark_runner):
        """Test variance when classifying similar documents."""
        docs = [generate_medium_document(i) for i in range(50)]

        result = benchmark_runner.run_classification_batch(
            docs, "Variance Test - 50 Similar Documents"
        )

        # Coefficient of variation should be reasonable
        cv = result.std_dev / result.avg_time_per_doc if result.avg_time_per_doc > 0 else 0
        assert cv < 0.5, "Too much variance in classification time"


class TestMemoryUsage:
    """Test memory usage during classification."""

    @pytest.mark.skipif(not MEMORY_PROFILER_AVAILABLE,
                       reason="memory_profiler not installed")
    def test_memory_usage_batch(self, benchmark_runner):
        """Test memory usage during batch classification."""
        docs = [generate_medium_document(i) for i in range(100)]

        result = benchmark_runner.run_classification_batch(
            docs, "Memory Usage Test - 100 Documents"
        )

        # Memory delta should be reasonable
        # Adjust threshold based on expected memory usage
        assert result.memory_mb < 500, "Memory usage too high"


# ============================================================================
# MANUAL BENCHMARK RUNNER (for standalone execution)
# ============================================================================

def run_all_benchmarks():
    """Run all benchmarks and save results."""
    runner = ClassificationBenchmark()
    runner.setup()

    try:
        print("\nRunning classification benchmarks...")
        print("This may take several minutes...\n")

        # Test 1: Short documents
        print("Benchmark 1/8: Short documents (100 docs)")
        docs = [generate_short_document(i) for i in range(100)]
        runner.run_classification_batch(docs, "Short Documents (100 docs, ~500 words)")

        # Test 2: Medium documents
        print("Benchmark 2/8: Medium documents (50 docs)")
        docs = [generate_medium_document(i) for i in range(50)]
        runner.run_classification_batch(docs, "Medium Documents (50 docs, ~2000 words)")

        # Test 3: Long documents
        print("Benchmark 3/8: Long documents (20 docs)")
        docs = [generate_long_document(i) for i in range(20)]
        runner.run_classification_batch(docs, "Long Documents (20 docs, ~5000 words)")

        # Test 4: Legislation
        print("Benchmark 4/8: Legislation documents (50 docs)")
        docs = [generate_legislation_document(i) for i in range(50)]
        runner.run_classification_batch(docs, "Legislation Documents (50 docs)")

        # Test 5: Mixed
        print("Benchmark 5/8: Mixed documents (100 docs)")
        docs = []
        for i in range(25):
            docs.append(generate_short_document(i))
            docs.append(generate_medium_document(i))
            docs.append(generate_legislation_document(i))
        runner.run_classification_batch(docs, "Mixed Documents (75 docs)")

        # Test 6: Large batch
        print("Benchmark 6/8: Large batch (500 docs)")
        docs = [generate_short_document(i) for i in range(500)]
        runner.run_classification_batch(docs, "Large Batch (500 short docs)")

        # Test 7: Consistency
        print("Benchmark 7/8: Consistency test")
        doc = generate_medium_document(1)
        docs = [doc] * 100
        runner.run_classification_batch(docs, "Consistency Test (same doc 100x)")

        # Test 8: Scalability
        print("Benchmark 8/8: Scalability test")
        docs = [generate_medium_document(i) for i in range(200)]
        runner.run_classification_batch(docs, "Scalability Test (200 medium docs)")

        # Print and save results
        runner.print_results()

        output_dir = Path(__file__).parent
        output_file = output_dir / 'benchmark_results.json'
        runner.save_results(output_file)

    finally:
        runner.teardown()


if __name__ == '__main__':
    # Run benchmarks if executed directly
    run_all_benchmarks()
