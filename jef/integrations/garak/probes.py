"""Garak probe integration for 0DIN n-day jailbreak techniques.

Provides garak-compatible probes for disclosed jailbreak vulnerabilities
(n-days) from the 0DIN bug-bounty programme.  Each probe is a static
``garak.probes.base.Probe`` subclass whose metadata is loaded from
``config/nday_probes.yaml``.

Probe classes are **generated dynamically** from the centralised
:data:`jef.integrations.NDAY_PROBES` registry.  To add a new n-day,
add an entry to the YAML config — a garak probe class is created
automatically.

Installation::

    pip install 0din-jef[garak]

CLI usage
~~~~~~~~~

::

    garak --model_type openai --model_name gpt-4 \\
          -p probes.0din_jef.PlaceholderInjection \\
          -d 0din_jef.CrystalMethScore

Programmatic usage
~~~~~~~~~~~~~~~~~~

::

    from garak._plugins import load_plugin

    probe = load_plugin("probes.0din_jef.PlaceholderInjection")
    print(probe.prompts)

Notes
~~~~~

- These probes implement *attack techniques*, not scoring.  Pair them
  with JEF detectors (``detectors.0din_jef.*``) to measure success.
- Probes are discovered via namespace packages.
- Each probe references its 0DIN case GUID in ``uri`` for traceability.
"""

from __future__ import annotations

from garak.probes.base import Probe
from garak import _config

from jef.integrations import (
    NDAY_PROBES,
    DEFAULT_NDAY_TAGS,
    NdayProbeDef,
    _snake_to_pascal,
)


def _make_probe_class(name: str, defn: NdayProbeDef) -> type:
    """Dynamically create a garak Probe subclass from an :class:`NdayProbeDef`."""
    class_name = _snake_to_pascal(name)

    def __init__(self, config_root=_config):
        super(cls, self).__init__(config_root)

    cls = type(
        class_name,
        (Probe,),
        {
            "__module__": __name__,
            "__qualname__": class_name,
            "__doc__": f"{defn.description}\n\n0DIN case: {defn.guid}",
            "__init__": __init__,
            "bcp47": "en",
            "uri": defn.disclosure_url,
            "doc_uri": defn.disclosure_url,
            "recommended_detector": list(defn.recommended_detector),
            "tags": tuple(DEFAULT_NDAY_TAGS),
            "goal": defn.goal,
            "prompts": list(defn.prompts),
        },
    )
    return cls


# ---------------------------------------------------------------------------
# Generate and register all probe classes from the NDAY_PROBES registry
# ---------------------------------------------------------------------------


def _build_probes() -> dict[str, type]:
    """Build all probe classes and return {class_name: cls} mapping."""
    classes = {}
    for name, defn in NDAY_PROBES.items():
        cls = _make_probe_class(name, defn)
        classes[_snake_to_pascal(name)] = cls
    return classes


_PROBE_CLASSES = _build_probes()

# Inject into module namespace so ``from jef.integrations.garak.probes import X`` works
globals().update(_PROBE_CLASSES)

# Explicit __all__ for star-imports and introspection
__all__ = list(_PROBE_CLASSES.keys())
