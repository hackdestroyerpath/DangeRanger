# 11_MAX_APPROVED_FEATURE_APPENDIX

## Назначение

Этот файл фиксирует **дополнительные утверждённые фичи максимальной версии**, которые были согласованы в чате после основной сборки пакета.

Это не альтернативная спецификация, а **нормативное дополнение** к:
- `01_SMART_TRADE_MASTER_SPEC_MAX.md`
- `08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL.md`
- `10_FEATURE_COVERAGE_MATRIX.md`

Если информация здесь детальнее, чем в базовом файле, использовать более детальную формулировку отсюда.

---

## 1. Market shift detection

Система должна различать четыре уровня уверенности смены рынка:

1. `EARLY_ALERT`
2. `WORKING_SUSPICION`
3. `ROUTING_SWITCH_READY`
4. `NICHE_BRANCH_READY`

### 1.1. Пороговые зоны по числу официальных терминальных кейсов внутри bucket

- `EARLY_ALERT` -> `5–7` кейсов
- `WORKING_SUSPICION` -> `10–12` кейсов
- `ROUTING_SWITCH_READY` -> `15–20` кейсов
- `NICHE_BRANCH_READY` -> `20–30` кейсов

### 1.2. Что считается сменой рынка

`market_shift_alert = true`, если одновременно:
- `ME_10 < 0`
- `ME_30` заметно хуже предыдущего стабильного окна
- `loss_density` выше порога
- `current phenotype_key` отличается от исторически сильного phenotype_key skill-линии
- альтернативная линия в этом фенотипе показывает лучший `routing_score`

---

## 2. Champion is not always chosen

Система **не выбирает чемпиона всегда**.
Она работает через `sample_by_weight`, а не `choose_best`.

### 2.1. Нормативное правило

- Champion получает наибольший case-flow
- Но routing всегда вероятностный и bounded
- Монополия запрещена

### 2.2. Hard bounds

- `max_weight_per_skill <= 0.35`
- `keep_alive_floor >= 0.05`
- `sandbox_cap <= 0.15`

---

## 3. Sandbox / Tester / Arena — не одно и то же

### 3.1. `sandbox`
Безопасная среда и ограничение риска.

### 3.2. `tester`
Исполнитель прогонов skill-версий.

### 3.3. `arena`
Логика сравнения skill-версий.

Нормативная вложенность:

```text
Sandbox
└── Tester
    └── Arena logic
```

---

## 4. Phenotype: роль и ограничения

### 4.1. Где phenotype НЕ влияет

Phenotype не должен:
- подсказываться агенту в `ISOLATED + empty`
- диктовать метод генерации сигнала
- подменять протокол

### 4.2. Где phenotype влияет

Phenotype влияет на:
- `routing`
- `arena bucketization`
- `mutation targeting`
- `speciation`
- `extinction memory`
- `recombination filter`

### 4.3. Двойной расчёт phenotype

- `pre-trade phenotype` -> для routing
- `post-trade phenotype` -> для evolution

### 4.4. Кто считает phenotype

Не агент.
Только:
- deterministic probe/tagger
- optional LLM audit

---

## 5. Skill family / branch / phenotype hierarchy

Нормативная схема:

```text
FRAME FAMILY
> FRAME SHARD
> SKILL FAMILY
> BRANCH / SUBSPECIES
> SKILL VERSION
> GENE BLOCK
```

Phenotype — не выше и не ниже skill. Он **ортогонален skill-структуре**.

### 5.1. Эквиваленты

- `skill_family` = вид
- `branch` = подвид / нишевая или ремонтная линия
- `skill_version` = конкретная версия организма внутри подвида
- `phenotype` = состояние среды, в которой организм живёт

---

## 6. Recombination and phenotype distance

### 6.1. Разрешение на скрещивание

Recombination допускается только если:
- родители в одном `frame_shard`
- имеют один `contract_version`
- не находятся в `QUARANTINED` / `REJECTED`
- имеют `similarity < 0.80`
- имеют разные сильные стороны
- `phenotype_distance <= threshold`

### 6.2. Разрешённые классы

- identical phenotype -> best case
- adjacent phenotypes -> allowed with caution
- distant phenotypes -> forbidden in MVP

### 6.3. Что именно может комбинироваться

Разрешено:
- `entry_policy`
- `sl_policy`
- `tp_policy`
- `timeout_policy`
- `eta_policy`
- частично `interpretation_policy`

Осторожно:
- `data_request_policy`
- `idea_source_policy`

Запрещено к прямому recombination:
- `protocol contract`
- `output discipline` как самостоятельный донор
- execution / infra logic

---

## 7. Fate of stale champion

Если skill A просел, а skill B вырос в новом фенотипе, система не переписывает A напрямую под B.

Разрешённые действия:
- `A` остаётся как `niche` или `watchlist`
- создаётся `A'` как repair-child
- создаётся `C` как recombination child от `A` и `B`, если admission gate проходит
- `B` может стать новым `champion`

Запрещено:
- уничтожать старую линию только потому, что рынок сменился
- переписывать A “под B” без lineage

---

## 8. expected_fill_window_sec vs expected_fill_deadline

### 8.1. `expected_fill_window_sec`

Это **оценка агента**:
- когда он ожидает нормальный fill
- нужна для `eta_accuracy`
- нужна человеку как ориентир актуальности сигнала

### 8.2. `expected_fill_deadline`

Это **системный kill-switch**:
- определяется `entry_timeout_sec`
- после этого момента неисполненная заявка считается умершей

### 8.3. Связь

- `window` < `deadline`
- `window` обучаемо
- `deadline` — policy, а не hypothesis

---

## 9. Evolution discipline imported from Evolution_TRADe

Подтверждено как обязательное:

1. `Post-Trade Evolution Controller`
2. `Protocol Integrity Gate`
3. `Composite Routing Score`
4. `Mutation Ladder`
5. `Recombination Admission Gate`
6. `Soft Selection Rehabilitation Gate`
7. `Two-Mode Hard Selection`
8. `Immutable Lineage Ledger`
9. `Family Rebalance Cadence`

Эти сущности считаются обязательной частью максимальной версии и уже должны существовать в проектном архиве.
