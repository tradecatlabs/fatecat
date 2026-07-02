# Repo Evidence
- `scripts/live-release-gate.sh` 已支持 `--api-url` 与 `--hf-space-url`。
- 已有本地 evidence：
  - `/tmp/fatecat-local-ci-0043/summary.json`
  - `/tmp/fatecat-container-release-0043.json`
  - `/tmp/fatecat-local-ci-0043/release-artifacts/sbom.cyclonedx.json`
  - `/tmp/fatecat-local-ci-0043/release-artifacts/provenance.slsa.json`
  - `/tmp/fatecat-public-release-0043/rollback-drill.json`
- 命令已执行并输出 `/tmp/fatecat-live-release-gate-public-hf-0043.json`。
- 结果：`status=passed`、`shipGate=blocked`、`passed=7`、`pending=3`、`failed=0`。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 外部验证必须真实 | 只记录实际命令输出 |
| 不伪造 token | Telegram Bot 保持 pending |
| 不伪造 CI | 远端 GitHub Actions 当前 commit 保持 pending |
| 不伪造 clean git | 当前 worktree dirty，clean git 保持 pending |

# Change Boundary
- 可改：0044 task docs、roadmap。
- 禁改：生产服务、token、Git history、远端 CI、Bot 配置。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| HF Space 后续状态变化 | 证据记录当前执行时间和 JSON 文件路径 |
| 把公开 HF 当作私有生产域名 | 文档明确只验证 `tradecatlabs-fatecat.hf.space` |
| 误报全部 ship-ready | `shipGate` 仍 blocked，pending 3 项保留 |

# Assumptions and Falsification
- 假设：公开 HF Space 可作为当前 Web/API live smoke 证据。
- 反证：若该 URL 下线或返回不含 marker，未来 gate 会回到 pending/fail。
- 调试模式: `Optional`

# Critical Ambiguities
- 无阻断歧义。Bot token、远端 CI 和 clean git 不在本任务范围。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | 执行公开 HF/API live gate |
| TP-02.01 | 记录 JSON 摘要 |
| TP-03.01 | 更新 roadmap 和 closeout |
