# Task-Level Acceptance
0150 is accepted when:

- It records current post-0149 facts: commit, remote Acceptance, local CI, certification blocked summary and remaining external blockers.
- It cites mature infrastructure source categories and maps them to FateCat requirements.
- It updates the roadmap with a post-0149 section that distinguishes completed local intake from missing external evidence.
- It provides a remaining task tree with explicit completion gates and failure predicates.
- It does not claim production live, expert review, external benchmark, independent audit or 100% certification completion.
- Task docs validate with `validate_task_docs.py --phase decompose`.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0150-measurement-infrastructure-100-post-0149-deep-research-plan --phase decompose` | `ok: true` |
| Roadmap section | `rg -n "Post-0149|6.40|canClaim100Percent=false|28717205411" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | required markers found |
| Certification baseline | `python3 scripts/measurement-infrastructure-certification.py --evidence-dir /tmp/fatecat-local-ci-0149-final --output-json /tmp/measurement-certification-0150-baseline.json` | `status=blocked`, `canClaim100Percent=false` |
| Diff hygiene | `git diff --check` | no whitespace errors |

# Review Gate
- PASS if the plan makes the remaining 100% blockers more precise and verifiable.
- WARN if it repeats older route maps without binding to 0149 evidence.
- BLOCK if it states or implies that real expert review, external benchmark, production live or certification is complete.

# Runtime Verification Gate
No runtime execution is in scope. Runtime truth remains delegated to existing gates:

- `external-validation-proof-ref-gate`
- `external-validation-live-proof-gate`
- `core-quality-human-review-gate`
- `live-release-gate`
- `current-release-proof`
- `current-audit-bundle`
- `measurement-infrastructure-certification`

# Ship Readiness
This planning slice can ship after task docs validation, roadmap marker check, certification baseline command, diff check, commit, push and remote Acceptance. It must still leave global 100% status active/blocked.

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | Current branch, commit, 0149, local CI and remote Acceptance facts recorded. |
| TP-01.02 | Official infrastructure source matrix recorded. |
| TP-02.01 | Certification blocked baseline summarized. |
| TP-02.02 | Missing evidence is grouped into explicit non-forgeable categories. |
| TP-03.01 | Remaining task tree covers external proof/live, core quality, release, audit and certification. |
| TP-03.02 | Next tasks are ordered without pretending external credentials are present. |
| TP-04.01 | Roadmap and task package updated. |
| TP-04.02 | Validation commands pass. |

# Anti-Goals
- 不执行真实外部 live。
- 不生成或伪造专家评审结论。
- 不把 external benchmark aggregate 写成已通过。
- 不把 certification blocked 改写成 100% 完成。
- 不新增 production 术数体系或修改默认报告范围。
