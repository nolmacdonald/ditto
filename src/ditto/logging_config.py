"""Logging configuration utilities for ditto.

Provides a simple function to configure Python's standard logging module
with sensible defaults suitable for library and application use.
"""

from __future__ import annotations

import logging
import sys


def configure_logging(
    level: int = logging.INFO,
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt: str = "%Y-%m-%dT%H:%M:%S",
    force: bool = False,
) -> None:
    """Configure the root logger with a StreamHandler writing to stdout.

    Call this once at the entry point of an application that uses ditto.
    Library code should *not* call this function; it is intended for
    end-user scripts and CLI entry points.

    Mirrors the semantics of :func:`logging.basicConfig`: if the root logger
    already has handlers, this function is a no-op unless ``force=True``.

    Parameters
    ----------
    level : int, optional
        Logging level (e.g. ``logging.DEBUG``, ``logging.INFO``), by default
        ``logging.INFO``.
    fmt : str, optional
        Log record format string accepted by :class:`logging.Formatter`.
    datefmt : str, optional
        Date/time format string for the formatter.
    force : bool, optional
        When ``True``, remove any existing handlers before configuring.
        Use this to reconfigure logging in scripts that may have pre-existing
        handlers. By default ``False``.

    Examples
    --------
    >>> from ditto.logging_config import configure_logging
    >>> configure_logging(level=logging.DEBUG)
    """
    root_logger = logging.getLogger()

    # Mirror logging.basicConfig semantics: skip setup if handlers already
    # exist unless the caller explicitly requests a forced reconfiguration.
    if root_logger.handlers and not force:
        return

    if force:
        # Remove existing handlers only when the caller explicitly opts in,
        # to avoid unexpectedly discarding file handlers or structured loggers.
        root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)

    root_logger.setLevel(level)
    root_logger.addHandler(handler)
