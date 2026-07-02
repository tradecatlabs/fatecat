# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：只证明 Postgres webhook outbox worker lease negative path。
- [x] 证据来源明确：blocked preflight、real Postgres smoke、focused tests、local-ci 和 task validators。
- [x] 外部生产未验证项明确保留：job execution worker lease、exactly-once、公网 webhook live、外部 Vault/KMS。
- [x] 隐私边界明确：summary 不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入。

# Task Package Checklists

## TP-01 边界与证据目标

Verify: 0071 closeout、runtime backend contract 和 roadmap 已确认。

Gate: 本任务只证明 Postgres webhook outbox lease negative path。

- [x] 0071 后缺口已明确。
- [x] non-claims 已写入任务包。

## TP-02 Worker lease negative smoke 实现

Verify: `scripts/postgres-worker-lease-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: duplicate claim、错误 owner release、lease expiry reclaim 均被脚本验证。

- [x] 并发 duplicate claim negative check 已实现。
- [x] 错误 owner release negative check 已实现。
- [x] lease expiry reclaim check 已实现。

## TP-03 Contract、文档和测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=worker_lease_smoke_baseline`。

- [x] RuntimeBackend contract 已同步。
- [x] local-ci quick 已加入 preflight artifact。
- [x] operations docs、roadmap、AGENTS 已同步。
- [x] focused regression 已新增。

## TP-04 验证、closeout 和交付

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan 和 task validator。

Gate: 本地验证通过，远端 CI 后续由 Git 交付刷新。

- [x] 语法检查通过。
- [x] blocked preflight 通过。
- [x] real Postgres smoke 通过。
- [x] focused tests 通过。
- [x] local-ci quick 通过。
- [x] task docs closeout validator 通过。
