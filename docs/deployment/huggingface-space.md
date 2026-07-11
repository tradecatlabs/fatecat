# Hugging Face Space 自助部署

这份文档说明普通用户如何把 FateCat 部署到自己的 Hugging Face Space，并通过云端 `/web` 工作台使用 Markdown 报告生成功能。目标是免费、公开、可复制，不要求用户在本机长期运行服务。

## 推荐路径

| 场景 | 路径 | 是否需要本机命令 | 是否自动跟随 GitHub 更新 |
|------|------|------------------|---------------------------|
| 只想马上有一个自己的在线网页 | Duplicate Space | 否 | 否 |
| 想 fork 后持续更新自己的 Space | GitHub Actions 手动部署 | 否 | 手动点 Run workflow |
| 开发者自己维护发布 | hf CLI | 是 | 由本地命令控制 |

## 路径 A：HF 网页一键复制

这是最简单的用户自部署方式。

1. 登录 Hugging Face。
2. 打开 `https://huggingface.co/spaces/tradecatlabs/fatecat`。
3. 点击页面右上角三个点。
4. 选择 `Duplicate this Space`。
5. 选择自己的 Owner、Space name、Visibility 和 Hardware。
6. 免费部署选择 `CPU Basic`。
7. 等待 Space build 完成。
8. 打开 `https://<你的用户名>-<space-name>.hf.space/web`。

这个方式不需要 GitHub、不需要本机命令，也不会把用户输入写回 FateCat 仓库。

用户侧使用流程：

1. 打开自己的 `/web`。
2. 填写出生日期、出生时间、出生地区、性别和输出体系。
3. 点击 `生成 Markdown 报告`。
4. 复制页面里的 Markdown 输出。
5. 打开项目归属块中的 `免费 AI 分析入口（Gemini Gem）`，自行粘贴 Markdown 分析。

FateCat 不会自动把输入或报告发送给 Gemini；Gemini 分析只发生在用户主动打开外部页面并粘贴内容之后。

限制：

- 后续项目更新不会自动同步到你的副本。
- 免费硬件会休眠，第一次访问可能要等它冷启动。
- 免费硬件默认只适合轻量公开使用，不是高并发生产服务。

## 路径 B：GitHub + HF 云端自部署

这个路径适合用户 fork GitHub 仓库，然后在 GitHub 网页里一键部署到自己的 HF Space。

### 1. 准备 HF token

1. 打开 `https://huggingface.co/settings/tokens`。
2. 创建一个有 Space 写入权限的 token。
3. 复制 token。

不要把 token 写进代码、README、issue、日志或聊天记录。

### 2. Fork GitHub 仓库

1. 打开 `https://github.com/tradecatlabs/fatecat`。
2. 点击 `Fork`。
3. 进入自己的 fork 仓库。

### 3. 设置 GitHub Secret

在自己的 fork 仓库页面：

1. 进入 `Settings`。
2. 进入 `Secrets and variables` -> `Actions`。
3. 新增 Repository secret：
   - Name：`HF_TOKEN`
   - Value：刚才创建的 Hugging Face token

### 4. 从 GitHub 网页部署

1. 进入 fork 仓库的 `Actions` 页面。
2. 选择 `Deploy Hugging Face Space`。
3. 点击 `Run workflow`。
4. 填写：
   - `space_id`：`你的HF用户名/fatecat`
   - `visibility`：`public` 或 `private`
   - `prune_remote`：通常保持 `true`
5. 点击绿色 `Run workflow` 按钮。

Workflow 会在 GitHub runner 中：

1. 检出仓库。
2. 安装 `hf` CLI。
3. 用 `scripts/hf-space-deploy.sh` 生成 Hugging Face Space 分发包。
4. 创建或更新你的 HF Space。
5. 上传 Docker Space 所需文件。

这里不是把整个企业 monorepo 原样同步到 HF，而是生成一个最小可运行 Space bundle。原因是 HF Space 的根目录需要 `README.md` front matter 和 `Dockerfile`，直接同步整仓会把 Space 根目录弄错。

部署完成后访问：

```text
https://<你的HF用户名>-fatecat.hf.space/web
```

如果 Space 名字不是 `fatecat`，URL 中最后一段改成你的 Space 名字。

该 workflow 只通过 `workflow_dispatch` 手动触发。Fork 用户需要发布时自己点 `Run workflow`；push 不会自动部署，也不会自动跑 FateCat Acceptance。

## 路径 C：本地 hf CLI 部署

开发者可以直接在本机部署：

```bash
hf auth login
bash scripts/hf-space-deploy.sh --space <你的HF用户名>/fatecat --allow-auth-mismatch
```

只生成分发包、不上传：

```bash
bash scripts/hf-space-deploy.sh --dry-run --bundle-dir /tmp/fatecat-hf-space
```

## 免费版运行口径

FateCat 的 HF 免费 Space 默认配置：

```text
FATE_RECORDS_ENABLED=0
FATE_SERVICE_PORT=7860
FATE_MAX_INFLIGHT_CALCULATIONS=1
FATE_REPORT_JOB_QUEUE_SIZE=20
FATE_REPORT_JOB_WORKERS=1
FATE_REPORT_JOB_TTL_SECONDS=1800
FATE_REPORT_JOB_MAX_ATTEMPTS=1
FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS=0
FATE_REPORT_JOB_RETRY_BACKOFF_SECONDS=0
FATE_WEBHOOK_MAX_ATTEMPTS=1
FATE_WEBHOOK_RETRY_BACKOFF_SECONDS=0
FATE_TELEGRAM_WEBHOOK_ENABLED=0
```

