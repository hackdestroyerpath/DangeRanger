"""Project-wide constants for PART 01 foundation."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_FRAME_ID = "binance_futures_btcusdc_1m"
DEFAULT_FRAME_FILE = CONFIG_DIR / "frames" / f"{DEFAULT_FRAME_ID}.yaml"

FRAME_KEY_SEPARATOR = "_"
PHENOTYPE_KEY_SEPARATOR = "|"

UUID_VERSION = 7
ISO8601_UTC_SUFFIX = "Z"

PRAGMA_BOOTSTRAP = (
    "PRAGMA journal_mode=WAL;",
    "PRAGMA foreign_keys=ON;",
    "PRAGMA synchronous=NORMAL;",
    "PRAGMA temp_store=MEMORY;",
    "PRAGMA busy_timeout=5000;",
)
