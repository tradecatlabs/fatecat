# Repo Evidence
| Evidence | Result |
| --- | --- |
| Current branch before 0108 | `git status --short --branch` -> `## main...origin/main` |
| Current HEAD before 0108 | `ef3b646 docs: close current remote ci evidence task` |
| 0107 remote CI | Acceptance run `28674483801` success; Container run `28674485043` success for `ef3b646`. |
| Pre-0108 release proof | `current-release-proof` reports remote CI pass, but release artifact upload pending, GHCR digest fail, attestation pending, rollback pending. |
| Container workflow | `.github/workflows/container.yml` supports `push_image=true`, release artifacts upload, GHCR push, `actions/attest@v4`, and `gh attestation verify`. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Release proof must bind to final HEAD | Commit/push 0108 task package before dispatch. |
| Container publish has external side effect | Explicitly use `push_image=true` only in 0108 after task package commit. |
| Attestation/digest must be real | Only accept GitHub Actions generated digest and attestation verify. |
| Rollback is dry-run | `productionRollbackExecuted=false`; do not claim true production rollback. |
| No secret leakage | Do not output GitHub token, registry token, user data, report body or production logs. |

# Change Boundary
Allowed files before dispatch:
- `governance/tasks/0108-measurement-infrastructure-current-release-artifact-proof/**`
- `governance/tasks/INDEX.md`

No production runtime source, provider algorithms, workflow YAML or release scripts are changed.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| CI/release workflow fails | Release proof remains blocked | Record failing run URL and do not claim pass. |
| GHCR publish succeeds but attestation verify fails | Supply-chain proof incomplete | Treat `current-release-proof` as failed until attestation passes. |
| Writing evidence back creates new HEAD | Evidence stale | Keep final proof in external GitHub Actions and `/tmp`, not committed files. |
| Dry-run rollback overstated | False production readiness | Explicitly report rollback as dry-run only. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| `push_image=true` container workflow uploads release artifacts and pushes GHCR image | Run logs or `current-release-proof` show missing artifact/digest. |
| GitHub token permissions allow package push and attestation | Workflow fails in login/push/attest/verify step. |
| Local rollback drill is accepted for current release proof | `current-release-proof` rejects rollback evidence kind/status/commit. |
| Acceptance must be rerun for final HEAD | If final HEAD already has successful Acceptance, rerun is redundant but still valid. |

# Critical Ambiguities
None blocking. This task intentionally performs a GitHub package publish for the current main HEAD because release artifact proof cannot be completed with `push_image=false`.

# Debug Evidence Contract
- 调试模式: Optional

If a release workflow fails, the follow-up fix task must flip to Required and preserve run URL, failing job, failing step and minimal log summary.

# Task Package Context Map
| Context | Path |
| --- | --- |
| Container workflow | `.github/workflows/container.yml` |
| Current release proof script | `scripts/current-release-proof.py`、`scripts/current-release-proof.sh` |
| Rollback drill | `scripts/rollback-drill.py`、`scripts/rollback-drill.sh` |
| Release artifacts | `scripts/release-artifacts.py`、`scripts/release-artifacts.sh` |
| 0107 prior remote CI | `governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh/` |
