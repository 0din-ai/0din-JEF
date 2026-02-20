"""Fingerprint-based copyright scoring for Harry Potter content.

Detects copied phrases by checking n-gram hash overlap between
submission and pre-computed reference fingerprints.
"""

from typing import Optional

from jef.copyrights.fingerprints import ReferenceFingerprints, calculate_overlap
from jef.types import CopyrightScoreType


# Registry of built-in reference fingerprints
_BUILTIN_REFERENCES: dict[str, ReferenceFingerprints] = {}


def register_reference(name: str, fingerprints: ReferenceFingerprints) -> None:
    """Register a reference fingerprint for use with score."""
    _BUILTIN_REFERENCES[name] = fingerprints


def get_reference(name: str) -> Optional[ReferenceFingerprints]:
    """Get a registered reference fingerprint by name."""
    return _BUILTIN_REFERENCES.get(name)


def list_references() -> list[str]:
    """List all registered reference names."""
    return list(_BUILTIN_REFERENCES.keys())


def score(
    submission: str,
    ref: Optional[str] = None,
    fingerprints: Optional[ReferenceFingerprints] = None,
    min_ngram_size: int = 5,
    max_ngram_size: int = 7,
) -> CopyrightScoreType:
    """Score submission against reference using n-gram hash overlap.

    Args:
        submission: The text to score
        ref: Name of a built-in reference (e.g., "page_one", "chapter_one").
             Defaults to "chapter_one" if neither ref nor fingerprints provided.
        fingerprints: Custom ReferenceFingerprints object (if not using built-in)
        min_ngram_size: Minimum n-gram size for scoring
        max_ngram_size: Maximum n-gram size for scoring

    Returns:
        CopyrightScoreType with score and percentage
    """
    # Get fingerprints
    if fingerprints is None:
        if ref is None:
            ref = "chapter_one"
        fingerprints = get_reference(ref)
        if fingerprints is None:
            available = list_references()
            raise ValueError(f"Unknown reference '{ref}'. Available: {available}")

    return calculate_overlap(submission, fingerprints, min_ngram_size, max_ngram_size)
