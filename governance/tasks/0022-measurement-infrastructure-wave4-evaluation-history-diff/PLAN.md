# Planning Summary
本任务把 EvaluationRun 的本地执行结果从“一次性 summary 文件”推进为“可留痕、可比较、可判定回归”的质量闭环。最小正确终态是：runner 可记录 history/latest，diff 工具可比较 baseline/current，policy 可用 0 容忍阈值阻断回归。

# Lifecycle Gates
不得跳过 gate；每个阶段必须以文件、命令输出、测试或任务状态作为证据后才能进入下一阶段。

| Phase | Gate |
| --- | --- |
| SPEC | 已确认 history/diff 是 0021 之后最小可落地缺口。 |
| PLAN | 任务树、风险、验收命令和范围落盘。 |
| BUILD | history、diff tool、diff policy、registry/AGENTS 同步。 |
| TEST | history/diff tests、contract tests、CLI smoke 通过。 |
| REVIEW | 检查不保存敏感信息、不宣称 dashboard/nightly 完成。 |
| SHIP | quick CI、diff check、任务 validators 和 closeout packet 通过。 |

# Simplest Path
不引入数据库或 dashboard，先把 summary JSON 文件做成可比较的稳定格式；用一个小型 diff 脚本和 JSON policy 判定回归。

# Split Strategy
- TP-01 明确缺口和边界。
- TP-02 实现 history/diff/policy。
- TP-03 以测试和文档锁住行为。
- TP-04 修正任务树索引漂移。
- TP-05 执行门禁并收口。

# Execution Waves
```text
Wave 1: TP-01
Wave 2: TP-02
Wave 3: TP-03 + TP-04
Wave 4: TP-05
```

# Runtime Workflow Contract
- `bash scripts/run-evaluations.sh --record-history` 写入 timestamp summary 并更新 `history/latest.json`。
- `bash scripts/compare-evaluations.sh --baseline-json <baseline> --current-json <current>` 输出 diff JSON。
- `contracts/fate/evaluations/diff-policy.json` 是本地 diff 阈值真相源。
- 本轮 CLI 输出默认进入 `infra/runtime/local-state/exports/` 或 `/tmp`，不进入 Git。

# Next Executable Leaves
- TP-05.01 执行 quick CI。
- TP-05.02 回填 closeout。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-02.03
TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03
TP-03.03 -> TP-04.01 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `scripts/compare-evaluations.py`、`scripts/compare-evaluations.sh` 和 `tests/regression/test_evaluation_history_diff.py`。
- 恢复 `scripts/run-evaluations.py` 的 `--record-history` 改动。
- 恢复 registry、AGENTS、docs、roadmap、local-ci 和 INDEX 的本任务改动。
- 不影响 0021 runner 的基础执行能力。
