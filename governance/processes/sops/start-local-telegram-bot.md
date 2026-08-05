---
id: SOP-DEV-LOCAL-TELEGRAM-BOT
type: process
status: current
owner: experience-delivery
route_key: start_local_telegram_bot
route_aliases: ["启动本地 Telegram Bot", "运行 Bot polling", "Bot dry-run"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 启动本地 Telegram Bot

## 任务定义
以本地 polling 或 dry-run 方式启动 Telegram delivery surface，复用统一报告计算和 renderer。

## 当前状态
Bot 代码和 dry-run smoke 成熟；真实 live 依赖 `FATE_BOT_TOKEN` 和 Telegram 网络。

## 适用场景
Bot 本地开发、消息流程 smoke 或真实 token 下的 polling 验证；不用于 HF Space webhook。

## 输入要求
真实运行需环境变量 `FATE_BOT_TOKEN`；可选 admin/proxy/dry-run 和限流参数。

## 前置条件
bootstrap 完成；token 存于 ignored env/secret store；确认没有另一 polling/webhook consumer 占用同一 Bot。

## 默认工具链
dry-run `FATE_BOT_DRY_RUN=1 bash scripts/delivery-smoke.sh --target bot --startup-timeout 8`；真实运行 `bash scripts/serve-bot.sh`。

## 固定路径
`domains/experience-delivery/services/fatecat-delivery/src/bot.py`、`rate_limiter.py`、local env example。

## 成熟参数
max concurrent 1、queue size 20、cooldown 0、daily limit 0；这些值可显式收紧，不得无界放大。

## 分步执行流程
1. 检查 token 只存在环境。
2. 确认 Telegram webhook 已清除或不与 polling 冲突。
3. 先跑 Bot dry-run smoke。
4. 授权后启动真实 polling并验证 `/start` 和一份匿名报告。
5. 停止进程并记录脱敏结果。

## 幂等与增量策略
同一 bot token 只允许一个 polling consumer；重启前停止旧 PID；消息任务使用已有幂等/队列语义。

## 限速与并发规则
默认并发 1、队列 20；遵守 Telegram rate limits；不并发启动多个实例。

## 输出目录
日志 `/tmp/fatecat-bot-<UTC>.log`；不得保存聊天正文到 tracked 目录。

## 命名规范
运行记录使用 bot ID hash，不使用 token 或用户名。

## 质量验收门禁
Bot dry-run、rate limiter tests、multi-surface parity；live 声明还需 `bash scripts/live-bot-smoke.sh`。

## 失败处理
token 缺失、401、409 consumer 冲突、网络或队列满时显式失败并停止。

## 恢复与重试策略
网络瞬时失败由 Bot SDK 有界处理；401 不重试，409 先清理冲突 consumer。

## 安全边界
token 不进入日志/命令/Git；Bot 不拥有独立算法；用户报告不作为训练数据。

## 临时文件清理
停止 Bot PID，删除临时日志和测试 update；必要时在授权下清除 webhook。

## 运行记录登记
记录 commit、bot ID hash、模式、PID、smoke/live 状态、错误码和停止时间。

## 明确禁止事项
- 禁止同时 polling 和 webhook。
- 禁止输出 token。
- 禁止 Bot 自行拼接或修改报告。
