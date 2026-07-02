# Execution Checklist
[x] TP-01.01 | P0 | 盘点 MI-04.03、provider registry、executor 和现有 smoke 模式 | Verify: `rg -n "MI-04.03|Provider health|dependency smoke|CapabilityExecutor" docs governance domains scripts tests` | Gate: MI-04.03 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 provider dependency smoke 脚本和脱敏 fixture | Verify: `bash scripts/provider-dependency-smoke.sh --output-json /tmp/fatecat-provider-dependency-smoke.json` | Gate: status passed, providerCount=4 | Parallelizable: No
[x] TP-02.02 | P0 | 接入 quick local-ci | Verify: `rg -n "provider dependency smoke|test_provider_dependency_smoke" scripts/local-ci.sh` | Gate: quick CI 包含脚本和测试 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 provider dependency smoke pytest | Verify: `.venv/bin/python -m pytest -q tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema'` | Gate: focused tests pass | Parallelizable: No
[x] TP-03.02 | P0 | 运行 quick local-ci | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-dependency-smoke` | Gate: quick CI passes | Parallelizable: No
[x] TP-04.01 | P1 | 同步 API 文档、roadmap、AGENTS 和任务索引 | Verify: `rg -n "provider-dependency-smoke|MI-04.03|0033" docs/reference-materials scripts/AGENTS.md domains/fate-analysis/services/fate-core/src/fate_core/capabilities/AGENTS.md governance/tasks/INDEX.md` | Gate: 不夸大真实公网 live smoke | Parallelizable: No
[x] TP-04.02 | P0 | 生成任务 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0033-measurement-infrastructure-provider-dependency-smoke --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
