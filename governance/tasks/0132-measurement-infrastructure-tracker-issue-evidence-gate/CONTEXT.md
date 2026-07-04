# Context

0131 已生成 external validation tracker import package：issue body files、import manifest 和人工可复核 `gh issue create` command text。该产物仍停在“可创建 issue”的准备阶段，没有结构化验证“operator 是否真的创建了对应 issue，以及 issue body 是否和 package hash 对齐”。

0132 补齐这一层：新增 tracker issue evidence gate。gate 默认不带外部 evidence，因此必须输出 pending/blocked；当 operator 后续在授权 tracker 会话中手工创建 issue 并提交脱敏 evidence bundle 时，gate 验证：

- evidence bundle source package sha256 与当前 import package 一致。
- commit 与当前 gate 预期 commit 一致。
- `workItemId` 存在于 import package。
- `issueTemplateId` 与对应 command/package body 一致。
- `bodySha256` 与 import package body file sha256 一致。
- `trackerIssueRef` 使用 sanitized `github:<owner>/<repo>#<number>`，不使用 raw URL。
- labels 包含 `external-validation`、`measurement-infrastructure`、`operator-action-required`。
- 输出不包含 token/secret/DSN/raw URL/placeholder。

# Constraints

- 不调用 GitHub API。
- 不执行 `gh`。
- 不创建真实 issue。
- 不连接任何 production/live 外部系统。
- 不保存真实 URL、凭证值、生产日志、用户输入或报告正文。
- 即使 issue evidence accepted，也不能放行 live proof、certification 或 third-party audit。

# Source Chain

```text
0130 issue export
  -> 0131 tracker import package
  -> 0132 tracker issue evidence gate
  -> 0120 proof-ref gate
  -> 0123 live proof gate
  -> certification
  -> third-party audit rehearsal
```

# Repo Evidence

- Current upstream artifact: `scripts/external-validation-tracker-import-package.py`
- New contract: `contracts/fate/audit/external-validation-tracker-issue-evidence.json`
- New gate: `scripts/external-validation-tracker-issue-evidence-gate.py`
- New wrapper: `scripts/external-validation-tracker-issue-evidence-gate.sh`
- New regression: `tests/regression/test_external_validation_tracker_issue_evidence_gate.py`
- Local CI hook: `scripts/local-ci.sh --profile quick`
- Roadmap source: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Must not create real issues | Gate only consumes local JSON and emits local JSON |
| Must not execute `gh` | Wrapper only runs Python gate; no tracker CLI call |
| Must not claim live passed | `shipGate.status` remains `blocked` |
| Must protect secrets | Raw URL, sensitive assignment and placeholder markers rejected |
| Must be auditable | Output binds package sha256, commit, workItemId, issueTemplateId and body hash |

# Change Boundary

In boundary:

- Contract, script, wrapper, regression, local-ci artifact wiring, AGENTS, roadmap and task docs.

Out of boundary:

- Tracker API clients, issue creation automation, production endpoint live checks, proof-ref upload, live proof closure, certification override and third-party audit result.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Evidence references wrong package | Source package sha256 and commit mismatch fail fast |
| Evidence maps to wrong issue body | `bodySha256` must match package file sha |
| Evidence leaks URL or secret | raw URL and sensitive assignment regex rejection |
| Gate is mistaken for production closure | `shipGate` remains blocked and non-claims are explicit |
| Duplicate or unknown work item accepted | rejected issues record `duplicate_work_item` / `unknown_work_item` |

# Assumptions and Falsification

- Assumption: operator can later provide sanitized `github:<owner>/<repo>#<number>` issue refs. Falsifier: tracker uses a non-GitHub issue namespace; then contract needs an allowed ref extension, not raw URL fallback.
- Assumption: package body file sha256 is sufficient to bind created issue body to import package. Falsifier: tracker normalizes body text before storage; then evidence bundle needs an additional tracker-rendered-body hash policy.
- Assumption: issue creation is an external side effect and should remain manual until explicitly authorized. Falsifier: user explicitly authorizes automated issue creation with a scoped token and rate limits.

# Critical Ambiguities

- Actual issue numbers are not known in repository-local execution.
- External tracker account, token and repository permissions are not available in local CI.
- Third-party audit acceptance criteria remain external to this task.

# Debug Evidence Contract

- 调试模式: Optional

No runtime bug is being fixed. If the gate rejects valid evidence later, reproduce with a redacted evidence bundle, record rejected reason, and add a regression fixture before changing validation rules.

# Task Package Context Map

| Asset | Role |
| --- | --- |
| `external-validation-tracker-import-package.json` | Required input source |
| `external_validation_tracker_issue_evidence_bundle` | Optional operator evidence |
| `external-validation-tracker-issue-evidence-gate.json` | Gate output |
| `summary.json.artifacts.externalValidationTrackerIssueEvidenceGate` | local-ci discovery path |
