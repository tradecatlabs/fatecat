# Execution Checklist
[x] TP-01.01 | P0 | 读取当前 git 状态、主路线图、0093/0094 状态和 core quality 资产 | Verify: `git status --short --branch`、`git rev-parse HEAD`、`sed`/`find`/`rg` | Gate: 计划基于当前 worktree 事实 | Parallelizable: Yes
[x] TP-01.02 | P0 | 查询并整理基础设施一手资料 | Verify: 外部资料 URL 写入 `RESEARCH.md` | Gate: 同构矩阵覆盖 API、事件、控制面、目录、provider、runtime、observability、security、supply chain | Parallelizable: Yes
[x] TP-02.01 | P0 | 建立资源成熟度矩阵 | Verify: `rg -n "100% 资源成熟度矩阵|Capability|Provider|CalculationJob|AuditHandoff" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md` | Gate: 每个资源都有 current/target/next evidence | Parallelizable: No
[x] TP-02.02 | P0 | 制定 post-0094 执行波次和不可伪造证据 | Verify: `rg -n "Wave A|Wave B|不可伪造完成标准" governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/RESEARCH.md` | Gate: 外部 live 和本地可执行任务分离 | Parallelizable: No
[x] TP-03.01 | P0 | 更新主路线图 | Verify: `rg -n "Post-0094|Next-01|Wave A|Wave B" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 不创建平行路线图 | Parallelizable: No
[x] TP-03.02 | P0 | 回填 0095 任务文档和 RESEARCH | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan --phase decompose` | Gate: 无模板占位符残留 | Parallelizable: No
[x] TP-04.01 | P0 | 校验任务文档与引用 | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan --phase decompose` | Gate: task docs valid | Parallelizable: No

说明：
- 0095 是计划刷新任务。
- 下一步实现任务应从 Wave A 的 `八字/紫微 corpus/report diff expansion` 开始。
