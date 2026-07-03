# Acceptance Checklist

# Global Standards
- [x] 只使用当前 branch/worktree 事实。
- [x] 引用外部资料时优先官方或事实标准来源。
- [x] 不把 local-ci、dry-run、staged gate、任务 closeout 或 blocked bundle 写成生产 live。
- [x] 远端 CI、Bot/API/HF、OIDC/SIEM/OTel/Vault/KMS、第三方审计没有真实证据时必须标为 pending/in_progress/外部连通验证待执行。
- [x] 任务包占位符清空，主路线图和任务索引同步。

# Task Package Checklists
## TP-01.01
- [x] `RESEARCH.md` 记录 OpenAPI、AsyncAPI、CloudEvents、Kubernetes、Temporal、OpenTelemetry、Google SRE、OWASP、NIST、SLSA、CycloneDX、GitHub Attestations。
- [x] 可见版本事实记录为当前观察，不当成永久事实。
- [x] Verify: `rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes|Temporal|OpenTelemetry|SRE|OWASP|NIST|SLSA|CycloneDX|Attestations" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan/RESEARCH.md`
- [x] Gate: 来源必须为官方或事实标准资料。

## TP-01.02
- [x] 当前 HEAD、Container run、Acceptance run、0108 INDEX 重复状态写入上下文。
- [x] 未完成内容保留为 pending/in_progress/外部连通验证待执行。
- [x] Verify: `gh run list --commit $(git rev-parse HEAD) --limit 20 --json databaseId,headSha,status,conclusion,workflowName,url,createdAt`
- [x] Gate: `in_progress` run 不得写成 passed。

## TP-02.01
- [x] 资源模型覆盖核心基础设施对象。
- [x] 每项都有 next slice 或 external live pending。
- [x] Verify: `rg -n "ReleaseArtifact|Capability|Provider|CalculationJob|Evidence|EvaluationRun|DeliverySurface|SecurityControl|ObservabilitySignal|DeveloperPlatform|AuditHandoff" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan/RESEARCH.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 资源矩阵必须覆盖 release、capability、provider、runtime、quality、security、SRE、DX 和 audit。

## TP-02.02
- [x] 不可伪造口径写入 roadmap 和 `RESEARCH.md`。
- [x] 明确 local-ci、dry-run、staged gate、workflow_dispatch、in_progress 的边界。
- [x] Verify: `rg -n "不可伪造|in_progress|dry-run|staged gate|外部连通验证待执行" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 未实现能力不得写成 production passed。

## TP-03.01
- [x] W0-W9 执行波次写入 `RESEARCH.md` 和主路线图。
- [x] W0 优先处理 current release truth。
- [x] Verify: `rg -n "W0|W1|W2|W3|W4|W5|W6|W7|W8|W9" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan/RESEARCH.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 下一 P0 必须可直接转换为实现任务。

## TP-03.02
- [x] 最短下一步写清楚：release truth finalizer -> control plane -> external proof packs。
- [x] 外部阻断项列明 owner 需求和证据边界。
- [x] Verify: `rg -n "最短下一步|Release proof finalizer|外部连通验证待执行|current-release-proof" governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: 不允许绕过 W0 直接宣称 100%。

## TP-04.01
- [x] `RESEARCH.md`、任务包和主路线图落盘。
- [x] `INDEX.md` 状态最终同步。
- [x] Verify: `git diff --name-only`
- [x] Gate: diff 只包含 0109 任务包、任务索引和主路线图。

## TP-04.02
- [x] task docs validator 通过。
- [x] placeholder scan 无输出。
- [x] reference scan 命中 post-0108 计划。
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0109-measurement-infrastructure-100-post-0108-deep-research-plan --phase decompose`
- [x] Gate: validator `ok=true` 且 placeholder scan 无输出。
