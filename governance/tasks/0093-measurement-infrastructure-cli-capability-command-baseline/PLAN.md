# Planning Summary
把 0092 规划中的 `MI-10.01 CLI capability command` 落成第一个本地可执行交付面基线。正确终态不是重写 CLI，而是让现有 `fatecat capability` 从单元测试能力升级为可发现、可验证、可审计、可被 local-ci 执行的基础设施入口。

# Lifecycle Gates
| Gate | Requirement | Result |
| --- | --- | --- |
| SPEC | 明确本任务只做 CLI capability JSON 交付面基线，不做 Markdown 同源或外部 live。 | Done |
| PLAN | 拆分为现有链路复核、wrapper/smoke、contract/local-ci/docs/tests、验证 closeout。 | Done |
| BUILD | 新增 wrapper、smoke、contract、registry/local-ci/docs/tests 接线。 | Done |
| TEST | CLI smoke、focused pytest、ruff、secret scan、local-ci quick 通过。 | Done |
| REVIEW | 检查 non-claim、privacy summary、executor reuse 和 AGENTS 同步。 | Done |
| SHIP | 任务包、INDEX 和 roadmap 同步，等待提交推送。 | Done |
| Executor reuse | CLI 必须复用 `CapabilityExecutor` | Done |
| Production capability smoke | bazi/ziwei/almanac/meihua 均可通过根脚本执行 | Done |
| Planned rejection | liuyao 必须拒绝执行 | Done |
| Privacy | summary 不保存完整报告正文、姓名、token、secret、DSN、webhook URL | Done |
| Delivery registry | `surface.cli` 保持 partial，并挂 contract/smoke | Done |
| Local CI | quick profile 包含 CLI capability smoke | Done |
| Non-claim | 不声明 Markdown 多端同源或外部 live | Done |

不得跳过 gate；任一 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP gate 缺证据时，0093 不得 closeout。

# Simplest Path
1. 不新增 capability executor，也不复制 provider 调用代码。
2. 新增 `scripts/capability-cli.sh` 作为根入口，直接转发到 `python -m fate_core.cli capability`。
3. 新增 `capability-cli-smoke` 执行脱敏固定样例，并只写 summary。
4. 通过 contract、registry、local-ci、AGENTS、pytest 把该入口纳入基础设施门禁。

# Split Strategy
| Package | Scope |
| --- | --- |
| TP-01 | 复核已有 CLI/executor 链路，确认不需要重写。 |
| TP-02 | 落地根级 wrapper 和 smoke。 |
| TP-03 | 接入 delivery contract、registry、local-ci、AGENTS 和 regression。 |
| TP-04 | 验证、修复误报、回填 closeout。 |

# Execution Waves
| Wave | Nodes | Notes |
| --- | --- | --- |
| Wave 1 | TP-01 | 读取现有 CLI、tests、registry。 |
| Wave 2 | TP-02 | 编写 wrapper 和 smoke，先单独运行。 |
| Wave 3 | TP-03 | 接线 contract/local-ci/tests/docs。 |
| Wave 4 | TP-04 | focused regression、ruff、secret scan、quick CI 和文档 closeout。 |

# Runtime Workflow Contract
```text
developer/agent
  -> bash scripts/capability-cli.sh <capability_id> ...
  -> python -m fate_core.cli capability <capability_id> ...
  -> CapabilityExecutor.execute(CapabilityInput)
  -> provider registry/admission
  -> JSON result
```

Smoke workflow:

```text
bash scripts/capability-cli-smoke.sh
  -> bazi/ziwei/almanac/meihua output files in TemporaryDirectory
  -> summary hash/key extraction
  -> liuyao planned rejection assertion
  -> machine-readable JSON summary
```

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.02 -> TP-04.03
TP-01.02 ----------------------^
TP-04.01 ----------------------^
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
