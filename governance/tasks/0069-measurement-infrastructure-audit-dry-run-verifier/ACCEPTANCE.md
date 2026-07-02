# Acceptance

## Task-Level Acceptance

- `contracts/fate/audit/dry-run.json` exists and defines verifier inputs, outputs, checks, ship gate and non-claims.
- `bash scripts/audit-handoff-dry-run.sh --bundle-json <json> --bundle-markdown <md> --output-dir <dir>` writes `audit-dry-run.json` and `AUDIT_DRY_RUN.md`.
- Dry-run output includes `status=passed` for structurally valid handoff bundles and `shipGate.status=blocked` while external live validations remain pending.
- Verifier checks JSON required fields, Markdown required sections, pending validation count/list consistency, risk register, final conclusion blocking language and sensitive assignment patterns.
- `scripts/local-ci.sh --profile quick` runs audit handoff dry-run and records `auditDryRun` artifact path.
- 回归测试覆盖 verifier 输出、blocked ship gate 语义、敏感 assignment 防护和 local-ci 接线。

## Task Package Acceptance

| Task Package | Acceptance |
| --- | --- |
| TP-01.01 | 0068 handoff output and MI-100.10.04 gap are documented. |
| TP-02.01 | Audit dry-run contract is present and declares non-claim policy. |
| TP-02.02 | Verifier writes Markdown and JSON dry-run report. |
| TP-03.01 | Regression test proves valid handoff passes dry-run while ship gate remains blocked. |
| TP-03.02 | local-ci writes audit dry-run artifact and AGENTS describe the script. |
| TP-03.03 | Roadmap records 0069 baseline without overclaiming third-party audit completion. |
| TP-04.01 | Focused validation and secret scan pass. |
| TP-04.02 | quick local-ci and task validators pass before commit/push. |

## Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/audit/dry-run.json` | valid JSON |
| Handoff generator | `bash scripts/audit-handoff.sh --output-dir /tmp/fatecat-audit-dry-run-0069/handoff` | status passed |
| Dry-run verifier | `bash scripts/audit-handoff-dry-run.sh --bundle-json /tmp/fatecat-audit-dry-run-0069/handoff/audit-handoff.json --bundle-markdown /tmp/fatecat-audit-dry-run-0069/handoff/AUDIT_HANDOFF.md --output-dir /tmp/fatecat-audit-dry-run-0069/dry-run` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_audit_handoff.py tests/regression/test_audit_handoff_dry_run.py` | passed |
| Lint/format | `.venv/bin/python -m ruff check scripts/audit-handoff-dry-run.py tests/regression/test_audit_handoff_dry_run.py` and format check | passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0069.json` | passed |
| Task validators | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | passed |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0069` | passed |

# Review Gate

- BLOCK if dry-run passes without required JSON fields or Markdown sections.
- BLOCK if `pendingExternalValidationCount` differs from listed pending external validations.
- BLOCK if dry-run fails to report `shipGate.status=blocked` when pending external validations exist.
- BLOCK if bundle contains `token=`, `secret=`, `password=`, `passwd=` or `private_key=`.
- BLOCK if dry-run states third-party audit, production API, Bot, OIDC, SIEM, monitoring or developer portal live is complete without external evidence.

# Runtime Verification Gate

- Dry-run output must include `kind=fatecat.audit_handoff_dry_run`.
- JSON and Markdown paths must be written to the chosen output directory.
- local-ci quick summary must expose `artifacts.auditDryRun`.
- The dry-run conclusion must keep production/live/third-party audit claims blocked until external evidence exists.

# Ship Readiness

- Local focused validation: passed.
- quick local-ci: passed at `/tmp/fatecat-local-ci-0069/summary.json`.
- Commit/push: handled by Git delivery step after task closeout.
- Remote CI current commit: handled by Git delivery step after push.

# Anti-Goals

- 不得替代第三方人工审计。
- 不得补写虚假的外部 live evidence。
- 不得把 dry-run passed 写成 100% production live 证明。
