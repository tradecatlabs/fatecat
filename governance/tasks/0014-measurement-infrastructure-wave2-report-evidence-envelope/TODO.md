# Execution Checklist
[x] TP-01.01 | P0 | 新增 Report schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'report or capability'` | Gate: schema 声明 Report resource、sections、evidenceRefs。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 更新 output/evidence/resource schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'report or capability'` | Gate: output requiredFields 包含 report，resource 有 reportResourceFields。 | Parallelizable: Yes
[x] TP-02.01 | P0 | capability response 增加 report envelope | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report or capability or metadata or openapi'` | Gate: production capability response 包含 Report resource。 | Parallelizable: No
[x] TP-02.02 | P0 | 暴露 report schema links | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report or capability or metadata or openapi'` | Gate: schemas/report 和 `/reports` 可发现。 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 report envelope 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'report or capability or metadata or openapi'` | Gate: report schema、response、OpenAPI 被覆盖。 | Parallelizable: No
[x] TP-03.02 | P0 | 更新文档和路线图 | Verify: `rg -n "report.schema|Report resource|evidenceRefs" docs/reference-materials contracts/fate/capabilities governance/tasks/0014-measurement-infrastructure-wave2-report-evidence-envelope` | Gate: API 文档和计划同步。 | Parallelizable: No
[x] TP-04.01 | P0 | 运行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: quick CI、governance strict、diff check 通过。 | Parallelizable: No
[x] TP-04.02 | P0 | 收口任务文档 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0014 closeout 无占位符，任务树全量有效。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
