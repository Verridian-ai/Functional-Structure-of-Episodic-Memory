"""
Corpus Domain Extractor - Multi-Dimensional Legal Document Classifier

Streams the Australian Legal Corpus and classifies documents into 37+ legal domains
using multi-dimensional scoring across:
  1. Keyword patterns (10,500+ terms from 111 categories)
  2. Legislation references (500+ Acts mapped to domains)
  3. Landmark case citations (150+ key cases)
  4. Court hierarchy (50+ court codes with authority scores)

Usage:
    python -m src.ingestion.corpus_domain_extractor --input corpus.jsonl --output data/processed/domains

Features:
- Streaming extraction (RAM-safe for 8.8GB+)
- Multi-dimensional classification (keywords + legislation + cases + courts)
- Enhanced metadata: court level, authority score, legislation refs, case refs
- 5-factor boost scoring for domain alignment
- Specialist court domain hints (Family, Federal, AAT, etc.)
- Multi-domain tracking in metadata
- Checkpoint/resume support
- Comprehensive statistics collection (courts, legislation refs, case refs)

Classification Output per Document:
- primary_domain: Main domain classification
- primary_category: Specific subcategory
- all_matches: Top 5 matching categories with scores
- court: Extracted court code (e.g., "HCA", "NSWCA")
- court_level: apex/intermediate/trial/tribunal
- authority_score: Precedent weight (0-100)
- legislation_refs: Referenced Acts (up to 10)
- case_refs: Referenced landmark cases (up to 10)
"""

import json
import re
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional, TextIO, Any
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.classification_config import CLASSIFICATION_MAP, DOMAIN_MAPPING
from src.ingestion.legislation_patterns import (
    LEGISLATION_TO_DOMAIN, LEGISLATION_PATTERNS, LEGISLATION_TITLE_PATTERNS,
    extract_legislation_refs, get_domain_for_legislation
)
from src.ingestion.case_patterns import (
    LANDMARK_CASES, CASE_NAME_PATTERNS,
    extract_case_citations, match_landmark_case
)
from src.ingestion.court_hierarchy import (
    COURT_CODES, get_court_info, get_authority_score,
    get_domain_hint, extract_court_from_citation
)
from src.ingestion.toon_integration import batch_to_toon, convert_doc_to_row, DOC_HEADERS
from src.utils.toon import ToonEncoder
from src.ingestion.auto_gsw_trigger import GSWExtractionQueue, SmartSampler


# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = BASE_DIR / "data" / "corpus.jsonl"
DEFAULT_OUTPUT = BASE_DIR / "data" / "processed" / "domains"
STATE_FILE = BASE_DIR / "data" / "processed" / "extraction_state.json"

