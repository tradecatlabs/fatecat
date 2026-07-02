# Execution Checklist

[x] TP-01.01 | P0 | 复核 0070 Postgres adapter、runtime backend contract 和本地运行条件 | Verify: git status / rg / docs review | Gate: 0071 只新增 live evidence path | Parallelizable: No
[x] TP-02.01 | P0 | 新增 Postgres live smoke 脚本与 wrapper | Verify: py_compile + real Docker Postgres smoke | Gate: schema/job/event/outbox/config 路径真实执行 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 production-readiness evidence gate | Verify: positive/negative readiness commands | Gate: 不得只靠布尔变量声明通过 | Parallelizable: No
[x] TP-02.03 | P0 | 同步 runtime backend contract、schema、registry 和 gate | Verify: runtime-backend-gate + schema tests | Gate: live_smoke_baseline 不等于 production ready | Parallelizable: Yes
[x] TP-03.01 | P0 | 新增 live smoke 回归测试 | Verify: focused pytest | Gate: missing DSN、privacy、contract、docs wiring covered | Parallelizable: Yes
[x] TP-03.02 | P0 | 运行无 DSN allow-missing blocked preflight | Verify: blocked JSON artifact | Gate: 本地无 DSN 不伪造通过 | Parallelizable: Yes
[x] TP-03.03 | P0 | 运行一次性 Docker Postgres live smoke | Verify: passed JSON artifact | Gate: 16 checks passed + no sensitive marker leak | Parallelizable: Yes
[x] TP-04.01 | P0 | 同步 AGENTS、operations docs、roadmap 和任务索引 | Verify: rg/diff review | Gate: 文档不夸大 production readiness | Parallelizable: Yes
[x] TP-04.02 | P0 | 运行 validation、quick local-ci、任务 validators、提交推送和远端 CI | Verify: local-ci/validators/git delivery evidence | Gate: 本地 quick CI 通过；远端 CI 推送后刷新 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
