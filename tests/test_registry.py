"""Tests for the scoring types registry."""

import pytest

from jef import registry


class TestRegistry:
    """Tests for registry module functions."""

    def test_version_returns_jef_version(self):
        """version() should return the JEF library version."""
        import jef

        assert registry.version() == jef.__version__

    def test_list_all_returns_all_scoring_types(self):
        """list_all() should return all scoring types including deprecated."""
        types = registry.list_all()

        # Should return a list of dicts
        assert isinstance(types, list)
        assert len(types) > 0

        # Each entry should have required fields
        for scoring_type in types:
            assert "name" in scoring_type
            assert "category" in scoring_type
            assert "display_name" in scoring_type
            assert "pass_threshold" in scoring_type
            assert "deprecated" in scoring_type

    def test_list_all_includes_known_types(self):
        """list_all() should include our known scoring types."""
        types = registry.list_all()
        names = [t["name"] for t in types]

        # These are the types with METADATA we've added
        assert "illicit_substances" in names
        assert "fentanyl" in names
        assert "harry_potter" in names
        assert "harmful_substances" in names
        assert "cbrm" in names
        assert "genetic_manipulation" in names
        assert "chinese_censorship" in names

    def test_list_active_excludes_deprecated(self):
        """list_active() should exclude deprecated scoring types."""
        active_types = registry.list_active()
        deprecated_names = [t["name"] for t in active_types if t.get("deprecated")]

        assert len(deprecated_names) == 0

    def test_list_active_includes_non_deprecated(self):
        """list_active() should include non-deprecated types."""
        active_types = registry.list_active()
        names = [t["name"] for t in active_types]

        # These should be active
        assert "illicit_substances" in names
        assert "harry_potter" in names

    def test_get_returns_metadata_for_known_type(self):
        """get() should return metadata for a known scoring type."""
        metadata = registry.get("illicit_substances")

        assert metadata is not None
        assert metadata["name"] == "illicit_substances"
        assert metadata["category"] == "illicit_substances"
        assert metadata["pass_threshold"] == 70

    def test_get_returns_none_for_unknown_type(self):
        """get() should return None for an unknown scoring type."""
        metadata = registry.get("nonexistent_type")

        assert metadata is None

    def test_harry_potter_has_options_schema(self):
        """harry_potter should have an options_schema for reference selection."""
        metadata = registry.get("harry_potter")

        assert metadata is not None
        assert metadata["requires_reference"] is True
        assert metadata["options_schema"] is not None
        assert "properties" in metadata["options_schema"]
        assert "ref" in metadata["options_schema"]["properties"]

    def test_chinese_censorship_is_deprecated(self):
        """chinese_censorship should be marked as deprecated."""
        metadata = registry.get("chinese_censorship")

        assert metadata is not None
        assert metadata["deprecated"] is True

    def test_score_delegates_to_module(self):
        """score() should delegate to the appropriate module's score function."""
        # Test with a simple case - harmful_substances (nerve_agent)
        result = registry.score("harmful_substances", "This is a test text")

        # Should return a score result
        assert result is not None
        assert "score" in result or hasattr(result, "score")

    def test_score_raises_for_unknown_type(self):
        """score() should raise ValueError for unknown scoring type."""
        with pytest.raises(ValueError, match="Unknown scoring type"):
            registry.score("nonexistent_type", "test text")

    def test_score_with_reference_type(self):
        """score() should handle reference-based scoring types."""
        # harry_potter.score() takes 'reference' parameter for the text to compare against
        result = registry.score(
            "harry_potter",
            "Mr. and Mrs. Dursley of number four, Privet Drive",
            reference="The boy who lived had come at last.",
        )

        assert result is not None
