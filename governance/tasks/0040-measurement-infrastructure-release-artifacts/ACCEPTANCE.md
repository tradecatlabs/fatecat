# Task-Level Acceptance
- `scripts/release-artifacts.sh` 可生成 SBOM、provenance 和 manifest。
- 生成的 SBOM 为 CycloneDX 兼容 JSON，包含 project 与 lockfile dependency components。
- provenance 为 in-toto statement + SLSA v1 predicate 风格，记录 git commit、dirty 状态、核心材料 hash 和 SBOM digest。
- manifest 记录 artifact path、size、sha256、privacyBoundary 和 limitations。
- `scripts/live-release-gate.sh` 能消费生成的 `--sbom-path` 和 `--provenance-path`，对应 checks 为 `pass`。
- 文档明确本地 baseline 不等于远端 CI attestation、registry signature 或 container digest。

# Validation Plan
| 验证项 | 命令 | 结果口径 |
| --- | --- | --- |
| Shell syntax | `bash -n scripts/release-artifacts.sh scripts/local-ci.sh scripts/public-release-gate.sh` | 必须通过 |
| Artifact generate | `bash scripts/release-artifacts.sh --output-dir /tmp/fatecat-release-artifacts-0040` | 必须通过 |
| Artifact verify | `bash scripts/release-artifacts.sh --verify-dir /tmp/fatecat-release-artifacts-0040` | 必须通过 |
| Gate consume | `bash scripts/live-release-gate.sh --sbom-path ... --provenance-path ...` | SBOM/provenance checks pass |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_release_artifacts.py` | 必须通过 |
| Ruff | `.venv/bin/python -m ruff check scripts/release-artifacts.py tests/regression/test_release_artifacts.py` | 必须通过 |
| Task docs | `validate_task_docs.py --phase closeout` | 必须通过 |

# Review Gate
- 不读取环境变量 secret。
- 不把 dirty worktree 写成 release-ready。
- 不把本地 artifact 写成远端 attestation。
- 不生成或宣称 container digest。

# Runtime Verification Gate
- 当前只执行本地 artifact generate/verify。
- 外部连通验证待执行：registry、远端 CI、GitHub release artifact、container digest、rollback drill。

# Ship Readiness
- 0040 本地 baseline：Ready。
- FateCat 100% 真实生产发布：仍 blocked by external evidence。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | 缺口来自真实文件和命令 |
| TP-02.01 | 脚本入口存在且无新依赖 |
| TP-02.02 | artifact 生成和 verify 通过 |
| TP-03.01 | public/local gate 接入 |
| TP-03.02 | live release gate 消费 artifact |
| TP-04.01 | 回归测试覆盖 |
| TP-04.02 | 文档同步不夸大 |
| TP-05.01 | closeout 可复核 |

# Anti-Goals
- 不推送 registry。
- 不生成真实 container digest。
- 不伪造远端 CI attestation。
- 不输出真实 token、secret、DSN、用户报告或生产日志。
