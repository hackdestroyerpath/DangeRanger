# 16_CROSS_REFERENCE_INDEX

## Назначение

Этот файл нужен как быстрый индекс по пакету.
Он отвечает на вопрос:

> “Где именно в архиве лежит конкретная тема?”

Использовать его как навигационную карту для команды и для Codex.

---

## 1. Базовая архитектура

| Тема | Где искать |
|---|---|
| Общая модель проекта | `01_SMART_TRADE_MASTER_SPEC_MAX.md` |
| Что брать из OpenSpace | `02_OPENSPACE_DONOR_MAP.md` |
| Какие агенты OpenClaw нужны | `03_OPENCLAW_AGENT_MODEL.md` |
| Где вызывается LLM | `04_LLM_CALL_MATRIX.md` |
| Что делает человек, что делает система | `05_HUMAN_AUTONOMY_MATRIX.md` |
| Короткий implementation view | `06_IMPLEMENTATION_CHECKLIST.md` |

---

## 2. Agent runtime / OpenClaw

| Тема | Где искать |
|---|---|
| Agent roles | `03_OPENCLAW_AGENT_MODEL.md` |
| Bootstrap files | `07_AGENT_BOOTSTRAP_TEMPLATES.md` |
| Materialization и allowlist | `03_OPENCLAW_AGENT_MODEL.md`, `CODE_SKELETON_PACK/smart_trade/openclaw_bridge/` |
| Codex start order | `12_CODEX_START_HERE.md` |

---

## 3. Торговый runtime

| Тема | Где искать |
|---|---|
| Frame model | `01_SMART_TRADE_MASTER_SPEC_MAX.md` |
| Signal contract | `examples/13_12_kontrakt_torgovogo_plana.md` |
| Data request contract | `examples/12_11_kontrakt_zaprosa_dannykh.md` |
| Terminal statuses | `examples/15_14_sostoyaniya_i_terminalnye_kody_keysa.md` |
| Physical project tree | `examples/28_27_fizicheskaya_struktura_proekta.md` |

---

## 4. Эволюция

| Тема | Где искать |
|---|---|
| Arena / Sandbox / Tester | `examples/18_17_arena_sandbox_tester.md` |
| Expectancy и метрики | `examples/19_18_matozhidanie_i_proizvodnye_metriki.md` |
| Tool quality / coverage | `examples/20_19_tool_quality_coverage_monitor.md` |
| Evolution core | `examples/23_22_evolyutsionnoe_yadro_mvp.md` |
| Phenotype / family / recombination | `08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL.md` |
| MAX approved late features | `11_MAX_APPROVED_FEATURE_APPENDIX.md` |

---

## 5. Схемы данных и API

| Тема | Где искать |
|---|---|
| SQL DDL | `examples/34_33_sql_ddl_kanonicheskaya_sqlite_schema.md` |
| JSON schemas | `examples/35_34_kanonicheskie_json_schemas.md` |
| Internal APIs | `examples/36_35_internal_service_apis_i_openclaw_integration_api.md` |
| LLM workflows | `examples/37_36_llm_workflows_kanonicheskie.md` |
| Lab orchestration | `examples/39_38_lab_workers_forward_arena_orchestration.md` |
| Overlay + source policy execution | `examples/40_39_overlay_evolution_and_source_policy_execution.md` |
| Filesystem artifacts | `examples/41_40_filesystem_artifacts.md` |

---

## 6. Codex handoff

| Тема | Где искать |
|---|---|
| Куда смотреть Codex первым | `12_CODEX_START_HERE.md` |
| Разбиение по частям | `13_CODEX_PARTITION_PLAN.md` |
| Как кормить Codex | `14_CODEX_EXECUTION_PROTOCOL.md` |
| Skeleton pack | `CODE_SKELETON_PACK/README.md` |
| Статус частей | `CODE_SKELETON_PACK/PART_STATUS.md` |
| Проектное дерево | `CODE_SKELETON_PACK/PROJECT_TREE.txt` |

---

## 7. Аудит и полнота

| Тема | Где искать |
|---|---|
| Достаточность для восстановления 1:1 | `09_RESTORE_FROM_ZERO_AUDIT.md` |
| Покрытие фич | `10_FEATURE_COVERAGE_MATRIX.md` |
| Финальный релиз-аудит | `15_FINAL_RELEASE_AUDIT.md` |

---

## 8. Что считать source of truth

### Канон
1. `01_SMART_TRADE_MASTER_SPEC_MAX.md`
2. companion docs
3. examples
4. code skeleton

### Не считать source of truth
- любые старые склейки и промежуточные черновики вне пакета
- production code
- устные договорённости, не попавшие в архив


## 9. Environment-level integration

| Тема | Где искать |
|---|---|
| Execution bridge contract | `17_EXECUTION_BRIDGE_CONTRACT.md` |
| Market data providers | `18_MARKET_DATA_PROVIDER_PROFILE.md` |
| OpenClaw runtime profile | `19_OPENCLAW_RUNTIME_PROFILE.md` |
| Production baseline | `20_PRODUCTION_BASELINE.md` |
| Price truth policy | `21_PRICE_TRUTH_POLICY.md` |
| Env contract | `22_ENV_CONTRACT.md` |
| Prod pilot acceptance | `23_PROD_PILOT_ACCEPTANCE.md` |
