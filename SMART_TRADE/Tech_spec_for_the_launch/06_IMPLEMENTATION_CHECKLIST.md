# 06_IMPLEMENTATION_CHECKLIST

## Назначение

Это короткий operational checklist для команды разработки.

Его задача:
- не объяснять архитектуру с нуля;
- а ежедневно проверять, что проект собирается **по канонической спецификации**, а не “как получилось”.

Использовать только вместе с главным файлом:
- `01_SMART_TRADE_MASTER_SPEC_MAX.md`

---

## 0. Codex readiness

- [ ] Прочитан `12_CODEX_START_HERE.md`
- [ ] Выбрана конкретная часть из `13_CODEX_PARTITION_PLAN.md`
- [ ] Работа ведётся внутри `CODE_SKELETON_PACK/` и канонических директорий
- [ ] Будут обновлены `PART_STATUS.md`, `CHANGELOG.md`, `TODO.md`

---

# 1. Перед стартом кодинга

## 1.1. Убедиться, что зафиксированы инварианты

- [ ] `SMART_TRADE` = отдельный кодовый контур
- [ ] `OpenSpace` = только donor patterns
- [ ] `OpenClaw` = agent runtime shell
- [ ] `1 кейс = 1 сигнал = максимум 1 сделка`
- [ ] `NO_TRADE` в MVP отсутствует как пользовательское право
- [ ] агент не знает live/demo и капитал
- [ ] только limit-only + mandatory TP/SL
- [ ] пустой isolated agent не получает подсказку по методу

## 1.2. Убедиться, что есть единый источник истины

- [ ] SQLite выбран как canonical source
- [ ] workspace OpenClaw = materialized copy only
- [ ] lineage append-only
- [ ] outcome events идемпотентны
- [ ] frame_resolved.json = machine truth для кейса

---

# 2. Runtime core

## 2.1. Frame

- [ ] `FRAME.MD` парсится детерминированно + LLM normalization
- [ ] есть `frame_resolved.json`
- [ ] frame включает only environment + execution constraints
- [ ] frame не содержит arena / mutation / source-policy внутренних ручек

## 2.2. Session run

- [ ] каждый кейс стартует в новой OpenClaw-сессии
- [ ] `prod_trader_agent` завершает сессию сразу после:
  - сигнала
  - `trade_thesis_snapshot`
- [ ] нет hanging session до outcome

## 2.3. Trade plan

- [ ] агент всегда отдаёт machine-readable `trade_plan`
- [ ] `expected_fill_window_sec` обязателен
- [ ] `expected_fill_deadline` вычисляется системой
- [ ] валидатор проверяет только техническую корректность
- [ ] валидатор не судит о quality edge

## 2.4. Data requests

- [ ] есть один универсальный tool `request_market_data`
- [ ] `data_type` = свободная строка
- [ ] отсутствие покрытия -> `BLOCKED_BY_DATA_COVERAGE`
- [ ] coverage gap логируется как отдельный артефакт

---

# 3. Execution bridge и outcome

## 3.1. Execution bridge

- [ ] submit ордера идемпотентен
- [ ] `entry_timeout_sec` применяется только к неисполненной заявке
- [ ] позиция после fill не закрывается автоматически по timeout
- [ ] `OPERATOR_INTERVENED` поддержан

## 3.2. Outcome ingestion

- [ ] webhook ingestion идемпотентен
- [ ] outcome codes ограничены каноническим набором
- [ ] official expectancy считает только `TP_HIT` и `SL_HIT`
- [ ] остальные terminal codes не попадают в official expectancy

---

# 4. Skill registry

## 4.1. Основные сущности

- [ ] есть `skill_family`
- [ ] есть `branch`
- [ ] есть `skill_version`
- [ ] есть `gene_block`
- [ ] есть `phenotype_key`

## 4.2. Materialization

- [ ] materialization идёт через `openclaw_bridge`
- [ ] agent не читает canonical registry напрямую
- [ ] `EXPLICIT`, `AUTO`, `ISOLATED` реализованы раздельно
- [ ] `ISOLATED + empty` не падает

## 4.3. Packaging

- [ ] каждая версия skill имеет:
  - `SKILL.md`
  - `contract.json`
  - `gene_map.json`
  - `phenotype_scope.json`
  - `mutation_note.md`
  - `references/`

---

# 5. Phenotype

## 5.1. До сделки

- [ ] есть `pretrade_probe`
- [ ] agent не видит phenotype напрямую
- [ ] phenotype влияет на routing, но не на подсказку пустому агенту

## 5.2. После сделки

- [ ] есть `posttrade_regime_tagger`
- [ ] posttrade phenotype может уточнять pretrade phenotype
- [ ] phenotype bucket используется в arena и speciation

---

# 6. Arena

## 6.1. Общая логика

- [ ] `sandbox` ≠ `tester` ≠ `arena`
- [ ] arena работает в рамках `frame_shard + phenotype bucket`
- [ ] routing bounded:
  - `max_weight_per_skill`
  - `keep_alive_floor`
  - `sandbox_cap`

## 6.2. Метрики

- [ ] считается `arena_score`
- [ ] считается `family_score`
- [ ] есть `fill_rate`, `timeout_rate`, `invalid_rate`, `freshness`, `stability`, `pain`
- [ ] routing строится не только на одном `E_R`

## 6.3. Статусы

