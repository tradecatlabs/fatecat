# Repo Evidence
- 一期产物：14 documents、33055 paragraphs、946 passages、567 duplicate records。
- `渊海子平 - 徐子平.txt` 的 1-64 与 4664-4713 行含下载站/公众号包装，正文主体位于 65-4663 行。
- 6 本 ctext 整理稿把 `整理说明`、`来源`、`抓取范围`、`来源章节` 写在 canonical TXT 中，当前被误当作检索正文。
- `三命通会` 明示卷十至卷十二缺失；`五行精纪` 明示缺第二十、第三十卷且尾行截断。
- `滴天髓原文` 与 `滴天髓阐微` 段落包含率约 0.862；`子平真诠原本` 与评注约 0.642，应建文献家族而非删除重复。
- 多个文件存在书名、作者、原著/评注者混写，必须保留 observed metadata 并进入人工复核。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 原典不可变 | policy 只控制派生正文选择，不修改 TXT |
| 规则可审计 | 每个文档策略绑定 `sourceSha256`，源变更立即失败 |
| 不误删古文 | 仅允许显式行范围和标准化 envelope 前缀；无通用广告关键词黑箱 |
| 书目不臆断 | observed 与 reviewed metadata 分离，默认 `review_required` |
| 版权不放宽 | 继承一期三项 false 权限边界 |
| 家族不去重 | 原本/评注只建立关系和 overlap 证据，不合并正文 |

# Change Boundary
- 新增 `classics/curation_policy.json` 及其 schema/registry 接线。
- 增强 `scripts/classics-dataset-clean.py` 和专项测试。
- 更新 classics 数据产品文档与任务证据。
- 不改 production provider、报告、规则索引或 canonical TXT。

# Risk Matrix
| Risk | Level | Control |
| --- | --- | --- |
| 行范围错误导致正文丢失 | High | source hash 绑定、逐文档 round-trip、负向 fixture |
| 关键词误删古籍正文 | High | 禁止通用关键词过滤，只接受显式 policy |
| 作者候选被包装成事实 | High | observed/reviewed 分离，reviewed 默认为 null |
| 缺卷文本被当完整语料 | High | completeness 状态与 issue queue |
| policy 漂移未被发现 | Medium | registry、contract、validate-only 和 focused test |

# Assumptions and Falsification
- 假设：当前 canonical hash 是二期策略的唯一输入版本；任一 hash 变化则生成失败。
- 假设：渊海正文选择 65-4663 来自当前文件人工检查；若发现正文位于范围外，必须调整 policy 并补回归。
- 证伪信号：来源 URL/推广文仍进入 passage、正文语义 fingerprint 与选择后源文本不等价、未核实书目字段被标记 verified。

# Critical Ambiguities
- “完整”仅表示当前文本是否有明确缺失证据，不等于与权威底本校勘完成。
- “作者”可能混合原作者、编者、注者、评注者或托名；本轮只记录 observed 值和待审原因。
- ctext wiki 页可作为当前电子来源，不证明底本、作者和版权已完成权威核验。

# Debug Evidence Contract
- 调试模式: Optional
- 策略失配必须输出 source path、expected/actual hash 或 line rule，不输出大段正文。

# Task Package Context Map
## TP-01
- 输入：canonical TXT、一期质量报告、source/copyright manifests。
- 输出：污染、完整性、家族与元数据异常清单。
- Gate：每个结论可定位到文件和行或 manifest 字段。

## TP-02
- 输入：TP-01 清单。
- 输出：`curation_policy.json` 与 schema。
- Gate：14/14 覆盖，所有策略绑定 source hash，verified 字段不得伪造。

## TP-03
- 输入：policy 与一期清洗器。
- 输出：策略驱动正文选择、embedded metadata 和 review queue。
- Gate：policy 缺失/漂移/越界 fail closed。

## TP-04
- 输入：合成 fixture 和 14 本真实语料。
- 输出：专项测试、重建数据集、噪声零命中和质量摘要。
- Gate：canonical hash 不变、lineage error=0。

## TP-05
- 输入：diff、测试、真实产物和性能证据。
- 输出：review、Quick CI、task closeout 和本地提交。
- Gate：无 BLOCK，ignored 正文不进入 Git；不自动 push。
