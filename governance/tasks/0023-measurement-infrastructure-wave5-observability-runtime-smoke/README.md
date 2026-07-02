# Task Overview
- Task ID: `0023`
- Slug: `measurement-infrastructure-wave5-observability-runtime-smoke`
- Objective: `把 ObservabilitySignal 从资源发现推进到本地可执行观测 smoke：用 TestClient 验证 health、ready、metrics、request-id、结构化 http_request log 和 registry metadata，输出机器可读 summary JSON；不接入 OpenTelemetry collector、dashboard 或生产监控平台。`
- Status: `In Progress`

## In Scope
- 新增 `scripts/observability-smoke.py` / `.sh`。
- smoke 使用 FastAPI `TestClient` 验证 `/health`、`/ready`、`/metrics`、`X-Request-ID`、结构化 `http_request` log 和 `/observability` metadata。
- smoke 输出机器可读 JSON 到本地运行态目录或指定路径。
- 在 `contracts/fate/observability/registry.json` metadata 中登记 smoke command/scope/output。
- 补回归测试、quick CI 接入、API 文档、roadmap 和任务 closeout。

## Out of Scope
- 不接入 OpenTelemetry SDK、collector、trace backend、dashboard 或生产监控平台。
- 不实现 provider/report span、SLO/error budget、queue alert 或真实生产流量监控。
- 不保存真实日志、请求体、用户输入、报告正文、token、secret 或 DSN。

## Task Package Tree
```text
TP-01 Observability runtime 缺口盘点
  TP-01.01 盘点 registry、API、metrics、日志和 roadmap 缺口
  TP-01.02 回填任务契约与任务树
TP-02 本地 smoke 实现
  TP-02.01 新增 observability smoke 脚本
  TP-02.02 将 smoke 登记到 registry/AGENTS
TP-03 测试与文档
  TP-03.01 新增 observability smoke 回归测试
  TP-03.02 更新 contract/API tests 与 quick CI
  TP-03.03 更新 API 文档与 100% 路线图
TP-04 验证收口
  TP-04.01 执行 smoke、focused tests、ruff/format、quick CI 和 diff check
  TP-04.02 回填 closeout 状态、全任务树验证和 closeout packet
```

## Requirement Alignment
- 用户目标：持续把 FateCat 推进为测算基础设施。
- 本任务切片：把观测资源从“可发现”推进到“本地可执行 smoke 可证明”，覆盖 health/ready/metrics/log/request-id 的当前 available 信号。
- 完成口径：本地观测链路可 smoke；OpenTelemetry、SLO、alert、dashboard 和生产监控仍是后续任务。

## Task Package Overview
| Node | Type | Purpose | Gate |
| --- | --- | --- | --- |
| TP-01 | SPEC | 明确 runtime smoke 范围 | 不夸大为生产监控 |
| TP-02 | BUILD | 新增 smoke 脚本与 registry metadata | JSON 输出可复核 |
| TP-03 | TEST/DOC | tests/docs/quick CI 同步 | focused tests 通过 |
| TP-04 | SHIP | 执行门禁并 closeout | validators 与 quick CI 通过 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
