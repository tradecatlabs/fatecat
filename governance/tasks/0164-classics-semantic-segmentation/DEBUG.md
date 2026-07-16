# Debug Record

## Bug

- 标题：典籍物理换行被误当语义段落，检索 passage 跨越章节和目录。
- 症状：`classics-clean-v2` 中 12,125/32,931 个 paragraph 少于 12 字；142 个 passage 包含多个 heading path，单个切片最多跨 53 个目录标题。
- 首次发现位置 / 时间：2026-07-17，完成 0163 source-hash curation 后继续审计派生数据结构时发现。

## Environment

- 仓库 / 模块：FateCat `main`，`scripts/classics-dataset-clean.py` 与 14 本 canonical TXT。
- 数据集：`infra/runtime/local-state/exports/datasets/classics-clean-v2/`。
- 外部依赖：无；全部复现使用 Python 标准库和本地 ignored 派生数据。

## Reproduction

1. 读取 v2 `paragraphs.ndjson`，统计 `charCount < 12`。
2. 读取 v2 `passages.ndjson`，按 `paragraphIds` 回查每段 `headingPath`。
3. 统计一个 passage 中连续不同 heading path 的数量。
4. 对照 `三命通会`、`五行精纪`、`千里命稿` 等源文件，确认短记录来自排版换行和目录项。

## Observations

- O1：paragraph 长度中位数 21 字，36.8% 少于 12 字。
- O2：passage 长度中位数 1,175 字，但中位数含 33 个物理行记录，最大含 170 个。
- O3：142 个 passage 跨 heading path；`五行精纪` 目录造成单段跨 53 个标题。
- O4：builder 在每个非空源行直接创建 paragraph；passage 只按字符上限 flush，不检查 heading path。
- O5：`minPassageChars` 只形成质量计数，不影响切片组合。

## Hypotheses

### H1: （ROOT HYPOTHESIS）数据模型把物理源行错误等同于语义段落

- Supports：每个非空 `raw_line` 直接生成一个 paragraph，源文件普遍以固定宽度断行。
- Conflicts：部分 ctext 文件一行本身就是完整自然段，不能无条件合并所有相邻行。
- Test：将相邻源行按强句末和标题边界重建后，短段数量应显著下降且语义指纹完全一致。

### H2: passage builder 缺少章节边界约束

- Supports：当前 flush 条件只有 `max_chars`。
- Conflicts：当前 passage 保存第一个非空 heading path，表面上可能让单路径检查漏掉内部变化。
- Test：heading path 变化时强制 flush，真实语料 violation 应归零。

### H3: 目录与正文没有记录类型边界

- Supports：目录项被 heading parser 识别后仍进入 passage。
- Conflicts：不是所有短标题列表都是目录，不能靠通用启发式自动排除。
- Test：source-hash policy 标记 navigation 范围，paragraph 保留但 passage 零消费。

## Experiments

### E1

- Hypothesis: H1
- Change: 只读统计 v2 paragraph 长度并回查对应 canonical 物理行。
- Expected: 若假设成立，应出现大量由排版换行形成的超短 paragraph。
- Result: 观察到 12,125 个少于 12 字的 paragraph，并在 canonical 中确认固定宽度断行。
- Verdict: confirmed
- Revert: 只读实验，无需回滚。

### E2

- Hypothesis: H2
- Change: 只读回查 v2 passage 的全部 paragraph heading path。
- Expected: 若假设成立，单一 passage 会包含多个连续不同的 heading path。
- Result: 观察到 142 个跨 heading path 的 passage，最大跨 53 个路径。
- Verdict: confirmed
- Revert: 只读实验，无需回滚。

### E3

- Hypothesis: H3
- Change: 对照 policy、canonical 行号和 v2 passage 中的目录项。
- Expected: 若假设成立，已确认目录行会作为正文 paragraph 被 passage 消费。
- Result: `五行精纪` 等目录项进入 passage；v3 显式分流后 navigation passage count 为 0。
- Verdict: confirmed
- Revert: 只读实验，无需回滚。

## Root Cause

- 当前清洗器只完成字符归一化和定长拼接，没有建立“物理行、语义段落、导航记录、检索切片”之间的模型边界。

## Fix

- 已升级 v3 契约和 source-hash policy，显式登记 7 个已确认目录范围。
- 已实现物理行到语义段落的确定性状态机、精确 `sourceLineNumbers`、Markdown 层级归一和 `卷上/中/下` 标题识别。
- 已让 passage 只消费 body paragraph，并在 heading path 变化和字符上限处 flush。
- 已排除 20 条 Markdown 分隔线和 2 条现代结束标记，保留 exclusion 血缘。

## Regression Evidence

- 专项与数据门禁回归：17 passed，覆盖中英文换行、目录分流、heading 边界、policy 漂移、validator 负例和真实 14 本构建。
- 真实 v3：14 documents、16,079 paragraphs、1,430 passages、484 duplicate records；semantic replay、heading boundary、navigation passage、lineage error 均为 0。
- 双重重建 dataset aggregate 均为 `48076db9c604017c8cdf51495f5309c68b413d22c6f48324a4674cb5f654a310`；canonical aggregate 前后均为 `7fb963a33eab652d28c76500e7c99678b76c1c7630fa05724acd2e7e7f38c2e9`。
- data supply chain gate：355 checks passed。
- Quick CI：529 passed；evidence `/tmp/fatecat-local-ci-20260717045106`。
- deep review：PASS；重复证据只消费 body paragraph，navigation 与 heading 不再影响重复判定。

## Failed Nodes

- 无。

## First Invalid Node

- 无；原首个无效节点 TP-01 已通过 v3 contract 和回归闭合。

## Upstream Lineage

- canonical TXT、curation policy 和 `_prepare_records` 源行循环。

## Downstream Blast Radius

- 内部检索、规则提炼、人工复核和后续 RAG 数据准备；不影响当前八字/紫微计算结果。

## Lowest Common Refinement Ancestor

- 典籍派生数据中 physical line 到 semantic paragraph 的结构边界。

## Repair Boundary

- 数据集 contract/policy、owner cleaner、data gate、tests 和对应文档。

## Frozen Nodes

- canonical TXT、书目/版权人工结论、命理计算核心、Web/API/Bot 和生产部署。

## Invalidated Nodes

- v2 paragraph 可直接作为语义检索单元、v2 passage 保持章节一致性的声明。

## Reverification Required

- 语义回放、目录分流、heading boundary、确定性、canonical hash、专项测试、data gate 和 Quick CI。
