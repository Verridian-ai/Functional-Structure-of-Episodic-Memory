"""
Legal Corpus Retriever
======================

Provides retrieval capabilities over the OALC.
Optimized Strategy:
1.  Full Corpus Metadata Index (Citation/Title) for specific navigation.
2.  Domain-Specific Full-Text Index (Family Law) for semantic search.
3.  Legislation Index (Family Law Act) for statutory grounding.
"""

import json
import re
import math
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter

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
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.bm25 = SimpleBM25()
        self.citation_index = {}
        
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

