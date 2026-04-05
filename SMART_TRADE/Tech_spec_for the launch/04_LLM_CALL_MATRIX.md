# 04_LLM_CALL_MATRIX

## Назначение

Этот файл фиксирует:

- **какие LLM-вызовы есть в SMART_TRADE**;
- **какими агентами они делаются**;
- **в каких сессиях OpenClaw они идут**;
- **с какими настройками модели / thinking / web**;
- **какие вызовы обязательны, а какие вторичны**.

Главный принцип:

> LLM используется максимально широко там, где нужен semantic edge.\
> Детерминированный код остаётся хозяином протокола, безопасности, БД и execution.

---

## 1. Базовые model profiles

### 1.1. Канонические профили

#### `MODEL_TRADER_PRIMARY`
- model: `GPT-5.4 Pro`
- thinking: `high`
- web: `off` by default
- tools: runtime only

#### `MODEL_TRADER_AUDIT`
- model: `GPT-5.4 Pro`
- thinking: `medium`
- web: `off`
- tools: no execution, no canonical write

#### `MODEL_EVOLVER_COMMITTEE`
- model: `GPT-5.4 Pro`
- thinking: `high`
- web: `off` by default
- tools: case artifacts + registry views

#### `MODEL_FOUNDRY`
- model: `GPT-5.4 Pro`
- thinking: `high`
- web: `restricted by source_policy`
- tools: no execution

#### `MODEL_RESEARCH`
- model: `GPT-5.4 Pro`
- thinking: `high`
- web: `on, allowlist only`
- tools: retrieval only

#### `MODEL_OVERLAY`
- model: `GPT-5.4 Pro`
- thinking: `medium`
- web: `off` by default
- tools: overlay refs only

### 1.2. Почему не делим модели на дешёвые и дорогие в стартовом max-pack

Потому что по твоему решению ресурс не ограничен. Значит оптимизация идёт не по цене, а по качеству решений.

Если позже потребуется cost optimization, отдельный policy layer может понизить model tier только для:
- baseline lab workers
- low-priority research jobs
- archive summarization

Но в главной спеки это **не дефолт**.

---

## 2. Runtime LLM-вызовы

## 2.1. `frame_normalizer`

### Кто вызывает
- `prod_trader_agent`
- все `lab_*_worker_agent`

### Когда
- сразу после получения `FRAME.MD`

### Сессия
- текущая торговая сессия

### Профиль
- `MODEL_TRADER_PRIMARY`

### Вход
- raw `FRAME.MD`
- project defaults
- frame defaults

### Выход
- `frame_resolved.json`

### Обязательность
- обязательный вызов

### Комментарий
- это LLM-нормализация формата, но не генерация сигнала
- двусмысленность помечается явно, а не домысливается бесконтрольно

---

## 2.2. `auto_skill_selector`

### Кто вызывает
- `prod_trader_agent` / `lab_worker_agent`

### Когда
- только если `skill_mode = AUTO`

### Профиль
- `MODEL_TRADER_PRIMARY`

### Вход
- `frame_resolved`
- pretrade phenotype
- allowed skill families / versions
- routing weights snapshot

### Выход
- выбранный `skill_family_id`
- выбранный `skill_version_id`
- rationale summary

### Обязательность
- обязательный, если AUTO
- не вызывается в `EXPLICIT`
- не имеет права подсказывать путь в `ISOLATED + empty`

---

## 2.3. `trade_plan_synthesis`

### Кто вызывает
- `prod_trader_agent`
- все `lab_*_worker_agent`

### Когда
- центральный вызов каждой торговой сессии

### Профиль
- `MODEL_TRADER_PRIMARY`

### Вход
- `FRAME`
- materialized skills
- overlays
- доступные tools
- доступные data artifacts / results from request_market_data

### Выход
- `trade_plan`

### Обязательность
- обязательный

---

## 2.4. `trade_thesis_snapshot`

