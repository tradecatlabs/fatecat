# Acceptance Checklist

# Global Standards

- [x] No real credentials, endpoints, DSNs, production logs or report body are stored.
- [x] No production live completion is claimed without external evidence.
- [x] No third-party audit completion is claimed.
- [x] New files are under canonical roots and documented in AGENTS.

# Task Package Checklists

## TP-01 Scope And Upstream Artifact Confirmation

Verify: README/CONTEXT explain MI-100.A.05 bridge.

Gate: no real credential dependency.

- [x] Scope tied to `MI-100.A.05`.
- [x] Upstream artifacts identified.
- [x] Out-of-scope real production calls documented.

## TP-02 Contract Schema Script Wrapper

Verify: contract/schema/script/wrapper exist and targeted tests cover pending/accepted/rejected paths.

Gate: live proof cannot pass without accepted proof-ref and source binding.

- [x] Contract added.
- [x] Live evidence schema added.
- [x] Python gate added.
- [x] Shell wrapper added.
- [x] Pending mode implemented.
- [x] Accepted live proof fixture supported.
- [x] Raw URL/placeholder/sensitive marker rejection implemented.

## TP-03 Wiring

Verify: local-ci, certification, closure trend dashboard, AGENTS and roadmap reference the new gate.

Gate: certification requires live proof artifact and trend can consume live proof gate.

- [x] local-ci artifact added.
- [x] certification audit domain updated.
- [x] closure trend dashboard optional live proof input added.
- [x] regression tests added.
- [x] AGENTS docs updated.
- [x] roadmap updated.

## TP-04 Validation

Verify: ruff, targeted pytest, secret scan, real local artifact chain and quick CI pass.

Gate: generated JSON stays blocked without external live evidence.

- [x] Targeted pytest passed.
- [x] Ruff check passed.
- [x] Ruff format check passed.
- [x] Secret scan passed.
- [x] Real local artifact chain passed.
- [x] Quick local CI passed.

## TP-05 Delivery Package

Verify: commit is pushed and remote CI is observed.

Gate: current remote CI result is recorded before closeout.

- [x] Git commit created.
- [x] Git push completed.
- [x] Remote Acceptance observed.
- [x] Remote Container observed if triggered.
