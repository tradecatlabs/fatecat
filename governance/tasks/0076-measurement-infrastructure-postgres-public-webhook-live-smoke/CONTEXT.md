# Repo Evidence

- `backend.postgres.implementationStatus` 在任务开始时为 `external_worker_restart_smoke_baseline`，本任务推进为 `public_webhook_live_smoke_gate_baseline`
- `backend.postgres.status=planned`
- `backend.postgres.migration.blockedClaims` 包含 `public_webhook_live`、`external_vault_kms`、`exactly_once`
- `ReportJobManager._dispatch_terminal_webhook()` 已持久化 outbox 并调用 `webhook_dispatcher`
- `WebhookConfig` 已校验公网 URL，默认拒绝 http、本机和私网地址

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| 真实公网 webhook 不能伪造 | 无 `FATE_WEBHOOK_LIVE_URL` 时只 blocked。 |
| DSN/URL/secret 不能泄露 | summary 只输出 hash/fingerprint。 |
| 不新增协议 | 复用现有 HMAC header、payload 和 dispatcher。 |
| 不改变默认用户路径 | 新增脚本为可选 gate，不改 Web/API/Bot 默认行为。 |

# Change Boundary

允许改动：

- `scripts/postgres-public-webhook-live-smoke.py`
- `scripts/postgres-public-webhook-live-smoke.sh`
- `scripts/local-ci.sh`
- `scripts/runtime-backend-gate.py`
- `contracts/fate/delivery/runtime-backends.json`
- `contracts/fate/delivery/schemas/runtime-backend.schema.json`
- 相关 docs/AGENTS/tests/task docs

禁止改动：

- 默认报告内容和排盘逻辑
- API/Bot/Web 业务路径
- 真实环境配置、`.env`、生产 secret

# Risk Matrix

| Risk | Level | Mitigation |
| --- | --- | --- |
| 真实 HTTP POST 产生外部副作用 | high | 只在显式 env vars 存在时执行；summary 标注 target hash。 |
| 敏感配置泄露 | high | 禁止输出 DSN/URL/secret，加入敏感扫描和回归测试。 |
| 生产能力过度声明 | medium | contract 保持 `status=planned` 和 `shipGate=blocked`。 |

# Assumptions and Falsification

Assumption: 一个真实 endpoint 能返回 2xx 即可作为 live delivery proof。

Falsifier:

- endpoint 返回 4xx/5xx
- 网络失败
- summary 泄露敏感值
- outbox 未进入 `succeeded`

# Critical Ambiguities

- 当前环境是否有真实公网 webhook endpoint：未知；实现必须允许 blocked。
- 当前环境是否有真实 Postgres：可用性不作为本地 CI 强要求。

# Debug Evidence Contract

- 调试模式: Optional

本任务不是 bugfix。若 live smoke 失败，必须区分：

- missing external config -> `blocked`
- dependency missing -> `blocked`
- webhook endpoint/network failure -> `failed`
- code/contract/test failure -> 修复后重跑

# Task Package Context Map

0076 接续 0075。0075 已证明 Postgres external backend 可以用 expired job execution lease 恢复 stale running job，但明确没有证明公网 webhook live、外部 Vault/KMS、exactly-once 或 production ready。

## TP-01 PRECHECK

当前缺口、边界、风险和现有 report job/webhook 能力已审查；本任务只推进 public webhook live smoke gate。

## TP-02 IMPLEMENT

新增 `scripts/postgres-public-webhook-live-smoke.py` 与 `.sh`，复用现有 manager/store/dispatcher。

## TP-03 VERIFY

同步 runtime backend contract、schema/gate、local-ci、docs、AGENTS 和 regression tests。

## TP-04 TEST

执行 blocked preflight、runtime backend gate、focused regression、ruff、format、quick CI 和 task validators。

## TP-05 SHIP

完成 closeout、提交、推送并记录远端 CI。
