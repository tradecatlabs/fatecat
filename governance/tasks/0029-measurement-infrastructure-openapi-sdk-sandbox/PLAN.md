# Planning Summary
本轮把 D0 开发者接入面从“文档描述”推进到“本地可执行 baseline”：OpenAPI 可导出、sandbox fixture 可执行、示例可静态检查、docs smoke 进入 quick CI。

# Lifecycle Gates
- SPEC：确认范围只覆盖本地开发者 baseline。
- PLAN：任务树、风险、out-of-scope、验证命令落盘。
- BUILD：新增 developer fixture、示例、OpenAPI 导出脚本、docs smoke。
- TEST：JSON、shell syntax、py_compile、OpenAPI 导出、docs smoke、focused tests、ruff/format、secret scan、quick CI、diff check。
- REVIEW：检查文档不夸大公网 sandbox、SDK 发布或生产门户；检查示例不泄露真实数据。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
复用 FastAPI `app.openapi()` 和 `TestClient`，不引入 OpenAPI generator、SDK generator、新依赖或公网服务。SDK 示例保持最小可读片段，发布版 SDK 留给后续任务。

# Split Strategy
先落契约和示例，再落脚本与测试，最后接入 local-ci 并同步文档。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 现状和任务契约 |
| Wave 2 | TP-02 | fixture 与示例 |
| Wave 3 | TP-03 | OpenAPI/docs smoke/CI |
| Wave 4 | TP-04 | 文档、验证、closeout |

# Runtime Workflow Contract
- `bash scripts/export-openapi.sh --output <path>` 导出 OpenAPI JSON，并校验必备路径和 operationId 唯一性。
- `bash scripts/developer-docs-smoke.sh --output-json <path> --openapi-json <path>` 使用 `TestClient` 执行 fixture 与示例静态检查。
- quick CI 默认执行 developer docs smoke，并把 OpenAPI 和 docs smoke summary 写入本地 evidence 目录。

# Next Executable Leaves
- TP-04.02：执行完整 quick CI、secret scan、diff check、task validators 和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Future-Optimal Contract
Target end state: FateCat 的开发者接入面具备机器契约、sandbox、SDK 示例、docs smoke、版本兼容策略和外部开发者门户。

Real constraints: 当前没有公网 sandbox token 服务、开发者账号系统或发布版 SDK；本任务必须保持本地可验证、不接真实外部服务。

Inertia constraints: 仅靠 README 列 endpoint、依赖 FastAPI 默认 `/docs`、人工复制 curl 的旧口径不能成为最终接入面。

Kill list: “文档写了就算可接入”“OpenAPI 只靠手动访问”“示例不进 CI”“本地 fixture 等同真实 sandbox token 服务”。

Proof point: `export-openapi.sh`、`developer-docs-smoke.sh`、回归测试和 quick CI 都能证明开发者 baseline 可重复执行。

Falsifier: OpenAPI 缺必备路径、docs smoke 不能执行 fixture、示例语法错误或 CI 未覆盖，则本任务失败。

Migration slice: 本轮完成本地 baseline；后续可在此基础上增加固定输出 snapshot、API changelog、发布版 SDK 和开发者门户。

Rejected short-term patches: 不只更新 README；不引入未使用的 SDK generator；不伪造公网 sandbox token；不保存真实报告正文 fixture。

# Ponytail Contract
Existence check: 开发者接入是基础设施 D0 必备能力，OpenAPI artifact、fixture、示例和 docs smoke 都有当前验收用途。

Selected ladder rung: 复用 FastAPI OpenAPI 与 TestClient，新增薄脚本和文档，不引入新依赖。

Skipped scope: SDK 包发布、OpenAPI schema 分组、固定输出 snapshot、公网 sandbox token、开发者门户、API changelog。

Ceiling / upgrade path: 当对外提供第三方开发者接入时，升级为正式 SDK、真实 sandbox 账号、版本策略和门户。

Do-not-simplify: 隐私边界、必备路径校验、示例静态检查、quick CI 接入必须保留。

Minimal runnable check: OpenAPI 导出、developer docs smoke、focused regression、quick CI。

Complexity review owner: auto-review/document-drift/ponytail-complexity/security。

# Documentation Impact
Operating model update: not needed；项目定位不变。

Toolchain model update: updated；新增 `export-openapi` 和 `developer-docs-smoke` 本地工具入口。

Process update: updated；quick CI 新增 developer docs smoke。

Source-of-truth updates: updated；developer fixture、developer docs、API 接入文档、roadmap 和 AGENTS 已同步。

Local README/AGENTS impact: updated；`scripts/AGENTS.md`、`contracts/fate/AGENTS.md`、`docs/reference-materials/AGENTS.md` 已补入口。

Contract/catalog/schema impact: updated；新增 `contracts/fate/developer/sandbox.json`。

ADR/Gate/module-context impact: not needed；本任务不改变架构边界，只补开发者接入 baseline。

Documentation exemption reason: 不新增 ADR；公网开发者门户和 SDK 发布再记录架构决策。

Validation evidence: 见 `STATUS.md`。

# Rollback Protocol
- 删除 `scripts/export-openapi.*`、`scripts/developer-docs-smoke.*` 和 developer docs smoke CI 接入。
- 删除 `contracts/fate/developer/` 与 `docs/reference-materials/developer/` 本轮新增内容。
- 恢复 API 文档、roadmap、AGENTS 和 0029 任务文档。
- 不影响 runtime capability 执行、records API、security/observability smoke。
