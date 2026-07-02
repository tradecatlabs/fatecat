# Planning Summary
把 D7 可观测从“能看 health/metrics/requestId”推进到“能追一条请求经过 API、capability、provider 和 report 层，并有可审计 SLO/alert 合同”。本轮最小正确切片是本地 trace/span 日志、SLO/alert contract、smoke/gate 和 quick CI，不接外部监控平台。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Requirement | Status |
| --- | --- | --- |
| SPEC | 明确本轮是本地 baseline，不是生产 OTel 平台 | Passed |
| PLAN | trace、SLO、alert、CI、docs 分包清楚 | Passed |
| BUILD | runtime、contracts、scripts、tests 和 docs 落地 | Passed |
| TEST | focused validation 和 local quick CI 通过 | Passed |
| REVIEW | 隐私、误报生产能力、planned capability 语义已自审 | Passed |
| SHIP | 任务文档与 closeout packet 生成 | Pending closeout generation |

# Simplest Path
1. 复用 W3C Trace Context 标准和 Python logging，不新增 OpenTelemetry SDK 依赖。
2. 在入口 middleware 建立 trace context，向核心路径追加 span，而不是改 provider 输出结构。
3. 用 JSON contract 定义 SLO/alert，先让审计和 CI 可验证。
4. 用 TestClient smoke 捕获结构化日志，验证 traceparent、span、SLO gate 和隐私边界。

# Split Strategy
- TP-01 确认 D7 缺口，防止把外部监控误混进本地切片。
- TP-02 先落 trace runtime 和核心调用链 instrumentation。
- TP-03 再落 SLO/alert contract 和 registry 状态。
- TP-04 把所有能力变成可重复门禁。
- TP-05 做文档同步、验证和任务收口。

# Execution Waves
| Wave | Packages | Result |
| --- | --- | --- |
| Wave 1 | TP-01 | 现状和边界确认完成。 |
| Wave 2 | TP-02, TP-03 | trace runtime、instrumentation、SLO/alert contracts 完成。 |
| Wave 3 | TP-04 | smoke/gate/tests/quick CI 完成。 |
| Wave 4 | TP-05 | docs、roadmap、task closeout 完成。 |

# Runtime Workflow Contract
- Runtime writes only structured logs and response headers.
- `trace_span` must sanitize attributes and avoid payload/report body.
- SLO/alert rules are file contracts plus gate output, not live alert delivery.
- External connectivity evidence must remain `external_connectivity_pending` until production credentials/platform exist.

# Next Executable Leaves
无；任务实现完成，剩余动作为 closeout packet 生成与验证。

# Dependency Graph
```text
TP-01.01
  -> TP-02.01 -> TP-02.02
  -> TP-03.01 -> TP-03.02
  -> TP-04.01 -> TP-04.02
  -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
