---
id: SOP-DEV-OBSERVABILITY-SLO
type: process
status: current
owner: sre
route_key: verify_observability_slo
route_aliases: ["验证 metrics", "检查 OTel SLO", "运行观测门禁"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 验证可观测性与 SLO

## 任务定义
验证 health/ready/metrics/request ID/日志、trace contract、SLO policy、alert rules 与外部 OTel backend 证据。

## 当前状态
本地 observability smoke 和 SLO gate 可用；真实 trace/metrics backend、告警路由、error budget 和事故演练待外部证据。

## 适用场景
服务、metrics、日志、追踪、SLO 或生产发布变更。

## 输入要求
observability registry、SLO policy、alert rules；可选脱敏 backend evidence。

## 前置条件
bootstrap 完成；端点可在 TestClient 或本地服务访问；外部 proof 不含敏感 URL/token。

## 默认工具链
`bash scripts/observability-smoke.sh`、`observability-slo-gate.sh`、`otel-collector-slo-gate.sh`、`otel-backend-slo-gate.sh`。

## 固定路径
`contracts/fate/observability/`、`infra/observability/`、delivery metrics/log middleware。

## 成熟参数
本地 gate 使用 contract 默认值；外部证据必须 current commit、proof refs、时间窗和脱敏；不自行修改 SLO 阈值求通过。

## 分步执行流程
1. 运行本地 observability smoke。
2. 校验 SLO policy/alert rules。
3. 校验 collector dry-run contract。
4. 有外部 evidence 时运行 backend gate。
5. 记录本地通过与外部 pending 的不同结论。

## 幂等与增量策略
同一 contract/commit 重复校验稳定；backend proof 过期或配置变化后自动 stale。

## 限速与并发规则
本地 smoke 串行；外部查询使用有界 timeout，不进行高基数或压力流量。

## 输出目录
`infra/runtime/local-state/exports/observability/`。

## 命名规范
`observability-<gate>-<short-sha>-<UTC>.json`。

## 质量验收门禁
本地 signal/SLO/alert 全 PASS；生产声明还需 collector/backend/dashboard/alert/error-budget/incident proof 全部有效。

## 失败处理
缺 signal、指标高基数、日志泄露、SLO/alert 不一致或 proof stale 均 block 相应成熟度。

## 恢复与重试策略
修复 signal/contract 后重跑本地链；外部连接失败有限重试并保留 pending。

## 安全边界
metrics/log/trace 不记录出生信息、报告正文、token、DSN 或 callback URL。

## 临时文件清理
删除本地 trace/log 临时文件；保留脱敏 gate JSON 和必要时间序列摘要。

## 运行记录登记
记录 commit、signal IDs、SLO/alert version、proof refs、时间窗和 gate。

## 明确禁止事项
- 禁止用本地 smoke 宣称生产告警已通。
- 禁止降低阈值掩盖失败。
- 禁止高基数个人数据标签。
