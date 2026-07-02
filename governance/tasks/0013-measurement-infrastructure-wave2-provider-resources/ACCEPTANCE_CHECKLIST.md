# Acceptance Checklist

# Global Standards
- [x] 改动只服务 provider resource 发现切片。
- [x] 不引入新第三方依赖。
- [x] 不暴露 token/secret/DSN。
- [x] 不让 planned capability 出现在 production provider 集合。
- [x] 所有“通过”都有命令证据。

# Task Package Checklists
## TP-01.01 provider schema

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k provider`

Gate: schema 声明 providerId、engineVersion、health。

- [x] 已通过：`test_capability_protocol.py -k 'provider or capability'` 14 passed。

## TP-01.02 provider schema refs

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k provider`

Gate: capability resource schemas 包含 provider。

- [x] 已通过：capability resource schema refs 包含 provider schema。

## TP-02.01 provider API

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k provider`

Gate: `/providers` 和 `/providers/{provider_id}` 可用。

- [x] 已通过：`/providers` 和 `/providers/{provider_id}` tests 通过。

## TP-02.02 capability provider link

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k capability`

Gate: capability detail links.provider 正确。

- [x] 已通过：capability detail links.provider 正确。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'provider or capability or metadata or openapi'`

Gate: provider 发现、详情、OpenAPI 均被测试覆盖。

- [x] 已通过：组合定向回归 22 passed。

## TP-03.02 docs

Verify: `rg -n "/providers|provider.schema|Provider resource" docs/reference-materials contracts/fate/capabilities governance/tasks/0013-measurement-infrastructure-wave2-provider-resources`

Gate: API 文档和计划同步。

- [x] 已通过：API 文档、contracts AGENTS、100% 计划已同步。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: 本地门禁通过。

- [x] 已通过：quick CI 68 passed，governance strict PASS，diff check PASS。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0013-measurement-infrastructure-wave2-provider-resources --phase closeout`

Gate: 任务 closeout 通过。

- [x] 已通过：0013 closeout validator 和全任务树 validator 均通过。
