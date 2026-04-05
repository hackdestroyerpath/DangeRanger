## 0. Назначение документа

Этот файл — **каноническая спецификация MAX-approved scope `SMART_TRADE`**.
Он включает ядро MVP **и все дополнительные функции, которые были обсуждены и утверждены**.  
Он задаёт:

- неизменяемые правила проекта;
- состав модулей;
- контракты данных;
- жизненный цикл кейса;
- формулы;
- параметры;
- места вызова LLM;
- правила эволюции навыков;
- структуру БД;
- структуру каталогов;
- порядок написания кода.

Если реализация расходится с этим файлом — реализация считается неправильной.

---


## 0.1. Companion docs пакета

Этот файл — главный. Дополняющие документы пакета:

- `02_OPENSPACE_DONOR_MAP.md` — точная карта, какие блоки брать из OpenSpace и откуда
- `03_OPENCLAW_AGENT_MODEL.md` — полный состав агентов, их роли, bootstrap-файлы и контуры вызова
- `04_LLM_CALL_MATRIX.md` — матрица LLM-вызовов по агентам и workflows
- `05_HUMAN_AUTONOMY_MATRIX.md` — где обязателен человек, а где всё автономно
- `06_IMPLEMENTATION_CHECKLIST.md` — короткий ежедневный checklist разработчиков
- `07_AGENT_BOOTSTRAP_TEMPLATES.md` — шаблоны bootstrap/workspace-файлов агентов
- `Smart_trade_requirments.MD` — обязательная инфраструктура, программы, парсеры и порядок запуска
- `08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL.md` — полный формальный разбор отношения phenotype ↔ skill family ↔ branch ↔ recombination
- `09_RESTORE_FROM_ZERO_AUDIT.md` — аудит полноты пакета для восстановления проекта 1:1
- `10_FEATURE_COVERAGE_MATRIX.md` — матрица покрытия всех утверждённых фич и решений
- `11_MAX_APPROVED_FEATURE_APPENDIX.md` — финальные max-approved уточнения из последних согласований
- `12_CODEX_START_HERE.md` — стартовый файл для работы Codex
- `13_CODEX_PARTITION_PLAN.md` — разбивка проекта на части под Codex
- `14_CODEX_EXECUTION_PROTOCOL.md` — протокол выполнения частей Codex
- `CODE_SKELETON_PACK/README.md` — канонический skeleton-каркас проекта
- `examples/` — вынесенные кодовые и структурные примеры по разделам

Если companion docs противоречат главному файлу, приоритет у главного файла.

---

## 0.2. Codex-оптимизация пакета

Архив дополнительно оптимизирован под пошаговую реализацию через Codex.
Для этого обязательны:

- `12_CODEX_START_HERE.md`
- `13_CODEX_PARTITION_PLAN.md`
- `14_CODEX_EXECUTION_PROTOCOL.md`
- `CODE_SKELETON_PACK/`

Нормативное правило:
Codex не имеет права менять проектную логику или перестраивать архитектуру.
Он должен писать код только как исполнитель этой спецификации.

---

## 1. Объект проекта

`SMART_TRADE` — это контур **генерации, исполнения, учёта, анализа и эволюции торговых сигналов**.

Целевая функция проекта:

> **максимизация математического ожидания сигнала на дистанции внутри конкретного `frame`**

Проект не является системой управления капиталом.  
Проект не оптимизирует размер позиции.  
Проект не оптимизирует портфель.  
Проект оптимизирует только качество сигнала.

---

## 2. Неизменяемые правила

### 2.1. Архитектурные правила

1. `SMART_TRADE` пишется **с нуля**.
2. `OpenSpace` используется только как **донор архитектурных паттернов**.
3. `OpenClaw` используется как:
   - оболочка агента;
   - загрузчик навыков;
   - раннер сессий;
   - runtime-workspace;
   - транспорт hooks/webhooks/subagents.
4. Каноническая истина живёт **только внутри `SMART_TRADE`**:
   - SQLite
   - артефакты кейсов
   - реестр навыков
   - lineage
   - routing weights
   - overlays
5. Папки `skills/` внутри OpenClaw — только materialized runtime copy.

### 2.2. Торговые правила MVP

1. `1 кейс = 1 попытка дать 1 сигнал = максимум 1 сделка`
2. В `MVP` нет пользовательского смысла `NO_TRADE`.
3. В `MVP` есть только **технические терминальные статусы**.
4. Разрешены только **лимитные ордера**.
5. В каждой сделке обязательны:
   - `entry_limit`
   - `stop_loss`
   - `take_profit`
6. Частичные выходы, scale in/out, усреднение и ручное управление агентом открытой позицией в `MVP` не допускаются.
7. Таймаут относится **только к неисполненной заявке на вход**.
8. После открытия позиции она живёт до:
   - `TP_HIT`
   - `SL_HIT`
   - `OPERATOR_INTERVENED`
9. Агент не знает:
   - live/demo
   - размер позиции
   - капитал
   - денежный риск
10. Оператор может вручную вмешаться в уже открытую сделку; такие кейсы логируются, но не используются как жёсткая основа для эволюции.

### 2.3. Правило режима без навыка

Если режим `ISOLATED` активен и папка навыков пуста, агент:

- не получает никакой подсказки по способу генерации сигнала;
- не получает списка допустимых данных;
- не получает метода анализа;
- не получает направляющей схемы выбора данных.

Он знает только:

- как подать сигнал;
- в каком формате подать сигнал;
- что сигнал должен быть технически валиден.

---

## 3. Термины и иерархия

**Вынесенные примеры:** `examples/04_3_terminy_i_ierarkhiya.md`


### 3.1. Иерархия

[Кодовые примеры и схемы вынесены: `examples/04_3_terminy_i_ierarkhiya.md`]

### 3.2. Сущности

#### `frame_family`
Крупный класс среды.  
Пример: `binance_futures_1m`

#### `frame_shard`
Основная единица изоляции эволюции.  
Пример: `binance_futures_btcusdc_1m`

#### `skill_family`
Главная эволюционная линия.  
Пример: `Lite_TRADING_SKILL_01_04_2026`

#### `branch`
Ветка внутри skill family:
- `main`
- `repair_entry_branch`
- `range_branch`
- `trend_pullback_branch`

#### `skill_version`
Конкретная версия внутри ветки.  
Пример: `Lite_TRADING_SKILL_01_04_2026@main@v18`

#### `gene_block`
Минимальный эволюционный блок:
1. `idea_source_policy`
2. `data_request_policy`
3. `interpretation_policy`
4. `entry_policy`
5. `sl_policy`
6. `tp_policy`
7. `timeout_policy`
8. `eta_policy`
9. `output_discipline`

#### `phenotype`
Состояние рынка. Это **не skill**. Это ортогональная ось среды.  
Пример: `dir=up|vol=expansion|liq=thin|session=us`

#### `arena`
Логика сравнения версий навыков.

#### `sandbox`
Безопасная среда ограниченного case-flow.

#### `tester`
Исполнитель, который гоняет версии навыков внутри sandbox.

### 3.3. Правило терминологии

Термин **“схема”** не используется.  
Во всём проекте используется только термин **“навык / skill”**.

---

## 4. Роли OpenClaw и OpenSpace

### 4.1. Роль OpenClaw

OpenClaw используется как:

- агентная оболочка;
- session runtime;
- workspace manager;
- loader `SKILL.md`;
- hooks/webhooks/cron/subagents слой;
- транспорт до и от агента.

### 4.2. Роль OpenSpace

Из OpenSpace заимствуются паттерны:

- post-execution analysis;
- analyzer/evolver split;
- lineage;
- metric monitor;
- quality monitor;
- versioning;
- популяционная эволюция навыков;
- batch review после завершения задачи.