### Кто вызывает
- тот же trader / worker agent

### Когда
- сразу после синтеза сигнала

### Профиль
- `MODEL_TRADER_PRIMARY`

### Выход
- structured `trade_thesis_snapshot`

### Обязательность
- обязательный

### Важное правило
- это часть ядра кейса
- без него evolution считается неполным

---

## 2.5. `trade_plan_semantic_audit`

### Кто вызывает
- либо тот же trader-agent как второй проход
- либо внутренний audit pass тем же session runner

### Профиль
- `MODEL_TRADER_AUDIT`

### Назначение
- semantic second opinion
- не имеет права блокировать технически валидный план в MVP

### Выход
- semantic flags
- contradiction hints
- confidence markers

---

## 3. Evolution LLM-вызовы

## 3.1. Общая схема committee

Для критических evolution decisions всегда использовать:

1. `Generator`
2. `Skeptic`
3. `Arbiter`

Это делается либо:
- тремя отдельными OpenClaw agent profiles,
- либо тремя отдельными isolated session запусками.

Канонический выбор для проекта:

> три отдельные agent role profile.

---

## 3.2. `outcome_analysis`

### Кто вызывает
- `evolver_generator_agent`

### Когда
- после терминального status case

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Вход
- full case bundle
- trade plan
- thesis snapshot
- outcome
- phenotype
- execution logs

### Выход
- structured outcome analysis

---

## 3.3. `fault_graph_tiebreaker`

### Кто вызывает
- `evolver_skeptic_agent` / `evolver_arbiter_agent`

### Когда
- только если deterministic fault graph оставил неоднозначность

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Выход
- blame refinement JSON

### Обязательность
- условный вызов, не всегда

---

## 3.4. `critic_pass`

### Кто вызывает
- `evolver_generator_agent`

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Назначение
- выделить слабое место skill
- выдать узкую, machine-usable критику

### Вход
- gene block text
- fault event
- counterfactual summary
- reflection capsules
- anti-pattern hits

### Выход
- `CritiqueReport`

---

## 3.5. `skeptic_pass`

### Кто вызывает
- `evolver_skeptic_agent`

### Назначение
- атаковать гипотезу critic-а
- искать leakage, self-justification, protocol drift

### Выход
- `SkepticReport`

---

## 3.6. `arbiter_pass`

### Кто вызывает
- `evolver_arbiter_agent`

### Назначение
- выбрать окончательный mutation path

### Выход
- `MutationDecision`

---

## 3.7. `rewrite_pass`

### Кто вызывает
- `evolver_generator_agent`

### Когда
- после арбитража, если разрешена мутация

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Выход
- candidate block replacement
- либо full candidate skill package

---

## 3.8. `validation_pass`

### Кто вызывает
- `evolver_arbiter_agent`
- optional second validator session

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Назначение
- semantic validation candidate
- protocol fit / output discipline fit

### Комментарий
- deterministic validator остаётся главным
- LLM validator — второе semantic opinion

---

## 3.9. `speciation_judge`

### Кто вызывает
- `evolver_arbiter_agent`

### Когда
- если phenotype divergence и статистика ветвления достаточны

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Выход
- branch vs family split decision

---

## 3.10. `recombination_composer`

### Кто вызывает
- `evolver_generator_agent`

### Когда
- только после прохождения deterministic recombination gate

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Выход
- hybrid candidate pack

---

## 3.11. `promotion_committee`

### Кто вызывает
- `evolver_generator_agent`
- `evolver_skeptic_agent`
- `evolver_arbiter_agent`

### Когда
- после arena evidence threshold

### Профиль
- `MODEL_EVOLVER_COMMITTEE`

### Выход
- `PROMOTE / KEEP / WATCHLIST / QUARANTINE / RETIRE`

---

## 4. Foundry and Research LLM calls

## 4.1. `foundry_skill_synthesis`

### Кто вызывает
- `skill_foundry_agent`

