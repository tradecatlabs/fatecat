# Acceptance Checklist

# Global Standards
- [x] 不改变默认综合八字 Markdown
- [x] planned 能力仍不执行
- [x] resource schema 已新增
- [x] error schema 和 errors catalog 已新增
- [x] capability detail API 已新增
- [x] errors API 已新增
- [x] 定向 pytest 通过
- [x] quick CI 通过
- [x] governance strict 通过
- [x] task closeout 通过

# Task Package Checklists
## TP-01.01 resource schema

Verify: `test -f contracts/fate/capabilities/schemas/resource.schema.json`

Gate: schema 包含核心资源类型。

- [x] 已新增 resource schema。

## TP-01.02 error schema and catalog

Verify: `test -f contracts/fate/capabilities/schemas/error.schema.json && test -f contracts/fate/capabilities/errors.json`

Gate: 标准错误码可被 API 读取。

- [x] 已新增 error schema。
- [x] 已新增 errors catalog。

## TP-02.01 capability detail endpoint

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k capability_detail`

Gate: detail API 返回资源字段。

- [x] 已新增 `/api/v1/capabilities/{capability_id}`。
- [x] 已新增 `/capabilities/{capability_id}`。

## TP-02.02 errors endpoint

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k error_catalog`

Gate: `/errors` 与 `/api/v1/errors` 同源。

- [x] 已新增错误码 API。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error'`

Gate: 定向回归通过。

- [x] 23 passed。

## TP-03.02 docs

Verify: `rg -n "/errors|/capabilities/\\{capability_id\\}" docs/reference-materials/operations/测算基础设施\ API\ 接入.md`

Gate: 文档同步新入口。

- [x] API 接入文档已同步。
- [x] 100% 实现计划 Wave 1 状态已同步。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: 本地门禁通过。

- [x] quick CI 通过。
- [x] governance strict 通过。
- [x] git diff --check 通过。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0010-measurement-infrastructure-wave1-resources --phase closeout`

Gate: 任务容器 closeout 通过。

- [x] closeout 通过。
