# Task-Level Acceptance
- webhook callback payload 是 `WebhookEvent` resource envelope，包含 `eventType=report_job.terminal`、`eventId/id`、job 状态和 status/cancel links。
- 提供 secret 时使用 `X-FateCat-Webhook-Signature: sha256=<hmac>`。
- callback 只在 `succeeded` / `failed` / `cancelled` 终态触发。
- API 默认关闭 callback；提供 URL 时未开启必须拒绝。
- 响应、audit_event、SQLite store 和 webhook payload 不泄露 webhook secret、Markdown 正文、姓名或出生地区。
- 本地 smoke 和 pytest 可复现验证。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| JSON registry parse | `python3 -m json.tool contracts/fate/security/registry.json` | Passed |
| webhook smoke | `bash scripts/webhook-smoke.sh --output-json /tmp/fatecat-webhook-smoke.json` | Passed |
| webhook focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook tests/regression/test_webhook_smoke.py` | Passed |
| broader related tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py tests/regression/test_webhook_smoke.py` | Passed |
| production readiness static | `env FATE_CORS_ALLOW_ORIGINS=https://fatecat.tradecatlabs.example FATE_RECORDS_ENABLED=0 FATE_DEPLOYMENT_REPLICAS=1 FATE_RATE_LIMIT_BACKEND=gateway FATE_EDGE_BODY_LIMIT_ENABLED=1 FATE_TRUST_PROXY_HEADERS=1 FATE_ENABLE_HSTS=1 bash scripts/production-readiness.sh --skip-bootstrap` | Passed; live skipped |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-webhook` | Passed; 102 regression tests passed |

# Review Gate
- 检查 callback 执行是否在锁外。
- 检查 callback 失败是否不会改变 job 状态。
- 检查 API/audit/log 不输出 URL secret。
- 检查文档没有声明真实公网 webhook live smoke、retry queue 或分布式任务系统已完成。

# Runtime Verification Gate
- quick CI 已通过，任务可标记 Done。
- 外部连通验证待执行：真实接收端、真实域名、真实 token、Bot live smoke。

# Ship Readiness
- 当前本地 baseline 已完成，可进入后续 retry/live smoke 任务。
- 不可声明生产 webhook 完整可靠：retry、DLQ、receiver SLA、external backend、live smoke 均未完成。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | runtime/API callback baseline 通过 focused tests。 |
| TP-03 | smoke simulator 接入 quick CI。 |
| TP-04 | contracts/docs/env/AGENTS/roadmap 同步且任务文档可校验。 |

# Anti-Goals
- 不接真实公网 webhook 接收端。
- 不实现持久重试、DLQ、指数退避、签名轮换或 replay window。
- 不把 webhook secret 持久化。
- 不把 report markdown 或用户输入发给 webhook。
