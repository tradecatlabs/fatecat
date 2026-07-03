# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Prior W0 | `0110-measurement-infrastructure-current-release-truth-finalizer` completed current release proof. |
| Capability source | `contracts/fate/capabilities/registry.json` has 9 capabilities: 4 production, 5 planned. |
| Provider source | `scripts/provider-lifecycle-gate.py` already validates production provider lifecycle metadata. |
| ReleaseGate source | `contracts/fate/delivery/release-gate.json` has 10 required evidence entries and live shipGate blocked. |
| EvaluationRun source | `contracts/fate/evaluations/registry.json` has 5 Dataset resources and 5 EvaluationRun resources. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No new runtime controller | Implement contract/gate baseline only. |
| Reuse existing gates | Provider depth delegated to provider lifecycle gate. |
| No production secret access | Gate reads contracts and provider metadata only. |
| No live overclaim | ReleaseGate status remains pending_external where external proof is required. |
| Minimal ownership | New directory only for control-plane envelope; existing source registries remain truth sources. |

# Change Boundary
- Allowed: `contracts/fate/control-plane/**`, `contracts/fate/AGENTS.md`, `scripts/control-plane-gate.py`, `scripts/control-plane-gate.sh`, `scripts/local-ci.sh`, `tests/regression/test_control_plane_gate.py`, `governance/tasks/0111-*`, task index, roadmap.
- Not allowed: business algorithms, API behavior, workflow YAML, production secrets, external deployment.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Duplicate truth source | Control plane could drift from registries | Store refs and expected summaries only; gate recomputes from source. |
| Reimplement provider lifecycle poorly | Miss source/license/vendor drift | Delegate provider depth to existing provider lifecycle gate. |
| ReleaseGate blocked seen as failure | False negative for local control plane | Treat contract availability separately from external live shipGate. |
| Overbroad local-ci cost | Quick CI slows unnecessarily | Gate is metadata-only and reuses existing provider lifecycle checks. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| W1 baseline can be satisfied by contract/gate resource reconciliation before a runtime controller. | User explicitly requires long-running controller runtime in this slice. |
| Capability count is 9, production 4, planned 5. | `contracts/fate/capabilities/registry.json` changes without control-plane update. |
| Evaluation registry has 5 datasets and 5 runs. | New EvaluationRun/Dataset lands without control-plane desiredState update. |
| ReleaseGate requiredEvidence count is 10. | ReleaseGate adds/removes evidence without control-plane update. |

# Critical Ambiguities
- Future W1+ may need a real reconciliation loop or status API, but this slice intentionally establishes the contract/gate baseline first.
- External live systems remain outside current proof boundary.

# Debug Evidence Contract
- 调试模式: Optional

No runtime bug is being fixed. If control-plane gate fails later, switch to `auto-debug` with the failing check name as root evidence.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Control-plane registry | `contracts/fate/control-plane/registry.json` |
| Control-plane schema | `contracts/fate/control-plane/schemas/control-plane.schema.json` |
| Control-plane gate | `scripts/control-plane-gate.py` |
| Provider lifecycle gate | `scripts/provider-lifecycle-gate.py` |
| Regression tests | `tests/regression/test_control_plane_gate.py` |
| Local CI | `scripts/local-ci.sh` |
