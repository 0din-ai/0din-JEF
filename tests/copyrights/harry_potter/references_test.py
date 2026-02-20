"""Tests for Harry Potter reference fingerprints.

Only tests that the built-in HP fingerprints load correctly.
Algorithm tests are in tests/copyrights/fingerprints_test.py
"""

import pytest

from jef.copyrights.harry_potter import score, list_references, get_reference


class TestBuiltinReferences:
    """Test that Harry Potter fingerprints load correctly."""

    def test_references_are_loaded(self):
        """Built-in references should be available."""
        refs = list_references()
        assert "page_one" in refs
        assert "chapter_one" in refs

    def test_fingerprints_have_hashes(self):
        """Loaded fingerprints should contain n-gram hashes."""
        fp = get_reference("page_one")
        assert fp is not None
        assert len(fp.ngram_hashes) > 0

    def test_default_ref_works(self):
        """Default ref (chapter_one) should work."""
        # Just verify it doesn't raise
        result = score("some random text here")
        assert "score" in result


class TestScoreAPI:
    """Test score() API behavior."""

    def test_returns_score_and_percentage(self):
        """score() should return score and percentage."""
        result = score("some test text here", ref="page_one")
        assert "score" in result
        assert "percentage" in result
        assert 0 <= result["score"] <= 1
        assert 0 <= result["percentage"] <= 100

    def test_invalid_ref_raises(self):
        """score() should raise error for unknown reference."""
        with pytest.raises(ValueError):
            score("test", ref="nonexistent")
