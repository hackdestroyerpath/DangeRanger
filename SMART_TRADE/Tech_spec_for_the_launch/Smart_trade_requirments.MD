# Smart_trade_requirments

## Назначение

Этот файл отвечает на практический вопрос:

> что именно должно быть установлено, настроено, подключено и поднято, чтобы после применения спецификации `SMART_TRADE` система могла стартовать и работать.

Здесь перечисляется именно **инфраструктурный и программный минимум**, а не логика проекта.

---

## 1. Обязательная инфраструктура

### 1.1. Оркестрационный хост / cluster

Нужен compute-контур, на котором поднимаются:

- `SMART_TRADE` backend
- `OpenClaw` runtime
- планировщик lab workers
- webhook receiver
- research jobs

Минимум для MVP на 1 active frame shard:

- 1 сервер backend
- 1 сервер / контейнер OpenClaw runtime
- 1 сервер / контейнер worker orchestration
- 1 сервер / контейнер reverse proxy + webhook ingress

При контейнеризации можно совместить, но логически это 4 слоя.

### 1.2. База данных

Обязательно:

- SQLite в canonical режиме (`WAL`)

Рекомендуется:
- отдельная директория под snapshots/backup
- автоматический backup rotation

### 1.3. Хранилище артефактов

Нужно файловое хранилище для:

- case artifacts
- materialized skills
- overlays
- mutation notes
- reports
- research evidence packages

Минимум: обычная файловая система.
Лучше: выделенный volume / object storage mirror.

### 1.4. Внешний торговый исполнительный контур

Нужен отдельный execution bridge, подключённый к:

- Binance API (demo / mirror / real)
- либо к твоему внутреннему исполнителю

SMART_TRADE сам не должен напрямую жить внутри биржевого SDK-слоя.

### 1.5. Live market data feed

Нужен поток рыночных данных для:

- runtime решений
- phenotype probe
- virtual forward arena
- post-trade counterfactual replay

Источники:
- websocket / streaming feed
- historical short rolling cache
- orderbook / trades / candles, в зависимости от реализованного покрытия

---

## 2. Обязательные программные контуры

## 2.1. OpenClaw

Обязательно:

- установленный OpenClaw runtime
- доступ к workspace-механике
- skills loader
- запуск изолированных agent sessions
- hooks / webhooks / sub-agents

Нужно уметь: 
- materialize workspace
- materialize skills
- запускать `prod_trader_agent`, `lab_*`, `evolver`, `foundry`, `research`

## 2.2. SMART_TRADE backend

Должен существовать отдельный backend / service layer, реализующий:

- frame engine
- case runtime
- execution bridge integration
- webhook ingestion
- case memory
- expectancy monitor
- evolution kernel
- skill registry
- research augmentation
- tool quality and coverage monitor

## 2.3. Scheduler / job orchestration

Нужен отдельный контур для:

- планирования lab workers
- периодического family rebalance
- research jobs
- evolution jobs
- retry jobs
- cleanup / archive jobs

Это может быть:
- встроенный async scheduler
- task queue
- job runner

Но контур обязан существовать явно.

---

## 3. Обязательные data parsers / providers

Ниже минимальный список того, что должно существовать, если проект реально должен “завестись”.

### 3.1. Candle provider
Подаёт:
- OHLCV
- быстрый lookback
- timeframe aggregation

### 3.2. Book / spread provider
Подаёт:
- spread
- top-of-book depth proxy
- liquidity thin/normal signals

### 3.3. Fill / execution telemetry provider
Подаёт:
- fill time
- timeout status
- cancel reason
- entry fill price
- close reason

### 3.4. Phenotype probe inputs
Минимально нужно, чтобы были доступны:
- candles
- ATR/volatility base
- spread
- liquidity proxy
- time/session bucket

### 3.5. Counterfactual replay inputs
Нужно хранить:
- рыночную траекторию после сигнала
- mark/last path (на выбор, но фиксировать единый источник)
- timeout and fill history

Без этого `Counterfactual Parameter Mutator` не будет работать.

---

## 4. Обязательные программы / библиотеки / контуры

Ниже не конкретные pinned версии, а обязательные классы зависимостей.

### 4.1. Python backend stack
Нужно:
- Python runtime
- SQLite driver
- HTTP server / API framework
- async scheduler / worker framework
- JSON schema validation
- filesystem artifact manager

### 4.2. LLM connectivity
Нужен рабочий контур вызова LLM с доступом к:
- strong model для runtime и evolver
- structured output / JSON mode
- retries + audit logging

