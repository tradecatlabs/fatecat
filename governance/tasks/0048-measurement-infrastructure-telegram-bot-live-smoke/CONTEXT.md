# Repo Evidence
- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`。
- 当前提交：`d54499a`。
- 当前 worktree：任务开始时 clean。
- 上一任务：0047 已刷新 post-0046 基础设施计划并推送；Acceptance/Container 对 `d54499a` 均通过。
- 本任务对应路线图项：`MI-NEXT-01 Telegram Bot live smoke`。

# Current Bot Live Contract
- 真实 Bot 验收入口：`FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh`。
- 脚本行为：调用 Telegram Bot API `get_me()`，拒绝 placeholder/smoke token。
- 生产就绪入口：`bash scripts/production-readiness.sh --api-url <real-url> --require-live-bot`。
- Release gate 入口：`bash scripts/live-release-gate.sh --run-live-bot ...`。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不能泄露 token | 只记录 set/unset 和脚本结果，不输出 secret 值 |
| 不能伪造 live smoke | 缺 token 时记录 blocked，不写 pass |
| 必须按 MI-NEXT 顺序推进 | 先处理 MI-NEXT-01，再继续后续任务 |
| 外部账号凭证不在仓库内 | 解除条件必须是外部提供真实 `FATE_BOT_TOKEN` |

# Change Boundary
允许修改：

- `governance/tasks/0048-measurement-infrastructure-telegram-bot-live-smoke/*`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

禁止修改：

- Bot 业务源码
- 部署 secret
- `.env` 文件
- GitHub secret / Telegram 外部账号

# Risk Matrix
| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 泄露真实 token | 高 | 不打印、不提交、不读取展示 token 内容 |
| 把缺 token 写成通过 | 高 | STATUS 保持 Blocked，命令失败证据落盘 |
| 使用 placeholder 误验收 | 高 | 依赖脚本内置 placeholder 拒绝逻辑 |
| 因外部阻断停止整体推进 | 中 | 记录 blocked 后继续后续独立任务 |

# Assumptions and Falsification
- 假设：当前环境没有真实 `FATE_BOT_TOKEN`。
- 证伪方式：环境或 `infra/environments/local/.env` 提供真实 token 后，`scripts/live-bot-smoke.sh` 成功输出 `live bot smoke ok`。
- 调试模式: Optional

# Critical Ambiguities
- 是否允许使用哪个 Telegram Bot 账号/token：当前未提供。
- 是否要把 Bot live smoke 纳入 GitHub Actions secret：当前未配置。

# Debug Evidence Contract
Not Required。本任务不是代码 bug 修复；失败原因是外部 secret 缺失。

# Task Package Context Map
- TP-01.01：读取 Bot live 相关脚本、release gate 和环境 token set/unset 状态。
- TP-02.01：运行 `bash scripts/live-bot-smoke.sh`，以真实退出码和错误输出作为证据。
- TP-03.01：把 blocked 状态、解除条件、路线图和任务索引同步落盘。
