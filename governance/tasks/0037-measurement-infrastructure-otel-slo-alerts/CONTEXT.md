# Repo Evidence
- `contracts/fate/observability/registry.json` 已存在 health、ready、metrics、requestId 和 structured log baseline；本轮新增 `signal.provider_report_traces` 与 `signal.slo_and_alerts` 的 available 本地 baseline。
- `scripts/observability-smoke.py` 已验证 health、ready、metrics、request-id 和结构化 http_request log；本轮补 trace/SLO/alert 专门门禁。
- `scripts/local-ci.sh --profile quick` 是当前本地快速门禁入口；本轮已接入 SLO gate 和 trace SLO smoke。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` D7 仍缺 trace、SLO 和 alert；本轮按本地可验证切片收敛，不声明外部生产监控完成。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 外部依赖 | 不新增未锁定 `opentelemetry-*` 依赖；先使用 W3C Trace Context 和 OpenTelemetry 语义兼容字段。 |
| 隐私 | trace/span 不采集姓名、出生地区、报告正文、token、secret、DSN 或 payload。 |
| 生产诚实口径 | registry 标记本地 available，外部 collector/backend/alert delivery 统一写 `external_connectivity_pending`。 |
| 兼容性 | 不改变现有 API 返回体；只追加 `Traceparent` 与 `X-Trace-ID` 响应头和结构化日志字段。 |
| 运行面 | 本轮只做 in-process span 日志，不做跨进程 worker trace、不做外部 exporter。 |

# Change Boundary
- Allowed: `fate_core` observability helper、capability executor、delivery HTTP/report/web report trace hook、observability contracts、smoke/gate scripts、regression tests、quick CI、docs/AGENTS/task docs。
- Not allowed: provider 算法重写、报告结构重写、生产部署脚本真实连通、外部监控平台接入、真实凭证处理。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把本地 span 误报为生产 OpenTelemetry | 审计误判生产可观测成熟度 | 文档和 registry 明确 external connectivity pending，不写 collector/backend 已接。 |
| span 泄露用户隐私 | 违反项目隐私边界 | trace smoke 检查姓名、出生地区和报告正文不进入 span。 |
| trace hook 破坏 planned capability 拒绝逻辑 | planned 能力可被执行 | provider lookup 放在 status gate 之后；相关 protocol/API 回归测试已通过。 |
| quick CI 变慢 | 本地开发成本上升 | smoke 使用 TestClient 和固定样例，不调用外部服务。 |

# Assumptions and Falsification
- Assumption: W3C traceparent + structured span logs 是当前最小可验证 trace baseline。
  Falsifier: 生产要求已明确必须接外部 collector/exporter 才能进入下一阶段。
- Assumption: SLO/alert 先合同化可降低后续平台迁移成本。
  Falsifier: alert rule 无法映射到 Prometheus/Alertmanager 或云监控条件。
- Assumption: 不记录 payload 能满足当前审计隐私要求。
  Falsifier: trace smoke 发现姓名、出生地区、报告正文或凭证进入 span。

# Critical Ambiguities
- 外部监控平台未选型：Prometheus/Grafana、OTel Collector、云厂商 APM 或日志平台待后续生产阶段决定。
- 生产 SLO 阈值仍需真实流量基线校准；当前阈值是 contract baseline，不是线上 error budget 结算事实。
- 异步 job worker 的跨线程/跨进程 trace 只做 submit span，持久队列和分布式 worker trace 待后续切片。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 如果 trace smoke、SLO gate 或 quick CI 失败，必须记录失败命令、失败检查项、根因和回归验证。

# Task Package Context Map
| Package | Required Context |
| --- | --- |
| TP-01 | Observability registry、runtime smoke、quick CI、D7 roadmap。 |
| TP-02 | `fate_core` capability executor、delivery middleware、report payload builder、web report service。 |
| TP-03 | Observability registry schema、SLO/alert 合同和 privacy policy。 |
| TP-04 | Shell wrappers、Python smoke/gate、regression tests、local CI。 |
| TP-05 | API 文档、roadmap、AGENTS、task closeout。 |
