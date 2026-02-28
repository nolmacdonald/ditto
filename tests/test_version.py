"""Unit tests for ditto version."""

from __future__ import annotations

import ditto


def test_version_exists():
    """__version__ is defined."""
    assert hasattr(ditto, "__version__")


def test_version_string():
    """__version__ is a non-empty string."""
    assert isinstance(ditto.__version__, str)
    assert ditto.__version__
