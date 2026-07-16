# Audit Case Sampling Decision

- Source: governance/tasks/0161-measurement-infrastructure-hardening-phase-two
- Fixed Problem: capability 生命周期已拆为 `availability` 与 `maturity.status` 后，control-plane、provider smoke 和 GEO audit 仍有消费者读取旧 `status`，导致 validated 且 available 的能力被误判。
- Decision: case-updated
- Case ID: CASE-9001
- Case Path: governance/evidence/audit-cases/cases/CASE-9001-canonical-field-and-compatibility-projection-double-consumption/CASE.md
- Root Cause Class: canonical_field_and_compatibility_projection_double_consumption
- Trigger Signals: availability/maturity migration；compatibility projection；stale lifecycle consumer；consumer migration；control-plane drift
- Evidence: `DEBUG.md` E4；`REVIEW.md`；`scripts/control-plane-gate.py`；`scripts/provider-dependency-smoke.py`；26 个生命周期专项回归；最终 Quick CI 513 passed。
- No-Case Reason: -

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次生命周期字段迁移必须全仓枚举直接消费者；兼容投影只能用于明确的公共兼容边界，不得重新成为内部执行真相源。
