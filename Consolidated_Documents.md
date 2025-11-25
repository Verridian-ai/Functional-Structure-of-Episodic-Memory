# Functional Structure of Episodic Memory - Consolidated Documentation

## Overview

This document consolidates all materials from the "Functional Structure of Episodic Memory" project, including visual diagrams and PDF documents related to the Global Semantic Workspace (GSW) system.

---

## Project Dev Log – Technical Plan for Legal GSW Implementation

### Objective

Build a **Verifiably Accurate Legal AI** that grounds every assertion in a structured knowledge graph derived from the *Australian Family Law Act 1975*. The system extends the reference GSW architecture so that each extraction, reconciliation, and answer can be audited, replayed, and stress-tested against real cases.

### GSW Requirements Recap

From the `motivation.png` and `operatorv2.png` analyses above:

- **Operator** – extracts actors, roles, states, verbs, spatio-temporal facts, and predictive questions from raw text.
- **Global Semantic Workspace (GSW)** – binds those facts into a working memory that supports retrieval, updates, and simulation.
- **Reconciler** – performs entity/space/time/question reconciliation and drives iterative updates.
- **Prompt Suite (`prompts/GSW_prompt_*.pdf`)** – defines downstream behaviors: QA reasoning, reconciliation, spacetime linking, summarization.

Any implementation must therefore (1) capture structured facts with high recall, (2) maintain an evolving, self-consistent ontology, and (3) expose APIs for reasoning and verification.

### Phases 1–5 (Current State) Mapped to GSW

| Phase | Implementation Highlights | GSW Alignment | Impact |
|-------|---------------------------|---------------|--------|
| 1. **Data Engineering** | Streaming generator filters the 9.2 GB corpus by Family Law keywords to stay within RAM limits. | Operator pre-processing (sensory cortex equivalent). | Guarantees privacy and zero data loss via on-the-fly filtering. |
| 2. **Ontology Induction** | Gemini-derived Pydantic schema with `Person`, `Object`, `Event`, `State`. | Operator role/state extraction schema. | Automates schema discovery and mirrors actor-centric modeling. |
| 3. **Ingestion Logic** | Hybrid GPU+cloud ingestion, fuzzy date capture (`Optional[str]`), polymorphic outcome types. | Operator + Reconciler working memory formation. | “Capture first, parse later” ensures high recall and prevents schema-induced data loss. |
| 3.5 **Self-Audit** | `involved_cases`, merge logic updates, connectivity scores via `generate_report.py`. | Reconciler’s entity reconciliation + question auditing. | Measures graph density, exposes duplicates, and proves cross-case linking. |
| 4. **Reflexion & Batching** | Operator self-review, stateful orchestration with `ingestion_state.json`, calibration mode. | Operator iterative improvement & GSW update loop. | Reduces extraction errors before data hits the graph; enables controlled batch runs. |
| 4.5 **Self-Improving Ontology** | `Reconciler.get_ontology_summary()` feeds known vocabulary to Operator prompts. | **Active inference loop** (GSW extension). | Creates a cybernetic feedback system; vocabulary gravitates toward standard terms. |
| 5. **Context Optimization (TOON)** | Token-Oriented Object Notation compresses ontology payloads by ~55%. | Workspace bandwidth optimization. | Solves the “context paradox” so the Operator can see decades of history per prompt. |

**Conclusion:** Phases 1–5 already realize the Operator and Reconciler behaviors described in the GSW research, with additional innovations (feedback loop + TOON) that make the architecture practical for messy legal data.

### Viability Assessment & Identified Gaps

