"""
GSW Integration Examples
========================

This file demonstrates how to integrate LangFuse observability
into the existing GSW (Global Semantic Workspace) implementation.

Copy these patterns into your existing code to enable full tracing.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Tuple

# Import observability
from src.observability import (
    GSWTracer,
    trace_gsw_operation,
    trace_graph_traversal,
    trace_llm_generation,
    get_session_tracker,
    GraphActivation,
    TraversalResult,
    LatencyBreakdown,
    OperationType,
    RetrievalScorer,
)

# Import your existing GSW modules
# from src.gsw.workspace import WorkspaceManager
# from src.gsw.legal_operator import TheOperator
# from src.gsw.legal_reconciler import LegalReconciler
# from src.gsw.legal_spacetime import LegalSpacetime
# from src.logic.gsw_schema import GlobalWorkspace, Actor, State


# =============================================================================
# EXAMPLE 1: Wrapping the Legal Operator with Tracing
# =============================================================================

@trace_llm_generation(model="gemini-2.0-flash", name="legal_extraction")
async def traced_extract_entities(operator, text: str) -> Dict[str, Any]:
    """
    Wrapped extraction with automatic LLM tracing.

    Usage:
        result = await traced_extract_entities(operator, document_text)
    """
    # Your existing extraction logic
    # result = await operator.extract(text)
    # return result
    pass


# =============================================================================
# EXAMPLE 2: Full Pipeline with Latency Breakdown
# =============================================================================

async def traced_gsw_pipeline(
    query: str,
    session_id: str,
    user_id: Optional[str] = None,
) -> Tuple[Dict[str, Any], float]:
    """
    Full GSW pipeline with comprehensive tracing.

    Returns:
        Tuple of (result, accuracy_score)
    """
    # Initialize tracer
    tracer = GSWTracer()

    # Start trace for this query
    trace = tracer.start_trace(
        name="gsw_legal_query",
        session_id=session_id,
        user_id=user_id,
        metadata={"query_length": len(query)},
        tags=["legal-ai", "gsw", "production"],
    )

    # Get session tracker for episodic memory
    session = get_session_tracker(session_id)
    session.start_turn(query)

    # Initialize latency tracking
    latency = LatencyBreakdown(total_ms=0)

    try:
        # -----------------------------------------------------------------
        # PHASE 1: Graph Traversal (Knowledge Graph Retrieval)
        # -----------------------------------------------------------------
        async with tracer.async_trace_span(
            "knowledge_graph_retrieval",
            OperationType.GRAPH_TRAVERSAL,
            input_data={"query": query},
        ) as span:
            span.start_sub_timer("graph_traversal")

            # Simulate graph traversal (replace with your actual code)
            # workspace = WorkspaceManager.load("path/to/workspace.json")
            # results = workspace.query_by_semantic_similarity(query)

            # Track activated nodes
            activated_nodes = []

            # Example: Record each activated entity
            # for entity in results:
            #     activation = GraphActivation(
            #         entity_id=entity.id,
            #         entity_type=entity.__class__.__name__,
            #         entity_name=getattr(entity, 'name', None),
            #         activation_score=entity.relevance_score,
            #         traversal_depth=entity.depth,
            #         connected_entities=entity.connected_ids,
            #     )
            #     activated_nodes.append(activation)
            #     span.record_graph_activation(activation)
            #
            #     # Also track in session
            #     session.record_entity_activation(
            #         entity_id=entity.id,
            #         entity_type=entity.__class__.__name__,
            #         entity_name=getattr(entity, 'name', None),
            #         relevance=entity.relevance_score,
            #     )

            latency.graph_traversal_ms = span.stop_sub_timer("graph_traversal")

            # Record full traversal result
            traversal_result = TraversalResult(
                query=query,
                activated_nodes=activated_nodes,
                traversal_path=[a.entity_id for a in activated_nodes],
                total_nodes_scanned=100,  # Replace with actual
                nodes_activated=len(activated_nodes),
                max_depth_reached=3,
                latency_ms=latency.graph_traversal_ms,
            )
            span.record_traversal(traversal_result)

        # -----------------------------------------------------------------
        # PHASE 2: Vector Search (if needed)
        # -----------------------------------------------------------------
        async with tracer.async_trace_span(
            "vector_search",
            OperationType.VECTOR_SEARCH,
        ) as span:
            span.start_sub_timer("vector")

            # vector_store = LocalVectorStore()
            # similar_entities = vector_store.find_similar_entity(query, threshold=0.92)

            latency.vector_search_ms = span.stop_sub_timer("vector")

        # -----------------------------------------------------------------
        # PHASE 3: LLM Generation
        # -----------------------------------------------------------------
        async with tracer.async_trace_span(
            "llm_response_generation",
            OperationType.LLM_GENERATION,
        ) as span:
            span.start_sub_timer("llm")

            # context = format_context_for_llm(traversal_result)
            # response = await llm.generate(
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": query},
            #     ],
            #     context=context
            # )

            response = "Placeholder response"  # Replace with actual

            latency.llm_generation_ms = span.stop_sub_timer("llm")

            # Record LLM call
            tracer.trace_llm_call(
                model="gemini-2.0-flash",
                input_messages=[{"role": "user", "content": query}],
                output=response,
                usage={"prompt_tokens": 500, "completion_tokens": 200},
                latency_ms=latency.llm_generation_ms,
            )

        # -----------------------------------------------------------------
        # PHASE 4: Scoring
        # -----------------------------------------------------------------
        scorer = RetrievalScorer(target_score=0.95)

        metrics = scorer.score_retrieval(
            query=query,
            retrieved_entities=[],  # Replace with actual
            response_text=response,
        )

        # Record all scores
        tracer.score_with_breakdown(
            scores={
                "entity_relevance": metrics.entity_relevance,
                "structural_accuracy": metrics.structural_accuracy,
                "temporal_coherence": metrics.temporal_coherence,
                "legal_precision": metrics.legal_precision,
                "answer_completeness": metrics.answer_completeness,
            },
            weights={
                "entity_relevance": 0.25,
                "structural_accuracy": 0.20,
                "temporal_coherence": 0.15,
                "legal_precision": 0.20,
                "answer_completeness": 0.20,
            },
        )

        # -----------------------------------------------------------------
        # FINALIZE
        # -----------------------------------------------------------------

        # Calculate total latency
        latency.total_ms = (
            latency.graph_traversal_ms +
            latency.vector_search_ms +
            latency.llm_generation_ms
        )
        latency.other_ms = latency.total_ms - sum([
            latency.graph_traversal_ms,
            latency.vector_search_ms,
            latency.llm_generation_ms,
        ])

        # Record latency breakdown
        tracer.record_latency_breakdown(latency)

        # End session turn
        session.end_turn(
            response=response,
            confidence=metrics.composite_score,
        )

        # Update session context
        # session.update_context(workspace=workspace)

        # Export session data
        session.export_to_langfuse()

        result = {
            "response": response,
            "metrics": metrics.to_dict(),
            "latency": latency.to_dict(),
            "session_summary": session.get_session_summary(),
        }

        tracer.end_trace(output=result)

        return result, metrics.composite_score

    except Exception as e:
        tracer.end_trace(
            output={"error": str(e)},
            level="ERROR",
        )
        raise

    finally:
        tracer.flush()


# =============================================================================
# EXAMPLE 3: Decorator-Based Integration
# =============================================================================

class TracedWorkspaceManager:
    """
    Example of wrapping WorkspaceManager with tracing.

    Usage:
        manager = TracedWorkspaceManager("path/to/workspace.json")
        actors = manager.query_actors_by_role("applicant")
    """

    def __init__(self, workspace_path: str):
        # self.workspace = WorkspaceManager.load(workspace_path)
        self.tracer = GSWTracer()

    @trace_graph_traversal(name="query_actors_by_role")
    def query_actors_by_role(self, role: str) -> List[Dict]:
        """Query actors with tracing."""
        # return self.workspace.query_actors_by_role(role)
        return []

    @trace_gsw_operation(OperationType.GRAPH_TRAVERSAL, name="get_timeline")
    def get_timeline(self) -> List[Dict]:
        """Get timeline with tracing."""
        # return self.workspace.get_timeline()
        return []

    @trace_gsw_operation(OperationType.GRAPH_TRAVERSAL, name="semantic_search")
    def semantic_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Semantic search with full tracing."""
        tracer = GSWTracer()

        # Record individual activations
        results = []  # self.workspace.search(query, top_k)

        for i, result in enumerate(results):
            activation = GraphActivation(
                entity_id=result.get("id", f"entity_{i}"),
                entity_type=result.get("type", "unknown"),
                entity_name=result.get("name"),
                activation_score=result.get("score", 1.0),
                traversal_depth=0,
            )
            tracer.trace_graph_activation(activation)

        return results


