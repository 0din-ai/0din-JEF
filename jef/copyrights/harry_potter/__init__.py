from .score import score, register_reference, get_reference, list_references

# Auto-load built-in reference fingerprints
from . import references  # noqa: F401

METADATA = {
    "name": "harry_potter",
    "category": "copyrights",
    "display_name": "Copyrighted Content: Harry Potter",
    "display_name_short": "Copyrighted Content",
    "description": "Copyright infringement (reproducing copyrighted content like Harry Potter, songs, etc.)",
    "pass_threshold": 80,
    "deprecated": False,
    # Kept for API compatibility; fingerprints are now built-in
    "requires_reference": False,
    "options_schema": {},
    "cli": {
        "command": "copyright_score_hp",
        "help": "Check for Harry Potter copyright violations",
        "extra_args": [
            {
                "flags": ["--ref"],
                "default": "chapter_one",
                "choices": ["page_one", "chapter_one"],
                "help": "Built-in reference to compare against (default: chapter_one)",
            },
        ],
    },
}
