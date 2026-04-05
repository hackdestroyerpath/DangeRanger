# Примеры к разделу: 34. Канонические JSON schemas

## Пример 1
Язык / тип: `json`

```json
{
  "frame_id": "binance_futures_btcusdc_1m",
  "frame_family_id": "binance_futures_1m",
  "frame_shard_id": "binance_futures_btcusdc_1m",
  "exchange": "Binance",
  "market": "Futures",
  "symbols": ["BTCUSDC"],
  "fee_pct": 0.0,
  "timeframe": "1m",
  "execution": {
    "order_type": "limit_only",
    "require_tp": true,
    "require_sl": true,
    "entry_timeout_sec": 900,
    "position_timeout_enabled": false
  },
  "skill_mode": "EXPLICIT",
  "skill_scope": {
    "explicit_skill_family_ids": ["Lite_TRADING_SKILL_01_04_2026"],
    "isolated_skill_dir": null
  },
  "source_policy_id": "source_policy_scalping_v1",
  "llm_policy_id": "llm_policy_default_v1"
}
```

## Пример 2
Язык / тип: `json`

```json
{
  "request_id": "uuid",
  "data_type": "orderflow.ofi_l1",
  "symbol": "BTCUSDC",
  "timeframe": "1m",
  "lookback": {"seconds": 300},
  "params": {
    "aggregation": "1s",
    "z_window": 120
  },
  "output_format": "json"
}
```

## Пример 3
Язык / тип: `json`

```json
{
  "request_id": "uuid",
  "status": "ok",
  "result_kind": "json",
  "provider_name": "internal_orderflow_provider",
  "as_of_ts": "2026-04-05T12:00:00Z",
  "payload": {},
  "meta": {
    "latency_ms": 42,
    "freshness_ok": true,
    "semantic_ok": true
  }
}
```

## Пример 4
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "frame_id": "binance_futures_btcusdc_1m",
  "symbol": "BTCUSDC",
  "side": "LONG",
  "entry_limit": 101250.0,
  "stop_loss": 100900.0,
  "take_profit": 101950.0,
  "expected_fill_window_sec": 180,
  "thesis_short": "string",
  "artifacts": []
}
```

## Пример 5
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "skill_family_id": "Lite_TRADING_SKILL_01_04_2026",
  "skill_version_id": "Lite_TRADING_SKILL_01_04_2026@main@v18",
  "why_entry": "string",
  "why_sl": "string",
  "why_tp": "string",
  "why_eta": "string",
  "requested_data_summary": ["..."],
  "key_observations": ["..."],
  "self_critic_note": "string"
}
```

## Пример 6
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "symbol": "BTCUSDC",
  "side": "LONG",
  "entry_limit": 101250.0,
  "stop_loss": 100900.0,
  "take_profit": 101950.0,
  "entry_timeout_sec": 900
}
```

## Пример 7
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "symbol": "BTCUSDC",
  "side": "LONG",
  "submitted_at": "2026-04-05T12:35:03Z",
  "filled_at": "2026-04-05T12:39:10Z",
  "entry_fill_price": 101248.5,
  "closed_at": "2026-04-05T13:02:18Z",
  "exit_price": 101950.0,
  "outcome_code": "TP_HIT",
  "operator_intervened": false,
  "raw_payload": {}
}
```

## Пример 8
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "type": "decision_capsule",
  "skill_family_id": "...",
  "skill_version_id": "...",
  "why_entry": "...",
  "why_sl": "...",
  "why_tp": "...",
  "claimed_edge": "...",
  "data_or_source_used": "..."
}
```

## Пример 9
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "type": "lesson_capsule",
  "fault_gene": "entry_policy",
  "what_was_wrong": "...",
  "what_to_change": "...",
  "confidence": 0.78
}
```

## Пример 10
Язык / тип: `json`

```json
{
  "skill_family_id": "Lite_TRADING_SKILL_01_04_2026",
  "skill_version_id": "Lite_TRADING_SKILL_01_04_2026@range_branch@v7",
  "branch_id": "range_branch",
  "contract_version": "1.0",
  "mutation_type": "LOCAL_REWRITE",
  "niche_key": "dir=range|vol=compression|liq=normal|session=eu",
  "source_case_ids": ["..."],
  "created_by": "evolver_agent"
}
```
