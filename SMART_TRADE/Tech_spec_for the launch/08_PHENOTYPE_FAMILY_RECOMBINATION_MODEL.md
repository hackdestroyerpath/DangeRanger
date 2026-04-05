# 08_PHENOTYPE_FAMILY_RECOMBINATION_MODEL

## Назначение

Этот файл — формальная карта отношений между:

- `frame_family`
- `frame_shard`
- `skill_family`
- `branch`
- `skill_version`
- `phenotype`
- `arena`
- `sandbox`
- `tester`
- `recombination`

Его цель: исключить двусмысленность при реализации routing, speciation и скрещивания skill-линий.

---

## 1. Иерархия

```text
PROJECT
└── FRAME FAMILY
    └── FRAME SHARD
        └── SKILL FAMILY
            └── BRANCH
                └── SKILL VERSION
                    └── GENE BLOCK
```

### 1.1. Что выше / что ниже

- `frame_family` — общий класс среды
- `frame_shard` — основная единица изоляции эволюции
- `skill_family` — эволюционный “вид”
- `branch` — подвид / ремонтная / нишевая / гибридная ветка
- `skill_version` — конкретная версия внутри ветки
- `gene_block` — минимальный эволюционный блок

`phenotype` не находится выше или ниже этой иерархии. Он является **ортогональной координатой среды**, которая применяется к кейсу и к skill-статистике.

---

## 2. Формальная роль фенотипа

### 2.1. Фенотип не равен skill

Фенотип — это описание состояния рынка / среды, а не описания skill-а.

Пример: 

```text
dir=up|vol=expansion|liq=thin|session=us
```

### 2.2. Когда считается фенотип

Фенотип считается дважды:

1. `pretrade_probe` — до генерации сигнала
2. `posttrade_regime_tagger` — после терминального исхода

### 2.3. Кто считает фенотип

Фенотип считает только серверный контур `SMART_TRADE`:

- детерминированный probe
- optional LLM audit

Агент не получает phenotype как подсказку в режиме без навыка.

### 2.4. На что влияет фенотип

Фенотип влияет на:

- routing skill version
- arena bucket
- speciation decisions
- mutation targeting
- recombination compatibility
- extinction memory scope
- curriculum queue

Фенотип не влияет на:

- формат сигнала
- protocol contract
- deterministic validation
- способ мышления пустого `ISOLATED` агента

---

## 3. Skill family как вид

### 3.1. Определение

`skill_family` = основная эволюционная линия с единым смыслом, lineage и contract-version.

### 3.2. Как появляется новая family

Разрешены 4 источника рождения family:

1. ручной seed skill
2. auto-synthesis через `Skill Foundry`
3. speciation, если divergence структурная
4. recombination child, если гибрид устойчив и требует новой линии

### 3.3. Branch

`branch` = подвид skill family.

Допустимые типы branch:

- `main`
- `repair_<gene>`
- `niche_<phenotype_slug>`
- `hybrid_<slug>`

---

## 4. Размножение и наследование

### 4.1. Version mutation

```text
parent version -> child version
```

Меняется 1 gene-block или 1–2 low-level параметра внутри него.

### 4.2. Repair child

```text
A@main -> A@repair_entry_branch
```

Создаётся, если skill family жива, но fault graph стабильно обвиняет локальный gene-block.

### 4.3. Speciation child

```text
A@main -> A@niche_dir_up_vol_expansion
```

Создаётся, если имеется phenotype-specific divergence.

### 4.4. Recombination child

```text
A + B -> C
```

или

```text
A@main + A@range_branch -> A@hybrid_range_entry
```

---

## 5. Когда skill-и можно скрещивать

### 5.1. Разрешённые случаи

#### A. Внутри одной family

Самый безопасный тип recombination.

#### B. Между families внутри одного `frame_shard`

Разрешено только если:

- same `frame_shard`
- same `contract_version`
- `similarity < 0.80`
- родители не weak / not quarantined
- есть complementarity по gene-blocks

### 5.2. Запрещённые случаи

Нельзя:

- `weak × weak`
- `clone × clone`
- `quarantined × anything`
- parents with protocol/integrity flag
- cross-frame_shard recombination в `MVP`
- cross-exchange / cross-market recombination в `MVP`

### 5.3. Phenotype-distance gate

Вводится функция:

```text
phenotype_distance(parent_a, parent_b)
```

Грубое правило `MVP`:

- distance `0` = одинаковый phenotype scope → recombination допустима
- distance `1` = близкий phenotype → допустима с critic approval
- distance `>=2` = запрещена

---

## 6. Что именно можно комбинировать

### 6.1. Свободно комбинируемые блоки

- `entry_policy`
- `sl_policy`
- `tp_policy`
- `timeout_policy`
- `eta_policy`

### 6.2. Условно комбинируемые блоки

- `data_request_policy`
- `interpretation_policy`

Только если совпадает input contract и нет противоречия по данным.

### 6.3. Некомбинируемые блоки

- protocol contract
- deterministic validation rules
- core output format

Эти вещи одинаковы на уровне системы, а не skill-line.

---

## 7. Arena / Sandbox / Tester

### 7.1. Различия

- `sandbox` = безопасная среда
- `tester` = исполнитель кейсов в sandbox
- `arena` = логика сравнения skill versions

### 7.2. Связь

```text
Sandbox
└── Tester
    └── Arena logic
```

### 7.3. Практический смысл

- sandbox ограничивает последствия
- tester генерирует практику
- arena перераспределяет case-flow

---

## 8. Что происходит со старым skill, когда рынок сменился

Старый skill не “забывается” сразу. Возможны состояния:

- `active`
- `watchlist`
- `niche`
- `quarantined`
- `retired`

Допустимые реакции системы:

1. оставить старый skill как niche
2. снизить его weight
3. создать repair-child
4. создать niche-child
5. создать recombined child

Запрещено делать прямой overwrite:

```text
A был -> A переписали под B
```

Правильный путь:

```text
A сохраняется
B усиливается
A' тестируется
C-гибрид появляется как challenger
```

---

## 9. Итоговые правила реализации

1. `skill_family` = вид
2. `branch` = подвид / repair / niche / hybrid
3. `phenotype` = состояние среды, не skill
4. recombination только внутри `frame_shard` в `MVP`
5. phenotype влияет на routing, arena, mutation, speciation, extinction, recombination
6. phenotype не должен быть прямой подсказкой агенту в пустом режиме
7. ни один skill не стирается “сразу”, пока не пройдёт path: `watchlist -> quarantine -> retired`
