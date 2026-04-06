"""Canonical ID generators and validators."""

from __future__ import annotations

import re
import secrets
import time
import uuid

from .errors import IdFormatError

FRAME_FAMILY_RE = re.compile(r"^[a-z0-9]+_[a-z0-9]+_[0-9]+[smhdw]$")
FRAME_SHARD_RE = re.compile(r"^[a-z0-9]+_[a-z0-9]+_[a-z0-9]+_[0-9]+[smhdw]$")
SKILL_VERSION_RE = re.compile(r"^[A-Za-z0-9_]+@[a-z0-9_]+@v[0-9]+$")
PHENOTYPE_KEY_RE = re.compile(r"^dir=[^|]+\|vol=[^|]+\|liq=[^|]+\|session=[^|]+$")


def new_uuid_v7() -> str:
    """Generate UUIDv7 string.

    Uses stdlib `uuid.uuid7` when available, with local fallback for runtimes
    where uuid7 is not exposed yet.
    """
    uuid7_factory = getattr(uuid, "uuid7", None)
    if callable(uuid7_factory):
        return str(uuid7_factory())

    # RFC 9562 layout: 48-bit unix_ms + version(7) + variant(10) + random tail.
    unix_ms = int(time.time_ns() // 1_000_000) & ((1 << 48) - 1)
    random_a = secrets.randbits(12)
    random_b = secrets.randbits(62)

    value = 0
    value |= unix_ms << 80
    value |= 0x7 << 76
    value |= random_a << 64
    value |= 0b10 << 62
    value |= random_b

    return str(uuid.UUID(int=value))


def validate_uuid_v7(value: str, *, field_name: str) -> str:
    """Ensure provided identifier is UUIDv7."""
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise IdFormatError(
            code="ID_INVALID_UUID",
            message=f"{field_name} must be UUID",
            details={"field": field_name, "value": value},
        ) from exc

    if parsed.version != 7:
        raise IdFormatError(
            code="ID_INVALID_VERSION",
            message=f"{field_name} must be UUIDv7",
            details={"field": field_name, "value": value, "version": parsed.version},
        )
    return str(parsed)


def validate_frame_family_id(value: str) -> str:
    if not FRAME_FAMILY_RE.fullmatch(value):
        raise IdFormatError(
            code="FRAME_FAMILY_ID_INVALID",
            message="frame_family_id must match <exchange>_<market>_<timeframe>",
            details={"value": value},
        )
    return value


def validate_frame_shard_id(value: str) -> str:
    if not FRAME_SHARD_RE.fullmatch(value):
        raise IdFormatError(
            code="FRAME_SHARD_ID_INVALID",
            message="frame_shard_id must match <exchange>_<market>_<symbol>_<timeframe>",
            details={"value": value},
        )
    return value


def validate_skill_version_id(value: str) -> str:
    if not SKILL_VERSION_RE.fullmatch(value):
        raise IdFormatError(
            code="SKILL_VERSION_ID_INVALID",
            message="skill_version_id must match <skill_family_id>@<branch_id>@v<int>",
            details={"value": value},
        )
    return value


def validate_phenotype_key(value: str) -> str:
    if not PHENOTYPE_KEY_RE.fullmatch(value):
        raise IdFormatError(
            code="PHENOTYPE_KEY_INVALID",
            message="phenotype key must match dir|vol|liq|session axis order",
            details={"value": value},
        )
    return value
