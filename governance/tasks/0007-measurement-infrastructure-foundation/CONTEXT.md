# Repo Evidence
- `git status --short --branch` 显示当前分支 `main...origin/main`，已有定位更新未提交。
- `bash scripts/local-ci.sh --profile quick` 已在定位更新后通过：58 passed，ruff/mypy/结构门禁通过。
- `governance_context_bundle.py --task-type governance` 曾提示缺少 `governance/processes/文档治理规则.md`，本任务补齐该流程文档。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不破坏现有 Web/API/Bot/Skill | 新增兼容入口，不删除旧 `/api/v1/*` 路径。 |
| 不让 planned 能力执行 | executor 必须在执行前检查 status。 |
| 不混入默认综合八字报告 | `defaultVisibility=default` 仍只能是 `bazi`。 |
| 复用成熟能力先于自写 | 只补协议、adapter 和路由胶水，不新造术数算法。 |
| 文档不能超过代码事实 | 路线图区分已实现、执行中和后续阶段。 |

# Change Boundary
- 文档：README、SKILL、AGENTS、reference docs、roadmap、governance task/process。
- 契约：`contracts/fate/capabilities/registry.json` 和 schemas。
- 运行时：`fate_core.capabilities` executor / registry / contracts；delivery API aliases。
- 测试：capability protocol、API contract、branding/Web regression。

# Risk Matrix
| 风险 | 缓解 |
| --- | --- |
| 协议字段新增导致 CLI/API 序列化不兼容 | 只新增字段，不删除既有字段；测试覆盖旧入口。 |
| executor 从硬编码分支改 provider map 后路由错误 | 用 bazi、ziwei、almanac、meihua focused tests 覆盖。 |
| 新 API 入口和旧入口结果分叉 | 新入口调用同一个 `CapabilityExecutor` 和 report job manager。 |
| 文档治理扩大范围 | 本任务只补缺失流程和本目标路线图。 |

# Assumptions and Falsification
- 假设：当前仓库已经具备 CapabilityExecutor、队列、metrics、ready 和 rate limit 基础，只需补基础设施契约缺口。
- 证伪：如果新 API 入口绕开 executor、planned 能力可执行、或 bazi 不再是唯一默认能力，则本任务失败。

# Critical Ambiguities
- 外部生产域名、真实 token、Bot live smoke 暂不在本任务内执行，标记为外部连通验证待执行。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix 主任务；若实现中出现回归，需记录失败命令、根因、修复和回归命令。

# Task Package Context Map
- `contracts/fate/capabilities/`：协议真相源。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/`：运行时协议边界。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`：API 交付入口。
- `tests/regression/test_capability_protocol.py`：协议回归。
- `tests/regression/test_api_contracts.py`：API 基础设施回归。
