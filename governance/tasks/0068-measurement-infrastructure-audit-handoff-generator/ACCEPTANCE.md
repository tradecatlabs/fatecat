# Acceptance

## Task-Level Acceptance

- `contracts/fate/audit/handoff.json` exists and defines required outputs, Markdown sections and pending external validation policy.
- `bash scripts/audit-handoff.sh --output-dir <dir>` writes `audit-handoff.json` and `AUDIT_HANDOFF.md`.
- JSON output includes every tracked and untracked non-ignored occurrence of `外部连通验证待执行` with path, line and excerpt.
- Markdown output includes Latest Status, Delivery Evidence, Code And Asset Index, Pending External Validations, Risk Register, Verification and Final Conclusion sections.
- `scripts/local-ci.sh --profile quick` runs audit handoff and records `auditHandoff` artifact path.
- 回归测试覆盖 generator 输出、pending count、敏感 assignment 防护和 local-ci 接线。

## Task Package Acceptance

| Task Package | Acceptance |
| --- | --- |
| TP-01.01 | Existing closeout/release gate/local-ci/roadmap/pending facts are documented. |
| TP-02.01 | Audit handoff contract is present and declares pending external validation policy. |
| TP-02.02 | Generator writes Markdown and JSON bundle. |
| TP-03.01 | Regression test proves pendingExternalValidationCount equals tracked + untracked non-ignored occurrence count. |
| TP-03.02 | local-ci writes audit handoff artifact and AGENTS describe the script. |
| TP-03.03 | Roadmap records 0068 baseline without overclaiming live evidence. |
| TP-04.01 | Focused validation and secret scan pass. |
| TP-04.02 | quick local-ci and task validators pass before commit/push. |

## Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/audit/handoff.json` | valid JSON |
| Generator | `bash scripts/audit-handoff.sh --output-dir /tmp/fatecat-audit-handoff-0068` | status passed |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_audit_handoff.py` | passed |
| Lint/format | `.venv/bin/python -m ruff check scripts/audit-handoff.py tests/regression/test_audit_handoff.py` and format check | passed |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0068.json` | passed |
| Task validators | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | passed |
| Quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0068` | passed |

# Review Gate

- BLOCK if pendingExternalValidationCount is lower than tracked + untracked non-ignored occurrence count.
- BLOCK if bundle contains `token=`, `secret=`, `password=`, `passwd=` or `private_key=`.
- BLOCK if bundle states production API/Bot/OIDC/SIEM/monitoring/developer portal live is complete without external evidence.
- WARN if remote acceptance is not queried during local generator use; local-ci and GitHub run will cover ship evidence separately.

# Runtime Verification Gate

- Generator output must include `kind=fatecat.audit_handoff_bundle`.
- JSON and Markdown paths must be written to the chosen output directory.
- local-ci quick summary must expose `artifacts.auditHandoff`.
- The bundle conclusion must keep 100% production/live claims blocked until external evidence exists.

# Ship Readiness

- Local focused validation: passed.
- quick local-ci: passed at `/tmp/fatecat-local-ci-0068/summary.json`.
- Commit/push: handled by Git delivery step after task closeout.
- Remote CI current commit: handled by Git delivery step after push.

# Anti-Goals

- 不得替代第三方人工审计。
- 不得补写虚假的外部 live evidence。
- 不得把 local-ci 或 contract baseline 写成 100% production live 证明。
