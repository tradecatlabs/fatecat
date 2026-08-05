---
id: SOP-CAP-DALIUREN-ACTIVATE
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: activate_daliuren
route_aliases: ["实现大六壬", "接入六壬 provider", "大六壬能力投产"]
capability_id: daliuren
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 研发接入大六壬

## 任务定义
将大六壬四课三传、天将和月将计算封装为独立 capability，并建立可追溯规则与投产门禁。

## 当前状态
planned、L0 registered、test gate blocked；现有资料和遗留字段不是生产 provider。

## 适用场景
算法研究、成熟实现复用、盘面 contract 和 golden 建设；不用于当前用户占事。

## 输入要求
目标必填 `question`、`castTime`、`place`，可选 `method`；研发需提供月将、贵人、涉害等口径与版权审查后的规则来源。

## 前置条件
候选实现和典籍用途获准；定义唯一课传算法；准备节气/月将、日干、昼夜贵人边界样本。

## 默认工具链
统一 capability/provider 协议、location/timezone、tracked classics 索引、pytest、provider supply-chain gates。

## 固定路径
Profile `contracts/fate/capabilities/profiles/daliuren.json`、registry、fate-core provider/usecase、classics data products、tests。

## 成熟参数
evidence 必须含 `fourLessons`、`threeTransmissions`、`heavenlyGenerals`、`ruleIds`；method 和 source version 不可省略。

## 分步执行流程
1. 选择可复用实现并完成 license/来源审查。
2. 固化四课三传和天将口径。
3. 建 red/golden/反例和证据 contract。
4. 接入 provider、CLI/API，保持 standalone。
5. 通过完整门禁和人类专业复核后申请 registry 晋级。

## 幂等与增量策略
相同时间、地点、method 复现同盘；先盘面后解释，规则按 registry 条目增量加入。

## 限速与并发规则
禁止共享全局盘面；批量样本有界并发，典籍索引只读。

## 输出目录
`infra/runtime/local-state/exports/evaluations/daliuren/`。

## 命名规范
规则 `daliuren.<layer>.<rule>`；fixture `daliuren-<boundary>-<case-id>.json`。

## 质量验收门禁
课传 golden、月将边界、字段完整、source/rule/trace、API/CLI、provider drift、版权和专家复核全部 PASS。

## 失败处理
算法派别冲突、资料版权不清、golden 不足或专业复核未接受时保持 blocked。

## 恢复与重试策略
固定输入和版本重放；只重算受影响规则层，不改原始 fixture 迎合输出。

## 安全边界
不输出确定未来或恐吓断语；未审查典籍原文不得公开分发。

## 临时文件清理
删除 raw 提取、候选仓和未审查原文副本；保留 hash、manifest 和脱敏证据。

## 运行记录登记
记录 method、source、provider、golden 覆盖、专家结论和阻断项。

## 明确禁止事项
- 禁止把遗留 `liuren.py` 直接列为 production。
- 禁止未经版权复核发布资料全文。
- 禁止以字段数量替代专业正确性验证。
