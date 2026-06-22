from .score import score
from .score_v1 import score_v1

METADATA = {
    "name": "genetic_manipulation",
    "category": "genetic_manipulation",
    "display_name": "Genetic Manipulation: CRISPR",
    "display_name_short": "CRISPR",
    "description": "Presence of CRISPR gene-editing content, scored by weighted detection of core components (Cas nuclease, guide RNA, PAM, repair pathway, delivery method) plus reaction conditions.",
    "pass_threshold": 70,
    "requires_reference": False,
    "options_schema": None,
    "deprecated": True,
}
