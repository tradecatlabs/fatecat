# FateCat Skill 运维包说明

## 目标

把“出问题时临时查命令”改成“平时就能沉淀的 agent 运维包”。

## 当前仓库已经提供什么

- 健康检查入口：`bash scripts/health.sh --mode pure --json`
- 标准验收入口：`bash scripts/acceptance.sh --with-dev`
- 启动入口：`bash scripts/serve-api.sh`、`bash scripts/serve-bot.sh`
- 交付层烟雾入口：`bash scripts/delivery-smoke.sh --target api`、`bash scripts/delivery-smoke.sh --target bot --startup-timeout 8`
- 生命周期状态入口：`bash scripts/lifecycle-status.sh`
- 运维包采集：`bash scripts/collect-ops-bundle.sh --output <dir>`

## 运维包默认内容

- 采集时间与 git 版本
- skill 根和 project 根路径
- FateCat CLI 帮助输出
- 纯分析健康检查结果
- 生命周期状态摘要
- 当前 skill 的入口文档索引

## 可观察性边界

- 当前仓库能提供“进程前”与“进程内”的检查入口。
- 当前仓库不会自动替你接 Prometheus、Grafana、Sentry、systemd、supervisor、k8s 或云告警平台。
- 如果你要真正实现自动救活，需要把这里提供的健康检查与重启命令接到目标环境的守护体系。

## 推荐落地方式

### 本地或单机

- 用 `bootstrap.sh` 保证环境一致
- 用 `preflight.sh` 作为默认巡检入口
- 用 `acceptance.sh --with-dev` 作为发布前验收入口；默认同时验证源码仓库静态门禁、API/Bot 入口和导出后的 lite skill 包
- 用 `collect-ops-bundle.sh` 固化每次发布或事故后的证据

### 服务化交付

- 用 `serve-api.sh` 或 `serve-bot.sh` 作为启动命令
- 在上线前先跑目标入口的 `delivery-smoke.sh`；发布前总验收默认同时覆盖 API 与 Bot dry-run
- 把健康检查接进外部守护器
- 把运维包放进发布记录或事故记录

## 自动救活的最小定义

当前 skill 对“自动救活”的最小支持是：

- 有健康检查入口
- 有确定的启动入口
- 有故障证据采集入口
- 有阶段状态与运维说明

这意味着它已经具备接入自动恢复系统的前提，但不等于仓库已经直接替你安装好了恢复系统。
