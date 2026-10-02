"""Top-level Konsave package."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, distribution

try:
    __version__ = distribution(__name__).version
except PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0"
