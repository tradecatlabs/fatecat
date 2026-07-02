# Planning Summary

0064 的目标不是部署真实监控平台，而是把 0061 中的 OTel collector/SLO adapter 缺口落成可验证基线。正确终态是：开发者和审计者能从仓库里看到 collector 配置、SLO evidence 契约、dry-run gate 和明确的外部 backend pending 状态。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0064 不能标记 Done，也不能声明 OpenTelemetry collector、trace backend、alert live 或真实 error budget 已生产。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确只做 collector/SLO dry-run contract baseline | Done |
| PLAN | 任务树、边界、验证计划落盘 | Done |
| BUILD | config、contract、gate、tests、local-ci、docs 接线完成 | Done |
| TEST | validators、gate CLI、focused tests、ruff、secret scan、quick local CI 通过 | Done |
| REVIEW | 不夸大 trace backend / production SLO / alert live | Done |
| SHIP | commit/push 后可进入下一切片 | Done |

# Simplest Path

复用 `contracts/fate/observability/` 作为观测资源真相源；新增一个 collector YAML、一个 SLO evidence JSON、一个 Python gate、一个 shell wrapper 和 focused tests。只验证配置结构和隐私边界，不启动真实 collector，不引入 OTel SDK exporter 或后端。

# Split Strategy

- TP-01：确认现有观测基线和 0064 标准。
- TP-02：实现机器契约。
- TP-03：实现 gate、测试和 local-ci 接线。
- TP-04：同步文档并完成验收。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核上下文和标准资料。 |
| 2 | TP-02.01, TP-02.02 | 新增 contract baseline 并挂到观测资源模型。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate、测试、local-ci。 |
| 4 | TP-04.01, TP-04.02 | 文档与验收。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无；0064 dry-run contract baseline 已通过本地验收，真实 collector/backend 留给后续外部连通任务。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`json.tool`、PyYAML parse、`pytest`、`ruff`、`secret-scan`、task validators、git |
| forbidden actions | 不切换分支、不启动真实 collector、不连接 trace backend、不读取真实 `.env`、不输出 secret |
| expected output | OTel collector config、SLO evidence contract、gate/test/docs/task closeout |
| required evidence | gate CLI、pytest、task validators、ruff、secret scan、quick local CI |
| stop condition | 需要真实 trace backend 或告警平台时，标记外部连通验证待执行，不阻塞 contract baseline |

# Future-Optimal Contract

- Target end state: Observability 资源能通过标准 OTel collector/exporter/SLO evidence contract 接入生产监控，而不是只靠本地日志 smoke。
- Real constraints: 当前没有真实 trace backend、collector deployment、告警平台或生产流量。
- Inertia constraints: 旧本地 smoke 名称和 registry 文案不能决定生产成熟度。
- Kill list: 删除“本地 trace smoke 已等于 production observability”的隐性口径。
- Proof point: `otel-collector-slo-gate` 能验证 config/evidence/registry/schema/docs 链接。
- Falsifier: gate 不能区分 dry-run 与 live backend，或 config 含真实 endpoint/secret。
- Migration slice: 本轮先做 dry-run contract，后续 live backend 可沿同一 contract 替换 pending evidence。
- Rejected short-term patches: 不写自然语言说明代替机器契约；不在 docs 中声明 collector 已上线。

# Ponytail Contract

- Existence check: 0061 明确 0064 是 P0；现有 observability 缺 collector/exporter/evidence contract。
- Selected ladder rung: project-native contract + direct gate implementation；不新增外部服务依赖。
- Skipped scope: OTel SDK exporter、真实 collector 进程、trace backend、dashboard、Alertmanager、PagerDuty。
- Ceiling / upgrade path: 一旦有真实 backend URL/token/部署环境，新增 live smoke 和 external evidence。
- Do-not-simplify: 隐私边界、external pending 状态、dry-run/live 区分不能删除。
- Minimal runnable check: `bash scripts/otel-collector-slo-gate.sh --output-json <path>`。
- Complexity review owner: `auto-review` 的 document-drift、feature-change-safety、ponytail-complexity。

# Document-Driven Contract

- Operating model update: not needed；项目定位未变。
- Toolchain model update: not needed；只新增本地 shell/Python gate，接入现有 local-ci 模式。
- Process update: not needed；继续使用 task validators、local-ci、remote acceptance。
- Source-of-truth updates: updated；`contracts/fate/observability`、API 文档和 roadmap。
- Local README/AGENTS impact: updated；`contracts/fate/observability/AGENTS.md` 与 `scripts/AGENTS.md`。
- Contract/catalog/schema impact: updated；observability schema/registry 新增 collector/SLO evidence contract 链接。
- ADR/Gate/module-context impact: not needed；不改变架构边界，只补同目录 gate。
- Documentation exemption reason: 无；本任务会同步相关文档。
- Validation evidence: gate、focused tests、ruff、secret scan、quick local CI。

# Rollback Protocol

- 删除新增 collector config、SLO evidence contract、gate 脚本和 tests。
- 从 observability registry/schema/local-ci/docs/AGENTS/roadmap 移除 OTel collector/SLO evidence 引用。
- 删除 0064 任务包和 INDEX 行。
