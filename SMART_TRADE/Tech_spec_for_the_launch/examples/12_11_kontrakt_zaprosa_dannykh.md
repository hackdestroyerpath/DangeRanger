# Примеры к разделу: 11. Контракт запроса данных

## Пример 1
Язык / тип: `text`

```text
request_market_data
```

## Пример 2
Язык / тип: `json`

```json
{
  "request_id": "uuid",
  "data_type": "string",
  "symbol": "BTCUSDC",
  "timeframe": "1m",
  "lookback": 300,
  "params": {
    "any_key": "any_value"
  },
  "output_format": "json|text|image|table"
}
```
