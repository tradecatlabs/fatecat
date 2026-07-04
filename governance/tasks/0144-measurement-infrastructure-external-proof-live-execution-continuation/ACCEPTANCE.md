# Task-Level Acceptance
- Current HEAD local-ci quick evidence exists and passed.
- Current external closure/work-queue/proof-ref/live-proof/certification status is recorded.
- Task status is `Blocked`, not `Done`.
- The next executable external leaf and required operator action are explicit.
- No real secret, token, DSN, raw URL, production payload or private user data is stored.

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Local CI current HEAD | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0144-abab926` | pass, `389 passed` |
| Proof-ref status | `jq '{status, proofRefStatus, acceptedProofRefs:(.acceptedProofRefs|length), pendingWorkItems:(.pendingWorkItems|length)}' /tmp/fatecat-local-ci-0144-abab926/external-validation-proof-ref-gate.json` | accepted 0, pending 22 |
| Live proof status | `jq '{status, liveProofStatus, acceptedLiveProofs:(.acceptedLiveProofs|length), pendingWorkItems:(.pendingWorkItems|length)}' /tmp/fatecat-local-ci-0144-abab926/external-validation-live-proof-gate.json` | accepted 0, pending 22 |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0144-measurement-infrastructure-external-proof-live-execution-continuation --phase decompose` | pass |
| Placeholder scan | `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0144-measurement-infrastructure-external-proof-live-execution-continuation` | no matches |

# Review Gate
Review must verify:
- Local readiness is not described as external proof/live completion.
- TP-03/TP-04/TP-05 remain blocked with concrete unblock requirements.
- No bulk runtime artifacts are copied into the repo.
- `canClaim100Percent=false` remains visible.

# Runtime Verification Gate
Runtime verification is current local-ci quick:
- `status=passed`
- `389 passed`
- evidence root `/tmp/fatecat-local-ci-0144-abab926`

External runtime/live verification remains `外部连通验证待执行`.

# Ship Readiness
This task package can be committed as a current blocked handoff. FateCat cannot ship as 100% measurement infrastructure until proof-ref/live proof/certification/audit are accepted.

# Task Package Acceptance
| TP | Acceptance |
| --- | --- |
| TP-01 | Current HEAD local-ci quick passed and artifact root recorded. |
| TP-02 | Operator readiness counts recorded. |
| TP-03 | Proof-ref blocker recorded with accepted=0 pending=22. |
| TP-04 | Live proof blocker recorded with accepted=0 pending=22. |
| TP-05 | Certification blocker recorded with `canClaim100Percent=false`. |

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
