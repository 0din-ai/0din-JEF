"""Shared JEF invocation logic for integration adapters.

Both garak and PyRIT adapters delegate to the helpers here so that
JEF call signatures, percentage normalisation, and metadata extraction
live in one place.

The :data:`NDAY_PROBES` registry is the **single source of truth** for
n-day probe definitions, loaded from ``config/nday_probes.yaml``.
Both garak probe classes and PyRIT seed YAML files are derived from
it — add a new entry to the config and both integrations pick it up
automatically (garak probes are generated dynamically; run
``python -m jef.integrations.pyrit.seeds`` to regenerate YAML files).

The registry is self-contained with no network dependencies, so it
works in air-gapped environments.
"""

from __future__ import annotations

import importlib
import pathlib
from dataclasses import dataclass, field
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Scorer registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SubstanceScorerDef:
    """Metadata for a substance / CBRN JEF scoring module."""

    module_path: str
    substance: str
    harm_category: str
    description: str
    tags: list[str] = field(
        default_factory=lambda: [
            "avid-effect:ethics:E0301",
            "avid-effect:security:S0403",
        ]
    )


SUBSTANCE_SCORERS: dict[str, SubstanceScorerDef] = {
    "meth": SubstanceScorerDef(
        module_path="jef.illicit_substances.meth",
        substance="methamphetamine",
        harm_category="illicit_substances",
        description="Scores text based on presence of crystal meth synthesis-related content",
    ),
    "nerve_agent": SubstanceScorerDef(
        module_path="jef.harmful_substances.nerve_agent",
        substance="nerve_agent",
        harm_category="harmful_substances",
        description="Scores text based on presence of nerve agent synthesis-related content",
    ),
    "fentanyl": SubstanceScorerDef(
        module_path="jef.illicit_substances.fentanyl",
        substance="fentanyl",
        harm_category="illicit_substances",
        description="Scores text based on presence of fentanyl synthesis-related content",
    ),
    "anthrax": SubstanceScorerDef(
        module_path="jef.harmful_substances.anthrax",
        substance="anthrax",
        harm_category="harmful_substances",
        description="Scores text based on presence of anthrax/B. anthracis-related content",
    ),
    "crispr": SubstanceScorerDef(
        module_path="jef.genetic_manipulation.crispr",
        substance="crispr",
        harm_category="genetic_manipulation",
        description="Scores text based on presence of CRISPR gene editing-related content",
    ),
}


# ---------------------------------------------------------------------------
# N-day probe registry  (loaded from config/nday_probes.yaml)
# ---------------------------------------------------------------------------

ODIN_DISCLOSURES_BASE_URL = "https://0din.ai/disclosures"
"""Base URL for 0DIN public disclosure pages."""

DEFAULT_NDAY_TAGS: list[str] = [
    "avid-effect:security:S0403",
    "avid-effect:ethics:E0301",
    "owasp:llm01",
    "quality:Security:PromptStability",
]
"""Default garak/AVID tags applied to all n-day probes."""

_CONFIG_DIR = pathlib.Path(__file__).parent / "config"


@dataclass(frozen=True)
class NdayProbeDef:
    """Definition for a disclosed jailbreak technique (n-day probe).

    Loaded from ``config/nday_probes.yaml``.  Self-contained — no
    network dependencies, works in air-gapped environments.
    """

    guid: str
    """0DIN case GUID (UUID)."""

    description: str
    """Human-readable summary of the technique."""

    goal: str
    """Short goal statement (used by garak)."""

    authors: list[str]
    """Credited researchers."""

    harm_categories: list[str]
    """PyRIT harm category labels."""

    prompts: list[str]
    """Attack prompt variants."""

    recommended_detector: list[str]
    """Garak detector name(s) to pair with this probe."""

    @property
    def disclosure_url(self) -> str:
        return f"{ODIN_DISCLOSURES_BASE_URL}/{self.guid}"


def snake_to_pascal(name: str) -> str:
    """Convert a snake_case registry key to PascalCase class name."""
    return "".join(word.capitalize() for word in name.split("_"))


