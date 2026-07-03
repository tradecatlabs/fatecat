# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Runtime proof contract | `contracts/fate/delivery/runtime-proof-pack.json` defines required components and negative evidence cases. |
| Runtime proof schema | `contracts/fate/delivery/schemas/runtime-proof.schema.json` defines component ids and invariants. |
| Gate implementation | `scripts/runtime-proof-gate.py/.sh` aggregates existing sub-gates. |
| Pending default | No-live mode returns `runtimeProofStatus=external_connectivity_pending` and blocked shipGate. |
| Live fixture | Regression test proves redacted synthetic live pack can pass. |
| Negative privacy | Raw URL/sensitive summary is rejected. |
| CI/audit integration | local-ci, certification and current audit bundle consume `runtime-proof-gate.json`. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Gate | `bash scripts/runtime-proof-gate.sh --output-json /tmp/fatecat-runtime-proof-gate.json` | status passed, shipGate blocked |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_runtime_proof_gate.py tests/regression/test_multi_replica_runtime_gate.py tests/regression/test_external_secret_provider_gate.py` | pass |
| Shell syntax | `bash -n scripts/runtime-proof-gate.sh scripts/local-ci.sh` | pass |
| Lint/format | `ruff check/format --check` on touched Python files | pass |
| Task docs | `validate_task_docs.py --task-dir governance/tasks/0112-measurement-infrastructure-runtime-proof-pack --phase decompose` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output <dir>` | pass |

# Review Gate
- Implementation must not reimplement sub-gate domain logic.
- Implementation must not treat blocked/allow-missing evidence as live.
- Implementation must not output raw URL, DSN, token, secret, private key, report body or user input.
- Implementation must keep exactly-once as a non-claim.

# Runtime Verification Gate
Default local runtime verification is metadata/evidence-gate only. Production runtime verification requires real Postgres, public webhook receiver, external secret provider and multi-replica evidence passed into the same gate.

# Ship Readiness
Ready when runtime proof gate, targeted pytest, lint/format, task docs validator and quick CI pass, then commit/push completes.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | Existing W2 runtime sub-gates and evidence gaps identified. |
| TP-02 | Runtime proof contract and schema exist and parse. |
| TP-03 | Runtime proof gate and local-ci/certification/audit wiring exist. |
| TP-04 | Regression tests and docs validate. |
| TP-05 | Changes committed/pushed or explicitly pending with evidence. |

# Anti-Goals
- 不连接真实外部系统。
- 不声明 production ready。
- 不声明 exactly-once。
- 不保存真实凭证、生产日志、用户资料或完整报告正文。
