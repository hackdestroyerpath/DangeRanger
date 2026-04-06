"""Canonical enum definitions for SMART_TRADE core domain."""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Enum that serializes as plain string."""

    def __str__(self) -> str:
        return self.value


class Environment(StrEnum):
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


class SkillMode(StrEnum):
    EXPLICIT = "EXPLICIT"
    AUTO = "AUTO"
    ISOLATED = "ISOLATED"


class SkillVersionStatus(StrEnum):
    DRAFT = "DRAFT"
    CANDIDATE = "CANDIDATE"
    CHALLENGER = "CHALLENGER"
    CHAMPION = "CHAMPION"
    NICHE = "NICHE"
    WATCHLIST = "WATCHLIST"
    QUARANTINED = "QUARANTINED"
    RETIRED = "RETIRED"
    REJECTED = "REJECTED"


class MutationType(StrEnum):
    MICRO_PATCH = "MICRO_PATCH"
    LOCAL_REWRITE = "LOCAL_REWRITE"
    MACRO_BRANCH = "MACRO_BRANCH"
    RECOMBINATION = "RECOMBINATION"
    DECOMPOSITION = "DECOMPOSITION"
    FOUNDRY_SYNTHESIS = "FOUNDRY_SYNTHESIS"
    OVERLAY_PATCH = "OVERLAY_PATCH"


class GeneBlock(StrEnum):
    IDEA_SOURCE_POLICY = "idea_source_policy"
    DATA_REQUEST_POLICY = "data_request_policy"
    INTERPRETATION_POLICY = "interpretation_policy"
    ENTRY_POLICY = "entry_policy"
    SL_POLICY = "sl_policy"
    TP_POLICY = "tp_policy"
    TIMEOUT_POLICY = "timeout_policy"
    ETA_POLICY = "eta_policy"
    OUTPUT_DISCIPLINE = "output_discipline"
