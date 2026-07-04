# Task-Level Acceptance
- Current HEAD quick local CI evidence is refreshed and recorded.
- Runtime backend/Postgres/multi-replica/runtime proof local gates are recorded with passed or blocked-as-expected state.
- Event contract/replay/DLQ/webhook local gates are recorded with passed or contract-baseline state.
- Four runtime/event external work items are identified with owner, id, status and stale reason.
- Task status remains `Blocked`; no runtime/event live or 100% infrastructure completion is claimed.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Current HEAD local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0147-c539c29` | Exit 0, focused regression `389 passed` |
| Runtime backend gate | `jq '.status' /tmp/fatecat-local-ci-0147-c539c29/runtime-backend-gate.json` | `passed` |
| Postgres dry-run | `jq '{status, shipGate:.shipGate.status}' /tmp/fatecat-local-ci-0147-c539c29/postgres-job-store-dry-run.json` | `status=passed`, ship gate `blocked` |
| Postgres live preflight | `jq '.status' /tmp/fatecat-local-ci-0147-c539c29/postgres-job-store-live-smoke.json` | `blocked` until external DB evidence exists |
| Multi-replica gate | `jq '{status, liveEvidenceStatus}' /tmp/fatecat-local-ci-0147-c539c29/multi-replica-runtime-gate.json` | `status=passed`, live evidence pending |
| Runtime proof gate | `jq '{status, runtimeProofStatus, shipGate:.shipGate.status}' /tmp/fatecat-local-ci-0147-c539c29/runtime-proof-gate.json` | `status=passed`, proof pending, ship gate blocked |
| Event contract gate | `jq '.summary' /tmp/fatecat-local-ci-0147-c539c29/event-contract-gate.json` | channels `4`, events `5`, operations `4`, replay examples `2`, DLQ eligible `4` |
| Related external work items | `jq '[.workItems[] | select(.category|test("^(runtime|event_platform)\\."))]' /tmp/fatecat-local-ci-0147-c539c29/external-validation-closure-work-queue.json` | 4 pending work items |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0147-measurement-infrastructure-runtime-event-external-live-evidence --phase decompose` | Pass |

# Review Gate
- Verify wording does not claim external live completion.
- Verify no DSN, token, secret, raw URL, production logs, trace payload, user input, report body or webhook secret is copied into task docs.
- Verify local gates and external blockers are separated.
- Verify 0147 remains aligned with 0143 and does not supersede 0144/0145/0146 external proof/live blockers.

# Runtime Verification Gate
- No external database, webhook endpoint or event broker is started by this task.
- Runtime evidence is limited to quick local CI artifacts in `/tmp/fatecat-local-ci-0147-c539c29`.
- Public/live verification remains operator-owned and must be supplied as redacted proof-ref/live proof bundles.

# Ship Readiness
- Local task package can be committed once decompose validation passes.
- Runtime/event external live is not shippable until:
  - Postgres job store and migration/job live smoke proof refs are accepted,
  - worker lease, job worker, restart recovery and heartbeat/polling proof refs are accepted,
  - public webhook live proof ref is accepted,
  - multi-replica runtime soak proof ref is accepted,
  - event platform/replay/DLQ proof refs are accepted.
- Measurement infrastructure 100% certification remains blocked.

# Task Package Acceptance
## TP-01 Current HEAD runtime/event evidence refresh
- Acceptance: current HEAD quick local CI passed and runtime/event artifacts exist.
- Evidence: `/tmp/fatecat-local-ci-0147-c539c29`.

## TP-02 Postgres runtime live proof
- Acceptance: local Postgres adapter/dry-run is passed, but external Postgres live proof is missing.
- Evidence: Postgres dry-run passed, live smoke preflights blocked.

## TP-03 Multi-replica and public webhook live proof
- Acceptance: multi-replica proof grammar is passed, but live soak/public webhook proof is missing.
- Evidence: multi-replica gate passed, runtime proof gate ship gate blocked.

## TP-04 Event platform replay/DLQ live proof
- Acceptance: event contract/replay/DLQ baseline is passed, but event platform live proof is missing.
- Evidence: event contract gate passed, event platform work item pending.

## TP-05 Runtime/event proof bundle and certification refresh
- Acceptance: 4 runtime/event work items remain pending and certification remains blocked.
- Evidence: work queue includes 4 runtime/event work items, certification `canClaim100Percent=false`.

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
