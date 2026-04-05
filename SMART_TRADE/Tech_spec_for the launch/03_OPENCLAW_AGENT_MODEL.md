# 03_OPENCLAW_AGENT_MODEL

## Назначение

Этот файл фиксирует:

- **какие OpenClaw-агенты нужны под SMART_TRADE**;
- **сколько их должно быть**;
- **за какие контуры они отвечают**;
- **какие bootstrap/workspace файлы должны быть у каждого типа агента**;
- **как выглядит запуск и взаимодействие агентов**.

Ключевой принцип:

> OpenClaw для SMART_TRADE = **агентная оболочка и раннер изолированных сессий**, а не хранилище истины.

SQLite, lineage, routing, promotion, mutation, phenotype и artifacts остаются внутри `SMART_TRADE`.

---

## Документы OpenClaw, которые нужно держать рядом

- [Agent Runtime](https://docs.openclaw.ai/concepts/agent)
- [Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace)
- [Skills](https://docs.openclaw.ai/skills)
- [Creating Skills](https://docs.openclaw.ai/tools/creating-skills)
- [Sub-Agents](https://docs.openclaw.ai/tools/subagents)
- [Hooks](https://docs.openclaw.ai/automation/)

Эти ссылки нужны не как source of truth проекта, а как reference по механике OpenClaw.

---

## 1. Общая карта агентов

### 1.1. Минимальный обязательный состав на 1 active `frame_shard`

#### Production контур
1. `prod_trader_agent` — `1`

#### LAB / arena контур
2. `lab_baseline_worker_agent` — `4`
3. `lab_challenger_worker_agent` — `4`
4. `lab_niche_worker_agent` — `2`
5. `lab_zero_skill_worker_agent` — `2`

#### Evolution контур
6. `evolver_generator_agent` — `1` logical role
7. `evolver_skeptic_agent` — `1` logical role
8. `evolver_arbiter_agent` — `1` logical role

#### Foundry / Research контур
9. `skill_foundry_agent` — `1`
10. `research_agent` — `1`

#### Optional later
11. `overlay_optimizer_agent` — `1` (выключен по умолчанию)

### 1.2. Что это значит по факту

Минимально одновременно в системе есть:

- `1` production trader
- `12` lab workers
- `3` evolver committee roles
- `1` foundry
- `1` research

Итого:

> **18 агентных ролей на один active frame_shard**

Важно:

- lab workers — это **реальные параллельные worker-сессии**;
- evolver committee роли можно держать как:
  - три отдельных agent profile,
  - или один profile с тремя разными isolated sessions.

Для воспроизводимости я рекомендую **раздельные agent profile**.

---

## 2. Зачем столько агентов

Потому что у нас есть четыре принципиально разные работы:

1. **дать сигнал**
2. **проверить и сравнить skill**
3. **эволюционировать skill**
4. **генерировать новые skill families**

Если всё это засунуть в одного агента, получится классическая человеческая система:

- сначала придумал,
- потом сам себя оправдал,
- потом сам себя продвинул,
- потом назвал это “обучением”.

Нам такое не нужно.

---

## 3. Роли агентов по контурам

## 3.1. `prod_trader_agent`

### Профессия

**Торговый агент production-контура**

### Что делает

- получает `FRAME`;
- получает materialized runtime skills;
- получает overlays;
- строит `trade_plan`;
- строит `trade_thesis_snapshot`;
- отправляет сигнал в `submit_trade_plan`;
- завершает сессию.

### Чего не делает

- не ждёт закрытия сделки;
- не мутирует skill;
- не делает promotion;
- не создаёт новые skill;
- не пишет в canonical registry.

### Сколько

- `1` на `frame_shard`

### Тип запуска

- по команде оператора / внешнего планировщика

---

## 3.2. `lab_baseline_worker_agent`

### Профессия

**Фоновый baseline-трейдер для арены**

### Что делает

- запускает champion-линии на потоке lab-кейсов;
- держит актуальный baseline performance;
- нужен для сравнения challengers и niche-линий.

### Чего не делает

- не мутирует skill;
- не принимает promotion decision.

### Сколько

- `4`

---

## 3.3. `lab_challenger_worker_agent`

### Профессия

**Фоновый тестировщик challenger skill versions**

### Что делает

- гоняет candidate/challenger versions;
- пишет `trade_plan`, `thesis_snapshot`, outcomes;
- кормит arena.

### Сколько

- `4`

---

## 3.4. `lab_niche_worker_agent`

### Профессия

**Фоновый тестировщик niche-веток**

### Что делает

- гоняет skill lines, живущие в узких phenotype buckets;
- помогает не убивать узких специалистов;
- даёт данные для `niche_registry`.

### Сколько

- `2`

---

## 3.5. `lab_zero_skill_worker_agent`

### Профессия

**Чистый агент без trading skill для isolated-песочницы**

### Что делает

- работает в `ISOLATED` + пустая skill-папка;
- получает только протокольные навыки;
- пытается генерировать сигнал без заранее навязанной методики;
- оставляет сырой материал для Foundry.

### Чего не знает

- не знает demo/live;
- не знает капитал;
- не знает “какой способ анализа правильный”.

### Сколько

- `2`

### Где использовать

- только в LAB, не в production по умолчанию.

---

## 3.6. `evolver_generator_agent`

### Профессия

**Первая линия эволюции: генерирует гипотезу улучшения**

### Что делает

- читает case bundle;
- читает fault graph;
- читает reflection capsules;
- строит:
  - mutation hypothesis
  - recombination hypothesis
  - speciation hypothesis
  - decomposition hypothesis

### Сколько

- `1` logical role

---

## 3.7. `evolver_skeptic_agent`

### Профессия

**Скептик эволюции**

### Что делает

- ищет, где hypothesis слаба;
- ищет leakage, self-justification, protocol conflicts;
- режет плохие мутации до того, как они попадут в validator.

### Сколько

- `1` logical role

---

## 3.8. `evolver_arbiter_agent`

### Профессия

**Арбитр эволюции**

### Что делает

- получает output generator + skeptic;
- выносит итоговый structured verdict;
- разрешает:
  - mutate
  - recombine
  - branch
  - decompose
  - no-op

### Сколько

- `1` logical role

---

## 3.9. `skill_foundry_agent`

### Профессия

**Фабрика новых skill families**

### Что делает

- смотрит isolated-zero кейсы;
- смотрит extinction memory;
- смотрит reflection capsules;
- смотрит phenotype clusters;
- синтезирует новые skill family candidates.

### Сколько

- `1`

---

## 3.10. `research_agent`

### Профессия

**Исследовательский агент эволюционного контура**

### Что делает

- ищет данные только по allowlist source policy;
- собирает статьи / venue docs / market microstructure references;
- отдаёт evidence packages для evolver / foundry.

### Сколько

- `1`

---

## 3.11. `overlay_optimizer_agent` (optional)

### Профессия

**Оптимизатор overlays**

### Что делает

- улучшает `AGENTS.md` и `TOOLS.md` overlays;
- не трогает свободно `SOUL` и `IDENTITY`.

### Статус

- optional, выключен по умолчанию в MVP+.

---

## 4. Какой bootstrap/workspace stack у каждого агента

## 4.1. Базовый обязательный набор файлов

Для всех agent workspaces SMART_TRADE стандартизирует такой стек:

1. `AGENTS.md`
2. `SOUL.md`
3. `TOOLS.md`
4. `IDENTITY.md`
5. `USER.md`
6. `HEARTBEAT.md`
7. `BOOTSTRAP.md` (одноразовый / optional after first run)

### Почему так

Официальные документы OpenClaw явно опираются как минимум на:
- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `BOOTSTRAP.md`

Но для SMART_TRADE нужен более жёсткий, управляемый стек. Поэтому мы фиксируем расширенный набор.

---

## 4.2. Роли файлов

### `AGENTS.md`
Операционные правила роли.

### `SOUL.md`
Persona, tone, behavioral limits.

### `TOOLS.md`
Краткие tool notes, порядок применения, ограничения.

### `IDENTITY.md`
Стабильная идентичность роли. Практически не мутирует.

### `USER.md`
Операторские предпочтения и приоритеты уровня пользователя.

### `HEARTBEAT.md`
Короткий operational heartbeat и последняя версия materialized overlays.

### `BOOTSTRAP.md`
Одноразовый файл для инициализации нового workspace / первого запуска.
После успешной materialization может быть очищен или помечен как consumed.

---

## 4.3. Что materialize-ится по ролям

| Агент | AGENTS | SOUL | TOOLS | IDENTITY | USER | HEARTBEAT | BOOTSTRAP |
|---|---|---|---|---|---|---|---|
| `prod_trader_agent` | да | да | да | да | да | да | optional |
| `lab_*_worker_agent` | да | да | да | да | да | да | optional |
| `evolver_*_agent` | да | да | да | да | да | да | optional |
| `skill_foundry_agent` | да | да | да | да | да | да | optional |
| `research_agent` | да | да | да | да | да | да | optional |
| `overlay_optimizer_agent` | да | да | да | да | да | да | optional |

---

## 4.4. Что разрешено мутировать из bootstrap stack

### Может эволюционировать ограниченно
- `AGENTS.md`
- `TOOLS.md`
- ограниченная часть `BOOTSTRAP.md`

### Почти фиксировано
- `SOUL.md`
- `IDENTITY.md`

### Не агент, а система может обновлять
- `HEARTBEAT.md`
- materialized markers

---

## 5. Процесс запуска агентов

## 5.1. Кто запускает

Не другие агенты, а:

# `SMART_TRADE orchestrator service`

Именно он решает:
- кого поднять;
- в каком workspace;
- с каким allowlist skill set;
- с каким overlay set;
- с каким model/thinking profile.

## 5.2. Почему не через prod trader

Потому что нельзя давать `prod_trader_agent` право быть диспетчером всей жизни системы. Он должен только давать сигнал.

---

## 5.3. Рекомендуемый порядок вызовов

### Production case

```text
orchestrator
-> materialize prod trader workspace
-> start prod_trader_agent new session
-> receive trade_plan + thesis
-> validate + submit to execution bridge
-> wait webhook
-> start evolver committee sessions
-> register results
```

### LAB case

```text
arena scheduler
-> choose worker lane
-> materialize worker workspace
-> start lab worker session
-> collect plan + thesis
-> virtual forward / demo mirror
-> webhook/result
-> evolution orchestrator
```

### Foundry case

```text
foundry scheduler
-> materialize foundry workspace
-> start skill_foundry_agent
-> receive candidate package
-> validate and register candidate
```

### Research case

```text
research scheduler
-> materialize research workspace
-> start research_agent
-> collect evidence pack
-> store citations + synthesis
```

---

## 6. Как именно использовать OpenClaw sub-agents

### Мой рекомендуемый режим

Sub-agents использовать **не в торговом runtime path**, а в:
- evolver committee
- research fan-out
- optional foundry decomposition tasks

### Почему

Потому что OpenClaw sub-agents уже умеют:
- isolated sessions;
- background runs;
- own model overrides.

Но торговый путь лучше запускать напрямую orchestrator-ом, а не изнутри другого агента.

---

## 7. Ключевые ограничения по видимости и правам

### `prod_trader_agent`

Видит:
- materialized runtime skills
- allowed tools
- current overlays
- frame-resolved context

Не видит:
- canonical SQLite
- full lineage tables
- source allowlist internals
- research archives
- live/demo switch
- capital/risk sizing

### `lab_worker_agents`

Видят то же, что и trader, но только внутри test/lab контуров.

### `evolver_*_agents`

Видят:
- case bundle
- lineage summaries
- phenotype data
- fault graph inputs
- anti-patterns
- candidate donor skills

Не видят:
- execution secrets
- direct capital layer

### `research_agent`

Видит:
- source policy
- research queues
- allowed domains

Не видит:
- execution tools
- live trading secrets

---

## 8. Что должно быть создано как отдельные OpenClaw-агенты в системе

Ниже итоговый список, который считаю каноническим.

### Обязательные profile IDs

```text
smarttrade.prod_trader
smarttrade.lab_baseline_worker
smarttrade.lab_challenger_worker
smarttrade.lab_niche_worker
smarttrade.lab_zero_worker
smarttrade.evolver_generator
smarttrade.evolver_skeptic
smarttrade.evolver_arbiter
smarttrade.skill_foundry
smarttrade.research
smarttrade.overlay_optimizer   # optional
```

### Recommended count per active frame_shard

| Agent profile | Количество |
|---|---:|
| `smarttrade.prod_trader` | 1 |
| `smarttrade.lab_baseline_worker` | 4 |
| `smarttrade.lab_challenger_worker` | 4 |
| `smarttrade.lab_niche_worker` | 2 |
| `smarttrade.lab_zero_worker` | 2 |
| `smarttrade.evolver_generator` | 1 |
| `smarttrade.evolver_skeptic` | 1 |
| `smarttrade.evolver_arbiter` | 1 |
| `smarttrade.skill_foundry` | 1 |
| `smarttrade.research` | 1 |
| `smarttrade.overlay_optimizer` | 1 optional |

---

## 9. Главное правило по OpenClaw-агентам

Все agent workspaces в SMART_TRADE — это:

> **materialized execution surfaces, а не source of truth**

То есть:
- skill registry живёт в SMART_TRADE;
- overlays живут в SMART_TRADE;
- lineage живёт в SMART_TRADE;
- OpenClaw получает только подготовленную копию на конкретный запуск.

Это главное условие, чтобы проект не расползся в человеческую привычку “поправим руками файлик в workspace и будем считать это архитектурой”.
