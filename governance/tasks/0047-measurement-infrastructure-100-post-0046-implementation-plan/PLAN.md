# Planning Summary

本任务把“100% 测算基础设施”在 0046 之后重新收束为可执行实现计划：先确认当前 release clean/CI 事实，再用外部基础设施同构模型刷新剩余任务树，最后更新主路线图和任务索引。

# Lifecycle Gates

禁止跳过任何 gate；不得把规划刷新扩大解释为生产 100% 已完成。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 目标、边界、当前事实和不可伪造证据口径明确 | Done |
| RESEARCH | 外部一手资料映射为 FateCat 基础设施域 | Done |
| PLAN | 后 0046 剩余实现任务树刷新 | Done |
| BUILD | 只更新路线图、任务包和索引 | Done |
| TEST | Markdown whitespace、任务文档和 git diff 可复核 | Done |
| REVIEW | 不把 pending/live 外部验证写成完成 | Done |
| SHIP | 可提交、可推送、可交接 | Done |

# Simplest Path

复用 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 作为单一主路线图，不新建平行 roadmap；新增本任务包只承载本轮 post-0046 调研与落盘证据。

# Split Strategy

- TP-01：当前仓库与远端 CI 事实复核。
- TP-02：外部基础设施资料同构调研。
- TP-03：主路线图 post-0046 刷新。
- TP-04：任务包、索引和验证收口。

# Execution Waves

| Wave | Nodes | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01 | `git status`、当前 commit、远端 workflows | Done |
| 2 | TP-02.01 | 官方资料矩阵：API、control plane、runtime、provider、SRE、安全、供应链 | Done |
| 3 | TP-03.01 | 刷新剩余任务树与 100% 验收域 | Done |
| 4 | TP-04.01 | 校验和 closeout | Done |

# Next Executable Leaves

None. 0047 规划刷新已完成；下一批真实实现应从 `MI-NEXT-01` 创建新任务包。

# Future-Optimal Contract

Target end state: FateCat 成为面向 Agent 与应用开发者的测算基础设施：统一能力协议、资源化控制面、可恢复运行面、provider 生命周期、证据化报告、评测平台、可观测、安全合规、供应链证明、多端交付和生产发布门禁。

Real constraints: 真实 Bot token、registry、OIDC/IdP、SIEM、监控/告警平台、生产私有域名和法律意见需要外部权限；当前任务只能规划和记录，不伪造外部连通。

Inertia constraints: 旧编号建议、已完成 local baseline、单机 SQLite、内存 job、文档里“待做”的旧说法不能决定 100% 终态。

Kill list: “功能更多等于基础设施”“本地 gate 等于生产可用”“计划任务编号等于已经完成”“Bot dry-run 等于 live smoke”“源码能跑等于开发者平台”。

Proof point: 主路线图已把 post-0046 状态、剩余 `MI-NEXT-*` 任务树和不可伪造证据口径更新为当前事实。

Falsifier: 如果后续无法直接从 `MI-NEXT-*` 创建任务，或仍需要回到聊天记录解释验收标准，说明本任务未完成。

Migration slice: 本轮只刷新计划；下一步按 `MI-NEXT-01` 开始真实实现或外部 live 验证。

Rejected short-term patches: 不把 Telegram token 缺失写成通过；不把旧 CI 证据扩大成未来提交的证明；不把 registry attestation、OIDC/SIEM、OTel collector 用 contract 伪装为生产完成。

# Ponytail Contract

Existence check: post-0046 之后原路线图仍含过期状态和未来编号绑定，需要一个轻量任务包记录刷新依据。

Selected ladder rung: 项目内任务文档和主路线图更新；不新增 schema、脚本或业务代码。

Skipped scope: Telegram live、registry push/signature、OIDC/SIEM/monitoring live、durable runtime 二期、新 capability 实现。

Ceiling / upgrade path: 当用户确认下一项实现时，用 `MI-NEXT-*` 直接创建下一个真实任务包。

Do-not-simplify: 生产外部证据、供应链证明、安全隐私和运维 SLO 不能从 100% 验收中移除。

Minimal runnable check: Markdown whitespace、task docs validation、git status。

# Runtime Workflow Contract

- risk_level: low
- affected_flows: documentation, roadmap, task governance
- state_changes: task docs, roadmap, task index
- side_effects: none beyond local docs writes and external web research
- rollback: revert task 0047 directory, roadmap diff and task index row
- required_tests: `git diff --check`, task docs validation, optional full tasks tree validation

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01
```

# Rollback Protocol

- 删除本任务目录新增文件。
- 恢复 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 恢复 `governance/tasks/INDEX.md`。
- 不影响 0009-0046 历史任务证据。
