# Task Context

## 背景

FateCat 已有 `control.retention_cleanup_plan`、production security policy 和 externalization evidence contract，但之前主要停留在“计划和证据格式”。这会造成基础设施视角下的灯下黑：最基础的数据保留与清理控制存在文档声明，却缺少本地可执行的清理路径。

## 当前切片

0091 只把 retention cleanup 推进为本地 SQLite baseline：

- `records`：按 `created_at` 与 `FATE_RECORD_RETENTION_DAYS` 找候选并删除。
- `reportJobs`：按 `expires_at` 删除过期终态 job，并级联删除 events/outbox/delivery config 行。
- `auditEvents`：当前是结构化日志，明确标记外部 SIEM/不可变审计存储 retention 待验证。

## 边界

- 默认 dry-run，只有显式 `--execute` 才删除。
- summary 只允许输出目标、计数、模式、cutoff 和状态。
- 缺库或缺表必须安全 skipped，而不是失败。
- 不处理 production scheduler、Postgres production cleanup live 或外部 SIEM。
