# Repo Evidence
- `scripts/live-release-gate.py` 已有 `--local-ci-summary` 参数，但当前 `build_checks()` 只调用 `path_or_url_exists()`。
- `scripts/local-ci.sh` 当前只写 `summary.txt`，没有机器可读 status JSON。
- `scripts/public-release-gate.sh` 默认会执行 `local-ci.sh --profile quick --output <dir>/local-ci-quick`，但没有把该证据路径传给 live gate。
- `/tmp/fatecat-local-ci-0040/live-release-gate.json` 显示 `evidence.local_ci_quick=pending`，即使 quick CI 已通过。
- `tests/regression/test_live_release_gate.py` 已覆盖 local-contract blocked gate，但未覆盖 local CI summary 内容校验。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不伪造外部 live 证据 | 只把 local quick CI 变为 pass，远端 CI/API/HF/Bot/digest/rollback/clean git 继续按事实 pending/fail |
| 兼容现有脚本调用 | 保留 `summary.txt`，新增 `summary.json` |
| 证据要可审计 | summary JSON 记录 schemaVersion、profile、status、commit、startedAt、finishedAt、artifacts |
| 失败不能被误判为通过 | local-ci 用 trap 在失败时写 `status=failed`，live gate 只接受 `status=passed` |
| 不扩大任务范围 | 不修改生产业务逻辑、不新增外部依赖 |

# Change Boundary
- 可改：`scripts/local-ci.sh`、`scripts/public-release-gate.sh`、`scripts/live-release-gate.py`、`tests/regression/test_live_release_gate.py`、release gate 相关文档。
- 可新增：必要时新增小型测试 fixture 或任务文档。
- 禁止：远端 CI 配置伪造、生产密钥、外部账号、container registry 发布、git clean/commit/push。

# Risk Matrix
| Risk | Level | Mitigation |
| --- | --- | --- |
| local-ci 失败时没有写入 failed summary | medium | `trap` 收口，失败路径也写 JSON |
| summary 文件存在但内容不可信 | medium | live gate 校验 JSON schema-like fields、profile/status/commit |
| public-release `--skip-local-ci` 误传不存在证据 | low | 只有默认执行 local-ci 时传 summary；skip 时继续 pending |
| 当前 dirty worktree 导致 commit 证据不稳定 | low | summary 与 live gate 都使用同一当前 HEAD，不要求 clean |

# Assumptions and Falsification
- 假设：本地 quick CI 成功后可作为 `evidence.local_ci_quick` 的本地证据。
- 反证：若 summary 不是 JSON、profile 不是 quick、status 不是 passed、commit 不等于当前 HEAD，则 live gate 必须 fail。
- 假设：public-release 默认路径执行 local-ci quick 后，可以把 `<output>/local-ci-quick/summary.json` 传给 live gate。
- 反证：`--skip-local-ci` 时不应假装 local CI 通过。

- 调试模式: `Optional`

# Critical Ambiguities
- 无阻断歧义。剩余外部 live release 证据不是本任务范围。

# Debug Evidence Contract
- 这是 gate 证据接线问题，不需要 `DEBUG.md`。若测试发现失败，将在 `STATUS.md` 记录最小复现命令和修复证据。

# Task Package Context Map
## TP-01.01
确认 `--local-ci-summary` 参数存在但接线和内容校验不足。

## TP-02.01
在 `local-ci.sh` 写 `summary.json`，保留 `summary.txt`。

## TP-03.01
在 `live-release-gate.py` 增加 local CI summary 解析和校验函数。

## TP-04.01
在 `public-release-gate.sh` 默认 local-ci 路径传递 summary JSON。

## TP-05.01
运行 targeted tests、shell syntax、local smoke、task docs validation、closeout。
