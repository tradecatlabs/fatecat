# Repo Evidence
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 将 `MI-04.03 provider health 和 external dependency smoke` 列为未完成缺口。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py` 是统一 capability 执行入口，可真实覆盖 provider validate/calculate。
- `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/providers.py` 已在 0032 提供 provider lifecycle metadata 和 in-process health。
- `contracts/fate/capabilities/registry.json` 当前 production capability 为 bazi、ziwei、almanac、meihua。
- `scripts/local-ci.sh` 已有 smoke 聚合模式，适合加入 provider dependency smoke。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 不伪造 external live | 输出 `externalConnectivity=外部连通验证待执行`，只声明本地 fixture smoke。 |
| 同源执行 | 只通过 `CapabilityExecutor` 调用，不旁路 usecase 或 provider internals。 |
| 隐私 | 固定样例只用北京、测试用户、测试问题，不读取真实请求、报告正文、token、secret、DSN。 |
| 生产 provider 覆盖 | 遍历 capability registry 中 `status=production` 的能力，不手写 provider 清单作为真相源。 |
| 快速门禁 | 脚本输出机器可读 JSON，接入 quick local-ci 和 pytest。 |

# Change Boundary
- 可改：`scripts/provider-dependency-smoke.*`、`tests/regression/test_provider_dependency_smoke.py`、`scripts/local-ci.sh`、docs/AGENTS/roadmap/task docs。
- 不改：底层命理算法、provider registry 生产状态、API 响应契约、Web/Bot/CLI 行为、生产外部凭证。

# Risk Matrix
| 风险 | 级别 | 缓解 |
| --- | --- | --- |
| smoke 绕过真实 provider 链路 | High | 使用 `CapabilityExecutor` 作为唯一执行入口。 |
| 样例泄露真实用户信息 | High | 样例固定为北京/测试用户/测试问题。 |
| 本地 smoke 被误解为公网 live | High | 文档和 JSON 均标注外部连通验证待执行。 |
| quick CI 变慢 | Medium | 只跑 4 个 production capability 的最小 fixture。 |
| 输出报告正文进入 artifact | Medium | summary 只存 dataKeys/evidenceKeys/duration，不存完整 report/data。 |

# Assumptions and Falsification
- 假设：当前生产 provider 的最低依赖 smoke 是固定样例执行成功并有关键字段/evidence。反证：生产要求真实远端依赖或账号，则进入 live smoke 任务。
- 假设：北京/测试用户样例足以覆盖 provider 装配链路。反证：某 provider 只在特殊输入触发外部依赖，则必须增加 provider 专属 fixture。
- 假设：summary 只保存 key 摘要即可审计。反证：需要字段级 snapshot，则进入 report snapshot/golden 任务。

# Critical Ambiguities
- 真实 external dependency live smoke 的目标服务、网络环境和凭证尚未定义。
- provider trace span 属性名和 collector 目标尚未定义。
- 是否需要 provider-specific retry/timeout policy 留到 MI-03.04 / MI-08。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；不需要 `DEBUG.md`。
- 若 smoke 失败，必须记录 capabilityId、providerId、失败字段、命令和修复后回归结果。

# Task Package Context Map
| Area | Files |
| --- | --- |
| Runtime | `scripts/provider-dependency-smoke.py`, `scripts/provider-dependency-smoke.sh`, `scripts/local-ci.sh` |
| Provider Runtime | `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py`, `providers.py`, `registry.py` |
| Tests | `tests/regression/test_provider_dependency_smoke.py` |
| Docs | `docs/reference-materials/operations/测算基础设施 API 接入.md`, `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`, `scripts/AGENTS.md`, `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/AGENTS.md` |
