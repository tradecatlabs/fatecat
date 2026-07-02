# Planning Summary
本任务把现有 observability 发现层推进为本地可执行 smoke。最小正确终态是：一个脚本能验证 health/ready/metrics/request-id/log/registry，并输出 JSON；文档明确这不是 OpenTelemetry/生产监控完成。

# Lifecycle Gates
不得跳过 gate；每个阶段必须有文件、命令输出、测试或任务状态证据。

| Phase | Gate |
| --- | --- |
| SPEC | 已确认 available signals 与 planned signals 边界。 |
| PLAN | 任务树、验收命令和范围落盘。 |
| BUILD | smoke 脚本、registry metadata、AGENTS 同步。 |
| TEST | smoke CLI、focused tests、ruff/format 通过。 |
| REVIEW | 检查不保存敏感数据、不夸大生产监控。 |
| SHIP | quick CI、diff check、validators 和 closeout packet 通过。 |

# Simplest Path
复用 FastAPI TestClient 和现有 app，不新增外部 collector 或监控依赖。

# Split Strategy
- TP-01 锁范围。
- TP-02 实现 smoke 与登记。
- TP-03 补测试和文档。
- TP-04 执行门禁。

# Execution Waves
```text
Wave 1: TP-01
Wave 2: TP-02
Wave 3: TP-03
Wave 4: TP-04
```

# Runtime Workflow Contract
- `bash scripts/observability-smoke.sh --output-json <path>` 输出 smoke summary。
- summary 只含检查结果和隐私边界，不含用户输入或日志正文。
- registry metadata 的 `smokeCommand` 是发现层到执行层的复现入口。

# Next Executable Leaves
- TP-04.01 执行 quick CI。
- TP-04.02 closeout。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03
TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 删除 `scripts/observability-smoke.py`、`.sh` 和 `tests/regression/test_observability_smoke.py`。
- 恢复 observability registry/AGENTS、scripts/AGENTS、local-ci、API 文档和 roadmap 的本任务改动。
- 不影响已有 `/observability` API 和 metrics/log 实现。
