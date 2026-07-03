# Task-Level Acceptance
| 验收项 | 命令 / 证据 | 通过标准 |
| --- | --- | --- |
| JSON parse | `python3 -m json.tool contracts/fate/security/retention-production-cleanup-staged.json` | exit 0 |
| staged gate | `bash scripts/retention-production-cleanup-gate.sh --output-json /tmp/fatecat-retention-production-cleanup-0098.json` | passed，shipGate=blocked，negativeEvidenceRejected=3 |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_retention_production_cleanup_gate.py tests/regression/test_retention_cleanup.py tests/regression/test_production_security_gate.py` | 18 passed |
| ruff | `ruff check/format --check` on new script/test | pass |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0098.json` | findingCount=0 |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0098` | passed |
| task docs | `validate_task_docs.py --phase closeout` | exit 0 |

# Validation Plan
1. Parse JSON contracts.
2. Run retention production cleanup gate.
3. Run focused pytest.
4. Run ruff, secret scan and diff check.
5. Run quick local-ci because 0098 adds a new quick gate and regression file.
6. Run task closeout validator.

# Review Gate
- No external connection.
- No production delete.
- No live passed claim.
- No real DSN, endpoint, token, secret, user input, report body, production log or real deletion result.

# Runtime Verification Gate
- Required local gate: `bash scripts/retention-production-cleanup-gate.sh --output-json /tmp/fatecat-retention-production-cleanup-0098.json`。
- Required regression: focused pytest listed above.
- Required release slice proof: quick local-ci before commit.
- External live verification: not required for this task.

# Ship Readiness
- 0098 can ship only after TP-04.01 is Done.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Existing baseline reviewed. |
| TP-02.01 | staged contract exists and parses. |
| TP-02.02 | gate outputs blocked/pending by default and rejects fake evidence. |
| TP-03.01 | registry/policy/local-ci/docs wired. |
| TP-03.02 | regression covers default, redacted evidence and negative cases. |
| TP-04.01 | final validators pass. |

# Anti-Goals
- 不连接真实 Postgres/scheduler/SIEM。
- 不执行生产删除。
- 不声明 live passed。