### 4.3. Собственный код SMART_TRADE

Своим кодом строятся:

- frame engine
- runtime core
- data routing
- signal contract
- execution bridge
- webhook receiver
- case memory
- expectancy monitor
- skill registry
- phenotype engine
- arena
- fault graph
- extinction memory
- mutation engine
- recombination engine
- decomposition engine
- skill foundry
- overlay registry
- research augmentation
- tool quality and coverage monitor

---

## 5. Конфигурация

**Вынесенные примеры:** `examples/06_5_konfiguratsiya.md`


### 5.1. Единое место конфигов

Все конфиги лежат в:

[Кодовые примеры и схемы вынесены: `examples/06_5_konfiguratsiya.md`]

### 5.2. Структура

[Кодовые примеры и схемы вынесены: `examples/06_5_konfiguratsiya.md`]

### 5.3. Приоритет конфигов

[Кодовые примеры и схемы вынесены: `examples/06_5_konfiguratsiya.md`]

### 5.4. Дефолтный frame MVP

[Кодовые примеры и схемы вынесены: `examples/06_5_konfiguratsiya.md`]

### 5.5. Что не должно быть в FRAME

В `FRAME` не должны находиться:

- split арены;
- веса routing;
- пороги promotion;
- пороги mutation;
- source allowlist;
- параметры decay;
- режимы quarantine/watchlist;
- lab workers.

Это серверная конфигурация, не пользовательская.

---

## 6. Frame: границы и granularity

**Вынесенные примеры:** `examples/07_6_frame_granitsy_i_granularity.md`


### 6.1. Каноническая единица frame

Для `MVP` канонический уровень изоляции:

> `exchange + market + symbol + timeframe + execution_rules`

Пример:

[Кодовые примеры и схемы вынесены: `examples/07_6_frame_granitsy_i_granularity.md`]

### 6.2. Почему именно так

Это минимизирует смешение:

- разных символов,
- разных таймфреймов,
- разных microstructure режимов.

### 6.3. Будущая расширяемость

Допускается двухуровневая модель:

- `frame_family_id`
- `frame_shard_id`

Но в `MVP` главным объектом учёта и эволюции является `frame_shard`.

---

## 7. Типы агентов и начальный парк

### 7.1. Обязательные агентные роли

1. `prod_trader_agent`
2. `lab_worker_agents`
3. `evolver_agent`
4. `skill_factory_agent`

### 7.2. Начальный объём lab workers

Начальное значение:

> **12 lab workers на один active frame_shard**

Разбивка:

- `4` baseline workers
- `4` challenger workers
- `2` niche workers
- `2` zero-skill isolated workers

### 7.3. Почему не больше на старте

Для одного `frame_shard` (BTCUSDC 1m) слишком большой парк workers даст:

- сильно коррелированные кейсы;
- лишний orchestration overhead;
- шум без прироста информации.

`12` — стартовый баланс между параллельностью и чистотой статистики.

### 7.4. Принцип масштабирования

После стабилизации можно масштабировать до `24` на shard, но не раньше, чем:

- работает deduplication;
- работает arena;
- корректно считаются phenotype buckets;
- case routing не конфликтует.

---

## 8. Сессии и рабочие пространства

### 8.1. Новая сделка = новая сессия

Каждый новый кейс запускается в новой OpenClaw-сессии.

### 8.2. Что делается в торговой сессии

В рамках одной сессии `prod_trader_agent` обязан:

1. получить `FRAME`
2. получить materialized skills + overlays
3. сгенерировать `trade_plan`
4. вызвать `submit_trade_plan`
5. записать `trade_thesis_snapshot`
6. завершить сессию

### 8.3. Чего НЕ делается в торговой сессии

В торговой сессии не делается:

- ожидание закрытия сделки;
- эволюция навыка;
- длительное hanging until outcome;
- promotion / demotion.

### 8.4. Кто делает пост-анализ

`evolver_agent` запускается отдельно после получения outcome hook.

---

## 9. Видимость навыков

### 9.1. Режим `EXPLICIT`

Агент видит только явно заданный skill family/version + протокольные навыки.

### 9.2. Режим `AUTO`

Агент видит отобранный системой набор skill families/versions, доступных в данном `frame_shard`.

### 9.3. Режим `ISOLATED`

Агент видит только навыки из указанной папки `skill_scope`.

### 9.4. `ISOLATED` + пустая папка

Агент:

- не видит торговых навыков;
- видит только протокольные навыки;
- может запуститься и выдать сигнал;
- не должен падать в ошибку только из-за отсутствия trading skills.

### 9.5. Протокольные навыки

Неэволюционируемые навыки:

- `smart_trade_protocol`
- `submit_signal_protocol`
- `execution_feedback_protocol`

Они объясняют:
- формат сигналов
- формат данных
- порядок записи артефактов
- обязательные поля

Они не содержат метода генерации сигнала.

---

## 10. Overlay Registry

### 10.1. Что разрешено эволюционировать

Ограниченно могут эволюционировать:

- `AGENTS` overlay
- `TOOLS` overlay
- `bootstrap` overlay

### 10.2. Что запрещено свободно эволюционировать

Практически фиксированы:

- `SOUL`
- `IDENTITY`

### 10.3. Почему

`SOUL` и `IDENTITY` влияют на стиль и личность, но не являются основным носителем trading edge.  
Свободная мутация этих файлов разрушит воспроизводимость.

### 10.4. Как это реализуется

Вводится `overlay_registry`, где версии overlay живут отдельно от runtime-workspace.

OpenClaw на старте сессии получает только approved overlay version.

---

## 11. Контракт запроса данных

**Вынесенные примеры:** `examples/12_11_kontrakt_zaprosa_dannykh.md`


### 11.1. Нужен один универсальный tool

В проекте используется один универсальный инструмент:

[Кодовые примеры и схемы вынесены: `examples/12_11_kontrakt_zaprosa_dannykh.md`]

### 11.2. Формат запроса

[Кодовые примеры и схемы вынесены: `examples/12_11_kontrakt_zaprosa_dannykh.md`]

### 11.3. Правила

- `data_type` — свободная строка;
- `params` — свободный словарь;
- агент не получает каталога доступных типов;
- маршрутизатор сам ищет обработчик.

### 11.4. Если покрытия нет

При отсутствии покрытия:

- кейс получает `BLOCKED_BY_DATA_COVERAGE`;
- создаётся `coverage_gap_artifact`;
- нормальная торговая эволюция по такому кейсу не запускается.

---

## 12. Контракт торгового плана

**Вынесенные примеры:** `examples/13_12_kontrakt_torgovogo_plana.md`


### 12.1. Агент обязан вернуть

[Кодовые примеры и схемы вынесены: `examples/13_12_kontrakt_torgovogo_plana.md`]

### 12.2. `expected_fill_window_sec`

Это поле **обязательно**.

Смысл:

- оценка ожидаемого времени исполнения лимитки;
- человеческий ориентир актуальности сигнала;
- вход для `eta_accuracy`;
- вход для counterfactual mutation.

Формат:

- целое число секунд
- `> 0`
- округление вверх до секунды

### 12.3. `expected_fill_deadline`

Это поле **не задаётся агентом**.

Оно вычисляется системой.

Финальная форма хранения:

[Кодовые примеры и схемы вынесены: `examples/13_12_kontrakt_torgovogo_plana.md`]

### Правило вычисления

[Кодовые примеры и схемы вынесены: `examples/13_12_kontrakt_torgovogo_plana.md`]

### Разница между полями

| Поле | Кто задаёт | Назначение |
|---|---|---|
| `expected_fill_window_sec` | агент | оценка нормального времени fill |
| `expected_fill_deadline_sec/ts` | система | жёсткий срок смерти заявки |

