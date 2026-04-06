"""Logging bootstrap helper."""

from __future__ import annotations

import logging


def configure_logging(level: str) -> None:
    """Configure root logging only once."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
