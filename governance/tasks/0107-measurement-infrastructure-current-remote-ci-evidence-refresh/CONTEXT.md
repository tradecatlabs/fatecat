# Repo Evidence
| Evidence | Result |
| --- | --- |
| Branch | `git status --short --branch` -> `## main...origin/main` before 0107 edits |
| HEAD before 0107 edits | `git log -1 --oneline` -> `2411e97 docs: refresh post-0105 infrastructure plan` |
| Existing remote CI | `gh run list --commit HEAD --limit 20 --json ...` -> `[]` |
| Acceptance workflow | `.github/workflows/acceptance.yml` has `workflow_dispatch` and runs `bash scripts/acceptance.sh --with-dev`. |
| Container workflow | `.github/workflows/container.yml` has `workflow_dispatch` with `push_image=false` default and runs build + smoke. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current commit evidence is recursive if written back into Git | Commit the task package first, then store final CI evidence in GitHub Actions external state. |
| Remote CI must be real | Use `gh workflow run`, `gh run list`, `gh run view`; no synthetic local evidence. |
| No production publish | Dispatch container with `push_image=false`. |
| Timeout possible | If workflow remains queued/in_progress beyond polling window, record as in-progress and do not claim pass. |
| Workflow failure possible | Record failure URL/conclusion and leave release proof blocked. |

# Change Boundary
Allowed files before dispatch:
- `governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh/**`
- `governance/tasks/INDEX.md`

No runtime code, workflow YAML, production configuration or release artifacts are modified.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| CI evidence becomes stale after writing run URLs into repo | Final HEAD differs from tested commit | Do not write run URLs into committed files; use external query for current HEAD. |
| Container workflow accidentally publishes image | External artifact changes without release intent | Dispatch with `push_image=false`; verify input/default. |
| CI fails | Current release proof remains blocked | Record run URL/conclusion; next task fixes failure. |
| `gh` auth/permissions fail | Cannot trigger or read workflow | Record blocker after retry; do not claim evidence. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| Current branch can dispatch workflows | `gh workflow run` returns permission/workflow disabled error. |
| Acceptance/Container are sufficient for current remote CI evidence slice | Release proof still additionally requires digest/attestation, handled by later task. |
| `push_image=false` prevents GHCR publish | Container run logs show push/attest steps executed. |
| Final CI evidence can live outside Git | Auditors can reproduce `gh run list --commit HEAD` with run URLs and headSha. |

# Critical Ambiguities
- Whether to run container with `push_image=true` for full release digest/attestation. This task intentionally does not; release artifact proof remains a later explicit publish task.

# Debug Evidence Contract
- 调试模式: Optional

If either workflow fails, flip to Required in the follow-up fix task and preserve run URL, failing job, failing step and log summary.

# Task Package Context Map
| Context | Path |
| --- | --- |
| 0106 plan | `governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan/` |
| Acceptance workflow | `.github/workflows/acceptance.yml` |
| Container workflow | `.github/workflows/container.yml` |
| Release proof gate | `scripts/current-release-proof.py`、`contracts/fate/delivery/release-gate.json` |
| Roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
