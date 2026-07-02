# Task Overview

- Task ID: `0064`
- Slug: `measurement-infrastructure-otel-collector-slo-adapter`
- Objective: `执行 0061 后续任务树的 OTel collector/SLO adapter P0 切片：为 FateCat observability 新增 OpenTelemetry Collector dry-run 配置、SLO evidence contract、collector contract gate、回归测试和文档 closeout；本任务不接入真实 trace backend、不声明生产监控或真实 error budget 已完成。`
- Status: `Done`

## In Scope

- 新增 OpenTelemetry Collector dry-run 配置文件和 SLO evidence contract。
- 更新 ObservabilitySignal registry/schema/AGENTS、API 文档和 100% roadmap。
- 新增 `otel-collector-slo-gate` Python/sh wrapper、回归测试，并接入 `local-ci --profile quick` artifact。
- 运行 JSON/YAML syntax、gate CLI、focused tests、ruff、secret scan、task validators 和 quick local CI。

## Out of Scope

- 不启动真实 OpenTelemetry Collector。
- 不接入 Jaeger、Tempo、Grafana Cloud、Prometheus、Alertmanager、PagerDuty 或云监控。
- 不声明真实 trace backend、生产 error budget、alert live 或 incident drill 已完成。
- 不保存真实日志、用户输入、出生地区、报告正文、token、secret、DSN 或 production trace。

## Requirement Alignment

- 对齐 0061 推荐任务：`0064 OTel collector/SLO adapter plan`，要求 `collector config、trace smoke dry-run、SLO evidence contract`，且不能伪造 trace backend。
- 对齐当前 observability 事实：已有 health/ready/metrics/requestId、本地 OTel-compatible span log、SLO/alert rules baseline；仍缺 collector/exporter/backend 与真实 error budget 证据。
- 对齐基础设施定位：观测是生产可运维性资源，不是业务预测算法。
- 对齐不可伪造原则：本轮只证明 collector/SLO adapter 契约可发现、可校验、可文档化；外部 backend 和生产告警仍标记外部连通验证待执行。

## Task Package Tree

```text
TP-01 Observability context
  TP-01.01 复核 0061/0063、现有 observability registry、SLO/alert gate 和 trace smoke
TP-02 Collector/SLO contract baseline
  TP-02.01 新增 OTel collector dry-run config 和 SLO evidence contract
  TP-02.02 更新 observability registry、schema 和 AGENTS 边界
TP-03 Gate、测试和 CI
  TP-03.01 新增 otel-collector-slo-gate Python/sh wrapper
  TP-03.02 新增 regression tests 覆盖 config、contract、gate 和 privacy
  TP-03.03 接入 local-ci quick artifact
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、scripts AGENTS 和 INDEX
  TP-04.02 运行 validators、focused tests、lint/hygiene、quick local CI 并收口
```

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核观测契约现状和 0064 边界。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 读取 0061/0063、observability registry、SLO/alert gate、trace smoke 和官方 OTel collector 资料。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 新增 collector/SLO adapter contract baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 新增 OTel collector dry-run config 和 SLO evidence contract。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 更新 observability registry、schema 和 AGENTS。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.02 | - | No | No | Gate、测试和 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.02 | 3 | No | No | 新增 otel-collector-slo-gate。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 新增 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并收口。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
