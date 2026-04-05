# Примеры к разделу: 33. SQL DDL (каноническая SQLite schema)

## Пример 1
Язык / тип: `sql`

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA foreign_keys=ON;
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=268435456;
```

## Пример 2
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS frames (
    frame_id TEXT PRIMARY KEY,
    frame_family_id TEXT NOT NULL,
    exchange TEXT NOT NULL,
    market TEXT NOT NULL,
    symbol_scope_json TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    fee_pct REAL NOT NULL,
    execution_rules_json TEXT NOT NULL,
    skill_mode_default TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_policy_profiles (
    source_policy_id TEXT PRIMARY KEY,
    frame_id TEXT,
    allow_domains_json TEXT NOT NULL,
    deny_domains_json TEXT NOT NULL,
    freshness_date TEXT,
    citation_required INTEGER NOT NULL DEFAULT 1,
    allow_open_web INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    FOREIGN KEY(frame_id) REFERENCES frames(frame_id)
);

CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    frame_family_id TEXT NOT NULL,
    frame_shard_id TEXT NOT NULL,
    mode TEXT NOT NULL,
    actor_agent_id TEXT NOT NULL,
    skill_family_id TEXT,
    skill_version_id TEXT,
    status TEXT NOT NULL,
    terminal_reason TEXT,
    created_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY(frame_id) REFERENCES frames(frame_id)
);
CREATE INDEX IF NOT EXISTS idx_cases_frame_status ON cases(frame_shard_id, status);
CREATE INDEX IF NOT EXISTS idx_cases_skill_version ON cases(skill_version_id);

CREATE TABLE IF NOT EXISTS case_events (
    event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);
CREATE INDEX IF NOT EXISTS idx_case_events_case ON case_events(case_id, created_at);

CREATE TABLE IF NOT EXISTS signal_plans (
    signal_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL UNIQUE,
    frame_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,
    entry_limit REAL NOT NULL,
    stop_loss REAL NOT NULL,
    take_profit REAL NOT NULL,
    expected_fill_window_sec INTEGER,
    expected_fill_deadline_ts TEXT NOT NULL,
    skill_family_id TEXT,
    skill_version_id TEXT,
    thesis_short TEXT,
    plan_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS trade_thesis_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL UNIQUE,
    signal_id TEXT NOT NULL UNIQUE,
    skill_family_id TEXT,
    skill_version_id TEXT,
    why_entry TEXT NOT NULL,
    why_sl TEXT NOT NULL,
    why_tp TEXT NOT NULL,
    why_eta TEXT,
    requested_data_summary_json TEXT NOT NULL,
    key_observations_json TEXT NOT NULL,
    self_critic_note TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id),
    FOREIGN KEY(signal_id) REFERENCES signal_plans(signal_id)
);

CREATE TABLE IF NOT EXISTS data_requests (
    request_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    data_type TEXT NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT,
    lookback_json TEXT,
    params_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);
CREATE INDEX IF NOT EXISTS idx_data_requests_case ON data_requests(case_id);

CREATE TABLE IF NOT EXISTS data_artifacts (
    artifact_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    result_kind TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    as_of_ts TEXT,
    payload_json TEXT NOT NULL,
    semantic_ok INTEGER,
    freshness_ok INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY(request_id) REFERENCES data_requests(request_id),
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS coverage_gaps (
    gap_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    request_id TEXT,
    frame_id TEXT NOT NULL,
    data_type TEXT NOT NULL,
    params_json TEXT NOT NULL,
    reason_code TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS execution_events (
    exec_event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id),
    FOREIGN KEY(signal_id) REFERENCES signal_plans(signal_id)
);

CREATE TABLE IF NOT EXISTS outcome_events (
    outcome_event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL UNIQUE,
    signal_id TEXT NOT NULL UNIQUE,
    outcome_code TEXT NOT NULL,
    submitted_at TEXT,
    filled_at TEXT,
    closed_at TEXT,
    entry_fill_price REAL,
    exit_price REAL,
    operator_intervened INTEGER NOT NULL DEFAULT 0,
    raw_payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id),
    FOREIGN KEY(signal_id) REFERENCES signal_plans(signal_id)
);
```

## Пример 3
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS case_phenotypes (
    phenotype_event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    pretrade_phenotype_key TEXT,
    posttrade_phenotype_key TEXT,
    pretrade_probe_json TEXT NOT NULL,
    posttrade_probe_json TEXT,
    llm_adjustments_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);
