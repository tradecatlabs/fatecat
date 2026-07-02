# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 RuntimeBackend contract baseline、gate、tests、docs 和任务文档。
- [x] 不实现真实 Postgres/Temporal/Redis adapter。
- [x] 不连接真实数据库或外部服务。
- [x] 不保存 DSN、secret、token、password 或 production log。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 读取 0061、roadmap、delivery contracts、job store docs 和 gate 风格。
Verify: `sed` / `rg`。
Gate: 缺口明确。

## TP-02.01

- [x] 新增 RuntimeBackend schema。
- [x] 新增 RuntimeBackend registry。
- [x] 更新 resource schema link。
Verify: focused tests。
Gate: resource model 可发现。

## TP-02.02

- [x] delivery registry 链接 runtime backend contract。
- [x] delivery AGENTS 说明职责边界。
Verify: focused tests / docs diff。
Gate: contract link 一致。

## TP-03.01

- [x] 新增 runtime-backend-gate Python 脚本。
- [x] 新增 shell wrapper。
Verify: gate CLI。
Gate: 无外部依赖。

## TP-03.02

- [x] regression tests 覆盖 gate summary。
- [x] regression tests 覆盖 CLI 输出。
- [x] regression tests 覆盖 Postgres/SQLite/Redis contract 边界。
Verify: focused pytest。
Gate: 边界断言通过。

## TP-03.03

- [x] quick local CI 运行 runtime backend gate。
- [x] quick local CI summary 包含 `runtimeBackendGate` artifact。
Verify: local-ci summary artifact。
Gate: quick CI 运行新 gate。

## TP-04.01

- [x] API 文档写入 RuntimeBackend contract。
- [x] roadmap 标记 0062 contract baseline。
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
