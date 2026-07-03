# Execution Checklist

[x] TP-01.01 | P0 | 查询官方资料和事实标准 | Verify: Source matrix in `RESEARCH.md` | Gate: 每个来源映射到 FateCat 资源/门禁 | Parallelizable: Yes
[x] TP-01.02 | P0 | 提炼 FateCat 映射原则 | Verify: `RESEARCH.md` sections 2-4 | Gate: 100% 定义不等同预测命中率 | Parallelizable: Yes
[x] TP-02.01 | P0 | 读取主路线图与 0095-0098 任务事实 | Verify: `git status` and task docs inspected | Gate: 不把 0098 写成已发布 | Parallelizable: Yes
[x] TP-02.02 | P0 | 识别当前 worktree 对计划的影响 | Verify: current worktree evidence recorded | Gate: 计划兼容 0098 local closeout 与外部 live pending 边界 | Parallelizable: Yes
[x] TP-03.01 | P0 | 定义资源成熟度矩阵 | Verify: matrix in `RESEARCH.md` and roadmap | Gate: 覆盖核心 infra resources | Parallelizable: No
[x] TP-03.02 | P0 | 定义执行波次、任务树和不可伪造证据 | Verify: roadmap post-0098 section | Gate: local/external waves clearly separated | Parallelizable: No
[x] TP-04.01 | P0 | 更新 RESEARCH、任务包和主路线图 | Verify: `rg -n "Post-0098|0099|外部连通验证待执行"` | Gate: no conflicting 0098 done claim | Parallelizable: No
[x] TP-04.02 | P0 | 运行文档校验与引用检查 | Verify: `validate_task_docs.py --phase decompose` and placeholder scan | Gate: no placeholders, no validator errors | Parallelizable: No
