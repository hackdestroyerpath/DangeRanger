# Примеры к разделу: 17. Arena, Sandbox, Tester

## Пример 1
Язык / тип: `text`

```text
frame_shard + phenotype bucket
```

## Пример 2
Язык / тип: `text`

```text
arena_score_raw =
  0.28 * E30_score
+ 0.16 * E100_score
+ 0.10 * PF_score
+ 0.10 * fill_feasibility
+ 0.08 * eta_accuracy
+ 0.08 * plan_validity
+ 0.08 * stability_score
+ 0.05 * regime_fit_score
+ 0.07 * freshness_score
- 0.05 * pain_penalty
- 0.03 * protocol_penalty
- 0.02 * anti_pattern_penalty

arena_score = clamp(arena_score_raw, 0, 1)
```

## Пример 3
Язык / тип: `text`

```text
family_score_raw =
  0.40 * top2_mean_arena_score
+ 0.20 * family_E100_score
+ 0.10 * diversity_score
+ 0.10 * niche_coverage_score
+ 0.10 * family_freshness_score
+ 0.10 * lineage_health_score
- 0.10 * family_pain_penalty

family_score = clamp(family_score_raw, 0, 1)
```

## Пример 4
Язык / тип: `text`

```text
routing_base = 0.65 * arena_score + 0.35 * family_score
```
