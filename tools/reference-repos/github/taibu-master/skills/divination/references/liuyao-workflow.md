# Liuyao Workflow (固定顺序)

## 0. Input Check

- **⏰ 先获取当前时间**（用于时机层分析参照）
- 必要输入：`question`, `yongShenTargets`
- 可选输入：
  - `method` — `auto`(默认自动起卦) / `select`(选卦模式)
  - `hexagramName` — 选卦模式下：卦名（如"天火同人"）或6位卦码（如"101111"）
  - `changedHexagramName` — 选卦模式下：变卦名或卦码（可选，提供后自动计算变爻）
  - `date` — 占卜日期（ISO格式），默认今天
  - `seed` — 随机种子，固定后可复现结果
- 问题必须单一且可验证（时间/目标明确）
- 复杂问题先拆分，不做混题断卦
- `yongShenTargets` 语义判断参考：

| 用神目标 | 适用问题范畴                                 |
| -------- | -------------------------------------------- |
| `父母`   | 合同文书、证件、学业考试、房屋车辆、长辈     |
| `官鬼`   | 功名求官、工作事业、规则法律、压力风险、疾病 |
| `兄弟`   | 同辈关系、合作伙伴、竞争对手                 |
| `妻财`   | 感情婚姻、钱财收入、资源获取                 |
| `子孙`   | 子女后辈、医药治疗、娱乐休闲、学生/下属      |

## 1. 卦象层

- 从 output 提取：
  - `hexagramName` / `changedHexagramName` → 本卦/变卦
  - `hexagramGong` / `hexagramElement` → 卦宫/五行
  - `guaCi` / `xiangCi` → 卦辞/象辞（辅助理解）
  - `ganZhiTime` → 占卜干支时间
  - `kongWang` → 旬空地支
- 标注是否 `liuChongGuaInfo.isLiuChongGua`（六冲卦）
- 检查 `sanHeAnalysis`（三合局 / 半合）
- 检查 `globalShenSha[]`（整盘级神煞）

## 2. 用神层（Mandatory）

- 使用 `yongShen[]` 分组列表分析：
  - `targetLiuQin` → 目标六亲
  - `candidates[0]` 为主用神，后续为候选
  - 每个候选含 `strengthScore`, `isStrong`, `movementState`, `kongWangState`, `factors[]`
- 结合 `shenSystemByYongShen[]` 分析：
  - `yuanShen`（原神）→ 辅助用神的力量
  - `jiShen`（忌神）→ 克制用神的力量
  - `chouShen`（仇神）→ 生忌神的力量
- 比较候选强弱（旺衰、动静、空破、受生受克）
- 若用神不在卦中，检查 `fuShen[]`（伏神）：含 `isAvailable` 和 `availabilityReason`

## 3. 结构关系层

- 分析世应关系（通过 `fullYaos[].isShiYao` / `isYingYao` 定位）
- 分析动爻变爻（`fullYaos[].isChanging` + `changedYao`）：
  - `changedYao.relation` → 变爻关系（回头克/回头生/化进/化退等）
  - `changedYao.liuQin` / `wuXing` → 变出六亲/五行
- 参考 `fullYaos[].liuShen`（六神）辅助判断事态特质
- 参考 `fullYaos[].changSheng`（十二长生）辅助旺衰定位
- 判断关键阻力来自哪里（时间、人、资源、判断偏差）

## 4. 时机层（Mandatory）

- 使用 `timeRecommendations[]` 结构化时间建议：
  - `type`: favorable / unfavorable / critical
  - `startDate` / `endDate`: 时间窗口
  - `confidence`: 置信度 (0-1)
  - `description`: 描述
- 结合时间建议输出：
  - 何时可推进
  - 何时宜观察
  - 何时需止损
- 检查 `warnings[]` 获取凶吉警告
- 明确时间窗口而非泛泛而谈

## 5. 结论层

- 给出倾向结论：`成/可成但延迟/暂难成`
- 每个结论必须绑定证据点（引用 `fullYaos` 爻位或 `yongShen` 强度数据）

## 6. Quick Template

1. 结论摘要（结果倾向 + 关键时间窗口）
2. 核心依据（用神状态 + 世应 + 动爻）
3. 风险点（空亡、冲克、伏神受制）
4. 行动建议（当下一周/一月具体做法）