CREATE INDEX IF NOT EXISTS idx_case_phenotypes_case ON case_phenotypes(case_id);

CREATE TABLE IF NOT EXISTS skill_metrics_windows (
    metrics_id TEXT PRIMARY KEY,
    frame_shard_id TEXT NOT NULL,
    skill_family_id TEXT NOT NULL,
    skill_version_id TEXT NOT NULL,
    phenotype_key TEXT,
    n_official_10 INTEGER NOT NULL,
    n_official_30 INTEGER NOT NULL,
    n_official_100 INTEGER NOT NULL,
    e10 REAL NOT NULL,
    e30 REAL NOT NULL,
    e100 REAL NOT NULL,
    pf30 REAL NOT NULL,
    pf100 REAL NOT NULL,
    fill_rate_30 REAL NOT NULL,
    timeout_rate_30 REAL NOT NULL,
    invalid_rate_30 REAL NOT NULL,
    stability_score REAL NOT NULL,
    regime_fit_score REAL NOT NULL,
    freshness_score REAL NOT NULL,
    pain_score REAL NOT NULL,
    arena_score REAL NOT NULL,
    family_relative_rank REAL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(metrics_id),
    UNIQUE(frame_shard_id, skill_version_id, phenotype_key)
);
CREATE INDEX IF NOT EXISTS idx_skill_metrics_rank ON skill_metrics_windows(frame_shard_id, arena_score DESC);
```

## Пример 4
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS skill_families (
    skill_family_id TEXT PRIMARY KEY,
    frame_family_id TEXT NOT NULL,
    frame_shard_id TEXT NOT NULL,
    origin_type TEXT NOT NULL,
    family_scope TEXT NOT NULL,
    contract_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS skill_versions (
    skill_version_id TEXT PRIMARY KEY,
    skill_family_id TEXT NOT NULL,
    branch_id TEXT NOT NULL,
    parent_version_id TEXT,
    contract_version TEXT NOT NULL,
    status TEXT NOT NULL,
    niche_key TEXT,
    mutation_type TEXT,
    mutation_intensity TEXT,
    file_path TEXT NOT NULL,
    created_by_agent TEXT,
    created_at TEXT NOT NULL,
    activated_at TEXT,
    retired_at TEXT,
    FOREIGN KEY(skill_family_id) REFERENCES skill_families(skill_family_id),
    FOREIGN KEY(parent_version_id) REFERENCES skill_versions(skill_version_id)
);
CREATE INDEX IF NOT EXISTS idx_skill_versions_family_status ON skill_versions(skill_family_id, status);

CREATE TABLE IF NOT EXISTS skill_contracts (
    skill_version_id TEXT PRIMARY KEY,
    input_contract_json TEXT NOT NULL,
    output_contract_json TEXT NOT NULL,
    phenotype_scope_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(skill_version_id) REFERENCES skill_versions(skill_version_id)
);

CREATE TABLE IF NOT EXISTS skill_gene_map (
    gene_map_id TEXT PRIMARY KEY,
    skill_version_id TEXT NOT NULL UNIQUE,
    contract_version TEXT NOT NULL,
    blocks_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(skill_version_id) REFERENCES skill_versions(skill_version_id)
);

CREATE TABLE IF NOT EXISTS skill_router_weights (
    weight_id TEXT PRIMARY KEY,
    frame_shard_id TEXT NOT NULL,
    skill_version_id TEXT NOT NULL,
    phenotype_key TEXT,
    routing_weight REAL NOT NULL,
    keep_alive_floor REAL NOT NULL,
    weight_source TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(frame_shard_id, skill_version_id, phenotype_key)
);
```