### Практический вывод

- `window` = обучаемая гипотеза
- `deadline` = системный kill-switch

---

## 13. Технический валидатор плана

### 13.1. Валидатор проверяет только форму и совместимость

Валидатор **не оценивает качество идеи**.

Он проверяет только:

1. наличие полей:
   - `entry_limit`
   - `stop_loss`
   - `take_profit`
2. корректность геометрии:
   - для `LONG`: `SL < entry < TP`
   - для `SHORT`: `TP < entry < SL`
3. `symbol` и `frame` consistency
4. limit-only compatibility
5. время генерации не старше системного порога
6. корректность типов и диапазонов
7. корректность `expected_fill_window_sec`

### 13.2. Что валидатор НЕ делает

Он не имеет права решать:

- хорошая это сделка или нет;
- сильный ли edge;
- стоило ли торговать.

---

## 14. Состояния и терминальные коды кейса

**Вынесенные примеры:** `examples/15_14_sostoyaniya_i_terminalnye_kody_keysa.md`


### 14.1. Основной state machine

[Кодовые примеры и схемы вынесены: `examples/15_14_sostoyaniya_i_terminalnye_kody_keysa.md`]

### 14.2. Терминальные коды

#### Торговые
- `TP_HIT`
- `SL_HIT`

#### Технические не-торговые
- `PLAN_NOT_SYNTHESIZED`
- `PLAN_INVALID`
- `BLOCKED_BY_DATA_COVERAGE`
- `EXECUTION_ABORTED`
- `ORDER_CANCELLED_TIMEOUT`

#### Операторские
- `OPERATOR_INTERVENED`

### 14.3. Что входит в official expectancy

Только:

- `TP_HIT`
- `SL_HIT`

Все остальные коды идут в:
- quality metrics
- coverage metrics
- execution metrics
- protocol metrics

---

## 15. Фенотип рынка

**Вынесенные примеры:** `examples/16_15_fenotip_rynka.md`


### 15.1. Ключевой принцип

Фенотип — это **измерение среды**, а не skill.

### 15.2. Считается дважды

1. `pretrade_probe`
2. `posttrade_regime_tagger`

### 15.3. Кто считает

Фенотип считает серверный модуль, а не агент:

- детерминированный probe;
- optional LLM audit.

### 15.4. Pre-trade phenotype

Используется для routing.

Стартовые оси:

1. `direction_state`
   - `up`
   - `down`
   - `range`

2. `volatility_state`
   - `compression`
   - `normal`
   - `expansion`

3. `liquidity_state`
   - `normal`
   - `thin`

4. `session_state`
   - `asia`
   - `eu`
   - `us`
   - `overlap`

### 15.5. Формулы MVP

#### direction
Использовать robust slope последних `30` свечей, нормированный на `ATR_30`.

[Кодовые примеры и схемы вынесены: `examples/16_15_fenotip_rynka.md`]

- `dir_score > +0.50` -> `up`
- `dir_score < -0.50` -> `down`
- иначе -> `range`

#### volatility
[Кодовые примеры и схемы вынесены: `examples/16_15_fenotip_rynka.md`]

- `< 0.75` -> `compression`
- `> 1.35` -> `expansion`
- иначе -> `normal`

#### liquidity
Использовать:
- spread / price
- top-of-book depth proxy
- recent timeout pressure

- `liq = thin`, если хотя бы два из трёх условий тревожны
- иначе `normal`

#### session
По UTC bucket.

### 15.6. Post-trade phenotype

После кейса допускается уточнение фенотипа через:

- actual fill speed
- realized path shape
- reversal/fake breakout detection
- sweep / exhaustion patterns

### 15.7. Важное ограничение

В режиме без навыка фенотип **не подсказывается агенту**.  
Он используется только системой.

---

## 16. Иерархия skill families и ветвление

### 16.1. Skill family = вид

`skill_family` — базовая эволюционная линия.

### 16.2. Branch = подвид / ветка

Ветки:
- `main`
- `repair`
- `niche`
- `hybrid`

### 16.3. Версии навыка

Конкретная версия внутри ветки:
- участвует в arena
- получает case-flow
- имеет score
- может быть promoted/demoted

### 16.4. Speciation

Новая ветка создаётся, если:

- есть устойчивый phenotype-specific edge;
- или устойчивый phenotype-specific failure;
- и накоплена достаточная выборка.

### 16.5. Что влияет на skill
Фенотип влияет на:

- routing
- arena bucket
- mutation targeting
- speciation
- extinction memory
- recombination filter

Фенотип не влияет на способ генерации сигнала агентом в режиме без навыка.

---

## 17. Arena, Sandbox, Tester

**Вынесенные примеры:** `examples/18_17_arena_sandbox_tester.md`


### 17.1. Разделение

- `sandbox` = безопасная среда
- `tester` = исполнитель прогонов
- `arena` = логика сравнения skill versions

### 17.2. Champion–Challenger Arena

Сравнение идёт внутри:

[Кодовые примеры и схемы вынесены: `examples/18_17_arena_sandbox_tester.md`]

### 17.3. Роли skill version в arena

- `champion`
- `challenger`
- `niche`
- `watchlist`
- `quarantined`
- `retired`

### 17.4. Split по умолчанию

- champion lane: `70%`
- challenger lane: `20%`
- niche lane: `5%`
- foundry / isolated lane: `5%`

Если активен слабый phenotype из curriculum queue:
- champion `60%`
- challengers `25%`
- niche `10%`
- foundry `5%`

### 17.5. `arena_score` — точная формула

Все компонентные метрики предварительно нормируются в диапазон `[0,1]`.

#### Компоненты

1. `E30_score = 0.5 * (1 + tanh(E30_shrunk / 0.50))`
2. `E100_score = 0.5 * (1 + tanh(E100_shrunk / 0.75))`
3. `PF_score = clamp((PF30 - 1.0) / 1.5, 0, 1)`
4. `fill_feasibility = 1 - timeout_rate_30`
5. `eta_accuracy = exp(-median_abs(fill_time_sec - expected_fill_window_sec) / 180)`
6. `plan_validity = 1 - invalid_rate_30`
7. `stability_score = clamp(1 - std([E10,E30,E100]) / (abs(E100_shrunk)+0.25), 0, 1)`
8. `regime_fit_score = 0.5 + 0.5 * tanh((Epheno30_shrunk - Eglobal30_shrunk) / 0.25)`
9. `freshness_score = exp(-cases_since_last_positive_E30 / 20)`
10. `pain_penalty = clamp(0.6 * loss_density_10 + 0.4 * negative_run_ratio_30, 0, 1)`
11. `protocol_penalty = clamp(protocol_breach_rate_30 / 0.10, 0, 1)`
12. `anti_pattern_penalty = clamp(anti_pattern_overlap_confidence, 0, 1)`

#### Формула

[Кодовые примеры и схемы вынесены: `examples/18_17_arena_sandbox_tester.md`]

### 17.6. `family_score`

`family_score` оценивает не отдельную версию, а силу семейства в данном `frame_shard`.

Компоненты:

- top-2 mean arena_score in family bucket
- family expectancy 100
- diversity bonus
- niche coverage
- family freshness
- family pain penalty

Формула:

[Кодовые примеры и схемы вынесены: `examples/18_17_arena_sandbox_tester.md`]

### 17.7. Routing weight

[Кодовые примеры и схемы вынесены: `examples/18_17_arena_sandbox_tester.md`]

Дальше routing веса распределяются bounded-softmax с ограничениями:

- `max_weight_per_skill = 0.35`
- `keep_alive_floor = 0.05`
- `sandbox_cap = 0.15`

---

## 18. Матожидание и производные метрики

