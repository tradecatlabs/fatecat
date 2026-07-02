# Task-Level Acceptance
- `rollback-drill.sh --output-json <path>` 生成 `kind=fatecat.rollback_drill_evidence`、`status=passed`、`mode=dry-run`、`productionRollbackExecuted=false` 的 JSON。
- JSON 包含当前 commit、prechecks、candidateCommands、requiredDocuments、artifacts、limitations。
- live gate 只在 rollback JSON 内容可信时让 `evidence.rollback_drill=pass`。
- public-release 默认路径生成并传递 rollback evidence。
- 真实生产 API/HF/Bot/CI/container/clean git 不因本任务被伪造成 pass。

# Validation Plan
- `bash -n scripts/rollback-drill.sh scripts/public-release-gate.sh scripts/live-release-gate.sh`
- `bash scripts/rollback-drill.sh --output-json /tmp/fatecat-rollback-drill-0042.json`
- `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py tests/regression/test_rollback_drill.py`
- `FATECAT_PUBLIC_RELEASE_SMOKE_PORT=<port> bash scripts/public-release-gate.sh --output /tmp/fatecat-public-release-0042`
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`

# Review Gate
- 不接受只检查 rollback artifact 路径存在。
- 不接受缺 candidate commands 或 `productionRollbackExecuted` 缺失的证据。
- 不接受把 dry-run 证据写成真实生产回滚完成。

# Runtime Verification Gate
- JSON 无 secret。
- `shipGate` 仍 blocked，除非外部证据全部真实提供。
- `evidence.rollback_drill` 可从 pending 变 pass。

# Ship Readiness
本任务完成只代表本地 rollback dry-run evidence baseline 可复核，不代表真实生产回滚演练已完成。

# Task Package Acceptance
## TP-01.01
- [x] rollback gate 和相关脚本/文档已盘点。

## TP-02.01
- [ ] rollback drill JSON 生成器完成。

## TP-03.01
- [ ] live gate 内容校验完成。

## TP-04.01
- [ ] public-release 默认路径传递 rollback evidence。

## TP-05.01
- [ ] 验证和 closeout 完成。

# Anti-Goals
- 不得执行真实生产回滚
- 不得虚构证据
- 不得改写 Git 历史