- [ ] поддержаны `CHAMPION/CHALLENGER/NICHE/WATCHLIST/QUARANTINED/RETIRED`
- [ ] promotion / demotion пишет историю в SQLite

---

# 7. Evolution core

## 7.1. Порядок after-terminal pipeline

- [ ] append_trade_record
- [ ] recompute rolling windows
- [ ] protocol integrity gate
- [ ] hard selection gate
- [ ] regime shift gate
- [ ] soft selection gate
- [ ] local mutation gate
- [ ] recombination gate
- [ ] routing rebalance
- [ ] lineage writeback
- [ ] cooldown update

## 7.2. Fault graph

- [ ] fault graph выдаёт `primary_fault_gene`
- [ ] есть tie-breaker только при ambiguity
- [ ] infrastructure failure не превращается в skill mutation

## 7.3. Local mutation

- [ ] правило `1 child / 1 gene block / 1 generation`
- [ ] mutation order: parameters -> filters -> features -> structure
- [ ] mutation не запускается без нужной статистики

## 7.4. Recombination

- [ ] recombination only after gate
- [ ] same frame_shard
- [ ] same contract_version
- [ ] `similarity < 0.80`
- [ ] weak × weak запрещено

## 7.5. Speciation / Decomposition

- [ ] niche branches рождаются из phenotype divergence
- [ ] decomposition только после repeated failed local mutations

## 7.6. Memory modules

- [ ] `reflection_capsules`
- [ ] `extinction_memory`
- [ ] `curriculum_queue`

---

# 8. Agents and OpenClaw runtime

## 8.1. Agent roster exists

- [ ] `prod_trader_agent`
- [ ] `lab_baseline_worker_agent`
- [ ] `lab_challenger_worker_agent`
- [ ] `lab_niche_worker_agent`
- [ ] `lab_zero_skill_worker_agent`
- [ ] `evolver_generator_agent`
- [ ] `evolver_skeptic_agent`
- [ ] `evolver_arbiter_agent`
- [ ] `skill_foundry_agent`
- [ ] `research_agent`

## 8.2. Workspace files exist per agent

- [ ] `AGENTS.md`
- [ ] `SOUL.md`
- [ ] `TOOLS.md`
- [ ] `IDENTITY.md`
- [ ] `USER.md`
- [ ] `HEARTBEAT.md`
- [ ] `BOOTSTRAP.md`

## 8.3. Visibility and rights

- [ ] prod trader не пишет в canonical registry
- [ ] evolver читает case bundle, а не raw secrets
- [ ] research agent не имеет execution tools
- [ ] overlays вступают в силу только на новой сессии

---

# 9. LLM usage

## 9.1. Mandatory workflows in place

- [ ] frame_normalizer
- [ ] auto_skill_selector
- [ ] trade_plan_synthesis
- [ ] thesis_snapshot
- [ ] outcome_analyzer
- [ ] critic
- [ ] skeptic
- [ ] arbiter
- [ ] rewrite
- [ ] promotion_committee
- [ ] foundry_synthesis
- [ ] research_synthesis

## 9.2. Deterministic ownership preserved

- [ ] protocol validation deterministic
- [ ] DB writes deterministic
- [ ] execution submission deterministic
- [ ] timeout logic deterministic
- [ ] security deterministic

---

# 10. Research and source policy

- [ ] allowlist domains enforced
- [ ] denylist enforced
- [ ] research only affects evolver/foundry/overlay optimizer
- [ ] research does not leak method hints into empty isolated runtime
- [ ] citations / hashes are stored

---

# 11. Security and secrets

- [ ] secrets не лежат в spec artifacts
- [ ] secrets не лежат в skills
- [ ] secrets не лежат в SQLite в открытом виде
- [ ] agent workspaces isolated
- [ ] no direct agent writes to canonical registry

---

# 12. Acceptance smoke-check before “done”

Считать релиз кандидатным только если можно ответить “да” на всё:

- [ ] можно поднять новый кейс из `FRAME.MD`
- [ ] empty isolated не получает подсказки и не падает
- [ ] валидный сигнал доходит до execution bridge
- [ ] invalid signal не доходит до bridge
- [ ] outcome корректно возвращается в case
- [ ] official expectancy пересчитывается
- [ ] fault graph срабатывает
- [ ] candidate skill может быть выпущен
- [ ] arena назначает champion/challenger
- [ ] lineage append-only
- [ ] rebuild case from DB + artifacts возможен
- [ ] production lane отделён от lab lane

---

# 13. Главный критерий успеха

Если после чтения этого checklist разработчик начинает писать код “как удобно”, а не “как здесь зафиксировано”, значит checklist не выполняет свою работу.

Он должен использоваться буквально:
- при проектировании модулей;
- при PR review;
- при integration review;
- при pre-release проверке.


## 0.5 Environment preflight

- [ ] Прочитан `17_EXECUTION_BRIDGE_CONTRACT.md`
- [ ] Прочитан `18_MARKET_DATA_PROVIDER_PROFILE.md`
- [ ] Прочитан `19_OPENCLAW_RUNTIME_PROFILE.md`
- [ ] Зафиксирован baseline из `20_PRODUCTION_BASELINE.md`
- [ ] Зафиксирован источник истины цены из `21_PRICE_TRUTH_POLICY.md`
- [ ] Создан `.env` по `22_ENV_CONTRACT.md`
- [ ] Прочитан `23_PROD_PILOT_ACCEPTANCE.md`
