# Acceptance Checklist

# Global Standards
- [x] 只桥接 `current-audit-bundle/current-audit-bundle.json`，不覆盖 release/live 证据。
- [x] 不保存 token、secret、DSN、URL、生产日志、用户输入或报告正文。
- [x] 不把 audit bundle generated 写成 third-party audit passed。
- [x] 默认无 sidecar 时保持兼容行为。

# Task Package Checklists
## TP-01
- [x] 确认 local-ci current audit bundle 可能引用旧 current release proof。
- [x] Verify: source scan and jq inspection.
- [x] Gate: 盲区定义清楚。

## TP-02
- [x] 新增 `--current-audit-bundle-json`。
- [x] 新增 audit bundle override 映射。
- [x] 复用 `evidenceOverrides` summary 字段。
- [x] Verify: CLI smoke.
- [x] Gate: audit sidecar 不绕过 release/live gate。

## TP-03
- [x] 更新 regression tests。
- [x] 更新 contract。
- [x] 更新 scripts/audit AGENTS。
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
