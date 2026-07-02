# Task Overview
- Task ID: `0037`
- Slug: `measurement-infrastructure-otel-slo-alerts`
- Objective: `把 D7 SRE/可观测从 health/ready/metrics/requestId/structured log baseline 推进为本地可验证 trace/SLO/alert baseline：新增 W3C traceparent/OpenTelemetry 语义兼容 span 日志、API/provider/report 本地 trace smoke、SLO policy、alert rules、observability gate，并接入 quick CI、observability registry、API 文档、roadmap 与任务 closeout；不接外部 collector、不引入未锁定依赖、不声称生产监控已完成。`
- Status: `Done`

## In Scope
- 新增本地 trace runtime：W3C `traceparent` 解析/生成、trace context、OpenTelemetry 语义兼容 span 日志。
- 给 HTTP 请求、capability executor、provider validate/calculate、同步 Markdown report、Web report 计算和渲染补本地 span。
- 新增 SLO policy 与 alert rules 合同，覆盖 availability、latency、report job success、provider success、error budget、queue、provider outage、secret scan 和 evaluation regression。
- 新增 `observability-slo-gate` 和 `observability-trace-slo-smoke`，验证 trace 字段、SLO/alert 合同、traceparent 传播和隐私边界。
- 接入 `scripts/local-ci.sh --profile quick`、observability registry、API 文档、roadmap、AGENTS 和任务 closeout。

## Out of Scope
- 不接入外部 OpenTelemetry collector、trace backend、Prometheus、Alertmanager、Grafana、云监控或日志平台。
- 不新增未锁定 Python 依赖；当前实现不声称已安装 OpenTelemetry SDK。
- 不采集报告正文、姓名、出生地区、token、secret、DSN、webhook URL 或原始请求 payload。
- 不做真实生产 API 域名、真实 CORS、真实 token、Bot live smoke 或远端 GitHub Actions 当前 diff 验证。
- 不改变 provider 算法、八字/紫微规则、报告业务语义或 capability 成熟度。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 observability registry、runtime smoke、quick CI 和 D7 roadmap 缺口
TP-02 trace runtime baseline
  TP-02.01 新增 fate_core observability runtime 和 W3C traceparent 支持
  TP-02.02 接入 HTTP、capability、provider、report 和 web report span
TP-03 SLO/alert contract baseline
  TP-03.01 新增 SLO policy 与 alert rules 合同
  TP-03.02 更新 observability registry schema、signal 状态和 metadata
TP-04 gates、tests 与 quick CI
  TP-04.01 新增 SLO gate 与 trace SLO smoke
  TP-04.02 新增/更新 regression tests 并接入 quick CI
TP-05 文档、验证与 closeout
  TP-05.01 同步 API 文档、roadmap 和 AGENTS
  TP-05.02 运行验证、回填任务包并生成 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 D7 SRE/可观测缺口。
- 对齐基础设施同构：trace 用统一上下文贯穿入口、编排、provider 和报告层；SLO/alert 先合同化，再接外部平台。
- 对齐胶水原则：采用 W3C Trace Context 和 OpenTelemetry 语义字段，不自造私有 trace 语义；外部 SDK/collector 暂不引入。
- 对齐隐私边界：span 只记录低敏字段、状态、耗时和 ID，不记录用户命理输入或报告正文。
- 对齐生产诚实口径：本轮是本地可验证 baseline，外部监控、真实告警和 live smoke 仍待生产环境执行。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 `contracts/fate/observability/registry.json`、`scripts/observability-smoke.py`、`scripts/local-ci.sh` 和 D7 roadmap。 |
| TP-02 | Done | `fate_core/observability.py` 新增；HTTP/capability/provider/report/web report span 已接入。 |
| TP-03 | Done | `slo-policy.json`、`alert-rules.json` 和 observability registry 已同步。 |
| TP-04 | Done | `observability-slo-gate`、`observability-trace-slo-smoke`、回归测试和 quick CI hook 已新增。 |
| TP-05 | Done | API 文档、roadmap、AGENTS 已同步；focused validation 和 local quick CI 已通过；closeout packet 待生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
