# Task-Level Acceptance
- production provider metadata 固定输出 `versionLock`、`lifecycle`、`sourcePolicy`、`licensePolicy`、`resourceManifest`、`promotionGate`、`deprecation`。
- Provider/resource schema 声明 lifecycle 字段、必填字段、枚举和供应链 production use invariant。
- `scripts/provider-lifecycle-gate.sh` 可本地执行，校验 4 个 production provider 覆盖、版本锁、路径引用、vendor 生产许可和 SPDX 状态。
- `iztro` 在 `vendor_sources.json` 中明确作为紫微 production dependency，且不再停留在 future candidate 口径。
- API `/providers` 输出 lifecycle 字段，测试覆盖 provider runtime metadata、schema 和 API 资源。
- quick local-ci 包含 provider lifecycle gate。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| provider schema parse | `python3 -m json.tool contracts/fate/capabilities/schemas/provider.schema.json` | Passed |
| resource schema parse | `python3 -m json.tool contracts/fate/capabilities/schemas/resource.schema.json` | Passed |
| vendor manifest parse | `python3 -m json.tool tools/reference-repos/vendor_sources.json` | Passed |
| provider lifecycle gate | `bash scripts/provider-lifecycle-gate.sh --output-json /tmp/fatecat-provider-lifecycle.json` | Passed |
| focused provider tests | `.venv/bin/python -m pytest -q tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py -k 'provider or schema' tests/regression/test_api_contracts.py -k provider` | Passed |
| broader related tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py tests/regression/test_provider_lifecycle_gate.py` | Passed; 87 passed |
| ruff check | `.venv/bin/python -m ruff check domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py scripts/provider-lifecycle-gate.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py scripts/provider-lifecycle-gate.py tests/regression/test_provider_lifecycle_gate.py tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py` | Passed |
| vendor health | `bash scripts/clean-runtime.sh && bash scripts/vendor-health.sh` | Passed |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-provider-lifecycle` | Passed; 104 passed |

# Review Gate
- 检查 provider resource/API/schema 三者 lifecycle 字段是否同源。
- 检查 supplyChainRefs 是否都能回到 `vendor_sources.json` 具体 id。
- 检查文档是否仍明确“外部连通验证待执行”。
- 检查新增 gate 是否没有读取真实用户输入、报告正文、token、secret 或 `.env`。

# Runtime Verification Gate
- focused tests、provider lifecycle gate、vendor health 和 quick local-ci 已通过。
- task closeout validator 已通过。
- 外部连通验证待执行：真实 provider 外部依赖、生产 trace/metrics、供应链人工法律复核、真实 token/Bot/API。

# Ship Readiness
- 本地 lifecycle baseline 已完成，可进入下一阶段 external dependency smoke / trace span。
- 不可声明 provider 生命周期 100% 生产闭环：SBOM、法律审计、动态依赖探测、真实生产观测和 release promotion workflow 仍未完成。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | runtime metadata、schema 和 vendor manifest 生命周期字段落地。 |
| TP-03 | provider lifecycle gate、回归测试和 quick CI 通过。 |
| TP-04 | docs/AGENTS/roadmap 同步且任务 closeout packet 生成。 |

# Anti-Goals
- 不做真实外部依赖 live smoke。
- 不接入 OpenTelemetry collector、trace backend 或 dashboard。
- 不做供应链许可证人工法律审计。
- 不新增 provider 或改变既有算法输出。
