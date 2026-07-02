# Planning Summary

本任务按“测算基础设施”的正确终态倒推：开发者接入必须有机器契约、版本兼容策略、SDK/package 边界、sandbox token contract 和本地 gate。最小切片不发布 SDK、不上线 token 服务，只把当前 OpenAPI、sandbox fixture 和 examples 提升为可验证 developer platform baseline。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0067 不能标记 Done，也不能声明 developer platform baseline 已可发布。

| Gate | Evidence |
| --- | --- |
| SPEC | 0061 roadmap、现有 developer docs、sandbox fixture、OpenAPI export、metadata 和 local-ci 已复核。 |
| PLAN | 本任务文档定义范围、非目标、任务树和验证命令。 |
| BUILD | 新增 developer platform contract、sandbox token contract、API changelog、SDK/package baseline doc、gate、metadata/local-ci 接线。 |
| TEST | 运行 developer platform gate、developer docs smoke、focused pytest、ruff、quick local-ci。 |
| REVIEW | 检查 SDK 发布边界、token live 边界、隐私边界、metadata 指针和文档一致性。 |
| SHIP | 本地 quick CI 通过后提交推送；远端 GitHub Actions 作为交付事实在最终汇报中记录。 |

# Simplest Path

- 不引入外部 developer portal、gateway、token issuer 或新依赖。
- 不发布 SDK package。
- 复用已有 OpenAPI export、developer docs smoke、sandbox fixture、examples 和 local-ci。
- 只新增一个专用 gate 校验 developer platform contract、SDK/package baseline、sandbox token contract 和 API changelog。

# Split Strategy

1. 静态契约：developer platform、sandbox token contract、API changelog。
2. 人类文档：SDK/package baseline、API changelog、developer README、API 接入文档。
3. 执行入口：developer-platform-gate + local-ci artifact。
4. 证据：metadata test、gate tests、任务文档、roadmap、quick local-ci。

# Execution Waves

| Wave | Tasks |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01、TP-02.02、TP-02.03 |
| 3 | TP-03.01、TP-03.02、TP-03.03 |
| 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract

- 运行入口：`bash scripts/developer-platform-gate.sh --output-json <path>`
- 输出：`kind=fatecat.developer_platform_gate`
- 成功条件：`status=passed`、`sdkPackageCandidates>=4`、`sandboxFixtures>=2`、`publishedSdkPackages=0`、`liveSandboxTokenService=false`。
- 失败处理：任何 SDK 发布边界、token live 边界、changelog evidence、fixture 隐私或 metadata 链接断裂都直接失败。

# Next Executable Leaves

- 无；0067 本地 developer platform contract/gate baseline 已通过 quick local-ci。

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚新增 `developer-platform.json`、`sandbox-token-contract.json`、`api-changelog.json`、developer platform gate、metadata/local-ci/test 接线和相关文档。
- 不执行 `git reset --hard` 或破坏性命令。
- 若 gate 失败，优先修复 contract/docs/test 不一致，而不是降低门槛。

## Target End State

FateCat developer platform baseline 具备机器可读 contract、SDK/package 发布边界、sandbox token contract、API changelog、本地 gate、API metadata 指针、quick local-ci 门禁和回归测试；任何人都能复核当前只是本地 baseline，不是已发布 SDK 或公网 sandbox token 服务。

## Future-Optimal Framing

- 正确终态：developer platform 应该像 API infra 一样有 contract、versioning、compatibility policy、sandbox、SDK/package、portal、token、docs 和 gate。
- 本轮切片：只落本地 contract/gate baseline，保持后续真实 SDK 发布和公网 sandbox 服务的证据入口。
- Proof point：`developer-platform-gate` 和 local-ci 能同时证明 contract 自洽与“不夸大发布状态”。
- Falsifier：任何新增文档、metadata 或 gate 输出把本地示例说成已发布 SDK，或把 token contract 说成 live token 服务。

## Ponytail Existence Check

- developer platform contract 应该存在：开发者接入跨 OpenAPI、SDK、sandbox、changelog 多个资产，需要单一机器入口。
- sandbox token contract 应该存在：外部 token 还未上线，先锁 claim/scope/negative evidence 可防伪造。
- API changelog 应该存在：公开 API 兼容策略不能只靠自然语言。
- gate 应该存在：基础设施目标要求契约可验证，而不是只写文档。
