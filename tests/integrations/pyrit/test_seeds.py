"""Tests for JEF PyRIT seed dataset integration (n-day probes).

Validates that all seed YAML files load correctly, have the expected
attributes, and stay in sync with the centralised NDAY_PROBES registry.

Does NOT require PyRIT to be installed — parses YAML directly and
optionally validates with PyRIT's SeedDataset if available.
"""

from __future__ import annotations

import pytest

try:
    import yaml
except ImportError:
    yaml = None

from jef.integrations import NDAY_PROBES
from jef.integrations.pyrit.seeds import SEEDS_DIR

# Derive expected file list from registry — no hardcoded list to maintain
SEED_FILES = [f"{name}.yaml" for name in NDAY_PROBES]


def _load_yaml(filename: str) -> dict:
    """Load a YAML seed file and return parsed dict."""
    path = SEEDS_DIR / filename
    assert path.exists(), f"Seed file not found: {path}"
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Seed files exist
# ---------------------------------------------------------------------------


class TestSeedFilesExist:
    """All expected seed YAML files exist in the seeds/data directory."""

    def test_seeds_directory_exists(self):
        assert SEEDS_DIR.is_dir(), f"Seeds directory not found: {SEEDS_DIR}"

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_seed_file_exists(self, filename):
        path = SEEDS_DIR / filename
        assert path.exists(), f"Missing seed file: {path}"

    def test_no_extra_yaml_files(self):
        """No stale YAML files exist beyond what the registry defines."""
        expected = set(SEED_FILES)
        actual = {p.name for p in SEEDS_DIR.glob("*.yaml")}
        extra = actual - expected
        assert not extra, f"Unexpected YAML files not in NDAY_PROBES registry: {extra}"


# ---------------------------------------------------------------------------
# YAML structure validation
# ---------------------------------------------------------------------------


@pytest.mark.skipif(yaml is None, reason="PyYAML not installed")
class TestSeedYAMLStructure:
    """Each seed YAML file uses the PyRIT ``seeds:`` format."""

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_has_dataset_name(self, filename):
        data = _load_yaml(filename)
        assert "dataset_name" in data
        assert isinstance(data["dataset_name"], str)
        assert len(data["dataset_name"]) > 0

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_has_description(self, filename):
        data = _load_yaml(filename)
        assert "description" in data
        assert isinstance(data["description"], str)
        assert len(data["description"]) > 0

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_has_seeds(self, filename):
        data = _load_yaml(filename)
        assert "seeds" in data
        assert isinstance(data["seeds"], list)
        assert len(data["seeds"]) >= 1

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_seeds_have_required_fields(self, filename):
        data = _load_yaml(filename)
        seed_name = filename.replace(".yaml", "")
        defn = NDAY_PROBES[seed_name]
        for i, seed in enumerate(data["seeds"]):
            assert "value" in seed, f"Seed {i} missing 'value' in {filename}"
            assert "data_type" in seed, f"Seed {i} missing 'data_type' in {filename}"
            assert seed["data_type"] == "text"
            assert isinstance(seed["value"], str)
            assert len(seed["value"].strip()) > 0
            assert seed["harm_categories"] == list(defn.harm_categories)
            assert seed["source"] == defn.disclosure_url
            assert seed["authors"] == list(defn.authors)
            assert "0din_nday" in seed["groups"]


# ---------------------------------------------------------------------------
# Registry sync — YAML files match the NDAY_PROBES source of truth
# ---------------------------------------------------------------------------


@pytest.mark.skipif(yaml is None, reason="PyYAML not installed")
class TestRegistrySync:
    """YAML files are consistent with the NDAY_PROBES registry."""

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_dataset_name_matches_registry_key(self, filename):
        """The seed 'dataset_name' field matches the registry key."""
        data = _load_yaml(filename)
        seed_name = filename.replace(".yaml", "")
        assert data["dataset_name"] == seed_name

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_seed_count_matches_registry(self, filename):
        data = _load_yaml(filename)
        seed_name = filename.replace(".yaml", "")
        defn = NDAY_PROBES[seed_name]
        assert len(data["seeds"]) == len(defn.prompts)

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_source_url_contains_guid(self, filename):
        """Each seed's source URL contains the probe's GUID."""
        data = _load_yaml(filename)
        seed_name = filename.replace(".yaml", "")
        defn = NDAY_PROBES[seed_name]
        for seed in data["seeds"]:
            assert defn.guid in seed["source"]

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_harm_categories_match_registry(self, filename):
        data = _load_yaml(filename)
        seed_name = filename.replace(".yaml", "")
        defn = NDAY_PROBES[seed_name]
        for seed in data["seeds"]:
            assert seed["harm_categories"] == list(defn.harm_categories)


# ---------------------------------------------------------------------------
# PyRIT SeedDataset loading (optional — only if pyrit is installed)
# ---------------------------------------------------------------------------


try:
    import pyrit  # noqa: F401

    _has_pyrit = True
except ImportError:
    _has_pyrit = False


@pytest.mark.skipif(not _has_pyrit, reason="pyrit not installed")
class TestPyRITSeedDatasetLoading:
    """Seed YAML files load via PyRIT's SeedDataset.from_yaml_file()."""

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_loads_via_seed_dataset(self, filename):
        from pyrit.models import SeedDataset

        path = SEEDS_DIR / filename
        dataset = SeedDataset.from_yaml_file(path)
        assert dataset is not None
        assert len(dataset.seeds) >= 1

    @pytest.mark.parametrize("filename", SEED_FILES)
    def test_seed_values_are_nonempty(self, filename):
        from pyrit.models import SeedDataset

        path = SEEDS_DIR / filename
        dataset = SeedDataset.from_yaml_file(path)
        for seed in dataset.seeds:
            assert seed.value is not None
            assert len(seed.value.strip()) > 0
