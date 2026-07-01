"""
ASTRAXIS-AI Structured Logger.

Provides a centralized, color-coded Rich console logger for all
ASTRAXIS-AI engine components.

Key Concept — Why Rich over print()?
    Plain print() gives you raw text with zero structure.
    Rich gives you:
        - Color-coded severity levels (DEBUG=blue, INFO=green, WARNING=yellow, ERROR=red)
        - Timestamps on every log line
        - Structured tracebacks for exceptions
        - Beautiful panels and tables for displaying scan results
"""
from rich.console import Console
from rich.logging import RichHandler
import logging

from astraxis.core.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Build and return a Rich-powered structured logger.

    Each module in ASTRAXIS-AI calls get_logger(__name__) to receive
    its own named logger that outputs colorized, timestamped log lines
    to the terminal.

    Args:
        name: The module name (pass __name__ from the calling module).

    Returns:
        A configured Python Logger instance with Rich console handler.

    Example:
        >>> from astraxis.core.logger import get_logger
        >>> log = get_logger(__name__)
        >>> log.info("Red-teaming scan started")
        >>> log.warning("Jailbreak payload detected")
        >>> log.error("Sandbox container failed to start")
    """
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False
            )
        ]
    )
    return logging.getLogger(name)


# Shared console instance for tables, panels, and banners
console = Console()
