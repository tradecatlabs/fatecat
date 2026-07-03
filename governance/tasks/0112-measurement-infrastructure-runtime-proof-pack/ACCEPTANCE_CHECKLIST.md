# Acceptance Checklist

# Global Standards
- [x] 复用现有子 gate，不复制 runtime/secret/multi-replica 真相。
- [x] 不保存 token、secret、DSN、URL、生产日志、用户输入或报告正文。
- [x] 不把 runtime proof gate pass 写成 production live pass。
- [x] exactly-once 保持非声明边界。

# Task Package Checklists
## TP-01
- [x] 扫描 runtime backend、public webhook、secret provider 和 multi-replica gates。
- [x] Verify: file scans and existing contract links.
- [x] Gate: reuse path identified.

## TP-02
- [x] 新增 runtime proof contract。
- [x] 新增 runtime proof schema。
- [x] Verify: JSON parse through tests.
- [x] Gate: required components present.

## TP-03
- [x] 新增 Python gate。
- [x] 新增 shell wrapper。
- [x] 接入 local-ci quick。
- [x] 接入 certification domain。
- [x] 接入 current audit bundle local artifact index。
- [x] Verify: `bash scripts/runtime-proof-gate.sh`.
- [x] Gate: status passed and shipGate blocked by pending externals.

## TP-04
- [x] 新增 regression test。
- [x] 更新 delivery/scripts AGENTS。
- [x] 更新 roadmap/task index。
- [x] Verify: targeted pytest and task docs validator.
- [x] Gate: tests pass.

## TP-05
- [x] Git 提交推送由最终交付执行。
- [x] Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-runtime-proof-pack`.
- [x] Gate: quick CI passed with 289 focused regression tests.
