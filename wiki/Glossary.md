# Glossary

Terminology used in the Verridian AI system.

---

## A

### Active Inference
A neuroscience-based framework where agents minimize "free energy" by both updating beliefs (perception) and taking actions (behavior). Used in the Agency layer for gap detection.

### Actor
A semantic entity in the GSW workspace. Can be a person, asset, date, institution, or abstract concept. Actors have roles, states, and relationships.

### Actor-Centric Memory
Memory model where information is organized around entities (actors) rather than events. Contrasts with verb-centric models.

---

## B

### Binding
VSA operation that creates a new hypervector from two inputs via element-wise multiplication. The result is dissimilar to both inputs. Used to create role-filler pairs.

### Bundling
VSA operation that combines multiple hypervectors via element-wise addition and sign function. The result is similar to all inputs. Used to represent sets.

---

## C

### ChunkExtraction
Data structure containing all extracted information from a text chunk: actors, verb phrases, questions, and spatio-temporal links.

### Cognitive Architecture
System design inspired by how the human brain processes information. Verridian uses a three-layer architecture (TEM, Agency, VSA).

---

## D

### Dimension (D)
The size of hypervectors in VSA. Verridian uses D=10,000. Higher dimensions provide more capacity but require more computation.

---

## E

### EFE (Expected Free Energy)
Quantity minimized during action selection in Active Inference. Combines pragmatic value (utility) and epistemic value (information gain).

### Epistemic Value
Component of EFE measuring how much an action reduces uncertainty. Actions with high epistemic value are "curious" or "exploratory."

---

## F

### Family Law Act 1975
Australian federal legislation governing family law matters including divorce, property settlement, and parenting arrangements.

### Free Energy
In Active Inference, a quantity that bounds surprise. Agents minimize free energy to maintain predictable states.

---

## G

### Gap Detection
The system's ability to identify missing evidence or information before answering a query. Implemented via the Agency layer.

### Grid Cells
Neurons in the brain's entorhinal cortex that fire in regular spatial patterns. Implemented in TEM's TransitionModule.

### GSW (Global Semantic Workspace)
The memory system that stores actor-centric representations. Inspired by Global Workspace Theory from consciousness research.

---

## H

### Hallucination
When an AI system generates false or unsupported information. Verridian uses VSA logic rules to prevent hallucination.

### Hebbian Learning
Learning rule where connections strengthen when neurons fire together. Used in TEM's memory update: "Neurons that fire together, wire together."

### Hyperdimensional Computing
Computing paradigm using high-dimensional vectors (D > 1000). Properties include near-orthogonality of random vectors and robust composition operations.

### Hypervector
High-dimensional vector (D=10,000) representing a concept. In Verridian, uses bipolar representation {-1, 1}.

---

## L

### LEC (Lateral Entorhinal Cortex)
Brain region processing sensory information. Implemented in TEM's SensoryModule.

### Legal Operator
Main extraction class that implements the 6-task pipeline for converting legal text to structured data.

---

## M

### MEC (Medial Entorhinal Cortex)
Brain region containing grid cells for spatial navigation. Implemented in TEM's TransitionModule.

### Mem0
External memory service used for persistent context across sessions.

---

## O

### Ontology
Structured vocabulary of legal concepts used for consistency. Includes entity types, relationships, and logic rules.

### OpenRouter
API gateway providing access to multiple LLM providers (Google, Anthropic, OpenAI).

---

## P

### Path Integration
Navigation method using internal motion signals rather than external landmarks. TEM uses path integration to navigate abstract legal spaces.

### Permutation
VSA operation that cyclically shifts vector elements. Used to encode sequences or order.

### POMDP
Partially Observable Markov Decision Process. Mathematical framework for decision-making under uncertainty. Used in Agency module.

### Pragmatic Value
Component of EFE measuring how much an action achieves desired goals. Actions with high pragmatic value are "useful."

---

## R

### RAG (Retrieval-Augmented Generation)
Standard approach where relevant documents are retrieved and provided to an LLM. Verridian extends RAG with cognitive processing.

---

## S

### Spatio-Temporal Link
Connection between actors with temporal or spatial context. Examples: "married_to (2008-2023)", "located_at (Sydney)".

### State
Time-varying property of an actor. Examples: marital status, employment status, health condition.

---

## T

### TEM (Tolman-Eichenbaum Machine)
Neural architecture that separates structural knowledge from sensory content. Named after psychologist Edward Tolman and neuroscientist Howard Eichenbaum.

### Three-Layer System
Verridian's cognitive architecture:
1. Navigation (TEM) - Structure/content separation
2. Agency (Active Inference) - Gap detection
3. Logic (VSA) - Anti-hallucination

---

## V

### VFE (Variational Free Energy)
Quantity minimized during perception in Active Inference. Measures difference between beliefs and observations.

### Verb Phrase
Action or relation connecting actors. Example: "Smith (applicant) seeks property settlement from Smith (respondent)."

### VSA (Vector Symbolic Architecture)
Computing paradigm using hyperdimensional vectors for symbolic reasoning. Enables anti-hallucination verification.

---

## Related Pages

- [Architecture-Overview](Architecture-Overview) - System design
- [Three-Layer-System](Three-Layer-System) - Layer details
- [File-Index](File-Index) - Code organization
