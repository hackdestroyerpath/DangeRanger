# Примеры к разделу: 18. Матожидание и производные метрики

## Пример 1
Язык / тип: `text`

```text
realized_R = (exit_price - entry_fill_price) / (entry_fill_price - stop_loss)
```

## Пример 2
Язык / тип: `text`

```text
realized_R = (entry_fill_price - exit_price) / (stop_loss - entry_fill_price)
```

## Пример 3
Язык / тип: `text`

```text
net_R = realized_R - fee_R - slippage_R
```

## Пример 4
Язык / тип: `text`

```text
net_R = realized_R
```

## Пример 5
Язык / тип: `text`

```text
trade_expectancy_N = mean(net_R over official filled cases)
```

## Пример 6
Язык / тип: `text`

```text
trade_expectancy = P(win) * AvgWinR - P(loss) * AvgLossR
```
