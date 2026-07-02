# Planning Summary
本任务把“100% 测算基础设施”从口号压成可执行蓝图：外部基础设施同构调研、当前仓库事实盘点、十个基础设施域、剩余任务树、下一批 `0028+` 任务和不可伪造证据口径。

# Lifecycle Gates
- SPEC：确认本任务只做调研与计划，不做功能实现。
- RESEARCH：使用官方文档建立外部同构矩阵。
- PLAN：刷新主路线图，给出 D0-D10 验收域和 MI-100 剩余任务树。
- BUILD：只执行文档/任务包落盘，不写业务代码。
- TEST：运行任务文档 closeout 验证、全任务树验证和 `git diff --check`。
- REVIEW：检查是否夸大本地/生产状态，是否把未验证项写成已完成。
- SHIP：任务文档无占位符，任务树验证通过。
- 不得跳过 gate。

# Simplest Path
复用已有 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 作为真相文档，不新增平行路线图；用 0027 任务包保存本轮调研证据和 closeout。

# Split Strategy
先外部调研，再仓库事实盘点，再重写主计划，最后回填任务包和验证。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 外部官方资料调研 |
| Wave 2 | TP-02 | 当前仓库事实盘点 |
| Wave 3 | TP-03 | 路线图重写 |
| Wave 4 | TP-04 | 任务包收口与验证 |

# Runtime Workflow Contract
- 本任务不启动服务，不运行生产 live smoke。
- 文档验证入口：`python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh --phase closeout`。
- 全任务树验证入口：`python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto`。

# Next Executable Leaves
- 后续首个实现叶子建议：`0028-measurement-infrastructure-rbac-policy`。
- 本任务自身无剩余叶子。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02
```

# Future-Optimal Contract
Target end state: FateCat 成为具备资源控制面、持久运行面、provider 生命周期、证据报告、评测、观测、安全、供应链、多端交付和生产发布门禁的测算基础设施。

Real constraints: 当前核心业务能力仍以八字/紫微为主；生产外部验证需要真实域名、token、Bot、监控/SIEM/身份系统权限；当前 worktree 未提交。

Inertia constraints: 旧报告服务路径、旧任务编号、已有文档表达、内存 job 和散落函数不能决定终态。

Kill list: “功能越多越接近基础设施”“本地能跑等于生产可用”“planned 能力可以混入默认报告”“没有证据也可宣称完成”。

Proof point: 主路线图已重写为 D0-D10 验收域、MI-100 剩余任务树和 `0028+` 顺序。

Falsifier: 如果后续任务无法从本文直接拆出可执行切片，说明计划仍不够基础设施化。

Migration slice: 本轮只刷新计划，后续从 RBAC、OpenAPI/Sandbox、durable job store 开始落地。

Rejected short-term patches: 不把 0028+ 功能混进本任务；不把外部 live smoke 伪造成已完成。

# Ponytail Contract
Existence check: 100% 目标已经跨越多个基础设施域，必须有单一完整计划承接，否则后续切片会失焦。

Selected ladder rung: 项目内文档和任务包；不新增工具、不新增 schema、不新增运行时代码。

Skipped scope: RBAC/OpenAPI/job store/webhook/OTel/OIDC/SIEM/生产 live smoke。

Ceiling / upgrade path: 当用户确认下一个实现切片时，按本文推荐顺序新建 `0028+` 任务。

Do-not-simplify: 不能删除外部验证、生产证据、安全隐私和供应链要求。

Minimal runnable check: 任务文档 closeout 验证和全任务树验证。

Complexity review owner: auto-review/document-drift/ponytail-complexity。

# Documentation Impact
Operating model update: not needed；项目定位未变，延续“测算基础设施”。

Toolchain model update: not needed；本任务未新增工具。

Process update: not needed；沿用 auto-tasks 任务包流程。

Source-of-truth updates: updated；`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已刷新。

Local README/AGENTS impact: not needed；未改变目录职责或执行入口。

Contract/catalog/schema impact: not needed；本任务不新增 contract。

ADR/Gate/module-context impact: not needed；本任务是计划刷新，不作架构决策落地。

Documentation exemption reason: 无需额外 README/AGENTS，因为未发生目录结构或模块边界变更。

Validation evidence: 见 `STATUS.md`。

# Rollback Protocol
- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 到本任务前版本。
- 恢复 `governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh/` 到初始化状态。
- 恢复 `governance/tasks/INDEX.md` 中 0027 状态。
- 不得影响其他任务目录。
