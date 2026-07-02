# Planning Summary
本任务处理 `MI-NEXT-01 Telegram Bot live smoke`。正确完成状态是：使用真实 `FATE_BOT_TOKEN` 成功调用 Telegram Bot API `get_me()`，并把 live release gate 的 `evidence.telegram_bot_live` 推进为 pass。当前环境没有 token，因此本轮只能完成前置复核、失败验证和可审计 blocked 落盘。

# Lifecycle Gates
禁止跳过任何 gate；不得把缺 token 的失败写成生产 live 通过。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Bot live 验收目标和 secret 边界明确 | Done |
| PLAN | 环境 token 状态、脚本和 release gate 逻辑已复核 | Done |
| BUILD | 不改业务代码；只落盘任务包、索引和路线图 blocked 证据 | Done |
| TEST | `scripts/live-bot-smoke.sh` 已真实执行并返回缺 token；任务文档校验通过 | Done |
| REVIEW | 失败原因确认是缺真实 `FATE_BOT_TOKEN` | Done |
| SHIP | blocked 任务包可提交、可复核 | Done |

# Simplest Path
不改代码，不新建 fake secret，不绕过 Telegram API。直接执行现有 `scripts/live-bot-smoke.sh`，以命令真实退出码作为证据。

# Split Strategy
- TP-01：读取脚本、门禁和环境 token 状态。
- TP-02：运行真实 Bot smoke。
- TP-03：记录 blocked 状态和解除条件。

# Execution Waves
| Wave | Nodes | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01 | 复核脚本、门禁、token 状态 | Done |
| 2 | TP-02.01 | 运行 live-bot-smoke | Blocked |
| 3 | TP-03.01 | 落盘阻断证据 | Done |

# Next Executable Leaves
None inside this task until external `FATE_BOT_TOKEN` is provided.

# Future-Optimal Contract
Target end state: Bot live smoke 是真实 Telegram API 连通证据，而不是 dry-run、placeholder token 或本地初始化 smoke。

Real constraints: `FATE_BOT_TOKEN` 是外部 secret，当前环境未提供；不能输出或提交 secret。

Inertia constraints: 旧 dry-run Bot smoke、delivery smoke 或 placeholder token 不能作为 live 证据。

Kill list: fake token、placeholder token、只跑 delivery-smoke 就写 live pass、把 pending 写成完成。

Proof point: `bash scripts/live-bot-smoke.sh` 返回缺少真实 token，STATUS 记录 blocked。

Falsifier: 如果提供真实 token 后脚本仍失败，则需要进入网络/API/token 权限调试，而不是继续归因于缺 secret。

Migration slice: 本轮只记录 blocked；后续提供 token 后重跑同一脚本并刷新状态。

Rejected short-term patches: 不修改脚本放宽 token 校验；不 mock Telegram Bot API；不把 `TELEGRAM_BOT_TOKEN` 私自映射为通过。

# Ponytail Contract
Existence check: `MI-NEXT-01` 是 live release gate 明确 pending 项，必须有任务包记录执行证据和外部阻断。

Selected ladder rung: 任务文档和命令证据；不新增脚本或抽象。

Skipped scope: Telegram token 管理、GitHub secret 配置、Bot 业务改造、registry attestation。

Ceiling / upgrade path: 提供真实 `FATE_BOT_TOKEN` 后，把本任务从 Blocked 推进为 Done，并继续生成 live release gate evidence。

Do-not-simplify: 不能移除真实 Telegram API 连通要求。

Minimal runnable check: `bash scripts/live-bot-smoke.sh`。

# Runtime Workflow Contract
- risk_level: medium
- affected_flows: release evidence, Telegram Bot delivery surface
- state_changes: task docs and roadmap only
- side_effects: one failed smoke command due missing token
- rollback: revert task 0048 docs/index/roadmap updates
- required_tests: task docs validation, git diff check, optional tasks tree validation

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01
```

# Rollback Protocol
- 恢复 `governance/tasks/INDEX.md` 的 0048 行。
- 恢复路线图中 MI-NEXT-01 的任务状态说明。
- 删除本任务目录新增文件。
