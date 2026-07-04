# Task-Level Acceptance
Accepted when all of the following are true:

- 22 external validation GitHub issues exist for the current HEAD import package.
- A redacted issue evidence bundle exists in `evidence/TRACKER_ISSUE_EVIDENCE_BUNDLE.json`.
- `scripts/external-validation-tracker-issue-evidence-gate.sh` accepts the bundle.
- The task package clearly states that live proof, proof-ref, certification and third-party audit are not complete.

# Validation Plan
| Validation | Command / Evidence | Result |
| --- | --- | --- |
| Local quick CI package generation | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0137-current-head` | Passed before issue creation; 380 tests passed. |
| Tracker issue evidence gate | `bash scripts/external-validation-tracker-issue-evidence-gate.sh ...` | Accepted, 22 accepted issues. |
| Evidence bundle | `evidence/TRACKER_ISSUE_EVIDENCE_BUNDLE.json` | 22 issue records. |
| Human-readable refs | `evidence/TRACKER_ISSUE_REFS.md` | 22 redacted refs. |
| Closeout local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0137-closeout` | Passed; 380 tests passed. |

# Review Gate
- Review should verify evidence contains only redacted refs/hashes and no raw GitHub URL, token, secret, production log or user data.
- Review should verify `shipGate.status=blocked` remains documented.

# Runtime Verification Gate
- Runtime live checks were not executed in this task.
- Required future gates remain:
  - `external-validation-proof-ref-gate`
  - `external-validation-live-proof-gate`
  - measurement infrastructure certification
  - independent third-party audit

# Ship Readiness
- `issueEvidenceGate`: passed.
- `shipGate`: blocked by design.
- This task is complete, but FateCat is not yet 100% measurement infrastructure.

# Task Package Acceptance
| TP | Acceptance |
| --- | --- |
| TP-01 | Current HEAD and package SHA recorded. |
| TP-02 | Tracker state verified before creation. |
| TP-03 | 22 issue refs recorded. |
| TP-04 | Evidence bundle stored. |
| TP-05 | Gate JSON stored and accepted. |
| TP-06 | Task docs contain no template placeholders. |

## TP-01 Current HEAD Package

Acceptance: current HEAD package is identified and bound to the evidence bundle source.

## TP-02 Tracker Preflight

Acceptance: tracker access and duplicate issue state were checked before issue creation.

## TP-03 Issue Creation

Acceptance: 22 tracker refs are recorded in redacted form.

## TP-04 Evidence Bundle

Acceptance: bundle records 22 issue artifacts and stores no raw URLs or secret-bearing values.

## TP-05 Evidence Gate

Acceptance: gate accepted 22 issue records with 0 pending and 0 rejected.

## TP-06 Closeout

Acceptance: task documents and roadmap state the remaining live/cert/audit blockers.

# Anti-Goals
- 不得修改业务代码或运行时实现
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把 tracker issue creation 写成生产 live 完成
