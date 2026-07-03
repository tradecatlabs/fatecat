# Acceptance Checklist

# Global Standards
- [x] 100% is defined as infrastructure maturity, not fortune-telling accuracy.
- [x] External live items are not marked complete without real evidence.
- [x] Existing 0098 local closeout state is acknowledged.
- [x] Existing roadmap remains the source of truth.
- [x] Task docs validator passes.

# Task Package Checklists

## TP-01.01 查询官方资料和事实标准
Verify: `rg -n "CNCF|OpenAPI|AsyncAPI|CloudEvents|Kubernetes|OpenTelemetry|SLSA|OWASP|NIST|Stripe" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan/RESEARCH.md`。
Gate: 官方/事实标准来源覆盖平台工程、API、事件、控制面、provider、runtime、observability、security、supply chain 和 webhook/idempotency。

- [x] Source matrix written.

## TP-01.02 提炼 FateCat 映射原则
Verify: `rg -n "FateCat 对应要求|资源成熟度矩阵|100% 不是预测准确率" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan/RESEARCH.md`。
Gate: 每个 source 映射到 FateCat resource/gate，且 100% 口径不等同预测命中率。

- [x] Mapping principles written.

## TP-02.01 读取主路线图与 0095-0098 任务事实
Verify: `sed`/`rg` against main roadmap and task docs。
Gate: Plan reflects 0096/0097 done and 0098 local closeout passed.

- [x] Current task facts recorded.

## TP-02.02 识别当前 worktree 对计划的影响
Verify: `git status --short --branch`。
Gate: Current worktree is not hidden and 0098 local closeout is not described as external live completion.

- [x] Dirty worktree impact recorded.

## TP-03.01 定义资源成熟度矩阵
Verify: `rg -n "Capability|Provider|CalculationJob|SecurityControl|ReleaseArtifact|AuditHandoff" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan/RESEARCH.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
Gate: Matrix covers core infra resources with current state, 100% target and next task.

- [x] Resource matrix written.

## TP-03.02 定义执行波次、任务树和不可伪造证据
Verify: `rg -n "Wave 0|Wave A|Wave B|不可伪造完成标准|外部连通验证待执行" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan/RESEARCH.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
Gate: Local-only and external-live waves are separated; external checks are not marked passed.

- [x] Waves and falsifiers written.

## TP-04.01 更新 RESEARCH、任务包和主路线图
Verify: `rg -n "Post-0098|0099|0098 已将|外部 live" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan`。
Gate: Roadmap has post-0098 delta and corrected 0098 local-closeout wording.

- [x] Docs patched.

## TP-04.02 运行文档校验与引用检查
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan --phase decompose`。
Gate: Validator exits 0 and placeholder scan has no output.

- [x] Validator passed.

# Verification Checklist
- [x] `rg -n "\\{\\{" governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan --phase decompose`
- [x] `rg -n "Post-0098|0099|外部连通验证待执行" docs/reference-materials/roadmap/测算基础设施100%实现计划.md governance/tasks/0099-measurement-infrastructure-100-post-0098-deep-research-plan`
