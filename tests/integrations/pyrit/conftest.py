"""Fixtures for PyRIT scorer integration tests.

Provides an in-memory SQLite database backend so PyRIT's ``score_text_async``
can persist scores without requiring a real database or environment config.

.. note::

    The ``sqlite_instance`` fixture is **session-scoped** because calling
    ``SQLiteMemory.dispose_engine()`` corrupts the shared SQLAlchemy
    ``Base.metadata`` state, preventing subsequent ``create_all`` calls from
    creating tables in a new in-memory database.  A single long-lived
    instance avoids this issue entirely.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

pytest.importorskip("pyrit", reason="pyrit not installed")

from pyrit.memory import CentralMemory, SQLiteMemory  # noqa: E402


@pytest.fixture(scope="session")
def sqlite_instance():
    """Create a single in-memory SQLite database for all PyRIT tests."""
    memory = SQLiteMemory(db_path=":memory:")
    CentralMemory.set_memory_instance(memory)
    yield memory
    # Intentionally skip dispose_engine() — see module docstring.


@pytest.fixture()
def patch_central_database(sqlite_instance):
    """Patch ``CentralMemory.get_memory_instance`` to return the in-memory DB."""
    with patch.object(
        CentralMemory, "get_memory_instance", return_value=sqlite_instance
    ):
        yield
