"""
Acts Interpretation Framework

Provides programmatic access to default statutory definitions from
Acts Interpretation Acts across all Australian jurisdictions.

These are the DEFAULT definitions that apply when an Act doesn't define
a term itself - critical for legal NLP and automated reasoning.

Usage:
    from src.logic.interpretation_acts import InterpretationActsDB

    db = InterpretationActsDB()

    # Get definition of 'person' in Commonwealth legislation
    definition = db.get_definition('person', jurisdiction='Commonwealth')

    # Check if 'may' is mandatory or permissive
    modal_type = db.classify_modal('may', jurisdiction='NSW')

    # Calculate 1 month from a date
    end_date = db.calculate_month('2024-01-31', jurisdiction='Vic')

Key Features:
- Definition lookup with jurisdiction-specific defaults
- Modal verb classification (may/must/shall)
- Temporal calculations (month, year, business day)
- Gender-neutral interpretation
- Corporate personality rules
- Commencement date calculation
"""

from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import re


# ============================================================================
# CONSTANTS
# ============================================================================

JURISDICTIONS = [
    "Commonwealth",
    "New South Wales",
    "Victoria",
    "Queensland",
    "Western Australia",
    "South Australia",
    "Tasmania",
    "Australian Capital Territory",
    "Northern Territory"
]

JURISDICTION_ABBREV = {
    "Commonwealth": "Cth",
    "New South Wales": "NSW",
    "Victoria": "Vic",
    "Queensland": "Qld",
    "Western Australia": "WA",
    "South Australia": "SA",
    "Tasmania": "Tas",
    "Australian Capital Territory": "ACT",
    "Northern Territory": "NT"
}

MODAL_VERBS = {
    "MANDATORY": ["must", "shall", "is required to", "is to", "required to"],
    "PERMISSIVE": ["may", "is empowered to", "has power to", "is permitted to", "can"],
    "PROHIBITED": ["must not", "shall not", "is prohibited from", "prohibited from"]
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Definition:
    """Represents a statutory definition from an Interpretation Act."""
    term: str
    jurisdiction: str
    section: str
    definition: str
    legal_significance: str
    examples: Optional[List[str]] = None
    modern_application: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term": self.term,
            "jurisdiction": self.jurisdiction,
            "section": self.section,
            "definition": self.definition,
            "legal_significance": self.legal_significance,
            "examples": self.examples,
            "modern_application": self.modern_application
        }


@dataclass
class ModalClassification:
    """Classification of a modal verb in statutory context."""
    modal: str
    modal_type: str  # MANDATORY, PERMISSIVE, PROHIBITED
    creates: str  # duty, power, prohibition
    jurisdiction: str
    section: str
    contextual_note: Optional[str] = None


@dataclass
class InterpretationAct:
    """Metadata about a jurisdiction's Interpretation Act."""
    jurisdiction: str
    act_name: str
    citation: str
    url: str
    definitions_section: str
    key_provisions: Dict[str, Any]


# ============================================================================
# MAIN DATABASE CLASS
# ============================================================================

