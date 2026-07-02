# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 webhook outbox lease baseline、local-ci、测试与文档。
- [x] 默认 report job/webhook 行为保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 roadmap、0058/0059、webhook/report job 源码和 smoke。
Verify: `rg` / `sed`。
Gate: lease baseline 边界明确。

## TP-02.01

- [x] Store 增加 claim/release 接口。
- [x] SQLite outbox 增加 lease owner/acquired/expires 字段。
- [x] Atomic claim 防止第二 owner 重复领取。
Verify: focused pytest。
Gate: 不新增外部依赖。

## TP-02.02

- [x] Manager redelivery 先 claim 再 dispatch。
- [x] claim 失败不 dispatch。
- [x] redelivery 完成后 release。
Verify: focused pytest / smoke。
Gate: webhook 不重复投递。

## TP-03.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实公网。

## TP-03.02

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] claim/release、重投一次、payload 内部字段不外露测试。
Verify: focused pytest。
Gate: 新增断言通过。

## TP-03.03

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 稳定通过。

## TP-04.01

- [x] API 文档说明 outbox lease baseline。
- [x] roadmap 标记 0060 首切片并保留剩余缺口。
- [x] scripts/tests/delivery AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把 SQLite lease 写成生产分布式 worker lease。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、secret scan、local-ci、git status。
Gate: 全部通过且无活动 blocker。
