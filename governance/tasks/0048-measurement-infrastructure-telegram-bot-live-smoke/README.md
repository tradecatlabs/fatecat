# Task Overview
- Task ID: `0048`
- Slug: `measurement-infrastructure-telegram-bot-live-smoke`
- Objective: `执行 MI-NEXT-01 Telegram Bot live smoke，用真实 FATE_BOT_TOKEN 调用 Telegram get_me()，把 live release gate 中的 telegram_bot_live 从 pending 推进为真实 pass；若缺少真实 token，则只记录阻断证据，不伪造通过。`
- Status: `Blocked`

## In Scope
- 复核 Telegram Bot live smoke 脚本和生产发布门禁对 `FATE_BOT_TOKEN` 的要求。
- 检查当前执行环境是否提供真实 `FATE_BOT_TOKEN`，但不输出 token 内容。
- 执行 `bash scripts/live-bot-smoke.sh`，记录真实结果。
- 把缺 token 的阻断状态、解除条件和后续验收命令落盘。

## Out of Scope
- 不创建或轮换 Telegram Bot token。
- 不读取、打印、提交或泄露任何真实 secret。
- 不用 placeholder/smoke token 替代真实 live 验收。
- 不修改 Bot 业务逻辑、Telegram 交互代码、部署配置或外部账号。

## Task Package Tree
```text
TP-01 Bot live 证据前置复核
  TP-01.01 复核脚本、门禁和环境 token 状态
TP-02 Bot live smoke 执行
  TP-02.01 运行 scripts/live-bot-smoke.sh
TP-03 阻断证据与解除路径
  TP-03.01 记录 blocked 状态、解除条件和后续命令
```

## Requirement Alignment
- 对齐 `MI-NEXT-01 Telegram Bot live smoke`。
- 对齐 `scripts/live-bot-smoke.sh` 的真实 Telegram Bot API `get_me()` 验收口径。
- 对齐 `scripts/live-release-gate.py` 中 `evidence.telegram_bot_live` 的 `--run-live-bot` 真实证据要求。
- 对齐项目安全要求：无真实 token 时只能标记外部连通验证待执行，不得写通过。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 确认 Bot live 验收所需脚本、门禁和 secret 状态。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | No | 检查 `FATE_BOT_TOKEN` 是否存在，读取脚本和门禁逻辑，不输出 token。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 执行真实 Bot live smoke 或得到可信失败。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 运行 `bash scripts/live-bot-smoke.sh`。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.01 | - | No | No | 把阻断状态和解除路径写成可审计证据。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.01 | 3 | No | No | 更新任务状态、索引和路线图，不伪造 live pass。 |

## Reading Order
1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
