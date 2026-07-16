# Repo Evidence
- `classics-clean-v2`：14 documents、32,931 paragraphs、943 passages。
- 段落长度：中位数 21 字；12,125 个短于 12 字，24,781 个短于 30 字，证明大量记录只是排版物理行。
- passage 长度：中位数 1,175 字；中位数包含 33 个所谓 paragraph，最大 170 个。
- 142 个 passage 跨越已识别 heading path；`五行精纪` 单个 passage 最多跨 53 个目录标题。
- `minPassageChars` 当前只统计短切片，不参与组合算法。
- canonical TXT 总聚合 hash 已由 0163 锁定，v3 必须证明前后不变。

# Constraints Matrix
| Constraint | Type | Required Handling |
| --- | --- | --- |
| canonical TXT 不可变 | Hard | 只读；构建前后 hash 对账 |
| source-hash 绑定 policy | Hard | 目录范围和结构覆盖随 source hash 失效 |
| 全文语义无损 | Hard | 归一化指纹按源行精确重放 |
| 章节不可串联 | Hard | heading path 变化前 flush passage |
| 目录不进入检索正文 | Hard | navigation 保留为 paragraph 证据，但不进入 passage |
| 权限继续关闭 | Hard | distribution/production/training 全为 false |
| 无新依赖 | Preference | 使用 Python 标准库与现有脚本 |

# Change Boundary
- 修改：典籍数据集 schema/registry、`curation_policy.json`、现有 cleaner、data gate、专项测试和对应 README/AGENTS。
- 新增：只新增任务 0164；不新增第二个 cleaner、数据库或运行时消费者。
- 运行产物：写入 ignored `infra/runtime/local-state/exports/datasets/classics-clean-v3/`。

# Risk Matrix
| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| 合并源行时吞字或改字 | Medium | Critical | sourceLineNumbers + semantic fingerprint round-trip |
| 标题误判导致正文断碎 | Medium | High | 保守 heading parser、真实样本、只影响派生导航 |
| 目录范围越界或漂移 | Low | High | source hash 和闭区间 fail closed |
| 短章节被跨章合并 | Medium | High | heading path 变化强制 flush |
| v3 指标被硬编码成脆弱快照 | Medium | Medium | 锁不变量和已知边界，避免无意义精确全文快照 |
| 内存随语料增长 | Low | Medium | 当前线性扫描基线；记录 >100MB 升级 streaming 触发条件 |

# Assumptions and Falsification
- 假设：多数无句末标点的相邻短行是排版换行。若语义指纹不一致、段落数量不降或真实样本被错误拼接，则否证。
- 假设：目录可由 source-hash 绑定行范围可靠标注。若源 hash 或行范围变化，构建必须失败而不是猜测。
- 假设：heading path 是检索导航而非版本校勘。若需要学术章节树，应另立人工校勘任务，不扩大本轮规则。

# Critical Ambiguities
- “段落”在不同电子底本中没有统一空行语义；本轮定义为标题边界、强句末边界或长度上限形成的派生语义单元，不宣称等同原刻段落。
- “目录”只对已人工确认行范围分流；未确认的疑似目录保持正文，避免静默误删。

# Debug Evidence Contract
- 调试模式: Required
- Red evidence：v2 统计显示 12,125 个超短段落与 142 个跨 heading passage。
- Green evidence：v3 的 source replay error=0、heading boundary violation=0、navigation passage count=0，且真实样本语义段落可读。
- Regression evidence：专项测试、真实 14 本 build/validate、data gate、Quick CI。

# Task Package Context Map
| Node | Required Context | Output |
| --- | --- | --- |
| TP-01 | v2 schema、policy、目录行证据 | v3 contract 与结构 policy |
| TP-02 | source lines、heading parser、归一化不变量 | semantic paragraph records |
| TP-03 | paragraph types、heading paths | boundary-safe passages 与 validator |
| TP-04 | 14 本 canonical、v3 builder | 质量报告和回归证据 |
| TP-05 | diff、测试、治理和 Git 状态 | review/closeout/local commit |
