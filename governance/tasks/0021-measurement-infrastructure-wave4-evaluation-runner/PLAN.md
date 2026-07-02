# Planning Summary
本任务把 EvaluationRun 从“资源声明”推进到“本地可执行门禁”。最小正确终态是：registry 声明 run，runner 受控执行 run，summary JSON 记录机器可读结果，文档明确 API 发现层不负责执行。

# Lifecycle Gates
不得跳过 gate；每个阶段必须有文件、命令或任务状态证据后才能进入下一阶段。

| Phase | Gate |
| --- | --- |
| SPEC | 已确认 EvaluationRun、Dataset、现有 scripts 与缺口。 |
| PLAN | 任务树、范围、风险和验收命令落盘。 |
| BUILD | runner、registry metadata、schema summary fields、AGENTS 同步。 |
| TEST | dry-run、安全拒绝、contract/API/focused tests 通过。 |
| REVIEW | 检查无 `shell=True`、无 secret、无外部 live 声明。 |
| SHIP | quick CI、diff check、任务 closeout validators 通过。 |

# Simplest Path
新增一个薄 Python runner 和 bash wrapper，直接复用 registry 中的 `commands` 字段；不引入数据库、队列、dashboard 或 CI 平台二次抽象。

# Split Strategy
- TP-01 先锁事实和边界。
- TP-02 完成最小 runner。
- TP-03 以测试锁住安全白名单和 contract 口径。
- TP-04 同步人类文档，防止“API 会执行评测”的误解。
- TP-05 真实运行并回填证据。

# Execution Waves
```text
Wave 1: TP-01
Wave 2: TP-02
Wave 3: TP-03 + TP-04
Wave 4: TP-05
```

# Runtime Workflow Contract
- runner 默认执行 `--all-local-required`。
- `--dry-run` 只验证选择器和命令白名单，不执行命令。
- `--run-id` 可重复指定。
- `--allow-reference-repo` 是执行可选 reference repo benchmark 的显式开关。
- summary JSON 写入 `infra/runtime/local-state/exports/evaluations/summary.json` 或用户指定路径。

# Next Executable Leaves
- TP-05.01：执行验证命令。
- TP-05.02：回填 closeout 状态。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-02.03
TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03
TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `scripts/run-evaluations.py`、`scripts/run-evaluations.sh` 和 `tests/regression/test_evaluation_runner.py`。
- 恢复 registry/schema/docs/AGENTS/local-ci 的本任务改动。
- 恢复 `governance/tasks/0021-*` 到初始化状态。
- 不影响已有 `/evaluations` 只读 API 和旧 golden tests。
