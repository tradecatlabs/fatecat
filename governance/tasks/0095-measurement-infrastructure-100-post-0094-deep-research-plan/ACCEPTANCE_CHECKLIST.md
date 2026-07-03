# Acceptance Checklist

# Global Standards
- [x] 0095 只做 post-0094 调研和实现计划，不改业务代码。
- [x] 主路线图继续作为 100% living plan，不创建平行真相源。
- [x] 外部 live 项必须保持 `外部连通验证待执行` 或真实证据，不用本地 dry-run 替代。
- [x] 下一步实现任务必须从 Wave A 的本地可执行切片开始。
- [x] 任务文档必须通过 `auto-tasks` decompose 校验。

# Task Package Checklists

## TP-01.01 读取当前仓库事实

Verify: `git status --short --branch`、`git rev-parse HEAD`、0093/0094 `STATUS.md`。

Gate: 计划基于当前 `main` 和 0093/0094 已完成事实。

- [x] 当前仓库事实已读取。

## TP-01.02 外部资料调研

Verify: `rg -n "OpenAPI|AsyncAPI|CloudEvents|Kubernetes Controllers|OpenTelemetry|SLSA|OWASP|NIST|Stripe" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md`。

Gate: 同构矩阵覆盖 API、事件、控制面、目录、provider、runtime、observability、security、supply chain。

- [x] 外部资料矩阵已落盘。

## TP-02.01 资源成熟度矩阵

Verify: `rg -n "100% 资源成熟度矩阵|Capability|Provider|CalculationJob|AuditHandoff" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md`。

Gate: 每个资源都有当前状态、100% 目标和下一步证据。

- [x] 资源成熟度矩阵已落盘。

## TP-02.02 执行波次和证据口径

Verify: `rg -n "Wave A|Wave B|Wave C|Wave D|不可伪造完成标准" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md`。

Gate: 本地可执行任务和外部 live 任务明确分离。

- [x] 波次和不可伪造证据已落盘。

## TP-03.01 主路线图同步

Verify: `rg -n "Post-0094|Next-01|Wave A|Wave B" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。

Gate: 主路线图包含 post-0094 刷新段，不创建第二真相源。

- [x] 主路线图已同步。

## TP-03.02 任务文档回填

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan --phase decompose`。

Gate: validator 返回 `placeholders=[]` 且文档结构合规。

- [x] 任务文档已回填。

## TP-04.01 任务校验

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan --phase decompose`。

Gate: exit 0。

- [x] 任务校验通过。
