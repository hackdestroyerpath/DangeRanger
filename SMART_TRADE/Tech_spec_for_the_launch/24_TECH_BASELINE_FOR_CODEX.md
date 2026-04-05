# 24_TECH_BASELINE_FOR_CODEX

## Назначение

Этот файл закрывает для Codex вопрос:

> какой технологический стек считать **обязательным baseline** для первой реализации backend-а.

Начиная с этой версии пакета, этот стек считается **жёстко выбранным**. Альтернативы без отдельного разрешения не допускаются.

---

## 1. Язык и рантайм

- `Python 3.12`
- типизация обязательна
- timezone-aware UTC only

---

## 2. HTTP / API framework

Выбранный стандарт:

- `FastAPI`
- `Uvicorn`

Использовать для:
- internal HTTP endpoints
- webhook receiver
- execution bridge client-facing adapters
- health/readiness endpoints

---

## 3. Схемы и валидация

Выбранный стандарт:

- `Pydantic v2`

Использовать для:
- request/response models
- JSON contract validation
- env/config parsing
- structured LLM outputs

Допускается `jsonschema` как вспомогательный слой только там, где нужен explicit JSON-schema export, но **основной стандарт — Pydantic v2**.

---

## 4. HTTP client stack

Выбранный стандарт:

- `httpx`

Использовать для:
- execution bridge calls
- market data provider calls
- OpenClaw runtime calls
- research retrieval adapters (если не требуется браузерный слой)

---

## 5. Scheduler / job orchestration

Выбранный стандарт для первой волны:

- `APScheduler`
- `asyncio` task groups / background tasks

Использовать для:
- lab scheduling
- family rebalance cadence
- evolution jobs
- research jobs
- cleanup/archive jobs

### Что не использовать в первой волне

Не вводить в первой волне:
- Celery
- Redis queues
- Kafka
- Airflow
- Temporal

Если потом понадобится масштабирование — это отдельный evolution stage, но **не baseline первого кода**.

---

## 6. База и доступ к БД

Выбранный стандарт:

- `SQLite`
- `sqlite3` standard library as canonical low-level driver
- raw SQL + repository layer

### Что это значит

- не использовать ORM как основной путь истины;
- migrations хранить как SQL files;
- repository layer писать руками.

Допускается вспомогательное использование `aiosqlite` для async adapters, но **каноническая SQL-модель и truth layer должны опираться на raw SQL**.

---

## 7. Тестовый baseline

Выбранный стандарт:

- `pytest`

Использовать для:
- smoke tests
- repository tests
- contract validation tests
- integration smoke

---

## 8. Линтеры и качество кода

Выбранный baseline:

- `ruff`
- `mypy`

---

## 9. Нормативный итог

Codex должен считать, что для первой coding-wave технологический baseline закрыт так:

- Python 3.12
- FastAPI + Uvicorn
- Pydantic v2
- HTTPX
- APScheduler + asyncio
- SQLite + raw SQL + repository layer
- pytest
- ruff
- mypy

Никаких дополнительных технологических развилок Codex вводить не должен.
