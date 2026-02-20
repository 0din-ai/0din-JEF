"""Garak detector integration for JEF scoring modules.

Provides garak-compatible detectors backed by JEF (Jailbreak Evaluation Framework)
scoring functions. Each detector inherits from ``garak.detectors.base.Detector``
and wraps a JEF scoring module, normalizing the result from JEF's 0-100
percentage scale to garak's 0.0-1.0 float scale.

Installation::

    pip install 0din-jef[garak]

Available detectors
~~~~~~~~~~~~~~~~~~~

==================================== ===================================
Detector                             JEF Scoring Module
==================================== ===================================
``CrystalMethScore``                 ``jef.illicit_substances.meth``
``NerveAgentScore``                  ``jef.harmful_substances.nerve_agent``
``FentanylScore``                    ``jef.illicit_substances.fentanyl``
``AnthraxScore``                     ``jef.harmful_substances.anthrax``
``CRISPRScore``                      ``jef.genetic_manipulation.crispr``
``CopyRightScoreHarryPotterPageOne`` ``jef.copyrights.harry_potter`` (page 1)
``CopyRightScoreHarryPotterChapterOne`` ``jef.copyrights.harry_potter`` (chapter 1)
==================================== ===================================

CLI usage
~~~~~~~~~

::

    garak --model_type openai --model_name gpt-4 \\
          -d 0din_jef.CrystalMethScore \\
          -p <probe>

Programmatic usage
~~~~~~~~~~~~~~~~~~

::

    from garak._plugins import load_plugin

    detector = load_plugin("detectors.0din_jef.CrystalMethScore")
    results = detector.detect(attempt)  # returns list[float] in 0.0-1.0

Notes
~~~~~

- Detectors are discovered via namespace packages. ``--list_detectors``
  may not show JEF detectors, but explicit ``-d 0din_jef.<Name>`` works.
"""

from __future__ import annotations

from garak.detectors.base import Detector
from garak import _config
import garak.attempt

from jef.integrations import (
    JEFResult,
    SubstanceScorerDef,
    SUBSTANCE_SCORERS,
    score_substance,
    score_copyright,
)


# ---------------------------------------------------------------------------
# Mixin: shared logic for all JEF-backed detectors
# ---------------------------------------------------------------------------


class JEFDetectorMixin:
    """Mixin providing shared functionality for JEF-based detectors.

    Provides:
    - Common ``display_name`` property with last-score display
    - ``_process_result`` helper that normalizes a :class:`JEFResult`
      and populates ``attempt.notes``

    Note on ``attempt.notes`` mutation: when ``detect()`` processes
    multiple outputs, ``details`` is extended cumulatively while
    ``score_percentage`` and ``missing`` reflect the *last* output
    processed.  This matches the upstream garak-0din-plugins behavior.
    """

    @property
    def display_name(self):
        """Return display name, appending last score if available."""
        if hasattr(self, "_last_score"):
            return f"{self._display_name} ({self._last_score:.2f}%)"
        return self._display_name

    def _process_result(self, result: JEFResult, attempt) -> float:
        """Populate *attempt.notes* from a :class:`JEFResult` and return 0-1 value."""
        self._last_score = result.percentage

        matches = result.metadata.get("matches")
        if matches:
            if "details" not in attempt.notes:
                attempt.notes["details"] = []
            attempt.notes["details"].extend(matches)

        missing = result.metadata.get("missing")
        if missing:
            attempt.notes["missing"] = missing

        attempt.notes["score_percentage"] = f"{result.percentage:.2f}%"
        return result.value


# ---------------------------------------------------------------------------
# Substance / CBRN detectors — share a common detect() via base class
# ---------------------------------------------------------------------------


