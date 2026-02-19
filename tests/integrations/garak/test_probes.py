"""Tests for JEF garak probe integration (n-day probes).

Uses real garak (load_plugin, Probe) -- no mocks.
Requires: ``pip install 0din-jef[garak]``

Skipped automatically when garak is not installed.
"""

import importlib
import inspect

import pytest

garak = pytest.importorskip("garak", reason="garak not installed")

from garak._plugins import load_plugin  # noqa: E402

from jef.integrations import NDAY_PROBES, _snake_to_pascal  # noqa: E402

# Derive probe names and GUIDs from the registry — no hardcoded lists
PROBE_NAMES = [_snake_to_pascal(key) for key in NDAY_PROBES]
DISCLOSURE_GUIDS = {
    _snake_to_pascal(key): defn.guid for key, defn in NDAY_PROBES.items()
}


def _load_probe(name: str):
    """Load a probe via garak's plugin loader."""
    return load_plugin(f"probes.0din_jef.{name}")


# ---------------------------------------------------------------------------
# Namespace bridge — garak.probes.0din_jef re-exports match source module
# ---------------------------------------------------------------------------


class TestNamespaceBridge:
    """The bridge module re-exports the same classes as the source."""

    def test_bridge_has_all_probes(self):
        """Every probe in __all__ is re-exported by the bridge."""
        bridge = importlib.import_module("garak.probes.0din_jef")
        import jef.integrations.garak.probes as source

        assert source.__all__, "source module has empty __all__"

        for name in source.__all__:
            assert hasattr(bridge, name), (
                f"{name} defined in jef.integrations.garak.probes "
                f"but missing from garak.probes.0din_jef bridge"
            )

    def test_probe_count_matches_registry(self):
        """Number of probe classes matches NDAY_PROBES registry entries."""
        import jef.integrations.garak.probes as source

        assert len(source.__all__) == len(NDAY_PROBES)


# ---------------------------------------------------------------------------
# Probe loading — all probes load via garak load_plugin
# ---------------------------------------------------------------------------


class TestProbeLoading:
    """All probes should load successfully via garak's plugin system."""

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_probe_loads(self, name):
        probe = _load_probe(name)
        assert probe is not None


# ---------------------------------------------------------------------------
# Probe attributes — required fields are populated correctly
# ---------------------------------------------------------------------------


class TestProbeAttributes:
    """Each probe has the expected attributes."""

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_has_prompts(self, name):
        """Each probe has at least one prompt string."""
        probe = _load_probe(name)
        assert hasattr(probe, "prompts")
        assert len(probe.prompts) >= 1
        for p in probe.prompts:
            assert isinstance(p, str)
            assert len(p.strip()) > 0

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_has_uri(self, name):
        """Each probe references its 0DIN disclosure URI."""
        probe = _load_probe(name)
        assert hasattr(probe, "uri")
        assert DISCLOSURE_GUIDS[name] in probe.uri

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_has_tags(self, name):
        """Each probe has at least one tag."""
        probe = _load_probe(name)
        assert hasattr(probe, "tags")
        assert len(probe.tags) >= 1

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_has_goal(self, name):
        """Each probe has a goal description."""
        probe = _load_probe(name)
        assert hasattr(probe, "goal")
        assert len(probe.goal) > 0

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_has_recommended_detector(self, name):
        """Each probe recommends at least one detector."""
        probe = _load_probe(name)
        assert hasattr(probe, "recommended_detector")
        assert len(probe.recommended_detector) >= 1
        for d in probe.recommended_detector:
            assert d.startswith("0din_jef.")

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_bcp47_is_english(self, name):
        """All n-day probes are English-language."""
        probe = _load_probe(name)
        assert probe.bcp47 == "en"

    @pytest.mark.parametrize("name", PROBE_NAMES)
    def test_prompt_count_matches_registry(self, name):
        """Prompt count matches the registry definition."""
        probe = _load_probe(name)
        # Find the registry entry for this class name
        defn = next(
            d for key, d in NDAY_PROBES.items() if _snake_to_pascal(key) == name
        )
        assert len(probe.prompts) == len(defn.prompts)