- ✅ **Data Fidelity:** Streaming ingestion + schema relaxation capture everything (Postel’s Law).
- ✅ **Ontology Coherence:** Feedback from the global graph creates a self-standardizing vocabulary.
- ✅ **Traceability:** Self-audit tooling (`LEGAL_LANDSCAPE_REPORT.md`) surfaces graph-level metrics.
- ⚠️ **Reasoning Gap:** No dedicated inference layer turns graph facts into legal conclusions.
- ⚠️ **QA Grounding:** Need a deterministic pipeline that runs `prompts/GSW_prompt_QA.pdf` over Australian Family Law contexts.
- ⚠️ **Evaluation:** Lacks benchmark datasets, accuracy metrics, and regression tests.
- ⚠️ **Deployment:** Need repeatable orchestration for batch + interactive inference (APIs, calibration, monitoring).

### Phase 6 – Technical Specification (Reasoning Experiment & Infrastructure)

#### 6.1 Knowledge Graph Reasoning Engine

- **Objective:** Execute neuro-symbolic reasoning over the legal knowledge graph to answer statutory questions and “what-if” scenarios.
- **Inputs:** Normalized entities/events/states, ontology dictionary, pending queries, grounding citations.
- **Process:**  
  1. Resolve query entities using the ontology (leveraging the existing feedback loop).  
  2. Traverse temporal + relational edges (e.g., marriage timeline, asset ownership, custody decisions).  
  3. Apply rule templates (e.g., *Family Law Act* sections translated into Python/PROLOG-like conditions).  
  4. Produce a proof trace listing matched clauses and graph nodes.
- **Outputs:** Structured answers (`{conclusion, supporting_nodes, statute_refs, confidence}`) ready for downstream QA.
- **Dependencies & Tooling:**  
  - Graph store (e.g., Neo4j or RDF) with temporal indexing.  
  - Rule engine layer (custom Python DSL or open-source logic engine).  
  - Integration hooks so the Operator can request “reasoning context” for future extractions.

#### 6.2 Question-Answering Pipeline (GSW Prompt Suite Integration)

- **Objective:** Operationalize the QA, reconcile, spacetime, and summary prompts on legal cases.
- **Inputs:**  
  - `GSW_prompt_operator.pdf`: structured chunks from ingestion phases.  
  - `GSW_prompt_QA.pdf`: user/legal questions.  
  - `GSW_prompt_reconcile.pdf`, `GSW_prompt_spacetime.pdf`, `GSW_prompt_summary.pdf`: reconciliation + summarization prompts.  
  - Reasoning-engine outputs (when available).
- **Workflow:**  
  1. **Chunk Selection:** Use TOON representations to feed 20+ years of case history while staying within context budgets.  
  2. **Operator Pass:** Re-run operator extraction if new context is injected (ensuring active inference).  
  3. **Reconciler Pass:** Execute reconcile + spacetime prompts to keep the graph consistent.  
  4. **QA Run:** Populate the QA prompt with relevant summaries and graph snippets.  
  5. **Answer Verification:** Cross-check QA output against reasoning-engine traces; fall back to “cannot answer” if evidence missing.  
  6. **Summary Generation:** Use the summary prompt to create human-readable explanations.
- **Deliverables:** API endpoint (or CLI) that accepts a legal question and returns (answer, citations, proof trace, prompt logs).

#### 6.3 Evaluation & Audit Framework

- **Objective:** Measure whether the system is “verifiably accurate.”
- **Components:**  
  - **Dataset Builder:** Sample labeled questions/outcomes from known Family Court cases.  
  - **Metrics:** Precision/recall on legal questions, ontology drift score, duplicate risk trend, reasoning coverage (% of answers with proof trace).  
  - **Connectivity Monitoring:** Extend the Phase 3.5 “Detective” to log before/after stats for each batch.  
  - **Regression Suite:** Re-run benchmark questions whenever ontology or prompts change; flag regressions automatically.
- **Outputs:** `LEGAL_LANDSCAPE_REPORT.md` v2 with accuracy dashboards + historical trends.

#### 6.4 Deployment & Orchestration

