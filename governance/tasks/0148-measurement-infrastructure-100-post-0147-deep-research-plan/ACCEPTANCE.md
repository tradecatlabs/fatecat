# Task-Level Acceptance
This task is accepted when:

- The post-0147 100% measurement infrastructure target state is defined in infrastructure language, not feature-list language.
- External research sources are cited with official URLs.
- Current repo evidence distinguishes completed local/remote proof from external pending proof.
- Remaining work is split into concrete task nodes with owner type, prerequisite, evidence and blocking condition.
- The roadmap is updated without claiming production live, expert review, third-party audit or final certification completion.
- The task package has no placeholders and passes `validate_task_docs.py --phase decompose`.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0148-measurement-infrastructure-100-post-0147-deep-research-plan --phase decompose` | `ok: true` |
| Placeholder scan | `rg "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0148-measurement-infrastructure-100-post-0147-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | no output |
| Git diff hygiene | `git diff --check` | no whitespace errors |
| Remote CI for previous 0147 commit | `gh run view 28715288541 --json status,conclusion,url,headSha` | success for commit `a7b6a6f...` |
| Quick local CI for 0148 docs | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0148-a7b6a6f` | passed; focused regression `389 passed` |

# Review Gate
- PASS if the plan is traceable to current repo facts and external sources.
- PASS if every future claim has an evidence gate.
- WARN if a future node depends on unavailable external credentials or human review.
- BLOCK if the plan states or implies `canClaim100Percent=true` before certification passes.

# Runtime Verification Gate
Runtime live verification is intentionally out of scope. The correct runtime state for this task is:

```text
planningDocsStatus = passed
externalLiveStatus = 外部连通验证待执行
certification.canClaim100Percent = false
```

# Ship Readiness
This planning task is shippable when task docs validate, quick local CI passes, roadmap is updated, changes are committed, pushed, and a current remote Acceptance run is triggered. It does not make FateCat production-certified.

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | External research table exists and uses official source URLs. |
| TP-01.02 | Current evidence table separates 0145/0146/0147 local/remote facts and pending proof. |
| TP-02.01 | Target end state includes capability, provider, runtime/event, evidence, eval, SRE/security, release and audit. |
| TP-02.02 | Gap matrix maps each domain to current state, 100% target and next evidence. |
| TP-03.01 | Implementation task tree names concrete next nodes and dependencies. |
| TP-03.02 | Completion gates and failure predicates are explicit. |
| TP-04.01 | Roadmap has a post-0147 refresh section. |
| TP-04.02 | Task docs validator passes. |

# Anti-Goals
- 不得修改业务代码、运行时代码或契约行为。
- 不得虚构 CI、live proof、专家评审、第三方审计或 certification 结果。
- 不得把 dry-run、contract、template、operator packet 写成生产完成。
