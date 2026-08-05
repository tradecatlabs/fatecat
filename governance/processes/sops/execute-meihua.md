---
id: SOP-CAP-MEIHUA-EXECUTE
type: process
status: current
owner: fate-analysis
route_key: execute_meihua
route_aliases: ["梅花起卦", "执行梅花易数", "计算梅花 capability"]
capability_id: meihua
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行梅花易数能力

## 任务定义
按明确起卦方式执行 `meihua` capability，输出本卦、互卦、变卦、体用和规则证据。

## 当前状态
available、L3 validated、`fate-core-meihua-v1`；只保证盘面与证据，不保证完整断事体系。

## 适用场景
时间或数字起卦的结构化研究与娱乐参考；不适用于六爻、奇门或确定性未来判断。

## 输入要求
必填 `question`、`castMethod`；可选 `castValue`、`castTime`、`place`。起卦方法对应字段必须完整。

## 前置条件
bootstrap 完成；问题不含高风险请求；时间和地点若提供必须明确时区。

## 默认工具链
`bash scripts/capability-cli.sh meihua --input-file <input.json> --pretty`；API 使用 `POST /api/v1/capabilities/meihua`。

## 固定路径
Registry、`contracts/fate/capabilities/profiles/meihua.json`、`fate_core.usecases.calculate_meihua`、capability/API tests。

## 成熟参数
默认结构化 JSON、`markdownDefault=false`；起卦值由用户提供，不使用隐藏随机源；同一输入必须可重放。

## 分步执行流程
1. 校验问题、起卦法及其必需值。
2. 规范化时间和地点。
3. 调用 CLI/API。
4. 检查 `bodyUse`、`hexagram`、`mutualHexagram`、`changedHexagram`、`ruleIds`。

## 幂等与增量策略
固定 `castMethod`、`castValue`、`castTime` 后结果确定；不得在重试时重新随机起卦。

## 限速与并发规则
按服务默认限流；同一问题同一起卦标识只执行一次，批量任务使用有界队列。

## 输出目录
`infra/runtime/local-state/exports/capabilities/meihua/`。

## 命名规范
`meihua-<cast-method>-<UTC timestamp>-<input-hash>.json`。

## 质量验收门禁
capability protocol、API contracts、CLI smoke 全部通过，evidence 字段完整。

## 失败处理
起卦参数不匹配、时间无时区、规则证据缺失或风险策略失败时拒绝输出。

## 恢复与重试策略
保留原起卦参数重试；禁止因失败生成新随机值或改变时间。

## 安全边界
仅供研究和娱乐；不得用于医疗、法律、金融、生死或违法规避决策。

## 临时文件清理
清理含问题正文的临时输入；长期证据只保留脱敏 hash 和状态。

## 运行记录登记
记录 castMethod、输入 hash、engineVersion、卦象摘要 hash、gate 和 commit。

## 明确禁止事项
- 禁止输出确定未来或恐吓式断语。
- 禁止混入综合八字默认报告。
- 禁止失败重试时改变起卦随机性。
