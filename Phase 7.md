1. The Navigation Layer: Tolman-Eichenbaum Machines (TEM)The Problem: Your GSW knows "Case A happened." But it doesn't intuitively understand how Case A relates to Case B in the "conceptual space" of law.The Brain Inspiration: The Hippocampus and Entorhinal Cortex.2How it works: Your brain doesn't just store memories; it maps them. It uses "Place Cells" (to know where you are) and "Grid Cells" (to measure distance/direction).3The Tech: Tolman-Eichenbaum Machines (TEM).TEMs generalize structural knowledge. If you learn how a "family" works in one legal case (Father, Mother, Child), a TEM creates a "schema" that instantly understands the structure of a new family case without relearning the concept of "family."Implementation: Use TEMs to factorize your data. Separate the "Sensory" data (the specific names/dates of a case) from the "Structural" data (the abstract relationship of Applicant vs. Respondent).Why for Legal? It allows "Zero-Shot Inference." The system can infer the existence of a hidden asset in a new case because the structure matches a previous fraud case, even if the text is totally different.2. The Agency Layer: Active Inference (The Friston Framework)4The Problem: Current AI is passive. It waits for a query. A human lawyer is active; they anticipate risks.The Brain Inspiration: The Free Energy Principle (Karl Friston).5How it works: The brain is a prediction machine, not a reaction machine. It constantly predicts sensory input and acts to minimize "surprise" (prediction error).The Tech: Active Inference Agents.Instead of "Input -> Output," the loop is "Belief -> Action -> Observation -> Update Belief."Implementation: Don't just ask the agent to "summarize this case." Give the agent a Generative Model of a "Perfect Legal Judgment" and tell it to minimize the divergence between that model and the messy raw text.Why for Legal? This powers your Phase 6. If the agent sees a "Financial Agreement" but no "Independent Legal Advice" certificate, an Active Inference agent experiences "surprise" (High Free Energy) and autonomously generates a query to find the missing certificate, without you asking.3. The Logic Layer: Vector Symbolic Architectures (VSA) / Hyperdimensional ComputingThe Problem: Neural Networks are "fuzzy" (probabilistic). Law is "crisp" (symbolic). You cannot be "80% guilty."The Brain Inspiration: Neuro-Symbolic Binding.How it works: The brain creates explicit symbols ("The Law") that bind to variable instances ("This Person") without losing the distinctness of either.The Tech: Holographic / Hyperdimensional Computing.It uses massive vectors (10,000+ dimensions) where operations are algebra (XOR, Permutation).Implementation: You can mathematically "bind" a Role (Applicant) to a Filler (Mr. Smith) and a Rule (Section 79).Why for Legal? It solves the "Variable Binding Problem." It ensures that when the AI reasons about Assets, it doesn't accidentally hallucinate Liabilities just because the words often appear together. It keeps the variables mathematically distinct.Summary: The "Brain-Inspired" GSW StackIf you are writing this up for your Dev Log or Research Plan, here is how these layers fit into your Generative Semantic Workspace:LayerBrain RegionTechnologyFunction in Legal AI1. MemoryNeocortexGSW (Your Project)Stores the specific narratives and timelines of cases.2. StructureHippocampusTolman-Eichenbaum MachineMaps the "Legal Space." Recognizes that this divorce follows the same structural path as that precedent.3. AgencyBasal GangliaActive InferenceDrives the "Curiosity." Notices missing evidence and actively seeks to resolve the gap (Minimizing Free Energy).4. LogicPrefrontal CortexNeuro-Symbolic / VSAApplies the "Rules." Ensures strict adherence to the Family Law Act without "fuzzy" hallucination.Next Step: Would you like me to create a "Phase 7" research plan specifically for integrating an Active Inference loop (Layer 3) to automate the "missing evidence" detection?


This is an excellent instinct. If you want to build a "Generative Semantic Workspace" that outperforms standard RAG, you need to look at the Cognitive Science literature, not just the Computer Science literature.

