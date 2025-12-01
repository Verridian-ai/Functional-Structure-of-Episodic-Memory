"""
Australian Court Hierarchy and Precedent Taxonomy

Structured data for Citator and Ratio Miner agents.
Based on comprehensive research of Australian court system (2025).

Usage:
    from src.agents.australian_courts_taxonomy import COURTS, get_court_info, is_binding_precedent

    court = get_court_info("HCA")
    binding = is_binding_precedent(precedent_court="NSWSC", current_court="NSWDC")
"""

from typing import Dict, List, Optional, Set, Literal
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class CourtLevel(Enum):
    """Court hierarchy level."""
    APEX = 1          # High Court
    APPELLATE = 2     # Courts of Appeal, Full Courts
    SUPERIOR = 3      # Supreme Courts, Federal Court
    INTERMEDIATE = 4  # District/County Courts
    LOWER = 5         # Magistrates/Local Courts
    TRIBUNAL = 6      # Administrative tribunals


class Jurisdiction(Enum):
    """Jurisdiction type."""
    FEDERAL = "federal"
    NSW = "nsw"
    VIC = "vic"
    QLD = "qld"
    SA = "sa"
    WA = "wa"
    TAS = "tas"
    ACT = "act"
    NT = "nt"


class CourtType(Enum):
    """Type of judicial body."""
    COURT = "court"
    TRIBUNAL = "tribunal"
    COURT_OF_RECORD = "court_of_record"  # Special status (e.g., QCAT)


class ReportType(Enum):
    """Law report type."""
    AUTHORIZED = "authorized"
    UNOFFICIAL = "unofficial"
    MEDIUM_NEUTRAL = "medium_neutral"
    UNREPORTED = "unreported"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class CourtInfo:
    """Complete information about a court."""
    abbreviation: str
    full_name: str
    jurisdiction: Jurisdiction
    level: CourtLevel
    court_type: CourtType

    # Binding relationships
    binds: List[str]  # List of court abbreviations this court binds
    bound_by: List[str]  # List of court abbreviations that bind this court

    # Citation format
    medium_neutral_format: str  # e.g., "[YEAR] HCA [NUMBER]"
    authorized_reports: List[str]  # e.g., ["CLR"]

    # Status
    active: bool  # False for defunct courts (e.g., FamCA)
    replaced_by: Optional[str] = None  # If defunct, what replaced it

    # Special characteristics
    can_overrule_self: bool = False
    is_court_of_record: bool = False

    # Appeals
    appeals_to: Optional[str] = None


@dataclass
class LawReportInfo:
    """Information about a law report series."""
    abbreviation: str
    full_name: str
    report_type: ReportType
    coverage: str  # Which courts/areas
    publisher: Optional[str] = None
    citation_format: str = "(Year) Volume Report Page"


# ============================================================================
# COURT TAXONOMY
# ============================================================================

