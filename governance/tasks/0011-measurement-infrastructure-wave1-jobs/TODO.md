# Execution Checklist
[x] TP-01.01 | P0 | job manager 支持 Idempotency-Key | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k idempotency` | Gate: 同一 key 返回同一 jobId。 | Parallelizable: No
[x] TP-01.02 | P0 | job manager 支持 cancelled 状态 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k cancelled` | Gate: cancel 后状态保持 cancelled，不写 succeeded result。 | Parallelizable: No
[x] TP-02.01 | P0 | job payload 暴露 CalculationJob resource links | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k report_job` | Gate: payload 包含 resourceType、apiVersion、links、cancelUrl。 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 cancel API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k cancel` | Gate: `/api/v1/report/jobs/{job_id}/cancel` 可用。 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 job 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or metadata or openapi'` | Gate: 定向 job/API 回归通过。 | Parallelizable: No
[x] TP-03.02 | P1 | 更新文档和 resource schema | Verify: `rg -n "Idempotency-Key|cancelled|cancel" docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md contracts/fate/capabilities/schemas/resource.schema.json` | Gate: 文档写明单进程 TTL 边界。 | Parallelizable: Yes
[x] TP-04.01 | P0 | 运行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: quick CI、governance、whitespace 通过。 | Parallelizable: No
[x] TP-04.02 | P0 | 收口任务容器 | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0011-measurement-infrastructure-wave1-jobs --phase closeout` | Gate: closeout 和全任务树通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
