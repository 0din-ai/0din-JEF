"""Fingerprint-based reference storage for copyright detection.

This module provides utilities to generate and use pre-computed fingerprints
for copyright detection, eliminating the need to ship raw copyrighted text.

Fingerprints are stored as gzip-compressed JSON for efficient storage.
The original copyrighted text cannot be recovered from the fingerprints.
"""

import gzip
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Set, Union

from .utils import (
    get_words,
    get_ngrams,
    rolling_hash,
)


@dataclass
class ReferenceFingerprints:
    """Compact pre-computed fingerprints for a reference text.

    Contains n-gram hashes for detecting copied phrases.
    """

    name: str  # e.g., "page_one", "chapter_one"
    ngram_hashes: List[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ReferenceFingerprints":
        """Create from dictionary (JSON deserialization)."""
        # Handle legacy format with extra fields
        return cls(
            name=data["name"],
            ngram_hashes=data.get("ngram_hashes", []),
        )

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "ReferenceFingerprints":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_gzip(self, filepath: Union[str, Path]) -> int:
        """Save fingerprints to a gzip-compressed JSON file."""
        filepath = Path(filepath)
        json_bytes = json.dumps(self.to_dict(), separators=(",", ":")).encode("utf-8")
        with gzip.open(filepath, "wb", compresslevel=9) as f:
            f.write(json_bytes)
        return filepath.stat().st_size

    @classmethod
    def from_gzip(cls, filepath: Union[str, Path]) -> "ReferenceFingerprints":
        """Load fingerprints from a gzip-compressed JSON file."""
        filepath = Path(filepath)
        with gzip.open(filepath, "rb") as f:
            json_bytes = f.read()
        return cls.from_dict(json.loads(json_bytes.decode("utf-8")))


def calculate_overlap(
    submission: str,
    fingerprints: ReferenceFingerprints,
    min_ngram_size: int = 5,
    max_ngram_size: int = 7,
) -> dict:
    """Calculate n-gram hash overlap between submission and reference.

    Args:
        submission: The text to check
        fingerprints: Reference fingerprints to compare against
        min_ngram_size: Minimum n-gram size
        max_ngram_size: Maximum n-gram size

    Returns:
        Dict with 'score' (0-1) and 'percentage' (0-100)
    """
    if not fingerprints.ngram_hashes:
        return {"score": 0.0, "percentage": 0.0}

    # Compute submission n-gram hashes
    words = get_words(submission)
    submission_hashes: Set[int] = set()
    for n in range(min_ngram_size, max_ngram_size + 1):
        if len(words) >= n:
            for ng in get_ngrams(words, n):
                submission_hashes.add(rolling_hash(ng))

    if not submission_hashes:
        return {"score": 0.0, "percentage": 0.0}

    # Calculate overlap
    ref_hashes = set(fingerprints.ngram_hashes)
    overlap = len(ref_hashes.intersection(submission_hashes))
    score_value = overlap / len(ref_hashes)

    return {
        "score": score_value,
        "percentage": round(score_value * 100, 2),
    }


def generate_fingerprints(
    reference: str,
    name: str,
    min_ngram_size: int = 5,
    max_ngram_size: int = 7,
    max_hashes: int = 2000,
) -> ReferenceFingerprints:
    """Generate fingerprints from a reference text.

    Args:
        reference: The raw reference text
        name: Name identifier (e.g., "page_one", "chapter_one")
        min_ngram_size: Minimum n-gram size
        max_ngram_size: Maximum n-gram size
        max_hashes: Maximum number of hashes to store. Default 2000 provides
            good coverage for typical chapter-length text (~5000 words) while
            keeping fingerprint files compact (<20KB compressed).

    Returns:
        ReferenceFingerprints object
    """
    words = get_words(reference)

    # N-gram hashes (deduplicated, all sizes combined)
    ngram_hash_set: Set[int] = set()
    for n in range(min_ngram_size, max_ngram_size + 1):
        if len(words) >= n:
            ngrams = get_ngrams(words, n)
            for ng in ngrams:
                ngram_hash_set.add(rolling_hash(ng))

    # Cap at max_hashes for bounded size. Sorting ensures deterministic
    # selection across runs. The specific hashes chosen don't affect accuracy
    # significantly since any sufficiently large subset provides good coverage.
    ngram_hashes = sorted(ngram_hash_set)[:max_hashes]

    return ReferenceFingerprints(
        name=name,
        ngram_hashes=ngram_hashes,
    )
