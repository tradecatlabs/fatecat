# Execution Checklist
[x] TP-01.01 | P0 | Git/worktree、HEAD 与 0091 远端 CI 事实复核 | Verify: `git status --short --branch`、`git log -1 --oneline`、`gh run list --limit 5` | Gate: 0091 只写成 local retention cleanup baseline，不写成 production scheduler/Postgres cleanup live | Parallelizable: No
[x] TP-01.02 | P0 | 既有计划和契约复核 | Verify: 主路线图、audit/release contracts、task index 已读取 | Gate: 既有 0.10 与新 0.11 不冲突 | Parallelizable: No
[x] TP-02.01 | P0 | 外部一手资料调研 | Verify: `RESEARCH.md` source matrix 已完成 | Gate: 来源为官方/一手资料或明确仓库事实 | Parallelizable: Yes
[x] TP-02.02 | P0 | FateCat 同构能力抽象 | Verify: `RESEARCH.md` synthesis 已完成 | Gate: 每个成熟领域映射到 FateCat 资源域 | Parallelizable: Yes
[x] TP-03.01 | P0 | 100% 完成门禁和失败判定 | Verify: 主路线图 `0.11.5`、`0.11.6` | Gate: external pending 不写成已完成 | Parallelizable: No
[x] TP-03.02 | P0 | Post-0091 任务队列和执行顺序 | Verify: 主路线图 `0.11.3`、`0.11.4` | Gate: 后续任务可直接拆成 0093+ | Parallelizable: No
[x] TP-03.03 | P0 | 外部阻断项分层 | Verify: `RESEARCH.md` External Validation Pending | Gate: 所有外部平台均标记 `外部连通验证待执行` | Parallelizable: No
[x] TP-04.01 | P0 | 主路线图更新 | Verify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 包含 `0.11` | Gate: 不创建平行 roadmap | Parallelizable: No
[x] TP-04.02 | P0 | 任务文档和 RESEARCH 回填 | Verify: 0092 目录无占位符 | Gate: README/CONTEXT/PLAN/ACCEPTANCE/CHECKLIST/TODO/STATUS/RESEARCH 均可读 | Parallelizable: No
[x] TP-04.03 | P0 | 文档校验 | Verify: `validate_task_docs.py --phase decompose` 和占位符检查 | Gate: validator exit 0；无模板占位符残留 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
