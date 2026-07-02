# Repo Evidence

- `git status --short --branch` 显示当前分支为 `main...origin/main`，且存在 0072/0073 相关未提交改动。
- `governance/tasks/INDEX.md` 显示 0071 与 0072 为 `Done`。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已有 0.5、0.6、0.8 等多轮 100% 计划，本任务只做 post-0072 口径刷新。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 当前 worktree 不干净 | 不回滚、不覆盖 0072；只新增 0073 planning 文档和主路线图追加章节。 |
| 0072 只覆盖 outbox lease | 不把 worker lease smoke 写成 job execution worker lease、exactly-once 或生产完成。 |
| 外部生产凭证不可用 | Bot live、OIDC、SIEM、OTel backend、Vault/KMS、真实公网 webhook 统一标记外部连通验证待执行。 |
| 用户要求“深度调研” | 使用外部一手资料链接并形成同构映射。 |

# Change Boundary

- 修改 `governance/tasks/0073-measurement-infrastructure-100-post-0071-deep-research-plan/`。
- 修改 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 修改 `governance/tasks/INDEX.md` 中 0073 状态。
- 不修改业务代码、契约、脚本或测试。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 计划与 0072 范围冲突 | 审计误判 outbox lease 等于 job execution worker lease | 明确 0072 只证明 Postgres webhook outbox worker lease negative path。 |
| 100% 口径夸大 | 形成伪生产结论 | 100% 只按基础设施成熟度和证据闭环判定，不按功能数量或预测准确率。 |
| 外部资料泛泛引用 | 计划不可执行 | 每个资料映射到 FateCat 资源域、任务树和门禁。 |

# Assumptions and Falsification

- Assumption: 0071 代表当前已交付 Postgres migration/job live smoke baseline。
- Assumption: 0072 已完成 Postgres webhook outbox worker lease negative smoke，但不证明 job execution worker lease。
- Falsifier: 如果 0072 summary 或 tests 不能证明 duplicate claim、错误 owner release 和 lease expiry reclaim，则 0.9 计划不合格。
- Falsifier: 如果后续无法从 `0.9.5` 的下一任务队列直接创建任务包，则本计划不合格。

# Critical Ambiguities

- 真实生产部署平台、监控平台、IdP、SIEM、Vault/KMS 尚未指定。
- 是否采用 Postgres job execution worker 作为生产首选，还是引入 Temporal 作为长流程 orchestrator，后续需要以成本、复杂度、运行环境和恢复语义决定。

# Debug Evidence Contract

- 调试模式: Optional

本任务不是 bugfix。若文档校验或链接检查失败，记录失败命令、原因和修复路径；不得伪造校验通过。

# Task Package Context Map

| Artifact | Purpose |
| --- | --- |
| `RESEARCH.md` | 100% 基础设施深度调研和完整实现计划真相源 |
| `PLAN.md` | 任务生命周期、执行波次和回滚口径 |
| `ACCEPTANCE.md` | 验收和 anti-goal |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 项目级 living roadmap |

## TP-01 现状复核

- Context: 当前 Git 状态、任务索引、主路线图和 0071/0072 状态是本计划的输入事实。
- Boundary: 只读取事实，不回滚、不提交、不修 0072。

## TP-02 外部同构调研

- Context: 使用外部一手资料抽取基础设施共同结构。
- Boundary: 链接用于计划依据，不声明第三方系统已集成。

## TP-03 FateCat 100% 计划

- Context: 把调研映射成资源成熟度、任务树、执行顺序和验收门禁。
- Boundary: 计划不是实现完成。

## TP-04 文档落盘与验证

- Context: 0073 交付物是任务包、`RESEARCH.md` 和主路线图 `0.9`。
- Boundary: 单任务 closeout 校验不等于全仓任务树 clean，0072 仍有独立占位符和未收口状态。