- **Objective:** Provide reliable, reproducible infrastructure for batch ingestion and interactive QA.
- **Key Elements:**  
  - **Stateful Scheduler:** Extend `ingestion_state.json` to include reasoning + QA job markers.  
  - **Calibration Mode Enhancements:** Allow sandboxed experiments with alternative prompts/models without contaminating production ontology.  
  - **API / gRPC Layer:** Serve QA + reasoning results with authentication and request logging.  
  - **Resource Strategy:**  
    - Local RTX 4090/5070 for embedding + entity linking.  
    - Cloud LLMs (Gemini or Anthropic) for heavy reasoning; batch requests with TOON compression.  
  - **Monitoring:** Collect latency, token usage, and accuracy stats per request; trigger alerts when drift detected.

### Implementation Roadmap

1. **Finalize Phase 6 specs (this document).**
2. **Reasoning Engine MVP:** Build rule templates for high-impact Family Law sections (e.g., property settlement, parenting orders).
3. **QA Pipeline Integration:** Wire Operator/Reconciler outputs into the QA prompt flow, backed by TOON context windows.
4. **Evaluation Harness:** Stand up automated benchmarks + reporting.
5. **Deployment Hardening:** Add orchestration/state tracking, calibration workflows, and public APIs.

Each milestone should end with: updated ontology snapshot, benchmark report, and prompt pack versioning so auditors can reproduce any answer.

---

## Image Explanations (Deep Analysis)

---

### motivation.png — Functional Structure of Episodic Memory

This diagram presents the **core theoretical foundation** of the Global Semantic Workspace (GSW) system by drawing a direct parallel between how the **human brain stores and processes episodic memories** and how an **AI system can computationally replicate this cognitive architecture**.

#### THE CENTRAL THESIS

The diagram argues that human episodic memory—our ability to remember personal experiences as coherent narratives with who, what, when, where, and how we felt—can be modeled computationally. The GSW system is designed to give AI systems this same capability: to process text/events and store them as structured, queryable episodic memories.

---

#### LEFT PANEL: The Biological Foundation of Episodic Memory

**What Is Stored (Aspects of Events)**

Human episodic memory doesn't store experiences as raw data. Instead, it decomposes experiences into fundamental aspects:

| Aspect | Meaning | Example |
|--------|---------|---------|
| **What** | Objects, people, actions involved | "Julian Ross", "hackathon", "coders" |
| **Where** | Spatial context/location | "Silicon Beach" |
| **When** | Temporal context/time | "May 31, 2024" |
| **How one felt/thought** | Emotional and cognitive states | "excited", "nervous", "jubilant" |
| **Bindings between above** | The relationships connecting all elements | Julian felt excited WHILE participating in the hackathon AT Silicon Beach ON May 31 |

This decomposition is crucial: it means memories are not monolithic blobs but **structured representations** that can be queried ("Where was Julian on May 31?") and updated ("Julian won the hackathon").

**How Processed**

The brain processes these memory aspects through specific mechanisms:

| Process | Function | Computational Analog |
|---------|----------|---------------------|
| **Hippocampus → Indexing** | Creates an "index" or pointer to where memory components are stored across the brain | The GSW creates entity IDs and links between actors |
| **Neocortex → Consolidation** | Long-term storage and integration of memories into existing knowledge | The Reconciler updates and merges entities across chunks |
| **Predictive Function** | Uses memories to simulate future scenarios, complete partial patterns, and infer states | Question generation and answer prediction in the GSW |

**Brain Regions Involved**

- **Medial Temporal Lobe**: Central hub for memory formation
- **Parahippocampal Place Area**: Specifically encodes spatial/location information ("where")
- **Insula, Amygdala**: Encode emotional states ("how one felt")
- **Default Mode Network**: Involved in self-referential thought, autobiographical memory, and mental time travel

---

#### RIGHT PANEL: The Computational Architecture (Two-Tier System)

The right side shows **two parallel architectures**—one biological (top) and one computational (bottom)—demonstrating how the GSW mirrors brain function.

