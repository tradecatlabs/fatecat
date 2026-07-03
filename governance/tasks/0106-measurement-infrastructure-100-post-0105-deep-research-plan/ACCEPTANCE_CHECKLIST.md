# Acceptance Checklist

# Global Standards
- [x] 只使用当前 branch/worktree 事实。
- [x] 引用外部资料时优先官方或事实标准来源。
- [x] 不把本地门禁、任务 closeout 或 blocked bundle 写成生产 live。
- [x] 远端 CI、Bot/API/HF、OIDC/SIEM/OTel/Vault/KMS、第三方审计没有真实证据时必须标为 pending/missing/外部连通验证待执行。
- [x] 任务包占位符清空，主路线图和任务索引同步。

# Task Package Checklists
## TP-01.01
- [x] `RESEARCH.md` 记录 OpenAPI、AsyncAPI、CloudEvents、Kubernetes、Backstage、Temporal、OpenTelemetry、DORA、SLSA、CycloneDX、GitHub Attestations、SRE sources。
- [x] 可见版本事实记录为当前观察，不当成永久事实。
- [x] Verify: `rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|Backstage|Temporal|OpenTelemetry|DORA|SLSA|CycloneDX|Attestations|SLO" governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan/RESEARCH.md`
- [x] Gate: 来源必须为官方或事实标准资料。

## TP-01.02
- [x] 每个资料映射到 FateCat resource/gate。
- [x] 未实现内容保留为 target 或 pending。
- [x] Verify: `rg -n "FateCat 映射|资源成熟度矩阵|Next Slice" governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan/RESEARCH.md`
- [x] Gate: 未实现能力不得写成 passed。

## TP-02.01
- [x] 0104/0105 Done 事实来自任务文档和 Git。
- [x] 主路线图读取并增量更新。
- [x] Verify: `rg -n "0104|0105|Overall Status: `Done`" governance/tasks/0104-measurement-infrastructure-evaluation-trend-store governance/tasks/0105-measurement-infrastructure-current-audit-bundle-evaluation-trend governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan`
- [x] Gate: 当前事实必须能从仓库文件或命令输出复核。

## TP-02.02
- [x] `gh run list --commit HEAD` 结果写入上下文。
- [x] workflow manual trigger 模型写清楚。
- [x] Verify: `gh run list --commit HEAD --limit 10 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt`
- [x] Gate: 空结果只能写 missing/pending，不得写 passed。

## TP-03.01
- [x] 资源成熟度矩阵覆盖核心基础设施对象。
- [x] 每项都有 next slice 或 external live pending。
- [x] Verify: `rg -n "ReleaseArtifact|EvaluationRun|Evidence|Runtime|SecurityControl|ObservabilitySignal|DeliverySurface|AuditHandoff" governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan/RESEARCH.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 资源矩阵必须覆盖 release、evaluation、evidence、runtime、security、observability、delivery 和 audit。

## TP-03.02
- [x] 执行波次明确下一 P0 是 current remote CI evidence refresh。
- [x] 不可伪造口径写入 roadmap 和 `RESEARCH.md`。
- [x] Verify: `rg -n "current remote CI evidence refresh|不可伪造|外部连通验证待执行" governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 下一 P0 必须可直接转换为实现任务。

## TP-04.01
- [x] `RESEARCH.md`、任务包和主路线图落盘。
- [x] `INDEX.md` 状态最终同步。
- [x] Verify: `git diff --name-only`
- [x] Gate: diff 只包含 0106 任务包、任务索引和主路线图。

## TP-04.02
- [x] task docs validator 通过。
- [x] placeholder scan 无输出。
- [x] reference scan 命中 post-0105 计划。
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0106-measurement-infrastructure-100-post-0105-deep-research-plan --phase decompose`
- [x] Gate: validator `ok=true` 且 placeholder scan 无输出。
