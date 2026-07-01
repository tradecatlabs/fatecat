# Execution Checklist
[x] TP-01.01 | P0 | `/metadata` 增加开发者发现、隐私和生产门禁字段 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k metadata` | Gate: 旧 metadata 字段不变，新 developer/privacy/productionGate 字段可断言。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 新增测算基础设施 API 接入文档并更新文档索引 | Verify: `test -f docs/reference-materials/operations/测算基础设施\\ API\\ 接入.md` | Gate: 文档覆盖 discovery、capability、reports、错误、隐私和本地验证。 | Parallelizable: Yes
[x] TP-02.01 | P0 | registry 增加 capability 准入校验 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k admission` | Gate: production/planned 不变量由代码强制。 | Parallelizable: No
[x] TP-02.02 | P0 | 增加 capability 准入和 OpenAPI 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi'` | Gate: 定向回归通过。 | Parallelizable: No
[x] TP-03.01 | P0 | 跑 quick CI、governance strict、task docs validator 和 git diff hygiene | Verify: `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` | Gate: 本地门禁通过且任务文档无占位符。 | Parallelizable: No
[x] TP-03.02 | P0 | 提交并推送当前硬化切片 | Verify: `git status --short --branch && git log -1 --oneline` | Gate: 本地提交存在且远端同步。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
