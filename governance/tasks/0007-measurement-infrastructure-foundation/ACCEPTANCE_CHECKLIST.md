# Acceptance Checklist

# Global Standards
- [x] 定位文档一致
- [x] 协议字段一致
- [x] executor 单一
- [x] planned 能力拒绝执行
- [x] bazi 唯一 default
- [x] API 兼容旧入口
- [x] quick CI 通过
- [x] governance strict 通过

# Task Package Checklists
- [x] TP-01 定位基线提交完成
- [x] TP-02 registry/schema/testGate 完成
- [x] TP-03 executor provider map 完成
- [x] TP-04 bazi/ziwei 样板完成
- [x] TP-05 API alias/metadata 完成

## TP-01.01 定位口径提交

Verify: `git log -1 --oneline`

Gate: 定位基线有独立提交。

- [x] 提交定位基线。

## TP-01.02 路线图文档

Verify: `test -f docs/reference-materials/roadmap/测算基础设施路线图.md`

Gate: 路线图存在并覆盖五阶段。

- [x] 已补路线图。

## TP-01.03 文档治理规则

Verify: `python3 governance/tools/governance_context_bundle.py --project-root . --task-type governance`

Gate: context bundle PASS。

- [x] 已补文档治理规则。

## TP-02.01 registry 基础设施字段

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: registry 新字段可读。

- [x] 增加 maturity、engineVersion、evidencePolicy、testGate。

## TP-02.02 schema 与协议测试

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: schema 和测试同步。

- [x] 更新 schema 和测试。

## TP-03.01 executor provider registry

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: executor 复用 provider map。

- [x] 收敛 executor 分支。

## TP-03.02 planned 能力拒绝执行

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py::test_planned_capability_cannot_execute_as_production`

Gate: planned 能力不可执行。

- [x] 保持拒绝策略。

## TP-04.01 bazi/ziwei 样板字段

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py`

Gate: bazi/ziwei 成为 production 样板。

- [x] 补样板字段。

## TP-04.02 API 暴露成熟度

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: API 返回成熟度和门禁。

- [x] 补 API 返回字段。

## TP-05.01 基础设施 API 别名

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: 新别名可用。

- [x] 补兼容入口。

## TP-05.02 API contract tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py`

Gate: 新旧入口均有回归。

- [x] 补测试。

## TP-05.03 总验证

Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`

Gate: 本地门禁通过。

- [x] 跑完整 quick 验证。
