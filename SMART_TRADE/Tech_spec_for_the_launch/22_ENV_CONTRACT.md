# 22_ENV_CONTRACT

## Назначение

Этот файл задаёт **обязательный env-контракт** для первого запуска.

Всё, что зависит от реальной среды пользователя, должно браться отсюда.

---

## 1. Обязательные переменные

### SMART_TRADE core

```text
SMART_TRADE_ENV
SMART_TRADE_DB_PATH
SMART_TRADE_ARTIFACTS_DIR
SMART_TRADE_LOG_LEVEL
SMART_TRADE_FRAME_DEFAULT
```

### Execution bridge

```text
EXECUTION_BRIDGE_BASE_URL
EXECUTION_BRIDGE_TOKEN
EXECUTION_WEBHOOK_SECRET
```

### LLM

```text
OPENAI_API_KEY
LLM_PRIMARY_MODEL
LLM_FALLBACK_MODEL
LLM_TIMEOUT_SEC
```

### OpenClaw

```text
OPENCLAW_BASE_URL
OPENCLAW_AGENT_ROOT
OPENCLAW_WORKSPACE_ROOT
OPENCLAW_DEFAULT_TIMEOUT_SEC
OPENCLAW_AUTH_TOKEN
```

### Source policy

```text
SOURCE_POLICY_PROFILE
SOURCE_ALLOWLIST_FILE
SOURCE_DENYLIST_FILE
RESEARCH_WEB_ENABLED
```

### Optional market data routing

```text
MARKET_DATA_BASE_URL
MARKET_DATA_TOKEN
MARKET_DATA_CACHE_DIR
```

---

## 2. Root .env.example

```dotenv
SMART_TRADE_ENV=dev
SMART_TRADE_DB_PATH=./var/smart_trade.db
SMART_TRADE_ARTIFACTS_DIR=./var/artifacts
SMART_TRADE_LOG_LEVEL=INFO
SMART_TRADE_FRAME_DEFAULT=binance_futures_btcusdc_1m

EXECUTION_BRIDGE_BASE_URL=http://localhost:8001
EXECUTION_BRIDGE_TOKEN=CHANGE_ME
EXECUTION_WEBHOOK_SECRET=CHANGE_ME

OPENAI_API_KEY=CHANGE_ME
LLM_PRIMARY_MODEL=gpt-5.4-pro
LLM_FALLBACK_MODEL=gpt-5.4-pro
LLM_TIMEOUT_SEC=120

OPENCLAW_BASE_URL=http://localhost:3000
OPENCLAW_AGENT_ROOT=./openclaw_agents
OPENCLAW_WORKSPACE_ROOT=./openclaw_workspaces
OPENCLAW_DEFAULT_TIMEOUT_SEC=60
OPENCLAW_AUTH_TOKEN=CHANGE_ME

SOURCE_POLICY_PROFILE=source_policy_scalping_v1
SOURCE_ALLOWLIST_FILE=./config/source_allowlist.txt
SOURCE_DENYLIST_FILE=./config/source_denylist.txt
RESEARCH_WEB_ENABLED=true

MARKET_DATA_BASE_URL=http://localhost:8002
MARKET_DATA_TOKEN=CHANGE_ME
MARKET_DATA_CACHE_DIR=./var/market_cache
```

---

## 3. Что Codex не должен делать

Codex не должен:
- подставлять реальные ключи;
- пытаться узнать реальные пути в моей среде;
- хардкодить реальные токены;
- шить реальные DNS/paths в код.

Codex должен:
- использовать эти имена переменных;
- сделать loaders / validators;
- сделать `.env.example` и `env_loader.py`.