class _SubstanceDetector(JEFDetectorMixin, Detector):
    """Base for detectors that call JEF with ``(recipe_text=..., show_matches=True)``.

    Subclasses set ``_scorer_key`` to select a definition from
    :data:`jef.integrations.SUBSTANCE_SCORERS`.
    """

    _scorer_key: str = ""

    @property
    def _def(self) -> "SubstanceScorerDef":
        return SUBSTANCE_SCORERS[self._scorer_key]

    def detect(self, attempt: garak.attempt.Attempt) -> list[float]:
        results: list[float] = []
        for output in attempt.all_outputs:
            if output is None or not output.text:
                continue
            result = score_substance(
                self._def.module_path, output.text, show_matches=True
            )
            results.append(self._process_result(result, attempt))
        return results if results else [0.0]


class CrystalMethScore(_SubstanceDetector):
    """Scores text for crystal meth synthesis content using JEF."""

    _scorer_key = "meth"
    description = SUBSTANCE_SCORERS["meth"].description
    tags = list(SUBSTANCE_SCORERS["meth"].tags)

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CrystalMethScore"


class NerveAgentScore(_SubstanceDetector):
    """Scores text for nerve agent synthesis content using JEF."""

    _scorer_key = "nerve_agent"
    description = SUBSTANCE_SCORERS["nerve_agent"].description
    tags = list(SUBSTANCE_SCORERS["nerve_agent"].tags)

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.NerveAgentScore"


class FentanylScore(_SubstanceDetector):
    """Scores text for fentanyl synthesis content using JEF.

    Detects precursors like 4-ANPP, NPP, propionyl chloride, and
    synthesis procedures.
    """

    _scorer_key = "fentanyl"
    description = SUBSTANCE_SCORERS["fentanyl"].description
    tags = list(SUBSTANCE_SCORERS["fentanyl"].tags)

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.FentanylScore"


class AnthraxScore(_SubstanceDetector):
    """Scores text for anthrax / B. anthracis content using JEF.

    Detects biological weapons content including spore formation, toxin
    components, and weaponisation indicators.
    """

    _scorer_key = "anthrax"
    description = SUBSTANCE_SCORERS["anthrax"].description
    tags = list(SUBSTANCE_SCORERS["anthrax"].tags)

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.AnthraxScore"


class CRISPRScore(_SubstanceDetector):
    """Scores text for CRISPR gene-editing content using JEF.

    Detects gene editing content including Cas9, guide RNA, PAM
    sequences, delivery methods, and HDR/NHEJ.
    """

    _scorer_key = "crispr"
    description = SUBSTANCE_SCORERS["crispr"].description
    tags = list(SUBSTANCE_SCORERS["crispr"].tags)

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CRISPRScore"


# ---------------------------------------------------------------------------
# Copyright detectors
# ---------------------------------------------------------------------------


class _CopyrightDetector(JEFDetectorMixin, Detector):
    """Base for copyright detectors that call JEF with fingerprint params.

    Subclasses set ``_ref`` to the reference fingerprint name
    (e.g. ``"page_one"`` or ``"chapter_one"``).
    """

    _ref: str = ""  # set by subclass

    def detect(self, attempt: garak.attempt.Attempt) -> list[float]:
        results: list[float] = []
        for output in attempt.all_outputs:
            if output is None:
                continue
            text = output.text
            if not text or not text.strip():
                results.append(0.0)
                continue
            result = score_copyright(text, ref=self._ref)
            results.append(self._process_result(result, attempt))
        return results if results else [0.0]


class CopyRightScoreHarryPotterPageOne(_CopyrightDetector):
    """Scores text for Harry Potter page-one copyright content using JEF.

    Uses pre-computed fingerprints (JEF v0.3.0+) instead of raw
    copyrighted text.
    """

    description = (
        "Scores text based on presence of Harry Potter content "
        "(chapter 1, page 1, <900 words)"
    )
    tags: list = []
    _ref = "page_one"

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CopyRightScoreHarryPotterPageOne"


class CopyRightScoreHarryPotterChapterOne(_CopyrightDetector):
    """Scores text for Harry Potter chapter-one copyright content using JEF.

    Uses pre-computed fingerprints (JEF v0.3.0+) instead of raw
    copyrighted text.
    """

    description = (
        "Scores text based on presence of Harry Potter content (chapter 1, <5k words)"
    )
    tags: list = []
    _ref = "chapter_one"

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CopyRightScoreHarryPotterChapterOne"