含义：

- 不保存用户报告记录到数据库。
- Web 提交会进入进程内有界队列。
- 默认 1 个 worker 生成报告。
- 默认 report job 不重试、不启用 attempt timeout；默认 webhook callback 不重试。免费 Space 上不要把 timeout 当成可强杀底层计算的生产隔离能力，也不要把本地 callback retry 当成持久 outbox。
- 最多 20 个等待任务。
- 结果默认 30 分钟后过期。
- Space 重启后队列和结果都会消失。

## 同一 Space 启用 Telegram Webhook

Telegram 作为独立 DeliverySurface 复用同一个 FastAPI 进程，不要把 Docker CMD 改成
`start.py both`。在 Space `Settings -> Secrets` 添加：

```text
FATE_BOT_TOKEN=<BotFather token>
FATE_TELEGRAM_WEBHOOK_SECRET=<32-256 位字母、数字、下划线或连字符>
```

在 `Settings -> Variables` 添加：

```text
FATE_TELEGRAM_WEBHOOK_ENABLED=1
```

默认 Webhook URL 会根据 HF 注入的 `SPACE_HOST` 生成：

```text
https://<space-host>/api/v1/integrations/telegram/webhook
```

如需覆盖，可设置 `FATE_TELEGRAM_WEBHOOK_URL`，但必须是 HTTPS 且路径保持不变。启动时服务会调用
Telegram `setWebhook`，使用 `X-Telegram-Bot-Api-Secret-Token` 验证请求，再把 Update 放入有界内存队列并
立即返回。队列满时返回 `503` 让 Telegram 重试；重复 `update_id` 在当前进程内去重。

验证：

```bash
bash scripts/live-bot-smoke.sh
curl -fsS https://<space-host>/ready
curl -fsS https://<space-host>/metrics | grep fatecat_telegram_webhook
```

免费 Space 默认会休眠；冷启动期间 Telegram 可能重试。Space 重启后 ConversationHandler、Update 队列和
去重窗口都会丢失，因此这里只适合演示和轻量使用。需要持续在线和持久会话时，应迁移到付费常驻实例并接入
Redis/Postgres。

## 隐私与公开性

免费公开 Space 适合演示和轻量自用，但不要输入敏感身份信息。

- Public Space 的源码公开。
- 免费 Space 运行在 Hugging Face 托管环境。
- 用户输入会在当前请求、内存任务队列和生成页面中短暂存在。
- 默认不写 FateCat 数据库，也不提交进 Git 仓库。
- 报告任务结果只在进程内保留到 TTL 到期；Space 重启后会消失。
- FateCat 不会自动把排盘输入或报告发送给 Gemini。
- Hugging Face 平台仍可能保留构建日志、运行日志和访问元数据。

建议：

- 姓名使用昵称或留空。
- 不要输入身份证、手机号、详细住址、真实账号 token。
- 如果需要私有访问，把 Space visibility 设为 private。

## 并发与升级

免费 HF `CPU Basic` 适合网页可用和轻量分享，不适合承诺高并发。

当前免费版通过异步任务队列解决的是：

- 浏览器请求不再长时间阻塞。
- 多个用户可以排队。
- 任务满时明确返回队列已满，而不是静默卡死。

如果要更强并发：

1. 增大 `FATE_REPORT_JOB_WORKERS` 和 `FATE_REPORT_JOB_QUEUE_SIZE`。
2. 升级 HF Space 硬件。
3. 自部署 Redis/RQ、Celery、Dramatiq 或云任务队列，把进程内队列替换成外部持久队列。
4. 多副本部署时必须使用外部队列，否则每个副本都有自己的内存队列，任务状态不会共享。

## 故障排查

| 现象 | 处理 |
|------|------|
| Build failed | 打开 Space `Logs`，优先看 Docker build 阶段错误 |
| 页面长时间冷启动 | 免费 Space 休眠后的正常现象，等待或在 Settings 里手动 Restart |
| 点击生成后提示队列满 | 稍后重试，或提高 `FATE_REPORT_JOB_QUEUE_SIZE` |
| 任务提交后结果消失 | 结果 TTL 到期或 Space 重启；重新提交即可 |
| 任务因 timeout 失败 | 检查 `FATE_REPORT_JOB_ATTEMPT_TIMEOUT_SECONDS` 是否设置过低；默认 `0` 表示关闭 |
| GitHub Action 报 HF_TOKEN 缺失 | 检查 fork 仓库 `Settings -> Secrets and variables -> Actions` 是否设置 `HF_TOKEN` |
| Space 创建到错误账号 | 检查 workflow 的 `space_id` 是否为 `你的HF用户名/space名` |

## 维护者发布前检查

维护者更新官方 Space 前，先在本地执行：

```bash
bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space
```

这个命令会检查：

- 本地 quick CI。
- GitHub Acceptance / Container workflow 仍为手动触发。
- HF 免费 Space 默认 `FATE_RECORDS_ENABLED=0`。
- README、HF README 和部署文档的免费部署与隐私口径保持同步。
- 本地 delivery smoke。
- 线上 `/health`、`/ready`、`/metrics`。

## 官方资料

- Hugging Face Spaces Overview: `https://huggingface.co/docs/hub/spaces-overview`
- Hugging Face Spaces GitHub Actions: `https://huggingface.co/docs/hub/spaces-github-actions`
- Hugging Face Spaces Configuration Reference: `https://huggingface.co/docs/hub/spaces-config-reference`
