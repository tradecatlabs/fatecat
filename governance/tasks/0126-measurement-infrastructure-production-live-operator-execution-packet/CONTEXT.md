# Repo Evidence

- Roadmap root: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` lists `MI-100.B.00 operator live execution packet and evidence template`.
- Upstream work queue: `scripts/external-validation-closure-work-queue.py`.
- Upstream proof-ref gate: `scripts/external-validation-proof-ref-gate.py`.
- Upstream runbooks: `scripts/external-validation-category-runbooks.py`.
- Downstream live bundle: `scripts/production-live-delivery-evidence-bundle.py`.
- Downstream live proof gate: `scripts/external-validation-live-proof-gate.py`.
- Current task output:
  - `contracts/fate/audit/production-live-operator-execution-packet.json`
  - `scripts/production-live-operator-execution-packet.py`
  - `scripts/production-live-operator-execution-packet.sh`
  - `tests/regression/test_production_live_operator_execution_packet.py`

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No real credentials in repo | Output excludes URL/token/secret/DSN/webhook secret/chat id/report body |
| No over-claim | `packetGate.status=blocked` and `status=operator_action_required` |
| Existing proof-ref/live proof chain | Reuse work queue、proof-ref gate、category runbooks、0123/0124 contracts |
| Operator usability | Output lists ordered steps, env var names, artifact paths, proof-ref template and final gate commands |
| Local CI cost | Add one small Python generator and one focused regression file |

# Change Boundary

- Allowed: audit contract, scripts, regression tests, local-ci wiring, AGENTS, roadmap, task docs.
- Not allowed: production provider algorithms, report rendering, API behavior, real deployment config, real secrets.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Packet accidentally includes raw URL | `_assert_output_safe` rejects `http://` / `https://` in output |
| Packet includes token/secret assignment | generator rejects sensitive-looking assignments in inputs and output |
| Operator step drifts from runbooks | generator consumes runbook id/category and tests lock wiring |
| Packet mistaken for live pass | contract non-claims and packet gate stay blocked |
| Final gate command not executable | command templates use existing repository scripts and verified CLI parameter names |

# Assumptions and Falsification

- Assumption: operator can run live commands from a local checkout with environment variables injected out-of-band. Falsifier: operator execution must run in a managed CI environment; then add a CI workflow packet rather than embedding credentials.
- Assumption: evidence handoff is proof-ref bundle plus delivery evidence bundle. Falsifier: external auditor requires a remote evidence store API; then add a proof-ref resolver and storage adapter while keeping this packet as the local runbook source.

# Critical Ambiguities

None for this local slice. Real production endpoint ownership, token custody and auditor access remain external execution inputs, not code design ambiguities.

# Debug Evidence Contract

- 调试模式: `Optional`

Not required. This is a new contract/generator slice with regression coverage, not a reproduced defect.

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01 | Confirm MI-100.B categories and upstream/downstream evidence chain |
| TP-02 | Implement operator packet contract/script/wrapper |
| TP-03 | Wire local-ci, AGENTS and roadmap |
| TP-04 | Run targeted tests, ruff, secret scan and quick CI |
| TP-05 | Commit/push/remote CI observation |
