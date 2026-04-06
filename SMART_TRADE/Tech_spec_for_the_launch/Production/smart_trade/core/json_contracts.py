"""Shared JSON contract helper utilities."""

from __future__ import annotations

import json
from typing import Any

from .errors import ValidationError


def ensure_json_object(payload: str, *, contract_name: str) -> dict[str, Any]:
    """Parse and validate that payload is a JSON object."""
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValidationError(
            code="JSON_INVALID",
            message=f"{contract_name} payload is not valid JSON",
            details={"contract": contract_name},
        ) from exc

    if not isinstance(value, dict):
        raise ValidationError(
            code="JSON_OBJECT_REQUIRED",
            message=f"{contract_name} must be a JSON object",
            details={"contract": contract_name, "type": type(value).__name__},
        )
    return value