# =============================================================================
# EXAMPLE 4: Session Memory Tracking
# =============================================================================

async def multi_turn_conversation_example():
    """
    Example of tracking episodic memory across a conversation.
    """
    session_id = "user_123_session_456"
    tracer = GSWTracer()
    session = get_session_tracker(session_id)

    # Turn 1
    tracer.start_trace("conversation", session_id=session_id)

    session.start_turn("What are my property rights after separation?")

    # Simulate retrieval
    session.record_entity_activation(
        entity_id="actor_wife",
        entity_type="Actor",
        entity_name="The Wife",
        relevance=0.95,
    )
    session.record_entity_activation(
        entity_id="actor_husband",
        entity_type="Actor",
        entity_name="The Husband",
        relevance=0.92,
    )
    session.record_entity_activation(
        entity_id="state_separation",
        entity_type="State",
        entity_name="Separated",
        relevance=0.98,
    )

    # Update context (simulate workspace state)
    session.update_context(
        actors={"actor_wife": {"name": "The Wife"}, "actor_husband": {"name": "The Husband"}},
        states={"state_separation": {"name": "Separated", "start_date": "2023-01-15"}},
    )

    session.end_turn(
        response="Under Section 79 of the Family Law Act...",
        confidence=0.92,
    )

    tracer.end_trace()

    # Turn 2 (follow-up)
    tracer.start_trace("conversation_followup", session_id=session_id)

    session.start_turn("What about the children?")

    # More entities activated
    session.record_entity_activation(
        entity_id="actor_child_1",
        entity_type="Actor",
        entity_name="Child 1",
        relevance=0.97,
    )

    # Context grows
    session.update_context(
        actors={
            "actor_wife": {"name": "The Wife"},
            "actor_husband": {"name": "The Husband"},
            "actor_child_1": {"name": "Child 1"},
        },
        states={"state_separation": {"name": "Separated"}},
    )

    session.end_turn(
        response="Under Section 60CC regarding parenting arrangements...",
        confidence=0.89,
    )

    tracer.end_trace()

    # Get session analytics
    summary = session.get_session_summary()
    print("Session Summary:")
    print(f"  Total turns: {summary['total_turns']}")
    print(f"  Entities activated: {summary['metrics']['entities_activated']}")
    print(f"  Context growth: {summary['metrics']['context_growth']}")
    print(f"  Top entities: {summary['top_entities']}")

    # Get visualization data
    growth_data = session.get_context_growth_chart_data()
    print(f"\nContext growth over turns: {growth_data}")

    tracer.flush()


