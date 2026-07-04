# Task-Level Acceptance
- Current HEAD quick local CI evidence is refreshed and recorded.
- Observability/OTel/SLO local gates are passed and tied to artifact paths.
- Production security/externalization/secret provider/retention local gates are passed and tied to artifact paths.
- Six SRE/security external work items are identified with owner, id, status and stale reason.
- Task status remains `Blocked`; no SRE/security live or 100% infrastructure completion is claimed.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Current HEAD local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0146-aea19ff` | Exit 0, focused regression `389 passed` |
| Production security gate | `jq '{status, controls:(.controls|length), owaspCoverageCount}' /tmp/fatecat-local-ci-0146-aea19ff/production-security-gate.json` | `status=passed`, controls `5`, OWASP coverage `10` |
| Security externalization gate | `jq '{status, liveEvidenceStatus}' /tmp/fatecat-local-ci-0146-aea19ff/security-externalization-gate.json` | `status=passed`, live evidence pending |
| External secret provider gate | `jq '{status, liveEvidenceStatus}' /tmp/fatecat-local-ci-0146-aea19ff/external-secret-provider-gate.json` | `status=passed`, live evidence pending |
| OTel collector gate | `jq '{status, collectorMode}' /tmp/fatecat-local-ci-0146-aea19ff/otel-collector-slo-gate.json` | `status=passed`, `collectorMode=dry-run-contract` |
| OTel backend gate | `jq '{status, liveEvidenceStatus}' /tmp/fatecat-local-ci-0146-aea19ff/otel-backend-slo-gate.json` | `status=passed`, live evidence pending |
| Related external work items | `jq '[.workItems[] | select(.category|test("^(observability|security)\\."))]' /tmp/fatecat-local-ci-0146-aea19ff/external-validation-closure-work-queue.json` | 6 pending work items |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0146-measurement-infrastructure-sre-security-external-live-evidence --phase decompose` | Pass |

# Review Gate
- Verify wording does not claim external live completion.
- Verify no token, secret, DSN, raw URL, production logs, trace payload, report body or user input is copied into task docs.
- Verify local gates and external blockers are separated.
- Verify 0146 remains aligned with 0143 and does not supersede 0144/0145 external proof/live blockers.

# Runtime Verification Gate
- No external service is started by this task.
- Runtime evidence is limited to quick local CI artifacts in `/tmp/fatecat-local-ci-0146-aea19ff`.
- Public/live verification remains operator-owned and must be supplied as redacted proof-ref/live proof bundles.

# Ship Readiness
- Local task package can be committed once decompose validation passes.
- SRE/security external live is not shippable until:
  - OTel collector/backend/SLO/alert/error-budget/incident-drill proof refs are accepted,
  - OIDC/IdP proof refs are accepted,
  - SIEM/immutable audit storage proof refs are accepted,
  - external secret provider/Vault/KMS proof refs are accepted,
  - retention cleanup scheduler/smoke/audit proof refs are accepted.
- Measurement infrastructure 100% certification remains blocked.

# Task Package Acceptance
## TP-01 Current HEAD SRE/security evidence refresh
- Acceptance: current HEAD quick local CI passed and SRE/security artifacts exist.
- Evidence: `/tmp/fatecat-local-ci-0146-aea19ff`.

## TP-02 Observability/OTel/SLO live proof
- Acceptance: local observability gates are passed, but external live proof is missing.
- Evidence: SLO gate passed, OTel collector mode `dry-run-contract`, OTel backend live evidence pending.

## TP-03 Identity/SIEM/security externalization proof
- Acceptance: local security gates are passed, but OIDC/SIEM live proof is missing.
- Evidence: production security gate passed, externalization live evidence pending.

## TP-04 Secret provider and retention cleanup proof
- Acceptance: local secret provider and retention staged gates are passed, but external Vault/KMS and production cleanup proof is missing.
- Evidence: external secret provider live evidence pending, retention ship gate blocked.

## TP-05 SRE/security proof bundle and certification refresh
- Acceptance: 6 work items remain pending and certification remains blocked.
- Evidence: work queue includes 6 SRE/security work items, certification `canClaim100Percent=false`.

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