**UPPER TIER: Neural Architecture (Brain)**

```
Sensory Cortex → Association Cortex → Prefrontal Cortex → EC (Entorhinal Cortex)
                                                              ↓
                              Neocortical Complex ←→ Subiculum ←→ Hippocampal Complex
                                                                        ↓
                                                              CA1 ← CA3 ← DG
```

| Component | Function |
|-----------|----------|
| **Sensory/Association/Prefrontal Cortex** | Initial processing of incoming information |
| **EC (Entorhinal Cortex)** | Gateway to the hippocampus; integrates spatial and temporal information |
| **Subiculum** | Bridge between neocortex and hippocampus |
| **DG (Dentate Gyrus)** | **Pattern Separation** — ensures similar memories are stored distinctly |
| **CA3** | **Sequence Modeling** — encodes temporal sequences of events |
| **CA1** | **Updates** — integrates new information with existing memories |

The arrows showing "step n" and "step n+1" indicate that memory is **iterative**—each new piece of information (step n+1) updates what was previously stored (step n).

**LOWER TIER: Computational Architecture (GSW)**

This is the AI system that mirrors the brain:

```
Text → LLM (Operator) → [actors, inter-actor relationships, verbs] → Global Semantic Workspace → LLM (Reconciler) → [Retrieval, Workspace, Update]
                         [roles, states, predictive questions, time/space]
```

| Component | Brain Analog | Function |
|-----------|--------------|----------|
| **Operator** | Sensory/Association Cortex | Takes raw text and extracts structured semantic information: actors, their roles, their states, actions (verbs), inter-actor relationships, and predictive questions |
| **Global Semantic Workspace** | Hippocampal Complex | Central integration point where all extracted information is bound together into a coherent representation |
| **Reconciler** | CA1/CA3/DG Functions | Three key functions: **Retrieval** (pattern completion—finding relevant stored memories), **Workspace** (current working memory), **Update** (integrating new information) |

---

#### WHY THIS MATTERS

The diagram makes a profound claim: **episodic memory is computable**. By understanding how the brain decomposes, processes, and stores experiences, we can build AI systems that:

1. **Remember narratives** as structured events, not just text
2. **Answer questions** about past events (like "When did Julian win?")
3. **Track entities** across time and space
4. **Update understanding** as new information arrives
5. **Make predictions** based on patterns in stored memories

This is fundamentally different from typical RAG (Retrieval-Augmented Generation) systems that just retrieve text chunks. The GSW creates a **semantic memory structure** that mirrors human cognition.

---

---

### operatorv2.png — Modeling the Global Workspace: Verb-Centric vs. Actor-Centric Representation

This diagram presents a **critical design decision** in natural language understanding: how should we represent the meaning of text in an intermediate form that an AI system can reason over?

#### THE EXAMPLE TEXT

> "moments later, police units involved in the chase arrived on scene. footage later from sky 4 shows the extent of the damage to both vehicles, and the area, as there was a mangled mess that would take hours to clean up. according to police, the innocent driver and officers were not hurt."

#### THE FUNDAMENTAL QUESTION

**"Which of the following intermediate representations do YOU think best reflects the representation of the text that you have just read?"**

This is asking: when you read this text, how does your brain organize this information? The answer reveals how the GSW should structure its memory.

---

#### CHOICE 1: Verb-Centric Representation (Traditional NLP Approach)

This approach organizes information **around verbs** (actions):

```
verb: involved
    object, thing affected: police units
    instrument, benefactive, attribute: in the chase

verb: arrived
    object, thing affected: police units involved in the chase
    ending point: on scene

verb: shows
    agent: footage later from sky 4
    object, thing affected: the extent of the damage...
```

**The Problem**: This representation:
- Fragments the narrative across multiple verb frames
- Loses track of WHO is doing things across the text
- Makes it hard to answer questions like "What happened to the police?"
- Treats verbs as primary when humans actually think about **actors/agents**

