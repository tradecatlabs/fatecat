# Task-Level Acceptance
- ReleaseGate 资源存在，required evidence 覆盖 local CI、remote CI、production API、HF Space、Telegram Bot、container digest、SBOM、provenance、rollback drill 和 clean git state。
- `scripts/live-release-gate.sh` 默认模式可本地运行并输出 JSON；缺真实外部证据时 `shipGate.status=blocked`。
- `scripts/live-release-gate.sh --require-live` 在缺真实外部证据时必须失败，不允许伪造 live 通过。
- `public-release-gate.sh` 和 `local-ci.sh --profile quick` 接入 release gate 合同检查。
- `/surfaces` API 响应暴露 `releaseGate` 元信息。
- 文档明确本轮不是生产 live 验收通过。

# Validation Plan
| 验证项 | 命令 | 结果口径 |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/delivery/release-gate.json` | 必须通过 |
| Shell syntax | `bash -n scripts/live-release-gate.sh scripts/public-release-gate.sh scripts/local-ci.sh` | 必须通过 |
| Gate dry run | `bash scripts/live-release-gate.sh --output-json /tmp/fatecat-live-release-gate-0039.json` | exit 0，`shipGate=blocked` |
| Focused tests | `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py ...` | 必须通过 |
| Ruff | `.venv/bin/python -m ruff check ...` | 必须通过 |
| Format | `.venv/bin/python -m ruff format --check ...` | 必须通过 |
| Task docs | `validate_task_docs.py --phase closeout` | 必须通过 |

# Review Gate
- 检查所有新增输出不包含真实 secret 值。
- 检查任何文档没有把本地 gate 通过写成 live release 通过。
- 检查新增脚本没有把外部依赖变成默认 CI 必需项。

# Runtime Verification Gate
- 当前只执行本地 contract gate。
- 外部连通验证待执行：生产 API、HF Space、Telegram Bot、GitHub Actions、container registry、SBOM/provenance artifact、rollback drill。

# Ship Readiness
- 0039 本地 baseline：Ready。
- FateCat 100% 真实生产发布：Blocked by external evidence。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | 缺口来自真实文件和命令，不凭记忆 |
| TP-02.01 | Contract/schema JSON 可解析且字段齐全 |
| TP-02.02 | delivery/resource registry 可发现 ReleaseGate |
| TP-03.01 | 脚本输出 JSON，可区分 local pass 与 ship blocked |
| TP-03.02 | public/local gate 已接入且不强制外部凭证 |
| TP-04.01 | 测试覆盖 local 与 require-live 两种模式 |
| TP-04.02 | API contract 测试覆盖 `/surfaces` |
| TP-05.01 | 文档同步，不夸大 |
| TP-05.02 | closeout 证据可复核 |

# Anti-Goals
- 不连接真实外部系统。
- 不输出真实 token、secret、DSN、私钥、生产日志正文或用户报告正文。
- 不宣称 live release ship gate 已通过。
