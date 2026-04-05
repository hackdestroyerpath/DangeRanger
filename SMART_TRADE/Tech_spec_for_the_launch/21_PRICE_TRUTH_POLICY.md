# 21_PRICE_TRUTH_POLICY

## Назначение

Этот файл фиксирует **единый источник истины цены** для:
- replay;
- метрик;
- phenotype;
- counterfactual analysis.

Без него команды будут считать `R`, fill и timeout по разным ценам.

---

## 1. Canonical truth source

### Для signal generation и phenotype
- canonical price source = `last traded price` + supporting top-of-book

### Для fill semantics
- canonical fill source = execution telemetry from execution bridge

### Для post-trade replay / counterfactual
- canonical replay path = `last trade price stream` of the same market feed family used at runtime

---

## 2. Priority order

### 2.1. Entry / exit truth

1. actual fill price from execution telemetry
2. if not filled -> no synthetic fill created in official outcome

### 2.2. Replay / counterfactual path

1. recorded live last-price path
2. fallback cached live path
3. if missing -> `censored=true`

### 2.3. Book / spread support

Used only for:
- liquidity state
- execution realism
- semantic audits

Not as primary truth for official `realized_R`.

---

## 3. Rounding and precision

### Rule
All prices must be normalized according to symbol precision and tick size **before** validation and before execution request.

### Canonical policy
- store raw source value
- store normalized value used for order geometry
- calculations use normalized value

---

## 4. Missing ticks / gaps

If replay path has gaps:
- mark gap in artifact metadata
- do not invent synthetic path segment silently
- if gap blocks confident replay result -> set `censored=true`

If official execution telemetry missing:
- do not infer official TP/SL result from market path
- case goes to infra/telemetry anomaly

---

## 5. Mid / mark / last

### Official outcome metrics
Use **fill prices** from telemetry.

### Phenotype / liquidity logic
Can use:
- top-of-book
- spread
- bid/ask

### Counterfactual replay
Use canonical `last-price path` for baseline implementation.

`mark price` or `mid price` may be stored additionally, but they are not the default truth source for official `R`.
