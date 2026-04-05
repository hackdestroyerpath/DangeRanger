# 17_EXECUTION_BRIDGE_CONTRACT

## Назначение

Этот файл фиксирует **точный внешний контракт execution bridge**, чтобы команда и Codex не гадали:
- куда слать сигнал;
- как выполнять отмену;
- как получать статус;
- как принимать outcome;
- как работать с auth и idempotency.

Этот файл обязателен для реализации `execution_bridge/` и `webhook_receiver/`.

---

## 1. Принцип

`SMART_TRADE` никогда не торгует напрямую на бирже.
Он всегда общается с промежуточным `execution bridge`.

Execution bridge отвечает за:
- submit order;
- cancel pending order;
- status/fills lookup;
- outcome webhook обратно в `SMART_TRADE`.

---

## 2. Base URL

Никаких hardcoded адресов.

Использовать только:

```text
EXECUTION_BRIDGE_BASE_URL
```

---

## 3. HTTP endpoints

### 3.1. Submit order

```text
POST /v1/execution/orders
```

### 3.2. Cancel pending order

```text
POST /v1/execution/orders/cancel
```

### 3.3. Order status

```text
GET /v1/execution/orders/{signal_id}
```

### 3.4. Fills / execution details

```text
GET /v1/execution/fills/{signal_id}
```

### 3.5. Outcome webhook -> SMART_TRADE

```text
POST /v1/execution/outcomes
```

---

## 4. Auth

### 4.1. SMART_TRADE -> execution bridge

Headers:

```text
Authorization: Bearer <EXECUTION_BRIDGE_TOKEN>
X-Idempotency-Key: <idempotency_key>
Content-Type: application/json
```

### 4.2. execution bridge -> SMART_TRADE webhook

Headers:

```text
X-Signature: <HMAC_SHA256(raw_body, EXECUTION_WEBHOOK_SECRET)>
Content-Type: application/json
```

### 4.3. Запрещено

- хранить реальные токены внутри `SKILL.md`
- хранить реальные токены внутри OpenClaw workspace
- логировать реальные секреты в артефакты кейса

---

## 5. Idempotency

### 5.1. Submit order

Формула:

```text
submit_idempotency_key = sha256(
  case_id + signal_id + symbol + side + entry_limit + stop_loss + take_profit
)
```

### 5.2. Outcome webhook

Формула:

```text
outcome_idempotency_key = sha256(
  case_id + signal_id + outcome_code + closed_at
)
```

### 5.3. Правило

Все дубли определяются только через эти ключи.
Повторный webhook / повторный submit не должен ломать state machine.

---

## 6. Error envelope

Единый формат ошибок:

```json
{
  "code": "STRING_CODE",
  "message": "human readable message",
  "retryable": true,
  "details": {}
}
```

### 6.1. Обязательные codes

- `AUTH_FAILED`
- `INVALID_PAYLOAD`
- `DUPLICATE_REQUEST`
- `UPSTREAM_TIMEOUT`
- `UPSTREAM_UNAVAILABLE`
- `ORDER_REJECTED`
- `NOT_FOUND`
- `INTERNAL_ERROR`

### 6.2. Mapping rule

- `retryable=true` -> runtime может safe-retry по policy
- `retryable=false` -> кейс переходит в terminal/non-terminal resolution по state machine

---

## 7. Canonical request/response payloads

### 7.1. Submit request

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "frame_id": "binance_futures_btcusdc_1m",
  "symbol": "BTCUSDC",
  "side": "LONG",
  "entry_limit": 101250.0,
  "stop_loss": 100900.0,
  "take_profit": 101950.0,
  "entry_timeout_sec": 300,
  "metadata": {
    "skill_family_id": "Lite_TRADING_SKILL_01_04_2026",
    "skill_version_id": "Lite_TRADING_SKILL_01_04_2026@main@v18"
  }
}
```

### 7.2. Submit ack

```json
{
  "signal_id": "uuid",
  "accepted": true,
  "bridge_order_id": "string",
  "submitted_at": "2026-04-05T12:35:03Z"
}
```

### 7.3. Cancel request

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "reason": "ENTRY_TIMEOUT"
}
```

### 7.4. Status response

```json
{
  "signal_id": "uuid",
  "state": "PENDING_FILL|OPEN|CANCELLED|CLOSED",
  "submitted_at": "...",
  "filled_at": null,
  "closed_at": null,
  "bridge_order_id": "string"
}
```

### 7.5. Outcome webhook

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "symbol": "BTCUSDC",
  "side": "LONG",
  "submitted_at": "2026-04-05T12:35:03Z",
  "filled_at": "2026-04-05T12:39:10Z",
  "entry_fill_price": 101248.5,
  "closed_at": "2026-04-05T13:02:18Z",
  "exit_price": 101950.0,
  "outcome_code": "TP_HIT",
  "operator_intervened": false,
  "raw_payload": {}
}
```

---

## 8. Timeout semantics

### 8.1. Pending entry timeout

Если заявка не исполнилась до `entry_timeout_sec`, execution bridge обязан:
- отменить pending order;
- отправить `ORDER_CANCELLED_TIMEOUT` webhook outcome.

### 8.2. Position timeout

В `MVP` и max-approved baseline:
- отключён.
- открытая позиция живёт до `TP_HIT`, `SL_HIT` или `OPERATOR_INTERVENED`.

---

## 9. Что Codex не должен делать

Не надо:
- подставлять реальные URL;
- подставлять реальные bearer tokens;
- подставлять реальные HMAC secrets;
- привязываться к конкретному продовому DNS.

Нужно сделать:
- интерфейсы;
- клиентские адаптеры;
- env placeholders;
- validators;
- tests на envelope и idempotency.
