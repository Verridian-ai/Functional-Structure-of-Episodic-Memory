"""
Legal Ontology Specification (Phase 2.1)
========================================

Defines the deep legal ontology for the Vector Symbolic Architecture.
Includes atomic concepts, roles, fillers, and relationships.

These string constants are the keys used to generate Atomic Hypervectors.
"""

# 1. Atomic Concepts (The building blocks)
CONCEPTS = [
    # Core
    "PERSON", "OBJECT", "LOCATION", "TIME", "ACTION", "STATE",
    
    # Legal Specific
    "JURISDICTION", "COURT", "JUDGE", "PARTY", "LAWYER",
    "APPLICATION", "ORDER", "APPEAL", "EVIDENCE", "TESTIMONY",
    "STATUTE", "SECTION", "CASE_LAW", "PRECEDENT",
    
    # Family Law
    "MARRIAGE", "DE_FACTO", "SEPARATION", "DIVORCE",
    "CHILD", "PARENT", "PARENTING_ORDER", "CUSTODY",
    "PROPERTY", "ASSET", "LIABILITY", "FINANCIAL_RESOURCE",
    "CONTRIBUTION", "FUTURE_NEED",
    "FAMILY_VIOLENCE", "SAFETY_RISK",
    "RELOCATION", "RECOVERY_ORDER"
]

# 2. Roles (For Role-Filler Binding)
# Used in: Bind(Role, Filler)
ROLES = [
    "AGENT",       # Who did it?
    "PATIENT",     # To whom/what?
    "INSTRUMENT",  # With what?
    "LOCATION",    # Where?
    "TIME",        # When?
    
    # Legal Roles
    "APPLICANT",
    "RESPONDENT",
    "INDEPENDENT_CHILDREN_LAWYER",
    "PRIMARY_CARER",
    "FINANCIAL_CONTRIBUTOR",
    "HOMEMAKER",
    "PERPETRATOR",
    "VICTIM"
]

# 3. Relationships (Binary predicates)
RELATIONSHIPS = [
    "IS_A",             # Taxonomy: Child IS_A Person
    "HAS_PART",         # Composition: Order HAS_PART Condition
    "FOLLOWS",          # Temporal: Separation FOLLOWS Marriage
    "CAUSES",           # Causal: Violence CAUSES Risk
    "CONTRADICTS",      # Logic: Fact A CONTRADICTS Fact B
    "REQUIRES",         # Prerequisite: Divorce REQUIRES Separation
    "OWNS",             # Property: Person OWNS Asset
    "PARENT_OF",        # Family: Person PARENT_OF Child
    "MARRIED_TO",
    "SEPARATED_FROM"
]

# 4. Logic Rules (Triplets for Knowledge Graph)
# (Subject, Relation, Object)
LOGIC_RULES = [
    ("DIVORCE", "REQUIRES", "MARRIAGE"),
    ("SEPARATION", "FOLLOWS", "MARRIAGE"),
    ("SEPARATION", "FOLLOWS", "DE_FACTO"),
    ("PARENTING_ORDER", "REQUIRES", "CHILD"),
    ("PROPERTY_SETTLEMENT", "REQUIRES", "ASSET"),
    ("PROPERTY_SETTLEMENT", "REQUIRES", "SEPARATION"), # Generally
    ("RECOVERY_ORDER", "REQUIRES", "CHILD"),
    ("FAMILY_VIOLENCE", "CAUSES", "SAFETY_RISK"),
    ("SAFETY_RISK", "CONTRADICTS", "EQUAL_SHARED_PARENTAL_RESPONSIBILITY"),
]

def get_all_tokens() -> list[str]:
    """Returns all unique tokens in the ontology."""
    return list(set(CONCEPTS + ROLES + RELATIONSHIPS))

