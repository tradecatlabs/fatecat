# Planning Summary
0103 是 0099 计划中的 Wave A A4：基于最新 commit 重新聚合 current audit bundle。最小正确切片不是重新发明审计系统，而是让现有 current-audit-bundle 显式吸收 local-ci gate artifact 摘要，尤其是 0102 evidence coverage trend gate，让第三方审计人员能从 evidence index 追到新增质量门禁。

# Lifecycle Gates
不得跳过 gate；每个 gate 都必须有文件或命令证据。

| Gate | Exit Criteria |
| --- | --- |
| SPEC | 明确 current audit bundle refresh 只聚合本地可复核证据，不声明外部 live 或第三方审计通过。 |
| PLAN | 任务树、范围、风险、验证命令和 rollback protocol 写入任务包。 |
| BUILD | current-audit-bundle、local-ci、contract、AGENTS/tests/roadmap 更新完成。 |
| TEST | focused tests、bundle generation、ruff、secret scan、diff check 通过或如实记录失败。 |
| REVIEW | 自审 evidence index、risk register、pending external 和 non-claims 一致。 |
| SHIP | closeout validator 通过，commit/push 完成，远端状态如实记录。 |

# Simplest Path
1. 在 `current-audit-bundle.py` 中新增 `--local-ci-output-dir`。
2. 从该目录读取 `evidence-coverage-trend-gate.json`。
3. 校验 `kind/status`、`trendFindings=[]`、`brokenRuleRefs=[]` 并输出 digest 与摘要计数。
4. local-ci 调用 current audit bundle 时传入自己的 output dir。
5. regression 断言 evidence index 包含 `evidence.evidence_coverage_trend_gate`。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先锁定审计刷新边界，避免伪造外部 live。 |
| TP-02 | 实现和接线集中在最小文件集。 |
| TP-03 | 验证独立，覆盖证据索引和隐私边界。 |
| TP-04 | closeout 与版本控制单独处理，避免证据状态漂移。 |

# Execution Waves
| Wave | Leaves | Parallelizable |
| --- | --- | --- |
| W1 | TP-01.01, TP-01.02 | Yes |
| W2 | TP-02.01 | No |
| W3 | TP-02.02, TP-03.01 | Yes |
| W4 | TP-03.02 | No |
| W5 | TP-04.01, TP-04.02 | No |

# Runtime Workflow Contract
- 允许工具：`rg`、`sed`、`pytest`、`ruff`、项目脚本、`git`。
- 禁止动作：切换分支、删除外部证据、修改真实凭证、伪造外部 live evidence。
- 输出：current audit bundle JSON/Markdown、evidence index、risk register、pending external validations、任务 closeout 文档。
- 失败策略：结构性失败先修脚本或测试；外部 pending 不修成 passed，只如实保留。

# Next Executable Leaves
- 当前 ready：TP-03.02、TP-04.01。
- TP-04.02 依赖 TP-03.02 和 TP-04.01 通过。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.02 -> TP-04.01 -> TP-04.02
TP-02.01 -> TP-03.01 -> TP-03.02
```

# Rollback Protocol
- 移除 `current-audit-bundle.py` 中 local-ci output dir artifact 展开逻辑。
- 恢复 `scripts/local-ci.sh` current audit bundle 调用。
- 恢复 `current-bundle.json`、AGENTS、roadmap 和 tests。
- 删除 0103 任务目录与 INDEX 行。
- 不触碰已提交的 0102 evidence coverage trend gate。

# Future-Optimal Task Contract
- target end state: current audit bundle 是当前 commit 的证据目录，不只是 release/audit 顶层包。
- real constraints: 外部 live 和第三方审计不能本地伪造；local bundle 可 blocked。
- inertia constraints: 旧 bundle 不展开 local-ci gate artifact，审计人员难以追踪新增质量门禁。
- kill list: 完整报告正文、真实用户输入、凭证值、把 blocked bundle 写成 audit passed。
- proof point: `evidence-index.json` 包含 `evidence.evidence_coverage_trend_gate` 且 current bundle generator 通过。
- falsifier: local-ci 已生成 evidence coverage gate，但 current audit bundle evidence index 看不到它。
- migration slice: 先纳入 evidence coverage trend gate，后续可扩展更多 local-ci gate artifact 摘要。

# Ponytail Existence Check
- selected ladder rung: 复用现有 current-audit-bundle generator，只增加必要输入参数和 evidence item。
- skipped scope: 不新增 UI、不新增外部依赖、不改 audit handoff/dry-run/current-release-proof 语义。
- ceiling / upgrade path: 后续可把 local-ci artifact 列表外置到 contract，统一管理所有 gate artifact。
- minimal runnable check: `bash scripts/current-audit-bundle.sh --local-ci-output-dir <dir> ...`。

# Document-Driven Change
- Operating model update: 不需要更新项目操作模型；本任务沿用现有审计包模型。
- Toolchain model update: local-ci current audit bundle 调用新增 `--local-ci-output-dir`。
- Process update: 不新增发布流程，只增强审计包 evidence index。
- Source-of-truth updates: scripts、contracts、tests、docs、task index。
- Local README/AGENTS impact: 更新 `scripts/AGENTS.md`、`contracts/fate/audit/AGENTS.md`。
- ADR/Gate/module-context impact: 不新增 ADR；gate 契约由 `contracts/fate/audit/current-bundle.json` 承担。
