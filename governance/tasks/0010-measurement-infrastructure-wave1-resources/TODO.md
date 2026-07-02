# Execution Checklist
[x] TP-01.01 | P0 | 新增 capability resource schema | Verify: `test -f contracts/fate/capabilities/schemas/resource.schema.json` | Gate: resource schema 包含 Capability、Provider、CalculationJob、Report、Evidence、Dataset、EvaluationRun。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 新增 error schema 和标准错误码字典 | Verify: `test -f contracts/fate/capabilities/schemas/error.schema.json && test -f contracts/fate/capabilities/errors.json` | Gate: error catalog 包含 capability/input/provider/evidence/auth/rate_limit/job/system 类错误。 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 capability detail API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k capability_detail` | Gate: `/capabilities/bazi` 返回 resourceType、schemas、links、admission。 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 errors API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k error_catalog` | Gate: `/errors` 与 `/api/v1/errors` 返回同一版本化错误码字典。 | Parallelizable: No
[x] TP-03.01 | P0 | 增加协议/API 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error'` | Gate: 定向回归通过。 | Parallelizable: No
[x] TP-03.02 | P1 | 更新 API 接入文档和 100% 计划状态 | Verify: `rg -n "/errors|/capabilities/\\{capability_id\\}" docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md` | Gate: 文档包含详情端点和错误码端点。 | Parallelizable: Yes
[x] TP-04.01 | P0 | 运行本地质量门禁 | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: quick CI、governance strict、whitespace 通过。 | Parallelizable: No
[x] TP-04.02 | P0 | 收口任务容器 | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0010-measurement-infrastructure-wave1-resources --phase closeout` | Gate: 0010 closeout 与任务树校验通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
