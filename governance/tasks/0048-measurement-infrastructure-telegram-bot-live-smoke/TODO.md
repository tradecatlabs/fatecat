# Execution Checklist

[x] TP-01.01 | P0 | 复核脚本、门禁和环境 token 状态 | Verify: env set/unset check and script inspection | Gate: 不输出 secret 内容 | Parallelizable: No
[ ] TP-02.01 | P0 | 运行真实 Telegram Bot live smoke | Verify: `FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh` | Gate: Telegram `get_me()` 成功，且 token 非 placeholder | Parallelizable: No
[x] TP-03.01 | P0 | 落盘 blocked 证据并校验任务包 | Verify: task docs validation and git diff check | Gate: 缺 token 时任务保持 Blocked，不写 Done | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
