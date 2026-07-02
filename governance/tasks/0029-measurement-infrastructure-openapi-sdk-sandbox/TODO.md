# Execution Checklist
[x] TP-01.01 | P0 | 盘点 OpenAPI、API 文档、示例和 CI 入口 | Verify: `rg -n "openapi|capabilities|local-ci|developer" scripts tests docs/reference-materials contracts/fate` | Gate: 现有缺口明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约、范围和验证计划 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 developer sandbox fixture | Verify: `python3 -m json.tool contracts/fate/developer/sandbox.json >/dev/null` | Gate: fixture 只使用北京和测试样本 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 curl/Python/Node/Agent 最小示例 | Verify: `find docs/reference-materials/developer/examples -maxdepth 1 -type f -print | sort` | Gate: 四类示例存在且不含真实凭证 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 OpenAPI 导出脚本 | Verify: `bash scripts/export-openapi.sh --output /tmp/fatecat-openapi-0029.json` | Gate: 导出成功且校验必备路径 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 developer docs smoke 脚本 | Verify: `bash scripts/developer-docs-smoke.sh --output-json /tmp/fatecat-developer-docs-smoke-0029.json --openapi-json /tmp/fatecat-openapi-smoke-0029.json` | Gate: smoke passed | Parallelizable: No
[x] TP-03.03 | P0 | 新增回归测试并接入 quick CI | Verify: `.venv/bin/python -m pytest -q tests/regression/test_developer_docs_smoke.py tests/regression/test_api_contracts.py -k 'developer_docs or openapi'` | Gate: focused tests 通过且 local-ci 串联 smoke | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap 和目录级 AGENTS | Verify: `rg -n "developer docs smoke|export-openapi|sandbox fixture|OpenAPI" docs/reference-materials scripts/AGENTS.md contracts/fate/AGENTS.md docs/reference-materials/AGENTS.md` | Gate: 文档口径不夸大生产能力 | Parallelizable: No
[x] TP-04.02 | P0 | 执行门禁、任务验证和 closeout packet | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check && validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py` | Gate: 0029 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
