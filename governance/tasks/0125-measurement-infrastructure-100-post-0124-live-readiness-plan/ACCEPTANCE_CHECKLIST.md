# Acceptance Checklist

# Global Standards

- [x] Scope maps to post-0124 100% infrastructure planning.
- [x] No new runtime code, production logic or external dependency is introduced.
- [x] Privacy boundary excludes URL/token/secret/DSN/webhook secret/chat id/report body.
- [x] Roadmap remains the single living plan.
- [x] External live blockers remain explicit.

# Task Package Checklists

## TP-01

- [x] Current baseline commit recorded.
- [x] 0124 final remote CI evidence recorded.
- [x] Live blockers remain explicit.
- Verify: `CONTEXT.md` and `STATUS.md` include 0124 final evidence.
- Gate: no stale 0124 `In Progress` state remains in task index.

## TP-02

- [x] OpenAPI/AsyncAPI/CloudEvents mapping captured.
- [x] Stripe webhook/OpenTelemetry/SRE mapping captured.
- [x] SLSA/GitHub attestation mapping captured.
- Verify: `RESEARCH.md` contains source mapping table.
- Gate: source mapping is used to define evidence requirements, not to claim live completion.

## TP-03

- [x] Resource readiness matrix added.
- [x] Recursive next task tree added.
- [x] Next local task identified as operator execution packet when no credentials are available.
- Verify: roadmap section `6.20` includes matrix, task tree and recommendation.
- Gate: real live tasks keep external credential prerequisites.

## TP-04

- [x] Task docs pass closeout validation.
- [x] Roadmap and index contain 0125.
- [x] No production live overclaim added.
- Verify: task docs validator, `rg` text checks and secret scan pass.
- Gate: `canClaim100Percent` remains false until external live evidence and third-party audit close.
