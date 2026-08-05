---
id: SOP-DEV-PROVIDER-SUPPLY-CHAIN
type: process
status: current
owner: platform
route_key: audit_provider_supply_chain
route_aliases: ["扫描 provider 漂移", "检查 vendor 健康", "审计来源许可证"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 审计 Provider 供应链

## 任务定义
聚合 provider lifecycle、依赖执行、来源、版本、license、vendor hash 和漂移基线，判断生产 provider 是否仍可复现。

## 当前状态
本地 lifecycle/dependency/drift gates 成熟；法律许可证最终意见和真实公网依赖仍需外部复核。

## 适用场景
依赖升级、vendor 更新、provider 变更、定期供应链巡检或发布前审计。

## 输入要求
tracked registry、provider manifests、source/license refs、vendor 快照和当前 commit。

## 前置条件
bootstrap 完成；reference repos 未被运行态修改；无未登记 vendor 更新。

## 默认工具链
`bash scripts/vendor-health.sh`、`provider-lifecycle-gate.sh`、`provider-dependency-smoke.sh`、`provider-drift-scanner.sh`。

## 固定路径
`contracts/fate/capabilities/`、`contracts/fate/providers/`、`tools/reference-repos/`、`catalog/`。

## 成熟参数
drift scanner 默认输出本地 JSON；所有 production provider 必须 version lock、source/license/resource manifest 和 passing health。

## 分步执行流程
1. 运行 vendor health。
2. 运行 lifecycle gate。
3. 运行 dependency smoke。
4. 生成 drift report并与 baseline/trend 比较。
5. 对 source/license 变化执行人工复核并更新 contract。

## 幂等与增量策略
同一 commit/vendor hash 应同结果；只重审发生变化的 provider，但发布门禁覆盖全部 production provider。

## 限速与并发规则
本地 provider smoke 有界执行；不得并发修改 reference repo；外部探测另行限速。

## 输出目录
`infra/runtime/local-state/exports/provider-governance/`。

## 命名规范
`provider-drift-<short-sha>-<UTC>.json`，趋势按 provider ID 分组。

## 质量验收门禁
vendor/lifecycle/dependency/drift 全 PASS；source/license refs 存在；无未解释版本漂移。

## 失败处理
hash、版本、license 或健康失败时阻断 release，不静默使用 vendor fallback。

## 恢复与重试策略
锁回已验证版本或完成升级评审；重跑受影响 provider及全局 drift gate。

## 安全边界
不得执行来源仓未知脚本；不输出私有仓凭证；license 不确定必须人工复核。

## 临时文件清理
删除临时 clone/build cache；不修改 tracked reference snapshot 以清理告警。

## 运行记录登记
记录 provider/version/source/license/hash、drift 分类、gate 和人工结论。

## 明确禁止事项
- 禁止无 manifest 更新 vendor。
- 禁止把“能 import”视为供应链通过。
- 禁止自动作法律许可结论。
