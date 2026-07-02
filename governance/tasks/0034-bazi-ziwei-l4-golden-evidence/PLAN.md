# Planning Summary
本轮把八字/紫微从“已有 scattered golden tests”收敛成基础设施视角的本地 L4 golden/evidence smoke。正确终态是八字、紫微都有大规模匿名 corpus、全文 diff、规则 coverage、冲突裁决、评测 dashboard 和远端 CI artifact。本轮只做本地 baseline：一个可执行 smoke、一个 quick CI hook、一组文档口径和任务 closeout。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义 scope、anti-goals 和隐私边界。 |
| PLAN | Done | 本文件拆出 runtime、tests、docs、closeout。 |
| BUILD | Done | smoke script、pytest 和 local-ci hook 已落地。 |
| TEST | Done | focused tests、ruff、format 和 quick CI 已通过。 |
| REVIEW | Done | closeout validator 已通过；diff check 和 tree validator 作为最终仓库校验执行。 |
| SHIP | Done | closeout packet 已生成。 |

# Simplest Path
- 不新增 L4 抽象；直接提供独立 smoke，复用现有 fixture 和 executor。
- 不存完整报告正文；summary 只记录 case id、gate 状态、计数和检查结果。
- 不把 full 跑进 quick CI；quick 跑代表集，full 留给 release/deep gate。

# Split Strategy
- TP-01：确认 MI-05 与现有 fixture 缺口。
- TP-02：新增 smoke 脚本、quick/full profile 和 local-ci hook。
- TP-03：补 pytest 并执行真实验证。
- TP-04：同步文档、AGENTS、roadmap、任务索引和 closeout。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02 | Done |
| Wave 3 | TP-02.03, TP-03.01 | Done |
| Wave 4 | TP-03.02, TP-04.01, TP-04.02 | Done |

# Runtime Workflow Contract
- Input: tracked anonymous bazi/ziwei golden fixtures and Markdown API payloads。
- Executor: `CapabilityExecutor.execute(CapabilityInput(...))` and FastAPI `TestClient`。
- Profiles: `quick` runs representative samples; `full` runs all currently configured fixture cases for the non-matrix sets and one representative per required matrix tag。
- Gate: pillar/fortune/evidence/rule/topic/conflict/Markdown policy and snapshot checks must pass。
- Output: machine-readable JSON summary under `infra/runtime/local-state/exports/golden/bazi-ziwei-l4.json` by default。
- Privacy: no real user input, no real non-Beijing sample, no token, no secret, no DSN。
- Failure: any mismatch returns non-zero and prints the failing check name。

# Next Executable Leaves
- TP-04.02：生成 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-04.02
TP-03.01 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 移除 `scripts/bazi-ziwei-l4-golden-smoke.*` 和 `tests/regression/test_bazi_ziwei_l4_golden_smoke.py`。
- 从 `scripts/local-ci.sh` 移除 bazi/ziwei L4 golden smoke step 和 focused test。
- 恢复 docs/AGENTS/roadmap 的 MI-05 口径。
- 不回滚 0009-0033 已完成测算基础设施切片。
