# Acceptance Checklist

# Global Standards
- [x] production provider metadata 包含 lifecycle baseline 字段。
- [x] Provider/resource schema 声明 lifecycle 字段和最小 invariant。
- [x] vendor source 引用必须可追溯到 `vendor_sources.json#id`。
- [x] `iztro` 已登记为紫微 production dependency。
- [x] provider lifecycle gate 不读取用户输入、报告正文、token、secret、DSN 或生产环境。
- [x] focused provider tests 已通过。
- [x] quick local-ci 通过。
- [x] closeout packet 已生成。

# Task Package Checklists
## TP-01.01 context audit
- [x] Verify: `rg -n "ProviderMetadata|provider.schema|vendor_sources|MI-04|provider lifecycle" domains contracts tools docs scripts tests`
- [x] Gate: MI-04 provider lifecycle 缺口明确。

## TP-02.01 provider runtime metadata
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k provider`
- [x] Gate: runtime metadata 输出 versionLock/lifecycle/source/license/resource/promotion/deprecation。

## TP-02.02 provider/resource schemas
- [x] Verify: `python3 -m json.tool contracts/fate/capabilities/schemas/provider.schema.json`
- [x] Gate: schema required fields 与 runtime metadata 对齐。

## TP-02.03 vendor source policy
- [x] Verify: `python3 -m json.tool tools/reference-repos/vendor_sources.json`
- [x] Gate: `iztro` productionUseAllowed=true 且 licenseStatus=spdx。

## TP-03.01 provider lifecycle gate
- [x] Verify: `bash scripts/provider-lifecycle-gate.sh --output-json /tmp/fatecat-provider-lifecycle.json`
- [x] Gate: summary status passed, providerCount=4。

## TP-03.02 regression tests
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema' tests/regression/test_api_contracts.py -k provider`
- [x] Gate: provider lifecycle focused tests pass。

## TP-03.03 quick local-ci
- [x] Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-lifecycle`
- [x] Gate: quick CI passes。

## TP-04.01 docs/contracts
- [x] Verify: `rg -n "provider-lifecycle-gate|versionLock|MI-04.01|0032" docs/reference-materials scripts/AGENTS.md contracts/fate/capabilities/AGENTS.md domains/fate-analysis/services/fate-core/src/fate_core/capabilities/AGENTS.md`
- [x] Gate: docs/AGENTS/roadmap do not claim external live dependency completion。

## TP-04.02 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0032-measurement-infrastructure-provider-lifecycle-gates --phase closeout`
- [x] Gate: closeout packet exists。
