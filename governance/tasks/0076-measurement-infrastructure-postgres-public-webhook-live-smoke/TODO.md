# Execution Checklist

[x] TP-01 | P0 | PRECHECK：公网 webhook live 边界和当前 runtime 能力审查 | Verify: 0075 closeout、runtime backend contract、report_jobs/webhook code 已审查 | Gate: 不把 mock、本地 callback 或 worker restart 当公网 live | Parallelizable: No
[x] TP-02 | P0 | IMPLEMENT：Postgres public webhook live smoke 脚本与 wrapper | Verify: 脚本支持 allow-missing blocked 和 live mode | Gate: summary 不泄露 DSN/URL/secret/user/report | Parallelizable: No
[x] TP-03 | P0 | VERIFY：契约、schema、gate、local-ci、文档和 AGENTS 接线 | Verify: runtime backend gate/test/docs/local-ci 均引用新 smoke | Gate: Postgres status 仍为 planned，non-claims 清楚 | Parallelizable: Yes
[x] TP-04 | P0 | TEST：blocked preflight、focused regression、runtime backend gate 和 quick CI | Verify: 本地验证命令通过 | Gate: live 缺配置时只写外部连通验证待执行 | Parallelizable: No
[ ] TP-05 | P0 | SHIP：任务 closeout、提交推送和远端 CI 证据 | Verify: validators、git clean、push、GitHub Acceptance | Gate: 当前 commit 远端 CI 通过 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
