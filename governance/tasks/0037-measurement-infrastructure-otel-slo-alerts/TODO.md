# Execution Checklist
[x] TP-01.01 | P0 | 盘点 observability registry、runtime smoke、quick CI 和 D7 roadmap 缺口 | Verify: `rg -n "provider_report_traces|slo_and_alerts|observability" contracts/fate/observability/registry.json scripts/local-ci.sh docs/reference-materials/roadmap` | Gate: D7 缺 trace/SLO/alert 明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 `fate_core.observability`，实现 trace context、traceparent 和 span 日志 | Verify: `test -f domains/fate-analysis/services/fate-core/src/fate_core/observability.py` | Gate: trace runtime 文件存在 | Parallelizable: No
[x] TP-02.02 | P0 | 接入 HTTP、capability、provider、report 和 web report span | Verify: `rg -n "trace_span|Traceparent|X-Trace-ID" domains/fate-analysis/services/fate-core/src/fate_core domains/experience-delivery/services/fatecat-delivery/src` | Gate: 核心调用链 span 接入 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 `slo-policy.json` 与 `alert-rules.json` | Verify: `python3 -m json.tool contracts/fate/observability/slo-policy.json contracts/fate/observability/alert-rules.json` | Gate: SLO/alert JSON 可解析 | Parallelizable: Yes
[x] TP-03.02 | P0 | 更新 observability registry schema、signal 状态、metadata 和 API/protocol tests | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Gate: registry/API/protocol 可发现 | Parallelizable: No
[x] TP-04.01 | P0 | 新增 `observability-slo-gate` 与 `observability-trace-slo-smoke` | Verify: `bash scripts/observability-slo-gate.sh --output-json /tmp/fatecat-observability-slo-gate.json && bash scripts/observability-trace-slo-smoke.sh --output-json /tmp/fatecat-observability-trace-slo-smoke.json` | Gate: SLO gate 和 trace smoke passed | Parallelizable: No
[x] TP-04.02 | P0 | 新增/更新 regression tests，并接入 `scripts/local-ci.sh --profile quick` | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0037` | Gate: quick CI passed | Parallelizable: No
[x] TP-05.01 | P0 | 同步 API 文档、roadmap 和 AGENTS | Verify: `rg -n "trace|SLO|alert" docs/reference-materials/operations docs/reference-materials/roadmap contracts/fate/observability/AGENTS.md scripts/AGENTS.md` | Gate: 文档明确本地 baseline 和外部 pending | Parallelizable: Yes
[x] TP-05.02 | P0 | 运行 focused validation、local quick CI，回填任务包并生成 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0037-measurement-infrastructure-otel-slo-alerts --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
