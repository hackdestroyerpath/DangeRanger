# Примеры к разделу: 32. Канонические идентификаторы и соглашения об именах

## Пример 1
Язык / тип: `text`

```text
frame_family_id   := <exchange>_<market>_<timeframe>
frame_shard_id    := <exchange>_<market>_<symbol>_<timeframe>
skill_family_id   := <PascalCase or SCREAMING_CASE root>
branch_id         := main | repair_<block> | niche_<phenotype_slug> | hybrid_<slug>
skill_version_id  := <skill_family_id>@<branch_id>@v<int>
case_id           := uuid_v7
signal_id         := uuid_v7
mutation_id       := uuid_v7
recombination_id  := uuid_v7
promotion_id      := uuid_v7
research_run_id   := uuid_v7
llm_judgment_id   := uuid_v7
```

## Пример 2
Язык / тип: `text`

```text
dir=<...>|vol=<...>|liq=<...>|session=<...>
```

## Пример 3
Язык / тип: `text`

```text
dir=up|vol=expansion|liq=thin|session=us
```

## Пример 4
Язык / тип: `text`

```text
DRAFT
CANDIDATE
CHALLENGER
CHAMPION
NICHE
WATCHLIST
QUARANTINED
RETIRED
REJECTED
```

## Пример 5
Язык / тип: `text`

```text
MICRO_PATCH
LOCAL_REWRITE
MACRO_BRANCH
RECOMBINATION
DECOMPOSITION
FOUNDRY_SYNTHESIS
OVERLAY_PATCH
```

## Пример 6
Язык / тип: `text`

```text
idea_source_policy
data_request_policy
interpretation_policy
entry_policy
sl_policy
tp_policy
timeout_policy
eta_policy
output_discipline
```