**Вынесенные примеры:** `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`


### 18.1. `realized_R`

Для `LONG`:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

Для `SHORT`:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

### 18.2. `net_R`

Если есть торговое трение:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

В `MVP` при fee=0 и без явной slippage модели можно использовать:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

### 18.3. `trade_expectancy`

Для filled кейсов:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

Эквивалентно:

[Кодовые примеры и схемы вынесены: `examples/19_18_matozhidanie_i_proizvodnye_metriki.md`]

### 18.4. Вспомогательные метрики

- `fill_rate`
- `timeout_rate`
- `invalid_rate`
- `eta_accuracy`
- `loss_density`
- `negative_run_ratio`
- `freshness`
- `stability`

---

## 19. Tool Quality + Coverage Monitor

**Вынесенные примеры:** `examples/20_19_tool_quality_coverage_monitor.md`


### 19.1. Отдельный модуль обязателен

Нужен модуль:

[Кодовые примеры и схемы вынесены: `examples/20_19_tool_quality_coverage_monitor.md`]

### 19.2. Что он оценивает

- data tools
- parsers
- feature calculators
- execution bridge
- webhook receiver
- research tools

### 19.3. Что фиксируется

- technical success/failure
- latency
- missing coverage
- semantic uselessness
- symbol/timeframe mismatch
- stale data
- malformed payload
- repeated infra issues

### 19.4. Правило

Если деградирует инструмент:

- это не равно “мутировать trading skill”
- сначала создаётся infra/coverage event
- skill mutation блокируется до отделения skill failure от infra failure

---

## 20. Source Policy

### 20.1. Назначение

Source policy работает только для:

- evolver
- skill foundry
- research augmentation
- overlay optimization

Он не имеет права подсказывать пустому агенту способ генерации сигнала.

### 20.2. Разрешённые домены

#### Академические / препринты
- `arxiv.org`
- `ssrn.com`
- `papers.ssrn.com`
- `nber.org`
- `ideas.repec.org`
- `doi.org`

#### Журналы / издатели
- `tandfonline.com`
- `onlinelibrary.wiley.com`
- `link.springer.com`
- `sciencedirect.com`
- `academic.oup.com`
- `journals.uchicago.edu`
- `cambridge.org`

#### Институциональные / market structure
- `bis.org`
- `sec.gov`
- `ecb.europa.eu`
- `newyorkfed.org`
- `federalreserve.gov`

#### Биржа и venue docs
- `developers.binance.com`
- `binance.com`
- `support.binance.com`

### 20.3. Запрещённые домены для эволюционного обучения

- `x.com`
- `t.me`
- `youtube.com`
- `medium.com`
- `substack.com`
- `reddit.com`
- любые сигнальные паблики / блоги / медиа без научной или официальной природы

### 20.4. Что считается “лучшим” источником для scalping research

Приоритет источников:

1. market microstructure papers
2. execution / order flow papers
3. exchange microstructure docs
4. practitioner-grade venue docs
5. только потом — любые вторичные обзоры

### 20.5. Принцип

Лучшие внешние знания для скальпинга — это:

- market microstructure
- order flow
- liquidity
- execution
- limit order behavior
- fill probability
- short-horizon regime transitions

Не retail-блоги и не “сигнальные каналы”.

---

## 21. Где вызывается LLM

### 21.1. Принцип

LLM вызывается везде, где он может хотя бы немного повысить точность решения или вердикта.  
Детерминированный код остаётся хозяином протокола, БД, таймеров и безопасности.

### 21.2. Обязательные LLM-вызовы

#### Runtime
1. `FRAME.MD -> frame_resolved.json`
2. `AUTO skill selection`
3. `trade_plan synthesis`
4. `trade_thesis_snapshot`
5. `semantic trade-plan audit`

#### Post-trade
6. `outcome analysis`
7. `fault graph arbitration`
8. `critique pass`
9. `rewrite pass`
10. `validation pass`
11. `speciation decision`
12. `recombination justification`
13. `anti-pattern summary`

#### Foundry / Research
14. `skill foundry concept pass`
15. `contract pass`
16. `skill draft pass`
17. `source curation`
18. `promotion committee`
19. `overlay optimization`

### 21.3. Критические решения — через тройной проход

Для:
- mutation
- promotion
- recombination
- root cause

использовать:

1. `Generator`
2. `Skeptic`
3. `Arbiter`

---

## 22. Эволюционное ядро MVP

**Вынесенные примеры:** `examples/23_22_evolyutsionnoe_yadro_mvp.md`


### 22.1. Пост-обработчик после терминального кейса

Порядок обязателен:

[Кодовые примеры и схемы вынесены: `examples/23_22_evolyutsionnoe_yadro_mvp.md`]

### 22.2. `Protocol Integrity Gate`

Если срабатывает protocol/infrastructure failure:
- skill mutation запрещена
- кейс идёт в infra/coverage logging
- evolution skips

### 22.3. `Hard Selection`

Срабатывает при:
- сильно отрицательном `E30` и `E100`
- `PF30 < 1` и `PF100 < 1`
- структурной деградации
- повторяемых тяжёлых protocol breaches skill-side

### 22.4. `Soft Selection`

Если линия слабее family median, но не умерла:
- вес режется
- версия идёт в `watchlist`
- keep_alive сохраняется

### 22.5. `Local Mutation`

Разрешается только если:
- `>= 30` official cases
- нет infra flag
- линия не в quarantine
- виден plateau / weak `ME_30`

Правило:
- `1 child`
- `1 gene block`
- `1 generation`

### 22.6. `Recombination`

Разрешается только если:
- минимум `40` official cases на родителя
- оба родителя положительны
- similarity < `0.80`
- contract_version совпадает
- strong complementary genes

### 22.7. `Regime Speciation`

Создаёт niche-ветки при:
- phenotype-specific edge
- phenotype-specific recurring failure

### 22.8. `Structural Decomposition`

Запускается только если:
- `2-3` локальные мутации не помогли
- fault graph снова указывает один и тот же gene block

---

## 23. Skill Foundry

### 23.1. Назначение

Генерация новых узких trading skills.

### 23.2. Не противоречит пустому isolated режиму

Foundry работает **после кейсов**, а не до них.  
Он не подсказывает агенту путь в конкретном кейсе.

### 23.3. Вход

- frame_id
- lineage
- reflection capsules
- extinction memory
- phenotype stats
- source policy
- skill contract template

### 23.4. Выход

Новый skill package:
- `SKILL.md`
- `contract.json`
- `gene_map.json`
- `mutation_note.md`
- `references/`

---

## 24. Skill Tester / Forward Arena

### 24.1. Два контура

#### PROD lane
- manual / operator-triggered
- uses promoted skills only
- no empty isolated by default

#### LAB lane
- always-on
- runs champions, challengers, niche, foundry, isolated-zero
- feeds arena and evolution

### 24.2. Тестер = не арена

- `sandbox` = безопасная среда
- `tester` = исполнитель прогонов
- `arena` = логика сравнения skill versions

### 24.3. Практическая реализация MVP

#### Массовый слой
Виртуальное исполнение на live market feed.

#### Подтверждающий слой
Небольшое число demo/mirror executions для финалистов.

---

## 25. Skill storage и packaging

**Вынесенные примеры:** `examples/26_25_skill_storage_i_packaging.md`


### 25.1. Каждая версия навыка должна иметь

[Кодовые примеры и схемы вынесены: `examples/26_25_skill_storage_i_packaging.md`]

### 25.2. `skill promotion`

`skill promotion` = перевод версии skill в более высокий operational статус:

- `candidate -> challenger`
- `challenger -> champion`
- `watchlist -> niche`
- `quarantined -> retired`

### 25.3. Истина о skill version

