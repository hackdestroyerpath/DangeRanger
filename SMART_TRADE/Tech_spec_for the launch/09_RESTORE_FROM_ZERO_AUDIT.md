# 09_RESTORE_FROM_ZERO_AUDIT

## Назначение

Этот файл отвечает на вопрос:

> достаточно ли текущего пакета, чтобы при полной потере production-кода восстановить проект 1:1 по логике, механике и структуре?

Короткий ответ: **да, при условии дисциплинированного следования пакету**.

---

## 1. Что именно должно быть восстановлено 1:1

Восстановлению подлежит не буквальный стиль кода, а следующее:

1. state machine кейса
2. frame-модель
3. skill hierarchy
4. contracts JSON/SQL
5. порядок post-trade evolution
6. правила protocol gate / hard / soft selection
7. arena scoring и routing
8. phenotype computation и buckets
9. роли агентов и их bootstrap surfaces
10. policy границы: source policy, overlays, autonomy boundaries

Если команда реализует эти пункты буквально по пакету, поведение проекта должно совпасть 1:1 по логике.

---

## 2. Что в пакете является канонической истиной

### Главный файл
- `01_SMART_TRADE_MASTER_SPEC_MAX.md`

### Нормативные companion docs
- `02_OPENSPACE_DONOR_MAP.md`
- `03_OPENCLAW_AGENT_MODEL.md`
- `04_LLM_CALL_MATRIX.md`
- `05_HUMAN_AUTONOMY_MATRIX.md`
- `07_AGENT_BOOTSTRAP_TEMPLATES.md`
- `08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL.md`
- `Smart_trade_requirments.MD`

### Операционный контроль
- `06_IMPLEMENTATION_CHECKLIST.md`

### Не являются канонической истиной
- `examples/` — это поясняющие и ускоряющие примеры, но не замена основному spec

---

## 3. Чего в пакете достаточно для восстановления

### 3.1. Архитектуры
Да.

### 3.2. Деревьев каталогов
Да.

### 3.3. SQL schema
Да.

### 3.4. JSON contracts
Да.

### 3.5. Agent model
Да.

### 3.6. LLM workflows
Да.

### 3.7. Policy boundaries
Да.

### 3.8. Recovery / idempotency
Да.

### 3.9. Hidden assumptions
Нет. Они должны считаться отсутствующими. Если предположение не зафиксировано в пакете, его нельзя внедрять.

---

## 4. Что команда не имеет права “додумывать”

1. нельзя вводить user-facing `NO_TRADE` в MVP
2. нельзя подсказывать пустому isolated агенту метод анализа
3. нельзя мутировать protocol / execution bridge
4. нельзя хранить truth только в workspace OpenClaw
5. нельзя считать деньги главным fitness target
6. нельзя делать cross-frame recombination в MVP
7. нельзя держать торговую сессию открытой до исхода сделки

Любая такая “инициатива” считается отклонением от проекта.

---

## 5. Проверка полноты пакета

### Пакет считается достаточным, если по нему можно без внешних пояснений восстановить:

- сервисы
- БД
- API
- job orchestration
- агентные роли
- файловую структуру
- routing
- arena
- evolution
- требования к инфраструктуре

Текущий пакет этому условию соответствует.

---

## 6. Что остаётся вариативным и может отличаться между командами

Допускаются различия только в:

- стиле кода
- именах отдельных функций
- выборе ORM / SQL wrapper
- способе packaging ZIP/CI/CD
- конкретных вспомогательных библиотеках

Но не допускаются различия в:

- semantics
- state machine
- formulas
- contracts
- roles
- source policy
- evolution logic

---

## 7. Итог

Если production-код будет потерян, а пакет останется, то по нему можно восстановить проект 1:1 **по логике, механике, ограничениям и поведению**.

Это и есть критерий достаточности пакета.
