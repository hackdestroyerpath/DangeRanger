# 02_OPENSPACE_DONOR_MAP

## Назначение

Этот файл фиксирует, **какие части OpenSpace допустимо брать за основу**, что именно у них копировать/адаптировать, и что **нельзя переносить один в один** в `SMART_TRADE`.

Ключевой принцип:

- OpenSpace = **донор архитектуры и некоторых модулей**
- SMART_TRADE = **самостоятельная кодовая система**
- переносить надо **паттерн и каркас**, а не слепо тащить семантику “обычной задачи” в торговый контур

---

## 1. Главные точки в OpenSpace, которые нужно изучить

### 1.1. Главный README
- [`README.md`](https://github.com/HKUDS/OpenSpace/blob/main/README.md)

Зачем:
- общая модель self-evolving skill system
- storage, lineage, cloud/local skill workflow
- high-level разделение skill-engine и quality layer

### 1.2. Post-run orchestration
- [`openspace/tool_layer.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/tool_layer.py)

Ключевые вещи для нас:
- последовательность после `execute()`
- `_maybe_analyze_execution()`
- `_maybe_evolve_quality()`
- фоновый запуск `process_tool_degradation()` и `process_metric_check()`
- идея: не всё происходит в главном потоке ответа, часть идёт после завершения кейса

Что брать:
- паттерн разделения runtime и post-analysis
- паттерн “после terminal outcome запускаются ветки анализа и эволюции”
- паттерн фоновых evolution jobs

Что НЕ брать как есть:
- общую семантику “task completed” как финальную truth-метрику
- привязку к generic task lifecycle без торговой state machine

### 1.3. Execution analyzer
- [`openspace/skill_engine/analyzer.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/skill_engine/analyzer.py)

Что брать:
- сбор execution context из артефактов
- построение большого аналитического context bundle
- iterative analysis loop
- фиксацию `tool_issues`, `skill_judgments`, `evolution_suggestions`

Что адаптировать:
- вместо generic execution context -> `trade case bundle`
- вместо `task_completed` -> торговые terminal outcomes + protocol statuses
- вместо generic skills -> trade skill families / branches / versions

### 1.4. Skill evolver
- [`openspace/skill_engine/evolver.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/skill_engine/evolver.py)

Что брать:
- триггеры `process_analysis`, `process_tool_degradation`, `process_metric_check`
- `_llm_confirm_evolution()` как идею дополнительного допуска к эволюции
- `_evolve_fix`, `_evolve_derived`, `_evolve_captured`
- retry/apply loop
- background task scheduler

Что адаптировать:
- `FIX` -> локальная починка gene block / repair child
- `DERIVED` -> niche/speciation branch
- `CAPTURED` -> Foundry-created reusable trading skill
- добавить `RECOMBINATION` и `DECOMPOSITION`
- адаптировать триггеры не к generic completion rate, а к expectancy / phenotype / routing

### 1.5. Skill store и типы
- [`openspace/skill_engine/store.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/skill_engine/store.py)
- [`openspace/skill_engine/types.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/skill_engine/types.py)

Что брать:
- persistent skill store
- append-only analysis records
- lineage-like модель и счётчики skill usage
- метрики на уровне skill records

Что адаптировать:
- skill metrics должны считаться на `realized_R`, `E30/E100`, `PF`, `fill_rate`, `timeout_rate`, `phenotype fit`
- вместо generic `total_completions`/`task_completed` использовать официальные terminal outcomes
- добавить family-level и phenotype-level aggregates

### 1.6. Prompt templates
- [`openspace/prompts/skill_engine_prompts.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/prompts/skill_engine_prompts.py)

Что брать:
- separation of analysis prompt / confirm prompt / evolve prompts
- idea of exact JSON schema output
- discipline of `critic-like` and `rewrite-like` prompting

Что адаптировать:
- все prompt schemas под trade cases
- explicit blame by gene block
- phenotype-aware mutation rationale
- routing / promotion decisions for arena

### 1.7. Tool quality
- [`openspace/grounding/core/quality/manager.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/grounding/core/quality/manager.py)
- [`openspace/grounding/core/quality/types.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/grounding/core/quality/types.py)
- [`openspace/grounding/core/grounding_client.py`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/grounding/core/grounding_client.py)

Что брать:
- отдельную линию качества инструментов
- хранение recent execution history
- поиск problematic tools
- semantic LLM feedback on tools

Что адаптировать:
- quality events не должны напрямую мутировать trade skills без integrity gate
- coverage gaps / parser failures / execution bridge failures должны идти в отдельный infra track
- торговый skill мутирует только если проблема не инфраструктурная

### 1.8. OpenClaw host integration path
- [`openspace/host_skills/README.md`](https://github.com/HKUDS/OpenSpace/blob/main/openspace/host_skills/README.md)

Что брать:
- общий принцип: OpenSpace-like system можно встраивать в агентный runtime через host skills / delegated flows
- идея отдельного delegate tool или внешнего engine

Что адаптировать:
- SMART_TRADE не должен растворяться в host skill; наоборот, OpenClaw для нас — оболочка и runner

---

## 2. Что можно копировать почти напрямую

Ниже блоки, которые допустимо взять почти как инженерный каркас с последующей адаптацией имён и структур.

### 2.1. Паттерн `runtime -> analyzer -> evolver -> monitor`
Можно копировать как архитектурный backbone.

### 2.2. Append-only lineage / analysis records
Можно копировать идею immutable history.

### 2.3. Background evolution jobs
Можно копировать модель, где mutation/monitor jobs идут вне основного user-facing ответа.

### 2.4. Quality manager separation
Можно копировать сам факт наличия отдельного tool quality слоя.

### 2.5. Prompt separation
Можно копировать разделение на:
- analyze
- confirm
- evolve
- validate

---

## 3. Что брать только как идею, но не копировать кодом

### 3.1. `task_completed`
В OpenSpace это нормальная generic сущность.

В SMART_TRADE это **нельзя использовать как центральную truth-метрику**, потому что:
- у нас есть `TP_HIT`, `SL_HIT`, `PLAN_INVALID`, `ORDER_CANCELLED_TIMEOUT`, `BLOCKED_BY_DATA_COVERAGE`, `OPERATOR_INTERVENED`
- торговый кейс не сводится к бинарному “выполнено/не выполнено”

### 3.2. `selected skills by LLM` как абсолютная истина
В OpenSpace skill selection допустимо строить по generic task relevance.

В SMART_TRADE selection должен быть bounded:
- frame
- phenotype
- arena routing
- explicit/auto/isolated mode

### 3.3. Generic metric monitor thresholds
В OpenSpace thresholds можно брать мягче.

В SMART_TRADE thresholds обязаны быть привязаны к:
- official case count
- phenotype bucket size
- expectancy windows
- family-relative performance

---

## 4. Что надо добавить сверху OpenSpace-паттерна, потому что у них этого нет

Это важно: в SMART_TRADE есть ключевые вещи, которых в OpenSpace нет как готовых элементов.

### 4.1. `frame_shard`-изоляция
OpenSpace не строился вокруг торговых frame-shard с независимой популяцией skill lines.

### 4.2. `arena_score` / `family_score`
OpenSpace не делает полноценную skill-population routing arena для торгового сигнала.

### 4.3. `Champion–Challenger Live Arena`
Это наш отдельный слой.

### 4.4. `Counterfactual Parameter Mutator`
В таком виде в OpenSpace нет.

### 4.5. `Causal Fault Graph` по gene blocks
Нужно строить отдельно.

### 4.6. `Extinction Memory`
Анти-паттерны на уровне trade setups — это уже специфически наш слой.

### 4.7. `Skill Foundry`
Генерация skill families из накопленного trade experience в OpenSpace нет как отдельного полноценного направления.

### 4.8. Overlay registry
Ограниченно эволюционируемые `AGENTS/TOOLS/BOOTSTRAP` overlays — тоже наш слой.

---

## 5. Практическая карта копирования

| SMART_TRADE блок | Ближайший аналог в OpenSpace | Статус переноса |
|---|---|---|
| `case post-analysis` | `analyzer.py` | взять паттерн, переписать семантику |
| `mutation orchestration` | `evolver.py` | взять каркас, расширить типы |
| `skill persistence` | `store.py` | взять идею и sqlite-паттерн |
| `skill metrics` | `types.py` | переписать под trade metrics |
| `tool quality monitor` | `quality/manager.py` | взять как отдельный infra layer |
| `prompt discipline` | `skill_engine_prompts.py` | взять структуру, переписать смыслы |
| `OpenClaw bridge concept` | `host_skills/README.md` | взять как идею, не как прямую реализацию |

---

## 6. Главная защита от ошибки “перепутать OpenSpace и SMART_TRADE”

Нельзя говорить программистам:

> “берите OpenSpace и допишите трейдинг сверху”

Правильно говорить так:

> “берём из OpenSpace только проверенные формы самоанализа, skill lineage, evolution orchestration и tool quality separation; торговый runtime, frame engine, arena, phenotype, expectancy и execution bridge строим сами”

Иначе они очень быстро начнут прикручивать generic `task_completed` к скальпингу, а это уже прямое приглашение к боли.