Истина живёт в:
- `skill_registry`
- SQLite
- lineage ledger

OpenClaw получает только materialized copy.

---

## 26. SQLite schema

### 26.1. Обязательные группы таблиц

#### Core
- `frames`
- `cases`
- `case_events`
- `signal_plans`
- `trade_thesis_snapshots`
- `execution_events`
- `outcome_events`
- `data_requests`
- `data_artifacts`
- `coverage_gaps`

#### Skills
- `skill_families`
- `skill_branches`
- `skill_versions`
- `skill_contracts`
- `skill_gene_map`
- `skill_lineage`
- `skill_metrics_windows`
- `skill_router_weights`
- `skill_status_history`

#### Evolution
- `mutations`
- `recombinations`
- `speciation_events`
- `decomposition_events`
- `fault_graph_nodes`
- `fault_graph_edges`
- `extinction_memory`
- `curriculum_queue`
- `counterfactual_variants`
- `reflection_capsules`

#### Arena
- `arena_assignments`
- `arena_results`
- `promotion_events`
- `demotion_events`
- `watchlist_entries`

#### Phenotypes
- `case_phenotypes`
- `skill_phenotype_stats`
- `niche_registry`

#### Research / LLM
- `research_runs`
- `research_sources`
- `source_policy_profiles`
- `llm_judgments`
- `llm_artifacts`

---

## 27. Физическая структура проекта

**Вынесенные примеры:** `examples/28_27_fizicheskaya_struktura_proekta.md`


[Кодовые примеры и схемы вынесены: `examples/28_27_fizicheskaya_struktura_proekta.md`]

---

## 28. Порядок написания кода (часть 1)

### Этап 1. Основа runtime
1. `frame_engine`
2. `signal contract`
3. `trade validator`
4. `execution_bridge`
5. `webhook_receiver`
6. `case_memory`
7. SQLite base schema

### Этап 2. Базовый сигнал и outcome
8. `trade_thesis_snapshot`
9. `official_expectancy`
10. `terminal statuses`
11. `phenotype pretrade/posttrade`

### Этап 3. Skill registry
12. `skill_families / branches / versions`
13. `materialization to OpenClaw`
14. `EXPLICIT/AUTO/ISOLATED modes`

### Этап 4. Базовый evolution core
15. `protocol_integrity_gate`
16. `fault_graph`
17. `reflection_capsules`
18. `critic/rewriter/validator`
19. `local mutation`
20. `lineage`

### Этап 5. Арена
21. `arena router`
22. `arena_score`
23. `family_score`
24. `watchlist/quarantine`
25. `promotion/demotion`

### Этап 6. Расширение
27. `speciation`
28. `recombination`
29. `decomposition`
30. `skill foundry`
31. `lab lane`
32. `research augmentation`

---

## 29. Что входит в PART 2

Во второй части должны быть раскрыты в полном объёме:

- точные SQL DDL по таблицам;
- API интерфейсы модулей;
- JSON schemas;
- подробные prompts / LLM workflows;
- точные правила mutation/recombination/speciation;
- тестовый контур и план оркестрации lab workers;
- detailed overlay evolution;
- detailed source policy execution;
- полный набор артефактов на файловой системе;
- схемы отказоустойчивости и recovery;
- подробный coding roadmap по файлам.

---

## 30. Итог part 1

`SMART_TRADE` в этой версии — это:

- изолированный кодовый контур;
- агентный runtime через OpenClaw;
- пост-эволюционная архитектура по мотивам OpenSpace;
- система skill families в `frame`-изоляции;
- управление через математическое ожидание сигнала;
- популяционная эволюция через arena, mutation, speciation, recombination и foundry;
- максимальное использование LLM для semantic decisions;
- жёсткий детерминированный контроль протокола и инфраструктуры.

Этот файл определяет MVP.  
Если реализация расходится с этим файлом — реализация не соответствует проекту.


---

# SMART_TRADE_final_part_2

## 31. Назначение part 2

Эта часть дополняет `SMART_TRADE_final_part_1.MD` и фиксирует:

- точные интерфейсы;
- точные структуры данных;
- точные SQL DDL;
- точные JSON schemas;
- точные правила LLM workflows;
- точные правила mutation / recombination / speciation / promotion;
- точную оркестрацию lab workers;
- точную схему артефактов на файловой системе;
- отказоустойчивость и recovery;
- roadmap написания кода по файлам.

Часть 2 не переопределяет часть 1. Если есть конфликт, приоритет:

1. текущая часть 2;
2. часть 1;
3. более ранние документы.

---

## 32. Канонические идентификаторы и соглашения об именах

**Вынесенные примеры:** `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`


### 32.1. Формат ID

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

### 32.2. Канонизация phenotype key

Порядок осей фиксирован:

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

Пример:

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

### 32.3. Канонизация статусов skill version

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

### 32.4. Канонизация mutation type

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

### 32.5. Gene blocks

Фиксированный набор для MVP:

[Кодовые примеры и схемы вынесены: `examples/33_32_kanonicheskie_identifikatory_i_soglasheniya_ob_imenakh.md`]

Никакие другие gene-block имена в MVP не допускаются.

---

## 33. SQL DDL (каноническая SQLite schema)

**Вынесенные примеры:** `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`


### 33.1. Общие правила

- SQLite `WAL` mode обязателен.
- Все временные поля хранятся как `TEXT` в ISO-8601 UTC.
- Все JSON хранятся как `TEXT` с валидным JSON.
- Все денежные величины опциональны и не участвуют в ядре эволюции.
- Все `R`-метрики хранятся как `REAL`.
- Удаление lineage / событий запрещено. Только append-only.

### 33.2. PRAGMA

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.3. Таблицы CORE

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.4. Таблицы PHENOTYPE и METRICS

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.5. Таблицы SKILLS

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.6. Таблицы EVOLUTION

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.7. Таблицы ARENA

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.8. Таблицы QUALITY / RESEARCH / LLM

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

### 33.9. Представления

[Кодовые примеры и схемы вынесены: `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md`]

---

## 34. Канонические JSON schemas

**Вынесенные примеры:** `examples/35_34_kanonicheskie_json_schemas.md`


### 34.1. `frame_resolved.json`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.2. `data_request`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

**Правила:**
- `data_type` свободная строка
- `params` свободный словарь
- система не раскрывает заранее каталог допустимых типов
- отсутствие покрытия => `BLOCKED_BY_DATA_COVERAGE`

### 34.3. `data_response`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.4. `trade_plan`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

**Канонические правила:**
- `expected_fill_window_sec` — оценка, не жёсткий kill switch
- `expected_fill_deadline_ts` — вычисляется runtime как `generated_at + entry_timeout_sec`
- агент не задаёт `expected_fill_deadline_ts` напрямую в MVP

### 34.5. `trade_thesis_snapshot`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.6. `execution_order_request`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.7. `outcome_webhook`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.8. `decision_capsule`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.9. `lesson_capsule`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

### 34.10. `candidate_skill_manifest`

[Кодовые примеры и схемы вынесены: `examples/35_34_kanonicheskie_json_schemas.md`]

---

## 35. Internal service APIs и OpenClaw integration API

**Вынесенные примеры:** `examples/36_35_internal_service_apis_i_openclaw_integration_api.md`


### 35.1. Internal Python interfaces

[Кодовые примеры и схемы вынесены: `examples/36_35_internal_service_apis_i_openclaw_integration_api.md`]

### 35.2. OpenClaw-facing tools

#### `smart_trade_start_case`

**Input:**
[Кодовые примеры и схемы вынесены: `examples/36_35_internal_service_apis_i_openclaw_integration_api.md`]

**Output:**
[Кодовые примеры и схемы вынесены: `examples/36_35_internal_service_apis_i_openclaw_integration_api.md`]

