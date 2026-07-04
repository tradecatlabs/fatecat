# Repo Evidence

| Evidence | Observation |
| --- | --- |
| Current branch | `main` |
| Upstream task chain | 0119 work queue, 0120 proof-ref gate, 0121 category runbooks, 0122 trend dashboard, 0123 live proof gate, 0127 operator packet |
| Existing roadmap anchor | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` section 6.22 lists final release/audit/certification all-sidecar and external closure evidence summary as remaining work |
| Existing local CI path | `scripts/local-ci.sh --profile quick` already produces all upstream external validation artifacts |
| Existing external blocker | Real external credentials, endpoints, operators and third-party audit are not present in repo |

# Constraints Matrix

| Constraint | Handling |
| --- | --- |
| No fake external success | `closureGate.status` remains blocked while proof-ref/live evidence is missing |
| No secrets in repo output | Generator rejects sensitive-looking assignments and raw URLs |
| Must reuse existing chain | Generator consumes existing local-ci external validation artifacts instead of inventing a new source |
| Must be reproducible locally | Script, shell wrapper, regression tests and quick CI artifact are tracked |
| Must not widen to production live | All real live requests remain out of scope and documented as external connectivity pending |

# Change Boundary

Allowed files:

- `contracts/fate/audit/external-validation-closure-evidence-summary.json`
- `scripts/external-validation-closure-evidence-summary.py`
- `scripts/external-validation-closure-evidence-summary.sh`
- `scripts/local-ci.sh`
- `scripts/measurement-infrastructure-certification.py`
- `contracts/fate/audit/measurement-infrastructure-certification.json`
- `tests/regression/test_external_validation_closure_evidence_summary.py`
- focused certification regression test updates
- local `AGENTS.md` owners, roadmap and this task package

Forbidden in this task:

- Production live request execution.
- Credential ingestion.
- New external dependency.
- Provider algorithm or report rendering changes.
- Any claim that external validation passed.

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Summary leaks endpoint or secret value | Security blocker | Raw URL and sensitive assignment rejection; secret scan |
| Summary duplicates trend dashboard without adding value | Complexity risk | Summary includes operator step/proof-ref/live/credential/status rollup for audit, not just stale alerts |
| Certification misses new evidence | Audit drift | Certification audit domain requires operator packet and closure evidence summary |
| Docs imply 100% completion | Audit blocker | Roadmap and task docs keep external live pending language |
| local-ci artifact exists but not wired into summary | Evidence drift | Regression asserts `externalValidationClosureEvidenceSummary` summary key |

# Assumptions and Falsification

Target end state: every external validation category has a single audit-ready closure evidence summary that maps required operator action to current proof-ref/live status and preserves blocked semantics until real evidence exists.

Real constraints: real external credentials and endpoints are unavailable in the repo; secrets must not be stored; current upstream gate outputs are the source of state.

Inertia constraints: trend dashboard already exists but is owner-alert oriented; certification already exists but is domain-gate oriented. Neither should be overloaded with per-work-item operator closure detail.

Wrong concept / wrong boundary: treating stale owner dashboard as the same thing as closure evidence summary.

Kill list: no chat-only status report, no fake proof refs, no raw URL examples, no certification passed claim.

Proof point: targeted pytest, ruff, task docs validation, secret scan and quick local CI prove the summary is generated, wired and certification-aware.

Falsifier: any output contains raw URL/secret assignment, any category is missing, local-ci summary lacks the artifact, or certification can claim 100% with blocked closure summary.

Migration slice: add the audit summary layer without touching production provider logic or executing live checks.

Rejected short-term patches: hand-writing audit prose, adding summary fields only to trend dashboard, or marking proof-ref/live-proof accepted without real external evidence.

# Critical Ambiguities

- Real operators, credentials and endpoints are intentionally unavailable; all live execution remains `外部连通验证待执行`.
- Third-party audit availability is outside repository control.
- This summary can show what is missing; it cannot make missing external evidence true.

# Debug Evidence Contract

- 调试模式: `Optional`
- This is not a bugfix task, but certification or local-ci wiring regressions found during implementation must be covered by regression tests.

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01 | Confirm upstream artifacts and non-overlap with trend dashboard |
| TP-02 | Build contract, generator and shell wrapper |
| TP-03 | Wire local-ci summary artifact and certification audit domain |
| TP-04 | Wire AGENTS, roadmap and task index |
| TP-05 | Run focused validation, docs validation and secret scan |
| TP-06 | Commit, push and observe remote CI through outer delivery flow |
