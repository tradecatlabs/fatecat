# Acceptance Checklist

# Global Standards

- [x] 不伪造公网 webhook live passed evidence。
- [x] 不输出 DSN、URL、secret、token、报告正文、姓名或出生地区。
- [x] `backend.postgres.status` 保持 `planned`。
- [x] `backend.postgres.migration.blockedClaims` 保留 `production_ready`、`multi_replica_ready`、`exactly_once`、`public_webhook_live`、`external_vault_kms`。
- [x] quick CI 只跑 `--allow-missing` preflight。
- [x] 真实 live smoke 若未执行，必须写 `外部连通验证待执行`。

# Task Package Checklists

## TP-01 PRECHECK：公网 webhook live 边界和当前 runtime 能力审查

Verify: 0075 closeout、runtime backend contract、report_jobs/webhook code 已审查。

Gate: 不把 mock、本地 callback 或 worker restart 当公网 live。

- [x] 确认 0075 不覆盖公网 webhook live。
- [x] 确认 `WebhookConfig` 默认拒绝本机、私网和非 HTTPS。
- [x] 确认 public webhook live 需要真实 DSN 与真实 endpoint。

## TP-02 IMPLEMENT：Postgres public webhook live smoke 脚本与 wrapper

Verify: 脚本支持 allow-missing blocked 和 live mode。

Gate: summary 不泄露 DSN/URL/secret/user/report。

- [x] 新增 Python smoke。
- [x] 新增 shell wrapper。
- [x] 实现 blocked summary。
- [x] 实现 live path 和 `_safe_summary`。

## TP-03 VERIFY：契约、schema、gate、local-ci、文档和 AGENTS 接线

Verify: runtime backend gate/test/docs/local-ci 均引用新 smoke。

Gate: Postgres status 仍为 planned，non-claims 清楚。

- [x] 更新 runtime backend registry/schema/gate。
- [x] 更新 local-ci artifact。
- [x] 更新 operations docs、roadmap、AGENTS。
- [x] 更新 regression tests。

## TP-04 TEST：blocked preflight、focused regression、runtime backend gate 和 quick CI

Verify: 本地验证命令通过。

Gate: live 缺配置时只写外部连通验证待执行。

- [x] 语法检查通过。
- [x] blocked preflight 通过。
- [x] runtime backend gate 通过。
- [x] focused tests 通过。
- [x] ruff / format / quick CI 通过。
- [x] task validators 通过。

## TP-05 SHIP：任务 closeout、提交推送和远端 CI 证据

Verify: validators、git clean、push、GitHub Acceptance。

Gate: 当前 commit 远端 CI 通过。

- [ ] 任务文档 closeout。
- [ ] 提交并推送。
- [ ] 远端 CI 通过。
