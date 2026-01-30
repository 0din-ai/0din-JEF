"""
Registry for JEF scoring types.

Provides auto-discovery of all scoring modules with METADATA.
"""

from importlib import import_module
from typing import Any

import jef

# Modules to scan for METADATA (category/variant paths)
_SCORING_MODULES = [
    "jef.illicit_substances.meth",
    "jef.illicit_substances.fentanyl",
    "jef.copyrights.harry_potter",
    "jef.harmful_substances.nerve_agent",
    "jef.harmful_substances.anthrax",
    "jef.genetic_manipulation.crispr",
    "jef.chinese_censorship.tiananmen",
]

# Cache for discovered types
_registry_cache: dict[str, dict[str, Any]] | None = None
_module_cache: dict[str, Any] = {}


def _discover_types() -> dict[str, dict[str, Any]]:
    """Discover all scoring types with METADATA."""
    global _registry_cache

    if _registry_cache is not None:
        return _registry_cache

    types: dict[str, dict[str, Any]] = {}

    for module_path in _SCORING_MODULES:
        try:
            module = import_module(module_path)
            if hasattr(module, "METADATA"):
                metadata = module.METADATA
                name = metadata["name"]
                types[name] = metadata
                _module_cache[name] = module
        except ImportError:
            # Skip modules that can't be imported
            continue

    _registry_cache = types
    return types


def version() -> str:
    """Return the JEF library version."""
    return jef.__version__


def list_all() -> list[dict[str, Any]]:
    """Return all scoring types including deprecated ones."""
    types = _discover_types()
    return list(types.values())


def list_active() -> list[dict[str, Any]]:
    """Return only non-deprecated scoring types."""
    types = _discover_types()
    return [t for t in types.values() if not t.get("deprecated", False)]


def get(name: str) -> dict[str, Any] | None:
    """Get metadata for a specific scoring type by name."""
    types = _discover_types()
    return types.get(name)


def get_module(name: str) -> Any | None:
    """Get the actual module for a scoring type by name."""
    _discover_types()  # Ensure modules are loaded
    return _module_cache.get(name)


def score(name: str, text: str, **kwargs) -> Any:
    """
    Score text using the specified scoring type.

    Args:
        name: The scoring type name (e.g., "illicit_substances")
        text: The text to score
        **kwargs: Additional arguments passed to the score function

    Returns:
        The scoring result from the module

    Raises:
        ValueError: If the scoring type is unknown
    """
    module = get_module(name)
    if module is None:
        raise ValueError(f"Unknown scoring type: {name}")

    return module.score(text, **kwargs)
