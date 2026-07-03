# Acceptance Checklist

# Global Standards
- [x] 只桥接 `current-release-proof.json`，不覆盖 `live-release-gate.json`。
- [x] 不保存 token、secret、DSN、URL、生产日志、用户输入或报告正文。
- [x] 不把 release proof passed 写成 production live passed。
- [x] 默认无 sidecar 时保持兼容行为。

# Task Package Checklists
## TP-01
- [x] 确认 certification 当前只从 evidence dir 读取 release proof。
- [x] Verify: source scan.
- [x] Gate: 盲区定义清楚。

## TP-02
- [x] 新增 `--current-release-proof-json`。
- [x] 新增 evidence override source 记录。
- [x] 新增 `evidenceOverrides` summary 字段。
- [x] Verify: CLI smoke.
- [x] Gate: sidecar 不绕过 live gate。

## TP-03
- [x] 更新 regression tests。
- [x] 更新 contract。
- [x] 更新 roadmap/task index。
- [x] Verify: targeted pytest and docs validator.
- [x] Gate: tests pass.

## TP-04
- [x] 运行 ruff/format。
- [x] 运行 secret scan。
- [x] 自审 diff。
- [x] 提交推送由最终交付执行。
- [x] Verify: ruff, secret scan and git status.
- [x] Gate: local validation passed; remote update handled by Git delivery step.
