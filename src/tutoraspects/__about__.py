"""
Expose some package metadata.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tutor-contrib-aspects")
except PackageNotFoundError:
    __version__ = "0.0.0"
