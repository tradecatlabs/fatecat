# Task-Level Acceptance

0141 is complete when:

- Task package files are fully populated with no template placeholders.
- `RESEARCH.md` contains external infrastructure source matrix, FateCat resource maturity matrix, complete implementation tree and execution waves.
- Main roadmap has a post-0140 summary that does not contradict existing blocked external items.
- Validation commands pass.
- No text claims 100% completion, production live completion or third-party audit completion.

# Validation Plan

| Check | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh --phase decompose` | pass |
| Placeholder scan | `rg -n "\\{\\{" governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | no matches |
| No-overclaim scan | `rg -n "100% 测算基础设施已完成|已经达到 100% 测算基础设施|production live passed|第三方审计已完成" governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh docs/reference-materials/roadmap/测算基础设施100%实现计划.md --glob '!ACCEPTANCE.md'` | no matches |
| Git diff review | `git diff --stat && git diff --name-only` | docs/task package only |

# Review Gate

- Future-optimal: plan targets resourceized infrastructure, not a local checklist patch.
- Ponytail: no new runtime code, script, schema or dependency introduced for a planning-only task.
- Document drift: task docs, task index and roadmap agree on status and scope.

# Runtime Verification Gate

Not applicable. This task intentionally does not change runtime behavior.

# Ship Readiness

This planning task can be closed after local validation. It does not establish production readiness.

# Task Package Acceptance

| TP | Acceptance |
| --- | --- |
| TP-01 | Current branch/task/roadmap baseline documented. |
| TP-02 | Official infrastructure references mapped to FateCat. |
| TP-03 | 100% admission model and resource matrix written. |
| TP-04 | Full implementation task tree and execution waves written. |
| TP-05 | Task package and roadmap updated. |
| TP-06 | Validator and scans pass. |

## TP-01 current worktree and task baseline

Verify: `git status --short --branch` and task/roadmap inspection.

Gate: current branch, 0140 state and roadmap baseline are documented without guessing.

## TP-02 external infrastructure research refresh

Verify: `RESEARCH.md` external source matrix.

Gate: each official source maps to at least one FateCat resource or gate.

## TP-03 100% admission model and resource matrix

Verify: `RESEARCH.md` admission and resource maturity sections.

Gate: local baseline, external live and independent audit boundaries are separate.

## TP-04 complete implementation task tree

Verify: `RESEARCH.md` complete implementation tree and execution waves.

Gate: next tasks have evidence requirements and blocker semantics.

## TP-05 roadmap/task package landing

Verify: `git diff --name-only`.

Gate: changes are limited to roadmap and 0141 task package/index docs.

## TP-06 validation and no-overclaim review

Verify: `validate_task_docs.py`, placeholder scan and no-overclaim scan.

Gate: validation passes and no unconditional completion claim is found.

# Anti-Goals

- 不修改运行时代码。
- 不虚构生产、CI、审计或外部平台结果。
- 不把 `external pending`、`blocked`、`dry-run`、`rehearsal` 写成 `passed`。
