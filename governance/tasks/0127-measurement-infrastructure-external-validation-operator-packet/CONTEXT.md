# Repo Evidence

| Evidence | Observation |
| --- | --- |
| Current branch | `main` |
| Upstream task chain | 0119 work queue, 0120 proof-ref gate, 0121 category runbooks, 0123 live proof gate, 0126 production live operator packet |
| Existing roadmap anchor | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` section 6.21 recommends operator packet / staged evidence template unification when real credentials are unavailable |
| Existing local CI path | `scripts/local-ci.sh --profile quick` already produces closure work queue, proof-ref gate and category runbooks |
| Existing external blocker | Real external credentials, endpoints, operators and third-party audit are not present in repo |

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No fake external success | New packet status remains `operator_action_required`; packet gate remains `blocked` |
| No secrets in repo output | Generator rejects sensitive-looking assignments and raw URLs |
| Must reuse existing chain | Generator consumes existing work queue, proof-ref gate and category runbooks instead of inventing a new source |
| Must be reproducible locally | Script, shell wrapper, regression tests and quick CI artifact are tracked |
| Must not widen to production live | All real live requests remain out of scope and documented as external connectivity pending |

# Change Boundary

Allowed files:

- `contracts/fate/audit/external-validation-operator-execution-packet.json`
- `scripts/external-validation-operator-execution-packet.py`
- `scripts/external-validation-operator-execution-packet.sh`
- `scripts/external-validation-category-runbooks.py`
- `scripts/production-live-operator-execution-packet.py`
- `scripts/local-ci.sh`
- `tests/regression/test_external_validation_operator_execution_packet.py`
- focused related regression tests
- local `AGENTS.md` owners, roadmap and this task package

Forbidden in this task:

- Production live request execution.
- Credential ingestion.
- New external dependency.
- Provider algorithm or report rendering changes.
- Any claim that external validation passed.

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Operator packet leaks endpoint or secret value | Security blocker | Raw URL and sensitive assignment rejection; secret scan |
| Packet source does not bind to upstream evidence | Audit blocker | Source hashes for work queue, proof-ref gate, category runbooks and proof-ref contract |
| Runbook command references nonexistent CLI flags | Operator failure | Regression asserts Postgres live runbooks do not use nonexistent `--require-live` |
| Docs imply 100% completion | Audit blocker | Roadmap and task docs keep external live pending language |
| local-ci artifact exists but not wired into summary | Evidence drift | Regression asserts `externalValidationOperatorExecutionPacket` summary key |

# Assumptions and Falsification

Target end state: every external validation category has a uniform, redacted, replayable operator execution packet that can be consumed by a human operator and then closed through proof-ref/live-proof/certification gates.

Real constraints: real external credentials and endpoints are unavailable in the repo; secrets must not be stored; current category runbooks are the source of executable operator commands.

Inertia constraints: 0126 production-specific operator packet exists and should not be overloaded into all-category execution because its scope is narrower.

Wrong concept / wrong boundary: treating production delivery live packet as equivalent to all external validation execution.

Kill list: no chat-only instructions, no fake proof refs, no raw URL examples, no nonexistent live smoke flags.

Proof point: targeted pytest, ruff, task docs validation, secret scan and quick local CI prove the packet is generated and wired without external credentials.

Falsifier: any output contains raw URL/secret assignment, any runbook category is missing, local-ci summary lacks the packet artifact, or packet gate claims passed external live.

Migration slice: add the all-category operator packet without touching production provider logic or executing live checks.

Rejected short-term patches: copying 0126 packet output by hand, leaving operator instructions only in roadmap prose, or marking proof-ref/live-proof accepted without real external evidence.

# Critical Ambiguities

- Real operators, credentials and endpoints are intentionally unavailable; all live execution remains `外部连通验证待执行`.
- Third-party audit availability is outside repository control.
- Some category commands still require future external infrastructure; this packet only standardizes the execution and evidence shape.

# Debug Evidence Contract

- 调试模式: `Optional`
- This is not a bugfix task, but command/env-var mismatches found during implementation must be covered by regression tests.

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01 | Confirm 0119/0120/0121 inputs and roadmap scope |
| TP-02 | Build contract, generator and shell wrapper |
| TP-03 | Align runbook command flags and production packet env var |
| TP-04 | Wire local-ci, AGENTS and roadmap |
| TP-05 | Run focused validation, docs validation and secret scan |
| TP-06 | Commit, push and observe remote CI through outer delivery flow |
