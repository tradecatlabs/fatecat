# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 restart recovery smoke、local-ci、测试与文档。
- [x] 默认 report job 行为不变。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 0054、roadmap、report job 源码、SQLite rebuild tests 和 local-ci。
Verify: `rg` / `sed` 读取相关文件。
Gate: restart recovery smoke 切片边界明确。

## TP-02.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实环境。

## TP-02.02

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 运行稳定。

## TP-03.01

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] 隐私边界测试。
Verify: `.venv/bin/python -m pytest -q tests/regression/test_report_job_restart_recovery_smoke.py`。
Gate: 新增断言通过。

## TP-03.02

- [x] API 文档说明 restart recovery smoke。
- [x] roadmap 标记 0055 首切片并保留剩余缺口。
- [x] scripts AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把 smoke 写成 production resume。

## TP-04.01

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、local-ci、git status。
Gate: 全部通过且无活动 blocker。
