# Task-Level Acceptance

- Assembler exists and can emit pending evidence without external credentials.
- Assembler can emit external-live evidence only with explicit ack and complete proof refs.
- Generated live evidence is accepted by `multi-replica-runtime-gate`.
- Generated fake/secret/overclaim evidence is rejected before or by the gate.
- Quick local-ci records an assembler artifact without claiming live passed.
- Docs and task closeout keep `外部连通验证待执行` for real multi-replica runtime.

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Shell/Python syntax | `python3 -m py_compile scripts/multi-replica-runtime-evidence-assembler.py scripts/multi-replica-runtime-gate.py` and `bash -n scripts/multi-replica-runtime-evidence-assembler.sh scripts/local-ci.sh` | exit 0 |
| Pending assembler | `bash scripts/multi-replica-runtime-evidence-assembler.sh --pending --output-json /tmp/fatecat-multi-replica-runtime-evidence-pending.json` | status `external_connectivity_pending` |
| Live fixture assembler | assembler with redacted proof refs and `--ack-external-live` | output accepted by gate |
| Gate reuse | `bash scripts/multi-replica-runtime-gate.sh --evidence-json <assembler-output>` | exit 0 for valid fixture |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_multi_replica_runtime_evidence_assembler.py tests/regression/test_multi_replica_runtime_gate.py tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py` | exit 0 |
| Ruff | focused `ruff check` and `ruff format --check` | exit 0 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0081.json` | exit 0 |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0081` | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| Syntax | passed: `python3 -m py_compile scripts/multi-replica-runtime-evidence-assembler.py scripts/multi-replica-runtime-gate.py`; `bash -n scripts/multi-replica-runtime-evidence-assembler.sh scripts/local-ci.sh` |
| Pending assembler | passed: output status `external_connectivity_pending` |
| Gate reuse | passed: pending evidence accepted by `multi-replica-runtime-gate`; live fixture accepted with `liveEvidenceStatus=external_live_passed` |
| Focused pytest | passed: `40 passed` |
| Ruff | passed: focused `ruff check`; format check passed after formatting assembler |
| Secret scan | passed in quick CI: `findingCount=0` |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0081`, focused regression `231 passed` |

# Review Gate

- evidence-integrity: generated live evidence must pass 0080 gate.
- security/privacy: no sensitive values in assembler output.
- future-optimal-drift: assembler must lead toward real live evidence generation, not another static plan.
- ponytail-complexity: no new dependency or duplicated gate logic.
- document-drift: roadmap/docs/AGENTS/local-ci must agree on non-claim boundary.

# Runtime Verification Gate

- Default/pending mode must not require credentials or external services.
- External live mode must require explicit operator ack.
- Any forbidden proof fragment, sensitive assignment, raw URL, or exactly-once overclaim must fail.
- Assembler output must be consumable by `multi-replica-runtime-gate`.

# Ship Readiness

- All TODO leaves complete.
- Worktree cleanliness is verified by the outer git delivery flow after commit.
- Remote CI evidence is reported from the actual post-push GitHub Actions run, not pre-claimed by this task snapshot.
- No document states real multi-replica live passed.

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 0080 roadmap/contract/gate gap verified. |
| TP-01.02 | pending/live/non-claim boundary documented. |
| TP-02.01 | CLI/schema produces 0080-compatible evidence. |
| TP-02.02 | fake/secret/overclaim cases rejected. |
| TP-03.01 | assembler Python and shell wrapper added. |
| TP-03.02 | local-ci, AGENTS and docs linked. |
| TP-04.01 | regression tests cover pending, live fixture, missing ack and secret rejection. |
| TP-04.02 | focused gates and quick CI pass. |
| TP-05.01 | closeout docs complete without overclaim. |
| TP-05.02 | task snapshot records that git push and remote CI evidence belong to the outer delivery flow after commit exists. |

# Anti-Goals

- 不运行真实 24h 多副本 soak。
- 不连接真实 Postgres、webhook receiver、Vault/KMS 或 metrics backend。
- 不声明 exactly-once、production ready 或 external live passed。
- 不输出真实 secret、token、DSN、URL、报告正文或用户输入。

# Live Evidence

外部连通验证待执行。需要真实多副本环境、公网 webhook receiver、external secret provider、metrics backend 和 24h/100 jobs evidence 后，才允许用 external live mode 生成 evidence 并交给 gate。
