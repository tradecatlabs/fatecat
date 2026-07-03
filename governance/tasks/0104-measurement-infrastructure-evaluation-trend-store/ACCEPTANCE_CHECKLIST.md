# Acceptance Checklist

# Global Standards
- [x] No placeholder remains in task docs.
- [x] No external live evidence is claimed without real evidence.
- [x] No command output tail, answer key, report body, user input or secret is copied into trend output.
- [x] Focused regression and smoke commands are recorded with true result.
- [x] Task docs validator passes for closeout.

# Task Package Checklists
## TP-01.01
Verify: `rg -n "record-history|latest.json|evaluation-dashboard|evaluation-nightly" scripts contracts tests docs`

Gate: EvaluationRun history/diff/dashboard/nightly 现状已盘点，趋势库缺口明确。

- [x] runner history/latest 已确认。
- [x] diff/dashboard/nightly 现有能力已确认。

## TP-01.02
Verify: `cat contracts/fate/evaluations/trend-policy.json`

Gate: trend policy 和隐私/生产边界明确。

- [x] latest/consecutive/failed run/failed command/missing required run 阈值已定义。
- [x] privacyBoundary 和 productionBoundary 已定义。

## TP-02.01
Verify: `bash scripts/evaluation-trend-gate.sh --help`

Gate: trend gate CLI 可执行并支持 history/policy/output 参数。

- [x] Python CLI 已添加。
- [x] Shell wrapper 已添加。

## TP-02.02
Verify: `bash scripts/evaluation-trend-gate-smoke.sh --output-dir /tmp/fatecat-evaluation-trend-gate-smoke-0104`

Gate: synthetic smoke passed，quick CI 接线存在。

- [x] Synthetic smoke 已添加。
- [x] local-ci trend smoke 已接入。
- [x] local-ci focused regression 列表已接入。

## TP-02.03
Verify: `rg -n "trendPolicy|trendCommand|evaluation-trend-gate" contracts scripts/AGENTS.md`

Gate: registry metadata 和 AGENTS 文档一致。

- [x] `registry.json` metadata 已添加 `trendPolicy` 和 `trendCommand`。
- [x] evaluation contracts AGENTS 已更新。
- [x] scripts AGENTS 已更新。

## TP-03.01
Verify: `.venv/bin/python -m pytest -q tests/regression/test_evaluation_trend_gate.py`

Gate: clean/failure/missing-required/privacy/wiring cases passed。

- [x] Focused regression 已添加。
- [x] 隐私 marker 不进入 trend report。

## TP-03.02
Verify: `rg -n "Post-0103|0104|trend policy" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 100% roadmap 已纳入 trend store，且不声明外部 live 完成。

- [x] Post-0103 深度调研刷新已添加。
- [x] 0104 执行更新已添加。

## TP-04.01
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0104-measurement-infrastructure-evaluation-trend-store --phase closeout`

Gate: validators、tests、smoke、runner history、lint、secret scan 和 diff check 通过或如实记录。

- [x] Task docs validator passed。
- [x] Focused tests passed。
- [x] Synthetic smoke passed。
- [x] Real runner history + trend gate passed。
- [x] Ruff check/format passed。
- [x] Secret scan passed。
- [x] Diff whitespace check passed。

## TP-04.02
Verify: `git status --short --branch`

Gate: scoped diff 清楚；如执行 commit/push，则版本状态如实记录。

- [x] STATUS/TODO/Checklist closeout synchronized。
- [x] Git delivery evidence recorded in final delivery output if commit/push is performed。
