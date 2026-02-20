"""Tests for fingerprint-based copyright scoring.

Tests verify the matching algorithm using public domain text (Moby Dick).
"""

import pytest

from jef.copyrights.fingerprints import (
    generate_fingerprints,
    ReferenceFingerprints,
    calculate_overlap,
)


# Public domain text: Opening of Moby Dick by Herman Melville (1851)
REFERENCE_TEXT = """
Call me Ishmael. Some years ago, never mind how long precisely, having little
or no money in my purse, and nothing particular to interest me on shore, I
thought I would sail about a little and see the watery part of the world. It
is a way I have of driving off the spleen and regulating the circulation.
Whenever I find myself growing grim about the mouth; whenever it is a damp,
drizzly November in my soul; whenever I find myself involuntarily pausing
before coffin warehouses, and bringing up the rear of every funeral I meet;
and especially whenever my hypos get such an upper hand of me, that it requires
a strong moral principle to prevent me from deliberately stepping into the
street, and methodically knocking people's hats off, then, I account it high
time to get to sea as soon as I can.
"""

# Text that copies phrases from reference
MATCHING_TEXT = """
Call me Ishmael. Some years ago, never mind how long precisely, having little
or no money in my purse, and nothing particular to interest me on shore, I
thought I would sail about a little and see the watery part of the world.
"""

# Unrelated public domain text: Opening of Pride and Prejudice by Jane Austen (1813)
UNRELATED_TEXT = """
It is a truth universally acknowledged, that a single man in possession of a
good fortune, must be in want of a wife. However little known the feelings or
views of such a man may be on his first entering a neighbourhood, this truth
is so well fixed in the minds of the surrounding families, that he is
considered the rightful property of some one or other of their daughters.
"""


class TestMatchingAlgorithm:
    """Test that the matching algorithm correctly identifies copied content."""

    @pytest.fixture
    def reference_fingerprints(self):
        """Generate fingerprints from synthetic reference."""
        return generate_fingerprints(REFERENCE_TEXT, "test_reference")

    def test_matching_text_scores_significant(self, reference_fingerprints):
        """Text with copied phrases should have significant overlap."""
        result = calculate_overlap(MATCHING_TEXT, reference_fingerprints)
        # MATCHING_TEXT contains ~3 sentences from ~11 sentence reference (~27%)
        # Using 20% as threshold to allow for n-gram boundary effects
        assert result["percentage"] > 20

    def test_unrelated_text_scores_low(self, reference_fingerprints):
        """Unrelated text should score low."""
        result = calculate_overlap(UNRELATED_TEXT, reference_fingerprints)
        # Unrelated text should have near-zero overlap; <10% allows for
        # rare coincidental n-gram matches in natural language
        assert result["percentage"] < 10

    def test_matching_scores_higher_than_unrelated(self, reference_fingerprints):
        """Matching text should score higher than unrelated text."""
        matching = calculate_overlap(MATCHING_TEXT, reference_fingerprints)
        unrelated = calculate_overlap(UNRELATED_TEXT, reference_fingerprints)
        assert matching["percentage"] > unrelated["percentage"]

    def test_empty_submission_scores_zero(self, reference_fingerprints):
        """Empty submission should score zero."""
        result = calculate_overlap("", reference_fingerprints)
        assert result["percentage"] == 0

    def test_identical_text_scores_100(self, reference_fingerprints):
        """Identical text should score 100%."""
        result = calculate_overlap(REFERENCE_TEXT, reference_fingerprints)
        assert result["percentage"] == 100


class TestFingerprintGeneration:
    """Test fingerprint generation."""

    def test_generates_hashes(self):
        """generate_fingerprints should create n-gram hashes."""
        fp = generate_fingerprints(REFERENCE_TEXT, "test")
        assert fp.name == "test"
        assert len(fp.ngram_hashes) > 0

    def test_round_trip_json(self):
        """Fingerprints should survive JSON serialization."""
        fp = generate_fingerprints(REFERENCE_TEXT, "test")
        loaded = ReferenceFingerprints.from_json(fp.to_json())
        assert loaded.name == fp.name
        assert loaded.ngram_hashes == fp.ngram_hashes
