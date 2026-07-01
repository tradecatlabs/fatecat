# Execution Checklist
[ ] TP-01.01 | P0 | 提交 README / SKILL / AGENTS / branding 口径更新 | Verify: git log -1 --oneline && git status --short --branch | Gate: 定位基线有独立提交且工作树不混入无关文件。 | Parallelizable: No
[x] TP-01.02 | P0 | 补测算基础设施路线图 | Verify: test -f docs/reference-materials/roadmap/测算基础设施路线图.md | Gate: 路线图覆盖定位、阶段、成熟度和不做事项。 | Parallelizable: Yes
[x] TP-01.03 | P0 | 补文档治理规则 | Verify: python3 governance/tools/governance_context_bundle.py --project-root . --task-type governance | Gate: governance context bundle PASS。 | Parallelizable: Yes
[ ] TP-02.01 | P0 | registry 增加 maturity、engineVersion、evidencePolicy、testGate | Verify: .venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py | Gate: registry 新字段可解析并对 bazi/ziwei 有样板值。 | Parallelizable: No
[ ] TP-02.02 | P0 | schema 和协议测试覆盖新增字段 | Verify: .venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py | Gate: capability schema required fields 和 invariants 同步。 | Parallelizable: No
[ ] TP-03.01 | P0 | executor 使用 provider registry | Verify: .venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py | Gate: executor 不新增第二套执行器且生产能力通过 provider map。 | Parallelizable: No
[ ] TP-03.02 | P0 | planned / experimental 能力继续拒绝执行 | Verify: .venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py::test_planned_capability_cannot_execute_as_production | Gate: planned 能力执行前失败。 | Parallelizable: No
[ ] TP-04.01 | P0 | bazi/ziwei 标记 L4 production 样板字段 | Verify: .venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py | Gate: bazi/ziwei 暴露成熟度、engine 和 evidence policy。 | Parallelizable: No
[ ] TP-04.02 | P0 | API 返回成熟度、测试门禁和 evidence policy | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py | Gate: API 能看到 maturity/testGate/evidencePolicy。 | Parallelizable: No
[ ] TP-05.01 | P1 | 补 /capabilities、/capabilities/{id}/calculate、/reports、/metadata | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py | Gate: 新入口可用且复用旧服务链路。 | Parallelizable: No
[ ] TP-05.02 | P1 | API contract tests 覆盖新入口 | Verify: .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py | Gate: 新旧入口均有回归。 | Parallelizable: No
[ ] TP-05.03 | P0 | quick CI、governance strict、Git diff hygiene | Verify: bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check | Gate: 本地门禁通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