#### `smart_trade_request_data`

**Input:** пакет `data_request`

**Output:** пакет `data_response`

#### `smart_trade_submit_signal`

**Input:** `trade_plan` + `trade_thesis_snapshot`

**Output:**
[Кодовые примеры и схемы вынесены: `examples/36_35_internal_service_apis_i_openclaw_integration_api.md`]

#### `smart_trade_case_status`

**Input:** `case_id`

**Output:** текущее состояние кейса и summary.

### 35.3. Execution bridge HTTP API

#### `POST /v1/execution/orders`
- body: `execution_order_request`
- response: `execution_ack`

#### `POST /v1/execution/outcomes`
- body: `outcome_webhook`
- idempotent by `(case_id, signal_id, outcome_code, closed_at)`

#### `GET /v1/cases/{case_id}`
- case summary

#### `GET /v1/skills/{skill_version_id}`
- skill metadata

---

## 36. LLM workflows (канонические)

**Вынесенные примеры:** `examples/37_36_llm_workflows_kanonicheskie.md`


### 36.1. Общие правила

- Default model: `GPT-5.4 Pro`
- Все важные вердикты: `Generator -> Skeptic -> Arbiter`
- Все LLM outputs должны быть JSON-first
- Любой LLM output проходит deterministic validation

### 36.2. Workflow list

| Workflow | Обязателен | Вход | Выход |
|---|---:|---|---|
| `frame_normalizer` | Да | `FRAME.MD` | `frame_resolved.json` |
| `auto_skill_selector` | Да | frame + active pool | selected skill family/version |
| `trade_plan_semantic_audit` | Да | `trade_plan` + thesis | semantic audit JSON |
| `outcome_analyzer` | Да | case bundle | outcome analysis JSON |
| `fault_graph_tiebreaker` | Условно | deterministic ambiguity | blame resolution JSON |
| `critic_pass` | Да | candidate mutation target | critique report |
| `rewrite_pass` | Да | critique + source blocks | candidate skill pack |
| `recombination_composer` | Условно | two parents + gene map | child pack |
| `speciation_judge` | Условно | niche divergence bundle | branch/family decision |
| `promotion_committee` | Да | arena evidence | promote/keep/quarantine |
| `research_synthesizer` | Да | retrieved papers/docs | evidence package |
| `overlay_optimizer` | Условно | execution traces | candidate overlay |

### 36.3. Prompt contract: `frame_normalizer`

**Goal:** превратить свободный `FRAME.MD` в machine-safe JSON без изменения смысла.

**Input:** raw `FRAME.MD`, project defaults.

**Output:** `frame_resolved.json`

**Hard rules:**
- не изобретать новые operator options;
- если поле двусмысленно — выставить `ambiguity_flag`;
- не добавлять knowledge about data generation method.

### 36.4. Prompt contract: `auto_skill_selector`

**Input:**
- `frame_resolved`
- current phenotype (если есть)
- active skill pool metadata
- routing weights

**Output:**
[Кодовые примеры и схемы вынесены: `examples/37_36_llm_workflows_kanonicheskie.md`]

**Hard rule:** не использовать hidden rationale outside JSON.

### 36.5. Prompt contract: `trade_plan_semantic_audit`

**Purpose:** semantic second opinion on plan quality, not technical validity.

**Hard rule:** аудит не имеет права заблокировать валидный план в MVP; только пишет semantic flags.

### 36.6. Prompt contract: `critic_pass`

**Input bundle:**
- target gene block
- fault event
- counterfactual summary
- anti-pattern hits
- reflection capsules
- current skill block text

**Output:**
[Кодовые примеры и схемы вынесены: `examples/37_36_llm_workflows_kanonicheskie.md`]

### 36.7. Prompt contract: `rewrite_pass`

**Input:** current block + critique + optional donor blocks

**Output:**
- exact replacement for one block;
- or full candidate package if `MACRO_BRANCH/RECOMBINATION`.

### 36.8. Prompt contract: `promotion_committee`

**Input:**
- arena metrics
- phenotype bucket
- anti-pattern overlap
- protocol flags
- lineage health

**Output:**
[Кодовые примеры и схемы вынесены: `examples/37_36_llm_workflows_kanonicheskie.md`]

---

## 37. Exact evolution rules

### 37.1. Protocol Integrity Gate

Запускается первым после terminal case.

**If any true:**
- malformed trade plan
- invalid geometry
- stale data
- execution bridge failure
- corrupted webhook payload
- symbol/frame mismatch

**Then:**
- create protocol / infra flag
- skip skill mutation
- allow only quality logging

### 37.2. Hard Selection

**Trigger A — immediate quarantine** if any:
- `E30 < 0` and `E100 < 0`
- `PF30 < 1` and `PF100 < 1`
- `invalid_rate_30 > 0.20`
- repeated protocol breach attributable to skill (`>=3 / last 20 official cases`)

**Action:** status -> `QUARANTINED`

**Trigger B — confirmed hard selection**:
- weak for two consecutive family review cycles

**Action:** `WATCHLIST -> QUARANTINED`

### 37.3. Soft Selection

**Trigger:**
- `n_official_30 >= 20`
- `arena_score < family_median_score - 0.10`
- no hard selection

**Action:**
- routing weight cut by `50–80%`
- status -> `WATCHLIST`
- keep_alive_floor preserved

**Rehabilitation gate:**
- `E30 > 0`
- `PF30 > 1`
- restored `regime_fit_score`

### 37.4. Local Mutation

**Trigger:**
- `n_official_30 >= 30`
- no protocol flag
- line not quarantined
- plateau OR repeated blame in one gene

**Rules:**
- 1 child per cycle
- 1 gene block per generation
- 1–2 low-level changes inside block
- mutation order: parameters -> filters -> features -> structure

### 37.5. Recombination

**Admission gate:**
- each parent: `n_official_40+`
- each parent: `E30 > 0`
- each parent not watchlisted/quarantined
- `similarity < 0.80`
- same `frame_shard`
- same `contract_version`
- complementarity evidence exists

**Action:** child starts as `CHALLENGER` with sandbox weight.

### 37.6. Regime Speciation

**Trigger:**
- phenotype bucket has `>=20` comparable official cases
- divergence exists between global and bucket performance
- deterministic phenotype stable

**Action:**
- new niche branch in same family, or
- new family if divergence is structural and persistent

### 37.7. Structural Decomposition

**Trigger:**
- `2–3` failed local mutations in a row
- same gene repeatedly blamed (`>=3 of last 5 comparable cases`)
- skill file too broad or mixed responsibility

**Action:**
- split into smaller branches / children
- parent stays live until challenger proves itself

### 37.8. Extinction Memory

**Create anti-pattern if:**
- `>=5` comparable cases
- `shrunk_expectancy_R < -0.35`
- repeated same signature
- no infra explanation

**Use:**
- penalize routing / promotion
- increase curriculum priority
- do not block raw signal generation in `NONE` mode

### 37.9. Promotion

**Promote challenger to champion if:**
- `>=30` comparable official cases in bucket
- `arena_score_delta >= +0.08`
- `E30_delta >= +0.15R`
- `fill_rate` not worse by more than `7pp`
- no major anti-pattern overlap
- no protocol flag

### 37.10. Cooldowns

- local mutation cooldown: `10 official cases` on same line
- major adaptation cooldown: `20 official cases`
- macro branch cooldown after promotion: `5 official cases`
- recombination cooldown: `10 official cases` per family

---

## 38. Lab workers / forward arena orchestration

**Вынесенные примеры:** `examples/39_38_lab_workers_forward_arena_orchestration.md`


### 38.1. Initial volume

Per active `frame_shard`:
- `12` trader-lab workers