Here are the specific, high-impact papers you should read to implement the "Navigation, Agency, Logic" stack I described. I have selected papers that are recent (2024–2025) or foundational, specifically chosen for their applicability to your Legal AI.

1. The Navigation Layer (Structure & Analogies)
Technology: Tolman-Eichenbaum Machines (TEM) Why read this: These papers explain how to separate "Abstract Legal Structure" (e.g., the concept of a breach of contract) from "Specific Case Facts" (Dates, Names), allowing your AI to instantly understand a new case because it recognizes the shape of the problem.

The Breakthrough Paper (2025):

Title: "The Spiking Tolman-Eichenbaum Machine: Emergent Spatial and Temporal Coding through Spiking Network Dynamics"

Authors: Kawahara & Fujisawa (RIKEN Center for Brain Science)

Key Insight: This paper extends the original TEM to include time. In Law, the sequence of events is as important as the events themselves. This paper shows how to model "temporal structural knowledge" (e.g., A must happen before B).

The Foundational Paper:

Title: "The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation"

Authors: Whittington et al. (Oxford/DeepMind)

Key Insight: This is the "User Manual" for building a TEM. It details how to factorize data into "Sensory" (Facts) and "Structural" (Rules) components.

Your Implementation: Use this to build a "Legal Geometry" where cases with similar legal principles are clustered together, even if the keywords are totally different.

2. The Agency Layer (Curiosity & Evidence Seeking)
Technology: Active Inference & The Free Energy Principle Why read this: These papers move your agent from a "Chatbot" (Passive) to an "Investigator" (Active). They define the math for an agent that feels uncomfortable (High Free Energy) when data is missing and acts to fix it.

The "Manifesto" Paper (2025):

Title: "The Missing Reward: Active Inference in the Era of Experience"

Context: Discusses replacing manual "Reward Functions" (RLHF) with an intrinsic drive to minimize uncertainty.

Key Insight: Instead of training your Legal AI to "give good answers," you train it to "minimize ambiguity." If a user says "I want a divorce," the agent shouldn't just answer; it should realize the ambiguity of "property settlement?" and ask clarifying questions automatically.

The Practical Guide:

