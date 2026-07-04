# Acceptance Checklist

# Global Standards
- [x] Current local evidence is bound to HEAD `c539c292c08fee1c8d9767ee0be05bbfbfc77a01`.
- [x] Local readiness is not claimed as runtime/event external live completion.
- [x] Postgres live remains blocked.
- [x] Multi-replica runtime live remains blocked.
- [x] Public webhook live remains blocked.
- [x] Event platform/replay/DLQ live remains blocked.
- [x] Exactly-once is not claimed.
- [x] Real credentials and raw production evidence are not stored.
- [x] 100% certification remains blocked.

# Task Package Checklists
## Current runtime/event evidence

### TP-01.01 Current HEAD runtime/event gates
- [x] quick local CI passed.
- [x] runtime backend gate passed.
- [x] Postgres dry-run passed.
- [x] multi-replica runtime gate passed.
- [x] runtime proof gate passed with ship gate blocked.
- [x] event contract gate passed.
Verify: `test -d /tmp/fatecat-local-ci-0147-c539c29 && jq '.status' /tmp/fatecat-local-ci-0147-c539c29/runtime-proof-gate.json`.
Gate: artifact root exists and focused regression showed `389 passed`.

## Postgres runtime live

### TP-02.01 Postgres runtime live proof
- [ ] External Postgres job store live smoke proof submitted by operator.
- [ ] Worker lease, job worker lease, external worker restart and heartbeat/polling proof submitted by operator.
- [ ] Proof refs are redacted and no DSN or database credential is stored.
Verify: `jq '.status' <accepted-postgres-runtime-live-proof-json>`.
Gate: `runtime.postgres_live` proof-ref/live-proof accepted.

## Multi-replica and public webhook live

### TP-03.01 Multi replica public webhook proof
- [ ] Multi-replica runtime soak proof submitted by operator.
- [ ] Public webhook live smoke proof submitted by operator.
- [ ] No duplicate terminal job proof is provided without claiming exactly-once.
- [ ] Public endpoint proof redacts raw URL, webhook secret and report body.
Verify: `jq '.runtimeProofStatus' <accepted-runtime-proof-pack-json>`.
Gate: `runtime.multi_replica_live` and `runtime.public_webhook_live` proof refs accepted.

## Event platform replay DLQ live

### TP-04.01 Event replay DLQ proof
- [ ] Event platform live proof submitted by operator.
- [ ] Replay runner proof submitted by operator.
- [ ] Dead-letter record/consumer proof submitted by operator.
- [ ] Event payload proof uses redacted payload refs only.
Verify: `jq '.summary' <accepted-event-platform-live-proof-json>`.
Gate: `event_platform.live` proof-ref/live-proof accepted.

## Certification refresh

### TP-05.01 Runtime event proof bundle
- [ ] Four runtime/event work items leave pending state.
- [ ] proof-ref gate accepts all relevant runtime/event proof refs.
- [ ] live-proof gate accepts all relevant runtime/event live proofs.
- [ ] certification rerun references accepted proof without leaking sensitive material.
Verify: `jq '.acceptedProofRefs, .acceptedLiveProofs' <accepted-external-validation-gate-json>`.
Gate: runtime/event categories no longer block certification.
