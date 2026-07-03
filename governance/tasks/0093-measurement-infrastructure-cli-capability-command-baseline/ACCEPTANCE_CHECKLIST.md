# Acceptance Checklist

# Global Standards
- [x] 不重写测算算法，只做入口、smoke、contract、门禁和文档接线。
- [x] production capability 通过统一 `CapabilityExecutor` 执行。
- [x] planned capability 仍拒绝执行。
- [x] CLI surface 保持 `partial`，不声明标准 Markdown 多端同源。
- [x] smoke summary 不保存完整报告正文、姓名、token、secret、DSN、webhook URL 或生产账号。
- [x] 外部 live 项保持 `外部连通验证待执行`。

# Task Package Checklists
## TP-01.01 确认 fate_core.cli capability 复用 CapabilityExecutor

Verify: `sed -n '220,260p' domains/fate-analysis/services/fate-core/src/fate_core/cli.py`。

Gate: `_run_capability_execute` 调用 `CapabilityExecutor().execute(CapabilityInput(...))`。

- [x] CLI executor 链路已复核。

## TP-01.02 确认 planned capability 拒绝策略已有单测覆盖

Verify: `tests/regression/test_fate_core_cli.py::test_main_capability_rejects_planned_system`。

Gate: liuyao 必须 `exit_code == 1` 且错误包含 `尚未生产化`。

- [x] planned 拒绝策略已复核并由 smoke 再次覆盖。

## TP-02.01 新增 scripts/capability-cli.sh

Verify: `bash scripts/capability-cli.sh bazi --input-json <redacted-json> --output-file <tmp>`。

Gate: 脚本只转发到 `python -m fate_core.cli capability`，不实现测算逻辑。

- [x] 根级 wrapper 已新增。

## TP-02.02 新增 scripts/capability-cli-smoke.py/.sh

Verify: `bash scripts/capability-cli-smoke.sh --output-json /tmp/fatecat-capability-cli-smoke-0093.json`。

Gate: bazi/ziwei/almanac/meihua passed；liuyao planned rejection passed；summary 只存 hash/key/status。

- [x] capability CLI smoke 已新增并通过。

## TP-03.01 新增 cli-capability-command contract 并更新 surface.cli registry

Verify: `python3 -m json.tool contracts/fate/delivery/cli-capability-command.json` 和 `registry.json`。

Gate: `surface.cli.status=partial`，`outputContracts` 和 `localVerification` 包含 CLI contract/smoke。

- [x] Delivery contract 和 registry 已接线。

## TP-03.02 接入 scripts/local-ci.sh quick gate 和 summary artifact

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0093`。

Gate: quick 运行 `CLI capability smoke`，summary artifacts 包含 `capabilityCliSmoke`。

- [x] local-ci quick gate 已接入并通过。

## TP-03.03 更新 scripts/tests/delivery AGENTS 与 regression test

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_cli_smoke.py tests/regression/test_fate_core_cli.py`。

Gate: regression 锁定 smoke summary、registry contract、local-ci 和 AGENTS wiring。

- [x] 文档和回归测试已更新。

## TP-04.01 修复 0092 secret scan 文档误报

Verify: `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0093.json`。

Gate: findingCount 0；只将类似配置赋值的 webhook 链接文字改为 Markdown 链接。

- [x] 0092 文档误报已修复。

## TP-04.02 运行 focused regression、ruff、secret scan 和 local-ci quick

Verify: focused pytest、ruff check、ruff format、secret scan、local-ci quick。

Gate: 全部 exit 0；local-ci quick 267 tests passed。

- [x] 验证已通过。

## TP-04.03 回填任务包与路线图状态

Verify: `validate_task_docs.py --task-dir governance/tasks/0093-measurement-infrastructure-cli-capability-command-baseline --phase closeout`。

Gate: 任务包无占位符，INDEX/roadmap 状态同步。

- [x] closeout 文档已回填。