# All broad domains we'll create files for
ALL_DOMAINS = list(DOMAIN_MAPPING.keys()) + ["Legislation_Other", "Unclassified"]


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class DomainStats:
    """Statistics collected for a single domain during extraction."""
    document_count: int = 0
    by_type: Dict[str, int] = field(default_factory=Counter)
    by_jurisdiction: Dict[str, int] = field(default_factory=Counter)
    by_source: Dict[str, int] = field(default_factory=Counter)
    by_category: Dict[str, int] = field(default_factory=Counter)
    by_court: Dict[str, int] = field(default_factory=Counter)
    by_court_level: Dict[str, int] = field(default_factory=Counter)
    date_min: Optional[str] = None
    date_max: Optional[str] = None
    text_lengths: List[int] = field(default_factory=list)
    authority_scores: List[int] = field(default_factory=list)
    sample_citations: List[str] = field(default_factory=list)
    top_legislation_refs: Dict[str, int] = field(default_factory=Counter)
    top_case_refs: Dict[str, int] = field(default_factory=Counter)

    def update_date_range(self, date_str: Optional[str]) -> None:
        """Update min/max date range."""
        if not date_str or len(date_str) < 4:
            return
        if self.date_min is None or date_str < self.date_min:
            self.date_min = date_str
        if self.date_max is None or date_str > self.date_max:
            self.date_max = date_str

    def add_sample_citation(self, citation: str, max_samples: int = 10) -> None:
        """Add a sample citation if we don't have enough."""
        if len(self.sample_citations) < max_samples and citation:
            self.sample_citations.append(citation)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "document_count": self.document_count,
            "by_type": dict(self.by_type),
            "by_jurisdiction": dict(self.by_jurisdiction),
            "by_source": dict(self.by_source),
            "by_category": dict(self.by_category),
            "by_court": dict(self.by_court),
            "by_court_level": dict(self.by_court_level),
            "date_range": {"min": self.date_min, "max": self.date_max},
            "text_length_stats": self._calc_text_stats(),
            "authority_stats": self._calc_authority_stats(),
            "sample_citations": self.sample_citations,
            "top_legislation_refs": dict(Counter(self.top_legislation_refs).most_common(20)),
            "top_case_refs": dict(Counter(self.top_case_refs).most_common(20)),
        }

    def _calc_authority_stats(self) -> Dict[str, float]:
        """Calculate authority score statistics."""
        if not self.authority_scores:
            return {"min": 0, "max": 0, "mean": 0, "count": 0}
        scores = self.authority_scores
        return {
            "min": min(scores),
            "max": max(scores),
            "mean": sum(scores) / len(scores),
            "count": len(scores)
        }

    def _calc_text_stats(self) -> Dict[str, float]:
        """Calculate text length statistics."""
        if not self.text_lengths:
            return {"min": 0, "max": 0, "mean": 0, "count": 0}
        lengths = self.text_lengths
        return {
            "min": min(lengths),
            "max": max(lengths),
            "mean": sum(lengths) / len(lengths),
            "count": len(lengths)
        }


@dataclass
class ExtractionState:
    """Checkpoint state for resumable extraction."""
    last_line: int = 0
    total_processed: int = 0
    started_at: str = ""
    domain_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractionState":
        return cls(**data)


@dataclass
class OverlapStats:
    """Statistics about multi-domain classification."""
    single_domain_count: int = 0
    multi_domain_count: int = 0
    domain_pairs: Dict[str, int] = field(default_factory=Counter)

    def record(self, domains: List[str]) -> None:
        """Record domain matches for a document."""
        if len(domains) <= 1:
            self.single_domain_count += 1
        else:
            self.multi_domain_count += 1
            # Record all pairs
            for i, d1 in enumerate(domains):
                for d2 in domains[i+1:]:
                    pair = tuple(sorted([d1, d2]))
                    self.domain_pairs[str(pair)] += 1


# ============================================================================
# CLASSIFICATION ENGINE
# ============================================================================

