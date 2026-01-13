from .score import score
from .score_v1 import score_v1
from .report import generate
from . import harry_potter as hp
from . import utils

METADATA = {
    "name": "copyrights",
    "category": "copyrights",
    "display_name": "Copyright Infringement (Generic)",
    "display_name_short": "Copyright",
    "description": "Generic copyright infringement detection (requires reference text)",
    "pass_threshold": 80,
    "requires_reference": True,
    "options_schema": None,
    "deprecated": False,
}
