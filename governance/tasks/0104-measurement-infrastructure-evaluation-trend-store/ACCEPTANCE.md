# Task-Level Acceptance
This task is accepted only if:
- `trend-policy.json` exists and documents trend thresholds, privacy boundary and production boundary.
- `evaluation-trend-gate.py` fails latest failed summary, failed commands, consecutive failures and missing required run cases.
- Trend report never copies command output tails, benchmark answers, report bodies, real user input or secrets.
- `local-ci.sh --profile quick` includes trend smoke and focused regression.
- Evaluation registry metadata exposes `trendPolicy` and `trendCommand`.
- Post-0103 roadmap explains where quality trend store fits in the 100% infrastructure plan.

# Validation Plan
| Check | Command |
| --- | --- |
| Task docs decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0104-measurement-infrastructure-evaluation-trend-store --phase decompose` |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_evaluation_trend_gate.py tests/regression/test_evaluation_history_diff.py tests/regression/test_evaluation_dashboard.py` |
| Synthetic smoke | `bash scripts/evaluation-trend-gate-smoke.sh --output-dir /tmp/fatecat-evaluation-trend-gate-smoke-0104` |
| Real runner history + trend | `bash scripts/run-evaluations.sh --run-id run.evaluation_dashboard_smoke --record-history --history-dir /tmp/fatecat-evaluation-history-0104 --output-json /tmp/fatecat-evaluation-summary-0104.json` then `bash scripts/evaluation-trend-gate.sh --history-dir /tmp/fatecat-evaluation-history-0104 --output-json /tmp/fatecat-evaluation-trend-0104.json` |
| Lint/format | `.venv/bin/ruff check scripts/evaluation-trend-gate.py tests/regression/test_evaluation_trend_gate.py` and `.venv/bin/ruff format --check scripts/evaluation-trend-gate.py tests/regression/test_evaluation_trend_gate.py` |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0104.json` |
| Diff check | `git diff --check` |

# Review Gate
- Review privacy boundary: generated trend JSON must be summary-only.
- Review registry/local-ci wiring: no orphan script or doc-only policy.
- Review roadmap claims: do not write "100%" as complete; keep external live pending explicit.

# Runtime Verification Gate
- Synthetic smoke must output `{"status":"passed" ...}` or equivalent pretty JSON.
- Runner history plus trend gate must use actual `run.evaluation_dashboard_smoke` summary output, not only fixture.
- If quick local-ci is run, record its evidence path and status; if not run due time, mark explicitly.

# Ship Readiness
- Worktree diff must contain only scoped changes.
- Task docs closeout validator must pass before final report.
- Commit/push, if requested, must use clean staged diff and true git status evidence.

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | Policy and boundary are explicit and machine readable. |
| TP-02 | Gate, smoke, CI and registry wiring are implemented. |
| TP-03 | Tests and roadmap reflect trend store. |
| TP-04 | Validation evidence and closeout docs are complete. |

# Anti-Goals
- 不得修改生产 provider 算法
- 不得保存完整报告正文、benchmark 标准答案、真实用户输入或凭证值
- 不得虚构证据
- 不得越权补全未确认信息
