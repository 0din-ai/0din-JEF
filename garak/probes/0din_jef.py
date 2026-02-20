"""JEF n-day probes for garak.

Installed via ``pip install 0din-jef[garak]``.

This module re-exports probe classes from :mod:`jef.integrations.garak.probes`
into the ``garak.probes`` namespace so that garak's plugin loader can
discover them via ``importlib.import_module("garak.probes.0din_jef")``.

Probe classes are generated dynamically from the
:data:`jef.integrations.NDAY_PROBES` registry.

Usage::

    garak -p probes.0din_jef.PlaceholderInjection -d <detector>
"""

# Re-export all dynamically generated probe classes.
from jef.integrations.garak.probes import *  # noqa: F401, F403
from jef.integrations.garak.probes import __all__  # noqa: F401
