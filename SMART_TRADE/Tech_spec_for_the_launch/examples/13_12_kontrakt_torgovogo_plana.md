# Примеры к разделу: 12. Контракт торгового плана

## Пример 1
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "frame_id": "binance_futures_btcusdc_1m",
  "skill_family_id": "Lite_TRADING_SKILL_01_04_2026",
  "skill_version_id": "Lite_TRADING_SKILL_01_04_2026@main@v18",

  "symbol": "BTCUSDC",
  "side": "LONG|SHORT",

  "entry_limit": 101250.0,
  "stop_loss": 100900.0,
  "take_profit": 101950.0,

  "expected_fill_window_sec": 120,

  "generated_at": "2026-04-05T12:34:56Z",
  "thesis_short": "string"
}
```

## Пример 2
Язык / тип: `json`

```json
{
  "expected_fill_deadline_ts": "2026-04-05T12:39:56Z",
  "expected_fill_deadline_sec": 300
}
```

## Пример 3
Язык / тип: `text`

```text
expected_fill_deadline_sec = frame.execution.entry_timeout_sec
expected_fill_deadline_ts = generated_at + expected_fill_deadline_sec
```
