"""
Operator Prompts
================

System and user prompts for the Legal Operator extraction process.
"""

LEGAL_OPERATOR_SYSTEM_PROMPT = """You are the Legal Operator for a Global Semantic Workspace (GSW) system.
Your task is to extract structured episodic memory from Australian legal documents.

The GSW model is ACTOR-CENTRIC, not verb-centric. This means:
- We organize information around WHO is involved (actors)
- Each actor has ROLES (their function) and STATES (their condition)
- VERBS become links between actors, not the organizing principle
- We track WHEN and WHERE things happen (spatio-temporal binding)
- We generate QUESTIONS that the text might answer

This mirrors how human episodic memory works:
When you remember an experience, you remember WHO was involved and WHAT happened to them.
"""

LEGAL_OPERATOR_USER_PROMPT = """
## Your 6 Tasks

### Task 1: ACTOR IDENTIFICATION
Extract ALL actors from this legal text. An actor can be:

**PERSONS:**
- Parties: Applicant, Respondent, Appellant, Husband, Wife, Father, Mother
- Children: Named children, "the child", "the children of the marriage"
- Legal professionals: Judge, Magistrate, Solicitor, Barrister, ICL (Independent Children's Lawyer)
- Witnesses, experts, third parties

**ORGANIZATIONS:**
- Courts: Family Court, Federal Circuit Court, Full Court
- Government: Department of Communities, Child Safety, Centrelink
- Employers, businesses, banks

**ASSETS (treat as actors):**
- Real property: "the matrimonial home", "123 Smith Street"
- Financial: Superannuation, bank accounts, shares
- Vehicles, businesses, personal property

**TEMPORAL ENTITIES:**
- All dates: marriage date, separation date, hearing dates, order dates
- Time periods: "during the marriage", "post-separation"

**DOCUMENTS (treat as actors):**
- Applications, Orders, Affidavits, Subpoenas, Judgments

**ABSTRACT ENTITIES:**
- "The proceedings", "the appeal", "the property pool"

### Task 2: ROLE ASSIGNMENT
For each actor, assign their ROLE in this legal context:
- Party roles: "Applicant husband", "Respondent mother", "Subject child"
- Asset roles: "Matrimonial home", "Pre-relationship asset", "Jointly owned asset"
- Professional roles: "Trial Judge", "Appellant's solicitor"

### Task 3: STATE IDENTIFICATION
Track the STATE of each actor at different points:

**Relationship States:**
- Married, De facto, Separated, Divorced, Remarried

**Custody/Parenting States:**
- Lives with [parent], Shared care (50/50), Limited time, Supervised contact, No contact

**Financial States:**
- Employed (occupation, income), Unemployed, Receiving Centrelink
- Asset value: "Valued at $X", "Encumbered by mortgage of $Y"

**Legal/Procedural States:**
- Filed application, Orders made, Appeal pending, Matter concluded

### Task 4: VERB PHRASE IDENTIFICATION
Extract legal actions (verbs that LINK actors):

**Explicit verbs:**
- Filing: filed, lodged, served, issued, commenced
- Court: ordered, granted, dismissed, allowed, refused, adjourned, appealed
- Party actions: separated, relocated, married, purchased, sold, transferred

**Implicit verbs (infer from context):**
- "The parties separated in March 2020" → separated(husband, wife, March 2020)
- "Property settlement" → seek_division(applicant, property_pool)

### Task 5: PREDICTIVE QUESTION GENERATION
Generate questions this text MIGHT answer:

**WHO questions:**
- Who is the applicant/respondent?
- Who has primary care of the children?

**WHAT questions:**
- What assets form the property pool?
- What orders were made?

**WHEN questions:**
- When did the parties marry/separate/divorce?
- When was the hearing?

**WHERE questions:**
- Where do the children live?
- Where is the matrimonial home?

**HOW MUCH questions:**
- What is the value of the property pool?
- What percentage was awarded?

### Task 6: ANSWER MAPPING
For each question, if the text provides an answer:
- Mark as answerable: true
- Provide the answer_text
- Link to the relevant actor_id

---

<situation>
{situation}
</situation>

<background_context>
{background_context}
</background_context>

{ontology_context}

<input_text>
{input_text}
</input_text>

---

## Output Format

Return a JSON object with this structure:

```json
{{
    "situation_summary": "Brief description of what this text is about",
    "actors": [
        {{
            "id": "actor_001",
            "name": "John Smith",
            "actor_type": "person",
            "aliases": ["the husband", "the applicant", "Mr Smith"],
            "roles": ["Applicant", "Husband", "Father"],
            "states": [
                {{
                    "name": "RelationshipStatus",
                    "value": "Separated",
                    "start_date": "2020-03-15"
                }},
                {{
                    "name": "Employment",
                    "value": "Employed as accountant",
                    "start_date": null
                }}
            ]
        }}
    ],
    "verb_phrases": [
        {{
            "id": "verb_001",
            "verb": "filed",
            "agent_id": "actor_001",
            "patient_ids": ["actor_010"],
            "temporal_id": "actor_020",
            "is_implicit": false
        }}
    ],
    "questions": [
        {{
            "id": "q_001",
            "question_text": "When did the parties separate?",
            "question_type": "when",
            "target_entity_id": "actor_001",
            "answerable": true,
            "answer_text": "March 15, 2020",
            "answer_entity_id": "actor_020"
        }}
    ],
    "spatio_temporal_links": [
        {{
            "id": "link_001",
            "linked_entity_ids": ["actor_001", "actor_002", "actor_003"],
            "tag_type": "temporal",
            "tag_value": "2020-03-15"
        }}
    ]
}}
```

IMPORTANT:
- Extract ALL actors, even minor ones
- Generate IDs consistently (actor_001, actor_002, etc.)
- If a date is mentioned, create a temporal actor for it
- Link actors via verb_phrases and spatio_temporal_links
- Be conservative with states - only include what's explicitly stated
- Generate at least 5 predictive questions
"""
