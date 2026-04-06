# readiness_to_write_code

## Итоговая оценка готовности к написанию кода (как кодер-исполнитель)

**Готовность: 100%**

С учётом новых нормативных уточнений от пользователя (backend-стек, первая coding-wave, single-frame baseline, runtime config policy, DoD без полного test-suite) проект готов к исполнению **без дополнительных архитектурных вопросов**.

---

## Что зафиксировано и закрывает прежние блокеры

1. **Обязательный backend-стек**
   - Python 3.12
   - FastAPI + Uvicorn
   - Pydantic v2
   - HTTPX
   - APScheduler + asyncio
   - SQLite + raw SQL + repository layer
   - pytest, ruff, mypy

2. **Первая coding-wave**
   - Реализация идёт строго по `PART 01 -> PART 10`.
   - Это и есть “основная часть” для первой поставки.

3. **Baseline первой реализации**
   - Первая версия строго single-frame:
     - `binance_futures_btcusdc_1m`
     - Exchange = Binance Futures
     - Symbol = BTCUSDC
     - Timeframe = 1m
   - Generic-архитектура сохраняется, но multi-frame поведение в первой wave не активируется.

4. **Политика runtime-конфигов**
   - Модель: **YAML + ENV**.
   - YAML = versioned каноническая конфигурация.
   - ENV = secrets и environment-specific endpoints/paths.

5. **DoD без полного тестового покрытия**
   Модуль считается `DONE_WITHOUT_TESTS`, только если выполнено:
   1) import clean
   2) contract complete
   3) manual smoke path exists
   4) artifacts/logs appear
   5) no spec deviation
   6) status files updated
   7) next-step note present

---

## Что не требуется от пользователя на текущем шаге

Сейчас не нужно запрашивать:
- реальные API keys
- реальные токены
- реальные URLs
- реальные runtime paths
- реальные OpenClaw secrets
- реальные execution bridge secrets

Используются placeholders и env loaders. Реальные значения пользователь подставляет позже в своей среде.

---

## Исполнительский режим с этого момента

1. Работать по порядку:
   - `12_CODEX_START_HERE.md`
   - `13_CODEX_PARTITION_PLAN.md`
   - реализация `PART 01` (затем дальше по порядку)

2. После завершения каждого PART обновлять:
   - `CODE_SKELETON_PACK/PART_STATUS.md`
   - `CODE_SKELETON_PACK/CHANGELOG.md`
   - `CODE_SKELETON_PACK/TODO.md`

3. Новые архитектурные уточнения по указанным 5 пунктам **не требуются**.
