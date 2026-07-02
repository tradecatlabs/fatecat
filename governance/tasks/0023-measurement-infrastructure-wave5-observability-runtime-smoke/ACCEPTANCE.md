# Task-Level Acceptance
- `bash scripts/observability-smoke.sh --output-json /tmp/fatecat-observability-smoke.json` 通过并输出 JSON。
- JSON 覆盖 health、ready、metrics、request-id、structured http_request log 和 registry metadata。
- registry metadata 暴露 `smokeCommand`、`smokeOutput` 和 `smokeScope`。
- quick CI 包含 `test_observability_smoke.py`。
- 文档和 roadmap 区分本地 smoke 与未完成的 collector/dashboard/SLO/alert。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/observability/registry.json >/dev/null` |
| smoke CLI | `bash scripts/observability-smoke.sh --output-json /tmp/fatecat-observability-smoke.json && python3 -m json.tool /tmp/fatecat-observability-smoke.json >/dev/null` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_observability_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'observability or smoke'` |
| ruff | `.venv/bin/ruff check scripts/observability-smoke.py tests/regression/test_observability_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| format | `.venv/bin/ruff format --check scripts/observability-smoke.py tests/regression/test_observability_smoke.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

# Review Gate
- smoke 输出不得包含真实日志正文、请求体、用户输入、token、secret、DSN 或报告正文。
- 文档不得写成 OpenTelemetry、SLO、alert、dashboard 或生产监控已完成。
- registry 中 planned signals 仍保持 planned。

# Runtime Verification Gate
- smoke CLI 至少返回 15 个 passed checks。
- focused tests 和 quick CI 必须通过。

# Ship Readiness
- 当前任务完成后可声明：available observability signals 具备本地 smoke。
- 不可声明：provider/report trace、SLO、alert、collector、dashboard 和生产监控平台完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 缺口和边界已落盘。 |
| TP-02 | smoke 和 registry metadata 已实现。 |
| TP-03 | tests/docs/quick CI 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不得接入外部 collector 或真实生产流量。
- 不得保存真实日志或用户数据。
- 不得把 TestClient smoke 当成公网生产验证。
