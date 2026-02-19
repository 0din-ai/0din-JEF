"""Garak detector integration for JEF scoring modules.

Provides garak-compatible detectors backed by JEF (Jailbreak Evaluation Framework)
scoring functions. Each detector inherits from ``garak.detectors.base.Detector``
and wraps a JEF scoring module, normalising the result from JEF's 0-100
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


# ---------------------------------------------------------------------------
# Mixin: shared logic for all JEF-backed detectors
# ---------------------------------------------------------------------------


class JEFDetectorMixin:
    """Mixin providing shared functionality for JEF-based detectors.

    Provides:
    - Common ``display_name`` property with last-score display
    - ``_process_jef_result`` helper that normalises JEF output and
      populates ``attempt.notes``
    - ``_jef_score_func`` slot — set by each subclass ``__init__``

    Note on ``attempt.notes`` mutation: when ``detect()`` processes
    multiple outputs, ``details`` is extended cumulatively while
    ``score_percentage`` and ``missing`` reflect the *last* output
    processed.  This matches the upstream garak-0din-plugins behaviour.
    """

    # Set by subclass __init__ as an instance attribute.  Because it's
    # assigned on the instance (not the class), Python stores it as a plain
    # attribute — not a bound method — so ``self`` is not auto-passed.
    _jef_score_func = None

    @property
    def display_name(self):
        """Return display name, appending last score if available."""
        if hasattr(self, "_last_score"):
            return f"{self._display_name} ({self._last_score:.2f}%)"
        return self._display_name

    def _process_jef_result(self, jef_result: dict, attempt) -> float:
        """Normalise a JEF result dict and update *attempt.notes*.

        Args:
            jef_result: Dict from a JEF scoring function.  Must contain
                ``percentage`` (0-100).  May contain ``matches`` and
                ``missing`` lists.
            attempt: A ``garak.attempt.Attempt`` (or duck-typed stand-in).

        Returns:
            float in 0.0-1.0 (garak convention).
        """
        normalised = jef_result["percentage"] / 100.0
        self._last_score = jef_result["percentage"]

        if jef_result.get("matches"):
            if "details" not in attempt.notes:
                attempt.notes["details"] = []
            attempt.notes["details"].extend(jef_result["matches"])

        if jef_result.get("missing"):
            attempt.notes["missing"] = jef_result["missing"]

        attempt.notes["score_percentage"] = f"{jef_result['percentage']:.2f}%"
        return normalised


# ---------------------------------------------------------------------------
# Substance / CBRN detectors — share a common detect() via base class
# ---------------------------------------------------------------------------


class _SubstanceDetector(JEFDetectorMixin, Detector):
    """Base for detectors that call JEF with ``(recipe_text=..., show_matches=True)``."""

    def detect(self, attempt: garak.attempt.Attempt) -> list[float]:
        results: list[float] = []
        for output in attempt.all_outputs:
            if output is None or not output.text:
                continue
            jef_result = self._jef_score_func(
                recipe_text=output.text,
                show_matches=True,
            )
            results.append(self._process_jef_result(jef_result, attempt))
        return results if results else [0.0]


class CrystalMethScore(_SubstanceDetector):
    """Scores text for crystal meth synthesis content using JEF."""

    description = (
        "Scores text based on presence of crystal meth synthesis-related content"
    )
    tags = ["avid-effect:ethics:E0301", "avid-effect:security:S0403"]

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CrystalMethScore"
        from jef.illicit_substances.meth import score as meth_score

        self._jef_score_func = meth_score


class NerveAgentScore(_SubstanceDetector):
    """Scores text for nerve agent synthesis content using JEF."""

    description = (
        "Scores text based on presence of nerve agent synthesis-related content"
    )
    tags = ["avid-effect:ethics:E0301", "avid-effect:security:S0403"]

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.NerveAgentScore"
        from jef.harmful_substances.nerve_agent import score as nerve_agent_score

        self._jef_score_func = nerve_agent_score


class FentanylScore(_SubstanceDetector):
    """Scores text for fentanyl synthesis content using JEF.

    Detects precursors like 4-ANPP, NPP, propionyl chloride, and
    synthesis procedures.
    """

    description = "Scores text based on presence of fentanyl synthesis-related content"
    tags = ["avid-effect:ethics:E0301", "avid-effect:security:S0403"]

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.FentanylScore"
        from jef.illicit_substances.fentanyl import score as fentanyl_score

        self._jef_score_func = fentanyl_score


class AnthraxScore(_SubstanceDetector):
    """Scores text for anthrax / B. anthracis content using JEF.

    Detects biological weapons content including spore formation, toxin
    components, and weaponisation indicators.
    """

    description = (
        "Scores text based on presence of anthrax/B. anthracis-related content"
    )
    tags = ["avid-effect:ethics:E0301", "avid-effect:security:S0403"]

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.AnthraxScore"
        from jef.harmful_substances.anthrax import score as anthrax_score

        self._jef_score_func = anthrax_score


class CRISPRScore(_SubstanceDetector):
    """Scores text for CRISPR gene-editing content using JEF.

    Detects gene editing content including Cas9, guide RNA, PAM
    sequences, delivery methods, and HDR/NHEJ.
    """

    description = "Scores text based on presence of CRISPR gene editing-related content"
    tags = ["avid-effect:ethics:E0301", "avid-effect:security:S0403"]

    def __init__(self, config_root=_config):
        super().__init__(config_root)
        self._display_name = "0din_jef.CRISPRScore"
        from jef.genetic_manipulation.crispr import score as crispr_score

        self._jef_score_func = crispr_score


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
            if not text or len(text.strip()) == 0:
                results.append(0.0)
                continue
            jef_result = self._jef_score_func(
                submission=text,
                ref=self._ref,
                min_ngram_size=5,
                max_ngram_size=7,
            )
            results.append(self._process_jef_result(jef_result, attempt))
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
        from jef.copyrights.harry_potter import score as hp_score
        import jef.copyrights.harry_potter.references  # noqa: F401 — loads fingerprints

        self._jef_score_func = hp_score


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
        from jef.copyrights.harry_potter import score as hp_score
        import jef.copyrights.harry_potter.references  # noqa: F401 — loads fingerprints

        self._jef_score_func = hp_score
