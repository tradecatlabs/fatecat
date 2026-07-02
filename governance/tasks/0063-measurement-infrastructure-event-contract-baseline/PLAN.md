# Planning Summary

本任务把 0061 规划中的 Event Platform P0 缺口落成可验证基线。正确终态不是“再写一段 webhook 文档”，而是让 job/webhook/evaluation/release 事件以标准 envelope、机器契约、示例和 gate 的形式进入基础设施资源模型。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0063 不能标记 Done，也不能声明外部 broker、公网 webhook live delivery 或事件平台生产可用。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确只做 CloudEvents/AsyncAPI contract baseline | Done |
| PLAN | 任务树、边界、验证计划落盘 | Done |
| BUILD | schema、registry、examples、gate、tests、local-ci、docs 接线完成 | Done |
| TEST | focused tests、gate CLI、validators、ruff/secret scan、quick local CI 通过 | Done |
| REVIEW | 不夸大 broker/webhook live/事件平台生产能力 | Done |
| SHIP | commit/push 后可进入下一切片 | Done |

# Simplest Path

复用 `contracts/fate/delivery/` 作为交付和事件契约真相源；新增一个 registry、一个 schema、一个 AsyncAPI 风格 JSON、五个 synthetic examples、一个 Python gate、一个 shell wrapper 和 focused tests。不引入外部 broker、事件 SDK、AsyncAPI 代码生成器或运行时事件总线。

# Split Strategy

- TP-01：确认事件契约的事实和边界。
- TP-02：实现机器契约。
- TP-03：实现 gate、测试和 local-ci 接线。
- TP-04：同步文档并完成验收。

# Execution Waves

| Wave | Leaves | Purpose |
| --- | --- | --- |
| 1 | TP-01.01 | 复核上下文和外部标准。 |
| 2 | TP-02.01, TP-02.02 | 新增 contract baseline 并挂到资源模型。 |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate、测试、local-ci。 |
| 4 | TP-04.01, TP-04.02 | 文档与验收。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无；0063 contract baseline 已通过本地验收，真实 receiver/broker 留给后续外部连通任务。 |

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`pytest`、`ruff`、`py_compile`、`secret-scan`、task validators、git |
| forbidden actions | 不切换分支、不连接真实 broker/receiver、不读取真实 `.env`、不输出 secret |
| expected output | AsyncEvent registry/schema/AsyncAPI/examples/gate/test/docs/task closeout |
| required evidence | gate CLI、pytest、task validators、ruff、secret scan、quick local CI |
| stop condition | 需要真实 receiver/broker 才能验证时，标记外部连通验证待执行，不阻塞 contract baseline |

# Rollback Protocol

- 删除 `contracts/fate/delivery/events.json`、`events.asyncapi.json`、`schemas/async-event.schema.json` 和 `examples/events/`。
- 从 delivery registry/resource schema/local-ci/tests/scripts/docs/AGENTS/roadmap 移除 AsyncEvent 引用。
- 删除 0063 任务包和 INDEX 行。
