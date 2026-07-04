# Acceptance Checklist

# Global Standards

- [x] Scope maps to `MI-100.B.00`.
- [x] No production algorithm, provider or renderer is changed.
- [x] Privacy boundary excludes URL/token/secret/DSN/webhook secret/chat id/report body.
- [x] Operator packet remains blocked until real external live evidence is supplied.
- [x] Validation gates have passed.
- [x] Git delivery and remote CI observation are handed to the outer delivery flow.

# Task Package Checklists

## TP-01

- [x] Five production live categories confirmed.
- [x] Upstream work queue/proof-ref/runbook chain confirmed.
- [x] Downstream 0124/0123 gate chain confirmed.
- Verify: `CONTEXT.md` records the evidence chain.
- Gate: no real credential dependency is added.

## TP-02

- [x] Contract added.
- [x] Python generator added.
- [x] Shell wrapper added.
- Verify: files exist and regression imports/executes CLI.
- Gate: packet output remains blocked and redacted.

## TP-03

- [x] local-ci artifact wiring added.
- [x] AGENTS references added.
- [x] Roadmap section added.
- Verify: regression asserts wiring strings.
- Gate: roadmap keeps real live tasks external.

## TP-04

- [x] Targeted pytest passed.
- [x] Ruff check passed.
- [x] Ruff format check passed.
- [x] Task docs validation passed after status closeout update.
- [x] Secret scan passed.
- [x] Quick local CI passed.
- Verify: validation commands in `ACCEPTANCE.md`.
- Gate: no URL/secret output and no over-claim.

## TP-05

- [x] Commit/push is delegated to the outer git delivery flow.
- [x] Remote Acceptance observation is delegated to the outer git delivery flow.
- [x] Remote Container observation is delegated to the outer git delivery flow.
- Verify: final response records commit and CI URLs after push.
- Gate: current remote CI result must be for the final pushed commit before final response.
