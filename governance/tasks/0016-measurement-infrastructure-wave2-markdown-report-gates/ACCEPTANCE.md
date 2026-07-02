# Task-Level Acceptance
- 同步 `/api/v1/report/markdown` 成功响应必须包含 `policyGate` 和 `snapshotGate`。
- 标准异步 `/api/v1/report/jobs/{job_id}` 成功结果必须包含 `policyGate` 和 `snapshotGate`。
- Web 异步 `/api/v1/report/jobs/web` 成功结果必须包含 `policyGate` 和 `snapshotGate`。
- `policyGate` 必须扫描 `report.markdown` 正文，违规样本返回 fail。
- `snapshotGate` 必须解析 Markdown headings，bazi/ziwei 核心 heading 缺失时返回 fail。
- 旧字段 `reportSystem`、`markdown`、Web result input/workbench 不得删除。

# Validation Plan
| 验证项 | 命令 | 目标 |
| --- | --- | --- |
| protocol | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy or snapshot or report'` | helper 与 schema。 |
| API focused | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown or job or web'` | 三条 Markdown 路径。 |
| combined focused | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or snapshot or report or markdown or job or web'` | 组合回归。 |
| lint | `.venv/bin/ruff check ...` | 改动文件 lint。 |
| format | `.venv/bin/ruff format --check ...` | 格式稳定。 |
| typecheck | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` | fate-core 类型。 |
| quick CI | `bash scripts/local-ci.sh --profile quick` | 仓库快速门禁。 |
| governance | `python3 governance/tools/validate_governance_package.py --project-root . --strict` | 治理校验。 |
| task docs | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | 任务闭环。 |
| diff | `git diff --check` | 无空白错误。 |

# Review Gate
- 不允许只给同步 API 加 gate，异步和 Web 缺失。
- 不允许 `snapshotGate` 硬编码 pass。
- 不允许删除旧字段。
- 不允许把本轮说成完整 NLP 或人工合规审核。

# Runtime Verification Gate
- 本轮不验证外部生产域名、token、Bot、webhook。
- 外部连通验证待执行。

# Ship Readiness
- TODO 全部完成。
- STATUS 有真实命令证据。
- closeout validator 与全任务树 validator 通过。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-01.01 | scope 写明三条 Markdown 路径。 |
| TP-01.02 | schema 文档声明 Markdown gate。 |
| TP-02.01 | policy helper fail/pass 单测。 |
| TP-02.02 | snapshot helper heading pass/fail 单测。 |
| TP-03.01 | 同步 Markdown API 返回 gate。 |
| TP-03.02 | 标准异步 job 返回 gate。 |
| TP-03.03 | Web 异步 job 返回 gate。 |
| TP-04.01 | 回归测试覆盖三条路径。 |
| TP-04.02 | 文档路线图同步。 |
| TP-05.01 | 本地门禁通过。 |
| TP-05.02 | closeout 通过。 |

# Anti-Goals
- 不得修改命理计算核心。
- 不得改变 Markdown 文案。
- 不得虚构生产外部验证。
