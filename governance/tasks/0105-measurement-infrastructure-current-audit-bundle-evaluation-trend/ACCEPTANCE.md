# Task-Level Acceptance
This task is accepted only if:
- current audit bundle evidence index contains `evidence.evaluation_trend_gate` when `--local-ci-output-dir` contains `evaluation-trend-gate-smoke/trend-gate.json`.
- The evidence item validates `kind=fatecat.evaluation_trend_gate`, `status=passed`, and empty `trendFindings`.
- Regression test fixture generates the trend gate artifact through the existing smoke script.
- Audit contract, AGENTS, roadmap, and task index are synchronized.
- No external live claim is introduced.

# Validation Plan
| Check | Command |
| --- | --- |
| Task docs decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0105-measurement-infrastructure-current-audit-bundle-evaluation-trend --phase decompose` |
| Focused current bundle tests | `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py tests/regression/test_evaluation_trend_gate.py` |
| Generate current bundle | `bash scripts/current-audit-bundle.sh --output-dir /tmp/fatecat-current-audit-0105/current-audit-bundle ... --local-ci-output-dir <dir>` |
| Ruff | `.venv/bin/ruff check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py && .venv/bin/ruff format --check scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py` |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0105.json` |
| Diff check | `git diff --check` |

# Review Gate
- Confirm the evidence item detail is summary-only.
- Confirm no full report, benchmark answer, stdout/stderr tail or secret is embedded.
- Confirm bundle remains blocked when external live proof is absent.

# Runtime Verification Gate
- Generated bundle must contain `evidence.evaluation_trend_gate` with `status=pass`.
- Required-mode behavior must not become easier due to the new evidence item.
- 0104 closeout validator remains passing after INDEX status fix.

# Ship Readiness
- Task docs closeout validator passes.
- Worktree diff is scoped.
- Commit/push evidence is recorded if version control is performed.

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | Gap and mapping are documented. |
| TP-02 | Implementation, tests, and docs are synchronized. |
| TP-03 | Validation and closeout evidence are recorded. |

# Anti-Goals
- 不得修改 production provider 算法
- 不得伪造外部 live、远端 CI 或第三方审计通过
- 不得保存完整报告正文、benchmark 标准答案、stdout/stderr tail、真实用户输入或凭证值
- 不得虚构证据
- 不得越权补全未确认信息
