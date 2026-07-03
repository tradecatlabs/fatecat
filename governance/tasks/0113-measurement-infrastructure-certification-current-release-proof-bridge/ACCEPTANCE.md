# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Optional sidecar input | Certification aggregator accepts `--current-release-proof-json <path>`. |
| Override metadata | Summary contains `evidenceOverrides` when sidecar is provided. |
| Evidence source traceability | Evidence entries include `logicalPath`, `path`, `source`, `status`, `blockingItems` and `pendingItems`. |
| Non-bypass behavior | Sidecar only overrides `current-release-proof.json`; `live-release-gate.json` remains evidence-dir source and may block. |
| Contract sync | Certification contract documents optional sidecar input and required output field. |
| Regression coverage | Tests prove sidecar passed current release proof does not turn release domain passed when live gate is blocked. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py` | pass |
| CLI sidecar smoke | `bash scripts/measurement-infrastructure-certification.sh --evidence-dir /tmp/fatecat-local-ci-runtime-proof-pack-recheck --current-release-proof-json /tmp/fatecat-release-finalizer-0112/current-release-proof.json --output-json /tmp/fatecat-certification-current-release-proof-bridge.json` | status blocked, override recorded |
| Lint/format | `.venv/bin/python -m ruff check ...` and `.venv/bin/python -m ruff format --check ...` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0113-measurement-infrastructure-certification-current-release-proof-bridge --phase decompose` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0113.json` | pass |

# Review Gate
- Sidecar must not override `live-release-gate.json`.
- Summary must not claim `canClaim100Percent=true` unless all domains pass.
- Implementation must not duplicate `current-release-proof` generation logic.
- Implementation must not output raw token, secret, DSN, URL, private key, report body or user input.

# Runtime Verification Gate
Runtime verification is local certification aggregation only. Production live verification remains separate and requires real external API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS/multi-replica evidence.

# Ship Readiness
Ready when targeted pytest, CLI sidecar smoke, lint/format, task docs validator and secret scan pass, then commit/push completes.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | Evidence-dir-only release proof blind spot identified. |
| TP-02 | Sidecar override implemented with source metadata. |
| TP-03 | Tests, contract, roadmap and task index updated. |
| TP-04 | Verification passes and changes are committed/pushed or explicitly pending with evidence. |

# Anti-Goals
- 不连接真实外部系统。
- 不声明 100% 测算基础设施已完成。
- 不把 release artifact proof 当成生产 live proof。
- 不保存真实凭证、生产日志、用户资料或完整报告正文。
