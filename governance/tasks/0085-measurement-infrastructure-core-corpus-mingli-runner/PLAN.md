# Planning Summary
0085 将已有 core corpus 与 MingLi-Bench 散落 runner 收敛为可审计、可脱敏保存、可接 quick CI 的 aggregate gate。核心原则是：benchmark 是外部质量信号，不是生产推理输入。

# Lifecycle Gates
不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；MingLi-Bench aggregate gate 不能替代外部模型评测、专家人工准确率或上游同步证据。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | repo evidence 证明已有能力和缺口 | Done |
| PLAN | aggregate/no-leak 边界明确 | Done |
| BUILD | contract + runner + wrapper + wiring | Done |
| TEST | focused tests and gates | Done |
| REVIEW | no leak, no overclaim, no production contamination | Done |
| SHIP | local task closeout; git/remote CI handled by outer delivery flow | Done |

# Simplest Path
新增一个薄 gate：

1. 复用 `core-quality-corpus-gate.py` 取得核心 corpus summary。
2. 读取 MingLi-Bench 本地 `data.json` 做 stats。
3. 复用 `fate_core.evaluation.mingli_baseline` 生成小样本 baseline。
4. 聚合 accuracy/coverage/category 结果，不输出逐题明细。
5. 校验 vendor/data-supply/evaluation registry 的 license/usage 边界。
6. 用 contract forbidden fragments 做 no-leak assertion。

# Split Strategy
- TP-01/02 锁定事实和边界。
- TP-03 只实现 gate，不重写 MingLi runner。
- TP-04 做仓库接线和文档同步。
- TP-05 做验证、提交和远端 CI。

# Execution Waves
```text
Wave 1: TP-01.01
Wave 2: TP-02.01
Wave 3: TP-03.01
Wave 4: TP-04.01, TP-04.02
Wave 5: TP-05.01, TP-05.02
```

# Future-Optimal Task Contract
Target end state: FateCat 所有核心测算质量信号都通过 evaluation resource、runner、diff/no-leak policy 和 artifact 交付。
Real constraints: 外部 benchmark 有题库/答案/出生信息，只能 evaluation_only；外部模型评测需要额外凭证和人工审核。
Inertia constraints: 既有 `run-mingli-bench.sh` 能输出详细结果，但不适合作为 CI artifact。
Wrong concept / wrong boundary: “能评分”不等于“能把逐题结果保存进发布证据”。
Kill list: benchmark answer leak；birth_info leak；question leak；production provider reads benchmark；optional run marked required；external API called by gate。
Proof point: `mingli-bench-gate` 输出 core corpus、160 questions、sample baseline、0 findings、noLeak passed。
Falsifier: summary 包含 forbidden fragments 或 releaseRequired 被改成 true。
Migration slice: 本轮只做 local aggregate gate；后续外部模型 benchmark runner 可以读取同一 contract。
Rejected short-term patches: 不把 `run-mingli-bench.sh --stats` 直接塞进 quick CI 冒充完整 gate。
Future-optimal review owner: `auto-review` future-optimal-drift.

# Ponytail Task Contract
Existence check: 需要一个新 gate，因为现有 stats/evaluation 会分散输出且可能含逐题结果。
Selected ladder rung: project-native thin wrapper over existing corpus gate and baseline generator。
Skipped scope: 外部模型 API、专家人工评测、上游 vendor 更新、长期趋势数据库。
Ceiling / upgrade path: 未来可新增 external prediction artifact verifier，但继续禁止标准答案进入 public summary。
Do-not-simplify: no-leak assertion、license/usage checks、optional/releaseRequired boundary 不可删除。
Minimal runnable check: `bash scripts/mingli-bench-gate.sh --year 2025 --sample 5 --output-json <path>`。
Complexity review owner: `auto-review` ponytail-complexity.

# Runtime Workflow Contract
- Input: optional `--year`、`--sample`、`--output-json`。
- Output: `kind=fatecat.mingli_bench_gate` JSON summary。
- Side effects: writes one local JSON summary when requested。
- External calls: none。
- Privacy: no question、birth_info、options、answer、expected、predicted、results、fourPillars、report body、token、secret or DSN。
- Validation: core corpus、benchmark stats、baseline aggregate、license/usage、evaluation boundary、no-leak。

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-02.01 -> TP-03.01
TP-03.01 -> TP-04.01
TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `contracts/fate/evaluations/mingli-bench-gate.json`。
- 删除 `scripts/mingli-bench-gate.py/.sh`。
- 删除 `tests/regression/test_mingli_bench_aggregate_gate.py`。
- 恢复 `scripts/local-ci.sh`、evaluation registry、data supply chain registry hash、docs 和 AGENTS。
- 保留既有 `run-mingli-bench.sh` 与 `generate-mingli-predictions.sh`。

# Plan

## Future-Optimal Target State

FateCat 的核心测算质量基础设施必须具备统一 evaluation 入口：核心 corpus、报告 diff、外部 benchmark、license/usage、no-leak 和 dashboard artifact 都能被机器复核，同时不会污染 production provider。

## Real Constraints

- MingLi-Bench 是外部 reference repo snapshot，不是 production dependency。
- 题库和标准答案只能用于离线评测。
- quick CI artifact 必须脱敏且可长期保存。
- 外部模型评测、上游同步和专家人工复核需要单独任务。

## Inertia Constraints

- 既有 `run-mingli-bench.sh` 可继续作为本地临时调试入口。
- 不能因为已有脚本能跑，就把逐题结果当成交付证据。

## Kill List

- CI artifact 保存标准答案。
- dashboard 展示 benchmark 题目或出生信息。
- production provider 读取 MingLi-Bench 标准答案。
- 把 optional reference repo benchmark 标成 releaseRequired。
- 本地 gate 自动联网更新上游。

## Task Tree

| Node ID | Task | Depends On | Verify | Gate |
| --- | --- | --- | --- | --- |
| TP-01 | 复核 core corpus、MingLi-Bench 和供应链现状 | - | git/rg/runner smoke | 找到散落能力与缺口 |
| TP-02 | 设计脱敏 aggregate gate | TP-01 | contract + no-leak fragments | 不输出逐题明细 |
| TP-03 | 实现 gate 和 shell wrapper | TP-02 | CLI writes summary | 不联网，不读 secret |
| TP-04 | 接入 registry、docs、AGENTS、quick CI | TP-03 | local-ci path and docs grep | optional benchmark 不变 production |
| TP-05 | 回归测试与任务 closeout | TP-04 | pytest/gates/tasks validator | 证据可复核 |

## Verification Plan

- `bash -n scripts/mingli-bench-gate.sh scripts/local-ci.sh`
- `python3 -m py_compile scripts/mingli-bench-gate.py`
- `bash scripts/mingli-bench-gate.sh --year 2025 --sample 5 --output-json <tmp>`
- `.venv/bin/python -m pytest -q tests/regression/test_mingli_bench_aggregate_gate.py tests/regression/test_mingli_bench_gate.py`
- `bash scripts/data-supply-chain-gate.sh --output-json <tmp>`
- `bash scripts/local-ci.sh --profile quick --output <tmp>`
