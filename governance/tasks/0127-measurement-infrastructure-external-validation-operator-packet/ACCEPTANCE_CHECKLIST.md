# Acceptance Checklist

# Global Standards

- [x] Scope is limited to external validation operator packet preparation.
- [x] No raw secret values are introduced.
- [x] No production endpoint is contacted.
- [x] No external live success is claimed.
- [x] New commands are wired into local validation and documentation.

# Task Package Checklists

## TP-01

- [x] 0119/0120/0121 upstream inputs identified.
- [x] 0126 production-only packet boundary kept separate.
- [x] Remaining external blockers retained.
- Verify: `CONTEXT.md` records the evidence chain and scope split.
- Gate: no real credential dependency is added.

## TP-02

- [x] Contract added.
- [x] Python generator added.
- [x] Shell wrapper added.
- [x] Output includes domain groups, operator steps, required credentials, proof-ref template and final gate commands.
- Verify: regression imports generator and executes CLI against generated runbooks.
- Gate: packet output remains blocked, redacted and all-category scoped.

## TP-03

- [x] Postgres live runbook commands do not use nonexistent `--require-live`.
- [x] Webhook allowed-hosts environment variable uses `FATE_WEBHOOK_LIVE_ALLOWED_HOSTS`.
- [x] Regression tests cover both alignments.
- Verify: focused regressions assert command/env-var strings.
- Gate: no nonexistent operator command flags remain in serialized runbooks.

## TP-04

- [x] `scripts/local-ci.sh` generates external validation operator packet artifact.
- [x] `summary.json` exposes `externalValidationOperatorExecutionPacket`.
- [x] `scripts/AGENTS.md`, `contracts/fate/audit/AGENTS.md`, `tests/AGENTS.md` and roadmap mention new files.
- Verify: regression asserts wiring strings.
- Gate: roadmap keeps real live tasks external.

## TP-05

- [x] Python syntax validation planned.
- [x] Focused pytest planned.
- [x] ruff check/format planned.
- [x] task docs validation planned.
- [x] secret scan planned.
- [x] quick CI planned for final HEAD.
- Verify: validation commands are listed in `ACCEPTANCE.md` and executed before delivery.
- Gate: no URL/secret output and no over-claim.

## TP-06

- [x] Commit/push handled by outer delivery flow.
- [x] Remote CI observation handled by outer delivery flow.
- [x] External live blockers remain documented.
- Verify: final response records commit and CI URLs after push.
- Gate: current remote CI result must be for the final pushed commit before final response.
