# Repo Evidence
- `git status --short --branch` 显示当前分支 `main...origin/main`，0009-0015 改动未提交。
- `_build_markdown_report_payload()` 当前只返回 `reportSystem` 和 `markdown`。
- `_serialize_report_job_result()` 对 dict 原样返回，对 `WebReportResult` 只返回 `reportSystem/reportSystemLabel/markdown/input`。
- `WebReportResult` 当前没有 gate 字段。
- 0015 已在 capability Report envelope 上实现 `policyGate`，但 Markdown 正文未覆盖。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不改 Markdown 正文 | gate 作为附加结构字段返回。 |
| 不引入新依赖 | 用简单 heading parser 与字符串扫描。 |
| 不夸大合规 | `snapshotGate` 锁 heading structure，不代表人工内容审查。 |
| 多端一致 | 同步 Markdown、标准 job、Web job 返回同名 gate 字段。 |
| 现有 API 兼容 | 只新增字段，不删除旧字段。 |

# Change Boundary
- May change:
  - `fate_core/capabilities/report_policy.py`
  - `fate_core/capabilities/__init__.py`
  - `contracts/fate/capabilities/schemas/report.schema.json`
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py`
  - `domains/experience-delivery/services/fatecat-delivery/src/web_forms.py`
  - `domains/experience-delivery/services/fatecat-delivery/src/web_report_service.py`
  - regression tests、API docs、roadmap、0016 docs
- Must not change:
  - 八字/紫微计算逻辑。
  - report_generator 输出正文内容。
  - 数据库 schema、Bot live、生产部署配置。

# Risk Matrix
| Risk | Level | Mitigation |
| --- | --- | --- |
| snapshotGate 锁得太细导致正常文案调整频繁失败 | medium | 只锁核心 heading 是否存在，不锁全文 hash。 |
| policyGate 误扫风险清单 | medium | Markdown gate 只扫描 `report.markdown` 正文字段。 |
| Web job dataclass 改动破坏页面渲染 | medium | 保持旧字段不变，只新增可选结构字段。 |
| 测试选择器过窄 | low | 同时跑 targeted 和 quick CI。 |

# Assumptions and Falsification
- Target end state: 所有用户可见 Markdown 报告结果都携带正文 policyGate 和结构 snapshotGate。
- Real constraints: 同步 API、异步 job、Web job 已对外存在，字段只能新增不能删除。
- Inertia constraints: 不能因为现有测试只看 Markdown 字符串，就继续让 gate 留在 capability JSON 摘要层。
- Wrong concept / wrong boundary: 把 capability envelope gate 当成完整报告正文 gate。
- Kill list: Markdown response 只有 `reportSystem/markdown`，没有可审计 gate。
- Proof point: API tests 证明同步、异步、Web 三条路径都有 `policyGate.status=pass` 和 `snapshotGate.status=pass`。
- Falsifier: 任一用户可见 Markdown 路径成功返回但缺 gate 字段，本切片失败。
- Migration slice: 本轮先覆盖 enabled Markdown systems bazi/ziwei；planned report systems 仍拒绝。
- Rejected short-term patches: 不只给同步 API 加字段；不在前端补字段；不写空 gate。

# Critical Ambiguities
- 完整 Markdown snapshot hash、diff 阈值、人工审核后台不在本轮。
- Bot Markdown 输出是否同源需要后续独立检查；本轮覆盖 Web/API job。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务是基础设施增强，不是已复现 bugfix。

# Future-Optimal Contract
- Target end state: Report resource 对 JSON、Markdown、job result 都具备 evidence、policy、snapshot 和 trace。
- Real constraints: 旧 API 兼容，公开 Web 不能展示复杂内部结构，外部连通不在本地验证范围。
- Inertia constraints: 旧结果 dict 只有 `markdown` 不应限制最终资源模型。
- Wrong concept / wrong boundary: Markdown 是最终字符串，不需要结构化 gate。
- Kill list: 多端 Markdown 结果缺少 policy/snapshot 机器证据。
- Proof point: 三条输出路径测试同时覆盖。
- Falsifier: gate 字段只出现在一个入口，或 snapshotGate 没有解析 heading。
- Migration slice: 先做 heading snapshot；后续可升级全文 snapshot/diff。
- Rejected short-term patches: 不使用硬编码 `status=pass`；不重写报告生成器。

# Ponytail Contract
- Existence check: 作为基础设施，用户可见报告正文必须可机器检查风险和结构。
- Selected ladder rung: 项目原生 helper；不引入依赖。
- Skipped scope: NLP 审核、全文黄金快照库、Bot live gate、远程策略服务。
- Ceiling / upgrade path: 当报告文案稳定后，升级为 golden snapshot manifest 和 diff 阈值。
- Do-not-simplify: 不删除旧字段；不改变报告正文；不误称完整合规。
- Minimal runnable check: 同步/异步/Web API regression + quick CI。
- Complexity review owner: 本轮用 tests/schema/docs 自审；后续 release gate 可交 auto-review。

# Document-Driven Contract
- Operating model update: not needed；定位未变。
- Toolchain model update: not needed；无新工具。
- Process update: not needed。
- Source-of-truth updates: updated；schema、API docs、roadmap、tasks。
- Local README/AGENTS impact: not needed；未新增目录。
- Contract/catalog/schema impact: updated；report schema 增加 Markdown gate 口径。
- ADR/Gate/module-context impact: not needed。
- Documentation exemption reason: none。
- Validation evidence: STATUS 记录真实命令输出。

# Task Package Context Map
| Node | Required Context |
| --- | --- |
| TP-01 | 0015 policyGate 差距、report schema |
| TP-02 | `report_policy.py` |
| TP-03 | `main.py`、`web_report_service.py`、`web_forms.py` |
| TP-04 | API/capability regression tests |
| TP-05 | local-ci、governance、task validators |
