"""
Legal Corpus Retriever
======================

Provides retrieval capabilities over the OALC.
Optimized Strategy:
1.  Full Corpus Metadata Index (Citation/Title) for specific navigation.
2.  Domain-Specific Full-Text Index (Family Law) for semantic search.
3.  Legislation Index (Family Law Act) for statutory grounding.
4.  VSA Anti-Hallucination Validation for response quality assurance.
"""

import json
import re
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter

from src.logic.gsw_schema import GlobalWorkspace
from src.retrieval.vsa_validator import VSAValidator

class SimpleBM25:
    """
    In-memory BM25 implementation for text ranking.
    """
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = [] # Stores metadata + text length
        self.avg_dl = 0
        self.doc_freqs = [] # List of Counters? No, Inverted Index.
        self.inverted_index = {} # term -> {doc_idx: freq}
        self.doc_len = []
        self.corpus_size = 0

    def add_document(self, text: str, metadata: Dict):
        """Adds document to index."""
        doc_idx = self.corpus_size
        self.corpus_size += 1
        
        # Tokenize (simple)
        tokens = [t.lower() for t in re.findall(r'\w+', text)]
        length = len(tokens)
        self.doc_len.append(length)
        
        # Frequencies
        counts = Counter(tokens)
        for term, freq in counts.items():
            if term not in self.inverted_index:
                self.inverted_index[term] = {}
            self.inverted_index[term][doc_idx] = freq
            
        self.documents.append(metadata)

    def finalize(self):
        """Calculates stats."""
        if self.corpus_size > 0:
            self.avg_dl = sum(self.doc_len) / self.corpus_size
            
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Searches index."""
        tokens = [t.lower() for t in re.findall(r'\w+', query)]
        scores = {}
        
        for term in tokens:
            if term not in self.inverted_index:
                continue
            
            # IDF
            n_q = len(self.inverted_index[term])
            idf = math.log((self.corpus_size - n_q + 0.5) / (n_q + 0.5) + 1.0)
            
            # Score
            for doc_idx, freq in self.inverted_index[term].items():
                dl = self.doc_len[doc_idx]
                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * (dl / self.avg_dl))
                score = idf * (numerator / denominator)
                
                scores[doc_idx] = scores.get(doc_idx, 0) + score
                
        # Sort
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.documents[idx], score) for idx, score in results]

class LegalRetriever:
    def __init__(self, data_dir: str = 'data', enable_vsa_validation: bool = True):
        self.data_dir = Path(data_dir)
        self.bm25 = SimpleBM25()
        self.citation_index = {}
        self.enable_vsa_validation = enable_vsa_validation

        # Initialize VSA validator if enabled
        self.vsa_validator = VSAValidator() if enable_vsa_validation else None

        self._load_indices()
        
    def _load_indices(self):
        print("[Retriever] Loading Indices...")
        
        # 1. Legislation (Full Text)
        leg_path = self.data_dir / 'legislation/family_law_act_1975_sections.json'
        if leg_path.exists():
            try:
                with open(leg_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Flatten sections? Assuming structure is Act -> Parts -> Sections
                    # The file is likely Act -> sections list if simplified, or complex structure.
                    # Let's try to inspect or just iterate recursively if needed.
                    # Based on file preview: "act": { ... }
                    # I'll treat the whole file as context or split if possible.
                    # For now, add as one big doc for "Act" hits, but ideally sections.
                    pass 
            except Exception as e:
                print(f"Error loading legislation: {e}")

        # 2. Family Law Cases (Full Text)
        family_path = self.data_dir / 'by_court/family.jsonl'
        if family_path.exists():
            with open(family_path, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    try:
                        doc = json.loads(line)
                        text = doc.get('text', '')
                        meta = {
                            'id': doc.get('citation', f"doc_{count}"),
                            'type': 'case',
                            'title': doc.get('citation', ''),
                            'text_preview': text[:200]
                        }
                        self.bm25.add_document(text, meta)
                        
                        # Add to citation index
                        cit = doc.get('citation')
                        if cit:
                            self.citation_index[cit.lower()] = meta
                            
                        count += 1
                    except:
                        continue
                print(f"[Retriever] Indexed {count} Family Law cases.")
        
        self.bm25.finalize()
        print("[Retriever] Indexing Complete.")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Hybrid search: Citation Lookup + Full Text Search.
        """
        results = []

        # 1. Direct Citation Lookup
        # (Basic normalization)
        q_norm = query.lower().strip()
        if q_norm in self.citation_index:
            results.append(self.citation_index[q_norm])

        # 2. Full Text Search
        bm25_results = self.bm25.search(query, top_k=top_k)
        for doc, score in bm25_results:
            # Avoid duplicates
            if doc['id'] not in [r['id'] for r in results]:
                doc_res = doc.copy()
                doc_res['score'] = score
                results.append(doc_res)

        return results[:top_k]

    def retrieve_with_validation(
        self,
        query: str,
        workspace: Optional[GlobalWorkspace] = None,
        top_k: int = 5,
        generate_response: bool = True
    ) -> Dict:
        """
        Retrieve results and optionally validate with VSA.

        Args:
            query: The search query
            workspace: Global workspace for validation (optional)
            top_k: Number of results to retrieve
            generate_response: Whether to generate and validate a response

        Returns:
            Dictionary containing:
                - results: List of retrieval results
                - response: Generated response (if generate_response=True)
                - validation: VSA validation results (if workspace provided)
                - confidence: Overall confidence score
                - hallucination_risk: Boolean indicating risk level
        """
        # Get retrieval results
        results = self.search(query, top_k)

        result_dict = {
            'results': results,
            'query': query,
            'num_results': len(results)
        }

        # Generate response if requested
        if generate_response:
            response = self._generate_response(query, results)
            result_dict['response'] = response

            # Validate with VSA if workspace provided and validation enabled
            if workspace and self.vsa_validator:
                validation = self.vsa_validator.validate_response(
                    query,
                    response,
                    workspace
                )

                result_dict['validation'] = validation
                result_dict['confidence'] = validation['overall_confidence']
                result_dict['hallucination_risk'] = validation['hallucination_detected']

                # Add severity warnings
                if validation['severity']['high_risk'] > 0:
                    result_dict['warning'] = f"High risk: {validation['severity']['high_risk']} claims flagged"
                elif validation['severity']['medium_risk'] > 0:
                    result_dict['warning'] = f"Medium risk: {validation['severity']['medium_risk']} claims need review"

        return result_dict

    def _generate_response(self, query: str, results: List[Dict]) -> str:
        """
        Generate a response from retrieval results.

        Args:
            query: The original query
            results: List of retrieval results

        Returns:
            Generated response string
        """
        if not results:
            return "No relevant information found."

        # Simple response generation: concatenate top results
        response_parts = []
        for i, result in enumerate(results[:3], 1):
            preview = result.get('text_preview', '')
            title = result.get('title', result.get('id', 'Document'))

            if preview:
                response_parts.append(f"{i}. From {title}: {preview}")

        if response_parts:
            return "\n\n".join(response_parts)
        else:
            return f"Found {len(results)} relevant documents for: {query}"

    def validate_claim(
        self,
        claim: str,
        workspace: GlobalWorkspace
    ) -> Dict:
        """
        Validate a single claim against workspace.

        Args:
            claim: The claim to validate
            workspace: The global workspace

        Returns:
            Validation result dictionary
        """
        if not self.vsa_validator:
            return {
                'error': 'VSA validation is not enabled',
                'valid': None
            }

        return self.vsa_validator.validate_claim(claim, workspace)

    def batch_validate_claims(
        self,
        claims: List[str],
        workspace: GlobalWorkspace
    ) -> List[Dict]:
        """
        Validate multiple claims against workspace.

        Args:
            claims: List of claims to validate
            workspace: The global workspace

        Returns:
            List of validation results
        """
        if not self.vsa_validator:
            return [{
                'error': 'VSA validation is not enabled',
                'valid': None
            } for _ in claims]

        return [
            self.vsa_validator.validate_claim(claim, workspace)
            for claim in claims
        ]

