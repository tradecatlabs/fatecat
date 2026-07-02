# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 report job retry/timeout policy、测试与文档。
- [x] 默认行为必须保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 0052、roadmap、report job 源码、API 文档和 production-readiness。
Verify: `rg` / `sed` 读取相关文件。
Gate: retry/timeout 切片边界明确。

## TP-02.01

- [x] 新增 execution policy 模型。
- [x] 新增 job attempts/policy 字段。
- [x] SQLite schema 兼容 policy 字段。
- [x] API payload 暴露 policy 字段。
Verify: py_compile + API contract tests。
Gate: 默认 `maxAttempts=1`。

## TP-02.02

- [x] 状态机支持 retry 成功。
- [x] 状态机支持 non-retryable 不重试。
- [x] 状态机支持 timeout 终态。
- [x] events 记录 retry/timeout/non-retryable 证据。
Verify: focused tests。
Gate: 无无限重试，无用户输入泄露。

## TP-03.01

- [x] retry 成功测试。
- [x] non-retryable 不重试测试。
- [x] timeout 失败测试。
- [x] SQLite policy persistence 测试。
Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or sqlite_report_job_store'`。
Gate: 所有新增断言通过。

## TP-03.02

- [x] API 文档说明 retry/timeout policy。
- [x] roadmap 标记 0053 首切片并保留剩余缺口。
- [x] deployment docs 增加 env vars。
- [x] production-readiness 校验 env vars。
- [x] AGENTS/INDEX 同步。
Verify: `git diff -- docs governance scripts domains/experience-delivery/services/fatecat-delivery/AGENTS.md`。
Gate: 不把本地 timeout baseline 写成生产硬中断。

## TP-04.01

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、local-ci、git status。
Gate: 全部通过且无活动 blocker。
