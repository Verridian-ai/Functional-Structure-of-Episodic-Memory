"""
Agent Knowledge Retrieval Performance Test
==========================================

Tests the Family Law Agent's knowledge retrieval capabilities and generates
a comprehensive performance report.

Run: python tests/test_agent_performance.py
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.family_law_knowledge import FamilyLawAgent
from src.agents.gsw_tools import GSWDirectAPI, set_workspace_path
from src.gsw.workspace import WorkspaceManager


# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    query_type: str
    query_params: Dict[str, Any]
    response_time_ms: float
    result_count: int
    success: bool
    error: str = ""


@dataclass
class PerformanceReport:
    """Complete performance report."""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    workspace_path: str = ""

    # Workspace Stats
    total_actors: int = 0
    total_questions: int = 0
    total_verb_phrases: int = 0
    total_links: int = 0
    answered_questions: int = 0

    # Performance Metrics
    queries_executed: int = 0
    queries_successful: int = 0
    total_query_time_ms: float = 0.0
    avg_query_time_ms: float = 0.0
    min_query_time_ms: float = float('inf')
    max_query_time_ms: float = 0.0

    # By Query Type
    metrics_by_type: Dict[str, List[float]] = field(default_factory=dict)

    # Detailed Results
    query_results: List[QueryMetrics] = field(default_factory=list)

    # Coverage Metrics
    actors_by_type: Dict[str, int] = field(default_factory=dict)
    actors_by_role: Dict[str, int] = field(default_factory=dict)
    questions_by_type: Dict[str, int] = field(default_factory=dict)

    def add_query(self, metrics: QueryMetrics):
        """Add a query result to the report."""
        self.queries_executed += 1
        if metrics.success:
            self.queries_successful += 1

        self.total_query_time_ms += metrics.response_time_ms
        self.min_query_time_ms = min(self.min_query_time_ms, metrics.response_time_ms)
        self.max_query_time_ms = max(self.max_query_time_ms, metrics.response_time_ms)

        if metrics.query_type not in self.metrics_by_type:
            self.metrics_by_type[metrics.query_type] = []
        self.metrics_by_type[metrics.query_type].append(metrics.response_time_ms)

        self.query_results.append(metrics)

    def finalize(self):
        """Calculate final averages."""
        if self.queries_executed > 0:
            self.avg_query_time_ms = self.total_query_time_ms / self.queries_executed
        if self.min_query_time_ms == float('inf'):
            self.min_query_time_ms = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            "timestamp": self.timestamp,
            "workspace_path": self.workspace_path,
            "workspace_stats": {
                "total_actors": self.total_actors,
                "total_questions": self.total_questions,
                "total_verb_phrases": self.total_verb_phrases,
                "total_links": self.total_links,
                "answered_questions": self.answered_questions,
                "answer_rate": f"{(self.answered_questions / max(1, self.total_questions) * 100):.1f}%"
            },
            "performance_summary": {
                "queries_executed": self.queries_executed,
                "queries_successful": self.queries_successful,
                "success_rate": f"{(self.queries_successful / max(1, self.queries_executed) * 100):.1f}%",
                "total_query_time_ms": round(self.total_query_time_ms, 2),
                "avg_query_time_ms": round(self.avg_query_time_ms, 2),
                "min_query_time_ms": round(self.min_query_time_ms, 2),
                "max_query_time_ms": round(self.max_query_time_ms, 2),
            },
            "performance_by_query_type": {
                qtype: {
                    "count": len(times),
                    "avg_ms": round(sum(times) / len(times), 2),
                    "min_ms": round(min(times), 2),
                    "max_ms": round(max(times), 2),
                }
                for qtype, times in self.metrics_by_type.items()
            },
            "coverage": {
                "actors_by_type": self.actors_by_type,
                "actors_by_role": dict(list(self.actors_by_role.items())[:20]),  # Top 20
                "questions_by_type": self.questions_by_type,
            },
            "detailed_results": [
                {
                    "type": q.query_type,
                    "params": q.query_params,
                    "time_ms": round(q.response_time_ms, 2),
                    "results": q.result_count,
                    "success": q.success,
                    "error": q.error
                }
                for q in self.query_results
            ]
        }


# ============================================================================
# TEST RUNNER
# ============================================================================

class AgentPerformanceTester:
    """
    Tests the Family Law Agent's knowledge retrieval performance.
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.report = PerformanceReport(workspace_path=str(workspace_path))
        self.agent: FamilyLawAgent = None
        self.api: GSWDirectAPI = None

    def setup(self) -> bool:
        """Initialize the agent and workspace."""
        print(f"\n{'='*60}")
        print("AGENT PERFORMANCE TEST")
        print(f"{'='*60}")
        print(f"Workspace: {self.workspace_path}")

        if not self.workspace_path.exists():
            print(f"ERROR: Workspace not found at {self.workspace_path}")
            return False

        # Load agent
        print("\nLoading agent...")
        start = time.perf_counter()
        self.agent = FamilyLawAgent.load(self.workspace_path)
        load_time = (time.perf_counter() - start) * 1000
        print(f"Agent loaded in {load_time:.2f}ms")

        # Setup API
        set_workspace_path(self.workspace_path)
        self.api = GSWDirectAPI(self.workspace_path)

        # Get workspace stats
        stats = self.agent.stats
        self.report.total_actors = stats.get("total_actors", 0)
        self.report.total_questions = stats.get("total_questions", 0)
        self.report.total_verb_phrases = stats.get("total_verb_phrases", 0)
        self.report.total_links = stats.get("total_spatio_temporal_links", 0)
        self.report.answered_questions = stats.get("answered_questions", 0)

        # Coverage stats
        self.report.actors_by_type = stats.get("actors_by_type", {})
        self.report.questions_by_type = stats.get("questions_by_type", {})

        print(f"\nWorkspace Statistics:")
        print(f"  - Actors: {self.report.total_actors}")
        print(f"  - Questions: {self.report.total_questions}")
        print(f"  - Verb Phrases: {self.report.total_verb_phrases}")
        print(f"  - Spatio-Temporal Links: {self.report.total_links}")
        print(f"  - Answered Questions: {self.report.answered_questions}")

        return True

    def _timed_query(self, query_type: str, query_func, params: Dict[str, Any]) -> QueryMetrics:
        """Execute a query and measure its performance."""
        start = time.perf_counter()
        try:
            result = query_func(**params)
            elapsed_ms = (time.perf_counter() - start) * 1000

            # Determine result count
            if isinstance(result, list):
                count = len(result)
            elif isinstance(result, dict):
                count = result.get("count", len(result.get("results", [])))
            elif isinstance(result, str):
                try:
                    parsed = json.loads(result)
                    count = parsed.get("count", 0)
                except:
                    count = 1 if result else 0
            else:
                count = 1 if result else 0

            return QueryMetrics(
                query_type=query_type,
                query_params=params,
                response_time_ms=elapsed_ms,
                result_count=count,
                success=True
            )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return QueryMetrics(
                query_type=query_type,
                query_params=params,
                response_time_ms=elapsed_ms,
                result_count=0,
                success=False,
                error=str(e)
            )

    def test_find_parties(self):
        """Test party finding queries."""
        print("\n--- Testing: find_parties ---")

        # Test cases
        test_cases = [
            {"query": ""},           # All parties
            {"query": "smith"},      # Name search
            {"query": "jones"},      # Another name
            {"query": "mother"},     # Role-like search
            {"query": "XYZ"},        # Anonymized party
        ]

        for params in test_cases:
            metrics = self._timed_query(
                "find_parties",
                self.agent.find_parties,
                params
            )
            self.report.add_query(metrics)
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] query='{params.get('query', '')}' -> {metrics.result_count} results in {metrics.response_time_ms:.2f}ms")

    def test_get_actors_by_role(self):
        """Test role-based actor queries."""
        print("\n--- Testing: get_actors_by_role ---")

        roles = ["Applicant", "Respondent", "Judge", "Mother", "Father", "Party", "Court"]

        for role in roles:
            metrics = self._timed_query(
                "get_actors_by_role",
                self.agent.get_actors_by_role,
                {"role": role}
            )
            self.report.add_query(metrics)
            self.report.actors_by_role[role] = metrics.result_count
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] role='{role}' -> {metrics.result_count} actors in {metrics.response_time_ms:.2f}ms")

    def test_find_cases_by_type(self):
        """Test case type queries."""
        print("\n--- Testing: find_cases_by_type ---")

        case_types = ["parenting", "property", "divorce", "child_support", "general"]

        for case_type in case_types:
            metrics = self._timed_query(
                "find_cases_by_type",
                self.agent.find_cases_by_type,
                {"case_type": case_type}
            )
            self.report.add_query(metrics)
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] type='{case_type}' -> {metrics.result_count} questions in {metrics.response_time_ms:.2f}ms")

    def test_get_unanswered_questions(self):
        """Test unanswered question retrieval."""
        print("\n--- Testing: get_unanswered_questions ---")

        limits = [5, 10, 20, 50]

        for limit in limits:
            metrics = self._timed_query(
                "get_unanswered_questions",
                self.agent.get_unanswered_questions,
                {"limit": limit}
            )
            self.report.add_query(metrics)
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] limit={limit} -> {metrics.result_count} questions in {metrics.response_time_ms:.2f}ms")

    def test_get_context(self):
        """Test context retrieval for LLM prompts."""
        print("\n--- Testing: get_context (TOON & JSON) ---")

        # TOON format
        for max_actors in [10, 30, 50]:
            metrics = self._timed_query(
                "get_context_toon",
                self.agent.get_context_toon,
                {"max_actors": max_actors}
            )
            self.report.add_query(metrics)
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] TOON max_actors={max_actors} in {metrics.response_time_ms:.2f}ms")

        # JSON format
        for max_actors in [10, 30, 50]:
            metrics = self._timed_query(
                "get_context_json",
                self.agent.get_context_json,
                {"max_actors": max_actors}
            )
            self.report.add_query(metrics)
            status = "OK" if metrics.success else "FAIL"
            print(f"  [{status}] JSON max_actors={max_actors} in {metrics.response_time_ms:.2f}ms")

    def test_timeline(self):
        """Test timeline retrieval."""
        print("\n--- Testing: get_timeline ---")

        metrics = self._timed_query(
            "get_timeline",
            self.agent.get_timeline,
            {}
        )
        self.report.add_query(metrics)
        status = "OK" if metrics.success else "FAIL"
        print(f"  [{status}] -> {metrics.result_count} events in {metrics.response_time_ms:.2f}ms")

    def test_workspace_stats(self):
        """Test stats retrieval."""
        print("\n--- Testing: workspace stats ---")

        metrics = self._timed_query(
            "get_stats",
            lambda: self.agent.stats,
            {}
        )
        self.report.add_query(metrics)
        status = "OK" if metrics.success else "FAIL"
        print(f"  [{status}] stats retrieved in {metrics.response_time_ms:.2f}ms")

    def run_all_tests(self):
        """Run all performance tests."""
        if not self.setup():
            return None

        print(f"\n{'='*60}")
        print("RUNNING PERFORMANCE TESTS")
        print(f"{'='*60}")

        self.test_find_parties()
        self.test_get_actors_by_role()
        self.test_find_cases_by_type()
        self.test_get_unanswered_questions()
        self.test_get_context()
        self.test_timeline()
        self.test_workspace_stats()

        self.report.finalize()
        return self.report

    def print_summary(self):
        """Print summary report."""
        print(f"\n{'='*60}")
        print("PERFORMANCE SUMMARY")
        print(f"{'='*60}")

        print(f"\nQueries: {self.report.queries_successful}/{self.report.queries_executed} successful")
        print(f"Success Rate: {(self.report.queries_successful / max(1, self.report.queries_executed) * 100):.1f}%")
        print(f"\nTiming:")
        print(f"  - Total: {self.report.total_query_time_ms:.2f}ms")
        print(f"  - Average: {self.report.avg_query_time_ms:.2f}ms")
        print(f"  - Min: {self.report.min_query_time_ms:.2f}ms")
        print(f"  - Max: {self.report.max_query_time_ms:.2f}ms")

        print(f"\nBy Query Type:")
        for qtype, times in self.report.metrics_by_type.items():
            avg = sum(times) / len(times)
            print(f"  - {qtype}: {len(times)} queries, avg {avg:.2f}ms")

        print(f"\nKnowledge Coverage:")
        print(f"  - Actors by Type: {self.report.actors_by_type}")
        print(f"  - Questions by Type: {self.report.questions_by_type}")
        print(f"  - Actors by Role (top 5): {dict(list(self.report.actors_by_role.items())[:5])}")

    def save_report(self, output_path: Path):
        """Save full report to JSON."""
        report_dict = self.report.to_dict()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2)

        print(f"\nReport saved to: {output_path}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run performance tests."""
    # Default workspace path
    workspace_path = Path("data/workspaces/family_law_gsw.json")

    # Allow override via command line
    if len(sys.argv) > 1:
        workspace_path = Path(sys.argv[1])

    # Run tests
    tester = AgentPerformanceTester(workspace_path)
    report = tester.run_all_tests()

    if report:
        tester.print_summary()

        # Save report
        output_path = Path("tests/performance_report.json")
        tester.save_report(output_path)

        print(f"\n{'='*60}")
        print("TEST COMPLETE")
        print(f"{'='*60}")

        return 0
    else:
        print("\nTEST FAILED - Could not initialize agent")
        return 1


if __name__ == "__main__":
    sys.exit(main())
