# Acceptance Checklist

# Global Standards
- [x] 改动只服务 report policy gate 切片。
- [x] 不引入新第三方依赖。
- [x] 不改变命理计算核心。
- [x] 不删除旧 API 字段。
- [x] `policyGate` 不扫描 `risk.forbiddenClaims` 清单自身。
- [x] 所有“通过”都有命令证据。

# Task Package Checklists
## TP-01.01 report policy scope

Verify: `rg -n "policyGate|forbidden claims|禁止性断语" contracts/fate/capabilities docs/reference-materials governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate`

Gate: scope、excludedFields、contentCoverage 不夸大。

- [x] 已完成：`policyGate` scope、contentCoverage 和 excludedFields 已写入 schema、API response 与文档。

## TP-01.02 report schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'report or policy or capability'`

Gate: `requiredReportFields` 包含 `policyGate`，后续项文字不再说 scanner 未实现。

- [x] 已通过：`test_capability_protocol.py -k 'policy or report or capability'` 16 passed。

## TP-02.01 forbidden claims scanner

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy'`

Gate: fail/pass 单测覆盖，排除字段不自误报。

- [x] 已通过：scanner fail/pass 单测覆盖，排除 `report.risk.forbiddenClaims`。

## TP-02.02 report envelope policyGate

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'capability and report'`

Gate: API response 包含 `report.policyGate.status=pass`。

- [x] 已通过：组合定向回归覆盖 API response 的 `report.policyGate.status=pass`。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or report or capability or metadata or openapi'`

Gate: protocol/API 组合回归通过。

- [x] 已通过：`test_api_contracts.py test_capability_protocol.py -k 'policy or report or capability or metadata or openapi'` 37 passed。

## TP-03.02 docs

Verify: `rg -n "policyGate|forbidden claims|禁止性断语" docs/reference-materials contracts/fate/capabilities governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate`

Gate: 文档说明最小门禁与后续 snapshot gate 区别。

- [x] 已完成：API 文档、100% 计划、contracts AGENTS 同步最小 policyGate 口径。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: quick CI、governance strict、diff check 通过。

- [x] 已通过：quick CI 68 passed，governance strict PASS，diff check PASS。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate --phase closeout`

Gate: 任务 closeout 通过。

- [x] 已通过：closeout validator 和全任务树 validator 已通过。

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
