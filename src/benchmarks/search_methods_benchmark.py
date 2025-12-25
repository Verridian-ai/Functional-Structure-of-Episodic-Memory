"""
Comprehensive Search Methods Benchmark Suite
=============================================

Scientific benchmark comparing all search methods in the Verridian AI system:
- SimpleBM25: Pure keyword-based BM25 ranking
- LegalRetriever: Citation lookup + BM25 hybrid
- GSWRetriever: Semantic actor-centric search over GSW structure
- HybridRetriever: Intelligent combination of GSW and BM25

Metrics measured:
- Accuracy: Precision, Recall, F1-Score, MRR (Mean Reciprocal Rank)
- Performance: Query latency, throughput, memory usage
- Robustness: Query variations, edge cases, domain coverage

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import sys
import time
import json
import uuid
import statistics
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import traceback

# Ensure src is in path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Graceful imports with fallbacks
SimpleBM25 = None
LegalRetriever = None
GSWRetriever = None
HybridRetriever = None
AccuracyTracker = None

try:
    from src.retrieval.retriever import SimpleBM25, LegalRetriever
except ImportError as e:
    print(f"[WARNING] Could not import retriever module: {e}")

try:
    from src.retrieval.gsw_retriever import GSWRetriever
except ImportError as e:
    print(f"[WARNING] Could not import gsw_retriever module: {e}")

try:
    from src.retrieval.hybrid_retriever import HybridRetriever
except ImportError as e:
    print(f"[WARNING] Could not import hybrid_retriever module: {e}")

try:
    from src.benchmarking.accuracy_tracker import AccuracyTracker
except ImportError as e:
    print(f"[WARNING] Could not import accuracy_tracker module: {e}")


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class BenchmarkQuery:
    """A single benchmark query with expected results."""
    query_id: str
    query_text: str
    domain: str
    category: str  # e.g., 'actor_search', 'citation_lookup', 'semantic_search'
    expected_entities: List[str]  # Expected actor/entity names
    expected_roles: List[str]  # Expected actor roles
    expected_keywords: List[str]  # Keywords that should appear in results
    difficulty: str  # 'easy', 'medium', 'hard'
    description: str


@dataclass
class QueryResult:
    """Result from a single query execution."""
    query_id: str
    method: str
    results: List[Dict[str, Any]]
    latency_ms: float
    result_count: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MethodMetrics:
    """Aggregated metrics for a search method."""
    method_name: str
    total_queries: int = 0
    total_results: int = 0

    # Accuracy metrics
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    mrr: float = 0.0  # Mean Reciprocal Rank

    # Performance metrics
    avg_latency_ms: float = 0.0
    min_latency_ms: float = float('inf')
    max_latency_ms: float = 0.0
    std_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0

    # Coverage metrics
    zero_result_queries: int = 0
    avg_result_count: float = 0.0

    # Category breakdown
    by_category: Dict[str, Dict[str, float]] = field(default_factory=dict)
    by_difficulty: Dict[str, Dict[str, float]] = field(default_factory=dict)
    by_domain: Dict[str, Dict[str, float]] = field(default_factory=dict)


@dataclass
class BenchmarkReport:
    """Complete benchmark report."""
    run_id: str
    timestamp: str
    duration_seconds: float
    total_queries: int
    methods_tested: List[str]
    method_metrics: Dict[str, MethodMetrics]
    comparison: Dict[str, Any]
    recommendations: List[str]
    raw_results: List[QueryResult] = field(default_factory=list)


# ============================================================================
# BENCHMARK QUERIES - GROUND TRUTH DATA
# ============================================================================

BENCHMARK_QUERIES: List[BenchmarkQuery] = [
    # === FAMILY LAW QUERIES ===
    BenchmarkQuery(
        query_id="FL001",
        query_text="custody arrangement for children",
        domain="family",
        category="semantic_search",
        expected_entities=["child", "children", "custody"],
        expected_roles=["child", "parent", "applicant", "respondent"],
        expected_keywords=["custody", "parenting", "child", "care"],
        difficulty="easy",
        description="Basic custody query - should match parenting-related entities"
    ),
    BenchmarkQuery(
        query_id="FL002",
        query_text="property settlement after separation",
        domain="family",
        category="semantic_search",
        expected_entities=["property", "asset", "settlement"],
        expected_roles=["applicant", "respondent"],
        expected_keywords=["property", "asset", "settlement", "division"],
        difficulty="easy",
        description="Property division query - should find asset-related results"
    ),
    BenchmarkQuery(
        query_id="FL003",
        query_text="spousal maintenance application",
        domain="family",
        category="semantic_search",
        expected_entities=["spouse", "maintenance", "application"],
        expected_roles=["applicant", "respondent", "spouse"],
        expected_keywords=["maintenance", "spouse", "support", "financial"],
        difficulty="medium",
        description="Spousal support query"
    ),
    BenchmarkQuery(
        query_id="FL004",
        query_text="intervention order domestic violence",
        domain="family",
        category="semantic_search",
        expected_entities=["intervention", "order", "violence"],
        expected_roles=["protected person", "defendant"],
        expected_keywords=["intervention", "order", "protection", "violence"],
        difficulty="medium",
        description="DVO/intervention order query"
    ),
    BenchmarkQuery(
        query_id="FL005",
        query_text="what happens to superannuation in divorce",
        domain="family",
        category="question_answering",
        expected_entities=["superannuation", "divorce"],
        expected_roles=[],
        expected_keywords=["superannuation", "super", "divorce", "split"],
        difficulty="hard",
        description="Complex question about super splitting"
    ),
    BenchmarkQuery(
        query_id="FL006",
        query_text="parenting order relocation interstate",
        domain="family",
        category="semantic_search",
        expected_entities=["parenting", "relocation"],
        expected_roles=["parent", "child"],
        expected_keywords=["relocation", "move", "interstate", "parenting"],
        difficulty="hard",
        description="Complex parenting scenario"
    ),

    # === ROLE-BASED QUERIES ===
    BenchmarkQuery(
        query_id="RB001",
        query_text="find all applicants",
        domain="family",
        category="role_search",
        expected_entities=[],
        expected_roles=["applicant"],
        expected_keywords=["applicant"],
        difficulty="easy",
        description="Role-based search for applicants"
    ),
    BenchmarkQuery(
        query_id="RB002",
        query_text="who is the respondent",
        domain="family",
        category="role_search",
        expected_entities=[],
        expected_roles=["respondent"],
        expected_keywords=["respondent"],
        difficulty="easy",
        description="Role-based search for respondents"
    ),
    BenchmarkQuery(
        query_id="RB003",
        query_text="children involved in case",
        domain="family",
        category="role_search",
        expected_entities=["child", "children"],
        expected_roles=["child"],
        expected_keywords=["child", "children"],
        difficulty="medium",
        description="Find children in cases"
    ),

    # === STATE-BASED QUERIES ===
    BenchmarkQuery(
        query_id="SB001",
        query_text="parties who are separated",
        domain="family",
        category="state_search",
        expected_entities=["separated"],
        expected_roles=[],
        expected_keywords=["separated", "separation"],
        difficulty="medium",
        description="State-based search for separated parties"
    ),
    BenchmarkQuery(
        query_id="SB002",
        query_text="divorced couples property",
        domain="family",
        category="state_search",
        expected_entities=["divorced", "property"],
        expected_roles=[],
        expected_keywords=["divorced", "divorce", "property"],
        difficulty="medium",
        description="Divorced parties with property"
    ),

    # === TEMPORAL QUERIES ===
    BenchmarkQuery(
        query_id="TQ001",
        query_text="cases from 2023",
        domain="family",
        category="temporal_search",
        expected_entities=["2023"],
        expected_roles=[],
        expected_keywords=["2023"],
        difficulty="medium",
        description="Temporal filter query"
    ),
    BenchmarkQuery(
        query_id="TQ002",
        query_text="orders made in January",
        domain="family",
        category="temporal_search",
        expected_entities=["January", "order"],
        expected_roles=[],
        expected_keywords=["January", "order"],
        difficulty="hard",
        description="Specific temporal query"
    ),

    # === NAMED ENTITY QUERIES ===
    BenchmarkQuery(
        query_id="NE001",
        query_text="John Smith parenting case",
        domain="family",
        category="entity_search",
        expected_entities=["John Smith"],
        expected_roles=[],
        expected_keywords=["John", "Smith", "parenting"],
        difficulty="easy",
        description="Named entity search"
    ),
    BenchmarkQuery(
        query_id="NE002",
        query_text="Smith v Jones property",
        domain="family",
        category="entity_search",
        expected_entities=["Smith", "Jones"],
        expected_roles=[],
        expected_keywords=["Smith", "Jones", "property"],
        difficulty="medium",
        description="Party names in adversarial format"
    ),

    # === ACTION/VERB QUERIES ===
    BenchmarkQuery(
        query_id="AV001",
        query_text="court ordered payment",
        domain="family",
        category="action_search",
        expected_entities=["court", "payment"],
        expected_roles=[],
        expected_keywords=["ordered", "payment", "court"],
        difficulty="medium",
        description="Action-based search"
    ),
    BenchmarkQuery(
        query_id="AV002",
        query_text="filed application custody",
        domain="family",
        category="action_search",
        expected_entities=["application", "custody"],
        expected_roles=[],
        expected_keywords=["filed", "application", "custody"],
        difficulty="medium",
        description="Filing action search"
    ),

    # === ADMINISTRATIVE LAW QUERIES ===
    BenchmarkQuery(
        query_id="AL001",
        query_text="tribunal review decision",
        domain="administrative",
        category="semantic_search",
        expected_entities=["tribunal", "review", "decision"],
        expected_roles=["applicant", "tribunal"],
        expected_keywords=["tribunal", "review", "decision"],
        difficulty="medium",
        description="Administrative tribunal query"
    ),
    BenchmarkQuery(
        query_id="AL002",
        query_text="migration visa appeal",
        domain="administrative",
        category="semantic_search",
        expected_entities=["migration", "visa", "appeal"],
        expected_roles=["applicant"],
        expected_keywords=["migration", "visa", "appeal", "refugee"],
        difficulty="hard",
        description="Migration tribunal appeal"
    ),

    # === TORTS QUERIES ===
    BenchmarkQuery(
        query_id="TO001",
        query_text="negligence claim damages",
        domain="torts",
        category="semantic_search",
        expected_entities=["negligence", "damages"],
        expected_roles=["plaintiff", "defendant"],
        expected_keywords=["negligence", "damages", "injury"],
        difficulty="medium",
        description="Negligence torts query"
    ),
    BenchmarkQuery(
        query_id="TO002",
        query_text="personal injury compensation",
        domain="torts",
        category="semantic_search",
        expected_entities=["injury", "compensation"],
        expected_roles=["plaintiff"],
        expected_keywords=["injury", "compensation", "personal"],
        difficulty="medium",
        description="Personal injury query"
    ),

    # === EDGE CASES ===
    BenchmarkQuery(
        query_id="EC001",
        query_text="",
        domain="family",
        category="edge_case",
        expected_entities=[],
        expected_roles=[],
        expected_keywords=[],
        difficulty="edge",
        description="Empty query - should handle gracefully"
    ),
    BenchmarkQuery(
        query_id="EC002",
        query_text="xyzzy123 nonexistent terms",
        domain="family",
        category="edge_case",
        expected_entities=[],
        expected_roles=[],
        expected_keywords=[],
        difficulty="edge",
        description="Nonsense query - should return empty or low-confidence"
    ),
    BenchmarkQuery(
        query_id="EC003",
        query_text="the a an is are",
        domain="family",
        category="edge_case",
        expected_entities=[],
        expected_roles=[],
        expected_keywords=[],
        difficulty="edge",
        description="Stopwords only - should handle gracefully"
    ),
]


# ============================================================================
# BENCHMARK RUNNER
# ============================================================================

class SearchMethodsBenchmark:
    """
    Comprehensive benchmark suite for all search methods.

    Usage:
        benchmark = SearchMethodsBenchmark(
            workspace_dir=Path("data/workspaces"),
            data_dir=Path("data")
        )
        report = benchmark.run_full_benchmark()
        benchmark.save_report(report, Path("data/benchmarks/search_benchmark_report.json"))
    """

    def __init__(
        self,
        workspace_dir: Path = None,
        data_dir: Path = None,
        tracker_db: Path = None,
        queries: List[BenchmarkQuery] = None
    ):
        """
        Initialize benchmark suite.

        Args:
            workspace_dir: Directory containing GSW workspace files
            data_dir: Directory containing corpus data
            tracker_db: Path to SQLite database for tracking
            queries: Custom benchmark queries (uses default if None)
        """
        self.workspace_dir = workspace_dir or Path("data/workspaces")
        self.data_dir = data_dir or Path("data")
        self.tracker_db = tracker_db or Path("data/benchmarks/search_benchmark.db")
        self.queries = queries or BENCHMARK_QUERIES

        # Initialize retrievers
        self.retrievers: Dict[str, Any] = {}
        self._initialize_retrievers()

        # Initialize tracker (if available)
        if AccuracyTracker is not None:
            self.tracker = AccuracyTracker(self.tracker_db)
        else:
            self.tracker = None
            print("[WARNING] AccuracyTracker not available - results will not be persisted")

        # Results storage
        self.results: List[QueryResult] = []

    def _initialize_retrievers(self) -> None:
        """Initialize all search method retrievers."""
        print("[Benchmark] Initializing retrievers...")

        # 1. SimpleBM25 (standalone)
        if SimpleBM25 is not None:
            try:
                self.bm25 = SimpleBM25()
                # We'll need to populate it with test data if available
                print("  - SimpleBM25: initialized")
            except Exception as e:
                print(f"  - SimpleBM25: FAILED ({e})")
                self.bm25 = None
        else:
            self.bm25 = None
            print("  - SimpleBM25: NOT AVAILABLE (missing dependencies)")

        # 2. LegalRetriever (BM25 + Citation)
        if LegalRetriever is not None:
            try:
                self.retrievers['legal_bm25'] = LegalRetriever(
                    data_dir=str(self.data_dir),
                    enable_vsa_validation=False  # Disable for speed
                )
                print(f"  - LegalRetriever: initialized ({self.retrievers['legal_bm25'].bm25.corpus_size} docs)")
            except Exception as e:
                print(f"  - LegalRetriever: FAILED ({e})")
                self.retrievers['legal_bm25'] = None
        else:
            self.retrievers['legal_bm25'] = None
            print("  - LegalRetriever: NOT AVAILABLE (missing dependencies)")

        # 3. GSWRetriever (Semantic)
        if GSWRetriever is not None:
            try:
                self.retrievers['gsw'] = GSWRetriever(
                    workspace_dir=self.workspace_dir
                )
                stats = self.retrievers['gsw'].get_statistics()
                print(f"  - GSWRetriever: initialized ({stats['total_actors']} actors, "
                      f"{stats['total_verbs']} verbs)")
            except Exception as e:
                print(f"  - GSWRetriever: FAILED ({e})")
                self.retrievers['gsw'] = None
        else:
            self.retrievers['gsw'] = None
            print("  - GSWRetriever: NOT AVAILABLE (missing dependencies)")

        # 4. HybridRetriever (GSW + BM25)
        if HybridRetriever is not None:
            try:
                self.retrievers['hybrid'] = HybridRetriever(
                    workspace_dir=self.workspace_dir,
                    data_dir=self.data_dir
                )
                print("  - HybridRetriever: initialized")
            except Exception as e:
                print(f"  - HybridRetriever: FAILED ({e})")
                self.retrievers['hybrid'] = None
        else:
            self.retrievers['hybrid'] = None
            print("  - HybridRetriever: NOT AVAILABLE (missing dependencies)")

        # 5. HybridRetriever with blending
        if HybridRetriever is not None:
            try:
                self.retrievers['hybrid_blend'] = HybridRetriever(
                    workspace_dir=self.workspace_dir,
                    data_dir=self.data_dir,
                    blend_results=True
                )
                print("  - HybridRetriever (blend): initialized")
            except Exception as e:
                print(f"  - HybridRetriever (blend): FAILED ({e})")
                self.retrievers['hybrid_blend'] = None
        else:
            self.retrievers['hybrid_blend'] = None
            print("  - HybridRetriever (blend): NOT AVAILABLE (missing dependencies)")

        print("[Benchmark] Retriever initialization complete")

    def _execute_query(
        self,
        method: str,
        query: BenchmarkQuery,
        top_k: int = 5
    ) -> QueryResult:
        """
        Execute a single query against a specific method.

        Args:
            method: Name of the retrieval method
            query: Benchmark query to execute
            top_k: Number of results to retrieve

        Returns:
            QueryResult with results and timing
        """
        retriever = self.retrievers.get(method)

        if retriever is None:
            return QueryResult(
                query_id=query.query_id,
                method=method,
                results=[],
                latency_ms=0.0,
                result_count=0
            )

        # Handle empty query edge case
        if not query.query_text.strip():
            return QueryResult(
                query_id=query.query_id,
                method=method,
                results=[],
                latency_ms=0.0,
                result_count=0
            )

        start_time = time.perf_counter()

        try:
            if method == 'legal_bm25':
                results = retriever.search(query.query_text, top_k=top_k)
            elif method == 'gsw':
                results = retriever.retrieve(
                    query.query_text,
                    top_k=top_k,
                    domain=query.domain if query.domain in retriever.workspaces else None
                )
            elif method in ('hybrid', 'hybrid_blend'):
                results = retriever.retrieve(
                    query.query_text,
                    top_k=top_k,
                    mode='auto',
                    domain=query.domain if query.domain in retriever.gsw_retriever.workspaces else None
                )
            else:
                results = []

        except Exception as e:
            print(f"    [ERROR] {method} failed on query {query.query_id}: {e}")
            results = []

        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000

        return QueryResult(
            query_id=query.query_id,
            method=method,
            results=results,
            latency_ms=latency_ms,
            result_count=len(results)
        )

    def _calculate_precision(
        self,
        result: QueryResult,
        query: BenchmarkQuery
    ) -> float:
        """
        Calculate precision for a query result.

        Precision = (relevant results found) / (total results returned)

        A result is considered relevant if it contains any expected entity,
        role, or keyword.
        """
        if not result.results:
            return 0.0

        expected_set = set(
            [e.lower() for e in query.expected_entities] +
            [r.lower() for r in query.expected_roles] +
            [k.lower() for k in query.expected_keywords]
        )

        if not expected_set:
            # Edge case queries - if we return empty, that's correct
            return 1.0 if not result.results else 0.5

        relevant_count = 0

        for res in result.results:
            # Build text to search in
            text_to_check = ""

            if 'name' in res:
                text_to_check += res['name'].lower() + " "
            if 'title' in res:
                text_to_check += res['title'].lower() + " "
            if 'roles' in res and res['roles']:
                text_to_check += " ".join([r.lower() for r in res['roles']]) + " "
            if 'verb' in res:
                text_to_check += res['verb'].lower() + " "
            if 'text_preview' in res:
                text_to_check += res['text_preview'].lower() + " "
            if 'question_text' in res:
                text_to_check += res['question_text'].lower() + " "
            if 'answer_text' in res and res['answer_text']:
                text_to_check += res['answer_text'].lower() + " "
            if 'states' in res and res['states']:
                for state in res['states']:
                    text_to_check += f"{state.get('name', '')} {state.get('value', '')}".lower() + " "

            # Check for any match
            for expected in expected_set:
                if expected in text_to_check:
                    relevant_count += 1
                    break

        return relevant_count / len(result.results)

    def _calculate_recall(
        self,
        result: QueryResult,
        query: BenchmarkQuery
    ) -> float:
        """
        Calculate recall for a query result.

        Recall = (expected items found in results) / (total expected items)
        """
        expected_set = set(
            [e.lower() for e in query.expected_entities] +
            [r.lower() for r in query.expected_roles] +
            [k.lower() for k in query.expected_keywords]
        )

        if not expected_set:
            return 1.0  # No expected items = perfect recall

        if not result.results:
            return 0.0

        # Build combined text from all results
        combined_text = ""
        for res in result.results:
            if 'name' in res:
                combined_text += res['name'].lower() + " "
            if 'title' in res:
                combined_text += res['title'].lower() + " "
            if 'roles' in res and res['roles']:
                combined_text += " ".join([r.lower() for r in res['roles']]) + " "
            if 'verb' in res:
                combined_text += res['verb'].lower() + " "
            if 'text_preview' in res:
                combined_text += res['text_preview'].lower() + " "
            if 'question_text' in res:
                combined_text += res['question_text'].lower() + " "
            if 'answer_text' in res and res['answer_text']:
                combined_text += res['answer_text'].lower() + " "

        # Count how many expected items were found
        found_count = sum(1 for exp in expected_set if exp in combined_text)

        return found_count / len(expected_set)

    def _calculate_mrr(
        self,
        result: QueryResult,
        query: BenchmarkQuery
    ) -> float:
        """
        Calculate Mean Reciprocal Rank.

        MRR = 1 / (rank of first relevant result)
        """
        expected_set = set(
            [e.lower() for e in query.expected_entities] +
            [r.lower() for r in query.expected_roles] +
            [k.lower() for k in query.expected_keywords]
        )

        if not expected_set:
            return 1.0  # No expectations = best case

        if not result.results:
            return 0.0

        for rank, res in enumerate(result.results, 1):
            text_to_check = ""
            if 'name' in res:
                text_to_check += res['name'].lower() + " "
            if 'title' in res:
                text_to_check += res['title'].lower() + " "
            if 'roles' in res and res['roles']:
                text_to_check += " ".join([r.lower() for r in res['roles']]) + " "
            if 'verb' in res:
                text_to_check += res['verb'].lower() + " "
            if 'text_preview' in res:
                text_to_check += res['text_preview'].lower() + " "

            for expected in expected_set:
                if expected in text_to_check:
                    return 1.0 / rank

        return 0.0  # No relevant result found

    def _aggregate_metrics(
        self,
        method: str,
        results: List[QueryResult],
        queries: List[BenchmarkQuery]
    ) -> MethodMetrics:
        """
        Aggregate metrics for a single method across all queries.
        """
        metrics = MethodMetrics(method_name=method)
        metrics.total_queries = len(results)

        precisions = []
        recalls = []
        mrrs = []
        latencies = []
        result_counts = []

        # Category/difficulty/domain breakdowns
        by_category: Dict[str, List[Tuple[float, float, float]]] = defaultdict(list)
        by_difficulty: Dict[str, List[Tuple[float, float, float]]] = defaultdict(list)
        by_domain: Dict[str, List[Tuple[float, float, float]]] = defaultdict(list)

        query_map = {q.query_id: q for q in queries}

        for result in results:
            query = query_map.get(result.query_id)
            if not query:
                continue

            # Calculate metrics for this result
            precision = self._calculate_precision(result, query)
            recall = self._calculate_recall(result, query)
            mrr = self._calculate_mrr(result, query)

            precisions.append(precision)
            recalls.append(recall)
            mrrs.append(mrr)
            latencies.append(result.latency_ms)
            result_counts.append(result.result_count)

            if result.result_count == 0:
                metrics.zero_result_queries += 1

            # Track by category
            by_category[query.category].append((precision, recall, mrr))
            by_difficulty[query.difficulty].append((precision, recall, mrr))
            by_domain[query.domain].append((precision, recall, mrr))

        # Aggregate accuracy metrics
        if precisions:
            metrics.precision = statistics.mean(precisions)
            metrics.recall = statistics.mean(recalls)
            metrics.mrr = statistics.mean(mrrs)

            # F1 Score
            if metrics.precision + metrics.recall > 0:
                metrics.f1_score = 2 * (metrics.precision * metrics.recall) / (metrics.precision + metrics.recall)

        # Aggregate performance metrics
        if latencies:
            metrics.avg_latency_ms = statistics.mean(latencies)
            metrics.min_latency_ms = min(latencies)
            metrics.max_latency_ms = max(latencies)
            metrics.total_results = sum(result_counts)
            metrics.avg_result_count = statistics.mean(result_counts)

            if len(latencies) > 1:
                metrics.std_latency_ms = statistics.stdev(latencies)

            # Percentiles
            sorted_latencies = sorted(latencies)
            n = len(sorted_latencies)
            metrics.p50_latency_ms = sorted_latencies[int(n * 0.50)]
            metrics.p95_latency_ms = sorted_latencies[min(int(n * 0.95), n - 1)]
            metrics.p99_latency_ms = sorted_latencies[min(int(n * 0.99), n - 1)]

        # Category breakdown
        for category, values in by_category.items():
            if values:
                prec_vals, rec_vals, mrr_vals = zip(*values)
                metrics.by_category[category] = {
                    'count': len(values),
                    'precision': statistics.mean(prec_vals),
                    'recall': statistics.mean(rec_vals),
                    'mrr': statistics.mean(mrr_vals)
                }

        # Difficulty breakdown
        for difficulty, values in by_difficulty.items():
            if values:
                prec_vals, rec_vals, mrr_vals = zip(*values)
                metrics.by_difficulty[difficulty] = {
                    'count': len(values),
                    'precision': statistics.mean(prec_vals),
                    'recall': statistics.mean(rec_vals),
                    'mrr': statistics.mean(mrr_vals)
                }

        # Domain breakdown
        for domain, values in by_domain.items():
            if values:
                prec_vals, rec_vals, mrr_vals = zip(*values)
                metrics.by_domain[domain] = {
                    'count': len(values),
                    'precision': statistics.mean(prec_vals),
                    'recall': statistics.mean(rec_vals),
                    'mrr': statistics.mean(mrr_vals)
                }

        return metrics

    def _generate_recommendations(
        self,
        method_metrics: Dict[str, MethodMetrics]
    ) -> List[str]:
        """Generate recommendations based on benchmark results."""
        recommendations = []

        # Find best method by F1
        best_f1_method = max(
            method_metrics.items(),
            key=lambda x: x[1].f1_score
        )[0]

        # Find fastest method
        fastest_method = min(
            method_metrics.items(),
            key=lambda x: x[1].avg_latency_ms if x[1].avg_latency_ms > 0 else float('inf')
        )[0]

        recommendations.append(
            f"Best accuracy (F1): {best_f1_method} with F1={method_metrics[best_f1_method].f1_score:.3f}"
        )
        recommendations.append(
            f"Fastest method: {fastest_method} with avg latency={method_metrics[fastest_method].avg_latency_ms:.1f}ms"
        )

        # Check for low-performing methods
        for method, metrics in method_metrics.items():
            if metrics.f1_score < 0.5:
                recommendations.append(
                    f"Warning: {method} has low F1 score ({metrics.f1_score:.3f}). "
                    f"Consider tuning or using alternative method."
                )
            if metrics.zero_result_queries > len(self.queries) * 0.2:
                recommendations.append(
                    f"Warning: {method} returned zero results for "
                    f"{metrics.zero_result_queries}/{metrics.total_queries} queries. "
                    f"Check index population."
                )

        # Compare hybrid vs individual methods
        if 'hybrid' in method_metrics and 'gsw' in method_metrics:
            gsw_f1 = method_metrics['gsw'].f1_score
            hybrid_f1 = method_metrics['hybrid'].f1_score

            if hybrid_f1 > gsw_f1:
                improvement = ((hybrid_f1 - gsw_f1) / gsw_f1 * 100) if gsw_f1 > 0 else 0
                recommendations.append(
                    f"Hybrid retriever improves F1 by {improvement:.1f}% over pure GSW"
                )
            elif gsw_f1 > hybrid_f1:
                recommendations.append(
                    "Pure GSW outperforms hybrid. Consider adjusting hybrid threshold."
                )

        return recommendations

    def run_full_benchmark(
        self,
        top_k: int = 5,
        save_raw_results: bool = True
    ) -> BenchmarkReport:
        """
        Run the complete benchmark suite.

        Args:
            top_k: Number of results per query
            save_raw_results: Whether to include raw results in report

        Returns:
            BenchmarkReport with all metrics and analysis
        """
        run_id = f"bench_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()

        print("\n" + "=" * 80)
        print("SEARCH METHODS BENCHMARK SUITE")
        print("=" * 80)
        print(f"Run ID: {run_id}")
        print(f"Queries: {len(self.queries)}")
        print(f"Methods: {list(self.retrievers.keys())}")
        print("=" * 80)

        all_results: Dict[str, List[QueryResult]] = defaultdict(list)
        methods_tested = [m for m, r in self.retrievers.items() if r is not None]

        # Run each query against each method
        total_iterations = len(self.queries) * len(methods_tested)
        iteration = 0

        for query in self.queries:
            print(f"\n[Query {query.query_id}] {query.description}")
            print(f"  Text: '{query.query_text[:50]}{'...' if len(query.query_text) > 50 else ''}'")

            for method in methods_tested:
                iteration += 1
                result = self._execute_query(method, query, top_k)
                all_results[method].append(result)

                print(f"  {method}: {result.result_count} results in {result.latency_ms:.1f}ms")

        # Aggregate metrics for each method
        print("\n" + "=" * 80)
        print("CALCULATING METRICS")
        print("=" * 80)

        method_metrics: Dict[str, MethodMetrics] = {}

        for method in methods_tested:
            print(f"\nProcessing {method}...")
            metrics = self._aggregate_metrics(method, all_results[method], self.queries)
            method_metrics[method] = metrics

            # Record to tracker (if available)
            if self.tracker is not None:
                self.tracker.record_benchmark(
                    stage='retrieval',
                    metrics={
                        f'{method}_precision': metrics.precision,
                        f'{method}_recall': metrics.recall,
                        f'{method}_f1': metrics.f1_score,
                        f'{method}_mrr': metrics.mrr,
                        f'{method}_avg_latency_ms': metrics.avg_latency_ms,
                    },
                    metadata={'run_id': run_id, 'method': method},
                    run_id=run_id
                )

        # Generate comparison
        comparison = self._generate_comparison(method_metrics)

        # Generate recommendations
        recommendations = self._generate_recommendations(method_metrics)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Flatten raw results
        raw_results = []
        if save_raw_results:
            for method, results in all_results.items():
                raw_results.extend(results)

        # Record suite run (if tracker available)
        if self.tracker is not None:
            self.tracker.record_suite_run(
                run_id=run_id,
                start_time=start_time,
                end_time=end_time,
                total_benchmarks=len(self.queries) * len(methods_tested),
                benchmarks_passed=sum(1 for m in method_metrics.values() if m.f1_score > 0.3),
                overall_score=statistics.mean([m.f1_score for m in method_metrics.values()]) if method_metrics else 0.0,
                status='completed',
                metadata={'methods': methods_tested, 'query_count': len(self.queries)}
            )

        report = BenchmarkReport(
            run_id=run_id,
            timestamp=start_time.isoformat(),
            duration_seconds=duration,
            total_queries=len(self.queries),
            methods_tested=methods_tested,
            method_metrics=method_metrics,
            comparison=comparison,
            recommendations=recommendations,
            raw_results=raw_results
        )

        return report

    def _generate_comparison(
        self,
        method_metrics: Dict[str, MethodMetrics]
    ) -> Dict[str, Any]:
        """Generate method comparison data."""
        comparison = {
            'ranking_by_f1': [],
            'ranking_by_latency': [],
            'best_by_category': {},
            'best_by_difficulty': {}
        }

        # Ranking by F1
        ranked = sorted(
            method_metrics.items(),
            key=lambda x: x[1].f1_score,
            reverse=True
        )
        comparison['ranking_by_f1'] = [
            {'method': m, 'f1': met.f1_score, 'precision': met.precision, 'recall': met.recall}
            for m, met in ranked
        ]

        # Ranking by latency
        ranked_latency = sorted(
            method_metrics.items(),
            key=lambda x: x[1].avg_latency_ms if x[1].avg_latency_ms > 0 else float('inf')
        )
        comparison['ranking_by_latency'] = [
            {'method': m, 'avg_latency_ms': met.avg_latency_ms}
            for m, met in ranked_latency
        ]

        # Best by category
        all_categories = set()
        for met in method_metrics.values():
            all_categories.update(met.by_category.keys())

        for category in all_categories:
            best_method = None
            best_f1 = -1
            for method, met in method_metrics.items():
                if category in met.by_category:
                    cat_data = met.by_category[category]
                    f1 = 2 * (cat_data['precision'] * cat_data['recall']) / (cat_data['precision'] + cat_data['recall']) if (cat_data['precision'] + cat_data['recall']) > 0 else 0
                    if f1 > best_f1:
                        best_f1 = f1
                        best_method = method
            if best_method:
                comparison['best_by_category'][category] = {
                    'method': best_method,
                    'f1': best_f1
                }

        # Best by difficulty
        all_difficulties = set()
        for met in method_metrics.values():
            all_difficulties.update(met.by_difficulty.keys())

        for difficulty in all_difficulties:
            best_method = None
            best_f1 = -1
            for method, met in method_metrics.items():
                if difficulty in met.by_difficulty:
                    diff_data = met.by_difficulty[difficulty]
                    f1 = 2 * (diff_data['precision'] * diff_data['recall']) / (diff_data['precision'] + diff_data['recall']) if (diff_data['precision'] + diff_data['recall']) > 0 else 0
                    if f1 > best_f1:
                        best_f1 = f1
                        best_method = method
            if best_method:
                comparison['best_by_difficulty'][difficulty] = {
                    'method': best_method,
                    'f1': best_f1
                }

        return comparison

    def save_report(
        self,
        report: BenchmarkReport,
        output_path: Path
    ) -> None:
        """Save benchmark report to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to serializable format
        report_dict = {
            'run_id': report.run_id,
            'timestamp': report.timestamp,
            'duration_seconds': report.duration_seconds,
            'total_queries': report.total_queries,
            'methods_tested': report.methods_tested,
            'method_metrics': {
                method: asdict(metrics)
                for method, metrics in report.method_metrics.items()
            },
            'comparison': report.comparison,
            'recommendations': report.recommendations
        }

        # Add simplified raw results (without full result objects)
        if report.raw_results:
            report_dict['raw_results_summary'] = [
                {
                    'query_id': r.query_id,
                    'method': r.method,
                    'result_count': r.result_count,
                    'latency_ms': r.latency_ms
                }
                for r in report.raw_results
            ]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, default=str)

        print(f"\nReport saved to: {output_path}")

    def print_summary(self, report: BenchmarkReport) -> None:
        """Print a formatted summary of the benchmark report."""
        print("\n" + "=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)

        print(f"\nRun ID: {report.run_id}")
        print(f"Duration: {report.duration_seconds:.2f} seconds")
        print(f"Total Queries: {report.total_queries}")
        print(f"Methods Tested: {', '.join(report.methods_tested)}")

        # Accuracy comparison table
        print("\n" + "-" * 80)
        print("ACCURACY METRICS")
        print("-" * 80)
        print(f"{'Method':<20} {'Precision':>10} {'Recall':>10} {'F1':>10} {'MRR':>10}")
        print("-" * 60)

        for method in report.methods_tested:
            metrics = report.method_metrics[method]
            print(f"{method:<20} {metrics.precision:>10.3f} {metrics.recall:>10.3f} "
                  f"{metrics.f1_score:>10.3f} {metrics.mrr:>10.3f}")

        # Performance comparison table
        print("\n" + "-" * 80)
        print("PERFORMANCE METRICS")
        print("-" * 80)
        print(f"{'Method':<20} {'Avg(ms)':>10} {'P50(ms)':>10} {'P95(ms)':>10} {'P99(ms)':>10}")
        print("-" * 60)

        for method in report.methods_tested:
            metrics = report.method_metrics[method]
            print(f"{method:<20} {metrics.avg_latency_ms:>10.1f} {metrics.p50_latency_ms:>10.1f} "
                  f"{metrics.p95_latency_ms:>10.1f} {metrics.p99_latency_ms:>10.1f}")

        # Rankings
        print("\n" + "-" * 80)
        print("RANKINGS")
        print("-" * 80)

        print("\nBy F1 Score (best to worst):")
        for i, item in enumerate(report.comparison['ranking_by_f1'], 1):
            print(f"  {i}. {item['method']}: F1={item['f1']:.3f}")

        print("\nBy Latency (fastest to slowest):")
        for i, item in enumerate(report.comparison['ranking_by_latency'], 1):
            print(f"  {i}. {item['method']}: {item['avg_latency_ms']:.1f}ms")

        # Best by category
        if report.comparison.get('best_by_category'):
            print("\nBest Method by Query Category:")
            for category, data in report.comparison['best_by_category'].items():
                print(f"  - {category}: {data['method']} (F1={data['f1']:.3f})")

        # Recommendations
        print("\n" + "-" * 80)
        print("RECOMMENDATIONS")
        print("-" * 80)
        for rec in report.recommendations:
            print(f"  * {rec}")

        print("\n" + "=" * 80)


# ============================================================================
# MAIN / CLI
# ============================================================================

def main():
    """Run the benchmark suite."""
    print("\n" + "=" * 80)
    print("VERRIDIAN AI - SEARCH METHODS BENCHMARK")
    print("=" * 80)
    print("Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory")
    print("=" * 80)

    try:
        # Initialize benchmark
        benchmark = SearchMethodsBenchmark(
            workspace_dir=Path("data/workspaces"),
            data_dir=Path("data"),
            tracker_db=Path("data/benchmarks/search_benchmark.db")
        )

        # Run benchmark
        report = benchmark.run_full_benchmark(top_k=5, save_raw_results=True)

        # Save report
        benchmark.save_report(
            report,
            Path("data/benchmarks/search_methods_benchmark_report.json")
        )

        # Print summary
        benchmark.print_summary(report)

        print("\n[SUCCESS] Benchmark completed successfully!")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Benchmark failed: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
