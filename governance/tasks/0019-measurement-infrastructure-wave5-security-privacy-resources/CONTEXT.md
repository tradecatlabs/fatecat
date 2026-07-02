# Repo Evidence
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已存在 `_require_record_access`、`_require_owner_or_admin`、`_check_rate_limit`、`RequestBodyLimitMiddleware`、`_apply_public_response_headers` 和 `production_guardrails`。
- `domains/experience-delivery/services/fatecat-delivery/src/service_config.py` 已存在 `cors_allow_origins()`。
- `scripts/check-source-hygiene.sh` 已检查 raw、运行态、缓存、数据库、日志和本机个人路径误入 Git。
- `scripts/check-privacy-fixtures.sh` 已检查一线代码、文档、测试和 vendor web 隔离示例。
- `scripts/check-public-release-policy.sh` 已检查 public release workflow 与 HF 默认隐私策略。
- `scripts/production-readiness.sh` 已检查 CORS allowlist、token 口径、限流、请求体、HSTS、真实 API 与 Bot live smoke。
- `scripts/local-ci.sh --profile quick` 已串联 source hygiene、privacy fixtures、public release policy 和 focused regression。
- `contracts/fate/evaluations/` 与 `contracts/fate/observability/` 已提供同类资源发现模式。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不泄露真实密钥 | registry 只列 env var 名称，不写真实值 |
| 不伪造外部验证 | production readiness 统一标记 `external_connectivity_pending` |
| 不改变鉴权行为 | 只增加资源发现 API，不改 `_require_record_access` 逻辑 |
| 不扩大安全承诺 | 明确 shared token 不是 OAuth/OIDC，多租户 RBAC 后续实现 |
| 文档要可复核 | 每个 control 绑定 implementationRefs 与 localVerification |

# Change Boundary
- Allowed: `contracts/fate/security/`、`resource.schema.json`、`main.py` 只读 API、contract/API tests、API 文档、100% 路线图、任务文档。
- Forbidden: 改鉴权执行路径、改 records 数据模型、接入外部安全平台、提交真实 secret、执行 live Bot 或真实域名 smoke。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把本地控制写成生产已验证 | 审计误判 | `externalConnectivity` 明确分层 |
| registry 泄露 env 值 | 高危安全泄露 | 只允许 env var 名称和实现路径 |
| SecurityControl 与脚本漂移 | 文档失真 | 测试锁定关键 control 与命令 |
| 过度实现安全平台 | 范围失控 | 本轮只做发现层，不接外部平台 |

# Assumptions and Falsification
- 假设：现有脚本是当前安全/隐私/发布门禁真相源。
- 证伪：若脚本不存在、命令失败或 main.py 不含对应实现，则不得登记为 `available`。
- 假设：`/security` 可按 `/evaluations`、`/observability` 同型实现。
- 证伪：若 OpenAPI、metadata 或 focused tests 无法稳定覆盖，则回退到纯文档登记。

# Critical Ambiguities
- 专用 secret scanner、OAuth/OIDC、RBAC、审计日志留存、数据 retention policy 尚未实现；本任务只登记缺口。
- 真实生产 API 域名、CORS、token 与 Bot live smoke 当前仓库内无法验证，必须保留“外部连通验证待执行”。

# Debug Evidence Contract
- 调试模式: Optional

- 本任务不是 bugfix，无需 `DEBUG.md`。
- 若 API endpoint 或 schema 测试失败，最小复现命令写入 `STATUS.md`。

# Task Package Context Map
| Path | Role |
| --- | --- |
| `contracts/fate/security/registry.json` | SecurityControl 资源真相源 |
| `contracts/fate/security/schemas/security-control.schema.json` | SecurityControl 字段契约 |
| `contracts/fate/capabilities/schemas/resource.schema.json` | 统一资源模型 |
| `domains/experience-delivery/services/fatecat-delivery/src/main.py` | API 只读发现入口 |
| `tests/regression/test_capability_protocol.py` | 契约回归 |
| `tests/regression/test_api_contracts.py` | API/metadata/OpenAPI 回归 |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | 开发者接入说明 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 100% 路线图 |
