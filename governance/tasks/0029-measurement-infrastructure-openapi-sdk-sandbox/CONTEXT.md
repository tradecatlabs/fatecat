# Repo Evidence
- 调试模式: Optional
- FastAPI 已内置 `/openapi.json`，但本地没有独立 OpenAPI 导出脚本和必备路径校验。
- `docs/reference-materials/operations/测算基础设施 API 接入.md` 已列出 API 发现入口，但原先缺少 developer sandbox 和 SDK 示例入口。
- quick CI 已覆盖结构、卫生、security、observability 等 smoke，但原先没有 developer docs smoke。
- `almanac` 和 `meihua` 可通过 `/capabilities/{capability_id}/calculate` 本地执行，适合作为不包含出生隐私的 sandbox 示例。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 隐私边界 | 示例只使用北京和测试样本，不保存真实 token、生产 URL、真实用户输入、非北京真实地区或报告正文。 |
| 最小实现 | 复用 FastAPI `app.openapi()` 和 `TestClient`，不引入 SDK generator、新依赖或公网服务。 |
| 可重复验证 | OpenAPI 导出、developer docs smoke 和 focused tests 都可本地执行。 |
| 不夸大生产能力 | 文档明确本轮不是公网 sandbox token、发布版 SDK 或开发者门户。 |
| CI 覆盖 | quick CI 串联 developer docs smoke 和回归测试。 |

# Change Boundary
- 可改：`contracts/fate/developer/`、`docs/reference-materials/developer/`、`scripts/export-openapi.*`、`scripts/developer-docs-smoke.*`、`scripts/local-ci.sh`、regression tests、API 文档、roadmap、目录级 AGENTS、0029 任务文档。
- 不改：FastAPI 路由行为、capability 计算逻辑、数据库 schema、生产凭证、Web UI、Bot、真实外部服务。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 示例泄露真实数据 | 隐私和审计风险 | fixture 和示例只允许北京/测试样本，secret scan 与 docs smoke 检查边界。 |
| OpenAPI 导出变成无校验 dump | 开发者契约漂移 | 导出脚本校验必备路径和 operationId 唯一性。 |
| 本地 fixture 被误读成真实 sandbox | 产品口径夸大 | README、API 文档、roadmap、任务文档都说明不是公网 sandbox token 服务。 |
| docs smoke 保存报告正文 | 隐私与仓库膨胀 | smoke summary 只保存检查名、路径和状态，不保存正文。 |
| quick CI 变慢 | 开发体验下降 | 使用 TestClient 和静态检查，不启动网络服务或容器。 |

# Assumptions and Falsification
- 假设：开发者接入 D0 baseline 可先用 OpenAPI artifact、fixture、示例和 docs smoke 表达。反证：如果第三方需要真实账号、quota、计费、门户，必须进入后续公网开发者平台任务。
- 假设：`almanac`/`meihua` 适合 sandbox，因为不需要出生隐私。反证：若未来必须展示八字能力，应新增脱敏八字 fixture 和输出 snapshot gate。
- 假设：本地示例不需要发布版 SDK。反证：如果对外发布需要语言包和版本兼容，则升级到 SDK 发布任务。

# Critical Ambiguities
- 正式 API 版本策略和 changelog 仍未定义；本任务只登记缺口。
- 公网 sandbox token 生成、权限、限流和留存策略未定义；本任务不实现。
- 是否需要 OpenAPI schema 分组、tag 规范和 SDK generator 尚未确定；本任务只做最小 artifact。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 若 OpenAPI/docs smoke 失败，必须记录失败命令、原因和修复结果到 `STATUS.md`。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 盘点 OpenAPI、API 文档、示例和 local-ci 缺口。 |
| TP-02 | 新增 developer sandbox fixture 和最小示例。 |
| TP-03 | 新增 OpenAPI 导出、developer docs smoke、回归测试和 quick CI 接入。 |
| TP-04 | 同步文档、执行门禁并 closeout。 |

# Blockers
- 无当前本地阻塞。
- 外部连通验证待执行：公网 sandbox token、开发者门户、真实开发者账号、发布版 SDK、生产域名。
