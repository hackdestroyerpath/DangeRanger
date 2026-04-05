# Примеры к разделу: 40. Filesystem artifacts

## Пример 1
Язык / тип: `text`

```text
cases/<case_id>/
  00_frame_original.md
  01_frame_resolved.json
  02_materialization.json
  03_data_requests.json
  04_data_artifacts/
  05_signal_plan.json
  06_trade_thesis_snapshot.json
  07_validation_report.json
  08_execution_request.json
  09_execution_events.jsonl
  10_pretrade_phenotype.json
  11_outcome_webhook.json
  12_posttrade_phenotype.json
  13_outcome_capsule.json
  14_fault_graph.json
  15_counterfactual_variants.json
  16_mutation_plan.json
  17_candidate_skill_manifest.json
  18_promotion_decision.json
  19_case_report.md
```

## Пример 2
Язык / тип: `text`

```text
skills/<skill_family_id>/<branch_id>/<skill_version_id>/
  SKILL.md
  contract.json
  gene_map.json
  phenotype_scope.json
  lineage.json
  mutation_note.md
  references/
```

## Пример 3
Язык / тип: `text`

```text
overlays/<overlay_type>/<overlay_version_id>/
  content.md
  manifest.json
  lineage.json
```
