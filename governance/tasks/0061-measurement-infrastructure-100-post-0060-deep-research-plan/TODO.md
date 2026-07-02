# Execution Checklist

[x] TP-01.01 | P0 | 读取 git 状态、最新提交、roadmap、任务索引和 0060 事实 | Verify: `git status` / `git log` / `sed` | Gate: 当前事实明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 复核成熟基础设施资料 | Verify: web research + existing roadmap source matrix | Gate: 资料来自官方或一手来源 | Parallelizable: Yes
[x] TP-02.02 | P0 | 把基础设施范式映射到 FateCat 资源模型 | Verify: `RESEARCH.md` | Gate: 覆盖核心资源和证据要求 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 `RESEARCH.md` 调研矩阵 | Verify: `rg -n "Source Matrix|Target End State" governance/tasks/0061-*` | Gate: 有来源、有映射、有缺口 | Parallelizable: No
[x] TP-03.02 | P0 | 刷新 100% roadmap post-0060 实现蓝图 | Verify: `rg -n "0.8|0061|Post-0060 深度调研" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 后续任务树明确 | Parallelizable: No
[x] TP-03.03 | P0 | 明确后续任务树、优先级、失败判定和证据口径 | Verify: roadmap + task README | Gate: 不夸大完成度 | Parallelizable: No
[x] TP-04.01 | P0 | 清理任务文档占位符，更新 TODO/STATUS/ACCEPTANCE | Verify: placeholder scan | Gate: 无模板占位符 | Parallelizable: No
[x] TP-04.02 | P0 | 执行任务文档校验、关键词检查和 git 状态复核 | Verify: validators + `git status` | Gate: 文档可复核 | Parallelizable: No
