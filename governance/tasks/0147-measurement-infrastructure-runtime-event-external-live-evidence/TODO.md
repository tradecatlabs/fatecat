# Execution Checklist
[x] TP-01.01 | P0 | Refresh current HEAD runtime/event local evidence | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0147-c539c29` | Gate: quick local CI passed with `389 passed` | Parallelizable: No
[ ] TP-02.01 | P0 | Collect Postgres runtime live proof | Verify: `jq '.status' <accepted-postgres-runtime-live-proof-json>` | Gate: runtime.postgres_live proof refs accepted without DSN or credential leakage | Parallelizable: Yes
[ ] TP-03.01 | P0 | Collect multi-replica public webhook proof | Verify: `jq '.runtimeProofStatus' <accepted-runtime-proof-pack-json>` | Gate: runtime.multi_replica_live and runtime.public_webhook_live proof refs accepted without exactly-once overclaim | Parallelizable: Yes
[ ] TP-04.01 | P0 | Collect event replay DLQ proof | Verify: `jq '.summary' <accepted-event-platform-live-proof-json>` | Gate: event_platform.live proof refs accepted with redacted payload refs | Parallelizable: Yes
[ ] TP-05.01 | P0 | Submit runtime/event proof bundle and rerun certification | Verify: proof-ref/live-proof/certification gate summaries | Gate: runtime/event categories no longer block certification | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
