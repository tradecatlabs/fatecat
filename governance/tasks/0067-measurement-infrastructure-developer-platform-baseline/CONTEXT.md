# Context

## Current Facts

- 当前 0061 后续路线图把 0067 定义为 `developer platform`。
- `docs/reference-materials/developer/` 已有 curl、Python、Node、Agent tool-call examples。
- `contracts/fate/developer/sandbox.json` 已登记本地 deterministic sandbox fixture。
- `scripts/developer-docs-smoke.py` 已验证 OpenAPI 必备路径、sandbox fixture 和示例文件，但它不证明 SDK package 已发布。
- `/metadata` 已暴露 developer API endpoints，但缺少 developer platform contract、SDK/package baseline、sandbox token contract 和 API changelog 指针。

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不伪造发布版 SDK | `developer-platform.json` 固定 `releaseStatus=baseline_not_published`、`packageRegistryStatus=not_published`，gate 要求 `publishedSdkPackages=0`。 |
| 不伪造公网 sandbox token 服务 | `sandbox-token-contract.json` 固定 `status=contract_only`、`liveServiceStatus=not_implemented`，gate 要求 `liveSandboxTokenService=false`。 |
| 不泄露真实凭证和用户数据 | 示例、fixture 和 contract 只允许北京/测试样本，不保存 token、secret、生产 URL 或报告正文。 |
| 复用已有开发者资产 | 复用 OpenAPI export、developer docs smoke、sandbox fixture、examples 和 local-ci。 |
| Change boundary | 只改 developer contracts/docs、gate scripts、metadata、local-ci、tests、AGENTS/roadmap 和 0067 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。0067 是 contract/gate 新增，不是已复现 bug；若 gate/test 失败再补 DEBUG 证据。 |

## Change Boundary

- 允许修改：`contracts/fate/developer/`、`docs/reference-materials/developer/`、`docs/reference-materials/operations/测算基础设施 API 接入.md`、`domains/experience-delivery/services/fatecat-delivery/src/main.py`、`scripts/developer-platform-gate.*`、`scripts/local-ci.sh`、`tests/regression/`、相关 AGENTS/roadmap 和 0067 任务文档。
- 禁止修改：真实生产 token、真实 `.env`、真实用户报告、外部 developer portal、公网 sandbox issuer、生产 API/Bot live 配置。
- 本轮只落本地 developer platform contract/gate baseline；发布版 SDK、developer portal 和公网 sandbox token 归后续任务。

## Repo Evidence

- `contracts/fate/developer/sandbox.json`
- `contracts/fate/developer/developer-platform.json`
- `contracts/fate/developer/sandbox-token-contract.json`
- `contracts/fate/developer/api-changelog.json`
- `docs/reference-materials/developer/examples/`
- `docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md`
- `docs/reference-materials/developer/API_CHANGELOG.md`
- `scripts/developer-docs-smoke.py`
- `scripts/developer-platform-gate.py`
- `scripts/local-ci.sh`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`

## Critical Ambiguities

- “SDK/package baseline” 在本任务中只表示 installable examples 和 package metadata baseline，不表示 PyPI/npm 已发布。
- “sandbox token contract” 在本任务中只表示 claim/scope/rate-limit/revocation 合同，不表示 token issuer 或 gateway 已上线。
- “developer platform” 在本任务中是本地可审计 contract/gate baseline，不表示外部 developer portal 可访问。

## Debug Evidence Contract

- 调试模式: Optional
- 0067 是 contract/gate 新增，不是已复现 bug；如果 JSON、gate、pytest、local-ci 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

## Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 本地示例被误写成发布版 SDK | contract、docs 和 tests 明确 `baseline_not_published` / `not_published`。 |
| token contract 被误写成 live token 服务 | contract、docs 和 gate 明确 `contract_only` / `not_implemented`。 |
| API 兼容策略只停留在自然语言 | 新增 machine-readable `api-changelog.json` 并由 gate 校验。 |
| metadata 与 contract 漂移 | `/metadata` 回归测试锁住 developer platform 指针。 |
| local-ci 漏跑新 gate | `local-ci.sh --profile quick` 生成 `developer-platform-gate.json` artifact。 |

## Assumptions and Falsification

- 假设：developer platform 的下一步正确切片是先锁住机器契约和本地 gate，再做真实外部发布。
- 证伪条件：如果任何文档或接口声明 PyPI/npm SDK 已发布、公网 sandbox token 已上线、或保存真实 token/生产 URL，本任务失败。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 现有 developer docs、sandbox fixture、OpenAPI export、local-ci 和 `/metadata`。 |
| TP-02.01 | `contracts/fate/developer/developer-platform.json` 是 developer platform 机器真相源。 |
| TP-02.02 | `contracts/fate/developer/sandbox-token-contract.json` 是未来 sandbox token  contract。 |
| TP-02.03 | `contracts/fate/developer/api-changelog.json` 与 `docs/reference-materials/developer/API_CHANGELOG.md` 是 API changelog。 |
| TP-03.01 | `scripts/developer-platform-gate.py` 复用本仓 contract gate 风格。 |
| TP-03.02 | `/metadata`、`scripts/local-ci.sh` 和 summary artifact 是发现与门禁入口。 |
| TP-03.03 | `tests/regression/test_developer_platform_gate.py` 与 API metadata test 是回归入口。 |
| TP-04.01 | AGENTS、developer README、API 接入文档和 roadmap 是文档同步点。 |
| TP-04.02 | quick local-ci、commit/push、remote CI 是 closeout 证据。 |
