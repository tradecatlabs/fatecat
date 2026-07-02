# Execution Checklist
[x] TP-01.01 | P0 | 新增 Provider schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'provider or capability'` | Gate: schema 声明 providerId、engineVersion、health。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 暴露 provider schema ref | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'provider or capability or metadata or openapi'` | Gate: capability resource schemas 包含 provider。 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 provider list/detail API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'provider or capability or metadata or openapi'` | Gate: `/providers` 和 `/providers/{provider_id}` 可用。 | Parallelizable: No
[x] TP-02.02 | P0 | capability link 指向 provider resource | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'provider or capability or metadata or openapi'` | Gate: capability detail links.provider 正确。 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 provider API 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'provider or capability or metadata or openapi'` | Gate: provider 发现、详情、OpenAPI 均被测试覆盖。 | Parallelizable: No
[x] TP-03.02 | P0 | 更新文档和路线图 | Verify: `rg -n "/providers|provider.schema|Provider resource" docs/reference-materials contracts/fate/capabilities governance/tasks/0013-measurement-infrastructure-wave2-provider-resources` | Gate: API 文档和计划同步。 | Parallelizable: No
[x] TP-04.01 | P0 | 运行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: quick CI、governance strict、diff check 通过。 | Parallelizable: No
[x] TP-04.02 | P0 | 收口任务文档 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0013 closeout 无占位符，任务树全量有效。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
