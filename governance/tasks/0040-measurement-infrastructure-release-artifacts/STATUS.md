# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- None. 本地 SBOM/provenance release artifacts baseline 已完成。

# Task Package Status Table
| Node | Parent | Depth | Depends On | Parallelizable | Status | Recent Evidence | Blocker | Next Action |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | 2 | - | No | Done | 已盘点 0039 release gate、lockfile、Dockerfile 和供应链文档 | 无 | 无 |
| TP-02.01 | TP-02 | 2 | TP-01.01 | No | Done | 新增 `scripts/release-artifacts.py` 与 `scripts/release-artifacts.sh` | 无 | 无 |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | `bash scripts/release-artifacts.sh --output-dir /tmp/fatecat-release-artifacts-0040` -> PASS，artifacts=2 | 无 | 无 |
| TP-03.01 | TP-03 | 2 | TP-02.02 | No | Done | `scripts/public-release-gate.sh` 与 `scripts/local-ci.sh` 已接入 release artifacts | 无 | 无 |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | `live-release-gate` 对 `evidence.sbom_artifact` 和 `evidence.provenance_artifact` 返回 `pass`，`shipGate` 仍 blocked | 无 | 无 |
| TP-04.01 | TP-04 | 2 | TP-03.02 | No | Done | `tests/regression/test_release_artifacts.py` 通过 | 无 | 无 |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | release gate contract、registry、AGENTS、API 文档、roadmap 已同步 | 无 | 无 |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Done | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0040` -> PASS，`123 passed in 76.14s`；`FATECAT_PUBLIC_RELEASE_SMOKE_PORT=8018 bash scripts/public-release-gate.sh --output /tmp/fatecat-public-release-0040 --skip-local-ci` -> PASS；closeout ready | 无 | 无 |

# Blockers
- 真实生产发布仍未完成：container digest、registry signature、远端 CI attestation、GitHub release artifact、rollback drill、真实 API/HF/Bot live evidence 仍待外部环境。

# Runtime State
- No long-running process.
- Generated local evidence under `/tmp/fatecat-release-artifacts-0040` during validation.
