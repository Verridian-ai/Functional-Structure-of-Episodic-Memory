"""
TOON Integration for Ingestion Pipeline
========================================
Provides utilities to batch and convert classified documents to TOON format
for efficient storage and downstream processing.
"""

from typing import List, Dict, Any
from src.utils.toon import ToonEncoder

# Define columns for the LegalDocument TOON table
DOC_HEADERS = [
    "citation",
    "type",
    "jurisdiction",
    "domain",
    "category",
    "court",
    "court_level",
    "score",
    "legislation_refs",
    "case_refs",
    "text"
]

def convert_doc_to_row(doc: Dict[str, Any]) -> List[str]:
    """
    Convert a classified document dictionary to a list of values for TOON.
    """
    # Extract classification metadata
    classification = doc.get("_classification", {})
    
    # Format lists as pipe-separated strings
    leg_refs = "|".join(classification.get("legislation_refs", []))
    case_refs = "|".join(classification.get("case_refs", []))
    
    return [
        doc.get("citation", ""),
        doc.get("type", ""),
        doc.get("jurisdiction", ""),
        classification.get("primary_domain", "Unclassified"),
        classification.get("primary_category", "Unclassified"),
        classification.get("court", "") or "",
        classification.get("court_level", "") or "",
        str(classification.get("authority_score", 0)),
        leg_refs,
        case_refs,
        doc.get("text", "")  # Full text
    ]

def batch_to_toon(docs: List[Dict[str, Any]], table_name: str = "LegalDocs") -> str:
    """
    Convert a batch of documents to a TOON block.
    
    Args:
        docs: List of document dictionaries
        table_name: Name of the TOON table (default: LegalDocs)
        
    Returns:
        Formatted TOON string
    """
    if not docs:
        return ""
        
    data = [convert_doc_to_row(doc) for doc in docs]
    return ToonEncoder.encode(table_name, DOC_HEADERS, data)
