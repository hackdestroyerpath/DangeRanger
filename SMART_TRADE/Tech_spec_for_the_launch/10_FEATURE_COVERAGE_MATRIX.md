# 10_FEATURE_COVERAGE_MATRIX

## Назначение

Этот файл нужен для последней проверки полноты.

Он отвечает на вопрос:

> все ли утверждённые в переписке крупные фичи реально покрыты пакетом спецификаций?

Если фича есть в этой матрице и у неё указан основной документ, значит она считается **явно покрытой**.

---

## Матрица покрытия

| Фича / решение | Статус | Где зафиксировано |
|---|---|---|
| `SMART_TRADE` = отдельный кодовый контур | Covered | `01_SMART_TRADE_MASTER_SPEC_MAX.md` §2 |
| `OpenSpace` = донор паттернов, не runtime dependency | Covered | `01` §2, `02_OPENSPACE_DONOR_MAP.md` |
| `OpenClaw` = shell / sessions / workspaces / skills | Covered | `01` §4, `03_OPENCLAW_AGENT_MODEL.md` |
| `1 кейс = 1 сигнал = max 1 сделка` | Covered | `01` §2, §14 |
| Нет пользовательского `NO_TRADE` в MVP | Covered | `01` §2, §14 |
| Пустой `ISOLATED` без подсказок | Covered | `01` §2, §9, `03` (zero-skill worker) |
| Универсальный data request tool | Covered | `01` §11 |
| `expected_fill_window_sec` vs `expected_fill_deadline` | Covered | `01` §12 |
| Агент не знает demo/live/capital | Covered | `01` §2, `03` |
| Отдельный `trade_thesis_snapshot` | Covered | `01` §6 |
| Technical validator не оценивает edge | Covered | `01` §13 |
| Фенотип считается 2 раза | Covered | `01` §15 |
| Фенотип не подсказывается пустому агенту | Covered | `01` §15 |
| Иерархия family / branch / version / gene | Covered | `01` §3, §16 |
| Arena / Sandbox / Tester разделены | Covered | `01` §17 |
| `arena_score` и `family_score` | Covered | `01` §17 |
| official expectancy на `R`, не на деньгах | Covered | `01` §18 |
| Tool quality + coverage monitor | Covered | `01` §19 |
| Source policy с allow/deny domains | Covered | `01` §20, `Smart_trade_requirments.MD` |
| Широкое использование LLM по семантическим шагам | Covered | `01` §21, `04_LLM_CALL_MATRIX.md` |
| Protocol Integrity Gate | Covered | `01` §22, `02_OPENSPACE_DONOR_MAP.md` |
| Hard / Soft Selection | Covered | `01` §22 |
| Local Mutation `1 child / 1 gene / 1 generation` | Covered | `01` §22 |
| Recombination gate | Covered | `01` §22 |
| Regime Speciation | Covered | `01` §22 |
| Structural Decomposition | Covered | `01` §22 |
| Skill Foundry | Covered | `01` §23 |
| Forward arena / lab lane | Covered | `01` §24, `03` |
| Skill packaging в OpenClaw-compatible вид | Covered | `01` §25, `07` |
| Полная SQLite truth model | Covered | `01` §26, `09_RESTORE_FROM_ZERO_AUDIT.md` |
| Physical project layout | Covered | `01` §27 |
| Coding roadmap | Covered | `01` §28, `06_IMPLEMENTATION_CHECKLIST.md`, examples |
| Exact SQL DDL | Covered | `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md` |
| Exact JSON schemas | Covered | `examples/35_34_kanonicheskie_json_schemas.md` |
| Exact APIs | Covered | `examples/36_35_internal_service_apis_i_openclaw_integration_api.md` |
| Exact LLM workflows | Covered | `04_LLM_CALL_MATRIX.md`, `examples/37_36_llm_workflows_kanonicheskie.md` |
| Lab workers count and process | Covered | `01` §7, `01` §38, `03` |
| OpenClaw bootstrap files per agent | Covered | `03`, `07_AGENT_BOOTSTRAP_TEMPLATES.md` |
| Human vs autonomous boundary | Covered | `05_HUMAN_AUTONOMY_MATRIX.md` |
| Infra / parsers / programs required to start | Covered | `Smart_trade_requirments.MD` |
| 1:1 reconstruction guarantee | Covered | `09_RESTORE_FROM_ZERO_AUDIT.md` |

---

## Что намеренно НЕ включено как обязательная часть MAX-pack

Ниже вещи, которые обсуждались как возможные будущие расширения, но **не утверждены как обязательные для текущей канонической версии**:

- portfolio allocator
- money management inside agent
- partial exits / laddered TP
- scale in / scale out
- full historical backtest engine as mandatory gate
- vector DB as обязательная часть MVP/MAX-core
- Kubernetes / distributed orchestration как обязательное условие

Если их добавлять позже, они должны идти как отдельный approved expansion.


## Дополнительное покрытие v4

| Feature | Status | Source |
|---|---|---|
| Max-approved late chat features | covered | `11_MAX_APPROVED_FEATURE_APPENDIX.md` |
| Codex start order | covered | `12_CODEX_START_HERE.md` |
| Codex part partitioning | covered | `13_CODEX_PARTITION_PLAN.md` |
| Codex execution protocol | covered | `14_CODEX_EXECUTION_PROTOCOL.md` |
| CODE_SKELETON_PACK | covered | `CODE_SKELETON_PACK/README.md` |


## Дополнительное покрытие v6

| Feature | Status | Source |
|---|---|---|
| Environment-level integration blockers from Codex | covered | files 17–23 |
| Execution bridge exact contract | covered | `17_EXECUTION_BRIDGE_CONTRACT.md` |
| Market data provider profile | covered | `18_MARKET_DATA_PROVIDER_PROFILE.md` |
| OpenClaw runtime API profile | covered | `19_OPENCLAW_RUNTIME_PROFILE.md` |
| Production baseline | covered | `20_PRODUCTION_BASELINE.md` |
| Price truth policy | covered | `21_PRICE_TRUTH_POLICY.md` |
| Env contract and placeholders | covered | `22_ENV_CONTRACT.md`, `.env.example` |
| Prod pilot acceptance | covered | `23_PROD_PILOT_ACCEPTANCE.md` |


## Codex blocker closure

| Feature | Status | Source |
|---|---|---|
| Tech baseline for Codex | covered | `24_TECH_BASELINE_FOR_CODEX.md` |
| First coding wave scope | covered | `25_FIRST_WAVE_DELIVERY_SCOPE.md` |
| Single-frame baseline confirmation | covered | `26_SINGLE_FRAME_BASELINE.md` |
| Runtime config policy | covered | `27_RUNTIME_CONFIG_POLICY.md` |
| Module DoD without tests | covered | `28_MODULE_DOD_NO_TESTS.md` |
