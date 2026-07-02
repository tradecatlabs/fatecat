# Repo Evidence
- `contracts/fate/delivery/release-gate.json` 已登记 `evidence.rollback_drill`。
- `scripts/live-release-gate.py` 当前对 `--rollback-evidence-path` 只做 `path_or_url_exists()`。
- `scripts/public-release-gate.sh` 已生成 local-ci summary 和 release artifacts，但未生成 rollback drill evidence。
- `docs/reference-materials/operations/测算基础设施 API 接入.md` 只要求传 `--rollback-evidence-path`，未定义可生成证据。
- `docs/deployment/huggingface-space.md`、`scripts/container-release.sh`、`scripts/hf-space-deploy.sh` 和 `scripts/production-readiness.sh` 可作为回滚演练引用对象。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不执行真实回滚 | 脚本默认 dry-run，只检查资料和候选命令 |
| 不伪造生产演练 | JSON 明确 `mode=dry-run`、`productionRollbackExecuted=false` |
| 证据可机器校验 | live gate 校验 kind/status/mode/commit/prechecks/commands |
| 不新增依赖 | Python 标准库实现 |
| 不泄露 secret | 不读取 env secret，不输出 token/password |

# Change Boundary
- 可改：`scripts/rollback-drill.*`、`scripts/live-release-gate.py`、`scripts/public-release-gate.sh`、`scripts/local-ci.sh`、delivery release gate contract/registry/docs、regression tests、0042 task docs。
- 禁改：真实生产环境、registry、Git 历史、HF/Bot token、部署远端状态。

# Risk Matrix
| Risk | Level | Mitigation |
| --- | --- | --- |
| dry-run 被误解为真实生产回滚 | medium | evidence limitations 和 docs 明确不是 production rollback |
| 回滚命令过于具体导致误执行 | medium | 只记录 candidate commands，不自动执行 |
| live gate 接受空 JSON | medium | 校验 kind/status/mode/prechecks/commands/commit |

# Assumptions and Falsification
- 假设：本地 dry-run rollback drill 可以作为 release gate 的仓库内基础证据。
- 反证：若 JSON 不含 `productionRollbackExecuted=false` 或候选命令为空，live gate 必须 fail。
- 假设：真实发布前仍需要人工或平台级回滚演练。
- 反证：如果真实 registry/HF/production rollback evidence 提供，应作为更高级证据，不用 dry-run 冒充。

- 调试模式: `Optional`

# Critical Ambiguities
- 真实生产回滚平台未提供；本轮只做本地 dry-run baseline。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。若 rollback evidence 校验失败，保留 output JSON 和 gate detail。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | 盘点 rollback gate 和现有部署脚本 |
| TP-02.01 | 生成 dry-run rollback drill JSON |
| TP-03.01 | live gate 校验 rollback JSON |
| TP-04.01 | public-release/local-ci/docs 接入 |
| TP-05.01 | 验证和 closeout |
