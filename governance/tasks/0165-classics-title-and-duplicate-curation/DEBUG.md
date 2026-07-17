# Debug Record

## Bug

- 标题：重复书名被标为多个 document_title，重复证据缺少关系语义。
- 症状：14 本数据有 29 个 title records；478 个 exact paragraph groups 全部使用同一 action，无法区分 404 个同家族共享文本、46 个同书重复和 28 个跨家族共享文本。
- 首次发现位置 / 时间：2026-07-17，完成 0164 后继续审计 v3 记录类型与复核可操作性时发现。

## Environment

- 仓库 / 模块：FateCat `main`，`scripts/classics-dataset-clean.py`。
- 数据集：ignored `classics-clean-v3`，14 本 canonical TXT。
- 外部依赖：无。

## Reproduction

1. 按 documentId 统计 `paragraphType=document_title`。
2. 按 exact paragraph group 的 documentIds 与 familyId 分类。
3. 对照 source/commentary 角色与原文内容，确认大部分跨文档重复发生在同一文献家族，不能据此自动删除。

## Observations

- O1：《神峰通考》8 个 title records，《滴天髓阐微》7 个。
- O2：重复书名出现在拼接分片或卷边界，文本必须保留但类型不应继续是文档身份。
- O3：《滴天髓》原文/阐微 213 条、《子平真诠》原本/评注 191 条精确重复。
- O4：当前 duplicate records 只有统一 action，没有 relationship。

## Hypotheses

### H1: （ROOT HYPOTHESIS）title matcher 缺少文档内状态

- Supports：每次文本等于 filename title 都无条件标为 document_title。
- Conflicts：后续重复书名仍是有意义的分片边界，不能直接排除。
- Test：只将首次命中标为 title，后续命中标为 heading；source replay 不变且 title count <=1。

### H2: duplicate evidence 缺少文献家族上下文

- Supports：familyId 和 documentRole 已存在，但 duplicate builder 未消费 documents。
- Conflicts：family 相同不证明具体版本谱系，只能描述结构关系。
- Test：由 documents 重算三类 relationship，tamper 任一字段时 validator 失败。

### H3: review queue 缺少聚合入口

- Supports：21 项明细需要逐行扫描才能判断问题类型和阻断范围。
- Conflicts：不应新增重复 sidecar 或人工结论。
- Test：quality report 用 Counter 聚合，validator 与明细精确对账。

## Experiments

### E1

- Hypothesis: H1
- Change: 只读列出全部 document_title 的 documentId、行号和文本。
- Expected: 若成立，同书第二次以后命中集中在分片/卷边界。
- Result: 29 条 title 中 18 条是同文档重复书名，最多单书 8 条。
- Verdict: confirmed
- Revert: 只读实验。

### E2

- Hypothesis: H2
- Change: 只读按 documentIds/familyId 聚合 478 个 exact paragraph groups。
- Expected: 若成立，应稳定分成同书、同家族跨文档、跨家族三类。
- Result: 46 / 404 / 28。
- Verdict: confirmed
- Revert: 只读实验。

### E3

- Hypothesis: H3
- Change: 只读聚合 review queue 的 issueType、severity 和 blocks。
- Expected: 所有统计可从 21 条明细确定性生成。
- Result: issueType 10 类、severity 2 类、blocks 10 类，均可用 Counter 重算。
- Verdict: confirmed
- Revert: 只读实验。

## Root Cause

- cleaner 已有文档级 family/role 元数据，但段落构建和重复证据阶段没有消费必要状态，导致文档身份与章节边界混淆、重复关系被压扁。

## Fix

- 在语义段落状态机中增加文档内 `document_title_seen`：首次命中是 `document_title`，后续重复书名保留为一级 `heading` 并形成 passage 边界。
- duplicate records 按文档集合与 `familyId` 分类为同书重复、同族共享文本、跨族共享文本；不使用“继承”名称推断版本谱系。
- quality report 聚合 title、duplicate relationship、review issue/severity/block；validator 从明细重算并拒绝篡改。
- 保持 canonical、source/copyright manifest、21 项 pending review 和权限边界不变。

## Regression Evidence

- red 阶段 3 个测试按预期失败：缺 review summaries、重复 title 数量为 2、duplicate relationship 缺失。
- green 专项与数据门禁回归：20 passed，覆盖重复书名 heading 边界、三类 duplicate relationship、review summaries、tamper rejection 和真实 14 本。
- 真实 v3：14 documents、16,079 paragraphs、1,437 passages、484 duplicate records、146 exclusions、21 pending reviews。
- title records 从 29 收敛到 11，多 title 文档为 0；3 本无显式书名的文档不伪造 title。
- duplicate relationship records：同族共享文本 407、同书重复 46、跨族共享文本 31；所有关系由明细可重算，未自动删除正文。
- semantic replay、heading boundary、navigation passage、lineage error 均为 0；data supply chain gate 355 checks passed。
- 连续重建耗时 2.717s / 2.786s / 2.764s，最大常驻内存约 119 MB；当前 14 文档下 document-pair O(d²) 不是瓶颈。
- artifact-list hash 为 `4f9032ed328242a4600db520cd6ef12dcb1fbd81159ed2baacfe46e028c99132`；canonical aggregate 前后均为 `7fb963a33eab652d28c76500e7c99678b76c1c7630fa05724acd2e7e7f38c2e9`。
- Quick CI：532 passed in 75.14s；evidence `/tmp/fatecat-local-ci-20260717081327`。
- deep review：PASS；principle gate scan 检查 5 个实现文件、0 findings。审查期间将 `same_family_inheritance` 收敛为 `same_family_shared_text`，避免超出证据推断传承方向。

## Failed Nodes

- 无；red failures 已由 TP-02/TP-03 修复并进入回归。

## First Invalid Node

- 无；原首个无效节点 TP-01 已由契约和 red/green evidence 闭合。

## Upstream Lineage

- filename title、curation policy familyId/documentRole、paragraph/passages。

## Downstream Blast Radius

- 典籍导航、重复复核、规则提炼和人工审计；不影响八字/紫微计算或公开报告。

## Lowest Common Refinement Ancestor

- v3 派生记录的文档身份与关系语义。

## Repair Boundary

- schema、owner cleaner、validator/data gate、tests 和对应文档。

## Frozen Nodes

- canonical、source/copyright manifest、人工 review 结论、生产 capability 和交付层。

## Invalidated Nodes

- “同文档可有多个 document_title”和“所有 duplicate evidence 关系相同”的隐含假设。

## Reverification Required

- title 唯一性、heading boundary、source replay、duplicate classification、review summary、确定性、canonical hash、专项测试、data gate 和 Quick CI。
