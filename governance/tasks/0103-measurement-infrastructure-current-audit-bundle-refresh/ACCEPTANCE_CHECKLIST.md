# Acceptance Checklist

# Global Standards
- [x] 不残留模板占位符。
- [x] 任务包包含 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 生命周期门禁。
- [x] `CONTEXT.md` 声明 `调试模式: Optional`。
- [x] Bundle 不连接真实外部系统，不读取真实 `.env`、token、secret 或 DSN。
- [x] `auditGate=blocked` 不能被解释为第三方审计通过。
- [x] focused tests、secret scan 和 closeout validator 通过。
- [x] 版本控制状态与远端状态收口。

# Task Package Checklists
## TP-01.01
Verify: `rg -n "current-audit-bundle|evidenceCoverageTrendGate" scripts tests contracts docs`

Gate: current bundle 现有输入和 0102 artifact 缺口明确。

- [x] current bundle 输入已盘点。
- [x] 0102 evidence artifact 缺口已确认。

## TP-01.02
Verify: `cat contracts/fate/audit/current-bundle.json`

Gate: local-ci gate artifact evidence source 已登记，non-claims 不回退。

- [x] contract 已登记 local-ci gate artifact evidence source。
- [x] non-claims 不变。

## TP-02.01
Verify: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`

Gate: current bundle evidence index 可纳入 evidence coverage trend gate。

- [x] `--local-ci-output-dir` 已实现。
- [x] evidence coverage trend artifact 已映射为 evidence item。

## TP-02.02
Verify: `rg -n "local-ci-output-dir|evidence.evidence_coverage_trend_gate|0103" scripts contracts tests docs governance/tasks`

Gate: local-ci、contract、AGENTS、tests 和任务索引接线一致。

- [x] local-ci 调用已接线。
- [x] AGENTS 和 contract 已同步。
- [x] regression 已更新。

## TP-03.01
Verify: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`

Gate: current bundle regression passed。

- [x] current bundle regression passed。

## TP-03.02
Verify: `bash scripts/current-audit-bundle.sh --output-dir /tmp/fatecat-current-audit-bundle-0103 ...`

Gate: current bundle 生成成功，evidence index 含 `evidence.evidence_coverage_trend_gate`。

- [x] current bundle generation passed。
- [x] evidence index contains `evidence.evidence_coverage_trend_gate`。
- [x] ruff check/format passed。
- [x] secret scan passed。
- [x] diff whitespace check passed。

## TP-04.01
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0103-measurement-infrastructure-current-audit-bundle-refresh --phase closeout`

Gate: task docs closeout validator passed。

- [x] task docs synchronized。
- [x] `governance/tasks/INDEX.md` 中 0103 状态正确。
- [x] closeout validator passed。

## TP-04.02
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 本地 HEAD 与 origin/main 匹配，或如实说明远端状态。

- [x] scoped files staged and committed。
- [x] push to `origin/main` completed。
- [x] 本地 HEAD 与 origin/main 匹配。
- [x] GitHub Actions 对当前 commit 的状态如实记录。
