# Acceptance Checklist

# Global Standards

- [x] 任务目标、范围和禁止项明确。
- [x] 外部资料链接可追溯。
- [x] 主路线图是唯一长期计划入口。
- [x] 0048 Bot live 阻断没有被掩盖。
- [x] `git diff --check` 通过。
- [x] `validate_task_docs.py` 通过。
- [x] `validate_tasks_tree.py` 通过。

# Task Package Checklists

## TP-01.01

- [x] 已复核现有路线图。
- [x] 已复核任务索引。
- [x] 已复核 0048 阻断状态。
- Verify: `git status --short --branch`、路线图和任务索引读取。
- Gate: 不基于聊天记忆脑补当前状态。

## TP-02.01

- [x] 已调研 API、事件、控制面、provider、durable runtime、observability、SRE、安全、供应链和 AI 风险治理资料。
- [x] 已在任务 context 中记录资料 URL。
- Verify: `CONTEXT.md` external research source table。
- Gate: 资料链接必须可追溯。

## TP-03.01

- [x] 已更新主路线图 `0.5` 深度调研补强章节。
- [x] 已写入 resource model、实现波次、下一步顺序和完成判定。
- Verify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- Gate: 不新建平行路线图。

## TP-04.01

- [x] 已运行文档校验。
- [x] 已更新 `STATUS.md` 验证结果。
- Verify: `git diff --check`、`validate_task_docs.py`、`validate_tasks_tree.py`。
- Gate: 不把未执行命令写成通过。
