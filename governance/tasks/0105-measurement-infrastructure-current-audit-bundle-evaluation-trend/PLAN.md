# Planning Summary
0105 是 0104 后续审计证据收口。目标是让 current audit bundle 明确纳入 EvaluationRun evaluation trend gate artifact，避免“门禁已存在，但审计包看不到”的近因盲区。

# Lifecycle Gates
不得跳过 gate；每个 gate 都必须有文件或命令证据。

| Gate | Exit Criteria |
| --- | --- |
| SPEC | 明确只聚合本地 local-ci trend artifact，不声明外部 live。 |
| PLAN | 任务树、证据映射、隐私边界和验证命令写入任务包。 |
| BUILD | current audit bundle、regression、contract、AGENTS、roadmap、task index 更新完成。 |
| TEST | focused tests、bundle generation、ruff、secret/diff/task validators 通过或如实记录。 |
| REVIEW | evidence index 只包含 summary-only detail 和 digest，不包含报告正文/答案/secret。 |
| SHIP | closeout validator 通过，提交/推送后如实记录 CI 与远端状态。 |

# Simplest Path
1. 在 `LOCAL_CI_GATE_ARTIFACTS` 增加 `evaluation-trend-gate-smoke/trend-gate.json`。
2. 复用 `local_ci_gate_artifact_evidence()` 的 kind/status/zeroList/detail/digest 机制。
3. 在 current audit bundle test fixture 中运行 synthetic trend smoke。
4. 断言 evidence index 包含 `evidence.evaluation_trend_gate` 且 detail 含 `latestStatus=passed`。
5. 同步 contract、AGENTS、roadmap 和任务索引。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认缺口和映射，避免把新 evidence item 变成无意义重复。 |
| TP-02 | 实现、测试和文档同波完成，避免机器契约漂移。 |
| TP-03 | 验证和交付单独收口，避免旧 evidence 状态混入。 |

# Execution Waves
| Wave | Leaves | Parallelizable |
| --- | --- | --- |
| W1 | TP-01.01, TP-01.02 | Yes |
| W2 | TP-02.01, TP-02.02, TP-02.03 | Partly |
| W3 | TP-03.01, TP-03.02 | No |

# Runtime Workflow Contract
Allowed tools: `rg`, `sed`, `pytest`, `ruff`, project scripts, `git`, `apply_patch`.

Forbidden actions: 切换分支、改写 Git 历史、删除外部证据、读取真实 `.env`、把外部 pending 写成 passed。

Output contract: current audit bundle evidence item `evidence.evaluation_trend_gate`、updated contract/tests/docs/task closeout。

Failure policy: 结构性失败先修脚本或 tests；外部 pending 不转换为 passed。

# Next Executable Leaves
当前 ready: TP-02.03, TP-03.01。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02
TP-02.01 -> TP-02.03 -> TP-03.01
```

# Rollback Protocol
- 移除 `LOCAL_CI_GATE_ARTIFACTS` 中 `evidence.evaluation_trend_gate` 规格。
- 恢复 `tests/regression/test_current_audit_bundle.py` 中 evaluation trend fixture/assertions。
- 恢复 audit contract、AGENTS、roadmap 和 0105 任务目录。
- 保留 0104 evaluation trend gate 本身，不回滚其已完成能力。

# Future-Optimal Task Contract
- target end state: current audit bundle 是当前 commit 证据目录，覆盖新增质量趋势门禁。
- real constraints: 外部 live/远端 CI/第三方审计需要真实证据，本地不可伪造。
- inertia constraints: local-ci summary 有 artifact path 不等于 audit bundle evidence index 可追踪。
- kill list: 完整报告正文、benchmark 标准答案、stdout/stderr tail、真实凭证、把 local artifact 当外部 live。
- proof point: current audit bundle evidence index 包含 `evidence.evaluation_trend_gate` 且 status 为 pass。
- falsifier: local-ci 已生成 trend gate artifact，但 audit bundle evidence index 看不到它。
- migration slice: 先纳入 synthetic local-ci trend artifact，后续再纳入远端 CI/current commit artifact。

# Ponytail Existence Check
- selected ladder rung: 复用现有 current audit bundle local-ci gate artifact 机制，只新增一条 spec。
- skipped scope: 不新增数据库、不新增 dashboard、不重写审计包、不改 trend gate 算法。
- ceiling / upgrade path: 后续把 gate artifact list 外置为 contract-driven registry。
- minimal runnable check: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`。

# Document-Driven Change
- Operating model update: 不需要更新项目操作模型。
- Toolchain model update: current audit bundle local-ci gate artifact 覆盖范围增加。
- Process update: 0104 trend gate 现在进入 current audit bundle evidence index。
- Source-of-truth updates: scripts、contracts、tests、roadmap、task index。
- ADR/Gate/module-context impact: 不新增 ADR；contract 由 `contracts/fate/audit/current-bundle.json` 承载。
