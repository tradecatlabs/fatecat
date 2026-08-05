---
id: SOP-CAP-ALMANAC-EXECUTE
type: process
status: current
owner: fate-analysis
route_key: execute_almanac
route_aliases: ["查询黄历", "执行黄历 capability", "计算基础择日数据"]
capability_id: almanac
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行黄历能力

## 任务定义
执行独立 `almanac` capability，返回日期范围内与事件类型相关的基础黄历推荐、避忌和证据。

## 当前状态
available、L3 validated、`fate-core-almanac-v1`；它是基础黄历，不代表完整择日体系。

## 适用场景
查询日期范围、事件类型和地点对应的基础黄历数据；不用于专业择日承诺或综合八字默认报告。

## 输入要求
必填 `dateRange`、`eventType`、`place`；可选 `birthDateTime`、`gender`。日期范围必须有界且格式符合 profile。

## 前置条件
bootstrap 完成；地点可解析；调用方接受民俗参考和非确定性边界。

## 默认工具链
`bash scripts/capability-cli.sh almanac --input-file <input.json> --pretty`；API 使用 `POST /api/v1/capabilities/almanac`。

## 固定路径
Registry、`contracts/fate/capabilities/profiles/almanac.json`、`fate_core.usecases.calculate_almanac` 和 capability protocol tests。

## 成熟参数
每次只处理业务需要的有界日期范围；默认结构化 JSON；`markdownDefault=false`；不得自动加入八字报告。

## 分步执行流程
1. 校验日期起止、事件类型和地点。
2. 将输入写入受控临时 JSON。
3. 调用 CLI 或 capability API。
4. 检查 `calendarDate`、`ruleIds`、`avoidReason`、`recommendReason` 和风险边界。

## 幂等与增量策略
同一输入和版本应确定性复现；批量日期按连续窗口切分，续跑只补缺失窗口。

## 限速与并发规则
遵守 delivery 默认限流；批量范围不使用无界并发，优先单请求有界窗口。

## 输出目录
`infra/runtime/local-state/exports/capabilities/almanac/`。

## 命名规范
`almanac-<start>-<end>-<event-slug>-<short-sha>.json`。

## 质量验收门禁
`tests/regression/test_capability_protocol.py`、`tests/regression/test_api_contracts.py` 和 `bash scripts/capability-cli-smoke.sh`。

## 失败处理
未知事件、无效范围、地点解析失败或 evidence 缺失时拒绝结果，不返回空壳推荐。

## 恢复与重试策略
修正输入后重跑；瞬时 API 错误按服务超时进行有限重试，不扩大日期范围兜底。

## 安全边界
只作民俗参考；不得替代医疗排期、法律期限、金融决策、工程安全或生育医疗建议。

## 临时文件清理
删除临时输入和未通过 gate 的输出；保留脱敏 summary/hash。

## 运行记录登记
记录 dateRange、eventType、place 标识 hash、engineVersion、输出 hash和 gate 状态。

## 明确禁止事项
- 禁止宣称完整择日已实现。
- 禁止混入默认综合八字 Markdown。
- 禁止输出“必吉”“必凶”等确定性断语。
