# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 webhook outbox redelivery baseline、local-ci、测试与文档。
- [x] 默认 report job 行为保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 roadmap、0054/0056/0057、report job webhook 源码和测试。
Verify: `rg` / `sed` 读取相关文件。
Gate: redelivery baseline 边界明确。

## TP-02.01

- [x] 增加 pending/failed outbox 查询。
- [x] 增加 redelivery API 或 manager 内部入口。
Verify: focused pytest。
Gate: 不改变已有 outbox persisted record 语义。

## TP-02.02

- [x] 增加 delivery resolver。
- [x] manager 重建后可调度 redelivery。
- [x] resolver missing 时不误投。
- [x] resolver error 时不误投且追加脱敏失败事件。
Verify: focused pytest。
Gate: 不持久保存 secret/完整 URL。

## TP-02.03

- [x] 增加 redelivery 事件。
- [x] event metadata 脱敏。
Verify: API contract test。
Gate: summary/API 不泄露 webhook 配置。

## TP-03.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实公网。

## TP-03.02

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] resolver success / resolver missing / resolver error 测试。
Verify: focused pytest。
Gate: 新增断言通过。

## TP-03.03

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 稳定通过。

## TP-04.01

- [x] API 文档说明 redelivery baseline。
- [x] roadmap 标记 0058 首切片并保留剩余缺口。
- [x] scripts/tests AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把 redelivery baseline 写成 external backend。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、secret scan、local-ci、git status。
Gate: 全部通过且无活动 blocker。