class InterpretationActsDB:
    """
    Database of Interpretation Acts definitions and rules.

    Provides lookup, classification, and calculation methods based on
    Australian Acts Interpretation Acts.
    """

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the Interpretation Acts database.

        Args:
            data_path: Path to acts_interpretation_acts_research.json
                      If None, uses default path in data/legislation/
        """
        if data_path is None:
            base_dir = Path(__file__).resolve().parents[2]
            data_path = base_dir / "data" / "legislation" / "acts_interpretation_acts_research.json"

        self.data_path = Path(data_path)
        self.data = self._load_data()
        self._build_indexes()

    def _load_data(self) -> Dict[str, Any]:
        """Load the research JSON data."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Interpretation Acts data not found: {self.data_path}")

        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _build_indexes(self) -> None:
        """Build lookup indexes for fast access."""
        # Build definition index: (term, jurisdiction) -> Definition
        self.definitions: Dict[Tuple[str, str], Definition] = {}

        for act_data in self.data['interpretation_acts']:
            jurisdiction = act_data['jurisdiction']

            # Extract definitions
            if 'critical_definitions' in act_data.get('key_provisions', {}):
                for term, def_data in act_data['key_provisions']['critical_definitions'].items():
                    definition = Definition(
                        term=term,
                        jurisdiction=jurisdiction,
                        section=def_data.get('section', ''),
                        definition=def_data.get('definition', ''),
                        legal_significance=def_data.get('legal_significance', ''),
                        examples=def_data.get('examples'),
                        modern_application=def_data.get('modern_application')
                    )
                    self.definitions[(term.lower(), jurisdiction)] = definition

        # Build acts index: jurisdiction -> InterpretationAct
        self.acts: Dict[str, InterpretationAct] = {}
        for act_data in self.data['interpretation_acts']:
            jurisdiction = act_data['jurisdiction']
            self.acts[jurisdiction] = InterpretationAct(
                jurisdiction=jurisdiction,
                act_name=act_data['act_name'],
                citation=act_data['citation'],
                url=act_data['url'],
                definitions_section=act_data['key_provisions'].get('definitions_section', ''),
                key_provisions=act_data['key_provisions']
            )

    # ========================================================================
    # DEFINITION LOOKUP
    # ========================================================================

    def get_definition(
        self,
        term: str,
        jurisdiction: str = "Commonwealth",
        fallback: bool = True
    ) -> Optional[Definition]:
        """
        Get the default definition of a term from an Interpretation Act.

        Args:
            term: The term to look up (e.g., 'person', 'month', 'may')
            jurisdiction: Jurisdiction (default: Commonwealth)
            fallback: If True and term not found, try Commonwealth as fallback

        Returns:
            Definition object or None if not found

        Example:
            >>> db = InterpretationActsDB()
            >>> person_def = db.get_definition('person', 'NSW')
            >>> print(person_def.definition)
            "Includes an individual, a corporation and a body corporate or politic"
        """
        term_lower = term.lower()

        # Try requested jurisdiction
        key = (term_lower, jurisdiction)
        if key in self.definitions:
            return self.definitions[key]

        # Fallback to Commonwealth if requested
        if fallback and jurisdiction != "Commonwealth":
            key = (term_lower, "Commonwealth")
            if key in self.definitions:
                return self.definitions[key]

        return None

    def get_all_definitions_for_term(self, term: str) -> List[Definition]:
        """
        Get all jurisdictional definitions for a term.

        Args:
            term: The term to look up

        Returns:
            List of Definition objects across all jurisdictions
        """
        term_lower = term.lower()
        results = []

        for jurisdiction in JURISDICTIONS:
            definition = self.get_definition(term, jurisdiction, fallback=False)
            if definition:
                results.append(definition)

        return results

    def search_definitions(self, search_term: str) -> List[Definition]:
        """
        Search for definitions containing the search term.

        Args:
            search_term: Text to search for in definitions

        Returns:
            List of matching Definition objects
        """
        search_lower = search_term.lower()
        results = []

        for (term, jurisdiction), definition in self.definitions.items():
            if (search_lower in term.lower() or
                search_lower in definition.definition.lower() or
                search_lower in definition.legal_significance.lower()):
                results.append(definition)

        return results

    # ========================================================================
    # MODAL VERB CLASSIFICATION
    # ========================================================================

    def classify_modal(
        self,
        modal: str,
        jurisdiction: str = "Commonwealth",
        context: Optional[str] = None
    ) -> ModalClassification:
        """
        Classify a modal verb as mandatory, permissive, or prohibited.

        Args:
            modal: Modal verb (e.g., 'may', 'must', 'shall')
            jurisdiction: Jurisdiction for specific rules
            context: Optional context for contextual analysis

        Returns:
            ModalClassification object

        Example:
            >>> db = InterpretationActsDB()
            >>> classification = db.classify_modal('may', 'Commonwealth')
            >>> print(classification.modal_type)
            "PERMISSIVE"
        """
        modal_lower = modal.lower().strip()

        # Determine base classification
        modal_type = None
        creates = None

        if modal_lower in [m.lower() for m in MODAL_VERBS["MANDATORY"]]:
            modal_type = "MANDATORY"
            creates = "duty"
        elif modal_lower in [m.lower() for m in MODAL_VERBS["PERMISSIVE"]]:
            modal_type = "PERMISSIVE"
            creates = "power"
        elif modal_lower in [m.lower() for m in MODAL_VERBS["PROHIBITED"]]:
            modal_type = "PROHIBITED"
            creates = "prohibition"
        else:
            modal_type = "UNKNOWN"
            creates = "unknown"

        # Get section reference
        definition = self.get_definition(modal_lower, jurisdiction)
        section = definition.section if definition else "unknown"

        # Contextual analysis
        contextual_note = None
        if context and modal_type == "PERMISSIVE":
            # Check for "may only" construction
            if re.search(r'\bmay\s+only\b', context.lower()):
                contextual_note = "'may only' construction indicates prohibition of other actions"

        return ModalClassification(
            modal=modal,
            modal_type=modal_type,
            creates=creates,
            jurisdiction=jurisdiction,
            section=section,
            contextual_note=contextual_note
        )

    def extract_obligations(self, text: str, jurisdiction: str = "Commonwealth") -> Dict[str, List[str]]:
        """
        Extract obligations, powers, and prohibitions from statutory text.

        Args:
            text: Statutory text to analyze
            jurisdiction: Jurisdiction for modal classification

        Returns:
            Dictionary with 'duties', 'powers', 'prohibitions' keys

        Example:
            >>> db = InterpretationActsDB()
            >>> text = "The Minister must approve applications. The Minister may delegate this power."
            >>> obligations = db.extract_obligations(text)
            >>> print(obligations['duties'])
            ["The Minister must approve applications."]
        """
        results = {
            "duties": [],
            "powers": [],
            "prohibitions": []
        }

        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check for mandatory modals
            if re.search(r'\b(must|shall|is required to|is to)\b', sentence, re.IGNORECASE):
                results['duties'].append(sentence)

            # Check for permissive modals
            elif re.search(r'\b(may|is empowered to|has power to)\b', sentence, re.IGNORECASE):
                results['powers'].append(sentence)

            # Check for prohibitions
            elif re.search(r'\b(must not|shall not|is prohibited from)\b', sentence, re.IGNORECASE):
                results['prohibitions'].append(sentence)

        return results

    # ========================================================================
    # TEMPORAL CALCULATIONS
    # ========================================================================

    def calculate_month(
        self,
        start_date: str,
        jurisdiction: str = "Commonwealth",
        months: int = 1
    ) -> str:
        """
        Calculate date that is N months from start date using calendar month rule.

        All jurisdictions use calendar month definition:
        - Go to same day next month
        - If no corresponding day, use last day of that month

        Args:
            start_date: Start date in YYYY-MM-DD format
            jurisdiction: Jurisdiction (for completeness, all use same rule)
            months: Number of months to add (default: 1)

        Returns:
            End date in YYYY-MM-DD format

        Example:
            >>> db = InterpretationActsDB()
            >>> db.calculate_month('2024-01-31')  # 1 month from Jan 31
            "2024-02-29"  # Feb 29 in leap year (or Feb 28 in non-leap)
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")

        # Calculate target month/year
        target_month = start.month + months
        target_year = start.year

        # Handle month overflow
        while target_month > 12:
            target_month -= 12
            target_year += 1

        while target_month < 1:
            target_month += 12
            target_year -= 1

        # Try to use same day
        try:
            end = datetime(target_year, target_month, start.day)
        except ValueError:
            # No corresponding day - use last day of month
            if target_month == 12:
                next_month = datetime(target_year + 1, 1, 1)
            else:
                next_month = datetime(target_year, target_month + 1, 1)

            end = next_month - timedelta(days=1)

        return end.strftime("%Y-%m-%d")

    def calculate_commencement(
        self,
        assent_date: str,
        jurisdiction: str = "Commonwealth"
    ) -> str:
        """
        Calculate default commencement date for an Act with no commencement clause.

        Rules vary by jurisdiction:
        - Commonwealth: 28 days after assent
        - Most states: Day of assent
        - WA: Publication in Gazette (cannot calculate without Gazette date)
        - ACT: Notification on register (cannot calculate without notification date)

        Args:
            assent_date: Date of assent in YYYY-MM-DD format
            jurisdiction: Jurisdiction

        Returns:
            Commencement date in YYYY-MM-DD format

        Raises:
            ValueError: For WA and ACT where additional information needed
        """
        assent = datetime.strptime(assent_date, "%Y-%m-%d")

        # Commencement rules by jurisdiction
        if jurisdiction == "Commonwealth":
            # 28 days after assent
            commencement = assent + timedelta(days=28)

        elif jurisdiction in ["New South Wales", "Victoria", "Queensland",
                              "South Australia", "Tasmania", "Northern Territory"]:
            # Immediate on assent
            commencement = assent

        elif jurisdiction == "Western Australia":
            raise ValueError(
                "WA Acts commence on publication in Gazette. "
                "Gazette date required - cannot calculate from assent date alone."
            )

        elif jurisdiction == "Australian Capital Territory":
            raise ValueError(
                "ACT Acts commence on notification on legislation register. "
                "Notification date required - cannot calculate from assent date alone."
            )

        else:
            raise ValueError(f"Unknown jurisdiction: {jurisdiction}")

        return commencement.strftime("%Y-%m-%d")

    def is_business_day(self, date: str, jurisdiction: str = "Commonwealth") -> bool:
        """
        Check if a date is a business day (not weekend or public holiday).

        Note: This basic implementation only checks weekends.
        Full implementation requires jurisdiction-specific public holiday calendars.

        Args:
            date: Date in YYYY-MM-DD format
            jurisdiction: Jurisdiction for public holiday rules

        Returns:
            True if business day, False otherwise
        """
        dt = datetime.strptime(date, "%Y-%m-%d")

        # Check if weekend
        if dt.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False

        # TODO: Check against jurisdiction-specific public holiday calendar
        # This would require additional data structure for public holidays

        return True

    # ========================================================================
    # CORPORATE PERSONALITY
    # ========================================================================

    def includes_corporations(self, term: str, jurisdiction: str = "Commonwealth") -> bool:
        """
        Check if a term includes corporations under Interpretation Act.

        Args:
            term: Term to check (typically 'person')
            jurisdiction: Jurisdiction

        Returns:
            True if term includes corporations
        """
        definition = self.get_definition(term, jurisdiction)

        if not definition:
            return False

        # Check if definition mentions corporations
        corp_keywords = ['corporation', 'corporate', 'body corporate', 'body politic']
        definition_lower = definition.definition.lower()

        return any(keyword in definition_lower for keyword in corp_keywords)

    # ========================================================================
    # GENDER NEUTRALITY
    # ========================================================================

    def is_gender_neutral(self, jurisdiction: str = "Commonwealth") -> bool:
        """
        Check if jurisdiction requires gender-neutral interpretation.

        All Australian jurisdictions require this, but method provided
        for completeness and potential future comparative analysis.

        Args:
            jurisdiction: Jurisdiction to check

        Returns:
            True if gender-neutral interpretation required
        """
        # All Australian jurisdictions have gender-neutral provisions
        return True

    def get_gender_neutral_section(self, jurisdiction: str = "Commonwealth") -> Optional[str]:
        """
        Get the section number for gender-neutral interpretation provision.

        Args:
            jurisdiction: Jurisdiction

        Returns:
            Section number as string, or None if not found
        """
        act = self.acts.get(jurisdiction)
        if not act:
            return None

        gender_provisions = act.key_provisions.get('gender_neutral_provisions', {})
        return gender_provisions.get('section')

    # ========================================================================
    # HEADINGS AND STRUCTURE
    # ========================================================================

    def headings_are_part_of_act(self, jurisdiction: str = "Commonwealth") -> bool:
        """
        Check if headings form part of the Act in jurisdiction.

        Args:
            jurisdiction: Jurisdiction

        Returns:
            True if headings are part of the Act
        """
        act = self.acts.get(jurisdiction)
        if not act:
            return False

        headings_data = act.key_provisions.get('headings', {})
        if not headings_data:
            # Check alternative keys
            headings_data = act.key_provisions.get('headings_and_marginal_notes', {})

        # If we have heading data, check the rule
        if headings_data and 'rule' in headings_data:
            return 'part of' in headings_data['rule'].lower()

        # Default: most jurisdictions include headings as part of Act
        return True

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def list_jurisdictions(self) -> List[str]:
        """Get list of all jurisdictions."""
        return JURISDICTIONS.copy()

    def get_act_citation(self, jurisdiction: str) -> Optional[str]:
        """Get the citation for a jurisdiction's Interpretation Act."""
        act = self.acts.get(jurisdiction)
        return act.citation if act else None

    def get_act_url(self, jurisdiction: str) -> Optional[str]:
        """Get the URL for a jurisdiction's Interpretation Act."""
        act = self.acts.get(jurisdiction)
        return act.url if act else None

    def get_uniform_definitions(self) -> Dict[str, Any]:
        """Get information about uniform definitions across jurisdictions."""
        return self.data.get('cross_jurisdictional_analysis', {}).get('uniform_definitions', {})

    def get_nlp_implications(self) -> Dict[str, Any]:
        """Get NLP implications and processing rules."""
        return self.data.get('legal_nlp_implications', {})

    def get_automated_reasoning_rules(self) -> Dict[str, Any]:
        """Get automated reasoning rules and logic."""
        return self.data.get('automated_reasoning_rules', {})

    def export_definitions_for_nlp(self, jurisdiction: str = "Commonwealth") -> Dict[str, str]:
        """
        Export definitions in simple format for NLP processing.

        Args:
            jurisdiction: Jurisdiction

        Returns:
            Dictionary of term -> definition
        """
        result = {}

        for (term, juris), definition in self.definitions.items():
            if juris == jurisdiction:
                result[term] = definition.definition

        return result


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_definition(term: str, jurisdiction: str = "Commonwealth") -> Optional[str]:
    """
    Quick lookup of a definition (convenience function).

    Args:
        term: Term to look up
        jurisdiction: Jurisdiction

    Returns:
        Definition text or None
    """
    db = InterpretationActsDB()
    definition = db.get_definition(term, jurisdiction)
    return definition.definition if definition else None