class DomainClassifier:
    """Enhanced document classifier with multi-dimensional scoring."""

    def __init__(self):
        # Pre-compile regex patterns for performance
        self.patterns: Dict[str, re.Pattern] = {}
        for category, keywords in CLASSIFICATION_MAP.items():
            pattern_str = "|".join([re.escape(k) for k in keywords])
            self.patterns[category] = re.compile(pattern_str, re.IGNORECASE)

        # Build category -> domain lookup
        self.category_to_domain: Dict[str, str] = {}
        for broad, granular_list in DOMAIN_MAPPING.items():
            for granular in granular_list:
                self.category_to_domain[granular] = broad

        # Pre-lowercase legislation names for fast string matching
        self.legislation_names: Dict[str, str] = {}  # lowercase -> original
        for act_name in LEGISLATION_TO_DOMAIN.keys():
            self.legislation_names[act_name.lower()] = act_name
        # Keep for compatibility
        self.legislation_patterns = self.legislation_names

        # Pre-lowercase case names for fast string matching
        self.case_names: Dict[str, str] = {}  # lowercase -> original
        for case_name in LANDMARK_CASES.keys():
            self.case_names[case_name.lower()] = case_name
        # Keep for compatibility
        self.case_patterns = self.case_names

    def classify(self, doc: Dict[str, Any]) -> Tuple[str, str, List[Tuple[str, int]], Dict]:
        """
        Classify a document into domains with enhanced metadata.

        Returns:
            (primary_domain, primary_category, all_matches, enhanced_metadata)
            where all_matches is [(category, score), ...]
            and enhanced_metadata contains legislation_refs, case_refs, court, etc.
        """
        doc_type = doc.get('type', '')
        citation = doc.get('citation', '') or ''
        text = doc.get('text', '') or ''
        jurisdiction = (doc.get('jurisdiction', '') or '').lower()

        # Initialize enhanced metadata
        enhanced_meta = {
            'legislation_refs': [],
            'case_refs': [],
            'court': None,
            'court_level': None,
            'authority_score': 0,
        }

        # Extract court from citation
        court_code = extract_court_from_citation(citation)
        if court_code:
            enhanced_meta['court'] = court_code
            court_info = get_court_info(court_code)
            if court_info:
                enhanced_meta['court_level'] = court_info.get('level')
                enhanced_meta['authority_score'] = court_info.get('authority_score', 0)
                # Get domain hint from specialist court
                domain_hint = get_domain_hint(court_code)
                if domain_hint:
                    enhanced_meta['domain_hint'] = domain_hint

        # Different strategies for legislation vs decisions
        if doc_type in ['primary_legislation', 'secondary_legislation', 'bill']:
            primary_domain, primary_category, all_matches = self._classify_legislation(citation, jurisdiction)
        else:
            primary_domain, primary_category, all_matches = self._classify_decision(
                citation, text, jurisdiction, enhanced_meta
            )

        # Extract legislation and case references (limit text for speed)
        search_text = f"{citation} {text[:5000]}"
        search_text_lower = search_text.lower()

        leg_refs = self._extract_legislation_fast(search_text_lower)
        if leg_refs:
            enhanced_meta['legislation_refs'] = leg_refs[:10]

        case_refs = self._extract_cases_fast(search_text_lower)
        if case_refs:
            enhanced_meta['case_refs'] = case_refs[:10]

        return primary_domain, primary_category, all_matches, enhanced_meta

    def _extract_legislation_fast(self, text_lower: str) -> List[str]:
        """Extract legislation references using pre-lowercased text."""
        refs = []

        # 1. Specific Legislation
        for name_lower, name_original in self.legislation_names.items():
            if name_lower in text_lower:
                refs.append(name_original)

        # 2. Fallback Patterns (if few specific refs found)
        if len(refs) < 3:
            for domain, keywords in LEGISLATION_TITLE_PATTERNS.items():
                for keyword in keywords:
                    kw_lower = keyword.lower()
                    # Simple check: keyword followed by "act" or "regulation"
                    if f"{kw_lower} act" in text_lower or f"{kw_lower} regulation" in text_lower:
                        refs.append(f"{keyword} Legislation")
                        break # One per domain is enough to avoid noise

        return refs

    def _extract_cases_fast(self, text_lower: str) -> List[str]:
        """Extract landmark case references using pre-lowercased text."""
        refs = []
        for name_lower, name_original in self.case_names.items():
            if name_lower in text_lower:
                refs.append(name_original)
        return refs

    def _classify_legislation(
        self,
        citation: str,
        jurisdiction: str
    ) -> Tuple[str, str, List[Tuple[str, int]]]:
        """Classify legislation using citation/title only."""
        scores = Counter()
        citation_lower = citation.lower()

        # 1. Title Pattern Matching (Broad Domains) - HIGHEST PRIORITY for Legislation
        # This is curated specifically for Act titles (e.g. "Local Government", "Public Health")
        for domain, keywords in LEGISLATION_TITLE_PATTERNS.items():
            for keyword in keywords:
                if keyword.lower() in citation_lower:
                    # Found a broad domain match
                    return domain, f"{domain}_Legislation", [(f"{domain}_Legislation", 10)]

        # 2. Exact Match (Category Keywords) - Fallback
        # This uses the massive keyword list designed for full text, which can be noisy for titles
        for category, pattern in self.patterns.items():
            if pattern.search(citation_lower):
                scores[category] = 5  # Lower weight than title patterns

        if scores:
            all_matches = scores.most_common()
            best_category = all_matches[0][0]
            best_domain = self.category_to_domain.get(best_category, "Legislation_Other")
            return best_domain, best_category, all_matches

        return "Legislation_Other", "Legislation_Other", []

    def _classify_decision(
        self,
        citation: str,
        text: str,
        jurisdiction: str,
        enhanced_meta: Dict = None
    ) -> Tuple[str, str, List[Tuple[str, int]]]:
        """Classify court decisions with enhanced multi-dimensional scoring."""
        scores = Counter()

        # Build searchable text (citation + first 15000 chars)
        search_text = f"{citation} {text[:15000]}".lower()
        citation_lower = citation.lower()

        for category, pattern in self.patterns.items():
            matches = pattern.findall(search_text)
            if not matches:
                continue

            base_score = len(matches)

            # BOOST 1: Citation match (strong indicator)
            if pattern.search(citation_lower):
                base_score += 10

            # BOOST 2: Jurisdiction alignment
            if "Family" in category:
                if "family" in jurisdiction or "family court" in search_text[:1000]:
                    base_score += 20

            if "Migration" in category or "Admin_Migration" in category:
                if "refugee" in search_text or "visa" in search_text or "migration" in jurisdiction:
                    base_score += 15

            if "Criminal" in category:
                if "criminal" in jurisdiction or "crime" in jurisdiction:
                    base_score += 15

            # BOOST 3: Court domain hint alignment
            if enhanced_meta and enhanced_meta.get('domain_hint'):
                domain_hint = enhanced_meta['domain_hint']
                category_domain = self.category_to_domain.get(category, '')
                if domain_hint == category_domain:
                    base_score += 25  # Strong boost for specialist court match

            scores[category] = base_score

        # BOOST 4: Legislation-based domain boost
        if enhanced_meta:
            for leg_ref in enhanced_meta.get('legislation_refs', []):
                if leg_ref in LEGISLATION_TO_DOMAIN:
                    leg_info = LEGISLATION_TO_DOMAIN[leg_ref]
                    for subcat in leg_info.get('subcategories', []):
                        if subcat in scores:
                            scores[subcat] += 15
                        else:
                            scores[subcat] = 15

        # BOOST 5: Case law-based domain boost
        if enhanced_meta:
            for case_ref in enhanced_meta.get('case_refs', []):
                if case_ref in LANDMARK_CASES:
                    case_info = LANDMARK_CASES[case_ref]
                    for subcat in case_info.get('subcategories', []):
                        if subcat in scores:
                            scores[subcat] += 10
                        else:
                            scores[subcat] = 10

        # BOOST 6: Case Title Patterns (Party Names)
        # Strong indicators of domain based on parties (e.g. Crown, Regulators)
        if "r v " in citation_lower or "regina v " in citation_lower or "dpp v " in citation_lower or "police v " in citation_lower:
            scores["Criminal_General"] += 20

        if "minister " in citation_lower:
            scores["Admin_Review"] += 15
            if "immigration" in citation_lower:
                scores["Admin_Migration"] += 20

        if "accc " in citation_lower:
            scores["Competition_Cartels"] += 15
            scores["Comm_Consumer"] += 15

        if "asic " in citation_lower:
            scores["Corp_Governance"] += 15
            scores["Securities_Licensing"] += 15

        if "commissioner of taxation" in citation_lower or "fct v" in citation_lower:
            scores["Tax_Federal"] += 20

        if not scores:
            return "Unclassified", "Unclassified", []

        all_matches = scores.most_common()
        best_category = all_matches[0][0]
        best_domain = self.category_to_domain.get(best_category, "Unclassified")

        return best_domain, best_category, all_matches