### 4.3. Web / research tooling
Нужно:
- браузерный/search-контур для research_agent
- enforceable allowlist source policy
- retrieval + ranking + synthesis pipeline

### 4.4. Execution integration
Нужен:
- HTTP/WebSocket client to exchange or bridge
- idempotent order submit
- webhook receiver
- signature validation

---

## 5. Обязательные файлы / bootstrap surface для OpenClaw агентов

Для каждого materialized agent workspace должны существовать:

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (при первом запуске / reset)

Важно: эти файлы должны **создаваться и обновляться из SMART_TRADE registry**, а не быть ручной истиной.

---

## 6. Обязательные агентные роли

На 1 active frame shard должны существовать:

### Production
- `prod_trader_agent` — 1

### LAB
- `lab_baseline_worker_agent` — 4
- `lab_challenger_worker_agent` — 4
- `lab_niche_worker_agent` — 2
- `lab_zero_skill_worker_agent` — 2

### Evolution
- `evolver_generator_agent` — 1
- `evolver_skeptic_agent` — 1
- `evolver_arbiter_agent` — 1

### Growth / support
- `skill_foundry_agent` — 1
- `research_agent` — 1

Итого: **18 агентных ролей** на shard, если считать логические роли evolver отдельно.

---

## 7. Обязательные настройки и секреты

### 7.1. Execution secrets

Нужно настроить:
- exchange API credentials
- webhook shared secrets / signatures
- routing endpoints

### 7.2. LLM secrets

Нужны:
- API ключи моделей
- лимиты
- fallback policy

### 7.3. Source policy config

Нужно задать:
- allowlist domains
- denylist domains
- freshness date
- source tiers

### 7.4. OpenClaw runtime config

Нужно задать:
- base workspaces
- agent IDs
- skill directories
- session spawning policy
- hooks/webhooks routes

---

## 8. Что должно существовать как отдельные сервисы / модули

Минимальный список:

1. `frame_engine`
2. `runtime_core`
3. `execution_bridge`
4. `webhook_receiver`
5. `case_memory`
6. `expectancy_monitor`
7. `skill_registry`
8. `phenotype engine`
9. `arena`
10. `fault_graph`
11. `extinction_memory`
12. `mutation engine`
13. `recombination engine`
14. `decomposition engine`
15. `skill foundry`
16. `research augmentation`
17. `tool quality and coverage monitor`
18. `openclaw_bridge`

Если хотя бы одного из этих блоков нет, система уже не является полной реализацией `SMART_TRADE`.

---

## 9. Минимальный путь “нажал старт — заработало”

Чтобы проект реально “завёлся”, должно быть выполнено всё ниже:

### Шаг 1
Поднят `SMART_TRADE backend`

### Шаг 2
Инициализирован SQLite schema

### Шаг 3
Поднят `OpenClaw runtime`

### Шаг 4
Созданы agent profiles и workspace templates

### Шаг 5
Настроены execution secrets и webhook route

### Шаг 6
Подключены хотя бы минимальные data providers:
- candles
- spread/liquidity proxy
- execution telemetry

### Шаг 7
Загружены canonical configs:
- `project.yaml`
- `frame.yaml`
- `llm.yaml`
- `source_policy.yaml`

### Шаг 8
Сгенерированы materialized bootstrap files для агентов

### Шаг 9
Запущены:
- 1 prod trader
- 12 lab workers
- evolver committee
- foundry
- research

### Шаг 10
Запущен orchestration loop:
- case intake
- trade run
- webhook ingest
- evolution
- arena routing

После этого система может считаться operational.

---

## 10. Что не является “инфраструктурой”, но обязательно для запуска

Это не серверы, но без этого проект не работоспособен:

- materialized skill families
- protocol skills
- overlays
- `FRAME.MD` or frame generation pipeline
- source policy
- routing defaults
- skill registry seed

То есть “поднять сервер” недостаточно.
Нужен ещё **содержательный bootstrap проекта**.

---

## 11. Финальный вывод

Чтобы `SMART_TRADE` реально заработал, мало просто написать код и положить markdown-файлы агентам.

Нужны одновременно:

1. backend-сервисы
2. SQLite и артефактное хранилище
3. OpenClaw runtime и materialized workspaces
4. data parsers / providers
5. execution bridge
6. webhook ingress
7. evolver / foundry / research / arena loops
8. конфиги и secrets
9. bootstrap-файлы агентов

Только после этого можно считать, что ты “нажал старт” и система реально в состоянии работать.
