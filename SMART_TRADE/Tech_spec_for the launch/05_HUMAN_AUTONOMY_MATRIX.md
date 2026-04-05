# 05_HUMAN_AUTONOMY_MATRIX

## Назначение

Этот файл фиксирует:

- какие процессы в SMART_TRADE работают **полностью автономно**;
- где нужен **обязательный человек**;
- где возможен **человек только как override**;
- где человеку вмешиваться запрещено.

Главная идея:

> Человек не должен заменять собой эволюционный контур, но должен оставаться владельцем production-риска, внешней инфраструктуры и правил допуска в боевой слой.

---

## 1. Категории процессов

### A. Полностью автономные
Процессы идут без человека по умолчанию.

### B. Human-gated
Процесс требует ручного подтверждения.

### C. Human-override only
Процесс автономный, но человек может вмешаться или отменить.

### D. Human-forbidden
Человек не должен менять это вручную в обход системных правил.

---

## 2. Полностью автономные процессы

## 2.1. Runtime inside one case

Автономно:
- materialization skills/overlays в workspace
- запуск новой OpenClaw session
- frame normalization
- skill selection в `AUTO`
- data-request routing
- technical plan validation
- submit to execution bridge
- запись `trade_thesis_snapshot`

## 2.2. Post-trade processing

Автономно:
- webhook ingestion
- case bundle assembly
- pre/post phenotype tagging
- official expectancy update
- fault graph
- counterfactual replay
- extinction memory update
- reflection capsule generation
- mutation scheduling
- critic / skeptic / arbiter evolution flows
- packaging candidate skills
- arena scoring
- watchlist / quarantine / keep-alive decisions
- curriculum queue updates

## 2.3. LAB lane

Автономно:
- case scheduling for lab workers
- champion/challenger routing
- niche routing
- zero-skill isolated test runs
- research runs by allowlist source policy
- foundry candidate generation

---

## 3. Human-gated процессы

## 3.1. Production enablement

Обязательно вручную:
- первичное включение production lane для нового `frame_shard`
- подключение внешнего execution bridge к real account / real venue
- активация операторского режима на боевом контуре

## 3.2. Secrets and execution credentials

Обязательно вручную:
- ввод API keys
- ротация execution secrets
- смена webhook secrets
- смена sandbox / live endpoints

## 3.3. Source policy boundaries

Обязательно вручную:
- расширение allowlist доменов
- изменение denylist
- разрешение новых source classes

## 3.4. Export из isolated/lab в production-eligible shared pool

Рекомендую как human-gated step:
- вывод skill family из isolated experimental origin
- перевод в общий production-eligible shared pool

Причина:
- это самая опасная граница загрязнения production.

## 3.5. Изменение core invariants

Обязательно вручную:
- разрешение новых order types
- отмена обязательности `TP/SL`
- изменение terminal semantics
- изменение frame isolation rules
- отключение protocol integrity gate

---

## 4. Human-override only процессы

## 4.1. Live case manual intervention

Человек может:
- вручную снять / закрыть уже открытую сделку
- поставить `OPERATOR_INTERVENED`

Но:
- это не должно подменять собой нормальную логику evolver;
- такие кейсы не становятся жёсткой основой для mutation.

## 4.2. Promotion freeze

Человек может:
- поставить `promotion_freeze` на frame/family/version
- временно остановить automatic promotion/demotion

## 4.3. Emergency quarantine

Человек может вручную перевести:
- `CHAMPION -> QUARANTINED`
- `CHALLENGER -> QUARANTINED`

если видит внешнюю аномалию, не отражённую системой.

## 4.4. Replay / re-run maintenance

Человек может инициировать:
- rebuild materialized workspace
- replay evolution from case bundle
- recompute metrics windows

Но не должен переписывать raw lineage events задним числом.

---

## 5. Human-forbidden зоны

## 5.1. Нельзя вручную менять canonical truth в обход сервисов

Запрещено вручную:
- редактировать canonical SQLite без migration/service layer
- менять skill lineage задним числом
- переписывать arena results руками
- редактировать official outcomes так, как будто их не было

## 5.2. Нельзя вручную подсказывать пустому isolated агенту метод анализа

Запрещено:
- тайно добавлять в `AGENTS.md` подсказки о способе генерации сигнала
- подсовывать списки “правильных” data types
- встраивать скрытую методику в протокольные навыки

Это ломает ключевую аксиому проекта.

## 5.3. Нельзя обходить deterministic validators

Ни человек, ни агент не должны:
- пропускать `PLAN_INVALID` мимо валидатора
- протаскивать прямую отправку ордера без bridge
- мимо source policy запускать web-research

---

## 6. Рекомендуемая human policy по production

### 6.1. В production человек должен делать только это

1. выбрать `FRAME`
2. запустить кейс
3. при необходимости руками вмешаться в уже открытую позицию
4. принимать решения по операционным вещам:
   - exchange credentials
   - source allowlist changes
   - enabling new shards
   - exporting isolated skills into shared prod pool

### 6.2. Всё остальное должно быть автономно

Если человеку приходится каждый день вручную:
- выбирать winner,
- подтверждать mutation,
- решать arena split,
- рулить watchlist,
- выбирать phenotype,

значит система собрана неправильно.

---

## 7. Граница между “автономно” и “опасно автономно”

### Автономно можно
- выбирать skill version внутри already-approved frame
- снижать/повышать routing weight
- мутировать skill внутри family
- создавать niche children
- recombine в lab
- двигать версии по ladder до `challenger`
- тестировать их в sandbox

### Осторожно автономно
- promotion в active shared pool
- overlay changes
- research-driven skill mutation
- export из isolated families в production-visible families

Для этих шагов допускается human gate или по крайней мере manual review flag.

---

## 8. Короткая итоговая матрица

| Процесс | Режим |
|---|---|
| Создание кейса | Human starts, дальше autonomously |
| Синтез trade plan | Autonomous |
| Submit сигнала | Autonomous |
| Outcome ingestion | Autonomous |
| Fault graph / mutation / arena | Autonomous |
| LAB routing | Autonomous |
| Production lane enablement | Human-gated |
| Secrets / credentials | Human-gated |
| Export isolated -> shared prod pool | Human-gated |
| Manual close live trade | Human-override only |
| Canonical lineage editing | Human-forbidden |
| Подсказки пустому isolated агенту | Human-forbidden |

---

## 9. Главный operational принцип

> Production-риски и внешние границы контролирует человек.\
> Внутреннюю эволюцию, отбор и skill-динамику контролирует система.

Именно такая граница даёт одновременно:
- безопасность,
- воспроизводимость,
- максимальную автономность без превращения проекта в ручное полууправление.
