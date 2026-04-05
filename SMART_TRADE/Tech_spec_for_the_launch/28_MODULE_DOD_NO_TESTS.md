# 28_MODULE_DOD_NO_TESTS

## Назначение

Этот файл задаёт `DoD` (Definition of Done) для части / модуля в режиме:

> код считается готовым даже если полный тестовый контур ещё не написан

Это закрывает вопрос Codex:

> по каким признакам модуль можно считать завершённым без полного test suite?

---

## 1. Общий DoD без тестов

Любой модуль считается завершённым без полного набора тестов только если одновременно выполнено всё:

1. **Import clean**
   - модуль импортируется без ошибок
   - нет knowingly broken imports

2. **Contract complete**
   - все модели / схемы / интерфейсы модуля реализованы по spec

3. **Manual smoke path exists**
   - есть один CLI / service / direct-call сценарий ручной проверки

4. **Artifacts/logs appear**
   - модуль создаёт ожидаемые записи в БД / логах / артефактах

5. **No spec deviation**
   - модуль не меняет терминологию и не упрощает проектную логику

6. **Status files updated**
   - `PART_STATUS.md`, `CHANGELOG.md`, `TODO.md` обновлены

7. **Next-step note present**
   - явно записано, какие тесты и доработки нужны потом

---

## 2. Minimal manual smoke examples

### Для `frame_engine`
- подать `FRAME.MD`
- получить `frame_resolved.json`

### Для `runtime_core`
- создать case
- провести его до `PLAN_VALIDATED`

### Для `execution_bridge`
- сформировать request
- получить stub/ack response

### Для `webhook_receiver`
- отправить webhook payload
- увидеть terminal event в БД

### Для `expectancy_monitor`
- вставить outcome events
- увидеть пересчитанные окна

### Для `skill_registry`
- зарегистрировать family/version
- материализовать runtime copy

### Для `arena`
- подать metrics
- получить routing weights

---

## 3. Что НЕ считается DoD

Следующее не считается “готово”:

- написаны только dataclasses без workflow;
- написаны только TODO-заглушки;
- нет ручного smoke пути;
- нет записей в артефактах;
- нет обновления status-файлов;
- есть логические расхождения со spec.

---

## 4. Нормативный вывод

До полного test suite модуль всё ещё может быть принят как `DONE_WITHOUT_TESTS`, но только по правилам выше.

Это и есть обязательный baseline DoD для первой coding-wave.
