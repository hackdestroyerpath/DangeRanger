"""Base error hierarchy for SMART_TRADE foundation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SmartTradeError(Exception):
    """Base project exception with machine-readable code and details."""

    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


@dataclass(slots=True)
class ConfigError(SmartTradeError):
    """Configuration read/validate errors."""


@dataclass(slots=True)
class ValidationError(SmartTradeError):
    """Domain validation errors."""


@dataclass(slots=True)
class IdFormatError(ValidationError):
    """Canonical identifier validation error."""
