# 23_PROD_PILOT_ACCEPTANCE

## Назначение

Этот файл фиксирует критерии:
- “часть завершена”;
- “пакет готов к интеграции”;
- “система готова к прод-пилоту”.

---

## 1. Release acceptance per PART

Каждый PART считается закрытым, если:

1. реализован его основной scope из `13_CODEX_PARTITION_PLAN.md`;
2. обновлены:
   - `PART_STATUS.md`
   - `CHANGELOG.md`
   - `TODO.md`
3. есть минимум smoke tests для новых модулей;
4. нет knowingly broken imports;
5. нет отклонения от spec.

---

## 2. Минимальные интеграционные тесты

### 2.1. Case lifecycle smoke

Сценарий:
- frame resolve
- skill materialization
- trader session
- trade_plan accepted
- execution submit ack
- outcome webhook
- case terminal
- evolution job created

### 2.2. Coverage gap path

Сценарий:
- agent requests unsupported data type
- coverage gap created
- case terminal = `BLOCKED_BY_DATA_COVERAGE`
- no trading mutation performed

### 2.3. Invalid plan path

Сценарий:
- malformed geometry
- `PLAN_INVALID`
- no execution submit
- protocol event logged

### 2.4. Timeout path

Сценарий:
- pending limit not filled
- timeout reached
- `ORDER_CANCELLED_TIMEOUT`
- no official expectancy update

### 2.5. Mutation path

Сценарий:
- official cases reach threshold
- fault graph identifies gene
- critic + rewriter + validator produce candidate
- candidate packaged and registered

### 2.6. Recombination path

Сценарий:
- two parents pass admission gate
- child challenger created
- lineage updated

### 2.7. Empty isolated path

Сценарий:
- isolated directory empty
- agent still starts
- no hidden method instruction injected
- case can run and log outputs

---

## 3. Prod-pilot readiness criteria

Система считается готовой к прод-пилоту, если выполнено всё:

1. all critical schemas created
2. all required env variables validated at startup
3. execution bridge contract implemented
4. webhook auth + idempotency implemented
5. case lifecycle smoke passes
6. coverage gap path passes
7. invalid plan path passes
8. timeout path passes
9. mutation path passes
10. empty isolated path passes
11. no secrets leak into artifacts/logs/workspaces
12. OpenClaw materialization works for prod + lab agents
13. lineage entries are append-only
14. routing weights recompute deterministically
15. recovery after duplicate webhook confirmed

---

## 4. Rollback triggers

Rollback / freeze required if any:
- execution bridge unstable
- webhook auth broken
- duplicated case submission unresolved
- official `R` calculation mismatch found
- routing weights drift non-deterministically
- mutation produced invalid packaged skill into active lane

---

## 5. Final rule

Пока этот файл не закрыт по всем пунктам, production pilot нельзя считать безопасно стартуемым.
