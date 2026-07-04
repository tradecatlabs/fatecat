# Repo Evidence
- Current branch: `main`.
- Current HEAD: `c539c292c08fee1c8d9767ee0be05bbfbfc77a01`.
- Fresh evidence root: `/tmp/fatecat-local-ci-0147-c539c29`.
- Command executed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0147-c539c29`.
- Result: quick local CI passed, focused regression `389 passed in 142.27s`.
- Runtime backend gate: `/tmp/fatecat-local-ci-0147-c539c29/runtime-backend-gate.json`, status `passed`; selected external candidate is `backend.postgres` in gate output and registry checks.
- Postgres dry-run: `/tmp/fatecat-local-ci-0147-c539c29/postgres-job-store-dry-run.json`, status `passed`, backend `backend.postgres`, ship gate `blocked`, required env includes `FATE_REPORT_JOB_STORE=postgres` and `FATE_REPORT_JOB_DATABASE_URL`.
- Postgres live preflight files are all status `blocked`: job store live, worker lease, job worker lease, external worker restart, worker heartbeat/polling and public webhook live.
- Multi-replica runtime evidence: `/tmp/fatecat-local-ci-0147-c539c29/multi-replica-runtime-evidence.json`, status `external_connectivity_pending`.
- Multi-replica runtime gate: `/tmp/fatecat-local-ci-0147-c539c29/multi-replica-runtime-gate.json`, status `passed`, runtime backend `backend.postgres`, live evidence status `外部连通验证待执行`, negative evidence rejected `4`.
- Runtime proof gate: `/tmp/fatecat-local-ci-0147-c539c29/runtime-proof-gate.json`, status `passed`, runtime proof status `external_connectivity_pending`, ship gate `blocked` with blocking items `public_webhook_live`, `external_secret_provider`, `multi_replica_runtime`.
- Event contract gate: `/tmp/fatecat-local-ci-0147-c539c29/event-contract-gate.json`, status `passed`, summary has channel count `4`, event count `5`, operation count `4`, replay example count `2`, dead-letter eligible count `4`, dead-letter status `contract_baseline`.
- Webhook smoke/outbox/redelivery/lease smokes all passed locally and omit callback URL, secret, name, birth place and report markdown from summaries.
- External validation work queue: `/tmp/fatecat-local-ci-0147-c539c29/external-validation-closure-work-queue.json`, work items `22`, total occurrences `453`, stale items `22`, ship gate `blocked`.
- Related work items pending:
  - `event_platform.live`: `external-work.615684420399d1b6`, owner `platform-events`, stale reason `proof_ref_missing`.
  - `runtime.multi_replica_live`: `external-work.592973cda51b7cfd`, owner `runtime-ops`, stale reason `proof_ref_missing`.
  - `runtime.postgres_live`: `external-work.ce47eec5e35ad149`, owner `runtime-ops`, stale reason `proof_ref_missing`.
  - `runtime.public_webhook_live`: `external-work.2cdce9fea4027cd1`, owner `runtime-ops`, stale reason `proof_ref_missing`.
- Certification: `/tmp/fatecat-local-ci-0147-c539c29/measurement-infrastructure-certification.json`, status `blocked`, `canClaim100Percent=false`, external pending domains `12`.

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No fabricated live evidence | Runtime/event proof remains blocked until external operator evidence exists. |
| No sensitive material | Store only paths, counts, status flags, work item IDs and redacted proof requirements. |
| Current worktree only | Evidence is bound to current HEAD `c539c29...`. |
| Runtime/event scope | Limit to Postgres runtime, multi-replica runtime, public webhook and event platform/replay/DLQ. |
| Task package scope | Write only this task directory and `governance/tasks/INDEX.md`; no business code changes. |
| Exactly-once boundary | Record no duplicate terminal job proof if supplied; do not claim exactly-once delivery. |

# Change Boundary
- Changed: `governance/tasks/0147-measurement-infrastructure-runtime-event-external-live-evidence/*`.
- Changed by scaffold: `governance/tasks/INDEX.md`.
- Not changed: application code, contracts, scripts, tests, CI workflows, runtime artifacts.
- `/tmp/fatecat-local-ci-0147-c539c29` is evidence output only and must not be copied into the repository.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Dry-run overclaim | Audit rejects production readiness if local runtime contract is called live evidence. | Task status remains `Blocked`; live smoke preflights remain blocked. |
| DSN or webhook secret leakage | External runtime proof could expose database or callback credentials. | Require redacted proof refs only; no raw URLs, DSNs or secrets in repo. |
| Exactly-once overclaim | Production semantics get overstated beyond evidence. | Explicitly forbid exactly-once claim; only accept no-duplicate-observed proof. |
| Event replay/DLQ ambiguity | Contract baseline may be mistaken for live broker/consumer operation. | Record replay/DLQ as contract baseline; event platform live proof remains blocked. |
| Public webhook ambiguity | Local webhook smoke may be mistaken for public HTTPS delivery. | Record public webhook live smoke preflight as blocked. |
| Certification drift | 100% claim could ignore runtime/event blockers. | Bind 4 work items to 0147 and keep certification blocked. |

# Assumptions and Falsification
- Assumption: Current local runtime/event gates are sufficient to prove readiness for operator live execution.
- Falsifier: Any runtime/event gate fails on current HEAD, or artifact root is missing.
- Assumption: Postgres, multi-replica runtime, public webhook and event platform live proof require external credentials/platform access.
- Falsifier: A redacted operator proof bundle accepted by existing gates shows these are live.
- Assumption: 0147 should not modify business code because it is a live handoff/planning task.
- Falsifier: Operator evidence reveals a contract or gate cannot express required live proof without code changes; that must become a separate implementation task.

# Critical Ambiguities
- Which external Postgres/database instance will be authoritative is not established in repo evidence.
- Which public HTTPS webhook endpoint will be authoritative is not established in repo evidence.
- Which multi-replica runtime environment and duration window will be authoritative is not established in repo evidence.
- Which event platform/broker, replay runner or DLQ consumer will be authoritative is not established in repo evidence.
- These ambiguities do not block documenting 0147 because they are the precise external live blockers.

# Debug Evidence Contract
- 调试模式: Optional
- This task is not a bugfix. No `DEBUG.md` is required.
- If a runtime/event gate fails in a future run, convert the relevant TP leaf into a debug task with reproduction command, root cause and regression evidence.

# Task Package Context Map
| TP | Context |
| --- | --- |
| TP-01 | Current HEAD quick local CI and runtime/event local artifacts. |
| TP-02 | Postgres job store, worker lease, job worker, restart and heartbeat/polling live proof requirements. |
| TP-03 | Multi-replica runtime, public webhook and runtime proof pack proof requirements. |
| TP-04 | Event platform, CloudEvents/AsyncAPI, replay and DLQ proof requirements. |
| TP-05 | Related work items, proof-ref/live-proof gate and certification linkage. |
