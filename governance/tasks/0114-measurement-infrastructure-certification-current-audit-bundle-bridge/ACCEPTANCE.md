# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Optional audit sidecar input | Certification aggregator accepts `--current-audit-bundle-json <path>`. |
| Override metadata | Summary contains `evidenceOverrides.current-audit-bundle/current-audit-bundle.json` when sidecar is provided. |
| Evidence source traceability | Audit evidence entry records `logicalPath`, `path`, `source=override`, `status`, `blockingItems` and `pendingItems`. |
| Non-bypass behavior | Audit sidecar does not override `current-release-proof.json` or `live-release-gate.json`. |
| Contract sync | Certification contract documents optional audit bundle sidecar input. |
| Regression coverage | Tests prove audit sidecar can change only audit domain evidence source, while release domain remains independently blocked. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Final audit bundle smoke | `bash scripts/current-audit-bundle.sh --output-dir /tmp/fatecat-current-audit-bundle-bridge-0114 ...` | generated bundle, no sensitive output |
| CLI sidecar smoke | `bash scripts/measurement-infrastructure-certification.sh --evidence-dir <local-ci-output> --current-release-proof-json <proof> --current-audit-bundle-json <bundle> --output-json <path>` | status blocked, two overrides recorded |
| Lint/format | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0114-measurement-infrastructure-certification-current-audit-bundle-bridge --phase decompose` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0114.json` | pass |

# Review Gate
- Audit bundle sidecar must not override release proof or live release gate.
- Summary must not claim `canClaim100Percent=true` unless all domains pass.
- Implementation must not duplicate current audit bundle generation logic.
- Implementation must not output raw token, secret, DSN, URL, private key, report body or user input.

# Runtime Verification Gate
Runtime verification is local certification aggregation only. Production live verification and third-party audit remain separate and require external evidence.

# Ship Readiness
Ready when targeted pytest, final audit bundle smoke, CLI sidecar smoke, lint/format, task docs validator and secret scan pass, then commit/push completes.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | Stale local-ci audit bundle blind spot identified. |
| TP-02 | Audit bundle sidecar override implemented with source metadata. |
| TP-03 | Tests, contract, AGENTS, roadmap and task index updated. |
| TP-04 | Verification passes and changes are committed/pushed or explicitly pending with evidence. |

# Anti-Goals
- 不连接真实外部系统。
- 不声明 100% 测算基础设施已完成。
- 不把 current audit bundle 当成第三方审计通过。
- 不把 audit sidecar 当成 production live proof。
- 不保存真实凭证、生产日志、用户资料或完整报告正文。
