---
id: SOP-CAP-NAME-MARRIAGE-ACTIVATE
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: activate_name_marriage
route_aliases: ["实现姓名合婚", "接入合婚 provider", "姓名关系能力投产"]
capability_id: name_marriage
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 研发接入姓名合婚

## 任务定义
建立双方输入、匹配因素、证据和风险边界明确的独立 `name_marriage` capability。

## 当前状态
planned、L0 registered、test gate blocked；候选 `bazi-name` 与遗留姓名/合婚模块均未生产化。

## 适用场景
姓名与八字合参能力的 contract、provider 和评测建设；不用于当前关系决策。

## 输入要求
必填 `personA`、`personB`；可选 `relationshipGoal`、`calendarPreference`。双方同意、字段口径和最小化收集必须明确。

## 前置条件
完成隐私影响评估；区分姓名学、八字合参和民俗生肖；建立非歧视、非决定性输出规则。

## 默认工具链
CapabilityExecutor、ProviderProtocol、现有 bazi provider 只读复用、schema、policy gate、privacy tests。

## 固定路径
Profile `contracts/fate/capabilities/profiles/name_marriage.json`、registry、fate-core provider/usecase、security/privacy contracts。

## 成熟参数
evidence 强制 `personA`、`personB`、`compatibilityFactors`、`ruleIds`；不得生成单一“匹配分数”替代因素解释。

## 分步执行流程
1. 定义最小双方输入和同意边界。
2. 分离姓名、八字和民俗因素。
3. 建匿名对称性、交换顺序和歧视性反例。
4. 写 provider 编排，复用已准入八字结果。
5. 通过隐私、证据、专家和发布门禁后申请晋级。

## 幂等与增量策略
双方顺序互换不得改变对称因素；新增因素必须独立 version 和 evidence，不覆盖旧结论。

## 限速与并发规则
双方数据按单任务处理；禁止批量画像和无界配对计算。

## 输出目录
`infra/runtime/local-state/exports/evaluations/name-marriage/`，只允许匿名 fixture。

## 命名规范
`name-marriage-<anonymous-case-id>-<engine-version>.json`。

## 质量验收门禁
输入同意、对称性、隐私脱敏、非歧视 policy、evidence、API/CLI/provider 和专家复核全部 PASS。

## 失败处理
缺任一方同意、输入不全、歧视风险或 evidence 缺失时拒绝执行并保持 blocked。

## 恢复与重试策略
只在相同匿名输入上重放；不得通过删除不利因素制造通过。

## 安全边界
不得输出“必离婚”、人格贬损、性别/地域歧视或替代心理法律建议。

## 临时文件清理
立即删除双方身份信息和临时报告；tracked 测试只留合成匿名样本。

## 运行记录登记
只登记双方输入 hash、同意状态、规则版本、gate 和人工复核，不登记姓名与出生信息。

## 明确禁止事项
- 禁止在未获双方同意时处理。
- 禁止单一分数决定关系。
- 禁止把两个八字报告简单拼接为合婚能力。
