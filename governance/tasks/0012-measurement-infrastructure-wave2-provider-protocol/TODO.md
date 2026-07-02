# Execution Checklist
[x] TP-01.01 | P0 | 定义 provider protocol | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'provider or capability'` | Gate: 协议对象包含 validate/calculate/metadata/health。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 建 production provider registry | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'provider or capability'` | Gate: bazi/ziwei/almanac/meihua 均有 provider，planned 无 provider。 | Parallelizable: Yes
[x] TP-02.01 | P0 | executor 改用 provider registry | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'provider or capability'` | Gate: 既有四个 production capability 执行行为不变。 | Parallelizable: No
[x] TP-02.02 | P0 | provider metadata、health 和错误边界 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'capability or provider or metadata or openapi or error or report_job'` | Gate: API metadata 可见 provider health；异常保留 capability/provider 上下文。 | Parallelizable: No
[x] TP-03.01 | P0 | 更新回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or provider or metadata or openapi or error or report_job'` | Gate: provider 协议、API、planned 拒绝均被测试覆盖。 | Parallelizable: No
[x] TP-03.02 | P0 | 更新文档和 AGENTS | Verify: `rg -n "ProviderProtocol|provider registry|provider health" domains/fate-analysis/services/fate-core/src/fate_core/capabilities docs/reference-materials/roadmap governance/tasks/0012-measurement-infrastructure-wave2-provider-protocol` | Gate: 局部架构说明和路线图状态同步。 | Parallelizable: No
[x] TP-04.01 | P0 | 运行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: quick CI、governance strict、diff check 通过。 | Parallelizable: No
[x] TP-04.02 | P0 | 收口任务文档 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0012 closeout 无占位符，任务树全量有效。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