Title: "A Free Energy Principle for Artificial Intelligence" (or look for Karl Friston's 2024/2025 surveys on "Active Inference Agents").

Key Insight: Look for the concept of "Epistemic Foraging." This is the technical term for "curiosity."

Your Implementation: When your GSW scans a case, if it finds a "Gap" in the timeline (e.g., no data for 2003-2005), an Active Inference agent will flag this as "High Entropy" and generate a specific task to find that missing data.

3. The Logic Layer (Strict Rule Application)
Technology: Vector Symbolic Architectures (VSA) / Hyperdimensional Computing Why read this: These papers describe how to do algebra with concepts. This is how you ensure your AI doesn't hallucinate. It allows you to bind "Variable: Assets" to "Value: $1M" and "Rule: s79(4)" without them getting mixed up.

The "New Architecture" Paper (IBM Research):

Title: "Neuro-Vector-Symbolic Architecture: Combining the strengths of Symbolic AI and Neural Nets"

Authors: Hersche et al. (IBM Research Zurich)

Key Insight: They describe a system that uses "High-Dimensional Vectors" to represent symbols. They demonstrate solving "Raven's Progressive Matrices" (IQ tests) using this method.

Your Implementation: Legal reasoning is an IQ test. "If A is an Asset, and B is a Liability, calculate Net Pool." VSA allows you to perform this calculation symbolically (perfect accuracy) while still using a Neural Network for the language part.

The Survey:

Title: "Hyperdimensional Computing: A Framework for Stochastic Computation and Symbolic AI" (2024/2025 Survey in Journal of Big Data)

Key Insight: Look for the section on "Variable Binding" and "Superposition." This explains how to store 100 different facts about a case in a single vector without losing the ability to query individual facts perfectly.

Summary of Your Reading List
For Structure: Whittington et al. on Tolman-Eichenbaum Machines (DeepMind).

For Agency: Karl Friston's recent work on Active Inference (VERSES AI / UCL).

For Logic: IBM Research's work on Neuro-Vector-Symbolic Architectures (NVSA).

Next Step: Would you like me to "decompress" one of these specific papers (e.g., the Whittington TEM paper) and write a summary of exactly how its architecture could be converted into Python code for your "Phase 7"?


This matches the level of ambition required for a "Phase 7" implementation. You are looking for the "Source Code of Cognition."

Here are the direct links to the papers and the most usable GitHub repositories for each.

### 1\. The Navigation Layer (Tolman-Eichenbaum Machines)

**The Paper:**

  * **Foundational (Must Read):** *The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation* (Whittington et al., 2020).
      * [Read the Paper (Cell)](https://www.google.com/search?q=https://www.cell.com/cell/pdf/S0092-8674\(20\)31388-4.pdf)
  * **The 2025 Upgrade:** *The Spiking Tolman-Eichenbaum Machine* (Kawahara & Fujisawa, Oct 2025).
      * [Read the Paper (bioRxiv)](https://www.biorxiv.org/content/10.1101/2025.10.16.682754v1)

**The Code:**

  * **Best Implementation (PyTorch):** The original DeepMind code is in TensorFlow 1 (painful to use). Use this community rewrite in PyTorch which is actively maintained and much cleaner.
      * [GitHub: jbakermans/torch\_tem](https://github.com/jbakermans/torch_tem)
  * **Official (TensorFlow 2):** If you strictly want the authors' code (Whittington).
      * [GitHub: djcrw/generalising-structural-knowledge](https://github.com/djcrw/generalising-structural-knowledge)

### 2\. The Agency Layer (Active Inference)

**The Paper:**

  * **The "Manifesto" (2025):** *The Missing Reward: Active Inference in the Era of Experience* (Wen et al., IBM Research).
      * [Read the Paper (arXiv)](https://arxiv.org/abs/2508.05619)

**The Code:**

  * **The Standard Library:** Don't build this from scratch. Use `pymdp`, the standard Python library for Active Inference agents. It handles the complex "Expected Free Energy" calculations (the $G$ value) for you.
      * [GitHub: infer-actively/pymdp](https://github.com/infer-actively/pymdp)
      * *Note:* The "Missing Reward" paper is theoretical, but you can implement its "intrinsic curiosity" logic by simply setting the `EFE` (Expected Free Energy) term in `pymdp` to prioritize *Information Gain* over *Extrinsic Reward*.

### 3\. The Logic Layer (Neuro-Vector-Symbolic Architectures)

**The Paper:**

  * **The Architecture:** *A Neuro-vector-symbolic architecture for Solving Raven's Progressive Matrices* (Hersche et al., Nature Machine Intelligence, 2023).
      * [Read the Paper (Nature)](https://www.nature.com/articles/s42256-023-00630-8)

**The Code:**

  * **Official IBM Research Repo:** This contains the code for "binding" symbols (vectors) together. It is essential for the "Rule Application" phase where you need to bind `Section 79` to `Asset_Value` without hallucination.
      * [GitHub: IBM/neuro-vector-symbolic-architectures-raven](https://github.com/IBM/neuro-vector-symbolic-architectures-raven)

-----

### Implementation Strategy for "Phase 7"

If you are building this alone, **do not try to implement all three at once.**

1.  **Start with `pymdp` (Active Inference).** It is the easiest "brain upgrade" to install. You can wrap your current RAG pipeline in a `pymdp` agent loop:
      * *Belief* = Context Retrieved.
      * *Action* = Generate Query.
      * *Observation* = New Text.
      * *Goal* = Minimize "Uncertainty" (entropy of the answer).

Would you like me to write a `main.py` script that wraps your current GSW "Reconciler" inside a `pymdp` Active Inference loop?

[Active Inference Framework in Python](https://www.youtube.com/watch?v=kGRczFpO8zQ)

This video demonstrates the `pymdp` library in action, showing how to structure an agent that minimizes free energy (uncertainty) rather than just maximizing reward, which is the core mechanic you need for your self-correcting legal AI.

http://googleusercontent.com/youtube_content/0