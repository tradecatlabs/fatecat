# Repo Evidence

- `git status --short --branch` 输出 `## main...origin/main`，0064 开始前 worktree 干净。
- `governance/tasks/INDEX.md` 最新已完成任务为 `0063 measurement-infrastructure-event-contract-baseline`。
- 0061 `RESEARCH.md` 推荐 0064：`OTel collector/SLO adapter plan`，最小交付物为 collector config、trace smoke dry-run、SLO evidence contract，不能伪造 trace backend。
- `contracts/fate/observability/registry.json` 已登记 health、readiness、metrics、structured logs、provider/report traces、SLO and alerts。
- `scripts/observability-slo-gate.py` 和 `scripts/observability-trace-slo-smoke.py` 已提供本地 SLO/alert policy gate 与本地 span smoke。
- `docs/reference-materials/operations/测算基础设施 API 接入.md` 已说明当前未接 OpenTelemetry collector、dashboard 或生产监控平台。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Target end state | FateCat 的观测资源具备 OTel collector/exporter 配置、SLO evidence contract、dry-run gate、真实 backend pending 边界和本地可验证证据。 |
| Real constraints | 不能连接外部 backend；不能读取真实 `.env`；不能保存真实日志或用户数据；必须保持 registry/API/docs 口径一致。 |
| Inertia constraints | 现有本地 span log 和 SLO gate 只能作为输入，不能被误称为真实 OTel collector 接入。 |
| Wrong concept / wrong boundary | “有本地 trace smoke”等于“有 trace backend”是错误边界，必须用 contract/gate 明确隔离。 |
| Change boundary | 只改 observability contracts、gate scripts、tests、docs、local-ci 和 0064 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。0064 是 contract/gate 新增，不是已复现 bug；若 gate/test 失败再补 DEBUG 证据。 |

# Change Boundary

- 允许修改：`contracts/fate/observability/`、`scripts/otel-collector-slo-gate.*`、`scripts/local-ci.sh`、`scripts/AGENTS.md`、`tests/regression/` 观测测试、API 文档、roadmap、0064 任务文档和 `governance/tasks/INDEX.md`。
- 禁止修改：业务算法、provider 计算逻辑、真实运行配置、真实 `.env`、外部部署配置和生产凭证。
- 本轮只落 dry-run contract baseline；任何真实 backend/live evidence 只能登记为 pending。

# Critical Ambiguities

- 真实 trace backend 供应商未知：不阻塞 dry-run contract，但阻止声明生产可用。
- 真实 collector 部署拓扑未知：不阻塞 static config/gate，但阻止声明 runtime collector 已运行。
- 真实生产流量和 error budget 数据未知：不阻塞 SLO evidence contract，但阻止声明 SLO 已被真实计算。

# Debug Evidence Contract

- 调试模式: Optional
- 调试模式：Optional。
- 如果 YAML/JSON/gate/test/CI 出现失败，再补充最小复现、根因、修复和回归证据。

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 伪造 trace backend | Contract 和 gate 必须强制 `externalConnectivity=external_connectivity_pending`，并写明 live evidence 待执行。 |
| Collector config 变成不可验证散文 | 新增机器可读 YAML/JSON，并用 gate 解析 receivers/processors/exporters/service pipelines。 |
| 保存敏感观测数据 | 示例与 evidence contract 只用 synthetic paths/status，不包含真实 URL、token、DSN、用户输入或报告正文。 |
| 文档夸大生产能力 | API 文档和 roadmap 明确本轮是 dry-run contract baseline。 |
| quick CI 漏跑新 gate | `scripts/local-ci.sh --profile quick` 必须生成 `otel-collector-slo-gate.json` artifact。 |

# Assumptions and Falsification

- Assumption: 当前仓库已有本地 OTel-compatible span 与 SLO/alert policy，本轮只需补 collector adapter contract，不需接真实 collector。
- Falsifier: 如果现有 trace smoke 无法产生 provider/report span，0064 不能 closeout，必须先修复旧 trace baseline。
- Assumption: PyYAML 可用，gate 可以解析 YAML；若远端 CI 缺 PyYAML，需改成 JSON 或纯标准库 parser。
- Falsifier: GitHub Acceptance 中 gate 因 YAML 依赖失败，则本轮实现必须回滚为无外部依赖解析路径。

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0061/0063 任务、observability registry、SLO/alert policy、trace smoke、OTel 官方资料。 |
| TP-02.01 | `contracts/fate/observability/` 是观测契约真相源。 |
| TP-02.02 | `contracts/fate/observability/AGENTS.md` 和 schema 必须同步新增资源边界。 |
| TP-03.01 | 复用现有 gate 脚本风格，不新增外部服务依赖。 |
| TP-03.02 | `tests/regression/test_observability_trace_slo.py` 是现有观测 gate 测试落点。 |
| TP-03.03 | `scripts/local-ci.sh` quick profile 已运行 observability gate，可插入新 gate artifact。 |
| TP-04.01 | API docs 与 roadmap 是人类接入口径真相源。 |
| TP-04.02 | validators、focused tests、ruff、secret scan、quick local CI 是 closeout 证据。 |
