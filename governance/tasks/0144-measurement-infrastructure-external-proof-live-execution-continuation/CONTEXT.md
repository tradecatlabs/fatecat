# Repo Evidence
- Current branch: `main`.
- Current commit: `abab9268b7a3e88bade4bf600d7becb08c887867`, message `docs: refresh measurement infrastructure plan`.
- Remote Acceptance for current commit: run `28712295577`, `success`, URL `https://github.com/tradecatlabs/fatecat/actions/runs/28712295577`.
- Local quick CI for current commit:
  - Command: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0144-abab926`
  - Result: passed, `389 passed`.
  - Evidence root: `/tmp/fatecat-local-ci-0144-abab926`.
- Current external validation artifacts:
  - `external-validation-closure-gate.json`: `status=passed`, `shipGate.status=blocked`, `total=442`, `categories=22`, `manualTriage=20`.
  - `external-validation-closure-work-queue.json`: `status=passed`, `workItems=22`, `owners=13`, `staleItems=22`, `totalOccurrences=442`.
  - `external-validation-proof-ref-gate.json`: `status=passed`, `proofRefStatus=external_connectivity_pending`, `acceptedProofRefs=0`, `pendingWorkItems=22`.
  - `external-validation-category-runbooks.json`: `status=passed`, `runbookStatus=operator_runbooks_ready`, `runbooks=22`.
  - `external-validation-operator-execution-packet.json`: `status=operator_action_required`, `operatorSteps=22`, `operatorCommands=104`, `requiredCredentials=99`.
  - `production-live-delivery-evidence-bundle.json`: `status=external_connectivity_pending`, `liveProofs=0`.
  - `external-validation-live-proof-gate.json`: `status=passed`, `liveProofStatus=external_connectivity_pending`, `acceptedLiveProofs=0`, `pendingWorkItems=22`.
  - `external-validation-closure-evidence-summary.json`: `status=passed`, `closureGate=blocked`, `externalPending=22`, `workItems=22`.
  - `measurement-infrastructure-certification.json`: `status=blocked`, `canClaim100Percent=false`, `externalPending=12`.

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| No fake live | 本任务只记录 pending/blocked，不填 accepted proof/live。 |
| Current HEAD evidence | 使用 `/tmp/fatecat-local-ci-0144-abab926`，不再引用旧 commit local-ci 作为当前证据。 |
| External credentials | 所有真实 token、账号、平台权限只作为依赖名称记录，不写入仓库。 |
| Task status | 0144 必须保持 `Blocked`，直到真实 proof-ref/live proof 被 accepted。 |
| Certification | `canClaim100Percent=false` 是当前正确状态。 |

# Change Boundary
Allowed changes:
- `governance/tasks/0144-measurement-infrastructure-external-proof-live-execution-continuation/*`
- `governance/tasks/INDEX.md`

Disallowed changes:
- Production code, scripts, contracts, tests, Web/API/Bot logic.
- Runtime artifact bulk-copy from `/tmp/fatecat-local-ci-0144-abab926`.
- Any real secret, token, DSN, raw URL, production payload or private user data.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Marking blocked work as done | 100% certification becomes false | Keep Overall Status `Blocked` and record accepted counts as 0. |
| Copying large runtime artifacts into repo | Repo bloat and possible privacy risk | Store only paths/counts/status in Markdown. |
| Operator credential leakage | Security incident | Record credential names only; no values. |
| Current HEAD evidence drift | Audit mismatch | Evidence root includes current commit local-ci output path and remote Acceptance URL. |
| Ignoring manual triage/policy guardrail | External closure remains stale | Record manualTriage=20 and policy guardrail category as blockers. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Current local-ci artifacts belong to `abab9268...`. | Local-ci summary or git status shows different commit. |
| 0144 cannot complete locally without external operator evidence. | An accepted proof-ref/live evidence bundle exists and gates report 22 accepted. |
| No production secrets are available in the repo. | Secret scan or artifact inspection finds token/secret/DSN/raw URL. |
| Certification remains blocked. | `measurement-infrastructure-certification.json` reports status `passed` and `canClaim100Percent=true`. |

# Critical Ambiguities
- Which human/operator owns each of the 22 work items in the external environment is not encoded as an executable credential in the repo.
- Whether external tracker issues from 0137 remain current for `abab9268...` needs operator confirmation before live closure.
- The manual triage count increased from 19 in prior local-ci to 20 for current HEAD; this is recorded as a current artifact fact and needs external review before closure.

# Debug Evidence Contract
- 调试模式: Optional
- This is not a bugfix; no `DEBUG.md` is required.
- If a verifier fails, record the command, artifact path, and corrected blocker in this task package.

# Task Package Context Map
| TP | Context |
| --- | --- |
| TP-01 | Current HEAD local-ci and remote Acceptance evidence. |
| TP-02 | Work queue/runbook/operator packet readiness. |
| TP-03 | Proof-ref gate remains blocked until operator bundle exists. |
| TP-04 | Live proof gate remains blocked until proof-ref accepted and live evidence exists. |
| TP-05 | Closure/certification/audit refresh remains blocked until TP-03 and TP-04 are accepted. |
