"""
ASTRAXIS-AI Command-Line Interface (CLI) Package.

Provides terminal entry points for running automated red-team audit scans,
inspecting payloads, rendering attack graphs, and exporting reports.
"""
from astraxis.cli.main import main, app

__all__ = ["main", "app"]
