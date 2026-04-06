"""YAML + ENV settings loader."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from smart_trade.config.models import (
    CoreConfig,
    FrameConfig,
    LLMConfig,
    OpenClawConfig,
    Settings,
    SourcePolicyConfig,
)
from smart_trade.core.constants import CONFIG_DIR, DEFAULT_FRAME_ID
from smart_trade.core.errors import ConfigError


ENV_OVERRIDE_MAP: dict[str, tuple[str, str]] = {
    "SMART_TRADE_ENV": ("core", "env"),
    "SMART_TRADE_DB_PATH": ("core", "db_path"),
    "SMART_TRADE_ARTIFACTS_DIR": ("core", "artifacts_dir"),
    "SMART_TRADE_LOG_LEVEL": ("core", "log_level"),
    "SMART_TRADE_FRAME_DEFAULT": ("core", "frame_default"),
    "LLM_PRIMARY_MODEL": ("llm", "primary_model"),
    "LLM_FALLBACK_MODEL": ("llm", "fallback_model"),
    "LLM_TIMEOUT_SEC": ("llm", "timeout_sec"),
    "OPENCLAW_DEFAULT_TIMEOUT_SEC": ("openclaw", "default_timeout_sec"),
    "SOURCE_POLICY_PROFILE": ("source_policy", "profile"),
    "RESEARCH_WEB_ENABLED": ("source_policy", "research_web_enabled"),
}


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(
            code="CONFIG_FILE_MISSING",
            message=f"Config file not found: {path}",
            details={"path": str(path)},
        )
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ConfigError(
            code="CONFIG_FILE_INVALID",
            message=f"Config must be YAML mapping: {path}",
            details={"path": str(path)},
        )
    return raw


def _coerce_env(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if value.isdigit():
        return int(value)
    return value


def _apply_env_overrides(settings_dict: dict[str, dict[str, Any]]) -> None:
    for env_name, (section, key) in ENV_OVERRIDE_MAP.items():
        if env_name in os.environ:
            settings_dict[section][key] = _coerce_env(os.environ[env_name])


def load_settings(
    *,
    config_dir: Path | None = None,
    frame_id: str | None = None,
) -> Settings:
    """Load canonical settings from YAML + ENV overrides."""
    root = config_dir or CONFIG_DIR

    project_raw = _read_yaml(root / "project.yaml")
    core_data = project_raw.get("project", {})

    frame_selected = frame_id or os.environ.get("SMART_TRADE_FRAME_DEFAULT") or DEFAULT_FRAME_ID
    frame_data = _read_yaml(root / "frames" / f"{frame_selected}.yaml")

    llm_data = _read_yaml(root / "llm.yaml").get("llm", {})
    openclaw_data = _read_yaml(root / "openclaw.yaml").get("openclaw", {})
    source_policy_data = _read_yaml(root / "source_policy.yaml").get("source_policy", {})

    model_data: dict[str, dict[str, Any]] = {
        "core": core_data,
        "frame": frame_data,
        "llm": llm_data,
        "openclaw": openclaw_data,
        "source_policy": source_policy_data,
    }

    _apply_env_overrides(model_data)

    try:
        return Settings(
            core=CoreConfig(**model_data["core"]),
            frame=FrameConfig(**model_data["frame"]),
            llm=LLMConfig(**model_data["llm"]),
            openclaw=OpenClawConfig(**model_data["openclaw"]),
            source_policy=SourcePolicyConfig(**model_data["source_policy"]),
        )
    except Exception as exc:  # pydantic ValidationError
        raise ConfigError(
            code="CONFIG_VALIDATION_FAILED",
            message="Runtime configuration failed validation",
            details={"error": str(exc)},
        ) from exc
