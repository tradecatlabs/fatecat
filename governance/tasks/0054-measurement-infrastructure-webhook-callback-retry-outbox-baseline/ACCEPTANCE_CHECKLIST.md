# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 webhook callback retry/outbox trail、测试与文档。
- [x] 默认行为必须保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 0053、roadmap、report job/webhook 源码、API 文档和 production-readiness。
Verify: `rg` / `sed` 读取相关文件。
Gate: webhook retry/outbox 切片边界明确。

## TP-02.01

- [x] 新增 webhook policy 模型。
- [x] 新增 manager webhook policy 配置。
- [x] main/env 接入 webhook retry vars。
Verify: py_compile + API contract tests。
Gate: 默认 `webhookMaxAttempts=1`。

## TP-02.02

- [x] 状态机支持 webhook retry 成功。
- [x] 状态机支持 webhook final failure。
- [x] events 记录 attempt failure、retry scheduled、succeeded/failed。
- [x] events 不记录 URL、secret、正文、用户输入或原始异常文本。
Verify: focused tests。
Gate: 无无限重试，无敏感信息泄露。

## TP-03.01

- [x] webhook retry 成功测试。
- [x] webhook final failure 测试。
- [x] webhook default once 测试。
- [x] webhook event privacy 测试。
Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'webhook or report_job'`。
Gate: 所有新增断言通过。

## TP-03.02

- [x] API 文档说明 webhook retry/outbox trail。
- [x] roadmap 标记 0054 首切片并保留剩余缺口。
- [x] deployment docs 增加 env vars。
- [x] production-readiness 校验 env vars。
- [x] AGENTS/INDEX 同步。
Verify: `git diff -- docs governance scripts domains/experience-delivery/services/fatecat-delivery/AGENTS.md`。
Gate: 不把本地 retry baseline 写成生产持久 outbox。

## TP-04.01

- [x] validators 通过。
- [x] focused tests 通过。
- [x] webhook smoke 通过。
- [x] ruff/py_compile 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、local-ci、git status。
Gate: 全部通过且无活动 blocker。
