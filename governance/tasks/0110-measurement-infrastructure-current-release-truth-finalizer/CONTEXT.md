# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `main` |
| Previous planning task | `0109-measurement-infrastructure-100-post-0108-deep-research-plan` |
| Prior proof snapshot | HEAD `2b587dfd131c3b654cedd2efea6aad41056e8442` passed current-release-proof before this finalizer patch |
| Current drift | `governance/tasks/INDEX.md` contained duplicate 0108 rows before this task |
| Proof gate | `scripts/current-release-proof.sh --require-current-release` |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current branch only | Stay on `main`; do not switch branch or worktree. |
| Documentation-only state fix | Change only governance task docs and task index. |
| Final proof after commit | Do not write final proof back to Git because it would create a new HEAD. |
| Remote CI required | GitHub Actions terminal success is required; local acceptance is auxiliary only. |
| Dry-run rollback boundary | Keep `productionRollbackExecuted=false`; no real traffic switch. |

# Change Boundary
- Allowed: `governance/tasks/0110-*`, `governance/tasks/INDEX.md`.
- Not allowed: runtime code, provider algorithms, workflow YAML, secrets, external deployment, production rollback.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Committed evidence changes HEAD | Release proof becomes stale | Keep exact final proof external to Git and report it after commit. |
| Duplicate 0108 status remains | Audit sees task-state contradiction | Remove duplicate row and verify count equals one. |
| workflow dispatch mistaken for success | False release readiness | Wait for terminal success and run current-release-proof. |
| local acceptance mistaken for remote CI | False remote proof | Treat local acceptance only as auxiliary evidence. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 0108 duplicate status is an index hygiene bug, not a business-code issue. | Another task source of truth requires two 0108 rows. |
| Final proof can remain outside Git to preserve immutable HEAD. | Project policy requires proof JSON committed even if that forces another proof cycle. |
| Production live systems are out of scope. | User provides live credentials and explicitly requires production live smoke. |

# Critical Ambiguities
- Exact final run IDs are not known until after this task package is committed and workflows are dispatched.
- External production credentials are not present in the repository.

# Debug Evidence Contract
- 调试模式: Optional

This is a release truth finalizer, not a code defect reproduction. If remote workflow fails, follow-up must switch to `auto-debug` with run logs.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Task index | `governance/tasks/INDEX.md` |
| Previous plan | `governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan/` |
| Acceptance workflow | `.github/workflows/acceptance.yml` |
| Container workflow | `.github/workflows/container.yml` |
| Release proof gate | `scripts/current-release-proof.sh` |
| Rollback drill | `scripts/rollback-drill.sh` |
