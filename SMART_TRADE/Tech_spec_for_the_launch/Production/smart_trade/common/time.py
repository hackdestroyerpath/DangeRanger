"""Time utilities for UTC-safe timestamps."""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Current UTC datetime with tzinfo."""
    return datetime.now(UTC)


def utc_now_iso() -> str:
    """Current UTC datetime in ISO-8601 Z form."""
    return utc_now().isoformat().replace("+00:00", "Z")
