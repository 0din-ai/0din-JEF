"""JEF-backed detectors for garak.

Installed via ``pip install 0din-jef[garak]``.

This module re-exports detector classes from :mod:`jef.integrations.garak.detectors`
into the ``garak.detectors`` namespace so that garak's plugin loader can
discover them via ``importlib.import_module("garak.detectors.0din_jef")``.

Usage::

    garak -d detectors.0din_jef.CrystalMethScore -p <probe>
"""

from jef.integrations.garak.detectors import (  # noqa: F401
    JEFDetectorMixin,
    CrystalMethScore,
    NerveAgentScore,
    FentanylScore,
    AnthraxScore,
    CRISPRScore,
    CopyRightScoreHarryPotterPageOne,
    CopyRightScoreHarryPotterChapterOne,
)
