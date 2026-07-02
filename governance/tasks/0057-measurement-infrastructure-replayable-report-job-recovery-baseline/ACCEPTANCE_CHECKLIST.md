# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 replayable report job recovery baseline、local-ci、测试与文档。
- [x] 默认 report job 行为保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 roadmap、0055/0056、report job 源码、API submit 路径和测试。
Verify: `rg` / `sed` 读取相关文件。
Gate: replayable recovery baseline 边界明确。

## TP-02.01

- [x] 增加 task_payload 字段。
- [x] 增加 SQLite schema/读写。
- [x] memory backend 保持兼容。
Verify: focused pytest。
Gate: 不保存 callable、secret 或 Markdown 正文。

## TP-02.02

- [x] 增加 task_factories。
- [x] active job 有 payload/factory 时重建重新入队。
- [x] active job 无 payload/factory 时继续安全失败。
Verify: focused pytest。
Gate: 兼容 0055 restart-safe failure。

## TP-02.03

- [x] Web report job 接入 payload。
- [x] Markdown report job 接入 payload。
- [x] payload 不包含 webhook secret。
Verify: API contract test。
Gate: 生产报告任务可恢复执行。

## TP-03.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实公网。

## TP-03.02

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] replayable success / non-replayable failure 测试。
Verify: focused pytest。
Gate: 新增断言通过。

## TP-03.03

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 稳定通过。

## TP-04.01

- [x] API 文档说明 replayable recovery baseline。
- [x] roadmap 标记 0057 首切片并保留剩余缺口。
- [x] scripts/tests AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把 replayable baseline 写成 external backend。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、secret scan、local-ci、git status。
Gate: 全部通过且无活动 blocker。
