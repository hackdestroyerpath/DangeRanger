# 26_SINGLE_FRAME_BASELINE

## Назначение

Этот файл закрывает вопрос:

> первая реализация мульти-frame или строго single-frame?

Ответ фиксируется окончательно.

---

## 1. Решение

Первая реализация проекта строго ограничена одним baseline frame shard:

```text
binance_futures_btcusdc_1m
```

То есть:
- Exchange = `Binance`
- Market = `Futures`
- Symbol = `BTCUSDC`
- Timeframe = `1m`

---

## 2. Что это означает practically

### Разрешено в первой реализации

- конфиги могут поддерживать модель нескольких frame-шардов;
- таблицы могут быть спроектированы расширяемо;
- маршрутизация может быть generic.

### Но фактически запускать и проверять надо только один baseline shard

```text
binance_futures_btcusdc_1m
```

---

## 3. Что запрещено в первой coding-wave

Codex не должен:
- пытаться делать production-ready multi-symbol scheduler;
- пытаться активировать cross-frame routing;
- писать cross-frame recombination как рабочий контур;
- распараллеливать реальные production flows по нескольким symbols.

---

## 4. Для чего всё равно сохраняется generic architecture

Generic architecture сохраняется только затем, чтобы потом:
- расширить проект без ломки фундамента;
- но не чтобы усложнить первую поставку.

---

## 5. Нормативный итог

Для первой реализации baseline жёстко один:

```text
frame_shard_id = binance_futures_btcusdc_1m
```

Если Codex начинает писать первую волну так, будто проект уже multi-frame, это считается отклонением от baseline.
