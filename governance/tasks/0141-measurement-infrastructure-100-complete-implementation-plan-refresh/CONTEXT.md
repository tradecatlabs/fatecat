# Repo Evidence

| Evidence | Result | Meaning |
| --- | --- | --- |
| `git status --short --branch` | `## main...origin/main` | 任务开始时本地分支干净且与远端同步。 |
| `governance/tasks/0140-measurement-infrastructure-independent-audit-result-intake/README.md` | `Status: Done` | 独立审计结果 intake gate 已落地，但只处理审计结果结构，不关闭外部 live/certification。 |
| `governance/tasks/INDEX.md` | 0138 `Blocked`，0140 `Done`，0141 `In Progress` | 当前真实阻断仍是外部 proof/live 证据；本任务是计划刷新。 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 已有 post-0138 路线和总验收清单 | 需要基于 post-0140 状态补一版更凝练的完整实现计划。 |
| `docs/reference-materials/roadmap/测算基础设施需求文档.md` | 已定义测算基础设施资源模型和需求 | 本任务不改定位，只细化 100% 实施顺序。 |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 只允许分析当前分支和当前 worktree | 不切分支、不 rebase、不改历史。 |
| 外部连通证据不可伪造 | 生产 API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS/第三方审计全部保留为外部待验证。 |
| 本任务是规划切片 | 不改业务代码，不新增运行时脚本，不变更 API 行为。 |
| 需要使用成熟基础设施同构视角 | 资料来源优先使用官方文档或事实标准文档。 |
| 任务包必须可校验 | 回填所有占位符，运行 `validate_task_docs.py`。 |

# Change Boundary

Allowed:

- `governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh/*`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Forbidden:

- `domains/`、`apps/`、`contracts/`、`scripts/`、`.github/` 运行时或 CI 行为变更。
- 真实外部服务调用、凭证读取、生产部署或第三方审计提交。

# Risk Matrix

| Risk | Impact | Control |
| --- | --- | --- |
| 把 100% 写成已经完成 | 审计结论失真 | 所有外部项写明 `外部连通验证待执行` 或 blocked。 |
| 重复已有路线图导致噪声 | 后续执行者难以判断优先级 | `RESEARCH.md` 聚合完整计划，主路线图只追加摘要。 |
| 外部资料泛泛引用 | 计划缺少基础设施依据 | 资料矩阵只使用官方/事实标准来源并映射到 FateCat 资源。 |
| 计划过度扩张成新功能堆叠 | 偏离基础设施目标 | 任务树按资源和门禁组织，不按玄学模块数量组织。 |

# Assumptions and Falsification

| Assumption | Falsifier |
| --- | --- |
| 100% 是基础设施成熟度，不是预测准确率 100% | 若用户要求“预测准度百分百”，则目标需要重新定义为不可能承诺的命中率问题。 |
| 当前最硬阻断仍是外部 live/proof/ref/audit | 若外部 operator 已提交真实 proof/live/audit evidence，必须先重新跑对应 gate，再刷新计划。 |
| 后续本地可推进的最大价值是核心质量和开发者平台证据 | 若生产凭证可用，应优先执行 0138/生产 live，而不是继续本地规划。 |

# Critical Ambiguities

- 真实生产域名、Bot token、HF Space、OIDC/SIEM/OTel/Vault/KMS 权限当前未在仓库内提供。
- 第三方审计人员、审计标准和签名结果当前没有真实外部材料。
- 八字/紫微“专业质量”需要人审或外部 benchmark 才能超过工程回归级别。

# Debug Evidence Contract

- 调试模式: Optional

Not required. This is a planning and task package refresh, not a defect root-cause task.

# Task Package Context Map

| Context | Path |
| --- | --- |
| Main roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Requirements document | `docs/reference-materials/roadmap/测算基础设施需求文档.md` |
| Previous deep research plan | `governance/tasks/0136-measurement-infrastructure-100-post-0135-deep-research-plan/RESEARCH.md` |
| Independent audit intake | `governance/tasks/0140-measurement-infrastructure-independent-audit-result-intake/` |
| Current task research | `governance/tasks/0141-measurement-infrastructure-100-complete-implementation-plan-refresh/RESEARCH.md` |

## TP-01 current worktree and task baseline

核查 `git status --short --branch`、0140 任务包、任务索引和现有路线图，确认本任务的当前证据基线。

## TP-02 external infrastructure research refresh

对照官方基础设施资料，把成熟 infra 的共同构件映射为 FateCat 的测算基础设施资源和门禁。

## TP-03 100% admission model and resource matrix

定义 capability maturity 与 infrastructure maturity 双轴模型，并列出所有资源域到 100% 的缺口。

## TP-04 complete implementation task tree

把 100% 目标拆成 MI-100 任务树、执行波次、后续任务和外部阻断项。

## TP-05 roadmap/task package landing

把 0141 任务包和主路线图同步到同一口径。

## TP-06 validation and no-overclaim review

执行任务文档校验、占位符扫描和 no-overclaim 扫描，确认计划没有伪造完成。
