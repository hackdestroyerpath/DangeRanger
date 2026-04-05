# 13_CODEX_PARTITION_PLAN

## Назначение

Разбивка проекта на части для Codex.

Цель:
- `1 запрос = 1 часть`
- `~5000` строк кода на часть
- после последней части готово `>=80%` кодовой базы

---

## Общие правила части

Каждая часть должна:
- собираться без логических конфликтов с предыдущими;
- иметь собственные acceptance criteria;
- не требовать незавершённых будущих частей для базовой компиляции;
- обновлять `PART_STATUS.md`, `CHANGELOG.md`, `TODO.md`.

---

## PART 01 — Project Foundation

### Scope
- package root
- config loader
- ids / enums / constants
- error base classes
- common utils
- pyproject / lint / typecheck / test scaffolding

### Target LOC
`3500–5000`

### Acceptance
- проект импортируется
- конфиги читаются
- базовые типы и id работают

---

## PART 02 — SQL Core + Repositories Base

### Scope
- SQLite schema
- PRAGMA bootstrap
- migrations bootstrap
- repository base
- transaction helpers
- append-only event primitives

### Target LOC
`4500–5500`

### Acceptance
- БД поднимается с нуля
- schema создаётся полностью
- базовые CRUD/append работают

---

## PART 03 — Frame Engine

### Scope
- `FRAME.MD` parser
- frame normalizer adapters
- frame validator
- `frame_resolved.json`
- frame precedence rules

### Target LOC
`4000–5000`

### Acceptance
- любой корректный FRAME превращается в resolved JSON
- ошибки двусмысленности помечаются

---

## PART 04 — Signal Contracts + Runtime Core

### Scope
- trade plan models
- thesis snapshot models
- case lifecycle state machine
- runtime case service
- signal submission service

### Target LOC
`4500–5500`

### Acceptance
- можно создать кейс
- можно принять план
- можно записать thesis snapshot

---

## PART 05 — OpenClaw Bridge + Materialization

### Scope
- workspace manager
- skill allowlist
- overlay materialization
- session runner
- agent launch adapters

### Target LOC
`4500–5500`

### Acceptance
- материализация навыков работает
- новая сессия поднимается правильно
- modes `EXPLICIT/AUTO/ISOLATED` соблюдаются

---

## PART 06 — Data Router + Tool Quality + Coverage

### Scope
- universal data request router
- provider registry
- data artifacts
- coverage gaps
- tool quality monitor
- semantic second opinion plumbing

### Target LOC
`4500–5500`

### Acceptance
- `request_market_data` работает
- coverage gap фиксируется
- quality events пишутся

---

## PART 07 — Execution Bridge + Webhooks

### Scope
- order submission API client
- idempotency keys
- outcome ingest
- webhook auth / dedup
- terminal status resolution

### Target LOC
`4000–5000`

### Acceptance
- submit / ack / outcome цепочка воспроизводима
- повторный webhook не ломает систему

---

## PART 08 — Phenotype Engine + Market Shift Detection

### Scope
- pretrade probe
- posttrade tagger
- phenotype tables
- bucket key generation
- market shift alert levels

### Target LOC
`4500–5500`

### Acceptance
- phenotype считается до и после сделки
- routing buckets стабильны
- market shift alert выдается по правилам

---

## PART 09 — Skill Registry + Packaging + Lineage

### Scope
- skill families / branches / versions
- packaging
- gene map
- lineage ledger
- filesystem skill artifacts

### Target LOC
`4500–5500`

### Acceptance
- skill version можно создать, упаковать, зарегистрировать
- lineage append-only

---

## PART 10 — Expectancy Monitor + Arena Scoring + Routing

### Scope
- official expectancy windows
- PF / stability / freshness / pain
- arena_score
- family_score
- routing weights and bounded softmax

### Target LOC
`4500–5500`

### Acceptance
- scores пересчитываются после terminal case
- routing weights корректны

---

## PART 11 — Outcome Analyzer + Capsules + Fault Graph

### Scope
- decision capsules
- lesson capsules
- outcome analyzer
- causal fault graph
- protocol integrity gate

### Target LOC
`4500–5500`

### Acceptance
- post-trade diagnostic bundle формируется
- primary fault gene определяется

---

## PART 12 — Mutation Core

### Scope
- mutation controller
- critic pass
- rewrite pass
- validation pass
- local mutation rules

### Target LOC
`4500–5500`

### Acceptance
- 1 child / 1 gene / 1 generation enforced
- invalid candidate не проходит

---

## PART 13 — Recombination + Speciation + Decomposition

### Scope
- recombination admission gate
- compatibility matrix
- speciation engine
- decomposition planner
- niche registry

### Target LOC
`4500–5500`

### Acceptance
- совместимые родители дают challenger-child
- niche branch появляется по trigger

---

## PART 14 — Extinction Memory + Curriculum + Selection Gates

### Scope
- anti-pattern memory
- curriculum queue
- soft selection
- hard selection
- family rebalance cadence
- keep-alive logic

### Target LOC
`4000–5000`

### Acceptance
- watchlist/quarantine/rehabilitation работают
- anti-pattern penalty участвует в routing

---

## PART 15 — Skill Foundry + Research Augmentation

### Scope
- foundry pipelines
- research retriever / ranker / synthesizer
- source policy enforcement
- candidate generation from empty isolated outcomes

### Target LOC
`5000–6000`

### Acceptance
- foundry может выпустить candidate skill package
- source deny/allow работает строго

---

## PART 16 — Forward Arena + Lab Workers

### Scope
- baseline/challenger/niche/zero-skill workers
- scheduler
- virtual fill lane
- demo mirror lane
- promotion controller

### Target LOC
`5000–6000`

### Acceptance
- lab workers гоняют кейсы автономно
- arena получает результаты

---

## PART 17 — Overlay Registry + Human/Autonomy Controls + Reporting

### Scope
- overlay registry
- overlay lineage
- human autonomy matrix bindings
- reports / summaries / admin views

### Target LOC
`3500–5000`

### Acceptance
- overlays materialize only on next session
- human intervention zones видны в reports

---

## PART 18 — Tests + Fixtures + Integration Glue

### Scope
- smoke tests
- repository tests
- phenotype tests
- routing tests
- mutation gate tests
- integration wiring

### Target LOC
`4000–6000`

### Acceptance
- ключевые модули покрыты тестами
- проект может пройти базовый CI

---

## Итог

После выполнения PART 18:
- кодовая база должна покрывать не менее `80%` спецификации;
- оставшийся `%` должен быть только в advanced polish, а не в фундаменте.
