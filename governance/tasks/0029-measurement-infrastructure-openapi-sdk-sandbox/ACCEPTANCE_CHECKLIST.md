# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] sandbox fixture 只使用北京和测试样本。
- [x] OpenAPI 导出有必备路径校验。
- [x] developer docs smoke 可执行 fixture 与示例检查。
- [x] quick CI 已接入 developer docs smoke。
- [x] quick CI、secret scan、diff check、task validators 和 closeout packet 全部通过。

# Task Package Checklists

## TP-01.01 盘点 OpenAPI、文档、示例和 CI
- [x] Verify: `rg -n "openapi|capabilities|local-ci|developer" scripts tests docs/reference-materials contracts/fate`
- [x] Gate: 现有缺口已确认。

## TP-01.02 回填任务契约
- [x] Verify: `validate_task_docs.py --phase decompose`
- [x] Gate: 任务树、scope 边界、out-of-scope 和验证计划已落盘。

## TP-02.01 新增 developer sandbox fixture
- [x] Verify: `python3 -m json.tool contracts/fate/developer/sandbox.json >/dev/null && rg -n "sandbox.almanac|sandbox.meihua|privacyBoundary" contracts/fate/developer/sandbox.json`
- [x] Gate: fixture 使用北京/测试样本，不含真实凭证。

## TP-02.02 新增 SDK/Agent 示例
- [x] Verify: `find docs/reference-materials/developer/examples -maxdepth 1 -type f -print | sort`
- [x] Gate: curl、Python、Node、Agent tool call 示例存在。

## TP-03.01 新增 OpenAPI 导出脚本
- [x] Verify: `bash scripts/export-openapi.sh --output /tmp/fatecat-openapi-0029.json && python3 -m json.tool /tmp/fatecat-openapi-0029.json >/dev/null`
- [x] Gate: 导出成功且必备路径存在。

## TP-03.02 新增 developer docs smoke
- [x] Verify: `bash scripts/developer-docs-smoke.sh --output-json /tmp/fatecat-developer-docs-smoke-0029.json --openapi-json /tmp/fatecat-openapi-smoke-0029.json`
- [x] Gate: docs smoke 返回 passed。

## TP-03.03 回归测试和 quick CI
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_developer_docs_smoke.py tests/regression/test_api_contracts.py -k 'developer_docs or openapi'`
- [x] Gate: focused tests 通过。
- [x] Verify: `rg -n "developer docs smoke|test_developer_docs_smoke.py" scripts/local-ci.sh`
- [x] Gate: quick CI 已串联 developer docs smoke 和测试文件。

## TP-04.01 更新文档和 AGENTS
- [x] Verify: `rg -n "developer docs smoke|export-openapi|sandbox fixture|OpenAPI" docs/reference-materials scripts/AGENTS.md contracts/fate/AGENTS.md docs/reference-materials/AGENTS.md`
- [x] Gate: 人类文档、目录说明和路线图同步。

## TP-04.02 执行门禁并 closeout
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。
- [x] Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py`
- [x] Gate: 0029 closeout 和全任务树校验通过。
