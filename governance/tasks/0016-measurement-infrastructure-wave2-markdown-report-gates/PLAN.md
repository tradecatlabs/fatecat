# Planning Summary
本轮补齐 0015 的下一层：不仅 capability JSON envelope 有 policyGate，用户真正复制/查看的 Markdown 报告也必须带正文 policyGate 和结构 snapshotGate。实现以最小、可验证、可回滚为原则：解析 Markdown heading，扫描正文禁止性断语，不改报告正文。

# Lifecycle Gates
| Gate | Requirement |
| --- | --- |
| SPEC | 明确覆盖同步 Markdown、标准异步 job、Web 异步 job。 |
| PLAN | 任务拆成 helper、接入、测试、文档、验证。 |
| BUILD | 只新增 gate 字段，不改变旧结果字段和 Markdown 正文。 |
| TEST | 三条路径回归 + helper 单测通过。 |
| REVIEW | gate 语义不夸大，snapshot 只锁核心 heading。 |
| SHIP | closeout validators 和 quick CI 通过。 |

不得跳过 gate；任一 gate 失败必须先修复或在 STATUS 中记录明确阻塞原因。

# Simplest Path
1. 在 `report_policy.py` 增加 `build_markdown_report_policy_gate()` 和 `build_markdown_snapshot_gate()`。
2. `_build_markdown_report_payload()` 附加 gate。
3. `WebReportResult` 增加 gate 字段，`build_web_report_result()` 附加 gate。
4. `_serialize_report_job_result()` 序列化 Web gate。
5. 更新 schema、tests、docs。

# Split Strategy
- TP-01：契约和范围。
- TP-02：helper。
- TP-03：多端接入。
- TP-04：测试文档。
- TP-05：验证收口。

# Execution Waves
| Wave | Leaves |
| --- | --- |
| Wave 1 | TP-01.01、TP-01.02 |
| Wave 2 | TP-02.01、TP-02.02 |
| Wave 3 | TP-03.01、TP-03.02、TP-03.03 |
| Wave 4 | TP-04.01、TP-04.02 |
| Wave 5 | TP-05.01、TP-05.02 |

# Runtime Workflow Contract
- 不访问外部服务。
- 不启动长期服务。
- 不提交、不推送。
- 所有证据写回 STATUS。

# Next Executable Leaves
- TP-01.01 define-markdown-gate-scope
- TP-01.02 update-report-schema-contract

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-03.03
TP-03.03 -> TP-04.01
TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 移除新增 gate helper 和导入。
- 恢复 Markdown/Web result 新增字段。
- 恢复 tests/docs/schema 中 0016 gate 声明。
- 不回滚 0009-0015 已完成切片。
