# FateCat Skill 命令参考

## 仓库内运行

### 标准预检（推荐默认入口）

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

### 标准预检并生成烟雾样例

```bash
bash scripts/preflight.sh \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file output/preflight-sample.json \
  --pretty
```

### 仓库总验收

```bash
bash scripts/acceptance.sh --with-dev
bash scripts/acceptance.sh --with-dev --with-mingli-bench
```

默认会执行 strict skill 校验、纯分析 smoke、vendor health、源仓卫生门禁、隐私示例门禁、全量 pytest、ruff、format、`fate_core` mypy、API 与 Bot dry-run delivery smoke、导出包卫生检查，以及导出后的 lite skill 包独立 smoke。追加 `--with-mingli-bench` 时会覆盖 MingLi-Bench 统计、prompt 生成和离线答案评分 smoke。只在明确需要缩短本地循环时使用 `--delivery-target api|bot`、`--skip-delivery` 或 `--skip-export`。

### 本地 CI/CD profile

```bash
bash scripts/local-ci.sh --profile quick
bash scripts/local-ci.sh --profile full
bash scripts/local-ci.sh --profile container
bash scripts/local-ci.sh --profile public-service
```

`local-ci.sh` 是本地流水线入口，不调用 GitHub Actions，也不 watch 远端 Acceptance。`quick` 用于日常快速门禁，`full` 复用本地完整验收，`container` 做真实 Docker 容器 smoke，`public-service` 做公网服务静态准入；需要一次跑完时使用 `--profile all`。

### 初始化生命周期包

```bash
bash scripts/init-lifecycle-pack.sh --name first-delivery
```

### 查看生命周期包状态

```bash
bash scripts/lifecycle-status.sh
```

### 安装

```bash
bash scripts/bootstrap.sh
```

### 纯分析健康检查

```bash
bash scripts/health.sh --mode pure --json
```

### 交付层健康检查

```bash
bash scripts/health.sh --mode delivery --json
```

### 纯分析

```bash
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --output-file output/bazi-result.json \
  --pretty
```

### 启动 API

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/serve-api.sh
```

API 启动后可访问原生 HTML Web 报告页：

```text
http://127.0.0.1:8001/web
```

交付层运行探针：

```text
GET /health   # 进程健康
GET /live     # liveness
GET /ready    # 数据库/能力注册表 readiness
GET /metrics  # Prometheus text 指标
```

最小指标检查：

```bash
curl -fsS http://127.0.0.1:8001/metrics | rg 'fatecat_request_latency_seconds|fatecat_request_errors_total|fatecat_bot_queue_size|fatecat_bot_queue_scope_info'
```

`/metrics` 至少应暴露 HTTP 请求量、延迟 histogram、错误分类、inflight 请求、Bot 队列 gauge 和队列 scope；告警与 SLO 口径见 `references/ops-pack.md`。

### Docker 容器构建与 smoke

```bash
bash scripts/container-build.sh --image fatecat-delivery:local
bash scripts/container-smoke.sh --image fatecat-delivery:local --skip-build
```

也可以使用 Compose：

```bash
FATECAT_HOST_PORT=8001 docker compose up --build delivery
```

### Docker 容器发布

Principle gate evidence：target end state 是容器 smoke 只证明镜像自托管可启动；real constraints 是公网 live 需要真实 URL/TLS/Bot token；inertia constraints 是本地容器通过不能替代托管公网验收；kill list 是把 dry-run 说成 live PASS；proof point 是 `container-smoke.sh` 与 `production-readiness.sh` 分开；falsifier 是缺真实输入却宣称公网通过；migration slice 是先本地镜像，再外部 live gate。

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u <user> --password-stdin
bash scripts/container-release.sh \
  --image ghcr.io/tradecatlabs/fatecat-delivery \
  --tag "$(git rev-parse --short=12 HEAD)" \
  --push
```

说明：容器发布前会先运行临时容器 smoke，覆盖 `/health`、`/ready` 与 `/api/v1/bazi/pure-analysis`。公网生产仍需继续执行 `production-readiness.sh --api-url <url>`。

### 无状态公共服务配置

如果用户独立部署单实例，只提供公开排盘/报告能力且不保存用户记录，推荐：

