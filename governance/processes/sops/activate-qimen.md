---
id: SOP-CAP-QIMEN-ACTIVATE
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: activate_qimen
route_aliases: ["实现奇门", "接入奇门 provider", "奇门能力投产"]
capability_id: qimen
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 研发接入奇门遁甲

## 任务定义
将 `qimen` 的协议登记转化为独立、确定、证据化且可拒绝高风险请求的生产候选 provider。

## 当前状态
planned、L0 registered、test gate blocked；没有可发布的生产计算链。

## 适用场景
时家奇门 provider 选型、宫盘结构化、规则验证和投产；不用于现阶段直接问事或择时。

## 输入要求
目标必填 `question`、`castTime`、`place`，可选 `method`；研发需明确阴阳遁、局数、拆补/置闰、转盘/飞盘口径。

## 前置条件
完成候选开源仓与许可证复核；选定唯一算法口径；准备跨节气、跨日和典型宫盘匿名 golden。

## 默认工具链
ProviderProtocol、CapabilityExecutor、capability schemas、location/timezone 基础设施、pytest、provider lifecycle/drift。

## 固定路径
Profile `contracts/fate/capabilities/profiles/qimen.json`；registry；fate-core provider/usecase；reference repos；regression tests。

## 成熟参数
必须输出 `doors`、`stars`、`gods`、`stems`、`palaces`、`ruleIds`；engineVersion 和 method 固定入证据。

## 分步执行流程
1. 固化算法派别与时间边界。
2. 建立 schema、匿名 golden 和反例。
3. 适配成熟库，不复制底层排盘算法。
4. 注册 provider 并接入 CLI/API。
5. 运行证据、风险、漂移、分发和性能门禁后申请晋级。

## 幂等与增量策略
相同 castTime/place/method 必须复现；先完成盘面，不提前输出未经验证的断语。

## 限速与并发规则
并发计算禁止共享可变盘对象；批量 golden 使用受控进程和固定时区。

## 输出目录
`infra/runtime/local-state/exports/evaluations/qimen/`。

## 命名规范
`qimen.<method>.<rule>`；fixture `qimen-golden-<case-id>.json`。

## 质量验收门禁
时间边界 golden、九宫字段完整、rule/source/trace、API/CLI、provider gate、安全禁用词和 package smoke 全部 PASS。

## 失败处理
派别未定、宫盘不一致、时间边界漂移或证据缺失时维持 blocked。

## 恢复与重试策略
按固定 provider/version 重放失败 fixture；不得通过切换 method 或时区掩盖。

## 安全边界
禁止军事行动、违法规避和确定未来建议；地点只用于计算，不作现实目标定位。

## 临时文件清理
清理候选仓缓存和临时 golden；只提交脱敏 fixture、manifest 和验证摘要。

## 运行记录登记
记录 method、时区口径、provider 版本、fixture hash、差异和 gate。

## 明确禁止事项
- 禁止调用 legacy `qimen.py` 即宣称生产化。
- 禁止多派别结果静默混合。
- 禁止 registry 门禁未通过先开放 Web/Bot。
