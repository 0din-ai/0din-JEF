"""Shared JEF invocation logic for integration adapters.

Both garak and PyRIT adapters delegate to the helpers here so that
JEF call signatures, percentage normalisation, and metadata extraction
live in one place.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any


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
# JEF invocation helpers
# ---------------------------------------------------------------------------


@dataclass
class JEFResult:
    """Normalised result from a JEF scoring call.

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
    """Invoke a substance/CBRN JEF scorer and return a normalised result.

    Args:
        module_path: Dotted module path (e.g. ``"jef.illicit_substances.meth"``).
        text: The text to score.
        show_matches: Whether to request matched components from JEF.

    Returns:
        :class:`JEFResult` with normalised value and metadata.
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
    """Invoke the JEF copyright scorer and return a normalised result.

    Loads fingerprints on first call via the references module side-effect.

    Args:
        text: The text to score.
        ref: Built-in reference name (e.g. ``"page_one"``, ``"chapter_one"``).
        min_ngram_size: Minimum n-gram size for fingerprint overlap.
        max_ngram_size: Maximum n-gram size for fingerprint overlap.

    Returns:
        :class:`JEFResult` with normalised value and metadata.
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
