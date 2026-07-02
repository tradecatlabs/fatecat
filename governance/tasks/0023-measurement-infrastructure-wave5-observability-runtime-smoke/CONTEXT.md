# Repo Evidence
- `contracts/fate/observability/registry.json` 已登记 available health、ready、metrics、requestId/structured logs，以及 planned trace/SLO/alert。
- `/health`、`/ready`、`/metrics` 和 `/observability` 已由 `main.py` 暴露。
- `tests/regression/test_api_contracts.py` 已有端点和日志断言，但缺少可运维复用的 smoke 脚本。
- roadmap 仍把完整观测运行链路标为未完成。

# Constraints Matrix
| 约束 | 决策 |
| --- | --- |
| 不依赖外部服务 | 使用 TestClient，不启动公网服务或 collector。 |
| 不保存敏感数据 | smoke 只保存检查名、布尔结果和摘要，不保存请求体或日志正文。 |
| 不夸大生产监控 | 文档明确 OpenTelemetry/collector/dashboard/SLO/alert 未完成。 |
| 可复现 | smoke 输出 JSON，可被 quick CI 和审计复核。 |

# Change Boundary
- 允许修改：`scripts/`、`contracts/fate/observability/`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0023-*`。
- 不允许修改：业务算法、报告生成、生产监控配置、外部 collector、生产日志存储。

# Risk Matrix
| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| smoke 被误解为生产监控完成 | 中 | registry/docs 明确 scope 和 not-covered。 |
| smoke 保存日志正文 | 中 | 只输出检查结果，不输出 log text。 |
| TestClient 与真实部署差异 | 中 | 标注为本地 smoke；生产外部验证仍待执行。 |

# Assumptions and Falsification
- 假设：本地 smoke 能证明当前 available signals 的最小运行链路。反证：若生产要求 collector、trace 和 alert，则进入后续 observability platform 任务。
- 假设：request-id 和 http_request log 字段足以证明当前日志链路。反证：若需要集中日志检索/retention，则进入日志平台任务。

# Critical Ambiguities
- OpenTelemetry backend、SLO 阈值、alert 接收方和 dashboard 形态未定；本任务不实现。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix，不维护 `DEBUG.md`。
- 若 smoke 失败，必须保留失败 check 名称、输出 JSON 和复现命令。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | observability 缺口和边界 |
| TP-02 | smoke script 与 registry |
| TP-03 | tests/docs/quick CI |
| TP-04 | 验证与 closeout |
