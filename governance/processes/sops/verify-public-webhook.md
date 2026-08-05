---
id: SOP-OPS-PUBLIC-WEBHOOK
type: process
status: current
owner: sre
route_key: verify_public_webhook
route_aliases: ["验证公网 webhook", "测试 outbox 投递", "检查 HMAC 回调"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 验证公网 Report Webhook

## 任务定义
使用真实 Postgres 和授权 HTTPS callback 验证报告终态事件、HMAC、allowlist、outbox 状态和可恢复投递。

## 当前状态
live smoke 工具已实现；需要真实 DSN/URL/secret，缺失时只能 blocked summary。

## 适用场景
公网 report webhook 上线、callback/签名/outbox 逻辑变更或生产证据更新。

## 输入要求
环境变量 `FATE_REPORT_JOB_DATABASE_URL`、`FATE_WEBHOOK_LIVE_URL`、`FATE_WEBHOOK_LIVE_SECRET`、`FATE_WEBHOOK_LIVE_ALLOWED_HOSTS`。

## 前置条件
callback endpoint 归操作者控制、HTTPS、可接收测试事件；Postgres smoke 已通过；secret 只在环境中。

## 默认工具链
`bash scripts/postgres-public-webhook-live-smoke.sh --output-json <file>`。

## 固定路径
Webhook contracts、`webhook_callbacks.py`、Postgres outbox store、public webhook live smoke。

## 成熟参数
HTTP timeout 5 秒、等待终态 12 秒、max attempts 1；默认一次性 schema并清理。

## 分步执行流程
1. 验证四个 env 名称已配置但不输出值。
2. 检查 URL HTTPS和 host allowlist。
3. 执行 live smoke。
4. 在 callback 侧核对 event ID、HMAC、timestamp 和脱敏 payload。
5. 检查 outbox succeeded 与数据库 cleanup。

## 幂等与增量策略
事件 ID 唯一；receiver 按 event ID 幂等；重放使用 outbox 原事件，不创建不同 payload 冒充恢复。

## 限速与并发规则
单次 smoke 单事件；不并发冲击 callback；遵守 endpoint 限流。

## 输出目录
`infra/runtime/local-state/exports/webhook-live/<short-sha>/`。

## 命名规范
`public-webhook-live-<short-sha>-<UTC>.json`；URL/secret 只记录 hash/ref。

## 质量验收门禁
HTTPS/allowlist/HMAC、terminal event、outbox persisted succeeded、payload no-leak、cleanup 和 commit 绑定 PASS。

## 失败处理
缺配置、SSRF/allowlist、HTTP、签名、数据库或 outbox 失败即 block；不要把 receiver 2xx 当全链通过。

## 恢复与重试策略
外部瞬时失败在有界策略内重投；修复后使用新 smoke event；不得无限重放。

## 安全边界
callback payload 不含报告正文/用户输入；secret 不输出；只访问 allowlist HTTPS host。

## 临时文件清理
默认 drop schema、删除 callback 测试事件和临时日志；保留脱敏 proof。

## 运行记录登记
记录 commit、DB/endpoint refs、event ID hash、HMAC 验证、outbox status、duration 和 cleanup。

## 明确禁止事项
- 禁止关闭 SSRF/allowlist。
- 禁止输出 callback URL secret。
- 禁止用本地 simulator 代替公网 live。
