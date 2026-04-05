# Примеры к разделу: 35. Internal service APIs и OpenClaw integration API

## Пример 1
Язык / тип: `python`

```python
class FrameEngine:
    def resolve_frame(self, frame_md: str) -> dict: ...

class SkillMaterializer:
    def materialize(self, frame_resolved: dict) -> dict: ...

class TraderRuntime:
    def run_case(self, case_id: str, materialized_env: dict) -> dict: ...

class ExecutionBridge:
    def submit_order(self, order_request: dict) -> dict: ...

class OutcomeIngest:
    def handle_webhook(self, payload: dict) -> None: ...

class EvolutionOrchestrator:
    def on_terminal_case(self, case_id: str) -> None: ...
```

## Пример 2
Язык / тип: `json`

```json
{ "frame_md": "string", "operator_note": "string|null" }
```

## Пример 3
Язык / тип: `json`

```json
{ "case_id": "uuid", "frame_id": "...", "agent_session_spec": {} }
```

## Пример 4
Язык / тип: `json`

```json
{
  "case_id": "uuid",
  "signal_id": "uuid",
  "status": "accepted|rejected",
  "validation_report": {}
}
```
