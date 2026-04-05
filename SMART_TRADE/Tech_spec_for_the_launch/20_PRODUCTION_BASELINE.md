# 20_PRODUCTION_BASELINE

## Назначение

Этот файл фиксирует **обязательный baseline config** для MVP/MAX старта, чтобы Codex не гадал дефолты.

---

## 1. Frame baseline

```yaml
exchange: Binance
market: Futures
symbols: [BTCUSDC]
timeframe: 1m
fee_pct: 0.0
```

---

## 2. Execution baseline

```yaml
execution:
  order_type: limit_only
  require_tp: true
  require_sl: true
  entry_timeout_sec: 300
  position_timeout_enabled: false
  webhook_timeout_sec: 10
```

---

## 3. Runtime baseline

```yaml
runtime:
  max_concurrent_prod_cases_per_frame_shard: 1
  max_concurrent_lab_cases_per_frame_shard: 12
  case_ttl_sec: 3600
  duplicate_case_guard: true
```

---

## 4. Arena baseline

```yaml
arena:
  champion_share: 0.70
  challenger_share: 0.20
  niche_share: 0.05
  foundry_or_zero_share: 0.05
  max_weight_per_skill: 0.35
  keep_alive_floor: 0.05
  sandbox_cap: 0.15
```

If weak phenotype in curriculum queue:

```yaml
arena_weak_regime_override:
  champion_share: 0.60
  challenger_share: 0.25
  niche_share: 0.10
  foundry_or_zero_share: 0.05
```

---

## 5. Evolution baseline

```yaml
evolution:
  windows: [10, 30, 100]
  local_mutation_min_cases: 30
  recombination_min_cases_per_parent: 40
  soft_selection_min_cases: 20
  hard_selection_min_cases: 50
  mutation_cooldown_cases: 10
  major_adaptation_cooldown_cases: 20
  max_children_per_parent: 3
  local_child_sandbox_weight: 0.15
  recombined_child_sandbox_weight: 0.10
  regime_shift_trigger_population_fail_share: 0.60
  similarity_cap: 0.80
```

---

## 6. Lab baseline

```yaml
lab:
  baseline_workers: 4
  challenger_workers: 4
  niche_workers: 2
  zero_skill_workers: 2
  scheduler_tick_sec: 5
  family_rebalance_every_n_cases: 5
  family_deep_review_every_n_cases: 20
```

---

## 7. Feature flags baseline

```yaml
features:
  enable_recombination: true
  enable_speciation: true
  enable_decomposition: true
  enable_foundry: true
  enable_research_augmentation: true
  enable_overlay_evolution: true
  enable_position_timeout: false
  enable_cross_frame_recombination: false
  enable_user_facing_no_trade: false
```

---

## 8. Stop rules baseline

Внутри `SMART_TRADE` stop-rules трактуются как **операционные стопы системы**, а не денежный риск-менеджмент.

Стартовые ограничения:
- если webhook ingestion unstable -> pause prod submit
- если execution bridge unavailable -> block submit, allow only logging
- если protocol breach rate explodes -> quarantine affected line
- если data coverage collapses -> block affected cases

---

## 9. Что не задаётся здесь

Здесь не задаются:
- реальные секреты;
- реальные домены;
- реальные лимиты капитала;
- реальные биржевые ключи;
- пользовательский portfolio risk.