## Пример 5
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS mutations (
    mutation_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    skill_family_id TEXT NOT NULL,
    from_skill_version_id TEXT NOT NULL,
    to_skill_version_id TEXT,
    mutation_type TEXT NOT NULL,
    target_gene TEXT,
    mutation_plan_json TEXT NOT NULL,
    critic_report_json TEXT,
    rewriter_report_json TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS recombinations (
    recombination_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    child_skill_version_id TEXT,
    parent_a_skill_version_id TEXT NOT NULL,
    parent_b_skill_version_id TEXT NOT NULL,
    compatibility_score REAL NOT NULL,
    selected_blocks_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS speciation_events (
    speciation_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    parent_skill_family_id TEXT NOT NULL,
    child_skill_family_id TEXT,
    parent_skill_version_id TEXT NOT NULL,
    niche_key TEXT NOT NULL,
    trigger_summary_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS decomposition_events (
    decomposition_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    parent_skill_version_id TEXT NOT NULL,
    created_children_json TEXT NOT NULL,
    trigger_summary_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS fault_events (
    fault_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    primary_fault_gene TEXT NOT NULL,
    secondary_faults_json TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    confidence REAL NOT NULL,
    resolver_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS counterfactual_variants (
    variant_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    source_skill_version_id TEXT NOT NULL,
    entry_limit REAL,
    stop_loss REAL,
    take_profit REAL,
    timeout_sec INTEGER,
    filled INTEGER NOT NULL,
    terminal_reason TEXT,
    realized_r REAL,
    censored INTEGER NOT NULL DEFAULT 0,
    summary_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS extinction_memory (
    anti_pattern_id TEXT PRIMARY KEY,
    frame_shard_id TEXT NOT NULL,
    phenotype_key TEXT,
    signature_hash TEXT NOT NULL,
    scope TEXT NOT NULL,
    confidence REAL NOT NULL,
    penalty_weight REAL NOT NULL,
    evidence_cases_json TEXT NOT NULL,
    decays_after_ts TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    UNIQUE(frame_shard_id, signature_hash)
);

CREATE TABLE IF NOT EXISTS reflection_capsules (
    capsule_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    capsule_type TEXT NOT NULL,
    skill_family_id TEXT,
    skill_version_id TEXT,
    phenotype_key TEXT,
    gene_block TEXT,
    capsule_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS curriculum_queue (
    queue_id TEXT PRIMARY KEY,
    frame_shard_id TEXT NOT NULL,
    phenotype_key TEXT,
    gene_block TEXT,
    reason TEXT NOT NULL,
    priority REAL NOT NULL,
    source_json TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_at TEXT NOT NULL,
    closed_at TEXT
);
```

## Пример 6
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS arena_assignments (
    assignment_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL UNIQUE,
    frame_shard_id TEXT NOT NULL,
    bucket_key TEXT NOT NULL,
    skill_family_id TEXT NOT NULL,
    assigned_skill_version_id TEXT NOT NULL,
    role TEXT NOT NULL,
    split_policy TEXT NOT NULL,
    routing_score_snapshot REAL NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS arena_results (
    arena_result_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL UNIQUE,
    frame_shard_id TEXT NOT NULL,
    bucket_key TEXT NOT NULL,
    skill_version_id TEXT NOT NULL,
    arena_score_after REAL NOT NULL,
    official_r REAL,
    timeout_flag INTEGER NOT NULL DEFAULT 0,
    invalid_flag INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY(case_id) REFERENCES cases(case_id)
);

CREATE TABLE IF NOT EXISTS promotion_events (
    promotion_id TEXT PRIMARY KEY,
    frame_shard_id TEXT NOT NULL,
    skill_family_id TEXT NOT NULL,
    from_skill_version_id TEXT,
    to_skill_version_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    decision_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

## Пример 7
Язык / тип: `sql`

```sql
CREATE TABLE IF NOT EXISTS tool_quality_events (
    tool_quality_event_id TEXT PRIMARY KEY,
    case_id TEXT,
    tool_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    technical_ok INTEGER,
    semantic_ok INTEGER,
    latency_ms INTEGER,
    payload_summary_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_runs (
    research_run_id TEXT PRIMARY KEY,
    source_policy_id TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_ref_id TEXT NOT NULL,
    query_text TEXT NOT NULL,
    selected_sources_json TEXT NOT NULL,
    synthesis_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS llm_judgments (
    llm_judgment_id TEXT PRIMARY KEY,
    case_id TEXT,
    subject_type TEXT NOT NULL,
    subject_ref_id TEXT NOT NULL,
    workflow_name TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    output_json TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

## Пример 8
Язык / тип: `sql`

```sql
CREATE VIEW IF NOT EXISTS v_active_skill_versions AS
SELECT sv.*
FROM skill_versions sv
WHERE sv.status IN ('CHAMPION','CHALLENGER','NICHE','WATCHLIST');

CREATE VIEW IF NOT EXISTS v_frame_latest_metrics AS
SELECT *
FROM skill_metrics_windows;
```
