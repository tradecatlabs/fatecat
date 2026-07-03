# Execution Checklist
[x] TP-01.01 | P0 | 确认 fate_core.cli capability 复用 CapabilityExecutor | Verify: `sed -n '220,260p' domains/fate-analysis/services/fate-core/src/fate_core/cli.py` | Gate: `_run_capability_execute` 调用 `CapabilityExecutor().execute(CapabilityInput(...))` | Parallelizable: No
[x] TP-01.02 | P0 | 确认 planned capability 拒绝策略已有单测覆盖 | Verify: `tests/regression/test_fate_core_cli.py::test_main_capability_rejects_planned_system` | Gate: liuyao 必须 `exit_code == 1` 且错误包含 `尚未生产化` | Parallelizable: No
[x] TP-02.01 | P0 | 新增根级 capability CLI wrapper | Verify: `bash scripts/capability-cli.sh bazi --input-json <redacted-json> --output-file <tmp>` | Gate: 脚本只转发到 `python -m fate_core.cli capability`，不实现测算逻辑 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 capability CLI smoke | Verify: `bash scripts/capability-cli-smoke.sh --output-json /tmp/fatecat-capability-cli-smoke-0093.json` | Gate: production capability passed，planned capability rejected，summary 只存 hash/key/status | Parallelizable: No
[x] TP-03.01 | P0 | 新增 delivery contract 并更新 surface.cli registry | Verify: `python3 -m json.tool contracts/fate/delivery/cli-capability-command.json` 和 `registry.json` | Gate: `surface.cli.status=partial` 且 contract/smoke 已接线 | Parallelizable: No
[x] TP-03.02 | P0 | 接入 local-ci quick gate 和 summary artifact | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0093` | Gate: quick 运行 `CLI capability smoke`，summary artifacts 包含 `capabilityCliSmoke` | Parallelizable: No
[x] TP-03.03 | P0 | 更新 AGENTS 与 regression test | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_cli_smoke.py tests/regression/test_fate_core_cli.py` | Gate: regression 锁定 smoke summary、registry contract、local-ci 和 AGENTS wiring | Parallelizable: No
[x] TP-04.01 | P0 | 修复 0092 secret scan 文档误报 | Verify: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0093.json` | Gate: findingCount 0；只改 Markdown 链接表达 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused regression、ruff、secret scan 和 local-ci quick | Verify: focused pytest、ruff check、ruff format、secret scan、local-ci quick | Gate: 全部 exit 0；local-ci quick 267 tests passed | Parallelizable: No
[x] TP-04.03 | P0 | 回填任务包与路线图状态 | Verify: `validate_task_docs.py --task-dir governance/tasks/0093-measurement-infrastructure-cli-capability-command-baseline --phase closeout` | Gate: 任务包无占位符，INDEX/roadmap 状态同步 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
