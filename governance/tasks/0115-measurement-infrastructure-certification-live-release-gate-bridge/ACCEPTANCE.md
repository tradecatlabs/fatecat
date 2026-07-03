# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Optional live gate sidecar input | Certification aggregator accepts `--live-release-gate-json <path>`. |
| Override metadata | Summary contains `evidenceOverrides.live-release-gate.json` when sidecar is provided. |
| Evidence source traceability | Release evidence entry records `logicalPath`, `path`, `source=override`, `status`, `blockingItems` and `pendingItems`. |
| Non-bypass behavior | Live gate sidecar does not override `current-release-proof.json` or `current-audit-bundle/current-audit-bundle.json`. |
| Contract sync | Certification contract documents optional live gate sidecar input. |
| Regression coverage | Tests prove live sidecar can change only live gate evidence source, while release proof and audit bundle remain independently blocked or passed. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py tests/regression/test_live_release_gate.py` | pass |
| Live gate sidecar smoke | `bash scripts/live-release-gate.sh --local-ci-summary <local-ci-summary> --github-run-url <run> --github-commit <head> --container-evidence-path <container-evidence> --sbom-path <sbom> --provenance-path <provenance> --rollback-evidence-path <rollback> --output-json <path>` | generated gate, external live missing remains blocked |
| CLI sidecar smoke | `bash scripts/measurement-infrastructure-certification.sh --evidence-dir <local-ci-output> --live-release-gate-json <live-gate> --current-release-proof-json <proof> --current-audit-bundle-json <bundle> --output-json <path>` | status blocked, three overrides recorded |
| Lint/format | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0115-measurement-infrastructure-certification-live-release-gate-bridge --phase decompose` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0115.json` | pass |

# Review Gate
- Live gate sidecar must not override release proof or audit bundle.
- Summary must not claim `canClaim100Percent=true` unless all domains pass.
- Implementation must not duplicate live gate generation logic.
- Implementation must not output raw token, secret, DSN, private key, report body or user input.

# Runtime Verification Gate
Runtime verification is local certification aggregation only. Production API/HF/Bot live verification and third-party audit remain separate and require external evidence.

# Ship Readiness
Ready when targeted pytest, live gate sidecar smoke, CLI sidecar smoke, lint/format, task docs validator and secret scan pass, then commit/push completes.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | Stale local-ci live gate blind spot identified. |
| TP-02 | Live gate sidecar override implemented with source metadata. |
| TP-03 | Tests, contract, AGENTS, roadmap and task index updated. |
| TP-04 | Verification passes and changes are committed/pushed or explicitly pending with evidence. |

# Anti-Goals
- 不连接真实外部系统。
- 不声明 100% 测算基础设施已完成。
- 不把 live gate generated 当成 production API/HF/Bot live passed。
- 不把 live sidecar 当成 release proof 或 audit bundle。
- 不保存真实凭证、生产日志、用户资料或完整报告正文。
