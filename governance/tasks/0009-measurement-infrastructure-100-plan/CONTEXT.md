# Repo Evidence
- 当前分支开始时：`main`，本地与 `origin/main` 同步。
- 工作区已有上一轮新增的 `docs/reference-materials/roadmap/测算基础设施需求文档.md` 与 `docs/reference-materials/README.md` 修改，属于用户要求的需求文档审阅资产，本任务继续复用并不覆盖。
- 已有路线图：`docs/reference-materials/roadmap/测算基础设施路线图.md`。
- 当前任务容器：`governance/tasks/0009-measurement-infrastructure-100-plan/`。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 用户要求 deep research | 使用官方资料并在计划文档列出来源 |
| 用户要求完整实现计划 | 输出 roadmap 文档，不只在聊天里总结 |
| 使用 auto-tasks | 创建并回填 0009 任务容器 |
| 不误导生产状态 | 所有未执行生产验证标为待执行 |
| 当前已有未提交需求文档 | 保留并纳入计划，不覆盖 |

# Change Boundary
- 可改：`docs/reference-materials/roadmap/`、`docs/reference-materials/README.md`、`governance/tasks/0009-*`、`governance/tasks/INDEX.md`。
- 不改：业务代码、API 行为、生产配置、secret、外部部署。

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| 计划过大不可执行 | 中 | 分成 IMP 主线、Wave 和最小首批切片 |
| 调研泛泛 | 中 | 只引用官方资料并映射到具体 FateCat 需求 |
| 把计划当完成 | 高 | 文档状态标 Draft，明确不代表已实现 |
| 与已有任务重复 | 中 | 0009 仅承载规划，后续执行另建任务 |

# Assumptions and Falsification
- 假设：测算基础设施 100% 的正确路径是先补资源模型、契约、执行生命周期、评测和观测，再扩新体系。
- 证伪：如果后续 Wave 1 无法在不破坏当前 bazi/ziwei 的情况下落地 schema/API/error/job 最小切片，则计划粒度需要重拆。

# Critical Ambiguities
- 真实生产域名、真实 token、Bot live smoke、私有部署权限未提供，本文只规划，不验证外部连通。
- OpenAI Evals 官方平台生命周期可能变化，本计划只借鉴“评测闭环”思想，不强绑定某单一平台。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务是规划任务，不是 bugfix；验证以文档存在、索引同步、任务文档校验和 whitespace 检查为准。

# Task Package Context Map
- Stripe：幂等请求、Webhook、测试模式。
- Twilio：错误码、消息状态回调。
- Plaid：Sandbox、Webhook。
- Kubernetes：声明式资源、controller、reconciliation。
- Terraform：provider、data source、state。
- Temporal：workflow、durable execution、retry。
- OpenTelemetry：traces、metrics、logs。
- OpenAI：structured outputs、evals。
