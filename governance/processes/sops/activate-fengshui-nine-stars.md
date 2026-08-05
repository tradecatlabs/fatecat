---
id: SOP-CAP-FENGSHUI-NINE-STARS-ACTIVATE
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: activate_fengshui_nine_stars
route_aliases: ["实现风水九星", "接入九星 provider", "玄空九星能力投产"]
capability_id: fengshui_nine_stars
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 研发接入风水九星

## 任务定义
将三元九运、流年飞星和宫位结构实现为独立 `fengshui_nine_stars` provider。

## 当前状态
planned、L0 registered、test gate blocked；`mikaboshi` 仅为候选，未获生产准入。

## 适用场景
九运/流年飞星的 provider 研究与结构化接入；不用于建筑安全或强制搬迁建议。

## 输入要求
必填 `place`、`direction`、`targetYear`；可选 `floorPlan`、`birthDateTime`。方向基准、坐标系和户型数据格式必须明确。

## 前置条件
候选库 license/维护性审查；确定三元九运和飞星口径；建立方向边界与典型宫盘匿名 golden。

## 默认工具链
CapabilityExecutor、ProviderProtocol、location data、成熟候选库 adapter、pytest、provider lifecycle/drift。

## 固定路径
Profile `contracts/fate/capabilities/profiles/fengshui_nine_stars.json`、registry、fate-core provider/usecase、reference repos。

## 成熟参数
evidence 强制 `period`、`annualStars`、`palaces`、`ruleIds`；方向使用显式单位和基准，不接受模糊方位。

## 分步执行流程
1. 定义坐向与年份输入 contract。
2. 评审并锁定成熟库版本。
3. 建宫盘 golden、边界反例和风险策略。
4. 写薄 adapter，接入 CLI/API。
5. 完成证据、性能、分发和人工复核后申请晋级。

## 幂等与增量策略
相同 place/direction/year/version 结果可重放；户型扩展在基础宫盘稳定后独立增量。

## 限速与并发规则
计算任务有界并发；大户型文件限制大小和解析时间，不保存原图到 tracked 目录。

## 输出目录
`infra/runtime/local-state/exports/evaluations/fengshui-nine-stars/`。

## 命名规范
`fengshui-nine-stars-<year>-<direction>-<input-hash>.json`。

## 质量验收门禁
方向/年份 golden、字段完整、provider lifecycle/drift、API/CLI、安全和人工规则复核全部 PASS。

## 失败处理
方向不明确、坐标系未知、候选库漂移或专家未确认时维持 blocked。

## 恢复与重试策略
固定方向原始值重试；禁止自动四舍五入到相邻坐向掩盖边界错误。

## 安全边界
不得替代结构、消防、电气或其他建筑安全判断；不得强制用户搬迁。

## 临时文件清理
清除上传户型和候选仓缓存；只保存脱敏结构 hash。

## 运行记录登记
记录方向基准、provider 版本、golden hash、风险门禁和人工复核。

## 明确禁止事项
- 禁止把趣味建议包装成建筑专业意见。
- 禁止静默猜测坐向。
- 禁止未准入先暴露 Web/API。
