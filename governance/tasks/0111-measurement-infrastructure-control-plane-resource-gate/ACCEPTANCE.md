# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Control-plane registry | `contracts/fate/control-plane/registry.json` defines Capability, Provider, ReleaseGate and EvaluationRun resources. |
| Control-plane schema | `contracts/fate/control-plane/schemas/control-plane.schema.json` defines required spec/status/admission/gate/reconciliation fields. |
| Gate implementation | `scripts/control-plane-gate.py/.sh` recomputes source-state and fails on drift. |
| Existing gate reuse | Provider depth delegates to provider lifecycle gate. |
| CI integration | `scripts/local-ci.sh --profile quick` includes control-plane gate. |
| Regression coverage | `tests/regression/test_control_plane_gate.py` passes. |
| Documentation sync | `contracts/fate/AGENTS.md` and task package reflect new control-plane directory. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Gate | `bash scripts/control-plane-gate.sh --output-json /tmp/fatecat-control-plane-gate.json` | status passed |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_control_plane_gate.py tests/regression/test_capability_protocol.py tests/regression/test_provider_lifecycle_gate.py` | pass |
| Shell syntax | `bash -n scripts/control-plane-gate.sh scripts/local-ci.sh` | pass |
| Task docs | `validate_task_docs.py --task-dir governance/tasks/0111-measurement-infrastructure-control-plane-resource-gate --phase decompose` | pass |
| Format/lint | `ruff check/format` on touched Python test/script | pass |

# Review Gate
- The implementation must not duplicate full source registries.
- The implementation must not store runtime proof, token, secret, DSN, report body or user input.
- ReleaseGate `pending_external` must remain explicit and must not be reported as production live pass.
- Planned capabilities must remain non-production and non-default.

# Runtime Verification Gate
The runtime part is metadata-only gate execution. Production runtime controller, external backend and live proof are W2+ tasks.

# Ship Readiness
Ready when gate, targeted pytest, lint/format and task docs validator pass, then commit/push completes with clean worktree.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | Existing source registries and gates identified. |
| TP-02 | Control-plane contract files exist and parse. |
| TP-03 | Gate passes and local-ci calls it. |
| TP-04 | Regression tests and docs validate. |
| TP-05 | Changes committed/pushed or explicitly pending with clean evidence. |

# Anti-Goals
- 不实现真实 controller runtime。
- 不触发生产部署或 live smoke。
- 不保存真实凭证、生产日志、用户资料或完整报告正文。
