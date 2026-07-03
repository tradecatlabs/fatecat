# Acceptance Checklist

# Global Standards
- [x] 复用现有 registry/gate，不复制第二套业务真相。
- [x] 不保存 token、secret、DSN、生产日志、用户输入或报告正文。
- [x] 不把 control-plane gate pass 写成 production live pass。
- [x] 任务包占位符清空。

# Task Package Checklists
## TP-01
- [x] 扫描 `contracts/fate/capabilities`、`delivery`、`evaluations` 和 provider scripts。
- [x] Verify: file scans and JSON counts.
- [x] Gate: identified reuse path.

## TP-02
- [x] 新增 control-plane registry。
- [x] 新增 control-plane schema。
- [x] 新增 control-plane AGENTS。
- [x] Verify: JSON parse through tests.
- [x] Gate: 4 core resources present.

## TP-03
- [x] 新增 Python gate。
- [x] 新增 shell wrapper。
- [x] 接入 local-ci quick。
- [x] Verify: `bash scripts/control-plane-gate.sh`.
- [x] Gate: status passed.

## TP-04
- [x] 新增 regression test。
- [x] 更新 `contracts/fate/AGENTS.md`。
- [x] 更新 roadmap/task index。
- [x] Verify: targeted pytest and task docs validator.
- [x] Gate: tests pass.

## TP-05
- [x] Git 提交推送由最终交付执行。
- [x] Verify: `git status --short --branch`.
- [x] Gate: worktree clean after delivery.
