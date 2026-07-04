# Repo Evidence

- Roadmap root: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` lists `MI-100.B Production Live Delivery`.
- Upstream gate: `scripts/external-validation-live-proof-gate.py` consumes `fatecat.external_validation_live_evidence_bundle`.
- Existing live summary producers:
  - `scripts/live-release-gate.py` for production API、HF Space、Telegram Bot checks.
  - `scripts/postgres-public-webhook-live-smoke.py` for public webhook delivery smoke.
  - `scripts/multi-surface-semantic-diff.py` for local semantic parity evidence.
- Current task output:
  - `contracts/fate/audit/production-live-delivery-evidence-bundle.json`
  - `scripts/production-live-delivery-evidence-bundle.py`
  - `tests/regression/test_production_live_delivery_evidence_bundle.py`

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No real credentials in repo | Output excludes URL/token/secret/DSN/webhook secret and report body |
| No over-claim | Pending mode remains successful local gate but `external_connectivity_pending` |
| Existing live proof schema | Reuse `contracts/fate/audit/schemas/external-validation-live-evidence.schema.json` |
| Category runbook truth | Consume category runbook id and fix invalid Bot command |
| Local CI cost | Add one small Python gate and one focused regression file |

# Change Boundary

- Allowed: audit contract, scripts, regression tests, local-ci wiring, AGENTS, roadmap, task docs.
- Not allowed: production provider algorithms, report rendering, API behavior, real deployment config, real secrets.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Raw live summary contains URL | Assembler hashes the artifact and never copies the URL |
| Live summary contains secret assignment | Assembler rejects sensitive-looking inline assignments |
| Proof-ref missing | Assembler emits no live proof for that work item |
| Runbook mismatch | 0123 live proof gate remains the authoritative verifier |
| Multi-surface local diff mistaken for live | `delivery.multi_surface_live` also requires API/HF/Bot pass in live-release-gate |

# Assumptions and Falsification

- Assumption: real live summaries are generated outside the repo and passed as local JSON paths. Falsifier: operator needs a remote evidence store; then add proof-ref resolver instead of copying artifacts.
- Assumption: live-release-gate remains the source for API/HF/Bot status. Falsifier: dedicated Bot JSON smoke is added; then add a new adapter category without changing live proof schema.

# Critical Ambiguities

None for this slice. Real production credentials and endpoint ownership remain external execution inputs, not design ambiguities.

# Debug Evidence Contract

- 调试模式: `Optional`

Not required. This is a new gate/contract slice with regression coverage, not a reproduced bug. The invalid Bot runbook command is fixed directly and covered by runbook tests.

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01 | Confirm MI-100.B categories and upstream 0123 schema |
| TP-02 | Implement assembler contract/script/wrapper |
| TP-03 | Wire local-ci/live proof gate/docs |
| TP-04 | Run targeted tests, ruff, local chain |
| TP-05 | Commit/push/remote CI observation |