Breakdown:
- `4` baseline workers
- `4` challenger workers
- `2` niche workers
- `2` zero-skill isolated workers

Control plane (not counted as lab workers):
- `1` arena scheduler
- `1` outcome analyzer/evolver dispatcher
- `1` foundry scheduler
- `1` research worker

### 38.2. Worker modes

#### Baseline worker
Runs current champion lines to keep baseline statistics warm.

#### Challenger worker
Runs candidate lines according to arena split.

#### Niche worker
Targets under-explored phenotype buckets.

#### Zero-skill isolated worker
Runs empty isolated environment to permit spontaneous emergence.

### 38.3. Scheduling loop

[Кодовые примеры и схемы вынесены: `examples/39_38_lab_workers_forward_arena_orchestration.md`]

### 38.4. Execution lanes

#### PROD lane
- only user-invoked
- uses promoted or explicit skills
- external execution bridge

#### LAB lane
- autonomous
- hybrid execution:
  - mass virtual forward on live data
  - selective demo mirror for finalists

### 38.5. Why hybrid lane

For one shard, unlimited real demo workers add correlation and API burden. Hybrid forward yields more information density.

---

## 39. Overlay evolution and source policy execution

**Вынесенные примеры:** `examples/40_39_overlay_evolution_and_source_policy_execution.md`


### 39.1. Overlay types

Mutable:
- `agents_overlay`
- `tools_overlay`
- limited `bootstrap_overlay`

Mostly fixed:
- `SOUL`
- `IDENTITY`

### 39.2. Overlay registry tables

Use `overlay_versions`, `overlay_lineage`, `overlay_assignments`.

### 39.3. Overlay application rule

- overlay mutations never affect current live session
- applied only on next session materialization
- same promotion ladder as skills, but separate pool

### 39.4. Source policy execution pipeline

[Кодовые примеры и схемы вынесены: `examples/40_39_overlay_evolution_and_source_policy_execution.md`]

### 39.5. Allowed domain tiers

#### Tier 1 — market microstructure and execution primary sources
- `developers.binance.com`
- `binance.com`
- `support.binance.com`
- `arxiv.org`
- `ssrn.com`
- `papers.ssrn.com`
- `nber.org`
- `pubsonline.informs.org`

#### Tier 2 — peer reviewed publishers
- `sciencedirect.com`
- `link.springer.com`
- `onlinelibrary.wiley.com`
- `tandfonline.com`
- `academic.oup.com`
- `journals.uchicago.edu`
- `cambridge.org`

#### Tier 3 — institutional / regulator / central bank
- `bis.org`
- `sec.gov`
- `cftc.gov`
- `ecb.europa.eu`
- `newyorkfed.org`
- `federalreserve.gov`

### 39.6. Deny list

- social media
- telegram channels
- reddit
- youtube
- medium/substack
- anonymous blogs
- pure signal-selling resources

### 39.7. Research use restriction

Research augmentation can influence:
- evolver
- foundry
- overlay optimizer

Research augmentation cannot:
- inject direct trading method instructions into empty isolated runtime
- override protocol validation

---

## 40. Filesystem artifacts

**Вынесенные примеры:** `examples/41_40_filesystem_artifacts.md`


### 40.1. Per-case directory

[Кодовые примеры и схемы вынесены: `examples/41_40_filesystem_artifacts.md`]

### 40.2. Per-skill directory

[Кодовые примеры и схемы вынесены: `examples/41_40_filesystem_artifacts.md`]

### 40.3. Overlay directory

[Кодовые примеры и схемы вынесены: `examples/41_40_filesystem_artifacts.md`]

---

## 41. Resilience and recovery

### 41.1. General rules

- no long-lived trading session waiting for outcome
- case state is source of truth, not agent memory
- every state transition writes append-only event
- webhook ingestion is idempotent
- all derived metrics are recomputable from events

### 41.2. Idempotency keys

#### Order submission
`(case_id, signal_id)`

#### Outcome webhook
`(case_id, signal_id, outcome_code, closed_at)`

### 41.3. Recovery procedures

#### If trader session crashes before signal
- case remains `AGENT_RUN_STARTED`
- safe to rerun same case with same frame and materialized pool

#### If crash after signal but before submit ack
- inspect `execution_events`
- if no ack -> retry with same `signal_id`
- if ack exists -> do not resubmit

#### If webhook arrives twice
- second event ignored by unique idempotency key

#### If evolution crashes mid-run
- `mutations.status = STARTED`
- rerun evolution from case bundle; no mutation event is overwritten

#### If packaging crashes after candidate creation
- candidate remains `DRAFT`
- packaging rerun by `mutation_id`

### 41.4. Dead letter handling

Need dead-letter tables:
- `dead_execution_events`
- `dead_webhooks`
- `dead_mutation_jobs`

No event may be silently dropped.

---

## 42. Detailed coding roadmap by files

**Вынесенные примеры:** `examples/43_42_detailed_coding_roadmap_by_files.md`


### 42.1. Phase 1 — runtime core

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.2. Phase 2 — contracts and database

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.3. Phase 3 — skill registry and materialization

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.4. Phase 4 — monitoring and analysis

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.5. Phase 5 — evolution kernel

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.6. Phase 6 — arena and lab

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.7. Phase 7 — foundry and research

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

### 42.8. Phase 8 — OpenClaw bridge

[Кодовые примеры и схемы вынесены: `examples/43_42_detailed_coding_roadmap_by_files.md`]

---

## 43. Acceptance criteria for part 2

Part 2 считается реализованной корректно, если:

1. любой кейс можно полностью восстановить из SQLite + файловых артефактов;
2. любая skill mutation воспроизводима и имеет lineage;
3. empty isolated mode запускается без подсказки метода;
4. protocol failures не мутируют trading skill;
5. champion/challenger работает на live-forward lane;
6. recombination не смешивает несовместимые contracts;
7. source policy enforce-ится технически, а не “по доброй воле агента”;
8. overlays вступают в силу только на новой сессии;
9. все важные semantic решения логируются через `llm_judgments`;
10. итог проекта можно восстановить 100 независимыми командами одинаково по логике.

---

## 44. Итог part 2

`SMART_TRADE_final_part_2` переводит проект из уровня “подробная архитектурная идея” в уровень:

- конкретных схем данных;
- конкретных интерфейсов;
- конкретной БД;
- конкретных JSON контрактов;
- конкретных правил мутации и продвижения;
- конкретного разбиения по файлам.

Если реализация расходится с частью 1 или 2, то реализация не соответствует проекту.

---

## 45. Матрица ответственности компонентов

### 45.1. Принцип

У каждого компонента должна быть ровно одна доминирующая ответственность.  
Если компонент одновременно:

- принимает торговое решение,
- проверяет собственную валидность,
- исполняет ордер,
- пишет lineage,
- продвигает skill,

то это архитектурная ошибка.

### 45.2. Ответственности

| Компонент | Единственная главная ответственность | Не имеет права делать |
|---|---|---|
| `frame_engine` | нормализовать и валидировать frame | принимать торговое решение |
| `skill_materializer` | собрать видимый агенту runtime context | менять lineage |
| `prod_trader_agent` | синтезировать trade plan и thesis snapshot | эволюционировать skill |
| `trade_validator` | проверять техническую валидность плана | судить о качестве идеи |
| `execution_bridge` | доставить заявку во внешний контур | менять skill |
| `webhook_receiver` | принять и нормализовать outcome | вычислять mutation |
| `expectancy_monitor` | считать окна и derived-метрики | выбирать текст патча skill |
| `fault_graph` | отнести провал к gene block / infra | паковать skill |
| `mutation_controller` | выбрать тип изменения | генерировать содержимое skill |
| `critic` | сформулировать критику | переписывать skill |
| `rewriter` | сгенерировать candidate patch | принимать promotion decision |
| `validator` | проверить candidate skill | менять arena weights |
| `promotion_controller` | принять решение о статусе skill | переписывать skill |
| `foundry` | синтезировать новые skill candidates | исполнять trade |
| `overlay_registry` | хранить версии overlay | принимать торговые решения |

