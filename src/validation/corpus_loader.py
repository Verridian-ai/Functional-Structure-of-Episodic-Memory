"""
Statutory Corpus Loader
========================

Loads and manages statutory corpus from JSON files.
Provides search and retrieval capabilities for statutory provisions.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


class CorpusLoader:
    """
    Loads and manages statutory corpus from JSON files.

    The corpus loader handles loading JSON files from the statutory corpus directory,
    indexing sections for efficient retrieval, and providing search capabilities.
    """

    def __init__(self, corpus_dir: str = "data/statutory_corpus"):
        """
        Initialize the corpus loader.

        Args:
            corpus_dir: Directory containing statutory JSON files
        """
        self.corpus_dir = Path(corpus_dir)
        self.acts: Dict[str, Dict] = {}
        self.section_index: Dict[str, List[Dict]] = {}  # section_number -> [provisions]
        self.keyword_index: Dict[str, List[Dict]] = {}  # keyword -> [provisions]

        if not self.corpus_dir.exists():
            print(f"[CorpusLoader] Warning: Corpus directory {corpus_dir} does not exist")
            return

        self._load_corpus()
        self._build_indices()

    def _load_corpus(self) -> None:
        """
        Load all JSON files from the corpus directory.
        """
        print(f"[CorpusLoader] Loading corpus from {self.corpus_dir}")

        json_files = list(self.corpus_dir.glob("*.json"))

        if not json_files:
            print(f"[CorpusLoader] No JSON files found in {self.corpus_dir}")
            return

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Extract act information
                    if 'act' in data:
                        act_name = data['act'].get('name', json_file.stem)
                        self.acts[act_name] = data
                        print(f"[CorpusLoader] Loaded {act_name}")
                    else:
                        print(f"[CorpusLoader] Warning: No 'act' key in {json_file}")

            except Exception as e:
                print(f"[CorpusLoader] Error loading {json_file}: {e}")

        print(f"[CorpusLoader] Loaded {len(self.acts)} acts")

    def _build_indices(self) -> None:
        """
        Build search indices for efficient retrieval.
        """
        print("[CorpusLoader] Building indices...")

        for act_name, act_data in self.acts.items():
            sections = act_data.get('sections', [])

            for section in sections:
                # Index by section number
                section_num = section.get('section', '')
                if section_num:
                    if section_num not in self.section_index:
                        self.section_index[section_num] = []

                    # Add act metadata to section
                    section_with_act = section.copy()
                    section_with_act['act_name'] = act_name
                    section_with_act['act_citation'] = act_data['act'].get('citation', '')
                    section_with_act['act_url'] = act_data['act'].get('url', '')

                    self.section_index[section_num].append(section_with_act)

                # Index by keywords
                keywords = section.get('keywords', [])
                for keyword in keywords:
                    keyword_lower = keyword.lower()
                    if keyword_lower not in self.keyword_index:
                        self.keyword_index[keyword_lower] = []

                    if section_with_act not in self.keyword_index[keyword_lower]:
                        self.keyword_index[keyword_lower].append(section_with_act)

        print(f"[CorpusLoader] Indexed {len(self.section_index)} sections, {len(self.keyword_index)} keywords")

    def get_section(self, section_number: str, act_name: Optional[str] = None) -> Optional[Dict]:
        """
        Retrieve a specific section by number.

        Args:
            section_number: The section number to retrieve
            act_name: Optional act name to filter by

        Returns:
            Section data if found, None otherwise
        """
        sections = self.section_index.get(section_number, [])

        if not sections:
            return None

        if act_name:
            for section in sections:
                if section.get('act_name') == act_name:
                    return section
            return None

        # Return first match if no act specified
        return sections[0]

    def search_by_keyword(self, keyword: str, top_k: int = 5) -> List[Dict]:
        """
        Search for sections by keyword.

        Args:
            keyword: Keyword to search for
            top_k: Maximum number of results to return

        Returns:
            List of matching sections
        """
        keyword_lower = keyword.lower()
        results = []

        # Exact match
        if keyword_lower in self.keyword_index:
            results.extend(self.keyword_index[keyword_lower])

        # Partial match
        for indexed_keyword, sections in self.keyword_index.items():
            if keyword_lower in indexed_keyword or indexed_keyword in keyword_lower:
                for section in sections:
                    if section not in results:
                        results.append(section)

        return results[:top_k]

    def search_by_text(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for sections by text content.

        Args:
            query: Text query to search for
            top_k: Maximum number of results to return

        Returns:
            List of matching sections with relevance scores
        """
        query_lower = query.lower()
        query_terms = set(re.findall(r'\w+', query_lower))

        results = []

        for act_name, act_data in self.acts.items():
            sections = act_data.get('sections', [])

            for section in sections:
                # Score based on term overlap
                section_text = ' '.join([
                    section.get('title', ''),
                    section.get('summary', ''),
                    section.get('legal_test', ''),
                    ' '.join(section.get('keywords', []))
                ]).lower()

                section_terms = set(re.findall(r'\w+', section_text))
                overlap = len(query_terms.intersection(section_terms))

                if overlap > 0:
                    section_with_act = section.copy()
                    section_with_act['act_name'] = act_name
                    section_with_act['act_citation'] = act_data['act'].get('citation', '')
                    section_with_act['act_url'] = act_data['act'].get('url', '')
                    section_with_act['relevance_score'] = overlap / len(query_terms)

                    results.append(section_with_act)

        # Sort by relevance score
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)

        return results[:top_k]

    def get_related_provisions(self, section_number: str, act_name: Optional[str] = None) -> List[Dict]:
        """
        Get provisions related to a given section.

        Related provisions are determined by shared keywords and similar legal tests.

        Args:
            section_number: The section number
            act_name: Optional act name to filter by

        Returns:
            List of related sections
        """
        base_section = self.get_section(section_number, act_name)

        if not base_section:
            return []

        # Get keywords from base section
        base_keywords = set(kw.lower() for kw in base_section.get('keywords', []))

        if not base_keywords:
            return []

        related = []

        for act_name, act_data in self.acts.items():
            sections = act_data.get('sections', [])

            for section in sections:
                # Skip the same section
                if section.get('section') == section_number:
                    continue

                # Calculate keyword overlap
                section_keywords = set(kw.lower() for kw in section.get('keywords', []))
                overlap = len(base_keywords.intersection(section_keywords))

                if overlap > 0:
                    section_with_act = section.copy()
                    section_with_act['act_name'] = act_name
                    section_with_act['act_citation'] = act_data['act'].get('citation', '')
                    section_with_act['act_url'] = act_data['act'].get('url', '')
                    section_with_act['keyword_overlap'] = overlap

                    related.append(section_with_act)

        # Sort by keyword overlap
        related.sort(key=lambda x: x.get('keyword_overlap', 0), reverse=True)

        return related[:10]

    def get_all_acts(self) -> List[Dict]:
        """
        Get metadata for all loaded acts.

        Returns:
            List of act metadata dictionaries
        """
        return [act_data['act'] for act_data in self.acts.values() if 'act' in act_data]

    def get_sections_by_legal_test(self, legal_test: str) -> List[Dict]:
        """
        Get sections by legal test name.

        Args:
            legal_test: Legal test to search for

        Returns:
            List of matching sections
        """
        legal_test_lower = legal_test.lower()
        results = []

        for act_name, act_data in self.acts.items():
            sections = act_data.get('sections', [])

            for section in sections:
                section_legal_test = section.get('legal_test', '').lower()

                if legal_test_lower in section_legal_test or section_legal_test in legal_test_lower:
                    section_with_act = section.copy()
                    section_with_act['act_name'] = act_name
                    section_with_act['act_citation'] = act_data['act'].get('citation', '')
                    section_with_act['act_url'] = act_data['act'].get('url', '')

                    results.append(section_with_act)

        return results
