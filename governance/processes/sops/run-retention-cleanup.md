---
id: SOP-OPS-RETENTION-CLEANUP
type: process
status: current
owner: security
route_key: run_retention_cleanup
route_aliases: ["清理过期记录", "执行 retention", "删除过期报告任务"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 执行数据保留期清理

## 任务定义
按记录、审计事件和报告任务保留策略先 dry-run，再在明确授权下删除或 tombstone/purge 过期数据。

## 当前状态
SQLite 本地 cleanup 成熟；生产 Postgres/scheduler/不可变审计清理需要外部 staged evidence。

## 适用场景
定期 retention、隐私删除验证或存储维护；不用于清理开发缓存。

## 输入要求
record/report-job DB 路径、record/audit days、job TTL、delete mode、可选固定 `--now`。

## 前置条件
备份/恢复策略已验证；数据库不被并发迁移；执行删除获得授权；策略与环境一致。

## 默认工具链
先 `bash scripts/retention-cleanup.sh --output-json <dry-run.json>`，复核后加 `--execute`；生产证据用 staged gate。

## 固定路径
默认 record DB `infra/runtime/local-state/databases/bazi.sqlite`、job DB `report_jobs.sqlite`、security retention contracts。

## 成熟参数
record days 默认 0、audit days 30、job TTL 1800 秒、mode `hard_delete`；默认 dry-run。

## 分步执行流程
1. 记录 DB hash/大小和策略。
2. 执行 dry-run并核对候选计数/截止时间。
3. 取得删除授权。
4. 使用相同参数执行 `--execute`。
5. 验证剩余/删除数、审计事件和恢复证据。

## 幂等与增量策略
重复执行只处理新增过期项；相同 `--now` 的第二次执行应删除 0。

## 限速与并发规则
单数据库单 cleanup worker；避免高峰和长事务；生产大表必须分批/平台化，不用本地脚本全表锁。

## 输出目录
`infra/runtime/local-state/exports/retention/`。

## 命名规范
`retention-dry-run-<db-ref>-<UTC>.json`、`retention-execute-<approval-id>-<UTC>.json`。

## 质量验收门禁
dry-run/execute 参数一致、候选合理、删除后重跑为 0、审计事件存在、备份恢复可用。

## 失败处理
计数异常、DB 锁、策略漂移、备份缺失或部分删除时停止并进入恢复流程。

## 恢复与重试策略
hard delete 依赖备份恢复；tombstone 按 policy purge；锁/瞬时错误有限重试，不重复未知 partial transaction。

## 安全边界
`--execute` 是不可逆副作用；不得删除 audit 保留范围内或 legal hold 数据。

## 临时文件清理
删除 dry-run 临时副本；保留执行证据和审计事件；备份按独立 retention 管理。

## 运行记录登记
记录 approval、operator、DB ref/hash、策略、now、候选/删除/剩余、事务和恢复点。

## 明确禁止事项
- 禁止跳过 dry-run。
- 禁止在无备份/授权时 `--execute`。
- 禁止把 SQLite cleanup 证据写成生产 Postgres cleanup 已完成。