### 45.3. Жёсткое правило

Если в реализации один класс/сервис делает две и более доминирующих роли из таблицы выше, реализация считается неправильной.

---

## 46. Наблюдаемость, аудит и журналы

### 46.1. Обязательные типы журналов

Должны существовать четыре независимых слоя журналирования:

1. `case journal`
2. `execution journal`
3. `evolution journal`
4. `operator/audit journal`

### 46.2. Минимум полей журнала

#### `case journal`
- `case_id`
- `frame_id`
- `skill_family_id`
- `skill_version_id`
- `status`
- `terminal_reason`
- `created_at`
- `closed_at`

#### `execution journal`
- `signal_id`
- `entry_limit`
- `submitted_at`
- `filled_at`
- `closed_at`
- `outcome_code`
- `latency_ms`
- `execution_bridge_version`

#### `evolution journal`
- `mutation_id`
- `recombination_id`
- `promotion_id`
- `target_gene`
- `from_skill_version_id`
- `to_skill_version_id`
- `decision`
- `confidence`
- `created_at`

#### `operator journal`
- `operator_event_id`
- `case_id`
- `event_type`
- `comment`
- `created_at`

### 46.3. Требование к логированию LLM

Каждый LLM workflow обязан логировать:

- `workflow_name`
- `model_name`
- `input_hash`
- `output_hash`
- `subject_ref_id`
- `created_at`

Полные prompt/response можно хранить отдельно и с ротацией, но **хэш + маршрут + субъект** должны храниться всегда.

### 46.4. Требование к мониторингу

Минимальные operational metrics:

- cases/hour
- signal_submit_success_rate
- execution_abort_rate
- webhook_lag_p50/p95
- mutation_success_rate
- promotion_success_rate
- arena_assignment_success_rate
- coverage_gap_rate
- zero-skill isolated survival rate

---

## 47. Безопасность, секреты и изоляция

### 47.1. Секреты

Секреты не имеют права жить:

- в `FRAME.MD`
- в `SKILL.md`
- в lineage
- в case artifacts
- в SQLite в открытом виде

### 47.2. Хранение секретов

Разрешённые места:

- environment variables
- external secrets manager
- encrypted local secret file вне project root

### 47.3. Что агент не должен видеть никогда

- API keys
- размер капитала
- live/demo routing secrets
- raw webhook secrets
- полные внутренние allow/deny security policies

### 47.4. Изоляция workspaces

Каждый агент OpenClaw должен иметь:

- отдельный `agentDir`
- отдельный `workspace`
- отдельный allowlist skill materialization
- отдельный overlay materialization

### 47.5. Политика чтения/записи

`prod_trader_agent`:
- может читать materialized runtime skills
- не может писать в canonical registry напрямую

`evolver_agent`:
- может читать case artifacts и registry
- пишет candidate artifacts только через `skill_packager`

`foundry_agent`:
- пишет только в candidate zone

### 47.6. Жёсткий запрет

Нельзя позволять агентам напрямую редактировать:
- canonical SQLite
- canonical skill registry
- canonical overlays
в обход соответствующих сервисов.

---

## 48. Политика хранения и очистки данных

### 48.1. Case artifacts

Хранить все case artifacts минимум:
- `180 дней` для MVP

### 48.2. Mutation / lineage / promotion события

Хранить бессрочно.
Удаление lineage запрещено.

### 48.3. LLM full payload retention

Допускается ротация full prompt/response:
- `30–90 дней`

Но summary hashes и маршруты хранятся бессрочно.

### 48.4. Research artifacts

Хранить:
- source list
- synthesis summary
- citation links
- source hashes

минимум `180 дней`, лучше бессрочно.

### 48.5. Cleanup jobs

Нужны отдельные jobs:
- prune ephemeral payloads
- compact stale temp artifacts
- validate orphan references
- rebuild materialized runtime copies if missing

---

## 49. Acceptance matrix по подсистемам

### 49.1. Runtime core считается готовым, если

- новый кейс можно создать из `FRAME.MD`
- агент получает только допустимый runtime context
- валидный trade plan доходит до `execution_bridge`
- невалидный trade plan не доходит до bridge
- пустой isolated mode не падает

### 49.2. Execution bridge считается готовым, если

- submit идемпотентен
- timeout неисполненной заявки обрабатывается
- webhook повторно не ломает состояние
- `OPERATOR_INTERVENED` корректно фиксируется

### 49.3. Evolution core считается готовым, если

- protocol failures не запускают mutation
- fault graph выдаёт `primary_fault_gene`
- mutation создаёт не более `1 child / 1 block / 1 generation`
- lineage append-only
- candidate skill проходит validator

### 49.4. Arena считается готовой, если

- назначения skill в кейс воспроизводимы
- champion/challenger split соблюдается
- routing weights ограничены (`max_weight`, `keep_alive`)
- promotion и demotion отражаются в registry

### 49.5. Foundry считается готовой, если

- может собрать skill из isolated опыта
- не нарушает contract version
- не подсказывает runtime-агенту метод в пустом режиме
- выпускает candidate только через packaging path

### 49.6. Research augmentation считается готовым, если

- соблюдается allowlist доменов
- denylist enforce-ится технически
- source package сохраняется
- mutation note получает ссылки на источники

---

## 50. Явно запрещённые упрощения

Ниже список того, что программистам делать нельзя, даже если им “так быстрее”.

1. Нельзя заменить `trade_expectancy` на raw PnL.
2. Нельзя хранить истину только в OpenClaw workspace.
3. Нельзя давать пустому isolated агенту скрытые подсказки о методе анализа.
4. Нельзя позволять protocol failure мутировать trading skill.
5. Нельзя делать recombination между несовместимыми contracts.
6. Нельзя продвигать skill без arena evidence.
7. Нельзя смешивать символы в один registry без frame-level изоляции.
8. Нельзя делать free-form mutation без critic -> rewriter -> validator chain.
9. Нельзя позволять агенту напрямую писать в canonical registry.
10. Нельзя держать торговую сессию подвешенной до outcome.
11. Нельзя делать смысловой пользовательский `NO_TRADE` в MVP.
12. Нельзя считать, что отсутствие fill эквивалентно прибыльной “осторожности”.
13. Нельзя отключать append-only lineage.
14. Нельзя использовать запрещённые research domains в автоматической эволюции.

---

## 51. Индекс final pack

Главный файл:
- `01_SMART_TRADE_MASTER_SPEC_MAX.md`

Companion docs:
- `02_OPENSPACE_DONOR_MAP.md`
- `03_OPENCLAW_AGENT_MODEL.md`
- `04_LLM_CALL_MATRIX.md`
- `05_HUMAN_AUTONOMY_MATRIX.md`
- `06_IMPLEMENTATION_CHECKLIST.md`

Папка примеров:
- `examples/`

Манифест:
- `SPEC_PACK_MANIFEST.json`

### 51.1. Порядок чтения

1. `00_README.md`
2. `01_SMART_TRADE_MASTER_SPEC_MAX.md`
3. `03_OPENCLAW_AGENT_MODEL.md`
4. `04_LLM_CALL_MATRIX.md`
5. `02_OPENSPACE_DONOR_MAP.md`
6. `05_HUMAN_AUTONOMY_MATRIX.md`
7. `06_IMPLEMENTATION_CHECKLIST.md`
8. `examples/` по мере надобности