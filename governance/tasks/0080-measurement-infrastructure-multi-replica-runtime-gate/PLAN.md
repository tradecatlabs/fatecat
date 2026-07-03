# Planning Summary

0080 的目标是把“长期多副本运行仍未完成”从自然语言缺口推进为机器可验证的 evidence contract 和反伪造门禁。它不做真实外部运行，也不改 worker 实现；正确切片是固定 live evidence schema、拒绝伪证、接入 runtime registry 和 quick CI，让后续真实多副本 soak 结果能通过同一入口提交脱敏证据。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0080 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 多副本 live evidence 最小字段、负例和非声明边界明确 | Done |
| PLAN | 任务树和验收写入 0080 文档 | Done |
| BUILD | contract、gate、registry、local-ci、tests/docs | Done |
| TEST | focused tests、runtime gates、quick CI | Done |
| REVIEW | 不把 worker smoke 写成 multi-replica live | Done |
| SHIP | task closeout and delivery handoff | Done |

# Future-Optimal Contract

- target end state: FateCat 的 production CalculationJob runtime 由外部 backend、多副本 worker、public webhook、external secret provider 和 observability evidence 共同证明。
- real constraints: 当前没有真实多副本运行环境，不能跑 live soak。
- inertia constraints: 已有 Postgres worker smoke 很容易被误读成 production multi-replica ready。
- kill list: single replica、short-run、SQLite、memory、placeholder proof、exactly-once overclaim。
- proof point: `multi-replica-runtime-gate` 拒绝伪证据并进入 quick CI。
- falsifier: fake evidence 被 gate 接受，或 registry 声称 production ready。
- migration slice: 新增 evidence contract/gate baseline，为后续真实 live evidence 铺路。
- rejected short-term patches: 只改 roadmap；把 worker heartbeat smoke 写成 multi-replica ready；直接新增复杂 worker runner。

# Ponytail Contract

- existence check: 100% 基础设施任务树明确要求长期多副本运行证据；文本缺口不足以防止误宣称。
- selected ladder rung: 项目内 JSON contract + gate，复用既有外部证据门禁模式。
- skipped scope: 真实多副本服务、真实 Postgres DSN、公网 webhook receiver、外部 metrics backend、exactly-once 证明。
- ceiling / upgrade path: 后续真实运行环境提供脱敏 evidence 后，用同一 gate 验证。
- do-not-simplify: 反伪造负例、exactly-once 非声明、summary 脱敏和 local-ci artifact 不能省略。
- minimal runnable check: gate summary + focused pytest + quick CI。
- complexity review owner: `auto-review` reliability/document-drift/future-optimal-drift。

# Document-Driven Contract

- Operating model update: not needed；项目定位不变。
- Toolchain model update: local-ci 新增 multi-replica runtime gate artifact。
- Process update: runtime backend gate 需要检查 multi-replica evidence contract 接线。
- Source-of-truth updates: runtime contract、delivery registry、operations docs、roadmap、task docs。
- Local README/AGENTS impact: `contracts/fate/delivery/AGENTS.md`、`scripts/AGENTS.md`、`tests/AGENTS.md`。
- Contract/catalog/schema impact: `contracts/fate/delivery/*`。
- ADR/Gate/module-context impact: not needed；沿用 runtime evidence gate 模式。
- Documentation exemption reason: 无。
- Validation evidence: focused tests、quick CI、task validators。

# Simplest Path

新增 `contracts/fate/delivery/multi-replica-runtime-contract.json` 和 `scripts/multi-replica-runtime-gate.py/.sh`；在 `runtime-backends.json` / `registry.json` 登记 contract 与 gate；扩展 `runtime-backend-gate.py`、`local-ci.sh` 和 regression tests；最后同步文档。

# Split Strategy

- Contract 先落地，保证 live evidence schema 和 negative cases 可被机器验证。
- Runtime registry 再接线，保证 Postgres 仍 planned 且不能误宣 production ready。
- local-ci 与 tests 随后接入，避免 contract 成为孤立文档。
- docs/AGENTS 最后同步，明确 live evidence 仍待真实外部环境。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01, TP-01.02 | 现状复核 | Done |
| 2 | TP-02.01, TP-02.02 | Contract | Done |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate wiring | Done |
| 4 | TP-04.01, TP-04.02 | Tests/docs | Done |
| 5 | TP-05.01, TP-05.02 | Verify/ship | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`apply_patch`、pytest、ruff、local-ci、git/gh |
| forbidden actions | 不读取真实 secret、不连接外部数据库、不声明 live passed、不修改业务算法 |
| required evidence | gate summary、focused tests、runtime-backend gate、quick CI、task validators、delivery closeout Git/CI evidence |
| stop condition | 缺真实多副本环境只阻止 live path，不阻止本地 contract/gate baseline |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph

```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol

- 删除 `contracts/fate/delivery/multi-replica-runtime-contract.json`。
- 删除 `scripts/multi-replica-runtime-gate.py/.sh` 和对应 regression tests。
- 恢复 runtime backend registry、delivery registry、runtime-backend-gate、local-ci、docs/AGENTS、task docs 和 task index。
