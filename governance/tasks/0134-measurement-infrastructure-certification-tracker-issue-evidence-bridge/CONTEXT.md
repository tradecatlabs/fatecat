# Context

0131-0133 已把外部验证 issue 链路推进为：

```text
issue export
  -> tracker import package
  -> tracker issue evidence template
  -> tracker issue evidence gate
```

`scripts/local-ci.sh` 已生成三项 artifact，并在 summary 中暴露路径。但 `scripts/measurement-infrastructure-certification.py` 的 audit domain 只消费 current audit bundle、proof-ref、runbook、operator packet、live proof、closure trend 和 closure evidence summary，没有消费 tracker import/template/gate。

# Repo Evidence

- Existing certification aggregator: `scripts/measurement-infrastructure-certification.py`
- Existing certification contract: `contracts/fate/audit/measurement-infrastructure-certification.json`
- Existing local-ci tracker artifacts: `scripts/local-ci.sh`
- Upstream tracker import task: `governance/tasks/0131-measurement-infrastructure-external-validation-tracker-import-package/`
- Upstream tracker issue evidence gate task: `governance/tasks/0132-measurement-infrastructure-tracker-issue-evidence-gate/`
- Upstream tracker issue evidence template task: `governance/tasks/0133-measurement-infrastructure-tracker-issue-evidence-template/`
- Regression target: `tests/regression/test_measurement_infrastructure_certification.py`

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Must not create real issues | Certification bridge only consumes existing local JSON artifacts |
| Must not execute `gh` | No tracker command execution path added |
| Must not claim 100% | Existing blocked/pending semantics remain; tracker artifacts add more blockers |
| Must not leak secrets | Aggregator stores path/status/blockingItems only |
| Must remain auditable | Contract requiredEvidenceFiles lists tracker import/template/gate |

# Change Boundary

In boundary:

- Certification contract, aggregator, regression tests, AGENTS, roadmap, task index and task docs.

Out of boundary:

- External tracker clients, issue creation automation, proof-ref upload, production live checks, release proof sidecar logic and third-party audit result.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Certification omits tracker issue creation blocker | Add tracker import/template/gate to audit domain required evidence |
| Template `operator_action_required` appears as non-blocking | Treat `operator_action_required` as blocking gate status |
| Current audit bundle sidecar bypasses tracker chain | Regression verifies tracker artifacts still block audit domain |
| Aggregator becomes impossible to pass | Synthetic full-pass fixture marks tracker artifacts passed and still succeeds |

# Assumptions and Falsification

- Assumption: `local-ci` output dir is the certification evidence dir. Falsifier: certification is run against a custom evidence dir missing tracker artifacts; result must be `failed`.
- Assumption: tracker issue evidence template should block certification until operator fills evidence. Falsifier: future accepted evidence bundle can make template/gate artifacts passed through a dedicated closure task.
- Assumption: raw external issue data stays outside certification. Falsifier: any certification output includes raw URL, token, DSN or report body.

# Critical Ambiguities

- Real issue numbers are unavailable in local CI.
- External tracker authorization is unavailable in this task.
- Independent auditor acceptance remains outside this task.

# Debug Evidence Contract

- 调试模式: Optional

No runtime bug is being fixed. If certification later accepts an incomplete tracker evidence chain, add a failing fixture to this regression suite and tighten the domain mapping.

# Task Package Context Map

| Asset | Role |
| --- | --- |
| `external-validation-tracker-import-package.json` | Required audit evidence |
| `external-validation-tracker-issue-evidence-template.json` | Required audit evidence |
| `external-validation-tracker-issue-evidence-gate.json` | Required audit evidence |
| `measurement-infrastructure-certification.json` | Aggregated certification output |
| `summary.json.artifacts.*` | local-ci artifact discovery path |

