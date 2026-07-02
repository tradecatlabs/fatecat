# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 webhook outbox baseline、local-ci、测试与文档。
- [x] 默认 report job 和 webhook 行为保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 roadmap、0054/0055、report job/webhook 源码、测试和 local-ci。
Verify: `rg` / `sed` 读取相关文件。
Gate: persistent webhook outbox baseline 边界明确。

## TP-02.01

- [x] 增加 outbox record 模型。
- [x] 增加 store 接口。
- [x] 增加 SQLite 表。
Verify: focused pytest。
Gate: memory backend 兼容。

## TP-02.02

- [x] dispatch 前写 pending。
- [x] dispatch 成功写 succeeded。
- [x] dispatch 最终失败写 failed。
Verify: focused pytest。
Gate: 不改变 job terminal 状态。

## TP-02.03

- [x] API payload 暴露 `webhookOutbox`。
- [x] API 不泄露 URL/secret/用户输入。
Verify: API contract test。
Gate: 输出为脱敏摘要。

## TP-03.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实公网。

## TP-03.02

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] outbox success/failure/rebuild 测试。
Verify: focused pytest。
Gate: 新增断言通过。

## TP-03.03

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 稳定通过。

## TP-04.01

- [x] API 文档说明 persistent outbox baseline。
- [x] roadmap 标记 0056 首切片并保留剩余缺口。
- [x] scripts/tests AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把 outbox baseline 写成 production redelivery。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、local-ci、git status。
Gate: 全部通过且无活动 blocker。
