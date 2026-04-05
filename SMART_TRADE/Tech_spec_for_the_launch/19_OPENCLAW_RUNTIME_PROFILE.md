# 19_OPENCLAW_RUNTIME_PROFILE

## Назначение

Этот файл фиксирует **рабочий профиль интеграции с OpenClaw**, чтобы Codex не гадал:
- какие agent workspaces нужны;
- как materialize skills;
- как спавнить session;
- что делать с hooks / webhooks / sub-agents;
- какие ограничения sandbox/FS/network учитывать.

---

## 1. Версия и принцип

Работать с актуальным OpenClaw runtime, но код строить через **adapter layer**, а не через жёсткую привязку к одной внутренней версии.

Нормативное правило:
- OpenClaw integration реализуется как `openclaw_bridge`;
- прямой runtime-specific code вне bridge запрещён.

---

## 2. Обязательные agent roles

### Production
- `prod_trader_agent` — `1` на активный `frame_shard`

### Lab workers
- `lab_baseline_worker_agent` — `4`
- `lab_challenger_worker_agent` — `4`
- `lab_niche_worker_agent` — `2`
- `lab_zero_skill_worker_agent` — `2`

### Evolution committee
- `evolver_generator_agent` — `1`
- `evolver_skeptic_agent` — `1`
- `evolver_arbiter_agent` — `1`

### Growth/support
- `skill_foundry_agent` — `1`
- `research_agent` — `1`

---

## 3. Workspace model

У каждого агента должен быть:
- свой `agentId`
- свой `agentDir`
- свой `workspace`
- свой skill allowlist
- свой overlay set

Truth не хранится в workspace.
Workspace = materialized runtime copy.

---

## 4. Canonical operations required from openclaw_bridge

1. `materialize_workspace(agent_role, frame_shard)`
2. `materialize_skills(agent_role, frame_shard, selected_pool)`
3. `materialize_overlays(agent_role, overlay_set)`
4. `spawn_session(agent_role, prompt_bundle)`
5. `collect_artifacts(session_id)`
6. `shutdown_session(session_id)`

---

## 5. Hooks / webhooks / sub-agents

### Hooks
Используются только как runtime tool-layer OpenClaw.

### Webhooks
Основной outcome webhook идёт в `SMART_TRADE`, а не в агент напрямую.

### Sub-agents
Допустимы для:
- skeptic
- arbiter
- research micro-tasks

Но production торговый проход не должен требовать обязательного fan-out в подагентов.

---

## 6. Sandbox / filesystem / network rules

### Filesystem
Агенту доступны только materialized runtime directories.

### Network
Network policy зависит от роли:
- `prod_trader_agent` -> только нужные smart-trade tools / bridge routes / research if allowed
- `lab workers` -> как минимум то же, плюс tester hooks
- `evolver/research` -> web access по source policy

### Important
Пустой isolated runtime не должен падать из-за отсутствия trading skills.

---

## 7. Retries / timeouts for OpenClaw calls

Стартовые значения:
- session spawn timeout: `60s`
- artifact collect timeout: `30s`
- materialization timeout: `30s`
- retry attempts: `3`
- exponential backoff: `1s -> 2s -> 4s`

Если runtime call не удался после retries:
- кейс не мутирует;
- создаётся infra event;
- возможно safe rerun кейса, если сигнал ещё не был отправлен.

---

## 8. Что Codex не должен делать

Не надо:
- хардкодить локальные пути моей среды;
- хардкодить реальные agent IDs;
- хардкодить реальные OpenClaw tokens;
- выдумывать новые роли агентов вне spec.

Нужно:
- сделать adapter interfaces;
- env-based paths/URLs;
- workspace materialization rules;
- tests с mock OpenClaw runtime.
