# Repo Evidence
- 当前分支开始时：`main`，`git status --short --branch` 为 `## main...origin/main`。
- 当前基线提交：`dcbff4e feat: establish measurement capability infrastructure`。
- 上一阶段已完成 `/capabilities`、`/reports`、`/metadata` 和 capability maturity/testGate 字段，但 registry 准入规则仍可继续硬化。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不新增业务体系 | 本轮只做协议、API discovery、文档、测试和门禁 |
| 默认报告不可污染 | `bazi` 仍是唯一 `default` 和唯一 `markdownDefault=true` |
| planned 能力不可执行 | registry 和 executor 双层拒绝 |
| 真实生产外部依赖 | 标为“外部连通验证待执行” |
| 根目录卫生 | 新文档进入 `docs/reference-materials/operations/`，任务进入 `governance/tasks/` |

# Change Boundary
- 可改：`contracts/fate/capabilities/`、`domains/*/capabilities/`、`domains/*/main.py`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0008-*`。
- 不改：预测算法核心结论、默认 Markdown 结构、生产 secret、远端部署配置。

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| registry 规则过严导致服务 ready 失败 | 中 | 定向 pytest 覆盖现有 registry 全量能力 |
| metadata 新字段破坏旧客户端 | 低 | 只增字段，不改旧字段 |
| 文档宣称超过事实 | 中 | 明确外部连通验证待执行 |
| task 文档漂移 | 中 | closeout 前跑 task validator |

# Assumptions and Falsification
- 假设：当前基础设施下一步应优先补“可接入、可拒绝、可审计”，而不是新增预测模块。
- 证伪方式：若 quick CI、API contract 或 registry tests 失败，则本假设实现不成立，需回滚或收窄。

# Critical Ambiguities
- 真实 API 域名、真实 token、Bot live smoke 未在本地提供，属于后续生产实测。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bug 调试任务；所有结论必须来自 pytest、ruff、mypy、quick CI、governance/task validators 或 git 状态。

# Task Package Context Map
- `contracts/fate/capabilities/registry.json`：capability 真相源。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/registry.py`：registry 读取和准入校验。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`：FastAPI 对外入口。
- `tests/regression/test_capability_protocol.py`：协议与准入回归。
- `tests/regression/test_api_contracts.py`：API discovery 与能力入口回归。
