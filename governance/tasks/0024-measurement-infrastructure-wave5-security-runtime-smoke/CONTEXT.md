# Repo Evidence
- 调试模式: Optional
- `contracts/fate/security/registry.json` 已存在 SecurityControl 资源发现层，原先缺少本地 runtime smoke 入口。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已有响应安全头、请求体限制、rate limit、API token、user token 和 records enabled 边界。
- `scripts/check-privacy-fixtures.sh`、`scripts/check-source-hygiene.sh`、`scripts/check-public-release-policy.sh` 已存在本地文件门禁，可被 security smoke 串联。
- `tests/regression/test_api_contracts.py` 与 `tests/regression/test_capability_protocol.py` 已覆盖 registry/API payload，可扩展 security metadata 断言。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 记录了安全治理未完成项，需要同步本地 smoke 进度和后续缺口。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不泄露真实 token/secret/DSN | smoke 只使用本地测试 token 字符串，不输出密钥值，不读取真实 `.env`。 |
| 不伪造生产验证 | 文档和 registry 只声明 TestClient 本地 smoke，不写真实域名/CORS/token/Bot live 已完成。 |
| 不扩大业务边界 | 只新增 smoke、metadata、测试和文档，不重构 API 鉴权模型。 |
| 可复核 | smoke 输出 JSON，测试覆盖函数与 CLI，quick CI 收入口。 |
| 调试模式 | Optional；本任务是运行时 smoke 加固，不是已复现 bug。 |

# Change Boundary
- 可改：`scripts/security-smoke.py`、`scripts/security-smoke.sh`、`contracts/fate/security/registry.json`、相关 `AGENTS.md`、回归测试、local CI focused list、API 文档、roadmap、0024 任务文档。
- 不改：真实生产配置、secret、部署凭证、业务算法、报告生成、provider executor、数据库 schema。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| smoke 只验证本地 TestClient，被误读成公网生产安全验收 | 审计结论夸大 | registry、docs、acceptance 明确生产外部验证待执行。 |
| monkeypatch main 全局变量污染测试 | 后续测试不稳定 | smoke 用 context manager 保存/恢复属性和环境变量。 |
| 运行 file gates 太慢或依赖缺失 | 本地 smoke 不稳定 | CLI 支持 `--skip-file-gates`，测试用跳过文件门禁路径，正式 smoke 默认执行文件门禁。 |
| security registry metadata 与 API payload 漂移 | 发现层与执行入口不一致 | contract/API tests 增加 `smokeCommand` 与 scope 断言。 |

# Assumptions and Falsification
- 假设：现有 delivery app 可以通过 TestClient 覆盖当前安全控制。若 import app 或路由失败，focused tests 会失败。
- 假设：privacy/source/public-release 文件门禁已可本地运行。若任一脚本失败，默认 security smoke 会失败。
- 假设：本任务不需要真实外部凭证。若需要验证生产 token、CORS、Bot webhook，则必须另起生产实测任务。

# Critical Ambiguities
- 真实生产域名、真实 token、Bot live smoke 尚无可用凭证和环境；本任务不处理，标记为外部连通验证待执行。
- OAuth/OIDC、RBAC、审计日志、retention 和专用 secret scanner 尚未设计完成；本任务只登记为后续安全基础设施缺口。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md` 根因闭环。
- 若 smoke 或 quick CI 失败，失败命令、错误摘要和修复证据必须回填 `STATUS.md` Evidence Log。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 读取 security registry、delivery app 安全控制、本地门禁脚本和 roadmap。 |
| TP-02 | 新增 smoke，确保属性/env 恢复，不保存真实敏感数据。 |
| TP-03 | 补函数测试、CLI 测试、registry/API 断言、quick CI 和文档。 |
| TP-04 | 执行 smoke、focused tests、ruff/format、quick CI、diff check 和 task validators。 |
