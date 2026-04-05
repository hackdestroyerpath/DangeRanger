# 27_RUNTIME_CONFIG_POLICY

## Назначение

Этот файл фиксирует, где живёт истина runtime-конфигов.

Он закрывает вопрос Codex:

> config files или env-only?

---

## 1. Решение

Выбран формат:

# `YAML + ENV`

Это окончательная политика.

---

## 2. Правило разделения ответственности

### YAML = каноническая versioned конфигурация проекта

В YAML хранятся:
- frame defaults
- evolution thresholds
- arena parameters
- lab composition
- source policy profiles
- feature flags
- agent role defaults

### ENV = только environment-specific и secret-specific слой

В ENV хранятся:
- токены
- ключи
- base URLs
- runtime paths
- deployment-specific ports
- включение/выключение конкретной среды

---

## 3. Приоритет

```text
project.yaml
-> frame YAML
-> specific profile YAML
-> ENV overrides (only allowed keys)
```

---

## 4. Что нельзя делать

### Нельзя делать env-only систему

Причина:
- теряется воспроизводимость baseline-конфигов
- сложнее сравнивать поведение разных версий
- Codex начнёт разносить runtime semantics по `.env`

### Нельзя делать YAML-only систему

Причина:
- secrets и deployment-specific endpoints не должны жить в versioned YAML

---

## 5. Обязательные загрузчики

Codex должен реализовать:

- `config_loader.py`
- `env_loader.py`
- `settings_resolver.py`

где итогом является единый `resolved_settings` объект.

---

## 6. Нормативный итог

Истина runtime-конфигов в первой версии:

- **структура и логика** -> YAML
- **секреты и среда** -> ENV

Точка.