# ============================================================================
# FILE MANAGER
# ============================================================================

# ============================================================================
# FILE MANAGER
# ============================================================================

class ToonFileManager:
    """Manages output file handles for TOON domain files."""

    def __init__(self, output_dir: Path, append: bool = False):
        self.output_dir = output_dir
        self.handles: Dict[str, TextIO] = {}
        self.append = append
        self.legislation_path = output_dir / "legislation" / "acts.toon"

    def __enter__(self) -> "ToonFileManager":
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "cases").mkdir(exist_ok=True)
        (self.output_dir / "legislation").mkdir(exist_ok=True)

        # We don't pre-open all files for TOON to allow for lazy creation/headers
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handle in self.handles.values():
            handle.close()

    def write(self, domain: str, doc: Dict[str, Any]) -> None:
        """Write document to appropriate TOON file."""
        doc_type = doc.get("type", "")

        # Determine target file and table name
        if doc_type in ['primary_legislation', 'secondary_legislation', 'bill']:
            target_path = self.legislation_path
            table_name = "Legislation"
            key = "legislation"
        else:
            # Case Law -> Organized by Domain
            domain_dir = self.output_dir / "cases" / domain
            domain_dir.mkdir(exist_ok=True)
            target_path = domain_dir / f"{domain}.toon"
            table_name = f"Cases_{domain}"
            key = domain

        # Get or create handle
        if key not in self.handles:
            mode = 'a' if self.append and target_path.exists() else 'w'
            f = open(target_path, mode, encoding='utf-8')
            self.handles[key] = f

            # Write header if new file or overwriting
            if mode == 'w':
                # We can't write the full TOON header "Name[Count]{cols}" yet because we stream.
                # Standard TOON expects a count.
                # For streaming, we might need a variant or just buffer.
                # However, for "perfect accuracy" and standard TOON, we usually batch.
                # Given strict streaming requirement, we will append rows and
                # relied on a post-processing step OR use a "Streaming TOON" concept (not standard).
                #
                # ALTERNATIVE: Write as separate TOON blocks per batch?
                # Or just write CSV-like lines but that violates "Name[Count]".
                #
                # Let's check `src/utils/toon.py`. It writes a block.
                # To support streaming to one file, we should probably write one block per document
                # OR (better) write a header with specific count if we knew it found
                # OR just write blocks of N documents.
                #
                # DECISION: We will buffer in memory until X docs for that domain, then flushing a block.
                pass

        # We actually need to Buffer per domain to write valid TOON blocks
        # So we won't write immediately to file handle in this method if we strictly follow TOON.
        # But `ToonFileManager` interface assumes `write` writes.
        # Let's change this class to buffer.
        pass # Replaced by buffered implementation below

