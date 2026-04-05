# Примеры к разделу: 5. Конфигурация

## Пример 1
Язык / тип: `text`

```text
SMART_TRADE/config/
```

## Пример 2
Язык / тип: `text`

```text
SMART_TRADE/
  config/
    project.yaml
    llm.yaml
    evolution.yaml
    execution.yaml
    source_policy.yaml
    openclaw.yaml
    lab.yaml
    frames/
      binance_futures_btcusdc_1m.yaml
    overlays/
      prod_trader.yaml
      tester.yaml
      evolver.yaml
      foundry.yaml
```

## Пример 3
Язык / тип: `text`

```text
project defaults
-> frame defaults
-> frame shard config
-> explicit run override
```

## Пример 4
Язык / тип: `yaml`

```yaml
frame_id: binance_futures_btcusdc_1m
frame_family_id: binance_futures_1m

exchange: Binance
market: Futures
symbols:
  - BTCUSDC

fee_pct: 0.0
timeframe: 1m

execution:
  order_type: limit_only
  require_tp: true
  require_sl: true
  entry_timeout_sec: 300
  position_timeout_enabled: false

skill_mode: EXPLICIT | AUTO | ISOLATED
skill_scope: []
```