---

#### CHOICE 2: Actor-Centric Representation (GSW Approach)

This approach organizes information **around actors/agents**:

```
Agents in the situation:

Agent: police units
    Role: chase participants
    State: arrived on scene

Agent: police
    Role: chase participant
    State: arrived on scene

Agent: officers
    Role: law enforcers
    State: arrived on scene
```

**Why This Is Better**:

| Advantage | Explanation |
|-----------|-------------|
| **Mirrors human cognition** | When we remember events, we remember WHO was involved and WHAT happened to them |
| **Enables entity tracking** | We can track "police" across the entire narrative |
| **Supports questions naturally** | "What happened to the officers?" → Look up their state: "arrived on scene, not hurt" |
| **Captures roles explicitly** | Knowing someone is a "law enforcer" vs "chase participant" changes how we interpret their actions |
| **Records states** | States like "arrived on scene" are first-class information, not buried in verb arguments |

---

#### THE DEEPER MEANING

This diagram illustrates **why the GSW uses an actor-centric model**:

1. **Human episodic memory is actor-centric**: When you recall an experience, you remember the people/things involved and what happened to them—not a list of verbs.

2. **Roles define relationships**: An "officer" behaves differently than a "suspect." Roles are essential context.

3. **States are memories**: The fact that officers "were not hurt" is a **state** that gets stored and can be queried later.

4. **Verbs become connections**: Instead of being the organizing principle, verbs become the **links** between actors (who did what to whom).

This is the foundation of how the **Operator** (from motivation.png) extracts information: it identifies **actors**, assigns them **roles**, tracks their **states**, and records the **verbs/actions** as relationships between actors.

---

#### IMPLICATIONS FOR THE GSW SYSTEM

The GSW Operator extracts:
- **Actors**: police units, police, officers, vehicles, innocent driver, sky 4 (news helicopter)
- **Roles**: chase participants, law enforcers, damage victims, news source
- **States**: arrived on scene, not hurt, mangled mess
- **Verbs as relations**: involved in → chase, arrived → on scene, shows → damage

This structured representation enables:
- Question answering: "Were officers hurt?" → Check state → "No"
- Timeline reconstruction: "What happened after the chase?" → arrived, footage shown, cleanup
- Entity tracking: "What do we know about police?" → participants, arrived, not hurt

---

---

# PDF Raw Text Content

---

## gsw_example1.pdf

### Page 1

Situation Summary: Participating in a hackathon.

Julian Ross felt a surge of excitement as he navigated through the throng of coders at the hackathon

coders
Julian Ross
Role: Event 

Julian glanced at his smartwatch nervously, the display reading May 31, 2024

Julian Ross
smartwatch
May 31 2024
hackathon

Role: Attendee 
Role: Participant in hackathon 
State:Starting
Emotional State:

participate
navigated through
glanced at

Role: Time Device 
State: Displaying Date

Role: Current Date 
State: Displayed on smartwatch

Possible Questions | Answerable | Answer | Comments
What did coders participate in? | Yes | Hackathon
How was Julian feeling? | Yes | Excited | Available in text
How was Julian feeling? | Yes | Nervous | Available in text
When did the Hackathon take place? | No | - | -
Who won the hackathon? | No | - | -
Where did the hackathon take place? | No | - | -

Role: Participant in hackathon 
State: Ongoing
Emotional State: 

Time: Unknown
Space: Unknown

Time: Unknown
Space: Unknown

Time: Unknown
Space: Unknown

Time: May 31 2024
Space: Unknown

Time: May 31 2024
Space: Unknown

Where? When? Where? When? Where? When? What? Who? Who? Who? What? When & What? Who? When? Who? What? Where?

State reconciled: No
Text

---

## gsw_example2.pdf

### Page 1

Julian Ross
smartwatch
May 31 2024

Role: Event 
hackathon

