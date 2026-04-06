"""Hash helpers for idempotency and content addressing."""

from __future__ import annotations

import hashlib


def sha256_hex(parts: list[str]) -> str:
    """Compute deterministic sha256 from ordered string parts."""
    joined = "|".join(parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()
