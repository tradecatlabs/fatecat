# Repo Evidence
- canonical 典籍：14 本，3,149,463 bytes，全部 UTF-8 可读。
- `copyright_review.tsv`：23 类 `review_required`，1 类 `blocked`，1 类 `blocked_until_manual_correction`。
- `source_manifest.tsv`：118 项、约 760 MB；当前 worktree 不包含 raw 实体。
- `classics_rule_index.json`：98 条规则，无精确 source span、置信度和逐规则版本。
- 算准网语料 3344 篇，仅限内部研究，本任务不处理。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 原典不可变 | 清洗器只读 `classics/*.txt` |
| 版权未闭合 | 输出继承 `review_required`，禁止公开分发声明 |
| 可复现 | 仅使用 Python 标准库；稳定排序、稳定 ID、SHA-256 |
| 可追溯 | 每个 passage 回指 document、source path、source hash 和 paragraph range |
| 防误删 | 重复只标记，不自动删除正文 |
| 仓库卫生 | 大型派生正文只进入 ignored local-state export |

# Change Boundary
- 新增清洗脚本、数据契约和回归测试。
- 更新 `scripts/AGENTS.md`、`tests/AGENTS.md`、`data-products/AGENTS.md` 与 `classics/README.md`。
- 不改生产 provider、报告输出、典籍原文、规则索引或供应链版权结论。

# Risk Matrix
| Risk | Level | Control |
| --- | --- | --- |
| 清洗改变原义 | High | NFC、空白清理为主；保留 source hash 和原段落序号 |
| 原本/评注交叉重复 | High | 文档家族和 exact paragraph overlap 报告，不随机去重 |
| 未授权内容外发 | High | 输出目录 ignored；manifest 固定 `distributionAllowed=false` |
| 误把短干支重复当垃圾 | Medium | 只统计，不自动删除重复行 |
| 切片过长或断裂 | Medium | 句界切分、字符预算和 round-trip 测试 |

# Assumptions and Falsification
- 假设：14 本 canonical TXT 是本轮唯一输入。若扫描发现非 UTF-8、NUL 或来源清单断链，生成必须失败。
- 假设：清洗结果仅用于内部规则提炼与检索实验。若用户要求公开训练集，必须另开版权审查任务。
- 证伪信号：相同输入产生不同 manifest hash、passage 无法回指 source、原文件被修改、输出宣称可分发。

# Critical Ambiguities
- “清洗”不等于删除重复命例或改写古文；本期只做可逆规范化与结构化。
- 原本与评注的包含关系需要专家定义保留策略，本期只输出 overlap 证据。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是已知 bug 修复；失败时保留最小输入 fixture、异常和输出目录，不用静默跳过坏数据。

# Task Package Context Map
## TP-01
- Step Key: `dataset-contract`
- 标题: 数据契约与边界
- 类型: `Contract`
- 目标: 定义清洗记录、血缘、质量、版权和输出边界
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 供应链 registry、source manifest、copyright review、dataset schema
- 输出: 清洗数据契约和任务验收边界
- 允许工具: 本地文件读取、JSON/Markdown 校验、apply_patch
- 禁止动作: 放宽版权、修改原文、访问外部网络
- 证据要求: JSON 解析、任务文档 strict 校验、diff
- 停止条件: 契约无法表达血缘或版权边界
- 风险: 契约过宽导致下游误用
- 备注: 原文不可变，派生结果可重建

## TP-02
- Step Key: `deterministic-cleaner`
- 标题: 确定性清洗器
- 类型: `Implementation`
- 目标: 用标准库实现规范化、段落、切片、重复、质量和 manifest
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: dataset-contract
- 依赖节点 ID: TP-01
- 输入: 14 本 canonical TXT 和 TP-01 契约
- 输出: `scripts/classics-dataset-clean.py`
- 允许工具: Python 标准库、apply_patch、本地临时目录
- 禁止动作: 覆盖输入、自动删除语义重复、引入第三方依赖
- 证据要求: fixture 两次运行输出一致
- 停止条件: 稳定 ID、原子输出或血缘无法保证
- 风险: 清洗改变古文原义
- 备注: 所有重复只标记

## TP-03
- Step Key: `tests-docs`
- 标题: 回归测试与文档
- 类型: `Verification`
- 目标: 固化正常、坏输入、重复、稳定性和边界行为并同步目录说明
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: deterministic-cleaner
- 依赖节点 ID: TP-02
- 输入: 清洗器和最小合成 fixture
- 输出: focused tests、README/AGENTS 更新
- 允许工具: pytest、临时目录、apply_patch
- 禁止动作: 测试访问网络或读取私有 raw
- 证据要求: focused pytest 通过
- 停止条件: 测试无法证明确定性或版权边界
- 风险: 测试只覆盖 happy path
- 备注: fixture 必须是合成文本

## TP-04
- Step Key: `dataset-build`
- 标题: 本地数据集生成与质量门禁
- 类型: `DataProduct`
- 目标: 生成并验证 14 本 canonical 典籍的本地派生数据集
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: tests-docs
- 依赖节点 ID: TP-03
- 输入: 真实 canonical TXT、manifest 和 copyright review
- 输出: ignored local-state dataset export 和质量摘要
- 允许工具: 清洗器 CLI、hash 校验、只读统计
- 禁止动作: 提交派生正文、处理算准网或 raw
- 证据要求: 14/14、零血缘错误、validate-only 通过
- 停止条件: 任一文档无法读取或来源断链
- 风险: 大文件输出、跨书重复和段落切片偏差
- 备注: 质量报告可记录 WARN，但硬错误必须失败

## TP-05
- Step Key: `review-closeout`
- 标题: 审查与版本控制收口
- 类型: `Review`
- 目标: 完成 correctness/license/performance/document drift 审查与交付
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: dataset-build
- 依赖节点 ID: TP-04
- 输入: tracked diff、测试结果、本地质量摘要
- 输出: review 结论、任务证据、语义提交
- 允许工具: auto-review、quick CI、git 非破坏性操作
- 禁止动作: 推送远端、提交 ignored 正文或重写历史
- 证据要求: quick CI、task strict、git diff/status
- 停止条件: 存在 BLOCK 或未解释失败
- 风险: 文档/任务状态与实际交付漂移
- 备注: push 需用户后续明确要求
