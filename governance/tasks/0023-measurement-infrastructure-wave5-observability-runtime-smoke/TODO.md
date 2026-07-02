# Execution Checklist
[x] TP-01.01 | P0 | 盘点 registry、API、metrics、日志和 roadmap 缺口 | Verify: `rg -n "observability|metrics|request-id|logs|SLO|ready" contracts docs scripts tests domains/experience-delivery/services/fatecat-delivery/src/main.py` | Gate: available signals 与 planned signals 边界明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约与任务树 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 observability smoke 脚本 | Verify: `bash scripts/observability-smoke.sh --output-json /tmp/fatecat-observability-smoke.json` | Gate: smoke 返回 passed 并覆盖 15 个 checks | Parallelizable: No
[x] TP-02.02 | P0 | 将 smoke 登记到 registry/AGENTS | Verify: `python3 -m json.tool contracts/fate/observability/registry.json >/dev/null && rg -n "observability-smoke|smokeCommand|smokeScope" contracts/fate/observability scripts/AGENTS.md` | Gate: registry metadata 与 AGENTS 均可定位 smoke 入口 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 observability smoke 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_observability_smoke.py` | Gate: script 函数和 CLI 输出均被覆盖 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 contract/API tests 与 quick CI | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k observability && rg -n "test_observability_smoke.py" scripts/local-ci.sh` | Gate: registry metadata、API payload 和 quick CI 测试入口一致 | Parallelizable: No
[x] TP-03.03 | P0 | 更新 API 文档与 100% 路线图 | Verify: `rg -n "observability-smoke|health/ready/metrics/request-id|OpenTelemetry|生产监控平台" docs/reference-materials` | Gate: 文档区分本地 smoke 与未完成生产监控 | Parallelizable: No
[x] TP-04.01 | P0 | 执行 smoke、focused tests、ruff/format、quick CI 和 diff check | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过 | Parallelizable: No
[x] TP-04.02 | P0 | 回填 closeout 状态、全任务树验证和 closeout packet | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0023 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
