# Task-Level Acceptance
- `local-ci.sh --profile quick --output <dir>` 成功时写入 `<dir>/summary.json`，且 `status=passed`、`profile=quick`、`commit=<current HEAD>`。
- local-ci 失败路径也尽力写入 `summary.json`，且 `status=failed`。
- `live-release-gate.py --local-ci-summary <summary.json>` 只在 summary 内容可信时让 `evidence.local_ci_quick=pass`。
- 错误 profile、错误 commit、failed status、缺失文件必须 fail 或 pending，不得 pass。
- `public-release-gate.sh` 默认执行 local-ci 时传递 summary JSON；`--skip-local-ci` 保持 pending。
- 远端 CI、生产 API、HF Space、Bot、container digest、rollback drill、clean git state 不因本任务被伪造为 pass。

# Validation Plan
- `bash -n scripts/local-ci.sh scripts/public-release-gate.sh scripts/live-release-gate.sh`
- `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py`
- `bash scripts/release-artifacts.sh --output-dir /tmp/fatecat-release-artifacts-0041 --summary-json /tmp/fatecat-release-artifacts-0041-summary.json`
- `bash scripts/live-release-gate.sh --local-ci-summary <fixture> --sbom-path ... --provenance-path ... --output-json ...`
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0041-measurement-infrastructure-local-ci-evidence-gate --phase closeout`
- `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto`

# Review Gate
- 不允许只检查 summary 路径存在。
- 不允许把 skipped local-ci 标为 pass。
- 不允许改变 live release 的 required evidence 集合。
- 不允许把本地 quick CI 证据扩大解释为远端 CI 或生产发布通过。

# Runtime Verification Gate
- 输出 JSON 无敏感值。
- `shipGate` 仍应 blocked，除非所有其他外部证据真实提供。
- dirty worktree 下 `evidence.clean_git_state` 仍 pending/fail。

# Ship Readiness
本任务完成只代表 local quick CI evidence gate 可复核，不代表 FateCat 可 live release。live release 仍取决于外部证据与 clean git state。

# Task Package Acceptance
## TP-01.01
- 已记录现有缺口。

## TP-02.01
- summary JSON 字段稳定，可被 live gate 消费。

## TP-03.01
- live gate 对 local CI summary 做内容校验。

## TP-04.01
- public-release 默认路径接线完成。

## TP-05.01
- 测试、任务文档、closeout 通过。

# Anti-Goals
- 不得把外部 live release 证据伪造成已完成
- 不得虚构证据
- 不得改变 required evidence ID 集合
