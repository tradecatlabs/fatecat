# Planning Summary
0102 是 0099 计划中的 Wave A A3：在已有八字/紫微 L4 golden、rule depth registry、classics rule index 和 Report evidenceRefs 之上增加一个 tracked baseline 趋势门禁。正确终态不是再造排盘算法，而是把现有机器可读 evidence 聚成一个 coverage trend summary，让规则引用断链、证据字段缺失、冲突解释缺反证或 baseline 回退能 fail-fast。

# Lifecycle Gates
不得跳过 gate；每个 gate 都必须有文件或命令证据。

| Gate | Exit Criteria |
| --- | --- |
| SPEC | 明确 evidence coverage 只消费本地 registry、executor 输出和 API Report envelope，不连接外部系统，不声明专业能力 100%。 |
| PLAN | 任务树、范围、风险、验证命令和 rollback protocol 写入任务包。 |
| BUILD | baseline、contract、CLI/wrapper、local-ci 接线、AGENTS/docs 更新完成。 |
| TEST | smoke、focused pytest、ruff、quick local-ci、secret scan、diff check 通过或如实记录失败。 |
| REVIEW | 自审 baseline 门槛、Report evidenceRefs 完整度、隐私边界、任务文档和索引一致性。 |
| SHIP | closeout validator 通过，commit/push 完成，远端状态如实记录。 |

# Simplest Path
1. 复用 `CapabilityExecutor` 和 FastAPI `TestClient`，不改 provider 算法。
2. 用固定北京测试样本执行 bazi/ziwei，统计 evidence items、Report evidenceRefs、appliedRules、conflicts 和 combinationStatements。
3. 校验所有 rule ids 和 sourceRuleIds 能回到 `classics_rule_index.json`。
4. 对比 `evidence-coverage-baseline.json`，任何回退输出 failed。
5. 只把 summary JSON 接入 local-ci，不保存完整报告正文。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先锁定 evidence coverage 边界，防止实现时过度声明。 |
| TP-02 | 代码实现与接线集中在最小文件集。 |
| TP-03 | 验证独立，能快速发现语义、格式和隐私问题。 |
| TP-04 | closeout 与版本控制单独处理，避免证据文件自己漂移。 |

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
- 输出：baseline JSON、contract JSON、evidence coverage summary JSON、local-ci artifact、任务 closeout 文档。
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
- 删除 `evidence-coverage-baseline.json` 和 `evidence-coverage-trend-contract.json`。
- 删除 `evidence-coverage-trend-gate.py/.sh`。
- 删除 `test_evidence_coverage_trend_gate.py`。
- 恢复 local-ci、AGENTS、roadmap/API 文档和 `governance/tasks/INDEX.md` 当前任务行。
- 不触碰已提交的 0101 certification aggregator dry-run。

# Future-Optimal Task Contract
- target end state: evidence coverage 是每个 production capability 的基础设施级发布门禁，而不是临时脚本。
- real constraints: 当前 production 核心先覆盖八字和紫微；外部 live 与第三方审计不在本地 gate 中伪造。
- inertia constraints: 旧 broken-ref 点状检查不能替代 coverage trend。
- kill list: 完整报告正文 snapshot、真实用户输入、降低 baseline 掩盖回退、把 pass 写成专业能力 100%。
- proof point: quick local-ci 生成 `evidence-coverage-trend-gate.json`，且 regression 证明断链和 baseline 回退会失败。
- falsifier: 任一规则引用断链、Report evidenceRefs 不完整或 baseline 低于当前门槛仍通过。
- migration slice: 先覆盖 bazi/ziwei，后续新增 production capability 时扩展 baseline 和 tests。

# Ponytail Existence Check
- selected ladder rung: 复用项目内现有 provider/executor/report/gate 模式，只新增一个必要的基础设施门禁。
- skipped scope: 不新增 UI、不新增外部依赖、不改算法、不做专家断语质量评审。
- ceiling / upgrade path: 后续可扩为 per-capability coverage registry、趋势历史库和人工审稿指标。
- minimal runnable check: `bash scripts/evidence-coverage-trend-gate.sh --output-json /tmp/fatecat-evidence-coverage-trend-0102.json`。

# Document-Driven Change
- Operating model update: 不需要更新项目操作模型；本任务沿用现有测算基础设施资源/门禁模型。
- Toolchain model update: `scripts/local-ci.sh` 新增 gate artifact，需同步脚本 AGENTS。
- Process update: 不新增发布流程，只把 quick CI 加一个本地门禁。
- Source-of-truth updates: contracts、scripts、tests、docs、roadmap、task index。
- Local README/AGENTS impact: 更新 `contracts/fate/AGENTS.md`、`scripts/AGENTS.md`、`tests/AGENTS.md`。
- ADR/Gate/module-context impact: 不新增 ADR；gate 契约由 `evidence-coverage-trend-contract.json` 承担。
