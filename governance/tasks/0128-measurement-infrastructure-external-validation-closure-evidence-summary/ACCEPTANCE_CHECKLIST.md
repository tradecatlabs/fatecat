# Acceptance Checklist

# Global Standards

- [x] Scope is limited to external validation closure evidence summary.
- [x] No raw secret values are introduced.
- [x] No production endpoint is contacted.
- [x] No external live success is claimed.
- [x] New commands are wired into local validation and documentation.

# Task Package Checklists

## TP-01

- [x] Upstream external validation artifacts identified.
- [x] Non-overlap with trend dashboard and certification recorded.
- [x] Remaining external blockers retained.
- Verify: `CONTEXT.md` records the evidence chain and scope split.
- Gate: no real credential dependency is added.

## TP-02

- [x] Contract added.
- [x] Python generator added.
- [x] Shell wrapper added.
- [x] Output includes domain/category/owner/work item summaries and external pending list.
- Verify: regression imports generator and executes CLI against generated 22-category inputs.
- Gate: summary output remains blocked and redacted when live evidence is missing.

## TP-03

- [x] local-ci artifact wiring added.
- [x] certification audit domain requires operator packet and closure evidence summary.
- [x] Regression tests cover certification contract and fixtures.
- Verify: focused regressions assert local-ci and certification wiring.
- Gate: certification remains blocked when closure summary is blocked.

## TP-04

- [x] AGENTS references added.
- [x] Roadmap section added.
- [x] Task index updated.
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
