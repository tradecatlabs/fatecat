# Planning Summary
本轮把 provider health 从“metadata says ready”推进到“生产 provider 可用固定样例真实执行”。正确终态是 provider 有本地 health、依赖 smoke、真实 live smoke、trace span、SBOM/provenance、release promotion 和 rollback policy。本轮只做本地 fixture dependency smoke，避免伪造外部网络和生产账号。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义 smoke scope 和 anti-goals。 |
| PLAN | Done | 本文件拆出 runtime、tests、docs、closeout。 |
| BUILD | Done | provider dependency smoke script、pytest、local-ci hook 已落地。 |
| TEST | Done | focused tests、smoke 和 quick local-ci 已通过。 |
| REVIEW | Done | task validator、ruff/format、diff check、tree validator 已通过。 |
| SHIP | Done | closeout packet 已生成。 |

# Simplest Path
- 不新增 provider 抽象；直接复用 `CapabilityExecutor`。
- 不存完整计算结果；summary 只保留 provider id、duration、data keys、evidence keys。
- 不在 provider.health() 中执行重计算；health 仍轻量，dependency smoke 单独作为门禁。

# Split Strategy
- TP-01：确认 MI-04.03 与当前 provider 执行链路。
- TP-02：新增 smoke 脚本和 local-ci hook。
- TP-03：补 pytest 与 quick CI 验证。
- TP-04：同步文档、AGENTS、roadmap 和任务 closeout。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02 | Done |
| Wave 3 | TP-03.01 | Done |
| Wave 4 | TP-03.02, TP-04.01, TP-04.02 | Done |

# Runtime Workflow Contract
- Input: production capability registry and fixed privacy-safe sample payloads.
- Executor: `CapabilityExecutor.execute(CapabilityInput(...))`。
- Gate: provider health ready, result.status production, output data dict, evidence dict, expected key presence。
- Output: machine-readable JSON summary under `infra/runtime/local-state/exports/providers/dependency-smoke.json` by default。
- Privacy: no real user input, no report body, no token, no secret, no DSN。
- Failure: any provider fixture, health, execute, evidence or key check failure returns non-zero。

# Next Executable Leaves
- 无；任务已完成。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.02
TP-03.01 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 移除 `scripts/provider-dependency-smoke.*` 和 `tests/regression/test_provider_dependency_smoke.py`。
- 从 `scripts/local-ci.sh` 移除 provider dependency smoke step 和 focused test。
- 恢复 docs/AGENTS/roadmap 的 MI-04.03 口径。
- 不回滚 0009-0032 已完成测算基础设施切片。
