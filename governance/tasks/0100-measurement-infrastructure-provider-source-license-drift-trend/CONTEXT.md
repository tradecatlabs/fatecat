# Repo Evidence
| Evidence | Current Fact |
| --- | --- |
| Branch | `main` |
| Pre-task state | clean and aligned with `origin/main` before 0100 work |
| Existing provider drift scanner | `scripts/provider-drift-scanner.py` outputs `kind=fatecat.provider_drift_report` |
| Existing provider count | scanner reports 4 providers and 4 production capabilities |
| Existing scanner boundary | local only; no external provider live, no external trace backend, no legal review |
| Roadmap source | `governance/tasks/0099-*` and roadmap Wave A A1 name provider/source/license long-running drift trend |

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| Reuse mature/project-native tooling | Reuse provider drift scanner output instead of re-running lower-level checks manually. |
| No external credential dependency | Gate runs fully local and marks external connectivity pending. |
| No user data | Baseline stores only provider/source/license/vendor metadata and hashes. |
| No hidden legal conclusion | License checks remain metadata/SPDX/project-license checks, not legal advice. |
| CI cost | Gate reuses scanner JSON in local-ci to avoid duplicate provider execution. |

# Change Boundary
Allowed:
- `contracts/fate/capabilities/provider-drift-baseline.json`
- `contracts/fate/capabilities/provider-drift-trend-contract.json`
- `contracts/fate/capabilities/schemas/provider.schema.json`
- `scripts/provider-drift-trend-gate.py/.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_provider_drift_trend_gate.py`
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `contracts/fate/capabilities/AGENTS.md`、`scripts/AGENTS.md`、`tests/AGENTS.md`
- `governance/tasks/0100-*`

Not allowed:
- Production provider algorithm changes.
- Registry status promotion/demotion.
- External provider live smoke or legal license conclusion.

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| Trend gate duplicates scanner logic | Only normalize and compare scanner summary; lower-level checks stay in scanner. |
| Legitimate dependency upgrade blocked | Require intentional baseline update in same reviewed change. |
| Baseline leaks sensitive data | Baseline excludes payloads, reports, locations, tokens and DSNs; tests assert forbidden fragments through gate contract. |
| Dynamic scanner timestamp breaks comparison | Trend gate compares normalized provider fields and fingerprints only. |

# Assumptions and Falsification
- Assumption: provider/source/license trend should be anchored by a tracked baseline.
- Falsifier: if source/license changes can be accepted without baseline update, the gate is too weak.
- Assumption: 0100 should not add external live checks.
- Falsifier: if production provider depends on real external SaaS/API, that needs a separate live smoke task with secrets policy.

# Critical Ambiguities
- No unresolved ambiguity blocks local implementation.
- External legal review and external provider live remain future/manual work.

# Debug Evidence Contract
- 调试模式: Optional

Not a bugfix task. If gate/test fails, record failing command, root cause, patch, and rerun evidence in STATUS.md.

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 0084 scanner, 0099 plan, provider schema, local-ci |
| TP-02 | contracts, scripts, AGENTS, docs |
| TP-03 | focused regression tests and formatting |
| TP-04 | task docs, git delivery evidence |
