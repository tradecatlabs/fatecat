# Acceptance Checklist

# Global Standards
- [x] provider dependency smoke 使用统一 `CapabilityExecutor`。
- [x] smoke 覆盖全部 production capability。
- [x] smoke summary 不保存完整报告正文。
- [x] 使用北京/测试用户脱敏固定样例。
- [x] docs/roadmap 标注真实公网 live 仍待执行。
- [x] quick local-ci 通过。
- [x] closeout packet 已生成。

# Task Package Checklists
## TP-01.01 context audit
- [x] Verify: `rg -n "MI-04.03|Provider health|dependency smoke|CapabilityExecutor" docs governance domains scripts tests`
- [x] Gate: MI-04.03 缺口明确。

## TP-02.01 smoke script
- [x] Verify: `bash scripts/provider-dependency-smoke.sh --output-json /tmp/fatecat-provider-dependency-smoke.json`
- [x] Gate: status passed, providerCount=4。

## TP-02.02 quick CI hook
- [x] Verify: `rg -n "provider dependency smoke|test_provider_dependency_smoke" scripts/local-ci.sh`
- [x] Gate: quick CI 包含脚本和测试。

## TP-03.01 pytest
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema'`
- [x] Gate: focused tests pass。

## TP-03.02 quick local-ci
- [x] Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-dependency-smoke`
- [x] Gate: quick CI passes。

## TP-04.01 docs/contracts
- [x] Verify: `rg -n "provider-dependency-smoke|MI-04.03|0033" docs/reference-materials scripts/AGENTS.md domains/fate-analysis/services/fate-core/src/fate_core/capabilities/AGENTS.md governance/tasks/INDEX.md`
- [x] Gate: 文档不夸大真实公网 live smoke。

## TP-04.02 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0033-measurement-infrastructure-provider-dependency-smoke --phase closeout`
- [x] Gate: closeout packet exists。
