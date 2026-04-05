# 18_MARKET_DATA_PROVIDER_PROFILE

## Назначение

Этот файл фиксирует **конкретный профиль market data providers**, payloads, SLA и fallback policy.

Он закрывает операционную дыру:
- “с какими данными проект вообще работает на старте?”

---

## 1. Provider stack

### P1. Binance Futures public market data

Используется как основной источник для:
- candles;
- trades / aggTrades;
- top-of-book best bid/ask;
- orderbook-derived liquidity proxies.

### P2. Internal derived providers

Используются для:
- phenotype probe inputs;
- feature calculators;
- rolling cached artifacts;
- OFI / imbalance / delta-like derived views.

### P3. Execution telemetry provider

Используется для:
- fill time;
- cancel reason;
- order pending/open/closed;
- entry/exit execution facts.

---

## 2. Canonical payload groups

### 2.1. Candles

```json
{
  "symbol": "BTCUSDC",
  "timeframe": "1m",
  "bars": [
    {
      "open_time": "...",
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "volume": 0,
      "close_time": "..."
    }
  ]
}
```

### 2.2. Spread / liquidity

```json
{
  "symbol": "BTCUSDC",
  "ts": "...",
  "bid": 0,
  "ask": 0,
  "spread": 0,
  "bid_size": 0,
  "ask_size": 0
}
```

### 2.3. Trades / aggTrades

```json
{
  "symbol": "BTCUSDC",
  "trades": [
    {
      "ts": "...",
      "price": 0,
      "qty": 0,
      "side": "buy|sell"
    }
  ]
}
```

### 2.4. Execution telemetry

```json
{
  "signal_id": "uuid",
  "submitted_at": "...",
  "filled_at": "...",
  "closed_at": "...",
  "entry_fill_price": 0,
  "exit_price": 0,
  "outcome_code": "TP_HIT"
}
```

---

## 3. MVP required providers

Чтобы проект реально “завёлся”, минимум должны существовать:

1. `candles_provider`
2. `spread_provider`
3. `execution_telemetry_provider`
4. `derived_feature_provider`

Без этих 4 провайдеров нельзя реализовать:
- phenotype;
- expectancy correctness;
- arena;
- mutation;
- routing.

---

## 4. Freshness / SLA defaults

### Candles
- lag tolerance: `<= 2s`

### Spread / book proxy
- lag tolerance: `<= 500ms`

### Trades / aggTrades
- lag tolerance: `<= 500ms`

### Execution telemetry
- event-driven
- monotonic ordering required

---

## 5. Fallback policy

Порядок fallback:

```text
primary provider
-> warm local cache
-> coverage_gap
```

Если данные stale:
- создаётся `freshness_flag`
- при критическом запросе -> `BLOCKED_BY_DATA_COVERAGE`
- skill mutation по такому кейсу не запускается

---

## 6. Provider priorities

### Priority order for MVP

1. `binance_public_ws_or_rest`
2. `internal_cache`
3. `derived_feature_cache`
4. `coverage_gap`

### Priority order for research / derived analytics

1. `internal_derived_provider`
2. `cached artifacts`
3. `research augmentation sources`

---

## 7. What is NOT decided here

Этот файл не зашивает:
- твои реальные endpoints;
- твои реальные private feeds;
- твой фактический provider deployment topology.

Он фиксирует:
- минимальный контракт;
- приоритет;
- payloads;
- SLA;
- fallback rules.
