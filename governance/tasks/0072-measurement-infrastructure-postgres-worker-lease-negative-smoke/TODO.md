# Execution Checklist

[x] TP-01 | P0 | 边界与证据目标 | Verify: 0071 closeout、runtime backend contract 和 roadmap 已确认 | Gate: 本任务只证明 Postgres webhook outbox lease negative path | Parallelizable: No
[x] TP-02 | P0 | Worker lease negative smoke 实现 | Verify: scripts/postgres-worker-lease-smoke.py 与 .sh 已新增并通过语法检查 | Gate: duplicate claim、错误 owner release、lease expiry reclaim 均被验证 | Parallelizable: No
[x] TP-03 | P0 | Contract、文档和测试接线 | Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线 | Gate: backend.postgres.status=planned 且 implementationStatus=worker_lease_smoke_baseline | Parallelizable: Yes
[x] TP-04 | P0 | 验证、closeout 和交付 | Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan 和 task validator | Gate: 本地验证通过且远端 CI 由 Git 交付刷新 | Parallelizable: No