```bash
FATE_RECORDS_ENABLED=0
FATE_CORS_ALLOW_ORIGINS=https://your-domain.example
FATE_MAX_REQUEST_BYTES=1048576
FATE_REQUEST_TIMEOUT_SECONDS=30
FATE_MAX_INFLIGHT_CALCULATIONS=2
FATE_RATE_LIMIT_PER_MINUTE=120
FATE_DEPLOYMENT_REPLICAS=1
FATE_RATE_LIMIT_BACKEND=memory
FATE_EDGE_BODY_LIMIT_ENABLED=
FATE_TRUST_PROXY_HEADERS=
FATE_ENABLE_HSTS=
```

启用记录接口时，必须配置 `FATE_API_ADMIN_TOKEN` 或 `FATE_API_USER_TOKENS`，并补持久化数据库、备份、删除和数据保留策略。

托管公网、多副本或反向代理部署时，再把 `FATE_RATE_LIMIT_BACKEND` 改为 `gateway`、`redis`、`waf` 或 `external`，并按真实代理/TLS 配置打开 `FATE_EDGE_BODY_LIMIT_ENABLED`、`FATE_TRUST_PROXY_HEADERS` 和 `FATE_ENABLE_HSTS`。

生产等价静态验收必须同时满足：

- `FATE_CORS_ALLOW_ORIGINS` 使用真实 HTTPS origin，禁止为空或 `*`。
- `FATE_RECORDS_ENABLED=0` 表示无状态公共排盘服务；如果设为 `1`，必须配置真实 API token。
- `FATE_DEPLOYMENT_REPLICAS>1` 时，`FATE_RATE_LIMIT_BACKEND` 必须是 `gateway`、`redis`、`waf` 或 `external`，不能使用单进程 `memory`。
- `FATE_EDGE_BODY_LIMIT_ENABLED=1` 只表示反向代理/CDN 层 body limit 已配置，不能替代真实网关配置。
- `FATE_TRUST_PROXY_HEADERS=1` 只能在服务直连端口被可信代理隔离时启用。
- `FATE_ENABLE_HSTS=1` 只在 HTTPS 生产域名确认后启用。

### 启动 Bot

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target bot --startup-timeout 8
bash scripts/serve-bot.sh
```

说明：Bot smoke 走 dry-run，不依赖真实 Telegram 连接。

### 真实 Bot 验收

```bash
FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh
```

说明：真实验收会连接 Telegram Bot API；无真实 token 时不得宣称线上通过。

### 生产就绪门禁

```bash
bash scripts/production-readiness.sh --api-url https://your-domain.example --require-live-bot
```

说明：该门禁要求 CORS allowlist、请求体上限、超时、限流、记录接口 token 或无状态模式，并可验证线上 `/health`、`/ready`、`/metrics` 与真实 Telegram Bot API。缺少真实外部环境时，不得宣称生产 live 验收通过。

### Vendor 快照健康检查

```bash
bash scripts/clean-runtime.sh
bash scripts/vendor-health.sh
python3 -m pytest -q tests/regression/test_fate_policy_assets.py
```

说明：先清理本机运行态污染，再校验 `vendor_sources.json` 覆盖所有 `tools/reference-repos/github/*` 快照、hash、license 边界和生产准入。

### 源仓卫生检查

```bash
bash scripts/check-source-hygiene.sh
```

说明：检查 raw 大资料、运行态、缓存、数据库、日志和本机个人绝对路径是否误入 Git。

### 清理本地缓存

```bash
bash scripts/clean-runtime.sh
```

### 导出包卫生检查

```bash
bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite
bash scripts/check-export-hygiene.sh /tmp/export-lite/fatecat
```

### 采集 agent 运维包

```bash
bash scripts/collect-ops-bundle.sh --output /tmp/fatecat-ops-bundle
```

## 导出独立 bundle

```bash
bash scripts/export-runtime.sh --output-parent /tmp/export-full --mode full
```

## 导出轻量 bundle

```bash
bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite
```

导出后的目录再执行：

```bash
bash scripts/check-export-hygiene.sh /tmp/export-lite/fatecat
bash scripts/bootstrap.sh
bash scripts/preflight.sh --mode pure --bootstrap --pretty
/home/lenovo/.codex/skills/auto-skill/scripts/validate-skill.sh /tmp/export-lite/fatecat --strict
```
