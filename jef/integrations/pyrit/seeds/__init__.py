"""PyRIT seed datasets for 0DIN n-day jailbreak probes.

Generated YAML files live in the ``data/`` subdirectory, separate from
code.  They are generated from the centralized
:data:`jef.integrations.NDAY_PROBES` registry.  To regenerate after
adding a new probe definition::

    python -m jef.integrations.pyrit.seeds

Each YAML file is loadable via ``pyrit.models.SeedDataset.from_yaml_file()``.
"""

from __future__ import annotations

import pathlib

SEEDS_DIR = pathlib.Path(__file__).parent / "data"
"""Absolute path to the directory containing seed YAML files."""
