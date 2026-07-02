# Acceptance Checklist

# Global Standards

- [x] 0061 任务目录已初始化。
- [x] 当前仓库事实已记录：`main...origin/main`、最新 commit `6b3d5cd`。
- [x] 外部基础设施资料已映射为 FateCat 100% 资源模型。
- [x] 文档明确 100% 是基础设施成熟度，不是预测准确率。
- [x] 文档明确外部连通验证待执行项。
- [x] `validate_task_docs.py --phase decompose` 通过。
- [x] `validate_tasks_tree.py --phase auto` 通过。
- [x] 占位符扫描无结果。
- [x] git status 只包含本任务预期文档改动。

# Task Package Checklists

## TP-01.01

- [x] 读取 git 状态、最新提交、roadmap、任务索引和 0060 事实。
Verify: `git status` / `git log` / `sed`。
Gate: 当前事实明确。

## TP-02.01

- [x] 复核成熟基础设施资料。
Verify: web research + existing roadmap source matrix。
Gate: 资料来自官方或一手来源。

## TP-02.02

- [x] 把基础设施范式映射到 FateCat 资源模型。
Verify: `RESEARCH.md`。
Gate: 覆盖核心资源和证据要求。

## TP-03.01

- [x] 新增 `RESEARCH.md` 调研矩阵。
Verify: `rg -n "Source Matrix|Target End State" governance/tasks/0061-*`。
Gate: 有来源、有映射、有缺口。

## TP-03.02

- [x] 刷新 100% roadmap post-0060 实现蓝图。
Verify: `rg -n "0.8|0061|Post-0060 深度调研" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
Gate: 后续任务树明确。

## TP-03.03

- [x] 明确后续任务树、优先级、失败判定和证据口径。
Verify: roadmap + task README。
Gate: 不夸大完成度。

## TP-04.01

- [x] 清理任务文档占位符，更新 TODO/STATUS/ACCEPTANCE。
Verify: placeholder scan。
Gate: 无模板占位符。

## TP-04.02

- [x] 执行任务文档校验、关键词检查和 git 状态复核。
Verify: validators + `git status`。
Gate: 文档可复核。