# =============================================================================
# EXAMPLE 5: Manual Scoring Trigger
# =============================================================================

def manual_scoring_example():
    """
    Example of manually triggering accuracy scoring.
    """
    scorer = RetrievalScorer(target_score=0.95)

    # Define test case
    query = "What percentage will I receive in the property settlement?"

    retrieved_entities = [
        {"id": "actor_1", "type": "Actor", "name": "Applicant", "roles": ["applicant"]},
        {"id": "actor_2", "type": "Actor", "name": "Respondent", "roles": ["respondent"]},
        {"id": "state_1", "type": "State", "name": "Property Pool", "value": "$1,500,000"},
        {"id": "verb_1", "type": "VerbPhrase", "action": "seeks", "subject": "actor_1", "object": "property division"},
    ]

    expected_entities = [
        {"id": "actor_1", "type": "Actor"},
        {"id": "actor_2", "type": "Actor"},
        {"id": "state_1", "type": "State"},
    ]

    response = """
    ## Property Division Under Section 79

    Under **Section 79** of the Family Law Act 1975 (Cth), the Court follows
    a four-step process for property division:

    1. **Identify the asset pool**: Your combined assets total $1,500,000
    2. **Assess contributions**: Both financial and non-financial contributions
    3. **Consider future needs**: Under s79(4)(e)
    4. **Just and equitable test**

    Based on similar cases like *Mallet v Mallet* [1984] HCA 21, where homemaker
    contributions were valued equally, you may expect a division in the range
    of 45-55%.
    """

    # Score the retrieval
    metrics = scorer.score_retrieval(
        query=query,
        retrieved_entities=retrieved_entities,
        expected_entities=expected_entities,
        response_text=response,
    )

    print("Accuracy Metrics:")
    print(f"  Entity Relevance: {metrics.entity_relevance:.3f}")
    print(f"  Structural Accuracy: {metrics.structural_accuracy:.3f}")
    print(f"  Temporal Coherence: {metrics.temporal_coherence:.3f}")
    print(f"  Legal Precision: {metrics.legal_precision:.3f}")
    print(f"  Answer Completeness: {metrics.answer_completeness:.3f}")
    print(f"  Citation Accuracy: {metrics.citation_accuracy:.3f}")
    print(f"  ---")
    print(f"  Composite Score: {metrics.composite_score:.3f}")
    print(f"  Meets Target (0.95): {metrics.meets_target()}")
    print(f"  Precision: {metrics.precision:.3f}")
    print(f"  Recall: {metrics.recall:.3f}")
    print(f"  F1 Score: {metrics.f1_score:.3f}")

    # Record to LangFuse
    tracer = GSWTracer()
    tracer.start_trace("manual_evaluation")

    for name, value in [
        ("entity_relevance", metrics.entity_relevance),
        ("structural_accuracy", metrics.structural_accuracy),
        ("legal_precision", metrics.legal_precision),
        ("composite_score", metrics.composite_score),
    ]:
        tracer.score_retrieval(name, value)

    tracer.end_trace(output=metrics.to_dict())
    tracer.flush()


