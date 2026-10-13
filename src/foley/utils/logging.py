"""Structured, rich-backed logging for the host and plugins."""

from __future__ import annotations

import logging

from rich.logging import RichHandler

_configured = False


def configure_logging(verbose: bool = False) -> None:
    global _configured
    if _configured:
        return
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)