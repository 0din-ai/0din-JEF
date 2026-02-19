"""Regenerate PyRIT seed YAML files from the NDAY_PROBES registry.

Usage::

    python -m jef.integrations.pyrit.seeds

Writes one YAML file per n-day probe definition into the ``data/``
directory alongside this module.  Existing files are overwritten.
"""

from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

from jef.integrations import NDAY_PROBES, nday_to_seed_dict


class _SeedDumper(yaml.Dumper):
    """Custom Dumper that uses literal block style for multiline strings."""

    pass


def _str_representer(dumper: yaml.Dumper, data: str) -> yaml.Node:
    """Use literal block style for multiline strings, plain style otherwise."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_SeedDumper.add_representer(str, _str_representer)


def main() -> None:
    seeds_dir = pathlib.Path(__file__).parent / "data"
    seeds_dir.mkdir(exist_ok=True)

    header = (
        "# AUTO-GENERATED — do not edit by hand.\n"
        "# Regenerate: python -m jef.integrations.pyrit.seeds\n"
        "# Source: jef/integrations/config/nday_probes.yaml\n\n"
    )

    written = 0
    for name, defn in NDAY_PROBES.items():
        seed_dict = nday_to_seed_dict(name, defn)
        path = seeds_dir / f"{name}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            yaml.dump(
                seed_dict,
                f,
                Dumper=_SeedDumper,
                default_flow_style=False,
                sort_keys=False,
            )
        written += 1
        print(f"  wrote {path.name}")

    print(f"\nGenerated {written} seed YAML files in {seeds_dir}")


if __name__ == "__main__":
    main()
