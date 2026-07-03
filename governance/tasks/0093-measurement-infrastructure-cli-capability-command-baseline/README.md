# Task Overview
- Task ID: `0093`
- Slug: `measurement-infrastructure-cli-capability-command-baseline`
- Objective: `执行 0092 后的首个本地可执行多端交付切片：把现有 fate-core fatecat capability CLI 从已存在的单元测试能力提升为可复核的基础设施交付面基线，新增根级脚本入口、机器可读 smoke、delivery contract、registry/local-ci/docs/tests 接线；必须复用统一 CapabilityExecutor/provider admission，不重新实现测算逻辑，不声明标准 Markdown 多端同源或外部 live 已完成。`
- Status: `Done`

## In Scope
- 复核现有 `fate_core.cli` capability 命令是否已经进入 `CapabilityExecutor`。
- 新增根级 `scripts/capability-cli.sh` wrapper，提供稳定本地命令入口。
- 新增 `scripts/capability-cli-smoke.py/.sh`，以机器可读 summary 验证 production capability 可执行和 planned capability 拒绝。
- 新增 `contracts/fate/delivery/cli-capability-command.json`，并接入 `surface.cli` registry、local-ci、AGENTS 和回归测试。
- 修复 0092 调研文档中触发 secret scan 的 webhook 链接误报写法。

## Out of Scope
- 不重新实现八字、紫微、黄历、梅花或任何测算算法。
- 不把 CLI 声明为标准 Markdown 多端同源交付面。
- 不声明真实 API、Telegram Bot、Hugging Face Space、外部 Postgres、webhook、IdP、SIEM、OTel backend 或 Vault/KMS live 已完成。
- 不新增六爻、奇门、大六壬等 planned capability 的 production 实现。

## Task Package Tree
```text
TP-01 现有 CLI 能力链路复核
  TP-01.01 确认 fate_core.cli capability 复用 CapabilityExecutor
  TP-01.02 确认 planned capability 拒绝策略已有单测覆盖
TP-02 根级入口与机器可读 smoke
  TP-02.01 新增 scripts/capability-cli.sh
  TP-02.02 新增 scripts/capability-cli-smoke.py/.sh
TP-03 Delivery contract、local-ci 和文档接线
  TP-03.01 新增 cli-capability-command contract 并更新 surface.cli registry
  TP-03.02 接入 scripts/local-ci.sh quick gate 和 summary artifact
  TP-03.03 更新 scripts/tests/delivery AGENTS 与 regression test
TP-04 验证、误报修复和 closeout
  TP-04.01 修复 0092 secret scan 文档误报
  TP-04.02 运行 focused regression、ruff、secret scan 和 local-ci quick
  TP-04.03 回填任务包与路线图状态
```

## Requirement Alignment
- 用户要求：按 0092 之后的 100% 测算基础设施计划继续执行本地可落地任务，优先补基础设施交付面缺口。
- 0092 路线图：0093 是首个本地可执行切片，目标是 CLI capability command baseline。
- 胶水原则：复用既有 `fate_core.cli::_run_capability_execute`、`CapabilityExecutor` 和 provider registry；新增代码只做入口、smoke、契约和门禁接线。
- 非声明边界：CLI 仍是 `partial` delivery surface，只证明 JSON capability 命令可执行，不证明 Markdown 同源或外部 live。

## Task Package Overview
| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | CLI capability executor 链路复核 | Done | `domains/fate-analysis/services/fate-core/src/fate_core/cli.py` |
| TP-01.02 | planned 拒绝策略复核 | Done | `tests/regression/test_fate_core_cli.py` |
| TP-02.01 | 根级 capability CLI wrapper | Done | `bash scripts/capability-cli.sh <capability_id>` |
| TP-02.02 | capability CLI smoke | Done | `bash scripts/capability-cli-smoke.sh --output-json /tmp/fatecat-capability-cli-smoke-0093.json` |
| TP-03.01 | Delivery contract / registry | Done | `contracts/fate/delivery/cli-capability-command.json`、`registry.json` |
| TP-03.02 | local-ci 接线 | Done | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0093` |
| TP-03.03 | 文档与 regression test | Done | `tests/regression/test_capability_cli_smoke.py` |
| TP-04.01 | secret scan 误报修复 | Done | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0093.json` |
| TP-04.02 | 验证 | Done | focused pytest、ruff、local-ci quick |
| TP-04.03 | closeout 文档 | Done | 当前任务包无占位符，INDEX/roadmap 同步 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
