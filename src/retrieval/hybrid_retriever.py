"""
Hybrid Retriever - GSW + BM25
==============================

Combines GSW-aware semantic retrieval with BM25 fallback.

Retrieval Modes:
- "gsw": Pure GSW semantic search (actor-centric)
- "bm25": Pure BM25 full-text search
- "auto": Hybrid with automatic selection (default)

The "auto" mode:
1. Tries GSW first
2. If GSW returns good results (score > threshold), use them
3. Otherwise, fall back to BM25
4. Can also blend results from both
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.retrieval.gsw_retriever import GSWRetriever
from src.retrieval.retriever import LegalRetriever


class HybridRetriever:
    """
    Hybrid retrieval combining GSW semantic search with BM25 fallback.

    Usage:
        retriever = HybridRetriever(
            workspace_dir="data/workspaces",
            data_dir="data"
        )

        # Auto mode (default)
        results = retriever.retrieve("custody arrangement")

        # Force GSW
        results = retriever.retrieve("custody arrangement", mode="gsw")

        # Force BM25
        results = retriever.retrieve("specific case citation", mode="bm25")

        # Get context expansion
        context = retriever.retrieve_with_context("property settlement")
    """

    def __init__(
        self,
        workspace_dir: Path = None,
        data_dir: Path = None,
        gsw_score_threshold: float = 2.0,
        blend_results: bool = False
    ):
        """
        Initialize hybrid retriever.

        Args:
            workspace_dir: Directory with workspace JSON files
            data_dir: Directory with case corpus
            gsw_score_threshold: Minimum GSW score to use GSW results (default 2.0)
            blend_results: If True, blend GSW and BM25 results (default False)
        """
        self.workspace_dir = workspace_dir or Path("data/workspaces")
        self.data_dir = data_dir or Path("data")
        self.gsw_score_threshold = gsw_score_threshold
        self.blend_results = blend_results

        # Initialize retrievers
        print("[HybridRetriever] Initializing retrievers...")

        self.gsw_retriever = GSWRetriever(workspace_dir=self.workspace_dir)
        self.bm25_retriever = LegalRetriever(data_dir=str(self.data_dir))

        print("[HybridRetriever] Initialization complete")

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        mode: str = "auto",
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents/entities.

        Args:
            query: User query string
            top_k: Number of results to return
            mode: "auto", "gsw", or "bm25"
            domain: Optional domain filter (for GSW)

        Returns:
            List of results with scores
        """
        if mode == "gsw":
            return self._retrieve_gsw(query, top_k, domain)

        elif mode == "bm25":
            return self._retrieve_bm25(query, top_k)

        elif mode == "auto":
            return self._retrieve_auto(query, top_k, domain)

        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'auto', 'gsw', or 'bm25'")

    def _retrieve_gsw(self, query: str, top_k: int, domain: Optional[str]) -> List[Dict[str, Any]]:
        """Pure GSW retrieval."""
        return self.gsw_retriever.retrieve(query, top_k=top_k, domain=domain)

    def _retrieve_bm25(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Pure BM25 retrieval."""
        bm25_results = self.bm25_retriever.search(query, top_k=top_k)

        # Normalize format to match GSW
        normalized = []
        for result in bm25_results:
            normalized.append({
                'id': result.get('id'),
                'type': 'case',
                'title': result.get('title'),
                'text_preview': result.get('text_preview'),
                'score': result.get('score', 0.0),
                'source': 'bm25'
            })

        return normalized

    def _retrieve_auto(self, query: str, top_k: int, domain: Optional[str]) -> List[Dict[str, Any]]:
        """
        Automatic hybrid retrieval.

        Strategy:
        1. Try GSW first
        2. If top GSW result has score > threshold, use GSW
        3. Otherwise, use BM25
        4. Optionally blend results
        """
        # Get GSW results
        gsw_results = self._retrieve_gsw(query, top_k, domain)

        # Check if GSW has good results
        has_good_gsw = (
            gsw_results and
            gsw_results[0]['score'] >= self.gsw_score_threshold
        )

        if has_good_gsw and not self.blend_results:
            # Use GSW results
            for result in gsw_results:
                result['source'] = 'gsw'
            return gsw_results

        # Get BM25 results
        bm25_results = self._retrieve_bm25(query, top_k)

        if not gsw_results:
            # No GSW results, use BM25
            return bm25_results

        if not bm25_results:
            # No BM25 results, use GSW
            for result in gsw_results:
                result['source'] = 'gsw'
            return gsw_results

        # Blend results
        if self.blend_results:
            return self._blend_results(gsw_results, bm25_results, top_k)

        # Default: prefer BM25 if GSW score is low
        if has_good_gsw:
            for result in gsw_results:
                result['source'] = 'gsw'
            return gsw_results
        else:
            return bm25_results

    def _blend_results(
        self,
        gsw_results: List[Dict],
        bm25_results: List[Dict],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """
        Blend GSW and BM25 results.

        Strategy:
        - Normalize scores to 0-1 range
        - Combine with weights (0.6 GSW, 0.4 BM25)
        - Re-rank and return top_k
        """
        # Normalize GSW scores
        if gsw_results:
            max_gsw = max(r['score'] for r in gsw_results)
            if max_gsw > 0:
                for r in gsw_results:
                    r['normalized_score'] = r['score'] / max_gsw
                    r['source'] = 'gsw'

        # Normalize BM25 scores
        if bm25_results:
            max_bm25 = max(r['score'] for r in bm25_results if r['score'] > 0)
            if max_bm25 > 0:
                for r in bm25_results:
                    r['normalized_score'] = r['score'] / max_bm25
                    r['source'] = 'bm25'

        # Combine and weight
        all_results = []

        # Add GSW results with weight
        for r in gsw_results:
            r['final_score'] = r.get('normalized_score', 0) * 0.6
            all_results.append(r)

        # Add BM25 results with weight
        for r in bm25_results:
            r['final_score'] = r.get('normalized_score', 0) * 0.4
            all_results.append(r)

        # Sort by final score
        all_results.sort(key=lambda x: x.get('final_score', 0), reverse=True)

        return all_results[:top_k]

    def retrieve_with_context(
        self,
        query: str,
        top_k: int = 3,
        depth: int = 2
    ) -> Dict[str, Any]:
        """
        Retrieve with graph context expansion (GSW only).

        Args:
            query: User query
            top_k: Number of primary matches
            depth: Relationship expansion depth

        Returns:
            Dict with primary matches and related entities
        """
        return self.gsw_retriever.retrieve_with_context(query, top_k, depth)

    def search_by_role(
        self,
        role: str,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for actors by role (GSW only)."""
        return self.gsw_retriever.search_by_role(role, domain)

    def search_by_state(
        self,
        state_name: str,
        state_value: Optional[str] = None,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for actors by state (GSW only)."""
        return self.gsw_retriever.search_by_state(state_name, state_value, domain)

    def get_statistics(self) -> Dict[str, Any]:
        """Get retriever statistics."""
        gsw_stats = self.gsw_retriever.get_statistics()

        return {
            'gsw': gsw_stats,
            'bm25': {
                'indexed_documents': self.bm25_retriever.bm25.corpus_size,
                'citation_index_size': len(self.bm25_retriever.citation_index)
            },
            'config': {
                'gsw_score_threshold': self.gsw_score_threshold,
                'blend_results': self.blend_results
            }
        }


# ============================================================================
# MAIN / TEST
# ============================================================================

if __name__ == "__main__":
    print("Testing HybridRetriever...")
    print("=" * 80)

    # Initialize
    retriever = HybridRetriever(
        workspace_dir=Path("data/workspaces"),
        data_dir=Path("data")
    )

    # Print statistics
    stats = retriever.get_statistics()
    print(f"\nRetriever Statistics:")
    print(f"  GSW Workspaces: {stats['gsw']['total_workspaces']}")
    print(f"  GSW Actors: {stats['gsw']['total_actors']}")
    print(f"  BM25 Documents: {stats['bm25']['indexed_documents']}")

    # Test queries with different modes
    test_cases = [
        ("custody arrangement", "auto"),
        ("property settlement", "gsw"),
        ("intervention order", "auto"),
        ("[2020] FamCA 123", "bm25"),  # Citation lookup
    ]

    print("\n" + "=" * 80)
    print("Test Queries:")
    print("=" * 80)

    for query, mode in test_cases:
        print(f"\nQuery: '{query}' (mode: {mode})")
        print("-" * 80)

        results = retriever.retrieve(query, top_k=3, mode=mode)

        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. [{result['type']}] {result.get('name', result.get('title', 'N/A'))}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   Source: {result.get('source', 'unknown')}")

                if result['type'] == 'actor' and 'roles' in result:
                    print(f"   Roles: {', '.join(result['roles']) if result['roles'] else 'None'}")
        else:
            print("  No results found")

    # Test context retrieval
    print("\n" + "=" * 80)
    print("Context Retrieval Test:")
    print("=" * 80)

    context = retriever.retrieve_with_context("property settlement", top_k=2, depth=1)

    print(f"\nPrimary Matches: {len(context['primary_matches'])}")
    print(f"Related Actors: {len(context['related_actors'])}")
    print(f"Temporal Links: {len(context['temporal_links'])}")
    print(f"Spatial Links: {len(context['spatial_links'])}")

    if context['primary_matches']:
        print("\nTop Match:")
        top = context['primary_matches'][0]
        print(f"  {top.get('name', 'N/A')} (score: {top['score']:.2f})")

    if context['related_actors']:
        print("\nRelated Actors:")
        for actor in context['related_actors'][:3]:
            print(f"  - {actor['name']} (relation: {actor.get('relation', 'N/A')})")

    print("\n" + "=" * 80)
    print("Test Complete!")
