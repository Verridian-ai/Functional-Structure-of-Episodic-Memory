"""
GSW-Aware Semantic Retrieval
==============================

Implements semantic retrieval over actor-centric GSW structure,
replacing raw BM25 text search with graph-aware entity retrieval.

This retriever understands:
- Actors with roles and states
- Verb phrases linking entities
- Temporal and spatial context
- Relationship graphs

Based on: arXiv:2511.07587 - Functional Structure of Episodic Memory
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict, Counter
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.gsw.workspace import WorkspaceManager
from src.logic.gsw_schema import (
    GlobalWorkspace, Actor, VerbPhrase, State,
    SpatioTemporalLink, ActorType, LinkType
)


class GSWRetriever:
    """
    Semantic retrieval over actor-centric GSW structure.

    Features:
    - Actor-centric search (name, role, state matching)
    - Verb phrase search (action-based retrieval)
    - Temporal context filtering
    - Graph-aware expansion (related entities)
    - Concept extraction from queries

    Usage:
        retriever = GSWRetriever(workspace_dir="data/workspaces")
        results = retriever.retrieve("custody arrangement for children", top_k=5)

        # With context expansion
        context = retriever.retrieve_with_context("property settlement", depth=2)
    """

    def __init__(self, workspace_dir: Path = None, domains: List[str] = None):
        """
        Initialize GSW retriever.

        Args:
            workspace_dir: Directory containing workspace JSON files
            domains: Specific domains to load (None = all)
        """
        self.workspace_dir = workspace_dir or Path("data/workspaces")
        self.workspaces: Dict[str, WorkspaceManager] = {}

        # Legal term patterns for enhanced matching
        self.legal_patterns = self._compile_legal_patterns()

        # Load workspaces
        self._load_workspaces(domains)

    def _load_workspaces(self, domains: Optional[List[str]] = None):
        """Load all workspace files from directory."""
        if not self.workspace_dir.exists():
            print(f"[GSWRetriever] Warning: Workspace directory {self.workspace_dir} not found")
            return

        # Load all *_workspace.json files
        workspace_files = list(self.workspace_dir.glob("*_workspace.json"))

        if not workspace_files:
            print(f"[GSWRetriever] Warning: No workspace files found in {self.workspace_dir}")
            return

        loaded_count = 0
        for workspace_file in workspace_files:
            # Extract domain from filename (e.g., "family_workspace.json" -> "family")
            domain = workspace_file.stem.replace('_workspace', '')

            # Filter by domains if specified
            if domains and domain not in domains:
                continue

            try:
                manager = WorkspaceManager.load(workspace_file)
                self.workspaces[domain] = manager
                loaded_count += 1

                stats = manager.get_statistics()
                print(f"[GSWRetriever] Loaded {domain}: {stats['total_actors']} actors, "
                      f"{stats['total_verb_phrases']} verbs, {stats['total_questions']} questions")
            except Exception as e:
                print(f"[GSWRetriever] Error loading {workspace_file}: {e}")

        print(f"[GSWRetriever] Loaded {loaded_count} workspace(s)")

    def _compile_legal_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for legal term detection."""
        return {
            'person_names': re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'),
            'dates': re.compile(r'\b(\d{4}|\d{1,2}/\d{1,2}/\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b'),
            'legal_actions': re.compile(r'\b(filed|ordered|granted|dismissed|appealed|settled|divorced|separated|contested|awarded|allocated)\b', re.I),
            'legal_entities': re.compile(r'\b(applicant|respondent|child|children|court|judge|property|asset|custody|parenting)\b', re.I),
            'amounts': re.compile(r'\$[\d,]+(?:\.\d{2})?'),
        }

    def retrieve(self, query: str, top_k: int = 5, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant actors/entities from GSW.

        Args:
            query: User query string
            top_k: Number of results to return
            domain: Specific domain to search (None = all domains)

        Returns:
            List of scored results with entity data
        """
        # Extract query concepts
        query_concepts = self._extract_concepts(query)

        # Determine which workspaces to search
        if domain and domain in self.workspaces:
            workspaces_to_search = {domain: self.workspaces[domain]}
        else:
            workspaces_to_search = self.workspaces

        results = []

        for domain_name, manager in workspaces_to_search.items():
            workspace = manager.workspace

            # Search actors
            for actor_id, actor in workspace.actors.items():
                score = self._score_actor(actor, query_concepts)
                if score > 0:
                    results.append({
                        'id': actor_id,
                        'type': 'actor',
                        'name': actor.name,
                        'actor_type': actor.actor_type.value,
                        'roles': actor.roles,
                        'states': [{'name': s.name, 'value': s.value} for s in actor.states[:3]],  # Top 3 states
                        'actor': actor,
                        'score': score,
                        'domain': domain_name
                    })

            # Search verb phrases
            for verb_id, verb in workspace.verb_phrases.items():
                score = self._score_verb(verb, query_concepts, workspace)
                if score > 0:
                    # Get agent name
                    agent_name = "Unknown"
                    if verb.agent_id and verb.agent_id in workspace.actors:
                        agent_name = workspace.actors[verb.agent_id].name

                    # Get patient names
                    patient_names = []
                    for patient_id in verb.patient_ids:
                        if patient_id in workspace.actors:
                            patient_names.append(workspace.actors[patient_id].name)

                    results.append({
                        'id': verb_id,
                        'type': 'verb_phrase',
                        'verb': verb.verb,
                        'agent': agent_name,
                        'patients': patient_names,
                        'verb_phrase': verb,
                        'score': score,
                        'domain': domain_name
                    })

            # Search questions (for question-answering)
            for question_id, question in workspace.questions.items():
                score = self._score_question(question, query_concepts)
                if score > 0:
                    results.append({
                        'id': question_id,
                        'type': 'question',
                        'question_text': question.question_text,
                        'answerable': question.answerable,
                        'answer_text': question.answer_text,
                        'question': question,
                        'score': score,
                        'domain': domain_name
                    })

        # Sort by score (descending)
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:top_k]

    def _extract_concepts(self, query: str) -> Dict[str, float]:
        """
        Extract weighted concepts from query.

        Concepts include:
        - Named entities (people, organizations) - weight 2.0
        - Legal terms (custody, property, etc.) - weight 1.5
        - Dates and amounts - weight 1.5
        - General terms - weight 1.0

        Returns:
            Dict mapping concept to weight
        """
        concepts: Dict[str, float] = {}

        # 1. Extract named entities (capitalized phrases)
        person_matches = self.legal_patterns['person_names'].findall(query)
        for person in person_matches:
            concepts[person.lower()] = 2.0

        # 2. Extract legal entities and roles
        legal_entity_matches = self.legal_patterns['legal_entities'].findall(query)
        for entity in legal_entity_matches:
            concepts[entity.lower()] = 1.5

        # 3. Extract legal actions
        action_matches = self.legal_patterns['legal_actions'].findall(query)
        for action in action_matches:
            concepts[action.lower()] = 1.5

        # 4. Extract dates
        date_matches = self.legal_patterns['dates'].findall(query)
        for date in date_matches:
            concepts[date.lower()] = 1.5

        # 5. Extract amounts
        amount_matches = self.legal_patterns['amounts'].findall(query)
        for amount in amount_matches:
            concepts[amount.lower()] = 1.5

        # 6. General terms (not already captured)
        words = query.lower().split()
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'my', 'our',
                    'what', 'how', 'when', 'why', 'who', 'where', 'for', 'in',
                    'on', 'at', 'to', 'of', 'and', 'or', 'but'}

        for word in words:
            word_clean = re.sub(r'[^\w]', '', word)
            if word_clean and word_clean not in stopwords and word_clean not in concepts:
                concepts[word_clean] = 1.0

        return concepts

    def _score_actor(self, actor: Actor, query_concepts: Dict[str, float]) -> float:
        """
        Score actor relevance to query.

        Scoring factors:
        - Name match: 3.0x weight
        - Alias match: 2.5x weight
        - Role match: 2.0x weight
        - State match: 1.5x weight
        - Actor type match: 1.0x weight

        Returns:
            Relevance score (0.0+)
        """
        score = 0.0

        # 1. Name match (most important)
        actor_name_lower = actor.name.lower()
        for concept, weight in query_concepts.items():
            if concept in actor_name_lower:
                score += weight * 3.0

        # 2. Alias match
        for alias in actor.aliases:
            alias_lower = alias.lower()
            for concept, weight in query_concepts.items():
                if concept in alias_lower:
                    score += weight * 2.5

        # 3. Role match
        for role in actor.roles:
            role_lower = role.lower()
            for concept, weight in query_concepts.items():
                if concept in role_lower:
                    score += weight * 2.0

        # 4. State match
        for state in actor.states:
            state_text = f"{state.name} {state.value}".lower()
            for concept, weight in query_concepts.items():
                if concept in state_text:
                    score += weight * 1.5

        # 5. Actor type match
        actor_type_str = actor.actor_type.value
        for concept, weight in query_concepts.items():
            if concept in actor_type_str:
                score += weight * 1.0

        return score

    def _score_verb(self, verb: VerbPhrase, query_concepts: Dict[str, float],
                   workspace: GlobalWorkspace) -> float:
        """
        Score verb phrase relevance to query.

        Scoring factors:
        - Verb match: 3.0x weight
        - Agent/patient name match: 2.0x weight
        - Connected entities: 1.5x weight

        Returns:
            Relevance score (0.0+)
        """
        score = 0.0

        # 1. Verb match
        verb_lower = verb.verb.lower()
        for concept, weight in query_concepts.items():
            if concept in verb_lower:
                score += weight * 3.0

        # 2. Agent match
        if verb.agent_id and verb.agent_id in workspace.actors:
            agent = workspace.actors[verb.agent_id]
            agent_score = self._score_actor(agent, query_concepts)
            score += agent_score * 0.5  # Partial credit

        # 3. Patient match
        for patient_id in verb.patient_ids:
            if patient_id in workspace.actors:
                patient = workspace.actors[patient_id]
                patient_score = self._score_actor(patient, query_concepts)
                score += patient_score * 0.5  # Partial credit

        return score

    def _score_question(self, question, query_concepts: Dict[str, float]) -> float:
        """
        Score question relevance to query.

        Returns:
            Relevance score (0.0+)
        """
        score = 0.0

        # Match question text
        question_lower = question.question_text.lower()
        for concept, weight in query_concepts.items():
            if concept in question_lower:
                score += weight * 2.0

        # Bonus for answered questions
        if question.answerable and question.answer_text:
            answer_lower = question.answer_text.lower()
            for concept, weight in query_concepts.items():
                if concept in answer_lower:
                    score += weight * 1.5

        return score

    def retrieve_with_context(self, query: str, top_k: int = 3, depth: int = 2) -> Dict[str, Any]:
        """
        Retrieve with relationship context expansion.

        This implements graph-aware retrieval:
        1. Find primary matches
        2. Expand to connected entities (via verb phrases)
        3. Include temporal/spatial context

        Args:
            query: User query
            top_k: Number of primary matches
            depth: How many hops to expand (1 or 2)

        Returns:
            Dict with primary_matches, related_actors, temporal_links, spatial_links
        """
        # Get primary matches
        primary = self.retrieve(query, top_k=top_k)

        context = {
            'primary_matches': primary,
            'related_actors': [],
            'related_verbs': [],
            'temporal_links': [],
            'spatial_links': []
        }

        # Track which entities we've already added
        seen_actor_ids: Set[str] = set()
        seen_verb_ids: Set[str] = set()

        for match in primary:
            domain = match['domain']
            workspace = self.workspaces[domain].workspace

            if match['type'] == 'actor':
                actor_id = match['id']
                seen_actor_ids.add(actor_id)

                # Find related actors via verb phrases
                related = self._find_related_actors(
                    actor_id, workspace, depth, seen_actor_ids
                )
                context['related_actors'].extend(related)

                # Find temporal/spatial context
                temporal, spatial = self._find_context_links(actor_id, workspace)
                context['temporal_links'].extend(temporal)
                context['spatial_links'].extend(spatial)

            elif match['type'] == 'verb_phrase':
                verb_id = match['id']
                seen_verb_ids.add(verb_id)
                verb = match['verb_phrase']

                # Add agent and patients as related actors
                if verb.agent_id and verb.agent_id not in seen_actor_ids:
                    actor = workspace.actors.get(verb.agent_id)
                    if actor:
                        context['related_actors'].append({
                            'id': verb.agent_id,
                            'name': actor.name,
                            'roles': actor.roles,
                            'relation': 'agent_of_verb',
                            'domain': domain
                        })
                        seen_actor_ids.add(verb.agent_id)

                for patient_id in verb.patient_ids:
                    if patient_id not in seen_actor_ids:
                        actor = workspace.actors.get(patient_id)
                        if actor:
                            context['related_actors'].append({
                                'id': patient_id,
                                'name': actor.name,
                                'roles': actor.roles,
                                'relation': 'patient_of_verb',
                                'domain': domain
                            })
                            seen_actor_ids.add(patient_id)

        return context

    def _find_related_actors(self, actor_id: str, workspace: GlobalWorkspace,
                            depth: int, seen: Set[str]) -> List[Dict[str, Any]]:
        """
        Find actors connected via verb phrases (BFS).

        Args:
            actor_id: Starting actor
            workspace: Workspace to search
            depth: How many hops
            seen: Already processed actors

        Returns:
            List of related actor dicts
        """
        related = []

        if depth <= 0:
            return related

        # Find all verbs involving this actor
        for verb_id, verb in workspace.verb_phrases.items():
            connected_ids = []

            # Check if actor is agent or patient
            if verb.agent_id == actor_id:
                # Add patients
                connected_ids.extend(verb.patient_ids)
            elif actor_id in verb.patient_ids:
                # Add agent
                if verb.agent_id:
                    connected_ids.append(verb.agent_id)
                # Add other patients
                connected_ids.extend([pid for pid in verb.patient_ids if pid != actor_id])

            # Add connected actors
            for connected_id in connected_ids:
                if connected_id not in seen and connected_id in workspace.actors:
                    actor = workspace.actors[connected_id]
                    related.append({
                        'id': connected_id,
                        'name': actor.name,
                        'roles': actor.roles,
                        'relation': f'via_{verb.verb}',
                        'depth': 1
                    })
                    seen.add(connected_id)

                    # Recursive expansion if depth > 1
                    if depth > 1:
                        deeper = self._find_related_actors(
                            connected_id, workspace, depth - 1, seen
                        )
                        for d in deeper:
                            d['depth'] = 2
                        related.extend(deeper)

        return related

    def _find_context_links(self, actor_id: str, workspace: GlobalWorkspace) -> Tuple[List[Dict], List[Dict]]:
        """
        Find temporal and spatial links for an actor.

        Returns:
            (temporal_links, spatial_links)
        """
        temporal_links = []
        spatial_links = []

        for link_id, link in workspace.spatio_temporal_links.items():
            if actor_id in link.linked_entity_ids:
                link_dict = {
                    'id': link_id,
                    'tag_value': link.tag_value,
                    'linked_entities': len(link.linked_entity_ids)
                }

                if link.tag_type == LinkType.TEMPORAL:
                    temporal_links.append(link_dict)
                elif link.tag_type == LinkType.SPATIAL:
                    spatial_links.append(link_dict)

        return temporal_links, spatial_links

    def search_by_role(self, role: str, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for all actors with a specific role.

        Args:
            role: Role to search for (e.g., "applicant", "respondent")
            domain: Optional domain filter

        Returns:
            List of matching actors
        """
        role_lower = role.lower()
        results = []

        workspaces_to_search = (
            {domain: self.workspaces[domain]} if domain and domain in self.workspaces
            else self.workspaces
        )

        for domain_name, manager in workspaces_to_search.items():
            matches = manager.query_actors_by_role(role)
            for actor in matches:
                results.append({
                    'id': actor.id,
                    'name': actor.name,
                    'roles': actor.roles,
                    'actor_type': actor.actor_type.value,
                    'domain': domain_name
                })

        return results

    def search_by_state(self, state_name: str, state_value: Optional[str] = None,
                       domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for actors with a specific state.

        Args:
            state_name: State type (e.g., "RelationshipStatus")
            state_value: Optional state value (e.g., "Separated")
            domain: Optional domain filter

        Returns:
            List of matching actors
        """
        results = []

        workspaces_to_search = (
            {domain: self.workspaces[domain]} if domain and domain in self.workspaces
            else self.workspaces
        )

        for domain_name, manager in workspaces_to_search.items():
            matches = manager.query_actors_by_state(state_name, state_value)
            for actor in matches:
                matching_states = [
                    s for s in actor.states
                    if s.name.lower() == state_name.lower() and
                       (state_value is None or s.value.lower() == state_value.lower())
                ]

                results.append({
                    'id': actor.id,
                    'name': actor.name,
                    'roles': actor.roles,
                    'matching_states': [{'name': s.name, 'value': s.value} for s in matching_states],
                    'domain': domain_name
                })

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Get retriever statistics."""
        stats = {
            'total_workspaces': len(self.workspaces),
            'domains': list(self.workspaces.keys()),
            'total_actors': 0,
            'total_verbs': 0,
            'total_questions': 0,
            'by_domain': {}
        }

        for domain, manager in self.workspaces.items():
            workspace_stats = manager.get_statistics()
            stats['total_actors'] += workspace_stats['total_actors']
            stats['total_verbs'] += workspace_stats['total_verb_phrases']
            stats['total_questions'] += workspace_stats['total_questions']
            stats['by_domain'][domain] = workspace_stats

        return stats


# ============================================================================
# MAIN / TEST
# ============================================================================

if __name__ == "__main__":
    print("Testing GSWRetriever...")
    print("=" * 60)

    # Initialize retriever
    retriever = GSWRetriever(
        workspace_dir=Path("data/workspaces"),
        domains=["family"]  # Focus on family law for testing
    )

    # Print statistics
    stats = retriever.get_statistics()
    print(f"\nRetriever Statistics:")
    print(f"  Workspaces: {stats['total_workspaces']}")
    print(f"  Total Actors: {stats['total_actors']}")
    print(f"  Total Verbs: {stats['total_verbs']}")
    print(f"  Total Questions: {stats['total_questions']}")

    # Test queries
    test_queries = [
        "custody arrangement",
        "property settlement",
        "intervention order",
        "child parenting"
    ]

    print("\n" + "=" * 60)
    print("Test Queries:")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 60)

        results = retriever.retrieve(query, top_k=3)

        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. [{result['type']}] {result.get('name', result.get('verb', 'N/A'))}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   Domain: {result['domain']}")

                if result['type'] == 'actor':
                    print(f"   Roles: {', '.join(result['roles']) if result['roles'] else 'None'}")
                    if result['states']:
                        print(f"   States: {', '.join([f'{s["name"]}={s["value"]}' for s in result['states'][:2]])}")
                elif result['type'] == 'verb_phrase':
                    print(f"   Action: {result['verb']} (Agent: {result['agent']})")
        else:
            print("  No results found")

    print("\n" + "=" * 60)
    print("Test Complete!")
