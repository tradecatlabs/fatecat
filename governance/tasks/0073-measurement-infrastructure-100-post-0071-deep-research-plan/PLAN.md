# Planning Summary

0073 的目标是把 FateCat “100% 测算基础设施”重新校准到 post-0072 状态：Postgres external backend 已有 adapter、live smoke baseline 和 outbox worker lease negative smoke baseline，但仍不能声明生产 durable runtime 完成。正确终态不是继续堆术数模块，而是让每个测算能力进入统一资源、控制面、运行时、证据、评测、可观测、安全、供应链、发布和审计闭环。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0073 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 planning-only，不实现业务代码 | Done |
| RESEARCH | 外部资料必须是一手/官方资料或明确链接 | Done |
| PLAN | 资源成熟度、任务树、执行顺序、验收口径落盘 | Done |
| BUILD | 只更新任务文档和主路线图 | Done |
| TEST | 任务文档 closeout validator 通过 | Done |
| REVIEW | 不把 0072、本地 baseline 或外部 pending 写成生产完成 | Done |
| SHIP | 本任务可提交；Git 交付由后续 auto-github 操作处理 | Pending |

# Future-Optimal Contract

- target end state: FateCat 是测算基础设施，所有能力都是可发现、可执行、可恢复、可观测、可评测、可审计、可回滚的资源。
- real constraints: 真实 Bot token、公网 webhook、生产数据库、IdP、SIEM、OTel backend、Vault/KMS、第三方审计权限均需要外部环境。
- inertia constraints: 已有路线图多轮追加，容易形成历史段落漂移；本轮追加 0.9 作为最新 living plan，不删除历史。
- kill list: 功能堆叠、局部 smoke 伪装生产、dry-run 伪装 live、outbox lease smoke 伪装 job execution worker lease、预测准确率 100% 口径。
- proof point: 0.9 可直接指导后续任务包创建。
- falsifier: 后续实现者无法从 0.9 判断下一步做什么、验收什么、不能伪造什么。
- migration slice: 下一步进入 job execution worker lease、public webhook live、external secret provider、OTel backend、OIDC/SIEM。

# Ponytail Contract

- existence check: 用户明确要求深度调研并制作完整计划；现有路线图需要 post-0072 口径刷新。
- selected ladder rung: 更新既有主路线图并新增 planning-only 任务包，不创建新平行路线图。
- skipped scope: 不实现代码，不接外部平台，不新增 capability。
- ceiling / upgrade path: 真实基础设施能力必须拆成后续 P0 任务包执行。
- minimal runnable check: task docs closeout validator。

# Simplest Path

复用现有主路线图 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`，新增 `0.9` 最新计划章节；在 0073 任务目录中保存 `RESEARCH.md` 作为调研证据。不新建第二份顶层 roadmap，避免事实源分裂。

# Split Strategy

- TP-01: 复核当前仓库事实和 0071/0072 状态。
- TP-02: 外部基础设施一手资料调研。
- TP-03: 映射 FateCat 100% 资源成熟度和任务树。
- TP-04: 落盘文档并校验。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01, TP-01.02 | 确认当前事实和约束 | Done |
| 2 | TP-02.01, TP-02.02 | 外部同构调研 | Done |
| 3 | TP-03.01, TP-03.02, TP-03.03 | 形成计划 | Done |
| 4 | TP-04.01, TP-04.02, TP-04.03 | 落盘和校验 | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `git status`、`rg`、`sed`、web research、`validate_task_docs.py` |
| forbidden actions | 不切分支、不删除文件、不改业务代码、不提交推送、不读取真实 secret、不声明外部 live 通过 |
| required evidence | Git 状态、任务索引、主路线图、外部资料链接、任务文档校验 |
| stop condition | 需要真实外部凭证或生产账号时，标记外部连通验证待执行 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| None | 0073 已完成。下一步应按 0.9 任务队列继续实现 job execution worker lease。 |

# Dependency Graph

```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-04.03
```

# Rollback Protocol

- 删除 `governance/tasks/0073-measurement-infrastructure-100-post-0071-deep-research-plan/`。
- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中 `0.9` 新增章节。
- 恢复 `governance/tasks/INDEX.md` 中 0073 行。
- 不影响 0072 已完成的 worker lease smoke 资产。
