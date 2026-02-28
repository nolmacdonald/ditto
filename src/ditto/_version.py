"""Version information for ditto."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ditto")
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed (e.g. running from source without install).
    __version__ = "unknown"
