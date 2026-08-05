---
id: SOP-OPS-POSTGRES-RUNTIME
type: process
status: current
owner: sre
route_key: verify_postgres_runtime
route_aliases: ["验证 Postgres job store", "测试多 worker lease", "检查持久任务恢复"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 验证 Postgres Durable Runtime

## 任务定义
在真实或一次性 Postgres 上验证 schema、job/idempotency/event、outbox、worker lease、崩溃恢复和 heartbeat/polling。

## 当前状态
adapter 与 live smoke 工具已实现；长期多副本生产、exactly-once、外部 secret manager 仍需外部证据。

## 适用场景
启用/升级 Postgres backend、迁移、worker 或 durable job 逻辑变更。

## 输入要求
DSN 环境变量名，默认 `FATE_REPORT_JOB_DATABASE_URL`；可选 smoke schema/keep/allow-missing。

## 前置条件
psycopg 可用；测试数据库授权；DSN 不进入命令/日志；确认 smoke schema 可创建/删除。

## 默认工具链
依次运行 `postgres-job-store-live-smoke.sh`、worker lease、external worker restart、heartbeat/polling 和 runtime gate。

## 固定路径
`contracts/fate/delivery/runtime-backends.json`、Postgres store/DDL、`scripts/postgres-*-smoke.sh`。

## 成熟参数
默认生成一次性 schema并结束后 drop cascade；仅巡检缺环境时使用 `--allow-missing`，release 不允许；不要 `--keep-schema`。

## 分步执行流程
1. 验证 DSN env 存在但不打印值。
2. 运行基础 live smoke。
3. 运行 outbox/job worker lease 竞争 smoke。
4. 运行 crash/restart 和 heartbeat/polling smoke。
5. 聚合 runtime proof/multi-replica gate。

## 幂等与增量策略
每次使用唯一 schema；smoke rows/namespace 隔离；同 commit 的通过证据可复核，但 backend/DDL 变化后全链重跑。

## 限速与并发规则
仅 smoke 内创建受控两个 worker竞争；外部执行串行；连接池和 DB 上限按测试库约束。

## 输出目录
`infra/runtime/local-state/exports/postgres-runtime/<short-sha>/`。

## 命名规范
schema `fatecat_smoke_<timestamp>_<random>`；证据 `postgres-<stage>-<short-sha>.json`。

## 质量验收门禁
基础 CRUD/idempotency/outbox、单 winner lease、错误 owner rejection、expiry reclaim、restart recovery、heartbeat/polling 和脱敏全部 PASS。

## 失败处理
DSN/driver/权限缺失标记 external pending；语义失败 block，默认清理 schema并保存脱敏摘要。

## 恢复与重试策略
数据库瞬时连接有限重试；逻辑失败修复后新 schema 全链重跑；不得复用污染 schema。

## 安全边界
不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入；只对授权测试数据库操作。

## 临时文件清理
默认 drop smoke schema；停止 worker/连接；删除本地临时 evidence副本。

## 运行记录登记
记录 DB provider/version、schema hash/name hash、commit、阶段结果、延迟、cleanup 和 external gaps。

## 明确禁止事项
- 禁止 `--allow-missing` 结果作为 release PASS。
- 禁止宣称 exactly-once。
- 禁止对生产业务 schema 直接运行 smoke。