### Профиль
- `MODEL_FOUNDRY`

### Веб-доступ
- разрешён по allowlist source policy

### Что делает
- выделяет повторяемый паттерн из zero-skill кейсов
- превращает его в frame-compatible skill candidate

---

## 4.2. `foundry_contract_pass`

### Кто вызывает
- `skill_foundry_agent`

### Назначение
- привести новый skill к contract discipline

---

## 4.3. `research_retrieval`

### Кто вызывает
- `research_agent`

### Профиль
- `MODEL_RESEARCH`

### Веб-доступ
- только allowlist domains

### Выход
- evidence package

---

## 4.4. `research_synthesis`

### Кто вызывает
- `research_agent`

### Выход
- structured synthesis with citations

---

## 5. Overlay-related LLM calls

## 5.1. `overlay_optimizer`

### Кто вызывает
- `overlay_optimizer_agent`

### Профиль
- `MODEL_OVERLAY`

### Что делает
- улучшает `AGENTS.md` и `TOOLS.md` overlays
- не меняет freely `SOUL` / `IDENTITY`

### Обязательность
- optional subsystem

---

## 6. Полная матрица по агентам

| Workflow | Агент | Model profile | Web | Tools | Session type |
|---|---|---|---|---|---|
| frame_normalizer | prod/lab trader | `MODEL_TRADER_PRIMARY` | off | runtime only | new trade session |
| auto_skill_selector | prod/lab trader | `MODEL_TRADER_PRIMARY` | off | runtime only | new trade session |
| trade_plan_synthesis | prod/lab trader | `MODEL_TRADER_PRIMARY` | off by default | runtime + data tools | new trade session |
| thesis_snapshot | prod/lab trader | `MODEL_TRADER_PRIMARY` | off | runtime only | same session |
| semantic audit | prod/lab trader or audit pass | `MODEL_TRADER_AUDIT` | off | no execution write | same session |
| outcome_analysis | evolver_generator | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| fault_tiebreaker | evolver_skeptic/arbiter | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| critic_pass | evolver_generator | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| skeptic_pass | evolver_skeptic | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| arbiter_pass | evolver_arbiter | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| rewrite_pass | evolver_generator | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| validation_pass | evolver_arbiter | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| speciation_judge | evolver_arbiter | `MODEL_EVOLVER_COMMITTEE` | off | case artifacts | isolated evolver session |
| recombination_composer | evolver_generator | `MODEL_EVOLVER_COMMITTEE` | off | donor packs | isolated evolver session |
| promotion_committee | evolver committee | `MODEL_EVOLVER_COMMITTEE` | off | arena evidence | isolated evolver session |
| foundry_synthesis | skill_foundry | `MODEL_FOUNDRY` | allowlisted | no execution | isolated foundry session |
| research_retrieval | research | `MODEL_RESEARCH` | allowlisted | retrieval only | isolated research session |
| overlay_optimizer | overlay_optimizer | `MODEL_OVERLAY` | off by default | overlay refs | isolated overlay session |

---

## 7. Жёсткие запреты по LLM

1. Никакой LLM не имеет права:
   - напрямую записывать в canonical SQLite;
   - напрямую редактировать canonical registry;
   - отправлять ордер минуя deterministic execution bridge.
2. Ни один runtime-trader не должен видеть:
   - live/demo mode;
   - capital allocation layer;
   - execution secrets.
3. Ни один research call не должен обходить source allowlist.
4. Ни один mutation call не должен миновать deterministic validator.

---

## 8. Краткий operational вывод

LLM в SMART_TRADE — это не один “большой умный агент”, а **сетка специализированных semantic workers**, запускаемых OpenClaw в изолированных сессиях под контролем `SMART_TRADE orchestrator`.

Именно это позволяет:
- широко использовать LLM;
- не терять воспроизводимость;
- не размывать роли;
- не превращать trading runtime в хаотичный monologue одной модели.
