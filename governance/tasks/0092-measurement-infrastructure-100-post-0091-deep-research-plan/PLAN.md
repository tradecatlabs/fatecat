# Planning Summary
0092 的目标是把 FateCat “100% 测算基础设施”从 Post-0091 状态重新校准：0091 已完成本地 retention cleanup baseline，并且 `44cbedd` 的远端 Acceptance/Container workflow 均已通过。当前真正缺口不再是“有没有路线图”，而是把剩余外部 live 证据、本地可执行交付面缺口、八字/紫微质量扩容、生产安全/观测/运行闭环排成不可伪造的实施顺序。本任务只做调研和计划落盘，不改业务代码。

# Lifecycle Gates
禁止跳过任何 gate；如果某个 gate 失败，0092 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 planning-only，不实现业务代码 | Done |
| RESEARCH | 外部资料使用官方/一手资料链接 | Done |
| PLAN | 100% 资源域、任务树、执行顺序、失败判定落盘 | Done |
| BUILD | 只更新主路线图和任务文档 | Done |
| TEST | 任务文档 decompose validator 与占位符检查通过 | Done |
| REVIEW | 不把 0091、本地 smoke、dry-run 或 contract 写成 live passed | Done |
| SHIP | 可进入后续 commit/push；本任务不自动声明生产 ready | Done |

# Future-Optimal Contract

- target end state: FateCat 是可被 Agent 与应用开发者接入的测算基础设施，所有 capability/provider/job/event/report/evidence/evaluation/security/observability/release/audit 都是可发现、可执行、可恢复、可观测、可评测、可审计、可回滚的资源。
- real constraints: 真实 Bot token、公网 webhook、生产数据库、IdP、SIEM、OTel backend、Vault/KMS、第三方审计权限和长期多副本运行都依赖外部环境。
- inertia constraints: 历史路线图多轮追加，容易把“已建 gate”误读为“live passed”；0092 只追加 Post-0091 最新章节，不删除历史证据。
- kill list: 功能堆叠、dry-run 伪装 live、retention local cleanup 伪装生产 scheduler、single smoke 伪装长期生产、多副本 evidence gate 伪装 exactly-once。
- proof point: 后续任务可以直接按 0.11 队列创建 0093+ 任务包。
- falsifier: 实现者无法从 0.11 判断下一步做什么、需要什么证据、哪些不能伪造成完成。
- migration slice: 从 Post-0091 planning 进入 CLI capability command、CLI/Skill semantic diff、core corpus/report diff、Postgres cleanup live gate、external live evidence pack。
- rejected short-term patches: 不新建平行 roadmap，不先堆新术数模块，不用聊天记录替代任务文档，不把外部待验证项写成已完成。

# Ponytail Contract

- existence check: 用户明确要求深度调研并制作实现 100% 基础设施完整计划；0091 后路线图需要最新可执行顺序。
- selected ladder rung: 复用既有主路线图和 `governance/tasks` 任务容器，不新增另一套路线图系统。
- skipped scope: 不实现 code slice，不接真实外部平台，不创建 SDK 包，不做发布操作。
- ceiling / upgrade path: 本计划只能指导后续任务；100% 结论必须由后续真实证据关闭。
- do-not-simplify: 外部 live、OIDC/SIEM/OTel/Vault/KMS、Bot token、生产 retention scheduler、Postgres production cleanup、exactly-once、长期多副本运行不得被本地 smoke 替代。
- minimal runnable check: `validate_task_docs.py --phase decompose` 和无占位符检查。
- complexity review owner: `auto-review` 的 document-drift / future-optimal-drift / ponytail-complexity。

# Document-Driven Contract

- Operating model update: not needed；项目定位未变，只刷新 100% 实现计划。
- Toolchain model update: not needed；未新增命令或工具链。
- Process update: not needed；仍按 `auto-tasks` 任务容器和路线图执行。
- Source-of-truth updates: updated；主路线图追加 Post-0091 最新计划，本任务目录保存调研证据。
- Local README/AGENTS impact: not needed；未改变目录职责或架构边界。
- Contract/catalog/schema impact: not needed；planning-only，不改 contract。
- ADR/Gate/module-context impact: not needed；未改变长期架构决策。
- Documentation exemption reason: 无。
- Validation evidence: task docs decompose validator、grep 无占位符。

# Simplest Path
复用 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 作为主路线图，追加 `0.11` 最新执行计划；在 `governance/tasks/0092-.../RESEARCH.md` 保存 source matrix 与推导。这样不会产生第二份互相冲突的计划。

# Split Strategy
1. 先复核当前仓库事实和 0091/远端 CI 交付边界。
2. 再从成熟基础设施领域提炼同构能力，不从“继续堆术数模块”出发。
3. 把 100% 拆成资源域、实现任务、外部阻断项和失败判定。
4. 最后只落文档和任务树，后续代码实现另建任务。

# Execution Waves
| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01, TP-01.02 | 仓库事实与既有路线图复核 | Done |
| 2 | TP-02.01, TP-02.02 | 外部同构资料调研和抽象 | Done |
| 3 | TP-03.01, TP-03.02, TP-03.03 | 形成 Post-0091 100% 实现计划 | Done |
| 4 | TP-04.01, TP-04.02, TP-04.03 | 落盘和校验 | Done |

# Runtime Workflow Contract
| Field | Value |
| --- | --- |
| allowed tools | `git status`、`git log`、`gh run list`、`rg`、`sed`、web research、`validate_task_docs.py` |
| forbidden actions | 不切分支、不删除业务文件、不改业务代码、不伪造 live evidence、不读取或输出真实 secret |
| required evidence | Git/worktree 状态、0091 任务状态、远端 CI、主路线图、官方资料链接、任务文档校验 |
| stop condition | 需要真实 token、公网 endpoint、生产账号或外部平台权限时，标记 `外部连通验证待执行` |

# Next Executable Leaves
None. 0092 是 planning-only 任务，已完成。下一步建议创建 0093 执行 `CLI capability command baseline`，因为它是本地可完成的多端交付缺口；若用户提供真实外部凭证，则可优先执行对应 live evidence 任务。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-04.03
```

# Rollback Protocol
- 恢复 `governance/tasks/INDEX.md` 的 0092 行。
- 删除或恢复 `governance/tasks/0092-measurement-infrastructure-100-post-0091-deep-research-plan/` 的 planning 文档。
- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 中新增 `0.11` 章节。
- 不影响 0091 已完成的 retention cleanup baseline 资产。
