# Repo Evidence
- 当前工作目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`，工作树已有 0009-0017 未提交基础设施切片；本任务必须叠加增量，不得回滚旧改动。
- 现有 API 观测入口：
  - `GET /health`
  - `GET /live`
  - `GET /ready`
  - `GET /metrics`
- 现有观测实现：
  - `X-Request-ID` 响应头：`_apply_public_response_headers()`
  - 请求上下文：`_request_id_context`
  - 结构化 JSON 日志：`_log_structured()`、`_log_request()`、`_log_business_exception()`
  - Prometheus 文本指标：`fatecat_requests_total`、`fatecat_request_latency_seconds_*`、`fatecat_request_errors_total`、`fatecat_inflight_requests`、`fatecat_calculation_slots_*`、`fatecat_report_job_*`、`fatecat_bot_*`
  - readiness：数据库、capability registry。
- 当前缺口：没有 ObservabilitySignal schema、registry、`/observability` 发现 API，也没有把 trace/metric/log/health/readiness/SLO future work 作为基础设施资源登记。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不引入外部平台 | 本轮只做 schema/registry/API/docs/tests，不引入 collector、dashboard 或 SDK。 |
| 不改指标语义 | `/metrics` 输出保持兼容，只登记已存在指标和后续计划。 |
| 不伪造生产 SLO | SLO、p95/p99、alert rule 只登记为 planned/future，不写成已生产验证。 |
| 文档驱动 | 更新 `contracts/fate/AGENTS.md`、API 接入文档和 100% 路线图。 |
| 架构变更 | 新增 `contracts/fate/observability/` 时必须补局部 `AGENTS.md`。 |

# Change Boundary
允许修改：
- `contracts/fate/AGENTS.md`
- `contracts/fate/capabilities/schemas/resource.schema.json`
- `contracts/fate/observability/**`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `tests/regression/test_capability_protocol.py`
- `tests/regression/test_api_contracts.py`
- `docs/reference-materials/**`
- `governance/tasks/0018-measurement-infrastructure-wave5-observability-resources/**`

禁止修改：
- 业务计算逻辑、报告正文、provider 算法。
- `/metrics` 现有指标名称和 label 兼容性。
- 外部监控系统、CI 远端配置、真实生产域名或 Bot live smoke。
- Git 历史、分支、远端。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把“资源发现”夸成完整 SRE | 审计过度承诺 | registry 区分 `available` 与 `planned`，文档说明外部验证待执行。 |
| 改坏 `/metrics` | 影响监控接入 | 本轮不改 metrics 语义，补 API 发现测试。 |
| 观测资源噪声太多 | 维护负担 | 只登记代表性 signals：health、readiness、request metrics、job metrics、bot metrics、structured logs、request trace id、planned provider spans。 |
| 文档/API 漂移 | 开发者接入失败 | API contract、OpenAPI、metadata、文档同步测试。 |

# Assumptions and Falsification
Target end state:
FateCat 的观测能力和生产排障入口是可发现资源；开发者能通过 `/observability` 知道哪些 signals 已可用、端点在哪里、指标名是什么、哪些还只是未来计划。

Real constraints:
现有 `/health`、`/ready`、`/metrics`、requestId header、结构化日志已经存在；不引入外部监控平台。

Inertia constraints:
当前指标命名、main.py 单文件实现、历史任务编号不能决定长期观测架构；本轮只保持兼容并补发现层。

Wrong concept / wrong boundary:
把“有 `/metrics`”当成“观测基础设施完整”是错误边界；基础设施还需要 schema、registry、开发者入口和可审计能力状态。

Kill list:
删除“观测只藏在代码实现里，无法被 API/文档发现”的状态。

Proof point:
`/observability` 能列出 health/readiness/metrics/log/trace signals；schema/API tests 验证字段、状态、端点、指标名和 planned 边界。

Falsifier:
如果本轮需要改变指标语义或引入外部 collector 才能成立，说明切片过大，应回退为更小 registry/API 发现层。

Migration slice:
本轮只做只读资源发现；后续再做 provider span、report span、OpenTelemetry export、SLO/alert rules 和生产 dashboard。

Rejected short-term patches:
不只在 `/metadata` 写一段文字替代资源 API；不把 SLO 写成已上线；不把日志内容样例写入含敏感值的文档。

Existence check:
路线图 IMP-09 已列为 100% 基础设施必备项，且当前代码已有 signals；补 ObservabilitySignal 资源是把已有能力从代码细节提升为基础设施契约的最低成本。

Selected ladder rung:
项目原生能力 + 直接实现。使用 JSON registry 和 FastAPI 只读 endpoint，不引入新依赖。

Skipped scope:
OpenTelemetry SDK、collector、dashboard、alertmanager、长期 trace store、生产 SLO 实测。

Ceiling / upgrade path:
当需要跨服务 trace、provider span 和生产 SLO 时，升级为 OpenTelemetry/Prometheus/alert rules 的真实运行链路。

Do-not-simplify:
不能省略 signal 状态、endpoint、privacy/security boundary、externalConnectivity、planned/available 区分。

Minimal runnable check:
contract/API focused pytest、ruff、format、mypy、quick CI、task docs closeout 校验。

# Critical Ambiguities
- 是否要直接接入 OpenTelemetry：本轮不做；当前最小正确切片是资源化现有 signals。
- 是否要提供真实 SLO：本轮不做；没有生产流量和外部监控证据，不能伪造。
- 是否要记录日志样例：本轮不输出真实日志样例，只声明字段契约和脱敏边界。

# Debug Evidence Contract
- 调试模式: Optional

本任务不是 bugfix；若发现 API/schema 回归，必须在 `STATUS.md` 记录失败命令、失败摘要、修复点和复跑证据。

# Task Package Context Map
| Package | Context |
| --- | --- |
| TP-01 | 读取 `main.py` metrics/log/requestId/health/ready 实现和 API tests。 |
| TP-02 | 新增 `contracts/fate/observability/`，扩展 resource schema。 |
| TP-03 | 修改 FastAPI 只读发现入口和 metadata 链接。 |
| TP-04 | 补 tests 和 docs，确保机器契约与人类文档一致。 |
| TP-05 | 跑本地门禁并 closeout。 |