Role: Attendee 

Role: Current Date 
State: Displayed on smartwatch

Role: Time Device 
State: Displaying Date

coders
Role: Participant   
State: Ongoing
Emotional State:

-> 

glanced at
participate
navigated through

When did Julian Ross participant in Hackathon?

Possible Questions | Answerable | Answer | Comments
May 31 2024 | Yes read
When did the Hackathon take place? | Yes | May 31 2024
Where did the Hackathon take place? | No | -
Who won the Hackathon? | No | -

Time: May 31 2024
Space: Unknown

What? Who? When? Where? Who? What? When? Who? What? What? Who? Where?

Time: May 31 2024
Space: Unknown

Time: May 31 2024
Space: Unknown

Time: May 31 2024
Space: Unknown

Where? Who? When?

Entitity reconciliation
Space/Time Reconciliation

---

## gsw_example3.pdf

### Page 1

Julian Ross
hackathon

Role: Participant in hackthon 
State: Winner
Emotional State:

-> ?

participate
Silicon Beach

When did Julian Ross participate in Hackathon?

Possible Questions | Answerable | Answer | Comments
May 31 2024 | Yes
When did the Hackathon take place? | Yes | May 31 2024
Where did the Hackathon take place? | Yes | Silicon Beach
Who won the Hackathon? | Yes | Julian Ross

...... as nighttime set on a cold night at Silicon Beach, Julian Ross emerged victorious after hours of intense focus, his innovative project securing the win and leaving him jubilant at the outcome.

Role: Location 
win

Role: Event 

In what? Who? Where? What? Who? Where?

Time: May 31 2024
Space: Silicon Beach

Time: May 31 2024
Space: Silicon Beach

Entitity reconciliation
Space/Time Reconciliation
Space/Time Reconciliation
Entity Reconciliation

---

## GSW_pipeline-2.pdf

### Page 1

Operator
Operator

Populating the Workspace

Task-specific Adaptation: Question Answering

documents
chunks

Operator
Reconciler

semantics: roles, states, verbs, valences, actors, questions, time and space

question
entities
summaries

reranker
LLM
answer

---

## GSW_QA_pipeline_small.pdf

### Page 1

Input Query: Reflect on the experiences of Carter Stewart related to Scientific Conference. List all the unique locations where these events took place, without mentioning the events themselves.

Named Entities: Carter Stewart, Scientific Conference

Retrieved Summaries:

Chapter 29:
Entity: Carter Stewart - Summary: On January 3, 2026, at Yankee Stadium, Carter Stewart, a performer and mime artist, was preparing for a significant performance....

Chapter 49:
Entity: Carter Stewart - Summary: Entity: Carter Stewart - Summary: On September 22, 2026, during the morning sessions of a scientific conference at the Metropolitan Museum of Art, Carter Stewart took on the role of a presenter,....
Entity: The scientific conference - Summary: The scientific conference, held on September 22, 2026, was a pivotal moment that took place at the Metropolitan Museum of Art. This event was attended by various individuals

Chapter 134:
Entity: Carter Stewart - Summary: On December 25, 2025, Carter Stewart organized a literary-themed festival at Yankee Stadium, stepping onto the field with a sense of pride as both an organizer and participant...
Entity: Carter Stewart's pocket watch - Summary: On December 25, 2025, Carter Stewart's pocket watch, a timekeeping device adorned with intricate clockwork gears and miniature constellations....

Chapter 166:
Entity: Carter Stewart - Summary: On March 23, 2024, Carter Stewart, a researcher and presenter, stepped onto the Bethpage Black Course to present his research findings at a Scientific Conference...
Entity: Scientific Conference - Summary: The Scientific Conference, held at the Bethpage Black Course on March 23, 2024, was an event that buzzed with anticipation as it unfolded in a unique setting—a golf course....

Reranked Summaries:

