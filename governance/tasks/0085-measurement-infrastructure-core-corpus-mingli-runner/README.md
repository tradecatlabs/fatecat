# Task Overview
- Task ID: `0085`
- Slug: `measurement-infrastructure-core-corpus-mingli-runner`
- Objective: `把核心八字/紫微 corpus、完整报告 diff policy、MingLi-Bench 离线 runner、license/usage 分级和 no-leak 策略收敛为一个本地可执行 gate，并进入 quick CI artifact。`
- Status: `Done`

## In Scope

把 0085 从“已有散落脚本”收敛为可复核的基础设施切片：核心八字/紫微 corpus、完整报告 diff policy、MingLi-Bench 离线 runner、license/usage 分级和 no-leak 策略必须形成一个本地可执行 gate，并进入 quick CI artifact。

- 新增 MingLi-Bench aggregate gate contract 与 runner。
- 复用既有 core-quality-corpus gate、MingLi-Bench reference repo、FateCat baseline prediction runner。
- 只输出聚合统计和 license/usage/no-leak 证据。
- 不保存题目、出生信息、标准答案、逐题结果或报告正文。
- 不调用外部模型 API。
- 不自动更新 MingLi-Bench vendor snapshot。

## Out of Scope

- 不证明外部模型 benchmark 已完成。
- 不证明专家人工准确率。
- 不把 MingLi-Bench 标准答案注入 production provider。
- 不把 evaluation fixture 作为生产断语依据。

## Task Package Tree
```text
TP-01 SPEC: 复核 core corpus、MingLi-Bench 和供应链现状
  TP-01.01 复核 core corpus、MingLi-Bench、vendor 和 evaluation registry
TP-02 PLAN: 设计脱敏 aggregate gate
  TP-02.01 新增 MingLi-Bench aggregate gate contract
TP-03 BUILD: 实现 gate
  TP-03.01 实现 mingli-bench-gate.py/.sh
TP-04 BUILD: 仓库接线
  TP-04.01 接入 registry、docs、AGENTS 和 quick CI
  TP-04.02 刷新 data supply chain registry hash
TP-05 TEST/SHIP: 回归与交付
  TP-05.01 增加 focused regression tests
  TP-05.02 运行完整验证、提交、推送和远端 CI
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| bazi/ziwei corpus | 复用 `core-quality-corpus-gate` 并在 aggregate summary 中只保留计数和 policy 路径 |
| benchmark runner | 新增 `mingli-bench-gate.py/.sh`，复用 FateCat baseline generator |
| full report diff | gate 关联 `report-diff-policy.json`，不保存报告正文 |
| no-leak policy | contract forbidden fragments + runtime summary assertion |
| license 分级 | 校验 vendor manifest 和 data supply chain registry 的 evaluation-only 边界 |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | repo evidence 证明缺口是 aggregate gate |
| TP-01.01 | 复核现状 | Done | core corpus、MingLi scripts、registry、vendor 已读 |
| TP-02 | PLAN | Done | no-leak aggregate contract 明确 |
| TP-02.01 | contract | Done | `mingli-bench-gate.json` added |
| TP-03 | BUILD | Done | gate runner added |
| TP-03.01 | script | Done | CLI smoke passed |
| TP-04 | BUILD | Done | registry/docs/local-ci linked |
| TP-04.01 | wiring | Done | registry、docs、AGENTS、quick CI updated |
| TP-04.02 | hash | Done | data supply chain registry sha refreshed |
| TP-05 | TEST/SHIP | Done | full local gates complete |
| TP-05.01 | tests | Done | focused tests passed |
| TP-05.02 | delivery | Done | local validation complete; git/remote CI evidence handled by outer delivery flow |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md

## Key Deliverables

- `contracts/fate/evaluations/mingli-bench-gate.json`
- `scripts/mingli-bench-gate.py`
- `scripts/mingli-bench-gate.sh`
- `tests/regression/test_mingli_bench_aggregate_gate.py`
- quick CI 中的 `mingli-bench-gate.json`
