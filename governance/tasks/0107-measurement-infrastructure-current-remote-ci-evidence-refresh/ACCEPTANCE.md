# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Current commit remote CI evidence | `gh run list --commit HEAD` returns Acceptance and Container runs for final HEAD. |
| Evidence quality | Each run has URL, workflowName, headSha equal to final HEAD, status `completed`, conclusion `success`. |
| No false release claim | Container run uses `push_image=false`; no GHCR digest/attestation claim is made. |
| No stale evidence | No commit is made after dispatch evidence is collected. |
| Failure honesty | Missing/running/failed/cancelled workflows are reported as pending/blocked/failed, not passed. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh --phase decompose` | Pass before commit. |
| Placeholder scan | `rg -n "\\{\\{" governance/tasks/0107-measurement-infrastructure-current-remote-ci-evidence-refresh` | No output. |
| Remote run list | `gh run list --commit HEAD --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt,event` | Acceptance and Container runs visible. |
| Run detail | `gh run view <run-id> --json headSha,status,conclusion,url,workflowName,event` | headSha matches `git rev-parse HEAD`. |

# Review Gate
- Confirm no workflow is claimed passed before `status=completed` and `conclusion=success`.
- Confirm no run for an older SHA is used.
- Confirm no container publish/release digest claim is introduced.

# Runtime Verification Gate
Remote GitHub Actions evidence is required. Local validators only prove task package hygiene.

# Ship Readiness
Ship readiness for this slice means task package is committed/pushed and both remote workflow runs for final HEAD are completed successfully or the failure/pending state is truthfully reported.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Current HEAD and workflows inspected. |
| TP-01.02 | Existing run absence recorded before dispatch. |
| TP-02.01 | Acceptance workflow dispatched after task package push. |
| TP-02.02 | Container workflow dispatched after task package push with `push_image=false`. |
| TP-03.01 | Poll loop reaches terminal state or records timeout. |
| TP-03.02 | Run SHA/conclusion verified. |
| TP-04.01 | Task docs validator and placeholder scan pass. |
| TP-04.02 | Task package committed/pushed before dispatch, no post-evidence commit. |

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
