---
id: SOP-CAP-LIUYAO-ACTIVATE
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: activate_liuyao
route_aliases: ["实现六爻", "接入六爻 provider", "六爻能力投产"]
capability_id: liuyao
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 研发接入六爻

## 任务定义
把已登记的 `liuyao` L0 协议推进为经过 provider、证据、golden、API 和风险门禁的独立 capability。

## 当前状态
planned、L0 registered、`testGate.status=blocked`；当前生产调用必须返回“尚未生产化”。

## 适用场景
六爻 provider 选型、适配、验证和投产申请；不适用于直接为用户起卦。

## 输入要求
目标输入为 `question`、`castMethod`，可选 `castValue`、`castTime`、`place`；研发还需候选库版本、许可证、算法口径和匿名 golden。

## 前置条件
完成成熟开源候选复核；批准任务包；确认世应、六亲、六神、动爻、月建日辰、空亡和应期边界。

## 默认工具链
统一 `ProviderProtocol`、`CapabilityExecutor`、现有 provider registry、capability schemas、pytest 和 provider lifecycle/drift gates。

## 固定路径
`contracts/fate/capabilities/profiles/liuyao.json`、registry、fate-core providers/usecases、`tests/regression/`、`tools/reference-repos/`。

## 成熟参数
provider 版本必须锁定；计算确定性必须为 true；evidence 强制 `hexagram`、`changingLines`、`sixRelatives`、`sixSpirits`、`ruleIds`。

## 分步执行流程
1. 评审候选库来源、license、维护状态和算法覆盖。
2. 写匿名输入/输出 contract 与 red tests。
3. 只写 adapter/usecase 胶水，注册 provider。
4. 补盘面 golden、evidence、planned rejection 转 passing 的测试。
5. 通过 lifecycle、drift、API、CLI、package 和安全门禁后申请 registry 状态迁移。

## 幂等与增量策略
起卦输入固定后必须可重放；先最小盘面，再逐项增加规则，不以空字段预占未来能力。

## 限速与并发规则
研发测试串行固定随机源；生产候选沿用有界 executor，不允许全局可变状态。

## 输出目录
测试证据写 `infra/runtime/local-state/exports/evaluations/liuyao/`；源码和 contract 写 canonical 路径。

## 命名规范
provider `liuyao.<implementation>`；规则 ID `liuyao.<domain>.<rule>`；golden 使用匿名 fixture ID。

## 质量验收门禁
协议/API/CLI/provider lifecycle/drift/package tests、匿名 golden、证据覆盖、风险断语扫描均 PASS，registry 才能从 blocked 迁移。

## 失败处理
候选库许可证不清、规则口径冲突、golden 不足或 trace 断链均保持 L0 blocked。

## 恢复与重试策略
冻结失败 provider 版本，修复最小适配层后重跑受影响门禁；不切换到 legacy 输出兜底。

## 安全边界
不得承诺确定未来，不替代医疗法律金融判断，不保存用户问题正文到 tracked fixture。

## 临时文件清理
删除候选仓临时 clone、构建缓存和含用户问题的输出；供应链 manifest 仅保留公开元数据和 hash。

## 运行记录登记
登记候选版本、license 结论、golden 覆盖、失败项、registry diff 和各 gate 证据。

## 明确禁止事项
- 禁止在 registry 仍为 planned 时提供生产执行。
- 禁止复制候选项目核心算法为自研私有实现。
- 禁止把 legacy 字段存在等同完整六爻能力。