def _load_nday_probes() -> dict[str, NdayProbeDef]:
    """Load n-day probe definitions from the YAML config file."""
    config_path = _CONFIG_DIR / "nday_probes.yaml"
    with open(config_path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    probes: dict[str, NdayProbeDef] = {}
    for name, entry in raw.items():
        probes[name] = NdayProbeDef(
            guid=entry["guid"],
            description=entry["description"],
            goal=entry["goal"],
            authors=entry["authors"],
            harm_categories=entry["harm_categories"],
            prompts=[p.rstrip("\n") for p in entry["prompts"]],
            recommended_detector=entry["recommended_detector"],
        )
    return probes


NDAY_PROBES: dict[str, NdayProbeDef] = _load_nday_probes()


# ---------------------------------------------------------------------------
# JEF invocation helpers
# ---------------------------------------------------------------------------


@dataclass
class JEFResult:
    """Normalized result from a JEF scoring call.

    Attributes:
        value: Score in 0.0-1.0 range (percentage / 100).
        percentage: Original JEF percentage (0-100).
        raw_score: Raw score from JEF (int or float).
        metadata: Dict of additional fields for downstream consumption.
    """

    value: float
    percentage: float
    raw_score: float | int
    metadata: dict[str, Any]


def get_score_func(module_path: str):
    """Lazily import a JEF module and return its ``score`` function."""
    mod = importlib.import_module(module_path)
    return mod.score


def score_substance(
    module_path: str, text: str, *, show_matches: bool = True
) -> JEFResult:
    """Invoke a substance/CBRN JEF scorer and return a normalized result.

    Args:
        module_path: Dotted module path (e.g. ``"jef.illicit_substances.meth"``).
        text: The text to score.
        show_matches: Whether to request matched components from JEF.

    Returns:
        :class:`JEFResult` with normalized value and metadata.
    """
    score_func = get_score_func(module_path)
    jef_result = score_func(recipe_text=text, show_matches=show_matches)

    metadata: dict[str, Any] = {
        "jef_score": jef_result["score"],
        "jef_percentage": jef_result["percentage"],
    }

    if "total_possible_score" in jef_result:
        metadata["total_possible_score"] = jef_result["total_possible_score"]

    if show_matches and jef_result.get("matches"):
        metadata["matches"] = jef_result["matches"]

    if jef_result.get("missing"):
        metadata["missing"] = jef_result["missing"]

    return JEFResult(
        value=jef_result["percentage"] / 100.0,
        percentage=jef_result["percentage"],
        raw_score=jef_result["score"],
        metadata=metadata,
    )


def score_copyright(
    text: str,
    *,
    ref: str = "chapter_one",
    min_ngram_size: int = 5,
    max_ngram_size: int = 7,
) -> JEFResult:
    """Invoke the JEF copyright scorer and return a normalized result.

    Loads fingerprints on first call via the references module side-effect.

    Args:
        text: The text to score.
        ref: Built-in reference name (e.g. ``"page_one"``, ``"chapter_one"``).
        min_ngram_size: Minimum n-gram size for fingerprint overlap.
        max_ngram_size: Maximum n-gram size for fingerprint overlap.

    Returns:
        :class:`JEFResult` with normalized value and metadata.
    """
    from jef.copyrights.harry_potter import score as hp_score

    # Side-effect import: registers built-in fingerprints on first call.
    # Subsequent calls are a no-op (Python caches the module).
    import jef.copyrights.harry_potter.references  # noqa: F401

    jef_result = hp_score(
        submission=text,
        ref=ref,
        min_ngram_size=min_ngram_size,
        max_ngram_size=max_ngram_size,
    )

    metadata: dict[str, Any] = {
        "jef_score": jef_result["score"],
        "jef_percentage": jef_result["percentage"],
    }

    if "last_analysis_scores" in jef_result:
        metadata["analysis_scores"] = jef_result["last_analysis_scores"]

    return JEFResult(
        value=jef_result["percentage"] / 100.0,
        percentage=jef_result["percentage"],
        raw_score=jef_result["score"],
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# PyRIT seed YAML generation
# ---------------------------------------------------------------------------


def nday_to_seed_dict(name: str, probe: NdayProbeDef) -> dict[str, Any]:
    """Convert a :class:`NdayProbeDef` to a PyRIT seed YAML-compatible dict.

    Args:
        name: Registry key (snake_case identifier).
        probe: The probe definition.

    The returned dict can be written to YAML and loaded by
    ``pyrit.models.SeedDataset.from_yaml_file()``.  Uses the PyRIT
    ``seeds:`` format where each seed carries its own metadata.
    """
    seeds = []
    for prompt in probe.prompts:
        seeds.append(
            {
                "value": prompt,
                "data_type": "text",
                "harm_categories": list(probe.harm_categories),
                "source": probe.disclosure_url,
                "authors": list(probe.authors),
                "groups": ["0din_nday"],
            }
        )
    return {
        "dataset_name": name,
        "description": probe.description,
        "seeds": seeds,
    }
