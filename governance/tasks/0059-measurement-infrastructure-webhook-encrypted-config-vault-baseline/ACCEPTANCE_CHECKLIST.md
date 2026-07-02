# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 encrypted webhook config vault baseline、local-ci、测试与文档。
- [x] 默认 report job 行为保持兼容。
- [x] 不读取、不提交、不输出真实 secret。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 已读取 roadmap、0056/0058、webhook/report job 源码、依赖和测试。
Verify: `rg` / `sed` 读取相关文件。
Gate: encrypted config vault 边界明确。

## TP-02.01

- [x] `cryptography` 加入 pyproject、requirements 和 lock。
- [x] Fernet codec 可生成/解析 key ring。
Verify: focused pytest。
Gate: 不自研密码学。

## TP-02.02

- [x] SQLite 增加 encrypted config 表。
- [x] save/load/delete encrypted config。
- [x] key rotation 可把旧 key 迁移到 active key。
Verify: focused pytest。
Gate: 原始 SQLite 不含明文 URL/secret。

## TP-02.03

- [x] Manager 在 outbox 创建时保存 encrypted config。
- [x] Manager redelivery 无 resolver 时可使用 encrypted config。
- [x] redelivery 成功后删除 encrypted config。
Verify: API contract test。
Gate: 无 vault 时兼容 0058 行为。

## TP-03.01

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] smoke 输出机器可读 JSON。
Verify: smoke CLI。
Gate: 不依赖真实公网。

## TP-03.02

- [x] smoke summary 测试。
- [x] smoke CLI 测试。
- [x] encrypted redelivery / delete / rotation / privacy 测试。
Verify: focused pytest。
Gate: 新增断言通过。

## TP-03.03

- [x] local-ci quick 接入 smoke。
Verify: quick local CI。
Gate: smoke 稳定通过。

## TP-04.01

- [x] API 文档说明 encrypted config vault baseline。
- [x] roadmap 标记 0059 首切片并保留剩余缺口。
- [x] scripts/tests AGENTS 同步。
- [x] INDEX 同步。
Verify: docs diff + validators。
Gate: 不把本地 vault 写成外部 Vault/KMS。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
- [x] commit/push 完成。
Verify: validators、pytest、ruff、secret scan、local-ci、git status。
Gate: 全部通过且无活动 blocker。
