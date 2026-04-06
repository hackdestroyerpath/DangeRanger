"""Pydantic models for YAML+ENV runtime configuration."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from smart_trade.core.enums import Environment, SkillMode


class ExecutionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_type: str = "limit_only"
    require_tp: bool = True
    require_sl: bool = True
    entry_timeout_sec: int = 300
    position_timeout_enabled: bool = False
    webhook_timeout_sec: int = 10


class FrameConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    frame_id: str
    frame_family_id: str
    exchange: str
    market: str
    symbols: list[str]
    timeframe: str
    fee_pct: float = 0.0
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    skill_mode: SkillMode = SkillMode.EXPLICIT
    skill_scope: list[str] = Field(default_factory=list)


class CoreConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    env: Environment = Environment.DEV
    db_path: Path = Path("./var/smart_trade.db")
    artifacts_dir: Path = Path("./var/artifacts")
    log_level: str = "INFO"
    frame_default: str = "binance_futures_btcusdc_1m"

    @field_validator("log_level")
    @classmethod
    def _normalize_log_level(cls, value: str) -> str:
        normalized = value.upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed:
            raise ValueError(f"Unsupported log level: {value}")
        return normalized


class LLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_model: str = "gpt-5.4-pro"
    fallback_model: str = "gpt-5.4-pro"
    timeout_sec: int = 120


class OpenClawConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default_timeout_sec: int = 60
    spawn_timeout_sec: int = 60
    materialization_timeout_sec: int = 30
    collect_artifacts_timeout_sec: int = 30
    retry_attempts: int = 3


class SourcePolicyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str = "source_policy_scalping_v1"
    research_web_enabled: bool = True


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    core: CoreConfig
    frame: FrameConfig
    llm: LLMConfig
    openclaw: OpenClawConfig
    source_policy: SourcePolicyConfig
