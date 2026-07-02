# Task-Level Acceptance
- `report.schema.json` 要求 `policyGate`，并声明 required fields、scope、excluded fields 和最小 gate invariants。
- `fate_core.capabilities.report_policy` 提供可单测的 forbidden claims scanner。
- capability API response 的 `report.policyGate.status` 正常输入为 `pass`，违规测试文本为 `fail`。
- `policyGate` 明确排除 `risk.forbiddenClaims`，不得因为风险清单本身含有禁止词而误报。
- 旧 capability response 字段 `data/evidence/risk/metadata/report.sections/report.evidenceRefs` 保持兼容。
- 文档必须说明这是最小 capability report envelope gate，不是完整 Markdown snapshot gate。

# Validation Plan
| 验证项 | 命令 | 目标 |
| --- | --- | --- |
| protocol tests | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy or report or capability'` | schema、helper、capability protocol。 |
| API tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'policy or report or capability or metadata or openapi'` | capability response 和 discovery。 |
| combined focused | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or report or capability or metadata or openapi'` | 组合回归。 |
| lint | `.venv/bin/ruff check ...` | 改动文件 lint。 |
| format | `.venv/bin/ruff format --check ...` | 格式不漂移。 |
| typecheck | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` | fate-core 类型检查。 |
| quick CI | `bash scripts/local-ci.sh --profile quick` | 仓库快速门禁。 |
| governance | `python3 governance/tools/validate_governance_package.py --project-root . --strict` | 治理包严格校验。 |
| diff check | `git diff --check` | 无空白错误。 |
| task docs | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | 任务文档闭环。 |

# Review Gate
- `policyGate.scope` 与 `contentCoverage` 不能夸大。
- `policyGate.excludedFields` 必须包含 `report.risk.forbiddenClaims` 或等价字段。
- `report.schema.json` 不得继续把 forbidden claims scanner 标成后续项。
- 测试必须覆盖正常 pass 和违规 fail。
- 文档必须说明外部连通验证不在本任务内。

# Runtime Verification Gate
- 本任务不启动线上服务。
- 本任务不访问真实 token、Bot、webhook、生产数据库、远程服务器。
- 外部连通验证待执行。

# Ship Readiness
- 所有 TODO 勾选。
- STATUS 写入真实命令和结果。
- closeout validators 通过。
- 未提交改动仍按用户后续命令统一控制版本。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-01.01 | policy scope 和排除字段在任务文档/schema 中可复核。 |
| TP-01.02 | report schema required fields 包含 `policyGate`。 |
| TP-02.01 | scanner helper 对违规文本返回 fail，对无违规文本返回 pass。 |
| TP-02.02 | capability API response 带 `report.policyGate`。 |
| TP-03.01 | targeted tests 覆盖 schema/helper/API。 |
| TP-03.02 | API 文档和路线图同步。 |
| TP-04.01 | 本地门禁命令通过或失败原因记录。 |
| TP-04.02 | 任务文档 closeout 无占位符。 |

# Anti-Goals
- 不得修改计算核心。
- 不得把本轮说成完整合规审查系统。
- 不得输出真实 token、生产路径或私密配置。
- 不得虚构验证结果。
