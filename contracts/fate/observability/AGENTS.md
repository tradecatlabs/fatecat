# AGENTS.md - observability resources

## 目录用途

`contracts/fate/observability/` 是测算基础设施观测能力的资源真相源。这里登记 health、ready、metrics、requestId、结构化日志和未来 trace/span/SLO 信号，只做发现、审计和接入说明，不保存运行时日志、指标或 trace 数据。

## 目录结构

```text
observability/
├── AGENTS.md
├── alert-rules.json
├── registry.json
├── slo-policy.json
└── schemas/
    └── observability-signal.schema.json
```

## 职责边界

- `registry.json`：登记 ObservabilitySignal 资源，记录信号类型、状态、端点、字段、验证命令、隐私边界和外部连通状态。
- `slo-policy.json`：登记本地 SLO/error budget baseline，覆盖 availability、latency、report job success 和 provider success 目标。
- `alert-rules.json`：登记本地 alert rules baseline，覆盖 error budget burn、queue depth、provider outage、secret scan failure 和 evaluation regression。
- `schemas/observability-signal.schema.json`：定义观测信号资源字段，覆盖 health、readiness、metrics、logs、trace、SLO 和 alerts。
- `scripts/observability-smoke.sh`：本地观测 smoke 入口；用 TestClient 验证 health、ready、metrics、request-id、结构化 http_request log 和 registry metadata。
- `scripts/observability-slo-gate.sh`：本地 SLO/alert policy gate；只校验契约和规则，不读取真实生产指标或外部告警平台。
- `scripts/observability-trace-slo-smoke.sh`：本地 trace/SLO smoke；验证 W3C `traceparent`、OpenTelemetry 语义兼容 span 日志和 API/provider/report trace。
- 这里不保存真实日志、真实请求体、真实 token、生产指标快照或 trace 数据。
- 当前 trace/SLO/alert 是本地 baseline；OpenTelemetry SDK exporter、collector、trace backend、Prometheus/Alertmanager、生产监控平台和真实流量 error budget 仍是外部连通验证待执行。
