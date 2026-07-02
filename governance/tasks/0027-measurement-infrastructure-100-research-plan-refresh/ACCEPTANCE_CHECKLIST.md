# Acceptance Checklist

# Global Standards
- [x] 外部基础设施官方资料已整理到主路线图。
- [x] 当前 worktree 事实和未完成生产化事项已区分。
- [x] D0-D10 十个基础设施域已定义。
- [x] MI-100 剩余任务树已定义。
- [x] 下一批 `0028+` 推荐任务已排序。
- [x] 不可伪造证据口径已写入。
- [x] 本任务明确不实现业务功能。
- [x] 任务包占位符已移除。
- [x] closeout 任务文档验证已执行。
- [x] 全任务树验证已执行。

# Task Package Checklists

## TP-01.01 收集外部官方资料
- [x] Verify: 主路线图第 1 节包含官方资料链接。
- [x] Gate: 官方资料覆盖 API、workflow、catalog、controller、provider、observability、SRE、supply chain、security、ML/eval。

## TP-01.02 提炼基础设施同构能力
- [x] Verify: 主路线图第 1 节把每类外部资料映射为 FateCat 同构要求。
- [x] Gate: 调研结论落到 FateCat 同构要求。

## TP-02.01 读取当前仓库事实
- [x] Verify: `git status --short --branch`、`governance/tasks/INDEX.md`、`contracts/fate/` 已读取。
- [x] Gate: 事实来源来自本地命令和仓库文件。

## TP-02.02 区分完成度
- [x] Verify: 主路线图第 3 节列出当前事实和仍不是生产 100% 的原因。
- [x] Gate: 本地已落地与生产待验证分开表达。

## TP-03.01 重写主路线图
- [x] Verify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已更新。
- [x] Gate: 没有新增平行路线图。

## TP-03.02 写入任务树和验收口径
- [x] Verify: 主路线图包含 D0-D10、MI-100、下一批任务、总验收清单。
- [x] Gate: 后续任务可从计划直接拆出。

## TP-04.01 回填任务包文档
- [x] Verify: 0027 README/CONTEXT/PLAN/ACCEPTANCE/ACCEPTANCE_CHECKLIST/TODO/STATUS 已回填。
- [x] Gate: 无占位符。

## TP-04.02 执行任务文档验证
- [x] Verify: task validators、占位符扫描和 diff check 已执行。
- [x] Gate: 0027 可 closeout。
