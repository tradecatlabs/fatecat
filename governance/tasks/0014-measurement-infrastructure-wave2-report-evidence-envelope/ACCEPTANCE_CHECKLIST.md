# Acceptance Checklist

# Global Standards
- [x] 改动只服务 report/evidence envelope 切片。
- [x] 不引入新第三方依赖。
- [x] 不改变默认 Markdown。
- [x] 不删除旧 API 字段。
- [x] 所有“通过”都有命令证据。

# Task Package Checklists
## TP-01.01 report schema

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k report`

Gate: schema 声明 Report resource、sections、evidenceRefs。

- [x] 已通过：`test_capability_protocol.py -k 'report or capability'` 15 passed。

## TP-01.02 output/evidence/resource schema

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k report`

Gate: output requiredFields 包含 report，resource 有 reportResourceFields。

- [x] 已通过：output/evidence/resource schema 同步。

## TP-02.01 report envelope

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k report`

Gate: production capability response 包含 Report resource。

- [x] 已通过：production capability response 包含 Report resource。

## TP-02.02 schema links

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k metadata`

Gate: schemas/report 和 `/reports` 可发现。

- [x] 已通过：schemas/report 和 `/reports.reportSchema` 可发现。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'report or capability or metadata or openapi'`

Gate: report schema、response、OpenAPI 被覆盖。

- [x] 已通过：组合定向回归 36 passed。

## TP-03.02 docs

Verify: `rg -n "report.schema|Report resource|evidenceRefs" docs/reference-materials contracts/fate/capabilities governance/tasks/0014-measurement-infrastructure-wave2-report-evidence-envelope`

Gate: API 文档和计划同步。

- [x] 已通过：API 文档、contracts AGENTS、100% 计划已同步。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: 本地门禁通过。

- [x] 已通过：quick CI 68 passed，governance strict PASS，diff check PASS。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0014-measurement-infrastructure-wave2-report-evidence-envelope --phase closeout`

Gate: 任务 closeout 通过。

- [x] 已通过：0014 closeout validator 和全任务树 validator 均通过。
