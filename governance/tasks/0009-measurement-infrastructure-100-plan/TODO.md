# Execution Checklist
[x] TP-01.01 | P0 | 调研成熟基础设施官方资料 | Verify: `rg -n "Stripe|Twilio|Plaid|Kubernetes|Terraform|Temporal|OpenTelemetry|OpenAI" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 计划文档列出官方资料和同构能力。 | Parallelizable: Yes
[x] TP-01.02 | P0 | 映射 FateCat 100% 基础设施差距 | Verify: `rg -n "IMP-01|IMP-12|100% 验收清单" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 覆盖资源、API、provider、job、evidence、eval、observability、security、多端。 | Parallelizable: No
[x] TP-02.01 | P0 | 写入完整实现计划文档 | Verify: `test -f docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 文档包含目标终态、架构、主线、波次、首批切片和验收清单。 | Parallelizable: No
[x] TP-02.02 | P1 | 更新文档索引 | Verify: `rg -n "测算基础设施100%实现计划.md" docs/reference-materials/README.md` | Gate: roadmap 索引能发现新计划文档。 | Parallelizable: Yes
[x] TP-03.01 | P0 | 回填 0009 任务容器 | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0009-measurement-infrastructure-100-plan --phase closeout` | Gate: 任务容器 closeout 校验通过。 | Parallelizable: No
[x] TP-03.02 | P0 | 检查文档和任务树卫生 | Verify: `git diff --check && python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown` | Gate: whitespace 和任务树校验通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
