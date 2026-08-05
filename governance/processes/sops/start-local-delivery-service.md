---
id: SOP-DEV-LOCAL-DELIVERY
type: process
status: current
owner: experience-delivery
route_key: start_local_delivery_service
route_aliases: ["启动本地 Web", "启动 FastAPI", "运行 delivery 服务"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 启动本地 Web 与 API 服务

## 任务定义
启动同一个 FateCat delivery 进程，同时提供 Web、FastAPI、健康、指标和可选 Telegram webhook 路由。

## 当前状态
本地服务成熟；默认监听 `127.0.0.1:8001`，不是公网生产部署。

## 适用场景
本地 Web 体验、API 调试、浏览器验收或 delivery 集成测试。

## 输入要求
可选环境文件、host/port、token/CORS/job store 配置；不得在命令行传真实 secret。

## 前置条件
执行 bootstrap；端口空闲；如使用 Postgres/webhook，外部配置单独满足。

## 默认工具链
前台运行 `bash scripts/serve-api.sh`；可回收 smoke 使用 `bash scripts/delivery-smoke.sh --target api`。

## 固定路径
入口 `domains/experience-delivery/services/fatecat-delivery/start.py`；服务 `src/main.py`；配置 `infra/environments/local/.env`。

## 成熟参数
host `127.0.0.1`、port `8001`、request timeout 30、rate 120/min、inflight 2、job queue 20、workers 1、TTL 1800 秒。

## 分步执行流程
1. 检查端口和 `.env` 是否 ignored。
2. 运行 delivery smoke。
3. 启动 `serve-api.sh` 并记录 PID。
4. 检查 `/health`、`/ready`、`/metrics`、`/web`、`/docs`。
5. 完成后优雅停止进程。

## 幂等与增量策略
重复启动前先确认现有 PID/端口；不启动第二个实例覆盖旧服务。

## 限速与并发规则
保持默认有界参数；本地调试需要调整时只通过环境变量，禁止设为近似无限。

## 输出目录
日志写 `/tmp/fatecat-delivery-<port>.log`；持久 runtime 按 `infra/runtime/local-state/` 配置。

## 命名规范
PID/日志带端口；调试 artifact `delivery-local-<short-sha>-<UTC>`。

## 质量验收门禁
delivery smoke、health/ready、API/Web regressions、zero-beauty HTML gate 和无端口残留。

## 失败处理
依赖、端口、配置或 startup check 失败时查看日志并停止，不换随机配置掩盖。

## 恢复与重试策略
修复根因后重启同一端口；瞬时冷启动在 smoke timeout 内等待，超时后终止进程。

## 安全边界
默认只监听 loopback；公开监听前必须完成鉴权、CORS、proxy/HSTS 和 production readiness。

## 临时文件清理
停止 PID，删除临时日志和 memory job；不得误杀其他项目/端口进程。

## 运行记录登记
记录 commit、host/port、配置名称而非值、PID、端点状态和停止时间。

## 明确禁止事项
- 禁止把本地服务称为生产部署。
- 禁止提交 `.env`。
- 禁止启动后遗留无人管理进程。
