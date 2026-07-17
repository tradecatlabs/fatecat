# Repo Evidence
- v3：14 documents、16,079 paragraphs、1,430 passages、484 duplicate records、21 review items。
- `paragraphTypeCounts.document_title=29`，但只有 11 本存在书名文本；《神峰通考》被标 8 次，《滴天髓阐微》被标 7 次。
- 478 个 exact paragraph groups：同家族跨文档 404、同文档 46、跨家族 28。
- 最大两组同家族共享文本为《滴天髓》原文/阐微 213 条、《子平真诠》原本/评注 191 条；该统计不证明版本传承方向。
- 21 项人工复核：high 13、medium 8；主要为底本、书目归属、贡献者角色、缺卷、截断与版权问题。

# Constraints Matrix
| Constraint | Type | Required Handling |
| --- | --- | --- |
| canonical TXT 不可变 | Hard | 只读并校验 manifest/hash |
| 重复不等于应删除 | Hard | 只分类、保留全部正文和血缘 |
| 人工结论不可伪造 | Hard | review status 保持 pending_human_review |
| v3 消费兼容 | Hard | 只增加字段和修复错误类型，不新增数据集分支 |
| 确定性 | Hard | 分类仅依赖 familyId、documentRole 和 documentId |
| 性能 | NFR | 线性分组；禁止重复全表嵌套扫描 |

# Change Boundary
- 修改：现有 v3 schema、cleaner、数据供应链 gate、专项测试、README/AGENTS 和任务证据。
- 不修改：canonical、source/copyright manifest、curation 人工结论、Web/API/Bot 与命理计算核心。
- 运行产物：继续只写 ignored `classics-clean-v3`。

# Risk Matrix
| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| 重复书名转换后 heading path 错乱 | Medium | High | 合成边界测试 + 真实 violation=0 |
| 把正常原文/评注共享文本误报为异常 | High | High | relationship 只描述结构，不给删除动作 |
| duplicate 字段可被篡改 | Medium | High | validator 从 documents/paragraphs 重算 |
| 统计与明细漂移 | Medium | Medium | quality summary 精确重算 |
| 新分类放大构建时间 | Low | Medium | document map + hash groups，保持 O(n) 主路径 |

# Assumptions and Falsification
- 假设：同文档中第二次及以后出现的书名是卷/分片边界，不是第二个文档身份。若转换导致正文丢失或章节串联，则否证。
- 假设：familyId 相同的跨文档精确重复应标为 same-family shared text。若 familyId 未经 policy 约束或分类不稳定，则否证。
- 假设：复核摘要可完全由 review queue 重算。若摘要与明细无法一一对账，则失败。

# Critical Ambiguities
- `same_family_shared_text` 只表示同一文献家族中存在精确相同文本，不证明底本先后、作者关系或版权状态。
- `cross_family_shared_text` 只表示精确文本相同，不判定抄袭、引用或共同来源。
- 缺少显式标题的 3 本书不自动注入虚构 title paragraph；只要求最多一个，不要求必须一个。

# Debug Evidence Contract
- 调试模式: Required
- Red：单文档出现 2-8 个 document_title；所有重复记录统一 `retain_and_review`，无法区分 404/46/28 三种关系。
- Green：每文档 title count <=1；重复 relationship 与重新计算结果一致；正文 fingerprint、计数和 canonical hash 不变。
- Regression：合成边界、分类、tamper、真实 14 本、data gate、Quick CI。

# Task Package Context Map
| Node | Required Context | Output |
| --- | --- | --- |
| TP-01 | v3 schema、title/duplicate red evidence | contract 与 red tests |
| TP-02 | title matcher、heading state machine | 唯一 title 与重复书名 heading |
| TP-03 | familyId、documentRole、duplicates/review queue | relationship 与 quality summaries |
| TP-04 | 14 本 canonical、validator | deterministic green evidence |
| TP-05 | diff、review、CI、治理和 Git | closeout 与本地 commit |
