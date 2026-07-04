# Repo Evidence
- Current branch: `main`.
- Current HEAD: `aea19ff4b060d30306cf65e008c3ba170f4f1df7`.
- Fresh evidence root: `/tmp/fatecat-local-ci-0146-aea19ff`.
- Command executed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0146-aea19ff`.
- Result: quick local CI passed, focused regression `389 passed in 141.06s`.
- Production security gate: `/tmp/fatecat-local-ci-0146-aea19ff/production-security-gate.json`, status `passed`, controls `5`, OWASP coverage count `10`.
- Security externalization gate: `/tmp/fatecat-local-ci-0146-aea19ff/security-externalization-gate.json`, status `passed`, controls `3`, negative evidence rejected `5`, live evidence status `外部连通验证待执行`.
- External secret provider gate: `/tmp/fatecat-local-ci-0146-aea19ff/external-secret-provider-gate.json`, status `passed`, controls `1`, negative evidence rejected `3`, live evidence status `外部连通验证待执行`.
- Retention production cleanup staged gate: `/tmp/fatecat-local-ci-0146-aea19ff/retention-production-cleanup-gate.json`, status `passed`, negative evidence rejected `3`, live evidence status `外部连通验证待执行`, ship gate `blocked`.
- Observability SLO gate: `/tmp/fatecat-local-ci-0146-aea19ff/observability-slo-gate.json`, status `passed`, objectives `4`, alert rules `5`.
- Observability trace SLO smoke: `/tmp/fatecat-local-ci-0146-aea19ff/observability-trace-slo-smoke.json`, status `passed`, SLO objectives `4`, alert rules `5`.
- OTel collector SLO gate: `/tmp/fatecat-local-ci-0146-aea19ff/otel-collector-slo-gate.json`, status `passed`, collector mode `dry-run-contract`, pipelines `3`, dry-run evidence checks `3`.
- OTel backend SLO staged gate: `/tmp/fatecat-local-ci-0146-aea19ff/otel-backend-slo-gate.json`, status `passed`, negative evidence rejected `4`, live evidence status `外部连通验证待执行`.
- External validation work queue: `/tmp/fatecat-local-ci-0146-aea19ff/external-validation-closure-work-queue.json`, work items `22`, total occurrences `443`, stale items `22`, ship gate `blocked`.
- Related work items pending:
  - `observability.otel_slo_live`: `external-work.5eddad3687b18ac8`, owner `sre-ops`, stale reason `proof_ref_missing`.
  - `security.external_secret_provider`: `external-work.48ca6cab90f9800c`, owner `security-ops`, stale reason `proof_ref_missing`.
  - `security.externalization_live`: `external-work.097db160a9dad0c1`, owner `security-ops`, stale reason `proof_ref_missing`.
  - `security.identity_oidc`: `external-work.adb578beb167a8b2`, owner `security-ops`, stale reason `proof_ref_missing`.
  - `security.retention_cleanup_live`: `external-work.4526896091f25f6d`, owner `security-ops`, stale reason `proof_ref_missing`.
  - `security.siem_audit`: `external-work.e90698a411fc18fe`, owner `security-ops`, stale reason `proof_ref_missing`.
- Certification: `/tmp/fatecat-local-ci-0146-aea19ff/measurement-infrastructure-certification.json`, status `blocked`, `canClaim100Percent=false`, external pending domains `12`.

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No fabricated live evidence | SRE/security proof remains blocked until external operator evidence exists. |
| No sensitive material | Store only paths, counts, status flags, work item IDs and redacted proof requirements. |
| Current worktree only | Evidence is bound to current HEAD `aea19ff...`. |
| SRE/security scope | Limit to OTel/SLO/alert, identity, SIEM, secret provider and retention cleanup. |
| Task package scope | Write only this task directory and `governance/tasks/INDEX.md`; no business code changes. |
| Release honesty | Dry-run/staged/local gates are readiness evidence, not production live evidence. |

# Change Boundary
- Changed: `governance/tasks/0146-measurement-infrastructure-sre-security-external-live-evidence/*`.
- Changed by scaffold: `governance/tasks/INDEX.md`.
- Not changed: application code, contracts, scripts, tests, CI workflows, runtime artifacts.
- `/tmp/fatecat-local-ci-0146-aea19ff` is evidence output only and must not be copied into the repository.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Dry-run overclaim | Audit rejects production readiness if local contracts are called live evidence. | Task status remains `Blocked`; live evidence status is recorded as pending. |
| Secret leakage | External proof may expose token, DSN, trace payload or production logs. | Require redacted proof refs only; no raw external payloads in repo. |
| Retention cleanup ambiguity | Production cleanup proof could be confused with destructive deletion. | Require smoke summary and audit proof ref; forbid production deletion markers in docs. |
| OIDC ambiguity | Scoped local tokens could be misreported as production IdP. | Record OIDC/IdP as external pending; local token baseline is not IdP proof. |
| OTel ambiguity | Local collector dry-run could be misreported as backend live. | Record collector mode `dry-run-contract` and backend live pending. |
| Certification drift | 100% claim could ignore SRE/security blockers. | Bind 6 work items to 0146 and keep certification blocked. |

# Assumptions and Falsification
- Assumption: Current local SRE/security gates are sufficient to prove readiness for operator live execution.
- Falsifier: Any SRE/security gate fails on current HEAD, or artifact root is missing.
- Assumption: OTel backend, alert route, error budget, IdP, SIEM, Vault/KMS and retention cleanup need external credentials/platform access.
- Falsifier: A redacted operator proof bundle accepted by existing gates shows these are live.
- Assumption: 0146 should not modify business code because it is a live handoff/planning task.
- Falsifier: Operator evidence reveals a contract or gate cannot express required live proof without code changes; that must become a separate implementation task.

# Critical Ambiguities
- Which OTel backend or observability vendor will be authoritative is not established in repo evidence.
- Which OIDC/IdP provider will be authoritative is not established in repo evidence.
- Which SIEM/immutable audit storage will be authoritative is not established in repo evidence.
- Which external secret provider or KMS will be authoritative is not established in repo evidence.
- Production retention cleanup scheduler and audit proof are not live-proven.
- These ambiguities do not block documenting 0146 because they are the precise external live blockers.

# Debug Evidence Contract
- 调试模式: Optional
- This task is not a bugfix. No `DEBUG.md` is required.
- If a SRE/security gate fails in a future run, convert the relevant TP leaf into a debug task with reproduction command, root cause and regression evidence.

# Task Package Context Map
| TP | Context |
| --- | --- |
| TP-01 | Current HEAD quick local CI and SRE/security local artifacts. |
| TP-02 | Observability, OTel collector/backend, SLO, alert route, error budget and incident drill proof requirements. |
| TP-03 | OIDC/IdP, SIEM/immutable audit and security externalization proof requirements. |
| TP-04 | External secret provider/Vault/KMS and retention cleanup proof requirements. |
| TP-05 | Related work items, proof-ref/live-proof gate and certification linkage. |
