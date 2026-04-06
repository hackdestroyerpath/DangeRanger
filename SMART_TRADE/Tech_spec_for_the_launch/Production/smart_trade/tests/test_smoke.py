"""Smoke tests for PART 01 foundation."""

from smart_trade.config.loader import load_settings
from smart_trade.core.ids import new_uuid_v7, validate_uuid_v7


def test_load_settings_smoke() -> None:
    settings = load_settings()
    assert settings.frame.frame_id == "binance_futures_btcusdc_1m"


def test_uuid_v7_helpers() -> None:
    value = new_uuid_v7()
    normalized = validate_uuid_v7(value, field_name="case_id")
    assert normalized == value
