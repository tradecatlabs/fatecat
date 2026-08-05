---
id: SOP-OPS-TELEGRAM-WEBHOOK
type: process
status: current
owner: experience-delivery
route_key: configure_telegram_webhook
route_aliases: ["配置 Telegram webhook", "部署 HF Bot webhook", "检查 getWebhookInfo"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 配置 Telegram Webhook

## 任务定义
在同一个 FastAPI delivery 进程中启用 Telegram webhook surface，由服务启动时注册 webhook 并使用 secret-token 校验 Update。

## 当前状态
实现和 HF 部署口径可用；真实可用性依赖 Bot token、HTTPS 域名、Telegram 和常驻性。

## 适用场景
HF Space 或其他 HTTPS 部署启用 Telegram；不用于本地 polling。

## 输入要求
Secret `FATE_BOT_TOKEN`、`FATE_TELEGRAM_WEBHOOK_SECRET`；Variable `FATE_TELEGRAM_WEBHOOK_ENABLED=1`；可选 HTTPS `FATE_TELEGRAM_WEBHOOK_URL`。

## 前置条件
公开 delivery 已部署；路径固定 `/api/v1/integrations/telegram/webhook`；没有 polling consumer；secret 32-256 位允许字符。

## 默认工具链
由 delivery startup 调用 Telegram `setWebhook`；验证使用 `bash scripts/live-bot-smoke.sh`、`/ready` 和 `/metrics`。

## 固定路径
Delivery webhook route、HF Space secrets/variables、`docs/deployment/huggingface-space.md`。

## 成熟参数
默认 URL 由 `SPACE_HOST` 推导；队列 20、worker 1；退避 30 秒起、最大 900 秒、20% jitter；队列满返回 503。

## 分步执行流程
1. 在 secret store 配置 token和 webhook secret。
2. 设置 enabled variable，必要时设置固定 HTTPS URL。
3. 重启/部署 service，等待 startup 注册。
4. 检查 `/ready` 的 telegram surface 和 metrics。
5. 执行 live Bot smoke并发送匿名测试 update。

## 幂等与增量策略
相同 URL/secret 的 setWebhook 可重复；变更 URL/secret 后重新部署；update_id 在进程内去重。

## 限速与并发规则
Update 入有界内存队列；不阻塞 HTTP 等待完整报告；遵守 Telegram rate limit；免费 Space 保持 worker 1。

## 输出目录
无业务持久输出；脱敏部署证据写 `infra/runtime/local-state/exports/telegram-webhook/`。

## 命名规范
证据 `telegram-webhook-<deployment>-<short-sha>-<UTC>.json`；只记录 bot ID/hash。

## 质量验收门禁
setWebhook 成功、secret header 拒绝负例、ready/metrics、queue 503、duplicate update和 live-bot smoke。

## 失败处理
401、secret mismatch、URL 非 HTTPS、ready degraded 或 Telegram 不可达时保持 Web/API 可用但渠道 not_ready。

## 恢复与重试策略
服务按有界指数退避重注册；401/配置错误不盲重试；修正 secret/URL 后重启。

## 安全边界
token/secret 仅存平台 Secrets；Update 和报告不写 Git；公网 endpoint 必须验证 secret-token。

## 临时文件清理
删除测试 update/日志；切换回 polling 前由授权 operator 清除 webhook。

## 运行记录登记
记录 deployment、bot ID hash、URL host、ready/metrics、live smoke、退避和最后成功时间。

## 明确禁止事项
- 禁止同一 Bot 同时 polling 和 webhook。
- 禁止把 token 放 Variables/README/日志。
- 禁止把免费 Space 休眠环境声明为持续在线生产 Bot。
