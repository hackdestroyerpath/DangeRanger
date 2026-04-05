# SMART_TRADE spec pack — README

## Что это

Это полный пакет спецификаций `SMART_TRADE` в текущей максимальной утверждённой версии.

Пакет собран так, чтобы:
- главный файл был единственной канонической спецификацией;
- companion docs раскрывали отдельные контуры без дублирования;
- кодовые примеры были вынесены отдельно;
- разработчики могли работать одновременно по “библии” и по короткому checklist.

---

## Состав пакета

### Главное
- `01_SMART_TRADE_MASTER_SPEC_MAX.md`

### Companion docs
- `15_FINAL_RELEASE_AUDIT.md`
- `16_CROSS_REFERENCE_INDEX.md`
- `02_OPENSPACE_DONOR_MAP.md`
- `03_OPENCLAW_AGENT_MODEL.md`
- `04_LLM_CALL_MATRIX.md`
- `05_HUMAN_AUTONOMY_MATRIX.md`
- `06_IMPLEMENTATION_CHECKLIST.md`
- `07_AGENT_BOOTSTRAP_TEMPLATES.md`
- `08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL.md`
- `09_RESTORE_FROM_ZERO_AUDIT.md`
- `10_FEATURE_COVERAGE_MATRIX.md`
- `11_MAX_APPROVED_FEATURE_APPENDIX.md`
- `12_CODEX_START_HERE.md`
- `13_CODEX_PARTITION_PLAN.md`
- `14_CODEX_EXECUTION_PROTOCOL.md`
- `Smart_trade_requirments.MD`
- `CODE_SKELETON_PACK/README.md`

### Вынесенные примеры
- папка `examples/`

### Meta
- `SPEC_PACK_MANIFEST.json`

---

## Как читать

1. Сначала прочитать `01_SMART_TRADE_MASTER_SPEC_MAX.md`
2. Затем `03_OPENCLAW_AGENT_MODEL.md`
3. Затем `04_LLM_CALL_MATRIX.md`
4. Затем `02_OPENSPACE_DONOR_MAP.md`
5. Затем `05_HUMAN_AUTONOMY_MATRIX.md`
6. Для ежедневной работы держать рядом `06_IMPLEMENTATION_CHECKLIST.md`
7. `examples/` открывать только по мере необходимости

---

## Что намеренно не включено

- старые дублирующие версии файлов
- склеенные промежуточные документы как отдельные источники истины
- устаревшие reference snapshots, если они дублируют основной spec

---

## Главный принцип

Если companion docs противоречат `01_SMART_TRADE_MASTER_SPEC_MAX.md`, приоритет всегда у `01_SMART_TRADE_MASTER_SPEC_MAX.md`.


## Принцип 1:1-восстановления

Этот пакет считается достаточным только если по нему можно заново восстановить проект `SMART_TRADE` без обращения к старому production-коду. Для этого в пакет добавлен `09_RESTORE_FROM_ZERO_AUDIT.md`.


## Что добавлено в v3

- формализована роль фенотипа, skill family, branches и рекомбинации;
- добавлен отдельный файл инфраструктурных требований `Smart_trade_requirments.MD`;
- добавлен аудит полноты пакета для восстановления кода 1:1;
- пакет очищен от дублирующих исходных склеек и содержит только канонические и вспомогательные файлы.


## Что добавлено в v4

- добавлен `11_MAX_APPROVED_FEATURE_APPENDIX.md` с финальными max-approved уточнениями из чата;
- архив оптимизирован под Codex через `12_CODEX_START_HERE.md`, `13_CODEX_PARTITION_PLAN.md`, `14_CODEX_EXECUTION_PROTOCOL.md`;
- добавлен `CODE_SKELETON_PACK/` с канонической кодовой структурой и статус-файлами для пошаговой реализации;
- обновлены центральные файлы пакета с ссылками на новые Codex-ориентированные артефакты.


## Что добавлено в v5

- добавлен `15_FINAL_RELEASE_AUDIT.md` как последний gate перед передачей в Codex;
- добавлен `16_CROSS_REFERENCE_INDEX.md` как сквозная карта по всему пакету;
- обновлены `00_README.md`, `12_CODEX_START_HERE.md` и `SPEC_PACK_MANIFEST.json`;
- пакет ещё раз проверен на логическую цельность и полноту относительно утверждённых в чате решений.
