# Task-Level Acceptance
本任务的真实完成条件是 Telegram Bot live smoke 通过。当前没有真实 `FATE_BOT_TOKEN`，因此任务状态必须保持 Blocked，直到外部 secret 提供。

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Token presence check | safe env status check | set/unset only, no token value |
| Bot live smoke | `FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh` | `live bot smoke ok` |
| Task docs validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0048-measurement-infrastructure-telegram-bot-live-smoke --phase decompose` | success |
| Task tree validation | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | success |

# Review Gate
- 不得输出真实 token。
- 不得使用 placeholder/smoke token。
- 不得把 `delivery-smoke.sh --target bot` 当作 live smoke。
- 不得把缺 token 的失败写成通过。

# Runtime Verification Gate
- `scripts/live-bot-smoke.sh` 必须真实连接 Telegram Bot API。
- 成功证据必须来自 `get_me()` 成功输出。
- 当前失败证据只证明缺 token，不证明 Bot 代码错误。

# Ship Readiness
- 0048 任务包记录 blocked 状态。
- 路线图和任务索引同步 MI-NEXT-01 状态。
- 本地文档校验通过。

# Task Package Acceptance
- TP-01.01 Done：脚本、门禁和 token 状态已复核。
- TP-02.01 Blocked：缺真实 `FATE_BOT_TOKEN`。
- TP-03.01 Pending：校验和提交后完成 blocked 记录。

# Anti-Goals
- 不创建 Bot token。
- 不配置 GitHub secret。
- 不修改 Bot 业务代码。
- 不绕过 Telegram API。

# Evidence Boundary
- 可以写：当前环境缺少真实 `FATE_BOT_TOKEN`，Bot live smoke blocked。
- 不可以写：Telegram Bot live 已通过。
