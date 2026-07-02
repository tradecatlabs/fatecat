# Repo Evidence
- `tests/regression/test_entrypoint_consistency.py` 已覆盖 API、Bot 路径和 Web 对 `calculate_delivery_result` 的核心字段一致性。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已提供 FastAPI canonical endpoints、Markdown report jobs 和 `/metadata`。
- `domains/experience-delivery/services/fatecat-delivery/src/web_report_service.py` 已通过 `calculate_delivery_result` 与 `generate_full_report` 构建 Web Markdown。
- `domains/experience-delivery/services/fatecat-delivery/src/bot.py` 已导入 `calculate_delivery_result` 与 `generate_full_report`。
- `domains/fate-analysis/services/fate-core/src/fate_core/cli.py` 已提供 `pure-analysis`、`capability`、`health`，但不生成标准 Markdown。
- `SKILL.md`、`references/commands.md` 和 `scripts/preflight.sh` 是 Agent Skill/本地运行入口。
- `docs/deployment/huggingface-space.md` 与 `infra/huggingface-space/` 是托管 Web 入口文档和容器上下文。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 多端不等于全部同输出格式 | CLI/Skill 标记 partial |
| Bot live 需要真实 token | `externalConnectivity=requires_real_credentials` |
| Hosted Web 需要真实平台 | `surface.huggingface_space` 标记 manual |
| 不保存运行时结果 | registry 只列 entrypoint、chain、contract、verification |
| 不改交付实现 | 本轮只做发现层和测试 |

# Change Boundary
- Allowed: `contracts/fate/delivery/`、`resource.schema.json`、`main.py` 只读 API、contract/API tests、API 文档、100% 路线图、任务文档。
- Forbidden: 改 Bot live 行为、改 Web UI 布局、改 CLI 输出格式、启动真实外部服务、执行真实 Telegram/HF/API live 验证。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 partial 入口写成完整 Markdown 同源 | 审计误判 | CLI/Skill 明确 partial |
| 把 Bot dry-run 写成 live | 生产风险 | externalConnectivity 标记真实凭证依赖 |
| DeliverySurface 与代码漂移 | 文档失真 | 测试锁定 canonicalChain 和 entrypoints |
| 过度做端到端 live | 范围失控 | 本轮只做本地发现与 contract tests |

# Assumptions and Falsification
- 假设：现有 API/Web/Bot/CLI/Skill 都可作为 delivery surfaces 被登记。
- 证伪：若没有入口、验证命令或 owner，则不得登记为 available。
- 假设：`/surfaces` 可按 `/security`、`/observability` 同型实现。
- 证伪：若 OpenAPI、metadata 或 focused tests 无法稳定覆盖，则回退到纯文档登记。

# Critical Ambiguities
- CLI 当前不生成标准 Markdown；只能算 JSON/capability surface。
- Skill 当前是安装与运行说明入口，不是独立线上服务。
- Bot live、HF Space、公网 API、多浏览器和完整 Markdown byte-level diff 仍需后续外部验证。

# Debug Evidence Contract
- 调试模式: Optional

- 本任务不是 bugfix，无需 `DEBUG.md`。
- 若 API endpoint 或 schema 测试失败，最小复现命令写入 `STATUS.md`。

# Task Package Context Map
| Path | Role |
| --- | --- |
| `contracts/fate/delivery/registry.json` | DeliverySurface 资源真相源 |
| `contracts/fate/delivery/schemas/delivery-surface.schema.json` | DeliverySurface 字段契约 |
| `contracts/fate/capabilities/schemas/resource.schema.json` | 统一资源模型 |
| `domains/experience-delivery/services/fatecat-delivery/src/main.py` | API 只读发现入口 |
| `tests/regression/test_entrypoint_consistency.py` | API/Bot/Web 同源链路现有回归 |
| `tests/regression/test_capability_protocol.py` | 契约回归 |
| `tests/regression/test_api_contracts.py` | API/metadata/OpenAPI 回归 |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | 开发者接入说明 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 100% 路线图 |
