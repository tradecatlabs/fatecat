# Planning Summary
0104 是 0099 后续的质量趋势库切片。目标不是新增一个 dashboard，而是把 EvaluationRun 的 `history/latest` 从“可保存历史”提升为“可拒绝回退的本地趋势门禁”，并把它纳入 100% 测算基础设施计划。

# Lifecycle Gates
不得跳过 gate；每个 gate 都必须有文件或命令证据。

| Gate | Exit Criteria |
| --- | --- |
| SPEC | 明确 trend gate 只证明本地 history summary 趋势，不证明外部 benchmark、远端 CI 或生产 live。 |
| PLAN | 任务树、隐私边界、失败阈值、验证命令和路线图更新写入任务包。 |
| BUILD | trend policy、CLI、smoke、CI wiring、registry metadata、AGENTS 和 tests 完成。 |
| TEST | focused pytest、synthetic smoke、真实 runner history+trend gate、ruff、secret scan、diff check 通过或如实记录。 |
| REVIEW | 自审输出不包含 tails/答案/报告正文/secret，路线图不宣称 100%。 |
| SHIP | closeout validator 通过；提交/推送证据单独收口。 |

# Simplest Path
1. 复用 `run-evaluations --record-history` 产出的 summary JSON，不新增数据库。
2. 新增 `trend-policy.json` 定义窗口、最新必须通过、连续失败、失败 run/command 和 required run 缺失阈值。
3. 新增 `evaluation-trend-gate.py` 输出 summary-only JSON。
4. 用 synthetic smoke 覆盖 quick CI，避免重型评测拖慢本地门禁。
5. 用 focused regression 锁隐私边界和 local-ci/registry 接线。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先锁 policy 和隐私边界，防止实现后补口径。 |
| TP-02 | 实现、接线和文档同波完成，避免散落脚本。 |
| TP-03 | 测试和路线图同波完成，确保 100% 计划反映最新能力。 |
| TP-04 | closeout 与版本控制单独处理，避免证据漂移。 |

# Execution Waves
| Wave | Leaves | Parallelizable |
| --- | --- | --- |
| W1 | TP-01.01, TP-01.02 | Yes |
| W2 | TP-02.01, TP-02.02, TP-02.03 | Partly |
| W3 | TP-03.01, TP-03.02 | Yes |
| W4 | TP-04.01, TP-04.02 | No |

# Runtime Workflow Contract
Allowed tools: `rg`, `sed`, project scripts, `pytest`, `ruff`, `git`, `apply_patch`.

Forbidden actions: 切换分支、删除外部证据、修改真实凭证、伪造外部 live、把 benchmark 标准答案或报告正文写入 trend output。

Output contract: trend gate JSON、local-ci artifact path、focused regression result、roadmap Post-0103 section、task closeout evidence。

Failure policy: 结构性失败先修脚本或 policy；外部 pending 不改成 passed。

# Next Executable Leaves
当前 ready: TP-02.02、TP-02.03、TP-03.01、TP-03.02。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-04.01 -> TP-04.02
TP-02.01 -> TP-02.03 -> TP-03.01
TP-01.02 -> TP-03.02 -> TP-04.01
```

# Rollback Protocol
- 移除 `scripts/evaluation-trend-gate.py`、shell wrapper 和 smoke。
- 恢复 `scripts/local-ci.sh` 中 trend smoke、regression test 和 summary artifact 接线。
- 恢复 `contracts/fate/evaluations/registry.json` metadata、删除 `trend-policy.json`。
- 恢复 `scripts/AGENTS.md`、`contracts/fate/evaluations/AGENTS.md`、路线图和 0104 任务目录。
- 不触碰已有 EvaluationRun runner/history/diff/dashboard/nightly。

# Future-Optimal Task Contract
- target end state: EvaluationRun 是测算基础设施质量控制面的一等资源，具备 history、diff、dashboard、nightly、trend 和审计证据。
- real constraints: 外部 benchmark、远端 CI、生产 live 需要真实凭证/平台证据，本地无法伪造。
- inertia constraints: 只看最新一次 summary 容易漏掉 required run 消失和连续失败。
- kill list: stdout/stderr tail、benchmark 标准答案、完整报告正文、真实用户输入、真实 secret。
- proof point: 最新失败或 required run 缺失时 trend gate fail；干净 synthetic history passed。
- falsifier: trend gate 对失败命令、失败 run 或 required run 缺失仍返回 passed。
- migration slice: 先做本地 JSON history trend gate，后续再接远端 CI artifact 和外部 benchmark trend。

# Ponytail Existence Check
- selected ladder rung: 复用现有 summary JSON 和本地脚本，新增最小 gate，不引入数据库或服务。
- skipped scope: 不新增 Web dashboard，不接外部监控，不新增 provider，不改生产算法。
- ceiling / upgrade path: 后续可把 trend store 升级成 CI artifact index 或对象存储，但需要真实远端证据。
- minimal runnable check: `bash scripts/evaluation-trend-gate-smoke.sh --output-dir <tmp>`.

# Document-Driven Change
- Operating model update: 不需要更新项目操作模型；本任务落入既有测算基础设施路线图。
- Toolchain model update: `local-ci.sh --profile quick` 新增 trend gate smoke 与 regression。
- Process update: 评测 history 从“可保存”升级为“可拒绝回退”的本地门禁。
- Source-of-truth updates: contracts、scripts、tests、roadmap、task index、AGENTS。
- ADR/Gate/module-context impact: 不新增 ADR；gate 由 `trend-policy.json` 承担。
