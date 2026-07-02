# Repo Evidence
- 0012 已新增 `fate_core/capabilities/providers.py`、`list_providers()`、`get_provider()`、`ProviderMetadata`、`ProviderHealth`。
- `main.py` 已能在 capability payload 中嵌入 provider metadata，但还没有 provider 资源集合入口。
- `contracts/fate/capabilities/schemas/resource.schema.json` 已声明 `Provider` resource type 与 `providerResourceFields`。
- 执行前 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 仍把 provider schema 独立资源端点列为后续切片；本轮已把该项落地。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| Provider registry 已在 fate-core | API 只读取 registry，不复制 provider 清单。 |
| planned capability 无 production provider | `/providers` 只列 production provider，planned 通过 capability admission 解释。 |
| 本地 health 非外部连通 | 文档必须说明 provider health 只代表进程内 adapter。 |
| 不改计算结果 | 只加发现入口和 schema。 |

# Change Boundary
- 可改：provider schema、`main.py` provider API、API tests、API 文档、100% 计划、0013 任务文档。
- 不改：具体 provider registry、算法 usecase、job manager、Web UI。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| provider_id 含斜杠/点导致路径问题 | detail endpoint 访问失败 | 当前 provider_id 使用点号模块路径，可直接作为 path segment；后续如出现 slash 再 encode。 |
| health 被误解为生产连通 | 过度承诺 | 文档写明本地 in-process adapter health。 |
| list endpoint 与 capability provider 字段不一致 | 审计漂移 | API tests 对 capability links 和 providers 集合做一致性断言。 |

# Assumptions and Falsification
- Target end state: Provider 与 Capability 一样是可发现、可审计、可链接的基础设施资源。
- Real constraints: provider_id 当前等于 Python 模块路径，外部 API 需稳定承载这个 ID。
- Inertia constraints: 不能因为 `metadata.provider` 已存在就放弃独立 Provider resource。
- Wrong concept / wrong boundary: provider 只藏在 capability payload 里，开发者无法独立审计 provider registry。
- Kill list: 无独立 provider 发现入口。
- Proof point: `/providers` 和 `/providers/{provider_id}` tests 通过，OpenAPI 包含入口，docs 同步。
- Falsifier: 如果 `/providers` 与 capability registry 的 production provider 不一致，本切片失败。
- Migration slice: 先做只读 provider resource；后续再加外部 health、trace 和 provider event。
- Rejected short-term patches: 不在文档里手写 provider 表替代 API。

# Critical Ambiguities
- 无阻塞歧义。provider id URL 编码策略后续在出现特殊字符 provider 时再升级。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；若失败，最小复现命令为 `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k provider`。

# Task Package Context Map
| Node | Required Context |
| --- | --- |
| TP-01.01 | `resource.schema.json`、provider metadata 字段 |
| TP-01.02 | `_capability_schema_refs()` |
| TP-02.01 | `list_providers()`、`get_provider()` |
| TP-02.02 | `_capability_resource_payload()` links |
| TP-03.01 | API regression tests |
| TP-03.02 | API docs and 100% plan |
| TP-04.01 | pytest、ruff、mypy、quick CI、governance validators |
| TP-04.02 | 0013 task docs and INDEX |
