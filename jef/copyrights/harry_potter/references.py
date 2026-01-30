"""Load built-in Harry Potter reference fingerprints."""

from pathlib import Path
from jef.copyrights.fingerprints import ReferenceFingerprints
from .score import register_reference

DATA_DIR = Path(__file__).parent / "data"


def _load_all() -> list[str]:
    """Load all fingerprints from data directory."""
    loaded = []
    if not DATA_DIR.exists():
        return loaded

    for filepath in DATA_DIR.glob("*.json.gz"):
        name = filepath.stem.replace(".json", "")
        fingerprints = ReferenceFingerprints.from_gzip(filepath)
        register_reference(name, fingerprints)
        loaded.append(name)

    return loaded


# Auto-load on import
_loaded = _load_all()
