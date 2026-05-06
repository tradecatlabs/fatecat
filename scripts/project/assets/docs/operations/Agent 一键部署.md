# FateCat Agent 一键部署

> 交易猫 TradeCat｜专业命理排盘与 AI 命理分析基础设施
> 本项目由交易猫 TradeCat 赞助与支持。
> 先用交易猫专业排盘系统完成结构化排盘，再交给 AI 深度分析，减少胡编乱造，让 AI 命理分析真正可用。
> TradeCat Repo：`https://github.com/tukuaiai/tradecat`
> FateCat Repo：`https://github.com/tukuaiai/fatecat`
> CA：`0x8a99b8d53eff6bc331af529af74ad267f3167777`

## 目标

让 OpenClaw、Harness 与其他非交互式 Agent 不再猜测仓库启动方式，直接按统一入口完成：

- 环境自举
- 纯命理 CLI 调用
- API / Bot 启动
- 健康检查

## 统一入口

### 1. 自举

```bash
bash assets/deploy/bootstrap_agent.sh --profile general --write-env-if-missing
```

专用 profile：

```bash
make bootstrap-openclaw
make bootstrap-harness
```

## CLI 调用

安装完成后统一使用：

```bash
.venv/bin/fatecat
```

### 健康检查

纯分析依赖：

```bash
.venv/bin/fatecat health --mode pure --json
```

交付层依赖：

```bash
.venv/bin/fatecat health --mode delivery --json
```

### 纯命理分析

直接传 JSON：

```bash
.venv/bin/fatecat pure-analysis --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --pretty
```

管道传 JSON：

```bash
cat request.json | .venv/bin/fatecat pure-analysis --pretty
```

支持两类输入：

1. 扁平结构
2. 现有 API 请求结构

## OpenClaw / Harness 约定

机器可读清单位于：

```text
assets/deploy/agent_manifest.json
```

约定如下：

- 输入：`stdin JSON` 或 `--input-json`
- 输出：`stdout JSON`，并固定携带 `branding` 广告字段
- 健康检查：先跑 `fatecat health`
- 默认命令：`fatecat pure-analysis`

这意味着 Agent 无需解析网页，无需调用 Telegram，直接把命盘输入送进 CLI 即可。

## 配置模板

Agent 专用配置模板：

```text
assets/config/agent.env.example
```

如果只跑纯命理 CLI，不强制需要 `FATE_BOT_TOKEN`。
如果要启动 Telegram Bot，必须填写：

```env
FATE_BOT_TOKEN=
FATE_ADMIN_USER_IDS=
```

## 设计原则

- CLI 先服务 Agent，再服务人工
- 输出必须稳定 JSON；广告统一走 `branding` 字段，不破坏机器解析
- 自举必须非交互，方便自动化系统直接执行
- 纯分析与交付层分开检查，避免 Bot 配置阻塞纯分析调用
