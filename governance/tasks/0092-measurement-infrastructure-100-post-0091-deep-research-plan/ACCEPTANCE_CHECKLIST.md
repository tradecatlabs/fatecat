# Acceptance Checklist

# Global Standards
- [x] planning-only，不改业务代码。
- [x] 使用官方/一手资料链接，且仓库事实来自本地命令或 tracked 文件。
- [x] 主路线图只追加 Post-0091 章节，不创建平行路线图。
- [x] 所有外部 token、endpoint、生产账号、外部平台权限均标记为 `外部连通验证待执行`。
- [x] 不声明预测准确率 100%，不声明生产 live 已完成。

# Task Package Checklists
## TP-01.01 Git/worktree、HEAD、远端 CI 复核

Verify: `git status --short --branch`、`git log -1 --oneline`、`gh run list --limit 5`。

Gate: 0091 只写成 local retention cleanup baseline，不写成 production scheduler/Postgres cleanup live。

- [x] Git/worktree、HEAD、远端 CI 已复核。

## TP-01.02 既有计划和契约复核

Verify: 主路线图、audit/release contracts、task index 已读取。

Gate: 既有 0.10 与新 0.11 不冲突。

- [x] Roadmap、audit/release contracts、task index 已复核。

## TP-02.01 外部一手资料调研

Verify: `RESEARCH.md` source matrix 已完成。

Gate: 来源为官方/一手资料或明确仓库事实。

- [x] 外部一手资料已整理进 source matrix。

## TP-02.02 FateCat 同构能力抽象

Verify: `RESEARCH.md` synthesis 已完成。

Gate: 每个成熟领域映射到 FateCat 资源域。

- [x] FateCat 资源域映射已整理。

## TP-03.01 100% 完成门禁和失败判定

Verify: 主路线图 `0.11.5`、`0.11.6`。

Gate: external pending 不写成已完成。

- [x] 完成门禁和失败判定已写入路线图。

## TP-03.02 Post-0091 任务队列和执行顺序

Verify: 主路线图 `0.11.3`、`0.11.4`。

Gate: 后续任务可直接拆成 0093+。

- [x] Post-0091 下一批任务队列已写入路线图。

## TP-03.03 外部阻断项分层

Verify: `RESEARCH.md` External Validation Pending。

Gate: 所有外部平台均标记 `外部连通验证待执行`。

- [x] 外部阻断项已分层列出。

## TP-04.01 主路线图更新

Verify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 包含 `0.11`。

Gate: 不创建平行 roadmap。

- [x] 主路线图已更新。

## TP-04.02 任务文档和 RESEARCH 回填

Verify: 0092 目录无占位符。

Gate: README/CONTEXT/PLAN/ACCEPTANCE/CHECKLIST/TODO/STATUS/RESEARCH 均可读。

- [x] 任务文档和 `RESEARCH.md` 已回填。

## TP-04.03 文档校验

Verify: `validate_task_docs.py --phase decompose` 和占位符检查。

Gate: validator exit 0；无模板占位符残留。

- [x] 文档 validator 和占位符检查已执行。
