# Acceptance Checklist

# Global Standards
- [x] 官方资料调研已进入计划文档
- [x] 计划文档不宣称未实现能力已完成
- [x] 计划覆盖资源、API、provider、job、report、evidence、eval、observability、security、多端、供应链
- [x] README 索引已更新
- [x] 任务容器已回填

# Task Package Checklists
## TP-01.01 official reference research

Verify: `rg -n "Stripe|Twilio|Plaid|Kubernetes|Terraform|Temporal|OpenTelemetry|OpenAI" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 官方资料和同构能力可复核。

- [x] Stripe / Twilio / Plaid 已覆盖。
- [x] Kubernetes / Terraform / Temporal 已覆盖。
- [x] OpenTelemetry / OpenAI 已覆盖。

## TP-01.02 FateCat gap mapping

Verify: `rg -n "IMP-01|IMP-12|100% 验收清单" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 计划覆盖完整实现主线。

- [x] 十二条 IMP 主线已写入。
- [x] 六个执行波次已写入。
- [x] 首批最小切片已写入。

## TP-02.01 Plan document

Verify: `test -f docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 文档存在。

- [x] 文档已新增。

## TP-02.02 Docs index

Verify: `rg -n "测算基础设施100%实现计划.md" docs/reference-materials/README.md`

Gate: 索引可发现文档。

- [x] 索引已更新。

## TP-03.01 Task container

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0009-measurement-infrastructure-100-plan --phase closeout`

Gate: closeout 校验通过。

- [x] 任务文档已回填。

## TP-03.02 Hygiene

Verify: `git diff --check && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown`

Gate: whitespace 和任务树校验通过。

- [x] `git diff --check` 与任务树校验已通过。
