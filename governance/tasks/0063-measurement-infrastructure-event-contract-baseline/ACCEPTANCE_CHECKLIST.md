# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 AsyncEvent contract baseline、gate、tests、docs 和任务文档。
- [x] 不实现真实公网 webhook live delivery。
- [x] 不连接外部 broker、消息队列或第三方消费者。
- [x] 不保存 webhook URL、secret、token、用户输入、出生地区、报告正文或 production log。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 读取 0061/0062、delivery contracts、report job/webhook/evaluation/release 事件事实。
- [x] 复核 CloudEvents 与 AsyncAPI 官方资料。
Verify: `sed` / `rg` / official docs。
Gate: 缺口明确。

## TP-02.01

- [x] 新增 AsyncEvent schema。
- [x] 新增 event registry。
- [x] 新增 AsyncAPI 风格文档。
- [x] 新增 synthetic CloudEvents examples。
Verify: JSON syntax + focused tests。
Gate: event contract 可发现。

## TP-02.02

- [x] resource schema 链接 AsyncEvent。
- [x] delivery registry 链接 event contract。
- [x] delivery AGENTS 说明职责边界。
Verify: focused tests / docs diff。
Gate: contract link 一致。

## TP-03.01

- [x] 新增 event-contract-gate Python 脚本。
- [x] 新增 shell wrapper。
Verify: gate CLI。
Gate: 无外部依赖。

## TP-03.02

- [x] regression tests 覆盖 gate summary。
- [x] regression tests 覆盖 CLI 输出。
- [x] regression tests 覆盖 registry links 与 examples。
Verify: focused pytest。
Gate: 边界断言通过。

## TP-03.03

- [x] quick local CI 运行 event contract gate。
- [x] quick local CI summary 包含 `eventContractGate` artifact。
Verify: local-ci summary artifact。
Gate: quick CI 运行新 gate。

## TP-04.01

- [x] API 文档写入 AsyncEvent contract。
- [x] roadmap 标记 0063 contract baseline。
- [x] scripts AGENTS 和 INDEX 同步。
Verify: docs diff + rg。
Gate: 文档不夸大。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/py_compile/secret scan 通过。
- [x] quick local CI 通过。
Verify: validation evidence。
Gate: 全部通过。
