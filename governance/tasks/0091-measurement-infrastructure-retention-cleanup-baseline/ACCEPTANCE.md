# Acceptance

## Required

- Retention cleanup smoke 通过，证明 dry-run 与 execute 均可运行。
- Execute 只删除过期 records 和过期终态 report jobs，不删除 fresh terminal 或 old running job。
- Report job 关联 `events`、`webhookOutbox`、`webhookDeliveryConfigs` 随目标 job 删除。
- 缺少本地数据库时 CLI 安全 skipped 且返回 passed summary。
- Summary 不输出 recordId、jobId、userId、姓名、出生地区、报告正文、token、secret、DSN、webhook URL。
- `contracts/fate/security/retention-cleanup.json`、registry、policy、production-security gate、local-ci 和 AGENTS 接线一致。
- 外部 SIEM、production scheduler、Postgres production cleanup live 继续明确标记外部连通验证待执行。

## Not Accepted

- 把本地 smoke 写成 production live passed。
- 默认执行删除。
- 删除 running/pending job。
- 输出真实 ID、用户字段、报告正文或 secret。
- 只更新文档而没有可执行 smoke。
