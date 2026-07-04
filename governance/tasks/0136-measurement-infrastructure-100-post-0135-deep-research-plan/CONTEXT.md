# Repo Evidence

| Evidence | Observation |
| --- | --- |
| `git status --short --branch` before task docs | `## main...origin/main` at commit `4710659`; task creation then made `governance/tasks/INDEX.md` modified and added this task directory. |
| Post-0135 evidence baseline commit | `47106593ac2efaed8668d1b9615aebd7499d3eed` / `4710659 docs: close 0135 task status` |
| Current release proof | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/current-release-proof.json`: `status=passed`, `proofGate.status=passed` |
| Current audit bundle | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/current-audit-bundle/current-audit-bundle.json`: `status=passed`, `auditGate.status=passed`, `git.clean=true`, commit matches `4710659`; still records `pendingExternalValidationCount=430` as external pending inventory. |
| Closure summary | `/tmp/fatecat-current-release-audit-chain-refresh-4710659/external-validation-closure-evidence-summary.json`: `status=passed`, `closureGate.status=blocked`, 22 live/proof-ref categories pending plus manual/policy guardrails. |
| Tracker import package | `status=operator_action_required`, `packageGate.status=blocked`; real tracker issue creation still required. |
| Tracker issue template | `status=operator_action_required`, `templateGate.status=operator_action_required`; sanitized issue refs and artifact hashes not filled. |
| Tracker issue evidence gate | `status=external_connectivity_pending`, `issueEvidenceGate.status=blocked`, `shipGate.status=blocked`. |
| Certification | `measurement-infrastructure-certification.json`: `status=blocked`, `certificationGate.canClaim100Percent=false`, `externalPending=12`, `blockingItems=4`. |
| Third-party audit rehearsal | `third-party-audit-rehearsal.json`: structure `status=passed`, `rehearsalGate.status=blocked`, `evidenceInputs=8`, `externalPending=22`, 7 blocking items. |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| This is a planning task | Only documentation/task package/roadmap changes are allowed. |
| External evidence is missing | Mark as `外部连通验证待执行`; do not synthesize pass status. |
| Release proof sidecar is tied to `4710659` | Do not treat it as proof for later commits; any new release commit needs a fresh release proof before a production release claim. |
| User wants 100% infrastructure plan | Define 100% from infrastructure dimensions, not from divination feature count. |
| Existing roadmap is living source | Append post-0135 section instead of creating a competing roadmap. |
| Sensitive data | Do not copy tokens, URLs with secrets, user report bodies, birth data, production logs or raw account details. |

# Change Boundary

In boundary:

- `governance/tasks/0136-measurement-infrastructure-100-post-0135-deep-research-plan/*`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Out of boundary:

- Business code, API behavior, provider algorithms, tests, CI workflows, production deployment and external live execution.

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Planning overclaims 100% | Audit failure and false production readiness | Every “complete” claim must bind to local file or external run evidence; external domains remain pending. |
| More planning instead of execution | Roadmap fatigue | Plan names exact next tasks and stop condition: after 0136, execute evidence closure tasks. |
| Old roadmap sections conflict | Maintainers may follow stale tasks | New section explicitly supersedes post-0135 next sequence while preserving history. |
| External source drift | Plan may cite stale standards | Use official URLs and mark research date `2026-07-04`. |
| Real secrets leak into plan | Security incident | Only path/status/hash/gate summaries; no raw token, DSN, URL-with-secret or payload. |

# Assumptions and Falsification

- Assumption: FateCat 100% should mean infrastructure maturity, not deterministic prediction accuracy. Falsifier: user defines 100% purely as metaphysical feature coverage; then this plan must split “infra 100%” and “domain ability 100%”.
- Assumption: current release proof and audit bundle sidecars under `/tmp/fatecat-current-release-audit-chain-refresh-4710659` are the newest evidence baseline for `4710659`. Falsifier: a newer pushed commit or newer proof path exists.
- Assumption: after 0135, the next highest-value work is external evidence closure and operationalization. Falsifier: certification reveals another local blocker before any external pending item.
- Assumption: official infrastructure sources are sufficient for the high-level plan. Falsifier: later regulatory, commercial SLA or legal requirements introduce additional domains.

# Critical Ambiguities

- Real production endpoints, credentials and account permissions are not present in this environment.
- Independent third-party audit acceptance criteria are not provided by an actual auditor.
- Commercial SLA, billing, tenant/account model and legal policy are not fully specified.
- “Prediction accuracy” targets for 八字/紫微 require expert-labeled corpus and cannot be inferred from engineering tests alone.

# Debug Evidence Contract

- 调试模式: Optional
- This task is not fixing a runtime bug. If a plan item later proves wrong, create a follow-up task with falsifying evidence and update the roadmap.

# Task Package Context Map

| Asset | Role |
| --- | --- |
| `RESEARCH.md` | External source matrix and FateCat mapping. |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Long-lived roadmap target updated by this task. |
| `/tmp/fatecat-current-release-audit-chain-refresh-4710659/*` | Current evidence baseline for release/audit/certification/rehearsal status. |
| `contracts/fate/*` | Existing resource contracts used to define maturity gaps. |
| `governance/tasks/0131`-`0135` | Immediate upstream tracker evidence and audit rehearsal bridge tasks. |
