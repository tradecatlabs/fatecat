# Task-Level Acceptance

| Requirement | Evidence |
| --- | --- |
| Task package exists | `governance/tasks/0125-measurement-infrastructure-100-post-0124-live-readiness-plan/` |
| Research exists | `RESEARCH.md` maps official infrastructure sources to FateCat post-0124 state |
| Roadmap updated | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` section `6.20` |
| Task index updated | `governance/tasks/INDEX.md` row `0125` |
| No live overclaim | All real external live items remain `外部连通验证待执行` or explicitly blocked |

# Validation Plan

```bash
python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0125-measurement-infrastructure-100-post-0124-live-readiness-plan --phase closeout
rg -n "6\\.20|0125|MI-100\\.B\\.00|外部连通验证待执行" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/INDEX.md governance/tasks/0125-measurement-infrastructure-100-post-0124-live-readiness-plan
```

# Review Gate

- No sentence may claim production API/HF/Bot/webhook/OTel/OIDC/SIEM/Vault/KMS live passed.
- No raw token, URL, DSN, webhook secret or report body may be added.
- Next task must be executable without pretending external credentials exist.

# Runtime Verification Gate

No runtime is introduced. Verification is task-doc validation, roadmap/index text checks and secret scan only.

# Ship Readiness

Ready when task docs validate, roadmap/index are updated, local secret scan is clean, and git delivery flow records commit/push evidence.

# Task Package Acceptance

## TP-01 Current State

Accepted when 0124 final status and remote CI evidence are recorded.

## TP-02 Research

Accepted when official infrastructure source mapping is captured in `RESEARCH.md`.

## TP-03 Roadmap

Accepted when roadmap section `6.20` contains resource matrix, task tree and recommended next slice.

## TP-04 Validation

Accepted when task docs validate and no-overclaim text checks pass.

# Anti-Goals

- Do not execute production live checks in this task.
- Do not save secrets, raw endpoints, DSNs, chat IDs or report bodies.
- Do not claim 100% measurement infrastructure completion.
