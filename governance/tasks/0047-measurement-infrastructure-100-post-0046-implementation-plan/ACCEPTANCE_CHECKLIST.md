# Acceptance Checklist

# Global Standards

- [x] 当前仓库事实来自真实命令。
- [x] 外部资料使用官方或一手来源。
- [x] 计划区分 local baseline、remote CI、external live、human/legal review。
- [x] 剩余任务树按基础设施域组织，而不是按术数功能堆叠。
- [x] 未来任务编号不再与尚未创建的目录强绑定。
- [x] `git diff --check` 通过。
- [x] task docs validation 通过。
- [x] tasks tree validation 通过。

# Task Package Checklists

## TP-01.01
- [x] 当前事实复核完成。
- Verify: `git status --short --branch`、`gh run view`。
- Gate: 只把真实 completed/success workflow 写成成功。

## TP-02.01
- [x] 外部基础设施资料同构调研完成。
- Verify: roadmap 外部同构矩阵。
- Gate: 使用官方/一手资料链接。

## TP-03.01
- [x] 主路线图 post-0046 刷新完成。
- Verify: roadmap `MI-NEXT-*` 剩余任务树。
- Gate: 不绑定尚未创建的目录编号。

## TP-04.01
- [x] 任务包、索引和校验收口完成。
- Verify: `git diff --check`、task docs validation、tasks tree validation。
- Gate: 任务容器可复核。
