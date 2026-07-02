# Task-Level Acceptance
- `contracts/fate/observability/registry.json` 存在，至少登记 health、ready、metrics、structured logs、request trace id 和 planned provider/report spans。
- ObservabilitySignal 条目必须声明 `signalType`、`status`、`endpoint`/`fields`、`privacyBoundary`、`localVerification`、`externalConnectivity` 和 links。
- `/observability` 与 `/api/v1/observability` 返回同一 payload。
- `/observability/{signal_id}` 与 `/api/v1/observability/{signal_id}` 返回单个 signal 详情。
- `/metadata` 与 OpenAPI 暴露 observability 入口。
- 文档明确：本轮是发现层，不等于完整 OpenTelemetry、SLO 或生产监控已经上线。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 任务文档 decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0018-measurement-infrastructure-wave5-observability-resources --phase decompose` |
| 契约测试 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'observability or resource'` |
| API 测试 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'observability or metadata or openapi'` |
| Python lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| Python format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| type check | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| closeout docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0018-measurement-infrastructure-wave5-observability-resources --phase closeout` |
| task tree | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` |

# Review Gate
- `future-optimal-drift`：本轮必须通向可审计 observability 资源层，不能只在 metadata 写文本。
- `ponytail-complexity`：不引入 OpenTelemetry SDK、collector、dashboard 或 alerting。
- `document-drift`：新增 API、schema、目录和路线图必须同步。
- `security/privacy`：不得输出真实日志、token、secret、DSN 或用户隐私样例。

# Runtime Verification Gate
本任务只验证本地发现层和现有 metrics/log/requestId 口径，不执行外部监控连通。生产 SLO、alert rule、collector、dashboard 和 trace backend 均标记为“外部连通验证待执行”或 planned。

# Ship Readiness
- 无非法占位符残留。
- focused pytest、ruff、format、mypy、quick CI、task validators 通过。
- `/metrics` 现有指标兼容性不被破坏。
- `STATUS.md` 记录真实执行命令和结果。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-01 | 任务边界、风险、终态、kill list 和最小验证已写入任务文档。 |
| TP-02 | ObservabilitySignal schema、registry 和 resource schema 有机器契约和测试断言。 |
| TP-03 | API 和 metadata/OpenAPI 暴露 observability 入口。 |
| TP-04 | 文档与路线图同步，测试覆盖新增契约。 |
| TP-05 | 本地门禁和 closeout 完成。 |

# Anti-Goals
- 不得只修改 `governance/tasks/` 而不落契约/API；本任务目标是可用观测资源发现层。
- 不得虚构证据
- 不得越权补全未确认信息