class BufferedToonFileManager:
    """Manages output file handles and buffers for TOON domain files."""

    def __init__(self, output_dir: Path, batch_size: int = 100, append: bool = False):
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.append = append
        self.legislation_path = output_dir / "legislation" / "acts.toon"
        self.buffers: Dict[str, List[Dict]] = defaultdict(list)

    def __enter__(self) -> "BufferedToonFileManager":
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "cases").mkdir(exist_ok=True)
        (self.output_dir / "legislation").mkdir(exist_ok=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Flush all remaining buffers
        for key in list(self.buffers.keys()):
            self._flush(key)

    def write(self, domain: str, doc: Dict[str, Any]) -> None:
        """Buffer document and flush if full."""
        doc_type = doc.get("type", "")

        if doc_type in ['primary_legislation', 'secondary_legislation', 'bill']:
            key = "legislation"
        else:
            key = domain

        self.buffers[key].append(doc)

        if len(self.buffers[key]) >= self.batch_size:
            self._flush(key)

    def _flush(self, key: str):
        docs = self.buffers[key]
        if not docs:
            return

        if key == "legislation":
            target_path = self.legislation_path
            table_name = "Legislation"
        else:
            domain = key
            domain_dir = self.output_dir / "cases" / domain
            domain_dir.mkdir(exist_ok=True)
            target_path = domain_dir / f"{domain}.toon"
            table_name = f"Cases_{domain}"

        # Generate TOON block
        toon_block = batch_to_toon(docs, table_name)

        # Write to file
        mode = 'a' if target_path.exists() else 'w'
        with open(target_path, mode, encoding='utf-8') as f:
            f.write(toon_block + "\n")

        # Clear buffer
        self.buffers[key] = []


# ============================================================================
# MAIN EXTRACTOR
# ============================================================================

class CorpusDomainExtractor:
    """
    Main extraction class for domain classification.

    Streams the corpus.jsonl file, classifies each document,
    and writes to domain-specific output files.
    """

    def __init__(
        self,
        input_path: Path,
        output_dir: Path,
        state_path: Optional[Path] = None,
        enable_auto_gsw: bool = False,
        gsw_queue: Optional[GSWExtractionQueue] = None,
        gsw_min_authority: int = 60
    ):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.state_path = Path(state_path) if state_path else STATE_FILE

        self.classifier = DomainClassifier()
        self.stats: Dict[str, DomainStats] = defaultdict(DomainStats)
        self.overlap_stats = OverlapStats()

        # Auto-GSW extraction
        self.enable_auto_gsw = enable_auto_gsw
        self.gsw_queue = gsw_queue or (GSWExtractionQueue(min_authority=gsw_min_authority) if enable_auto_gsw else None)
        self.sampler = SmartSampler() if enable_auto_gsw else None

    def extract_all(
        self,
        progress_interval: int = 5000,
        resume: bool = False,
        limit: Optional[int] = None
    ) -> Dict[str, DomainStats]:
        """
        Process entire corpus with streaming.

        Args:
            progress_interval: Print progress every N documents
            resume: Whether to resume from checkpoint
            limit: Maximum number of documents to process (for testing)

        Returns:
            Dictionary of domain -> DomainStats
        """
        start_line = 0
        if resume:
            state = self._load_checkpoint()
            if state:
                start_line = state.last_line
                print(f"[Resume] Starting from line {start_line}")

        print(f"[Extractor] Input: {self.input_path}")
        print(f"[Extractor] Output: {self.output_dir}")
        print(f"[Extractor] Domains: {len(ALL_DOMAINS)}")
        print("-" * 60)

        start_time = datetime.now()

        with BufferedToonFileManager(self.output_dir, append=resume) as file_manager:
            with open(self.input_path, 'r', encoding='utf-8') as infile:
                for line_num, line in enumerate(infile):
                    # Skip lines if resuming
                    if line_num < start_line:
                        continue

                    # Stop if limit reached
                    if limit and line_num >= start_line + limit:
                        print(f"\n[Limit] Reached limit of {limit} documents")
                        break

                    try:
                        doc = json.loads(line)
                        self._process_document(doc, file_manager, line_num)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"\n[Error] Line {line_num}: {e}")
                        continue

                    # Progress reporting
                    if line_num % progress_interval == 0 and line_num > 0:
                        self._print_progress(line_num, start_time)
                        # Save checkpoint
                        self._save_checkpoint(line_num)

        elapsed = datetime.now() - start_time
        print(f"\n[Complete] Processed {sum(s.document_count for s in self.stats.values())} documents in {elapsed}")

        # Save final statistics
        self._save_statistics()

        return dict(self.stats)

    def _process_document(
        self,
        doc: Dict[str, Any],
        file_manager: BufferedToonFileManager,
        line_num: int
    ) -> None:
        """Process a single document with enhanced multi-dimensional classification."""
        # Classify with enhanced metadata
        primary_domain, primary_category, all_matches, enhanced_meta = self.classifier.classify(doc)

        # Track overlap statistics
        all_domains = list(set([
            self.classifier.category_to_domain.get(cat, "Unclassified")
            for cat, _ in all_matches
        ]))
        self.overlap_stats.record(all_domains)

        # Inject classification metadata with enhanced fields
        doc['_classification'] = {
            'primary_domain': primary_domain,
            'primary_category': primary_category,
            'all_matches': [(cat, score) for cat, score in all_matches[:5]],  # Top 5
            'match_count': len(all_matches),
            'line_number': line_num,
            # Enhanced multi-dimensional metadata
            'court': enhanced_meta.get('court'),
            'court_level': enhanced_meta.get('court_level'),
            'authority_score': enhanced_meta.get('authority_score', 0),
            'legislation_refs': enhanced_meta.get('legislation_refs', []),
            'case_refs': enhanced_meta.get('case_refs', []),
        }

        # Add domain hint if specialist court detected
        if enhanced_meta.get('domain_hint'):
            doc['_classification']['domain_hint'] = enhanced_meta['domain_hint']

        # Write to primary domain file
        file_manager.write(primary_domain, doc)

        # Collect statistics
        stats = self.stats[primary_domain]
        stats.document_count += 1
        stats.by_type[doc.get('type', 'unknown')] += 1
        stats.by_jurisdiction[doc.get('jurisdiction', 'unknown')] += 1
        stats.by_source[doc.get('source', 'unknown')] += 1
        stats.by_category[primary_category] += 1
        stats.update_date_range(doc.get('date'))

        # Track court and authority statistics
        court = enhanced_meta.get('court')
        if court:
            stats.by_court[court] += 1
        court_level = enhanced_meta.get('court_level')
        if court_level:
            stats.by_court_level[court_level] += 1

        # Track legislation and case references (top occurrences)
        for leg_ref in enhanced_meta.get('legislation_refs', []):
            stats.top_legislation_refs[leg_ref] += 1
        for case_ref in enhanced_meta.get('case_refs', []):
            stats.top_case_refs[case_ref] += 1

        # Sample text lengths and authority scores (every 100th doc to save memory)
        if stats.document_count % 100 == 0:
            text = doc.get('text', '')
            stats.text_lengths.append(len(text) if text else 0)
            authority_score = enhanced_meta.get('authority_score', 0)
            if authority_score > 0:
                stats.authority_scores.append(authority_score)

        # Sample citations
        stats.add_sample_citation(doc.get('citation', ''))

        # Auto-trigger GSW extraction if enabled
        if self.enable_auto_gsw and self.gsw_queue:
            # Use smart sampler to determine priority
            priority = self.sampler.get_sampling_priority(doc)
            if priority >= self.gsw_queue.min_authority:
                self.gsw_queue.add(doc, priority=priority)

    def _print_progress(self, line_num: int, start_time: datetime) -> None:
        """Print progress update."""
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = line_num / elapsed if elapsed > 0 else 0

        # Top domains by count
        top_domains = sorted(
            [(d, s.document_count) for d, s in self.stats.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_str = " | ".join([f"{d}:{c}" for d, c in top_domains])
        print(f"\r[Progress] {line_num:,} docs | {rate:.0f}/sec | {top_str}", end="", flush=True)

    def _save_checkpoint(self, line_num: int) -> None:
        """Save extraction state for resume."""
        state = ExtractionState(
            last_line=line_num,
            total_processed=sum(s.document_count for s in self.stats.values()),
            started_at=datetime.now().isoformat(),
            domain_counts={d: s.document_count for d, s in self.stats.items()}
        )

        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state.to_dict(), f, indent=2)

    def _load_checkpoint(self) -> Optional[ExtractionState]:
        """Load previous extraction state."""
        if not self.state_path.exists():
            return None

        try:
            with open(self.state_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ExtractionState.from_dict(data)
        except Exception as e:
            print(f"[Warning] Could not load checkpoint: {e}")
            return None

    def _save_statistics(self) -> None:
        """Save extraction statistics to JSON."""
        stats_path = self.output_dir / "extraction_statistics.json"

        output = {
            "extraction_completed": datetime.now().isoformat(),
            "total_documents": sum(s.document_count for s in self.stats.values()),
            "domain_stats": {d: s.to_dict() for d, s in self.stats.items()},
            "overlap_stats": {
                "single_domain": self.overlap_stats.single_domain_count,
                "multi_domain": self.overlap_stats.multi_domain_count,
                "top_pairs": dict(Counter(self.overlap_stats.domain_pairs).most_common(20))
            }
        }

        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        print(f"[Stats] Saved to {stats_path}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract and classify Australian Legal Corpus into domains"
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to corpus.jsonl"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory for domain files"
    )
    parser.add_argument(
        "--progress", "-p",
        type=int,
        default=5000,
        help="Progress reporting interval"
    )
    parser.add_argument(
        "--resume", "-r",
        action="store_true",
        help="Resume from checkpoint"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Limit number of documents to process"
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"[Error] Input file not found: {args.input}")
        sys.exit(1)

    extractor = CorpusDomainExtractor(
        input_path=args.input,
        output_dir=args.output
    )

    extractor.extract_all(
        progress_interval=args.progress,
        resume=args.resume,
        limit=args.limit
    )


if __name__ == "__main__":
    main()
