# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| 0108 index uniqueness | `INDEX.md` contains exactly one row for task 0108. |
| Task package hygiene | `validate_task_docs.py --phase decompose` passes. |
| Final git state | `origin/main` contains final HEAD and worktree is clean. |
| Acceptance workflow | Final HEAD run reaches terminal success. |
| Container release workflow | Final HEAD run reaches terminal success with release artifact upload and attestation verification steps successful. |
| Rollback boundary | rollback drill status is passed and production rollback is false. |
| Release proof aggregate | current-release-proof status is passed with zero pending and zero failed items. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| 0108 uniqueness | `rg "^\\| 0108 \\|" governance/tasks/INDEX.md` | one row |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0110-measurement-infrastructure-current-release-truth-finalizer --phase decompose` | pass |
| Placeholder scan | scan 0110 task docs for unreplaced template tokens | no output |
| Git check | `git status --short --branch` | clean and origin current |
| Acceptance | `gh run view <acceptance-run-id>` | completed success and headSha equals final HEAD |
| Container | `gh run view <container-run-id>` | completed success and headSha equals final HEAD |
| Proof | `bash scripts/current-release-proof.sh --require-current-release ...` | status passed |

# Review Gate
- The task must not write exact post-commit proof back into Git.
- The task must not claim production live completion.
- The task must distinguish local acceptance from remote Acceptance workflow.
- The task must preserve rollback as dry-run only.

# Runtime Verification Gate
Runtime verification is remote CI/release proof only. If either workflow fails, the task must stop and switch to debug with run logs instead of forcing a pass.

# Ship Readiness
Ready when the task docs validate, `INDEX.md` has no duplicate 0108 row, final HEAD is pushed, both remote workflows succeed, and current-release-proof passes.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01 | 0108 row count equals one and 0110 task docs validate. |
| TP-02 | Commit/push completed and final HEAD is clean/origin current. |
| TP-03 | Acceptance and Container workflows exist for final HEAD and terminal success. |
| TP-04 | rollback dry-run and current-release-proof passed. |

# Anti-Goals
- 不修改业务代码、运行脚本、workflow 触发行为或生产配置。
- 不虚构远端 CI、release artifact、Bot live 或外部平台证据。
- 不把 dry-run rollback 说成真实生产 rollback。
