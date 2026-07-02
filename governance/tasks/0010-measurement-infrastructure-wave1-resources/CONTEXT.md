# Repo Evidence
- 当前分支：`main`。
- 当前工作区已有 0009 计划文档与需求文档，未提交。
- Wave 1 来源：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 第 7 节最小首批切片。
- 现有能力契约目录：`contracts/fate/capabilities/schemas/`。
- 现有 API 入口：`domains/experience-delivery/services/fatecat-delivery/src/main.py`。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不改变算法 | 只改契约、API discovery、测试和文档 |
| 不污染默认报告 | 不改 report builder，不改 `bazi` 默认结构 |
| 复用现有目录 | 新 schema 放入 `contracts/fate/capabilities/schemas/` |
| 不伪造生产验证 | 外部 live smoke 不在本任务内 |
| 文档驱动 | API/contract 变化同步 README/AGENTS/roadmap/operations |

# Change Boundary
- 可改：`contracts/fate/capabilities/`、`domains/experience-delivery/.../main.py`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0010-*`。
- 不改：命理计算核心、数据库 schema、Bot 生产 token、CI workflow。

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| 详情 API 暴露字段不稳定 | 中 | tests 锁定 resourceType、schemas、links、admission |
| 错误码只写文档不进契约 | 中 | errors.json 作为 API 数据源 |
| 新 schema 无测试 | 中 | test_capability_protocol 覆盖 |
| 文档声明超过事实 | 中 | 100% 计划写明 Wave 1 进行中，剩余切片仍待做 |

# Assumptions and Falsification
- 假设：先补 resource schema、capability detail 和 error catalog 能有效提升基础设施可接入性。
- 证伪：如果 OpenAPI/API contract 无法稳定暴露这些资源，说明需要先重构 API 边界。

# Critical Ambiguities
- 标准错误响应是否立即带 `errorCode` 仍是后续切片；本轮先提供错误码发现资源。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务是新增功能切片，不是 bugfix；验证以 pytest、lint、typecheck、quick CI 和 task validators 为准。

# Task Package Context Map
- `contracts/fate/capabilities/schemas/resource.schema.json`：资源模型。
- `contracts/fate/capabilities/schemas/error.schema.json`：错误契约。
- `contracts/fate/capabilities/errors.json`：错误码字典。
- `main.py`：API discovery。
- `test_api_contracts.py`：API contract。
- `test_capability_protocol.py`：契约静态回归。
