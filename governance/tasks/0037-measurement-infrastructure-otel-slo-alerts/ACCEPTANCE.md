# Task-Level Acceptance
- `fate_core.observability` 提供 W3C `traceparent` 解析/生成、trace context 和结构化 span 日志。
- HTTP response 包含 `Traceparent` 与 `X-Trace-ID`，结构化 `http_request` log 包含 `traceId`。
- capability executor 在 status gate 后执行 provider lookup，并为 `capability.execute`、`provider.validate`、`provider.calculate` 生成 span。
- 同步 Markdown report 和 Web report 计算/渲染生成 span。
- `contracts/fate/observability/slo-policy.json` 定义 4 个本地 SLO objective。
- `contracts/fate/observability/alert-rules.json` 定义 5 条 alert rule，并包含 severity、condition、runbook 和 signals。
- `contracts/fate/observability/registry.json` 登记 trace/SLO available 本地 baseline、verification command、schema 和 external connectivity pending。
- Trace smoke 验证 traceparent 传播、核心 span 存在、SLO gate 通过，并确认 span 不包含出生地区、姓名或报告正文。
- `scripts/local-ci.sh --profile quick` 已接入新门禁并通过。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/observability/registry.json contracts/fate/observability/slo-policy.json contracts/fate/observability/alert-rules.json` | Passed |
| shell syntax | `bash -n scripts/observability-slo-gate.sh scripts/observability-trace-slo-smoke.sh scripts/observability-smoke.sh scripts/local-ci.sh` | Passed |
| ruff check | `.venv/bin/python -m ruff check domains/fate-analysis/services/fate-core/src/fate_core/observability.py domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py domains/experience-delivery/services/fatecat-delivery/src/main.py domains/experience-delivery/services/fatecat-delivery/src/web_report_service.py scripts/observability-slo-gate.py scripts/observability-trace-slo-smoke.py scripts/observability-smoke.py tests/regression/test_observability_trace_slo.py tests/regression/test_observability_smoke.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check <same file set>` | Passed |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_observability_trace_slo.py tests/regression/test_observability_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Passed; 90 passed |
| SLO gate | `bash scripts/observability-slo-gate.sh --output-json /tmp/fatecat-observability-slo-gate.json` | Passed; objectives=4, alertRules=5, checks=40 |
| trace SLO smoke | `bash scripts/observability-trace-slo-smoke.sh --output-json /tmp/fatecat-observability-trace-slo-smoke.json` | Passed; spans=7, alertRules=5 |
| observability smoke | `bash scripts/observability-smoke.sh --output-json /tmp/fatecat-observability-smoke-0037.json` | Passed; checks=17 |
| local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0037` | Passed; summary timestamp 2026-07-02T13:04:34+08:00 |

# Review Gate
- Trace implementation uses W3C compatible IDs and response headers, but does not claim full OpenTelemetry SDK/exporter support.
- Span attributes are explicitly sanitized and low-sensitive; smoke asserts no name、birthPlace、report title/body in span logs.
- Planned capability still rejects before provider lookup; capability/API regression tests passed.
- SLO/alert contract is local policy/gate evidence only; no external alert delivery is claimed.
- `local-ci.sh` runs new gates before ruff/mypy/focused regression tests.

# Runtime Verification Gate
- Local TestClient smoke verifies `/capabilities/almanac/calculate` accepts incoming traceparent and returns matching `X-Trace-ID`.
- Local TestClient smoke verifies `/api/v1/report/markdown` produces `http.request`、`capability.execute`、`provider.validate`、`provider.calculate`、`report.calculate`、`report.render_markdown` spans.
- `observability-slo-gate` validates 4 SLO objectives and 5 alert rules.
- 外部连通验证待执行：collector/exporter、trace backend、Prometheus/Alertmanager/Grafana、生产告警投递、真实生产流量 SLO、远端 CI 当前 diff。

# Ship Readiness
- 当前 0037 本地切片可进入审计：runtime、contracts、scripts、tests、quick CI、文档和任务 closeout 均有本地证据。
- 不能声明测算基础设施可观测 100% 生产完成：缺外部 OpenTelemetry pipeline、真实 SLO burn rate、告警投递、dashboard/backend 和生产 live smoke。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | trace runtime 和核心调用链 span 落地。 |
| TP-03 | SLO policy、alert rules 和 observability registry 落地。 |
| TP-04 | SLO gate、trace SLO smoke、回归测试和 quick CI 落地。 |
| TP-05 | API 文档、roadmap、AGENTS、验证和 closeout 完成。 |

# Anti-Goals
- 不接外部 collector/exporter/backend。
- 不新增未锁定 OpenTelemetry SDK 依赖。
- 不采集姓名、出生地区、报告正文、token、secret、DSN、webhook URL 或原始 payload。
- 不声明真实生产 SLO、真实告警投递、远端 CI 或 live smoke 已完成。
- 不改变 provider 算法或报告业务语义。
