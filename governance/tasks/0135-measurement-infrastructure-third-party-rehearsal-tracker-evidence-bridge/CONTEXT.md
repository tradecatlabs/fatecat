# Context

0131-0134 已把外部验证 issue 链路推进为：

```text
issue export
  -> tracker import package
  -> tracker issue evidence template
  -> tracker issue evidence gate
  -> measurement infrastructure certification audit domain
```

`scripts/local-ci.sh` 已在 third-party audit rehearsal 前生成三项 tracker artifact。但 `scripts/third-party-audit-rehearsal.py` 原先只消费 current audit bundle、audit dry-run、current release proof、certification 和 external validation closure evidence summary。审计人员只能通过 certification 间接看到 tracker issue evidence blocker，不能在 rehearsal 自身 evidence index 中直接复核 tracker artifact。

# Repo Evidence

- Existing rehearsal generator: `scripts/third-party-audit-rehearsal.py`
- Existing rehearsal contract: `contracts/fate/audit/third-party-audit-rehearsal.json`
- Existing local-ci tracker artifacts: `scripts/local-ci.sh`
- Upstream tracker import task: `governance/tasks/0131-measurement-infrastructure-external-validation-tracker-import-package/`
- Upstream tracker issue evidence gate task: `governance/tasks/0132-measurement-infrastructure-tracker-issue-evidence-gate/`
- Upstream tracker issue evidence template task: `governance/tasks/0133-measurement-infrastructure-tracker-issue-evidence-template/`
- Upstream certification tracker bridge task: `governance/tasks/0134-measurement-infrastructure-certification-tracker-issue-evidence-bridge/`
- Regression target: `tests/regression/test_third_party_audit_rehearsal.py`

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Must not create real issues | Rehearsal bridge only consumes existing local JSON artifacts |
| Must not execute `gh` | No tracker command execution path added |
| Must not claim 100% | Existing blocked/pending semantics remain; tracker artifacts add more checklist blockers |
| Must not leak secrets | Rehearsal scanner rejects raw URL and sensitive assignment fragments |
| Must remain auditable | Evidence index lists tracker artifact path/hash/gate/status |

# Change Boundary

In boundary:

- Rehearsal contract, rehearsal generator, local-ci invocation, regression tests, AGENTS, roadmap, task index and task docs.

Out of boundary:

- External tracker clients, issue creation automation, proof-ref upload, production live checks, release proof sidecar logic and third-party audit result.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Audit rehearsal hides tracker issue creation blocker | Add tracker import/template/gate as direct rehearsal inputs |
| Template `operator_action_required` appears as non-blocking | Add explicit tracker checklist item that remains blocked |
| Rehearsal becomes impossible to generate | Only require local-ci artifacts already generated before rehearsal |
| Sensitive tracker details leak | Keep raw URL/secret scanner across JSON and Markdown output |

# Assumptions and Falsification

- Assumption: `local-ci` output dir contains tracker artifacts before rehearsal runs. Falsifier: quick CI rehearsal step fails on missing required tracker input.
- Assumption: third-party auditors need direct evidence index entries, not certification-only indirection. Falsifier: an external audit process explicitly treats certification JSON as the sole evidence handoff and rejects duplicated index entries.
- Assumption: raw external issue data stays outside rehearsal. Falsifier: any rehearsal output includes raw URL, token, DSN or report body.

# Critical Ambiguities

- Real issue numbers are unavailable in local CI.
- External tracker authorization is unavailable in this task.
- Independent auditor acceptance remains outside this task.

# Debug Evidence Contract

- 调试模式: Optional

No runtime bug is being fixed. If third-party audit rehearsal later accepts an incomplete tracker evidence chain, add a failing fixture to this regression suite and tighten checklist/gate mapping.

# Task Package Context Map

| Asset | Role |
| --- | --- |
| `external-validation-tracker-import-package.json` | Rehearsal direct evidence input |
| `external-validation-tracker-issue-evidence-template.json` | Rehearsal direct evidence input |
| `external-validation-tracker-issue-evidence-gate.json` | Rehearsal direct evidence input |
| `third-party-audit-rehearsal.json` | Auditor-facing pre-audit package |
| `summary.json.artifacts.*` | local-ci artifact discovery path |
