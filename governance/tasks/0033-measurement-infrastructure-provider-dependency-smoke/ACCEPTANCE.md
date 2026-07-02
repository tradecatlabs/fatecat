# Task-Level Acceptance
- `scripts/provider-dependency-smoke.sh` 可本地执行并输出 JSON summary。
- summary 覆盖所有 production capability/provider，当前 providerCount=4。
- 每个 provider 使用 `CapabilityExecutor` 真实执行 fixed fixture，不旁路 provider。
- summary 只保留 key 摘要，不保存完整报告正文或真实用户输入。
- quick local-ci 包含 provider dependency smoke 和 pytest。
- docs/AGENTS/roadmap 明确本轮不是真实公网外部依赖 live smoke。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| provider dependency smoke | `bash scripts/provider-dependency-smoke.sh --output-json /tmp/fatecat-provider-dependency-smoke.json` | Passed |
| smoke JSON parse | `python3 -m json.tool /tmp/fatecat-provider-dependency-smoke.json` | Passed |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_provider_dependency_smoke.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema'` | Passed; 13 passed |
| ruff check | `.venv/bin/python -m ruff check scripts/provider-dependency-smoke.py tests/regression/test_provider_dependency_smoke.py scripts/provider-lifecycle-gate.py tests/regression/test_provider_lifecycle_gate.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check scripts/provider-dependency-smoke.py tests/regression/test_provider_dependency_smoke.py scripts/provider-lifecycle-gate.py tests/regression/test_provider_lifecycle_gate.py` | Passed |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-dependency-smoke` | Passed; 106 passed |

# Review Gate
- 检查 smoke 是否通过 `CapabilityExecutor`，而不是直接调用 usecase。
- 检查 artifact 是否只保存摘要，不保存完整报告。
- 检查 docs 是否标注真实外部连通验证待执行。
- 检查 quick CI 顺序是否仍先清理 runtime，再跑 vendor health。

# Runtime Verification Gate
- provider dependency smoke、focused tests、quick local-ci、task closeout validator 和 task tree validator 已通过。
- 外部连通验证待执行：真实公网 API、真实 token、Bot、webhook、生产 provider 远端依赖。

# Ship Readiness
- 本地 dependency smoke baseline 已完成，可进入 provider trace span 或八字/紫微 L4 golden evidence。
- 不可声明 provider 外部依赖 live 已完成：真实网络、真实账号、SLA、retry 和 trace 仍未实现。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | smoke script 与 local-ci hook 落地。 |
| TP-03 | smoke、focused tests 和 quick CI 通过。 |
| TP-04 | docs/AGENTS/roadmap 同步且 closeout packet 生成。 |

# Anti-Goals
- 不做真实公网外部依赖 live smoke。
- 不接 OpenTelemetry trace span。
- 不生成 SBOM/provenance。
- 不新增 provider 或改变算法输出。
