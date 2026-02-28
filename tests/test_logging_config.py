"""Unit tests for ditto.logging_config module."""

from __future__ import annotations

import logging
import sys

from ditto.logging_config import configure_logging


def _stream_handlers(logger: logging.Logger) -> list[logging.StreamHandler]:
    """Return only StreamHandler instances from logger's handler list."""
    return [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]


def test_configure_logging_sets_level():
    """configure_logging sets the root logger level."""
    configure_logging(level=logging.DEBUG, force=True)
    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_adds_stream_handler():
    """configure_logging adds a StreamHandler pointing to stdout."""
    configure_logging(force=True)
    handlers = _stream_handlers(logging.getLogger())
    assert len(handlers) >= 1
    assert any(h.stream is sys.stdout for h in handlers)


def test_configure_logging_no_duplicate_stream_handlers():
    """Second call without force=True does not add another StreamHandler."""
    configure_logging(force=True)
    count_before = len(_stream_handlers(logging.getLogger()))
    configure_logging()
    assert len(_stream_handlers(logging.getLogger())) == count_before


def test_configure_logging_force_reconfigures():
    """force=True replaces existing StreamHandlers and updates the level."""
    configure_logging(level=logging.INFO, force=True)
    configure_logging(level=logging.WARNING, force=True)
    assert logging.getLogger().level == logging.WARNING
    # After force, there should be exactly one StreamHandler (the new one).
    assert len(_stream_handlers(logging.getLogger())) == 1


def test_configure_logging_skips_when_handlers_exist(monkeypatch):
    """configure_logging is a no-op when handlers exist and force=False."""
    sentinel = logging.NullHandler()
    root = logging.getLogger()
    original_level = root.level
    # Use monkeypatch to isolate: temporarily replace the handlers list.
    monkeypatch.setattr(root, "handlers", [sentinel])
    configure_logging(level=logging.DEBUG)
    # Level should remain unchanged (no-op because handlers already exist).
    assert root.level == original_level
    # No new handler should have been added.
    assert root.handlers == [sentinel]
