# Task-Level Acceptance
- 仓库主定位统一为“测算基础设施”。
- capability registry 能表达成熟度、provider、engineVersion、evidencePolicy、testGate。
- CapabilityExecutor 仍拒绝 planned / experimental 能力，生产能力通过同一执行器执行。
- bazi / ziwei 作为生产样板暴露成熟度和门禁字段。
- API 至少提供 `/capabilities`、`/capabilities/{id}/calculate`、`/reports`、`/metadata` 兼容入口。

# Validation Plan
- `python3 governance/tools/governance_context_bundle.py --project-root . --task-type governance`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py`
- `bash scripts/local-ci.sh --profile quick`
- `git diff --check`

# Review Gate
- 不接受第二套 capability executor。
- 不接受 planned 能力可执行。
- 不接受 README/SKILL/contracts/branding 口径不一致。
- 不接受文档宣称 live production 已验证。

# Runtime Verification Gate
- focused regression 必须通过。
- quick CI 必须通过。
- governance context bundle 不再因缺少 `文档治理规则.md` 阻塞。

# Ship Readiness
- 本地通过后可以提交并推送。
- 外部生产域名、真实 token、Bot live smoke 仍标记为外部连通验证待执行。

# Task Package Acceptance
- TP-01：路线图和治理规则存在，定位 baseline 可提交。
- TP-02：registry/schema/tests 同步。
- TP-03：executor provider map 和拒绝策略有测试。
- TP-04：bazi/ziwei 样板字段有 API 回归。
- TP-05：API alias 和 metadata 有 contract tests。

## TP-01.01 定位口径提交

Verify: `git log -1 --oneline` 与 `git status --short --branch`

Gate: 定位基线有独立提交，且 README / SKILL / AGENTS / branding 口径一致。

## TP-01.02 路线图文档

Verify: `test -f docs/reference-materials/roadmap/测算基础设施路线图.md`

Gate: 路线图区分定位、五阶段、成熟度和不做事项。

## TP-01.03 文档治理规则

Verify: `python3 governance/tools/governance_context_bundle.py --project-root . --task-type governance`

Gate: governance context bundle 不再因缺少文档治理规则而 BLOCK。

## TP-02.01 registry 基础设施字段

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: registry 暴露 maturity、engineVersion、evidencePolicy、testGate。

## TP-02.02 schema 与协议测试

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: schema 描述新增字段，测试拒绝缺字段回潮。

## TP-03.01 executor provider registry

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: 生产能力通过 provider map 执行，不新增第二套 executor。

## TP-03.02 planned 能力拒绝执行

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py::test_planned_capability_cannot_execute_as_production`

Gate: planned / experimental 能力仍在执行前被拒绝。

## TP-04.01 bazi/ziwei 样板字段

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: bazi / ziwei 暴露生产样板成熟度、engine 和 evidence policy。

## TP-04.02 API 暴露成熟度

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: `/api/v1/capabilities` 和兼容新入口返回 maturity/testGate/evidencePolicy。

## TP-05.01 基础设施 API 别名

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: `/capabilities`、`/capabilities/{id}/calculate`、`/reports`、`/metadata` 可用且复用旧服务链路。

## TP-05.02 API contract tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: 新入口有回归测试，旧入口不回归。

## TP-05.03 总验证

Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`

Gate: quick CI、diff whitespace、governance strict 通过。

# Anti-Goals
- 不得把未来体系塞入默认综合八字报告
- 不得虚构证据
- 不得把外部连通验证写成本地已通过
