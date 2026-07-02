# Acceptance Checklist

# Global Standards
- [x] Scope 明确，不混入外部监控平台、生产部署或 live smoke。
- [x] trace 使用 W3C Trace Context / OpenTelemetry 语义兼容字段，不自造私有语义。
- [x] span 隐私边界明确，不输出姓名、出生地区、报告正文或凭证。
- [x] SLO/alert 明确为本地合同和门禁，不声明生产告警已上线。
- [x] quick CI hook 已接入并通过。
- [x] task closeout packet 生成。

# Task Package Checklists
## TP-01.01 现状审计
Verify: `rg -n "provider_report_traces|slo_and_alerts|observability" contracts/fate/observability/registry.json scripts/local-ci.sh docs/reference-materials/roadmap`

Gate: D7 缺 trace/SLO/alert 明确。

- [x] 已盘点 observability registry、runtime smoke、quick CI 和 roadmap。

## TP-02.01 trace runtime
Verify: `test -f domains/fate-analysis/services/fate-core/src/fate_core/observability.py`

Gate: trace context、traceparent 和 span log helper 存在。

- [x] `fate_core.observability` 已新增。

## TP-02.02 instrumentation
Verify: `rg -n "trace_span|Traceparent|X-Trace-ID" domains/fate-analysis/services/fate-core/src/fate_core domains/experience-delivery/services/fatecat-delivery/src`

Gate: HTTP、capability、provider、report 和 web report span 接入。

- [x] HTTP middleware 已接入 trace context 和 response headers。
- [x] capability executor 已接入 `capability.execute`、`provider.validate`、`provider.calculate`。
- [x] report 和 web report 计算/渲染已接入 span。

## TP-03.01 SLO/alert contracts
Verify: `python3 -m json.tool contracts/fate/observability/slo-policy.json contracts/fate/observability/alert-rules.json`

Gate: 4 个 SLO objective 和 5 条 alert rule 可解析。

- [x] `slo-policy.json` 已新增。
- [x] `alert-rules.json` 已新增。

## TP-03.02 registry metadata
Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`

Gate: registry/API/protocol 可发现 trace/SLO baseline。

- [x] `signal.provider_report_traces` 标记本地 available。
- [x] `signal.slo_and_alerts` 标记本地 available。
- [x] external connectivity 明确 pending。

## TP-04.01 gates and smokes
Verify: `bash scripts/observability-slo-gate.sh --output-json /tmp/fatecat-observability-slo-gate.json && bash scripts/observability-trace-slo-smoke.sh --output-json /tmp/fatecat-observability-trace-slo-smoke.json`

Gate: SLO gate 和 trace SLO smoke passed。

- [x] SLO gate passed，objectives=4，alertRules=5，checks=40。
- [x] Trace SLO smoke passed，spans=7，alertRules=5。

## TP-04.02 quick CI/tests
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0037`

Gate: quick CI passed。

- [x] focused pytest passed，90 passed。
- [x] quick CI passed，summary timestamp 2026-07-02T13:04:34+08:00。

## TP-05.01 docs
Verify: `rg -n "trace|SLO|alert" docs/reference-materials/operations docs/reference-materials/roadmap contracts/fate/observability/AGENTS.md scripts/AGENTS.md`

Gate: 文档明确本地 baseline 和外部 pending。

- [x] API 接入文档、roadmap、AGENTS 已同步。

## TP-05.02 closeout
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0037-measurement-infrastructure-otel-slo-alerts --phase closeout`

Gate: closeout packet 写入任务目录。

- [x] closeout validator 通过，`TASK_CLOSEOUT_PACKET.json` 已生成。
