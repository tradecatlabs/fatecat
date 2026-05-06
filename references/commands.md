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
```

默认会执行 strict skill 校验、纯分析 smoke、vendor health、全量 pytest、ruff、format、`fate_core` mypy、API 与 Bot dry-run delivery smoke、导出包卫生检查，以及导出后的 lite skill 包独立 smoke。只在明确需要缩短本地循环时使用 `--delivery-target api|bot`、`--skip-delivery` 或 `--skip-export`。

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

说明：该门禁要求 API 鉴权、CORS allowlist、真实 token 口径，并可验证线上 `/health` 与真实 Telegram Bot API。缺少真实外部环境时，不得宣称生产 live 验收通过。

### Vendor 快照健康检查

```bash
bash scripts/vendor-health.sh
```

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
