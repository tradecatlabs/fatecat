# Repo Evidence
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py` 已是 production provider registry 真相源，负责包装 bazi、almanac、ziwei、meihua usecase。
- `contracts/fate/capabilities/schemas/provider.schema.json` 和 `resource.schema.json` 已承载 Provider resource 字段，但本任务前生命周期字段不足。
- `tools/reference-repos/vendor_sources.json` 是成熟开源/供应链登记入口，本任务前 `iztro` 仍偏未来候选口径。
- `scripts/local-ci.sh` 是 quick gate 聚合入口，适合接入本地 provider lifecycle gate。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已将 provider lifecycle、source/license、version lock 列为测算基础设施剩余缺口。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 胶水原则 | provider metadata 必须说明项目 usecase、成熟库或 vendor source，而不是只写自有名词。 |
| 本地可验证 | gate 只读仓库文件、provider metadata 和 vendor manifest，不读取真实 `.env`、token 或用户输入。 |
| 不夸大 | `health` 仍限定为 in-process，不代表真实外部服务连通。 |
| 供应链 | production provider 引用 `vendor_sources.json#id` 时，该 vendor 必须 `productionUseAllowed=true` 且 `licenseStatus=spdx`。 |
| 退役治理 | provider 必须声明 `deprecation` policy，防止生产 provider 被无迁移窗口删除。 |
| 路线图 | 本轮只能关闭本地 baseline；external dependency smoke、trace span 和人工法律审计仍待后续任务。 |

# Change Boundary
- 可改：`providers.py`、capability schemas、`vendor_sources.json`、provider lifecycle gate scripts/tests、`local-ci.sh`、docs/AGENTS/roadmap/task docs。
- 不改：底层命理算法、Markdown 报告结构、Web UI、Telegram Bot、生产部署脚本语义、真实外部凭证。

# Risk Matrix
| 风险 | 级别 | 缓解 |
| --- | --- | --- |
| metadata 字段存在但无门禁 | High | 新增 `scripts/provider-lifecycle-gate.py` 并接入 quick CI。 |
| vendor source 生产使用口径不一致 | High | gate 校验 `productionUseAllowed` 与 SPDX 状态；`iztro` 明确提升为紫微 production dependency。 |
| provider health 被误解为外部 live | Medium | API 文档写明 `healthScope=in-process` 和外部连通待执行。 |
| 生命周期字段漂移 | Medium | 回归测试同时覆盖 schema、runtime metadata 和 API `/providers` 输出。 |
| 供应链法律审计被误宣称完成 | High | 文档和任务反范围明确保留人工法律复核。 |

# Assumptions and Falsification
- 假设：当前 provider lifecycle gate 的最低充分门槛是字段完整、路径存在、供应链生产许可和版本锁一致。反证：若生产准入要求真实动态依赖探测，则进入 external dependency smoke 任务。
- 假设：`iztro` 可作为紫微 production dependency 登记。反证：许可证或构建产物审计发现不能分发，则必须降级紫微 provider 或替换供应链。
- 假设：provider 退役只需先有 policy，不需要当前实现迁移工具。反证：出现实际 deprecated provider 后，必须增加 migration runner 和 release gate。

# Critical Ambiguities
- 真实生产环境中的 provider dependency live smoke 形式未定：进程内 import、样例计算、远端服务 ping 或 SBOM attest。
- 人工法律复核的 owner、频率和证据存储位置未定。
- trace span 的 provider lifecycle attribute 命名未定，留到 observability 深化任务。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；不需要 `DEBUG.md`。
- 若 gate 失败，必须记录失败 provider id、失败字段、命令和修复后回归结果。

# Task Package Context Map
| Area | Files |
| --- | --- |
| Runtime | `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py` |
| Contracts | `contracts/fate/capabilities/schemas/provider.schema.json`, `contracts/fate/capabilities/schemas/resource.schema.json` |
| Supply Chain | `tools/reference-repos/vendor_sources.json` |
| Scripts | `scripts/provider-lifecycle-gate.py`, `scripts/provider-lifecycle-gate.sh`, `scripts/local-ci.sh` |
| Tests | `tests/regression/test_provider_lifecycle_gate.py`, `tests/regression/test_capability_protocol.py`, `tests/regression/test_api_contracts.py` |
| Docs | `docs/reference-materials/operations/测算基础设施 API 接入.md`, `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`, directory `AGENTS.md` |