# =============================================================================
# EXAMPLE 6: Environment Setup
# =============================================================================

def setup_langfuse():
    """
    Example of setting up LangFuse with environment variables.

    Set these in your .env file or environment:
        LANGFUSE_PUBLIC_KEY=pk-...
        LANGFUSE_SECRET_KEY=sk-...
        LANGFUSE_HOST=https://cloud.langfuse.com  (optional)

    Or pass directly to GSWTracer:
        tracer = GSWTracer(
            public_key="pk-...",
            secret_key="sk-...",
        )
    """
    import os

    # Option 1: Environment variables (recommended)
    os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-your-public-key"
    os.environ["LANGFUSE_SECRET_KEY"] = "sk-your-secret-key"

    # Initialize tracer (picks up from environment)
    tracer = GSWTracer(debug=True)

    # Option 2: Direct initialization
    tracer = GSWTracer(
        public_key="pk-your-public-key",
        secret_key="sk-your-secret-key",
        host="https://cloud.langfuse.com",
        enabled=True,
        debug=True,
    )

    return tracer


# =============================================================================
# QUICK START
# =============================================================================

if __name__ == "__main__":
    print("GSW Observability Integration Examples")
    print("=" * 50)

    # Run manual scoring example
    print("\n1. Manual Scoring Example:")
    manual_scoring_example()

    # Run session tracking example
    print("\n2. Session Memory Tracking Example:")
    asyncio.run(multi_turn_conversation_example())

    print("\n" + "=" * 50)
    print("Examples complete. Check LangFuse dashboard for traces.")
