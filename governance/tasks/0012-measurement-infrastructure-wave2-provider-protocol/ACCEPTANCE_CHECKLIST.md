# Acceptance Checklist

# Global Standards
- [x] 改动只服务 IMP-03 provider 协议切片。
- [x] 不引入新第三方依赖。
- [x] 不改变默认 Markdown 体系。
- [x] 不让 planned capability 可执行。
- [x] 所有“通过”都有命令证据。

# Task Package Checklists
## TP-01.01 provider protocol

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k provider`

Gate: 协议对象包含 validate/calculate/metadata/health。

- [x] 已通过：`test_capability_protocol.py -k 'provider or capability'` 14 passed。

## TP-01.02 provider registry

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k provider`

Gate: bazi/ziwei/almanac/meihua 均有 provider，planned 无 provider。

- [x] 已通过：production providers 覆盖 bazi、ziwei、almanac、meihua。

## TP-02.01 executor migration

Verify: `python -m pytest -q tests/regression/test_capability_protocol.py -k capability`

Gate: 既有四个 production capability 执行行为不变。

- [x] 已通过：executor 经 provider registry 执行。

## TP-02.02 provider metadata and errors

Verify: `python -m pytest -q tests/regression/test_api_contracts.py -k metadata`

Gate: API metadata 可见 provider health；异常保留 capability/provider 上下文。

- [x] 已通过：API metadata 暴露 provider health。

## TP-03.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or provider or metadata or openapi or error or report_job'`

Gate: provider 协议、API、planned 拒绝均被测试覆盖。

- [x] 已通过：组合定向回归 30 passed。

## TP-03.02 docs and agents

Verify: `rg -n "ProviderProtocol|provider registry|provider health" domains/fate-analysis/services/fate-core/src/fate_core/capabilities docs/reference-materials/roadmap governance/tasks/0012-measurement-infrastructure-wave2-provider-protocol`

Gate: 局部架构说明和路线图状态同步。

- [x] 已通过：AGENTS、API 接入文档和 100% 计划已同步。

## TP-04.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: 本地门禁通过。

- [x] 已通过：quick CI 67 passed，governance strict PASS，diff check PASS。

## TP-04.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0012-measurement-infrastructure-wave2-provider-protocol --phase closeout`

Gate: 任务 closeout 通过。

- [x] 已通过：0012 closeout validator 和全任务树 validator 均通过。