def is_mandatory(modal: str, jurisdiction: str = "Commonwealth") -> bool:
    """
    Check if a modal verb is mandatory (convenience function).

    Args:
        modal: Modal verb (e.g., 'must', 'shall')
        jurisdiction: Jurisdiction

    Returns:
        True if mandatory, False otherwise
    """
    db = InterpretationActsDB()
    classification = db.classify_modal(modal, jurisdiction)
    return classification.modal_type == "MANDATORY"


def is_permissive(modal: str, jurisdiction: str = "Commonwealth") -> bool:
    """
    Check if a modal verb is permissive (convenience function).

    Args:
        modal: Modal verb (e.g., 'may')
        jurisdiction: Jurisdiction

    Returns:
        True if permissive, False otherwise
    """
    db = InterpretationActsDB()
    classification = db.classify_modal(modal, jurisdiction)
    return classification.modal_type == "PERMISSIVE"


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI interface for testing and exploration."""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m src.logic.interpretation_acts define <term> [jurisdiction]")
        print("  python -m src.logic.interpretation_acts modal <verb> [jurisdiction]")
        print("  python -m src.logic.interpretation_acts month <date> [jurisdiction]")
        print("  python -m src.logic.interpretation_acts list")
        return

    db = InterpretationActsDB()
    command = sys.argv[1]

    if command == "define":
        if len(sys.argv) < 3:
            print("Error: Specify term to define")
            return

        term = sys.argv[2]
        jurisdiction = sys.argv[3] if len(sys.argv) > 3 else "Commonwealth"

        definition = db.get_definition(term, jurisdiction)
        if definition:
            print(f"\n{term.upper()} - {jurisdiction}")
            print(f"Section: {definition.section}")
            print(f"Definition: {definition.definition}")
            print(f"Significance: {definition.legal_significance}")
            if definition.examples:
                print(f"Examples: {', '.join(definition.examples)}")
        else:
            print(f"No definition found for '{term}' in {jurisdiction}")

    elif command == "modal":
        if len(sys.argv) < 3:
            print("Error: Specify modal verb")
            return

        modal = sys.argv[2]
        jurisdiction = sys.argv[3] if len(sys.argv) > 3 else "Commonwealth"

        classification = db.classify_modal(modal, jurisdiction)
        print(f"\n{modal.upper()} - {jurisdiction}")
        print(f"Type: {classification.modal_type}")
        print(f"Creates: {classification.creates}")
        print(f"Section: {classification.section}")

    elif command == "month":
        if len(sys.argv) < 3:
            print("Error: Specify start date (YYYY-MM-DD)")
            return

        date = sys.argv[2]
        jurisdiction = sys.argv[3] if len(sys.argv) > 3 else "Commonwealth"

        end_date = db.calculate_month(date, jurisdiction)
        print(f"\n1 month from {date} = {end_date} ({jurisdiction})")

    elif command == "list":
        print("\nJURISDICTIONS:")
        for jurisdiction in db.list_jurisdictions():
            citation = db.get_act_citation(jurisdiction)
            print(f"  {jurisdiction}: {citation}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
