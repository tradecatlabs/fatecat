# Repo Evidence
- 调试模式: Optional
- Current commit: `a5bc4d23c57915608b1f4392c477f9d40cb81703`.
- 0137 tracker issue evidence gate accepted 22 issue refs.
- Current proof-ref gate artifact: `/tmp/fatecat-local-ci-0137-closeout/external-validation-proof-ref-gate.json`.
- Current proof-ref gate state: `acceptedProofRefs=0`, `pendingWorkItems=22`, `proofRefStatus=external_connectivity_pending`.
- Current live proof gate artifact: `/tmp/fatecat-local-ci-0137-closeout/external-validation-live-proof-gate.json`.
- Current live proof gate state: `acceptedLiveProofs=0`, `pendingWorkItems=22`, `liveProofStatus=external_connectivity_pending`.
- Readiness matrix: `evidence/EXTERNAL_PROOF_LIVE_READINESS_MATRIX.json`.
- Human-readable matrix: `evidence/ISSUE_RUNBOOK_PROOF_REF_MATRIX.md`.

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current worktree only | Used current `main` at `a5bc4d2`. |
| External live evidence cannot be fabricated | No proof/live bundle was invented. |
| Redaction boundary | Stored issue refs, credential names and hashes only. |
| Gate order | proof-ref gate must pass before live proof gate can accept live evidence. |
| Certification/audit | Remain blocked until proof/live accepted and independently reviewed. |

# Change Boundary
- Added 0138 task package and redacted readiness evidence.
- Did not modify business code, runtime scripts, contracts, schemas, provider logic, API/Bot/Web behavior or CI workflows.
- Did not modify external GitHub issues during this task.

# Risk Matrix
| Risk | Status | Evidence / Mitigation |
| --- | --- | --- |
| Proof-ref confused with live proof | Active | TP-03 and TP-04 are separate and ordered. |
| Local matrix mistaken for external validation | Active | Evidence `nonClaims` explicitly states it executes no live checks. |
| Secret leakage through evidence | Controlled | Generated matrix excludes raw URL and sensitive assignment patterns. |
| 100% claim made too early | Controlled | Task status remains Blocked; certification/audit remain blocked. |

# Assumptions and Falsification
| Assumption | Falsifier | Current Result |
| --- | --- | --- |
| All 22 work items have tracker refs from 0137 | Missing trackerIssueRef in readiness matrix | Not falsified; 22 refs present. |
| No proof refs are accepted yet | proof-ref gate shows acceptedProofRefs > 0 | Not falsified; acceptedProofRefs=0. |
| Live proof cannot pass before proof-ref accepted | live proof gate acceptedLiveProofs > 0 while proof refs pending | Not falsified; acceptedLiveProofs=0. |
| Evidence contains no raw URL/secrets | secret scan or grep finds sensitive assignment/raw URL | Pending final validation. |

# Critical Ambiguities
- Which external operator owns each real credential is not represented by a secret value in this repo.
- Some work items need third-party human review or cloud/account access; this cannot be replaced by local dry-run.
- The `manual_triage` work item requires human classification before it can truly close.

# Debug Evidence Contract
- Debug mode is optional because this task is not a bugfix; the blocking state is caused by missing external execution evidence, not a known code failure.
- Required reproduction commands:

```bash
bash scripts/external-validation-proof-ref-gate.sh \
  --work-queue-json /tmp/fatecat-local-ci-0137-closeout/external-validation-closure-work-queue.json \
  --output-json /tmp/fatecat-0138-proof-ref-gate.json

bash scripts/external-validation-live-proof-gate.sh \
  --work-queue-json /tmp/fatecat-local-ci-0137-closeout/external-validation-closure-work-queue.json \
  --proof-ref-gate-json /tmp/fatecat-local-ci-0137-closeout/external-validation-proof-ref-gate.json \
  --category-runbooks-json /tmp/fatecat-local-ci-0137-closeout/external-validation-category-runbooks.json \
  --output-json /tmp/fatecat-0138-live-proof-gate.json
```

# Task Package Context Map
- `evidence/EXTERNAL_PROOF_LIVE_READINESS_MATRIX.json`: machine-readable readiness and blockers.
- `evidence/ISSUE_RUNBOOK_PROOF_REF_MATRIX.md`: human-readable issue/runbook/proof-ref mapping.
- `evidence/EXTERNAL_PROOF_LIVE_BLOCKERS.json`: concise external blockers.

## TP-01 Current External Validation Input Chain

Current HEAD artifacts from local CI are available for work queue, category runbooks, operator packet, proof-ref gate, live proof gate and closure summary.

## TP-02 Issue/Runbook/Proof-Ref Readiness Matrix

All 22 work items are mapped to tracker issue refs and category runbook metadata.

## TP-03 Execute Proof-Ref Runbooks

Blocked until operators execute each runbook using real external credentials and submit a redacted proof-ref bundle.

## TP-04 Execute Live Proof Validation

Blocked until proof-ref gate accepts proof refs; live proof gate currently rejects closure because proof refs are not schema-accepted.

## TP-05 Re-Run Closure/Certification/Audit Chain

Blocked until TP-03 and TP-04 complete; certification still has external pending items.

## TP-06 Ship-Readiness Claim Check

Blocked until certification and third-party audit consume accepted proof/live evidence.