COURTS: Dict[str, CourtInfo] = {

    # ========================================================================
    # FEDERAL COURTS
    # ========================================================================

    "HCA": CourtInfo(
        abbreviation="HCA",
        full_name="High Court of Australia",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.APEX,
        court_type=CourtType.COURT,
        binds=["ALL"],  # Special: binds all Australian courts
        bound_by=[],
        medium_neutral_format="[YEAR] HCA [NUMBER]",
        authorized_reports=["CLR", "ALJR"],
        active=True,
        can_overrule_self=True,
        is_court_of_record=True,
        appeals_to=None  # Apex court
    ),

    "FCAFC": CourtInfo(
        abbreviation="FCAFC",
        full_name="Federal Court of Australia Full Court",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["FCA", "FedCFamC", "FCCA", "FamCA"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] FCAFC [NUMBER]",
        authorized_reports=["FCR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "FCA": CourtInfo(
        abbreviation="FCA",
        full_name="Federal Court of Australia",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["FedCFamC", "FCCA"],
        bound_by=["HCA", "FCAFC"],
        medium_neutral_format="[YEAR] FCA [NUMBER]",
        authorized_reports=["FCR"],
        active=True,
        is_court_of_record=True,
        appeals_to="FCAFC"
    ),

    "FedCFamC": CourtInfo(
        abbreviation="FedCFamC",
        full_name="Federal Circuit and Family Court of Australia",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "FCAFC", "FCA"],
        medium_neutral_format="[YEAR] FedCFamC [NUMBER]",
        authorized_reports=["FamLR"],
        active=True,
        is_court_of_record=True,
        appeals_to="FCAFC"
    ),

    # Defunct federal courts
    "FamCA": CourtInfo(
        abbreviation="FamCA",
        full_name="Family Court of Australia",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "FamCAFC"],
        medium_neutral_format="[YEAR] FamCA [NUMBER]",
        authorized_reports=["FamLR"],
        active=False,
        replaced_by="FedCFamC",
        is_court_of_record=True,
        appeals_to="FamCAFC"
    ),

    "FamCAFC": CourtInfo(
        abbreviation="FamCAFC",
        full_name="Family Court of Australia Full Court",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["FamCA"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] FamCAFC [NUMBER]",
        authorized_reports=["FamLR"],
        active=False,
        replaced_by="FedCFamC",
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "FCCA": CourtInfo(
        abbreviation="FCCA",
        full_name="Federal Circuit Court of Australia",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "FCAFC", "FCA"],
        medium_neutral_format="[YEAR] FCCA [NUMBER]",
        authorized_reports=[],
        active=False,
        replaced_by="FedCFamC",
        is_court_of_record=True,
        appeals_to="FCA"
    ),

    "AATA": CourtInfo(
        abbreviation="AATA",
        full_name="Administrative Appeals Tribunal",
        jurisdiction=Jurisdiction.FEDERAL,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "FCAFC", "FCA"],
        medium_neutral_format="[YEAR] AATA [NUMBER]",
        authorized_reports=[],
        active=False,
        replaced_by="ART",
        is_court_of_record=False,
        appeals_to="FCA"
    ),

    # ========================================================================
    # NEW SOUTH WALES
    # ========================================================================

    "NSWCA": CourtInfo(
        abbreviation="NSWCA",
        full_name="Court of Appeal of New South Wales",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["NSWSC", "NSWDC", "NSWLC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] NSWCA [NUMBER]",
        authorized_reports=["NSWLR", "NSWCAR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "NSWCCA": CourtInfo(
        abbreviation="NSWCCA",
        full_name="Court of Criminal Appeal of New South Wales",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["NSWSC", "NSWDC", "NSWLC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] NSWCCA [NUMBER]",
        authorized_reports=["NSWLR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "NSWSC": CourtInfo(
        abbreviation="NSWSC",
        full_name="Supreme Court of New South Wales",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["NSWDC", "NSWLC"],
        bound_by=["HCA", "NSWCA", "NSWCCA"],
        medium_neutral_format="[YEAR] NSWSC [NUMBER]",
        authorized_reports=["NSWLR"],
        active=True,
        is_court_of_record=True,
        appeals_to="NSWCA"
    ),

    "NSWDC": CourtInfo(
        abbreviation="NSWDC",
        full_name="District Court of New South Wales",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=["NSWLC"],
        bound_by=["HCA", "NSWCA", "NSWCCA", "NSWSC"],
        medium_neutral_format="[YEAR] NSWDC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="NSWCA"
    ),

    "NSWLC": CourtInfo(
        abbreviation="NSWLC",
        full_name="Local Court of New South Wales",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "NSWCA", "NSWCCA", "NSWSC", "NSWDC"],
        medium_neutral_format="[YEAR] NSWLC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="NSWDC"
    ),

    "NCAT": CourtInfo(
        abbreviation="NCAT",
        full_name="NSW Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.NSW,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "NSWCA", "NSWSC"],
        medium_neutral_format="[YEAR] NCAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,  # NOT a court of record
        appeals_to="NSWCA"
    ),

    # ========================================================================
    # VICTORIA
    # ========================================================================

    "VSCA": CourtInfo(
        abbreviation="VSCA",
        full_name="Court of Appeal of Victoria",
        jurisdiction=Jurisdiction.VIC,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["VSC", "VCC", "VMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] VSCA [NUMBER]",
        authorized_reports=["VR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "VSC": CourtInfo(
        abbreviation="VSC",
        full_name="Supreme Court of Victoria",
        jurisdiction=Jurisdiction.VIC,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["VCC", "VMC"],
        bound_by=["HCA", "VSCA"],
        medium_neutral_format="[YEAR] VSC [NUMBER]",
        authorized_reports=["VR"],
        active=True,
        is_court_of_record=True,
        appeals_to="VSCA"
    ),

    "VCC": CourtInfo(
        abbreviation="VCC",
        full_name="County Court of Victoria",
        jurisdiction=Jurisdiction.VIC,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=["VMC"],
        bound_by=["HCA", "VSCA", "VSC"],
        medium_neutral_format="[YEAR] VCC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="VSCA"
    ),

    "VMC": CourtInfo(
        abbreviation="VMC",
        full_name="Magistrates' Court of Victoria",
        jurisdiction=Jurisdiction.VIC,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "VSCA", "VSC", "VCC"],
        medium_neutral_format="[YEAR] VMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="VCC"
    ),

    "VCAT": CourtInfo(
        abbreviation="VCAT",
        full_name="Victorian Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.VIC,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "VSCA", "VSC"],
        medium_neutral_format="[YEAR] VCAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,  # NOT a court of record
        appeals_to="VSCA"
    ),

    # ========================================================================
    # QUEENSLAND
    # ========================================================================

    "QCA": CourtInfo(
        abbreviation="QCA",
        full_name="Court of Appeal of Queensland",
        jurisdiction=Jurisdiction.QLD,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["QSC", "QDC", "QMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] QCA [NUMBER]",
        authorized_reports=["Qd R"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "QSC": CourtInfo(
        abbreviation="QSC",
        full_name="Supreme Court of Queensland",
        jurisdiction=Jurisdiction.QLD,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["QDC", "QMC"],
        bound_by=["HCA", "QCA"],
        medium_neutral_format="[YEAR] QSC [NUMBER]",
        authorized_reports=["Qd R"],
        active=True,
        is_court_of_record=True,
        appeals_to="QCA"
    ),

    "QDC": CourtInfo(
        abbreviation="QDC",
        full_name="District Court of Queensland",
        jurisdiction=Jurisdiction.QLD,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=["QMC"],
        bound_by=["HCA", "QCA", "QSC"],
        medium_neutral_format="[YEAR] QDC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="QCA"
    ),

    "QMC": CourtInfo(
        abbreviation="QMC",
        full_name="Magistrates Court of Queensland",
        jurisdiction=Jurisdiction.QLD,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "QCA", "QSC", "QDC"],
        medium_neutral_format="[YEAR] QMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="QDC"
    ),

    "QCAT": CourtInfo(
        abbreviation="QCAT",
        full_name="Queensland Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.QLD,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.COURT_OF_RECORD,  # UNIQUE: QCAT IS a court of record
        binds=[],
        bound_by=["HCA", "QCA", "QSC"],
        medium_neutral_format="[YEAR] QCAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,  # UNIQUE among tribunals
        appeals_to="QCA"
    ),

    # ========================================================================
    # SOUTH AUSTRALIA
    # ========================================================================

    "SASCFC": CourtInfo(
        abbreviation="SASCFC",
        full_name="Full Court of the Supreme Court of South Australia",
        jurisdiction=Jurisdiction.SA,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["SASC", "SADC", "SAMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] SASCFC [NUMBER]",
        authorized_reports=["SASR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "SASC": CourtInfo(
        abbreviation="SASC",
        full_name="Supreme Court of South Australia",
        jurisdiction=Jurisdiction.SA,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["SADC", "SAMC"],
        bound_by=["HCA", "SASCFC"],
        medium_neutral_format="[YEAR] SASC [NUMBER]",
        authorized_reports=["SASR"],
        active=True,
        is_court_of_record=True,
        appeals_to="SASCFC"
    ),

    "SADC": CourtInfo(
        abbreviation="SADC",
        full_name="District Court of South Australia",
        jurisdiction=Jurisdiction.SA,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=["SAMC"],
        bound_by=["HCA", "SASCFC", "SASC"],
        medium_neutral_format="[YEAR] SADC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="SASCFC"
    ),

    "SAMC": CourtInfo(
        abbreviation="SAMC",
        full_name="Magistrates Court of South Australia",
        jurisdiction=Jurisdiction.SA,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "SASCFC", "SASC", "SADC"],
        medium_neutral_format="[YEAR] SAMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="SADC"
    ),

    "SACAT": CourtInfo(
        abbreviation="SACAT",
        full_name="South Australian Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.SA,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "SASCFC", "SASC"],
        medium_neutral_format="[YEAR] SACAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,
        appeals_to="SASCFC"
    ),

    # ========================================================================
    # WESTERN AUSTRALIA
    # ========================================================================

    "WASCA": CourtInfo(
        abbreviation="WASCA",
        full_name="Court of Appeal of Western Australia",
        jurisdiction=Jurisdiction.WA,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["WASC", "WADC", "WAMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] WASCA [NUMBER]",
        authorized_reports=["WAR"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "WASC": CourtInfo(
        abbreviation="WASC",
        full_name="Supreme Court of Western Australia",
        jurisdiction=Jurisdiction.WA,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["WADC", "WAMC"],
        bound_by=["HCA", "WASCA"],
        medium_neutral_format="[YEAR] WASC [NUMBER]",
        authorized_reports=["WAR"],
        active=True,
        is_court_of_record=True,
        appeals_to="WASCA"
    ),

    "WADC": CourtInfo(
        abbreviation="WADC",
        full_name="District Court of Western Australia",
        jurisdiction=Jurisdiction.WA,
        level=CourtLevel.INTERMEDIATE,
        court_type=CourtType.COURT,
        binds=["WAMC"],
        bound_by=["HCA", "WASCA", "WASC"],
        medium_neutral_format="[YEAR] WADC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="WASCA"
    ),

    "WAMC": CourtInfo(
        abbreviation="WAMC",
        full_name="Magistrates Court of Western Australia",
        jurisdiction=Jurisdiction.WA,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "WASCA", "WASC", "WADC"],
        medium_neutral_format="[YEAR] WAMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="WADC"
    ),

    "WASAT": CourtInfo(
        abbreviation="WASAT",
        full_name="State Administrative Tribunal of Western Australia",
        jurisdiction=Jurisdiction.WA,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "WASCA", "WASC"],
        medium_neutral_format="[YEAR] WASAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,
        appeals_to="WASCA"
    ),

    # ========================================================================
    # TASMANIA
    # ========================================================================

    "TASCCA": CourtInfo(
        abbreviation="TASCCA",
        full_name="Court of Criminal Appeal of Tasmania",
        jurisdiction=Jurisdiction.TAS,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["TASSC", "TASMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] TASCCA [NUMBER]",
        authorized_reports=["Tas R"],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "TASSC": CourtInfo(
        abbreviation="TASSC",
        full_name="Supreme Court of Tasmania",
        jurisdiction=Jurisdiction.TAS,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["TASMC"],
        bound_by=["HCA", "TASCCA"],
        medium_neutral_format="[YEAR] TASSC [NUMBER]",
        authorized_reports=["Tas R"],
        active=True,
        is_court_of_record=True,
        appeals_to="TASCCA"
    ),

    "TASMC": CourtInfo(
        abbreviation="TASMC",
        full_name="Magistrates Court of Tasmania",
        jurisdiction=Jurisdiction.TAS,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "TASCCA", "TASSC"],
        medium_neutral_format="[YEAR] TASMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="TASSC"
    ),

    # ========================================================================
    # AUSTRALIAN CAPITAL TERRITORY
    # ========================================================================

    "ACTSC": CourtInfo(
        abbreviation="ACTSC",
        full_name="Supreme Court of the Australian Capital Territory",
        jurisdiction=Jurisdiction.ACT,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["ACTMC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] ACTSC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "ACTMC": CourtInfo(
        abbreviation="ACTMC",
        full_name="Magistrates Court of the Australian Capital Territory",
        jurisdiction=Jurisdiction.ACT,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "ACTSC"],
        medium_neutral_format="[YEAR] ACTMC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="ACTSC"
    ),

    "ACAT": CourtInfo(
        abbreviation="ACAT",
        full_name="ACT Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.ACT,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "ACTSC"],
        medium_neutral_format="[YEAR] ACAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,
        appeals_to="ACTSC"
    ),

    # ========================================================================
    # NORTHERN TERRITORY
    # ========================================================================

    "NTCA": CourtInfo(
        abbreviation="NTCA",
        full_name="Court of Appeal of the Northern Territory",
        jurisdiction=Jurisdiction.NT,
        level=CourtLevel.APPELLATE,
        court_type=CourtType.COURT,
        binds=["NTSC", "NTLC"],
        bound_by=["HCA"],
        medium_neutral_format="[YEAR] NTCA [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="HCA"
    ),

    "NTSC": CourtInfo(
        abbreviation="NTSC",
        full_name="Supreme Court of the Northern Territory",
        jurisdiction=Jurisdiction.NT,
        level=CourtLevel.SUPERIOR,
        court_type=CourtType.COURT,
        binds=["NTLC"],
        bound_by=["HCA", "NTCA"],
        medium_neutral_format="[YEAR] NTSC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="NTCA"
    ),

    "NTLC": CourtInfo(
        abbreviation="NTLC",
        full_name="Local Court of the Northern Territory",
        jurisdiction=Jurisdiction.NT,
        level=CourtLevel.LOWER,
        court_type=CourtType.COURT,
        binds=[],
        bound_by=["HCA", "NTCA", "NTSC"],
        medium_neutral_format="[YEAR] NTLC [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=True,
        appeals_to="NTSC"
    ),

    "NTCAT": CourtInfo(
        abbreviation="NTCAT",
        full_name="Northern Territory Civil and Administrative Tribunal",
        jurisdiction=Jurisdiction.NT,
        level=CourtLevel.TRIBUNAL,
        court_type=CourtType.TRIBUNAL,
        binds=[],
        bound_by=["HCA", "NTCA", "NTSC"],
        medium_neutral_format="[YEAR] NTCAT [NUMBER]",
        authorized_reports=[],
        active=True,
        is_court_of_record=False,
        appeals_to="NTSC"
    ),
}


# ============================================================================
# LAW REPORT SERIES
# ============================================================================

LAW_REPORTS: Dict[str, LawReportInfo] = {
    # Federal Authorized
    "CLR": LawReportInfo(
        abbreviation="CLR",
        full_name="Commonwealth Law Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="High Court of Australia",
        publisher="Lawbook Co."
    ),

    "FCR": LawReportInfo(
        abbreviation="FCR",
        full_name="Federal Court Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Federal Court of Australia",
        publisher="Lawbook Co."
    ),

    "FamLR": LawReportInfo(
        abbreviation="FamLR",
        full_name="Family Law Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Family Court / Federal Circuit and Family Court",
        publisher="LexisNexis"
    ),

    # State Authorized
    "NSWLR": LawReportInfo(
        abbreviation="NSWLR",
        full_name="New South Wales Law Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="NSW Supreme Court",
        publisher="Lawbook Co."
    ),

    "VR": LawReportInfo(
        abbreviation="VR",
        full_name="Victorian Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Supreme Court of Victoria",
        publisher="Council of Law Reporting"
    ),

    "Qd R": LawReportInfo(
        abbreviation="Qd R",
        full_name="Queensland Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Supreme Court of Queensland",
        publisher="Supreme Court of Queensland Library"
    ),

    "SASR": LawReportInfo(
        abbreviation="SASR",
        full_name="South Australian State Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Supreme Court of South Australia",
        publisher="Supreme Court of South Australia"
    ),

    "WAR": LawReportInfo(
        abbreviation="WAR",
        full_name="Western Australian Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Supreme Court of Western Australia",
        publisher="Supreme Court of Western Australia"
    ),

    "Tas R": LawReportInfo(
        abbreviation="Tas R",
        full_name="Tasmanian Reports",
        report_type=ReportType.AUTHORIZED,
        coverage="Supreme Court of Tasmania",
        publisher="Supreme Court of Tasmania"
    ),

    # Unofficial
    "ALR": LawReportInfo(
        abbreviation="ALR",
        full_name="Australian Law Reports",
        report_type=ReportType.UNOFFICIAL,
        coverage="Cross-jurisdictional significant cases",
        publisher="LexisNexis"
    ),

    "ALJR": LawReportInfo(
        abbreviation="ALJR",
        full_name="Australian Law Journal Reports",
        report_type=ReportType.UNOFFICIAL,
        coverage="HCA and significant appellate decisions",
        publisher="Lawbook Co."
    ),

    "A Crim R": LawReportInfo(
        abbreviation="A Crim R",
        full_name="Australian Criminal Reports",
        report_type=ReportType.UNOFFICIAL,
        coverage="Criminal law across jurisdictions",
        publisher="Lawbook Co."
    ),
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_court_info(abbreviation: str) -> Optional[CourtInfo]:
    """Get court information by abbreviation."""
    return COURTS.get(abbreviation.upper())


def is_binding_precedent(precedent_court: str, current_court: str) -> bool:
    """
    Determine if a precedent from precedent_court is binding on current_court.

    Args:
        precedent_court: Abbreviation of court that created precedent (e.g., "HCA")
        current_court: Abbreviation of court where precedent is being applied (e.g., "NSWDC")

    Returns:
        True if precedent is binding, False if only persuasive
    """
    prec = get_court_info(precedent_court)
    curr = get_court_info(current_court)

    if not prec or not curr:
        return False

    # High Court binds all
    if precedent_court.upper() == "HCA":
        return True

    # Must be same jurisdiction (except HCA)
    if prec.jurisdiction != curr.jurisdiction:
        return False

    # Check if current court is in precedent court's "binds" list
    return current_court.upper() in [c.upper() for c in prec.binds]


def get_binding_relationship(court1: str, court2: str) -> Literal["binds", "bound_by", "persuasive", "equal"]:
    """
    Determine relationship between two courts.

    Returns:
        - "binds": court1 binds court2
        - "bound_by": court1 is bound by court2
        - "persuasive": courts are persuasive on each other
        - "equal": same court
    """
    if court1.upper() == court2.upper():
        return "equal"

    if is_binding_precedent(court1, court2):
        return "binds"

    if is_binding_precedent(court2, court1):
        return "bound_by"

    return "persuasive"


def get_courts_by_jurisdiction(jurisdiction: Jurisdiction) -> List[CourtInfo]:
    """Get all courts in a jurisdiction."""
    return [c for c in COURTS.values() if c.jurisdiction == jurisdiction and c.active]


def get_courts_by_level(level: CourtLevel) -> List[CourtInfo]:
    """Get all courts at a specific level."""
    return [c for c in COURTS.values() if c.level == level and c.active]


def parse_medium_neutral_citation(citation: str) -> Optional[Dict[str, str]]:
    """
    Parse a medium neutral citation.

    Args:
        citation: e.g., "[2024] HCA 15 [42]"

    Returns:
        Dict with keys: year, court, number, paragraph (optional)
    """
    import re

    # Pattern: [YEAR] COURT NUMBER [PARAGRAPH]
    pattern = r'\[(\d{4})\]\s+([A-Z]{2,10})\s+(\d+)(?:\s+\[(\d+)\])?'
    match = re.match(pattern, citation.strip())

    if not match:
        return None

    result = {
        "year": match.group(1),
        "court": match.group(2),
        "number": match.group(3),
    }

    if match.group(4):
        result["paragraph"] = match.group(4)

    return result


def validate_citation(citation: str) -> bool:
    """Validate if citation is properly formatted medium neutral citation."""
    parsed = parse_medium_neutral_citation(citation)
    if not parsed:
        return False

    # Check if court code is valid
    court = get_court_info(parsed["court"])
    return court is not None


def get_court_hierarchy_path(from_court: str, to_court: str) -> Optional[List[str]]:
    """
    Get the hierarchy path from one court to another.

    Returns list of court abbreviations from from_court to to_court,
    or None if no direct hierarchical path exists.
    """
    from_info = get_court_info(from_court)
    to_info = get_court_info(to_court)

    if not from_info or not to_info:
        return None

    # Same court
    if from_court.upper() == to_court.upper():
        return [from_court]

    # Check if direct binding relationship
    if is_binding_precedent(from_court, to_court):
        return [from_court, to_court]

    # Try to find path through appeals
    path = [from_court]
    current = from_info

    while current.appeals_to:
        path.append(current.appeals_to)
        if current.appeals_to.upper() == to_court.upper():
            return path
        current = get_court_info(current.appeals_to)
        if not current:
            break

    return None


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AUSTRALIAN COURT TAXONOMY - DEMO")
    print("=" * 70)

    # Test 1: Get court info
    print("\n1. High Court Information:")
    hca = get_court_info("HCA")
    print(f"   Full Name: {hca.full_name}")
    print(f"   Level: {hca.level.name}")
    print(f"   Binds: {hca.binds}")
    print(f"   Can overrule self: {hca.can_overrule_self}")

    # Test 2: Binding precedent check
    print("\n2. Binding Precedent Tests:")
    tests = [
        ("HCA", "NSWSC", "Should be binding"),
        ("NSWSC", "NSWDC", "Should be binding"),
        ("NSWSC", "VSC", "Should NOT be binding (different states)"),
        ("FCA", "NSWDC", "Should NOT be binding (different hierarchies)"),
        ("NSWDC", "NSWSC", "Should NOT be binding (lower to higher)"),
    ]

    for prec_court, curr_court, expected in tests:
        binding = is_binding_precedent(prec_court, curr_court)
        status = "[BINDS]" if binding else "[PERSUASIVE]"
        print(f"   {prec_court} -> {curr_court}: {status} ({expected})")

    # Test 3: Parse citations
    print("\n3. Citation Parsing:")
    test_citations = [
        "[2024] HCA 15",
        "[2023] NSWSC 123 [45]",
        "[2022] QCAT 567",
    ]

    for cit in test_citations:
        parsed = parse_medium_neutral_citation(cit)
        if parsed:
            court = get_court_info(parsed["court"])
            print(f"   {cit}")
            print(f"      -> {court.full_name if court else 'Unknown'}")
            print(f"      -> Year: {parsed['year']}, Number: {parsed['number']}")

    # Test 4: Jurisdiction overview
    print("\n4. NSW Court Hierarchy:")
    nsw_courts = get_courts_by_jurisdiction(Jurisdiction.NSW)
    nsw_courts.sort(key=lambda c: c.level.value)

    for court in nsw_courts:
        if court.court_type != CourtType.TRIBUNAL:
            print(f"   Level {court.level.value}: {court.abbreviation} - {court.full_name}")

    # Test 5: Special cases
    print("\n5. Special Cases:")
    qcat = get_court_info("QCAT")
    vcat = get_court_info("VCAT")
    print(f"   QCAT is court of record: {qcat.is_court_of_record} [YES] (UNIQUE)")
    print(f"   VCAT is court of record: {vcat.is_court_of_record} [NO]")

    print("\n" + "=" * 70)