Chapter 166:
Entity: Carter Stewart - Summary: On March 23, 2024, Carter Stewart, a researcher and presenter, stepped onto the Bethpage Black Course to present his research findings at a Scientific Conference...
Entity: Scientific Conference - Summary: The Scientific Conference, held at the Bethpage Black Course on March 23, 2024, was an event that buzzed with anticipation as it unfolded in a unique setting—a golf course....

Chapter 49:
Entity: Carter Stewart - Summary: Entity: Carter Stewart - Summary: On September 22, 2026, during the morning sessions of a scientific conference at the Metropolitan Museum of Art, Carter Stewart took on the role of a presenter,....
Entity: The scientific conference - Summary: The scientific conference, held on September 22, 2026, was a pivotal moment that took place at the Metropolitan Museum of Art. This event was attended by various individuals

....

Final Answer: Bethpage Black Course, Metropolitan Museum of Art

Other reranked summaries

---

## prompts/GSW_prompt_operator.pdf

### Page 1

User Prompt: 

You are required to perform the operator extraction, you should follow the following steps:

Task 1: Actor Identification

Your first task is to identify all actors from the given context. An actor can be:
1. A person (e.g., directors, authors, family members)
2. An organization (e.g., schools, festivals)
3. A place (e.g., cities, countries)
4. A creative work (e.g., films, books)
5. A temporal entity (dates, years)
6. A physical object or item (e.g., artifacts, products) 
7. An abstract entity (e.g., awards, concepts that function as actors)

Guidelines for Actor Extraction:
- Ground actor extraction in the given situation (<situation>) and the background context (<background_context>).
- It is crucial that you follow the above, since we will attempt to merge relevant actors across chunks in the next step.
- If an entity mentioned in the <input_text> (e.g., 'the journey', 'the event', 'the project') is clearly a direct reference to the overall <situation>, you should name the extracted actor based on the situation description itself.
- Include all mentioned dates as temporal entities
- Do not include phrases or complete sentences
- Extract each actor only once, even if mentioned multiple times

[Further guidelines omitted for brevity]

Task 2: Role Assignment
[Description of role assignment task]

Task 3: State Identification
[Description of state identification task]

Task 4: Explicit Verb Phrase Identification
[Description of verb phrase identification task]

Task 4.5: Implicit Action Phrase Inference
[Description of implicit action phrase inference task]

Task 5: Prototypical Semantic Role Question Generation
[Description of semantic role question generation task]

Task 6: Answer Mapping and Actor Connection
[Description of answer mapping task]

Inputs:
Input Text: "Input chunk to be processed by the operator" 
Background Context: "This chunk places the chunking within the entire document, providing context to the chunk.
Situation: "The situation that is presented in this chunk"

---

## prompts/GSW_prompt_QA.pdf

### Page 1

User Prompt:

You are a question answering agent that only uses provided information to answer questions.

Your task is to answer questions based exclusively on the knowledge graph information provided. Do not use any external knowledge.

The information provided is extracted from a Generative Semantic Workspace (GSW) representation, which captures:
- Entities: People, places, objects, and concepts
- Verb Phrases: Actions or events involving the entities
- Spatial Relationships: Locations of entities
- Temporal Relationships: Time periods of entities

We use the GSW to extract entity summaries, and you will be provided with these summaries along with graph structure for the GSW for each relevant chapter in order to answer the question.

Always ground your answer in the provided information, and only provide answers for which there is clear evidence in the information provided. If the information needed is not available, state that you cannot answer based on the available information.

Please answer the following question using ONLY the information provided in the knowledge base extract below.

First determine which chapters are most likely to contain relevant information based on the question, then based on the entity summaries and the graph structure for those chapters, determine the most likely answer.

Answers will always be a SINGLE entity representing a person, event, location or time period. It will not be a description or a concept.

QUESTION: questions

KNOWLEDGE BASE INFORMATION: gsw summaries

