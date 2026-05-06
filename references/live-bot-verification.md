# 真实 Bot 验收

## 边界

`delivery-smoke.sh --target bot` 只验证 Bot 进程能用临时 smoke 配置完成初始化，不访问真实 Telegram。

真实线上验收必须使用真实 `FATE_BOT_TOKEN`，并运行：

```bash
FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh
```

完整生产上线前建议使用总门禁：

```bash
bash scripts/production-readiness.sh --api-url https://your-domain.example --require-live-bot
```

脚本会调用 Telegram Bot API `get_me()`。如果 token 缺失、是 placeholder、网络不可达或 Telegram 返回错误，脚本必须失败。

## 验收结果解释

- `live bot smoke ok: id=... username=@...`：真实 token 可用，Bot API 可达。
- `缺少真实 FATE_BOT_TOKEN`：仓库内无法完成真实线上验收，需要部署环境提供 secret。
- `拒绝使用 placeholder/smoke token`：当前只适合 dry-run，不得宣称真实线上通过。

## 不做的事

- 不把真实 token 写入仓库。
- 不用 smoke token 冒充生产验收。
- 不在 acceptance 默认链路里强制真实联网验收。
