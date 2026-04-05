# 12_CODEX_START_HERE

## Назначение

Этот файл оптимизирует весь пакет под **Codex от OpenAI**.

Задача: скормить Codex весь архив и получать код **частями**, где:
- один запрос = одна часть проекта;
- каждая часть даёт около `~5000` строк кода;
- после последней части готово не менее `80%` кодовой базы.

---

## 1. Что Codex должен читать в первую очередь

Порядок чтения обязателен:

1. `00_README.md`
2. `01_SMART_TRADE_MASTER_SPEC_MAX.md`
3. `11_MAX_APPROVED_FEATURE_APPENDIX.md`
4. `03_OPENCLAW_AGENT_MODEL.md`
5. `04_LLM_CALL_MATRIX.md`
6. `02_OPENSPACE_DONOR_MAP.md`
7. `Smart_trade_requirments.MD`
8. `10_FEATURE_COVERAGE_MATRIX.md`
9. `12_CODEX_PARTITION_PLAN.md`
10. `13_CODEX_EXECUTION_PROTOCOL.md`
11. `17_EXECUTION_BRIDGE_CONTRACT.md`
12. `18_MARKET_DATA_PROVIDER_PROFILE.md`
13. `19_OPENCLAW_RUNTIME_PROFILE.md`
14. `20_PRODUCTION_BASELINE.md`
15. `21_PRICE_TRUTH_POLICY.md`
16. `22_ENV_CONTRACT.md`
17. `23_PROD_PILOT_ACCEPTANCE.md`
18. `CODE_SKELETON_PACK/README.md`

Если Codex начинает писать код, не прочитав эти файлы, результат считается потенциально дефектным.

---

## 2. Главные правила работы Codex

1. Не менять проектную логику.
2. Не упрощать контракты без явного указания.
3. Не придумывать альтернативную архитектуру.
4. Не смешивать production и lab контуры.
5. Не менять терминологию.
6. Не трогать файлы вне текущей части, кроме:
   - `PART_STATUS.md`
   - `CHANGELOG.md`
   - `TODO.md`
7. Не удалять никакие файлы из архива.
8. Все новые файлы создавать **внутри `CODE_SKELETON_PACK/` или рабочих каталогов проекта**, а не хаотично рядом.

---

## 3. Главный принцип под Codex

Codex должен работать по модели:

```text
read spec -> implement one part -> run local checks -> update part status -> stop
```

Не нужно пытаться “закончить весь проект за один проход”.

---

## 4. Что Codex обязан обновлять после каждой части

После завершения части Codex обязан обновить:

- `CODE_SKELETON_PACK/PART_STATUS.md`
- `CODE_SKELETON_PACK/CHANGELOG.md`
- `CODE_SKELETON_PACK/TODO.md`

Если этого не произошло, часть считается незавершённой.

---

## 5. Что Codex не должен делать

- не сокращать спецификацию;
- не удалять старые блоки “как дубли”, если это не разрешено явно;
- не менять `frame` semantics;
- не удалять пустой `ISOLATED` режим;
- не превращать `expected_fill_window_sec` в kill switch;
- не превращать `expected_fill_deadline` в поле, задаваемое агентом;
- не вводить пользовательский `NO_TRADE`;
- не упрощать arena до “всегда выбирай champion”.

---

## 6. Где Codex должен брать основу кода

1. Из `CODE_SKELETON_PACK/`
2. Из `02_OPENSPACE_DONOR_MAP.md`
3. Из `03_OPENCLAW_AGENT_MODEL.md`
4. Из `04_LLM_CALL_MATRIX.md`

Если у модуля есть donor reference на OpenSpace, Codex сначала смотрит его.
Если у модуля есть OpenClaw runtime binding, Codex сначала смотрит agent/bridge model.

---

## 7. Результат

Если соблюдать этот протокол, Codex будет работать не как хаотичный генератор кода, а как **пошаговый исполнитель проектной спецификации**.


## Дополнительно перед стартом

Перед началом реализации Codex должен один раз проверить:

1. `15_FINAL_RELEASE_AUDIT.md`
2. `16_CROSS_REFERENCE_INDEX.md`
3. `10_FEATURE_COVERAGE_MATRIX.md`

Это нужно, чтобы не потерять late-approved фичи и не реализовать только “удобный срез” проекта.


## 8. Статус готовности

После появления файлов `17`–`23` пакет считается **готовым к кодингу на 100%** в исполнительном режиме, кроме реальных секретов, которые пользователь вставляет сам в своей среде.