First provide a reasoning for which chapters are most likely to contain relevant information based on the question.

Then provide a reasoning for which entity is most likely to be the correct answer based on the entity summaries and the graph structure for those chapters.

Inputs:
Question: "Question to be answered"
GSW Summaries: "Summaries produced by the GSW relevant to answer questions"

---

## prompts/GSW_prompt_reconcile.pdf

### Page 1

User Prompt:

You are an expert question answering system. Analyze the provided text and answer the specified questions based ONLY on the text. Provide answers in the specified JSON format.

Your task is to determine if the Text Chunk provides a specific answer for any of these unanswered questions. Base your answers ONLY on the provided Text Chunk.

Respond ONLY with a JSON list containing objects for the questions you can now answer. Each object should have:
- "question_id": The ID of the question being answered.
- "answer_text": The specific text snippet from the Text Chunk that answers the question.
- "answer_entity_id": (Optional) If the answer corresponds exactly to one of the Entities Introduced in This Chunk, provide its ID. Otherwise, omit this field or set it to null.

If no questions can be answered from the text, respond with an empty JSON list: []

Inputs:
Input Text: "Input chunk to be processed by the operator" 
Entities: "Entities that were introduced in this chunk"
Unanswered Questions: "Unanswered questions that could be answered"

---

## prompts/GSW_prompt_spacetime.pdf

### Page 1

User Prompt:

You are a helpful assistant that is an expert at understanding spatio-temporal relationships between entities. You will be given a list of entities along with the context of the narrative in which they appear. Your task is to link entities that share a spatio-temporal relationship. Read the `Text Chunk` and examine the entities in the `Operator Output`. Identify groups of entity IDs that share the same location (spatial context) or the same time/date (temporal context) based on the events described.

The entities have the following attributes:
* `id`: (String) The entity ID.
* `name`: (String) The entity name.
* `roles`: A role is a situation-relevant descriptor (noun phrase) that describes how an actor functions or exists within the context. Roles define the potential relationships an actor can have with other actors.
* `states`: A state is a condition or description (using adjectives or verb phrases) that characterizes how an actor exists in their role at a specific point. States provide additional context about the actor's condition, status, or situation. 

Return a JSON object with a single key "spatio_temporal_links". The value should be a list of link objects. Each link object must have:
* `linked_entities`: (List of Strings) Entity IDs sharing the context (e.g., `["e1", "e2", "e3"]`).
* `tag_type`: (String) Either "spatial" or "temporal".
* `tag_value`: (String or Null)
    * If the specific location/time/date is mentioned in the `Text Chunk` for this group, extract it.
    * Otherwise, use `null`.

Inputs:
Input Text: "Input chunk used to perform linking" 
Operator Output: "Operator output for above chunk"

---

## prompts/GSW_prompt_summary.pdf

### Page 1

User Prompt:

You are an expert narrative summarizer. Your task is to create a concise, chronological summary paragraph about a single entity based on structured information extracted from a text. Focus on creating a coherent story of the entity's involvement and changes based *only* on the provided timeline.

INSTRUCTIONS:
1. Write a single paragraph summarizing the key roles, states, experiences, and actions of the entity.
2. Follow the chronological order presented by the Chunk IDs.
3. Integrate the roles, states, and actions into a coherent narrative. Mention key interactions with other entities or objects when provided in the context.
4. You will be provided with spatial and temporal context for entity.
5. These will be provided in the form of a timeline of how they were captured in the text, be sure to incorporate all this spatial and temporal information particularly, provide importance to specific information (like name of place/ explicit dates etc.).
6. Focus on what entity did, what roles they held, their state of being, where they were located, when events happened, and significant events they participated in.
5. Keep the summary concise and factual according to the input. Do not add outside information or make assumptions.
6. Output *only* the summary paragraph, with no preamble or markdown formatting.

Inputs:
Input Entity: "Entity with role/state information and space/time links as well as questions answered by it."
