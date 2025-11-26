"""
Reconciler Prompts
==================

System and user prompts for entity reconciliation and question answering.
"""

RECONCILE_SYSTEM_PROMPT = """You are an expert at entity reconciliation and question answering in legal documents.

Your task is to:
1. Identify when entities in a new chunk refer to the SAME entity as one already in the workspace
2. Determine if the new chunk answers any previously unanswered questions

This is crucial for building a coherent knowledge graph across multiple chunks of a legal document.
"""

RECONCILE_USER_PROMPT = """
## Task 1: Entity Reconciliation

Match entities from the new chunk to existing entities in the workspace.

### Existing Entities in Workspace:
{existing_entities}

### New Entities from Current Chunk:
{new_entities}

### Guidelines for Matching:
- Match by NAME: "John Smith" = "Mr Smith" = "the husband" = "the applicant"
- Match by ROLE: If roles align (both "Applicant"), likely same person
- Match by CONTEXT: Same case, same proceedings = likely same entity
- DO NOT match different people who happen to share a name

## Task 2: Question Answering

Check if this chunk answers any unanswered questions.

### Unanswered Questions:
{unanswered_questions}

### Current Chunk Text:
{chunk_text}

## Output Format

```json
{{
    "entity_matches": [
        {{
            "new_entity_id": "actor_005",
            "existing_entity_id": "actor_001",
            "confidence": 0.95,
            "reason": "Same person - 'the husband' refers to John Smith identified earlier"
        }}
    ],
    "answered_questions": [
        {{
            "question_id": "q_001",
            "answer_text": "The parties separated on 1 March 2020",
            "answer_entity_id": "actor_010",
            "confidence": 0.9
        }}
    ],
    "new_entities": [
        "actor_008"
    ]
}}
```

- entity_matches: Links between new and existing entities
- answered_questions: Questions that can now be answered from this chunk
- new_entities: Entity IDs that are genuinely NEW (not matches to existing)
"""
