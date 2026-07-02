# Task-Level Acceptance
- `contracts/fate/evaluations/registry.json` 存在，至少登记 3 类资源：golden Dataset、benchmark Dataset、EvaluationRun。
- Dataset 条目必须声明 `usageRole`、`localAvailability`、`privacyClass`、`sourceRef`、`paths`、`commands` 和风险说明。
- EvaluationRun 条目必须声明 `datasetIds`、`commands`、`gateType`、`releaseRequired`、`lastKnownStatusPolicy` 和 links。
- `/evaluations` 与 `/api/v1/evaluations` 返回同一 payload。
- `/evaluations/{evaluation_id}` 与 `/api/v1/evaluations/{evaluation_id}` 返回单个资源详情。
- `/metadata` 与 OpenAPI 暴露 evaluation 入口。
- 文档明确：MingLi-Bench 是 evaluation_only/offline runner，不是生产测算输入。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 任务文档 decompose | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase decompose` |
| 契约测试 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset or resource'` |
| API 测试 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'evaluation or metadata or openapi'` |
| Python lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| Python format | `.venv/bin/ruff format --check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| type check | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| closeout docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase closeout` |
| task tree | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` |

# Review Gate
- `future-optimal-drift`：本轮必须通向“评测资源化”，不能退化成在文档里写一段说明。
- `ponytail-complexity`：不引入数据库、队列、dashboard 或外部 API。
- `document-drift`：新增 API、schema、目录和路线图必须同步。
- `security/privacy`：不得输出真实密钥、真实用户隐私样例或 benchmark 标准答案细节。

# Runtime Verification Gate
本任务只验证本地资源发现和契约，不执行外部连通。真实外部模型评测、线上 CI、生产域名和 Bot live smoke 均标记为“外部连通验证待执行”。

# Ship Readiness
- 无非法占位符残留。
- 工作树允许仍包含 0009-0017 未提交切片，但 0017 证据必须自洽。
- focused pytest、ruff、format、mypy、quick CI、task validators 通过。
- `STATUS.md` 记录真实执行命令和结果。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-01 | 任务边界、风险、终态、kill list 和最小验证已写入任务文档。 |
| TP-02 | Dataset/EvaluationRun/schema fields 有机器契约和测试断言。 |
| TP-03 | registry 覆盖关键 golden、benchmark 和 evaluation run，并能被测试读取。 |
| TP-04 | API 和 metadata/OpenAPI 暴露 evaluation 入口。 |
| TP-05 | 文档与路线图同步，测试覆盖新增契约。 |
| TP-06 | 本地门禁和 closeout 完成。 |

# Anti-Goals
- 不得只修改 `governance/tasks/` 而不落契约/API；本任务目标是可用资源发现层。
- 不得虚构证据
- 不得越权补全未确认信息
