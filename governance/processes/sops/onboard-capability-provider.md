---
id: SOP-CAP-PROVIDER-ONBOARD
type: process
status: current
owner: platform
route_key: onboard_capability_provider
route_aliases: ["新增未知测算能力", "注册新 capability", "新增通用 provider"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 接入新的 Capability Provider

## 任务定义
为尚未登记的新测算体系建立 capability contract、成熟 provider 适配、证据策略、风险政策和发布门禁。

## 当前状态
统一 ProviderProtocol/registry/executor 已生产使用；本 SOP 不适用于 registry 已列出的明确 capability。

## 适用场景
新增全新体系或替换生产 provider；已登记六爻等体系必须使用各自激活 SOP。

## 输入要求
能力定义、输入/输出 schema、成熟开源候选、版本/license/source、evidence 字段、风险声明、golden 与维护 owner。

## 前置条件
完成存在性检查和胶水原则评审；确认该能力不能通过现有 capability 扩展完成；建立批准任务包。

## 默认工具链
`CapabilityExecutor`、`ProviderProtocol`、provider registry、capability schema、lifecycle/drift/dependency smoke、pytest。

## 固定路径
`contracts/fate/capabilities/`、`domains/fate-analysis/services/fate-core/src/fate_core/capabilities/`、providers/usecases、`catalog/`、tests。

## 成熟参数
初始状态必须 `availability=planned`、`maturity=L0`、`testGate=blocked`；engineVersion、deterministic、evidencePolicy 和 riskPolicy 必填。

## 分步执行流程
1. 证明能力对象应存在并选择成熟候选。
2. 先登记 planned contract/profile 和拒绝测试。
3. 建 adapter、usecase、golden/evidence，不复制底层通用算法。
4. 接入 CLI/API 和资源发现。
5. 通过 lifecycle、dependency、drift、package、安全和专业复核后按 ADR 晋级。

## 幂等与增量策略
先 registry planned，再最小计算，再解释层；每次状态迁移单向、有证据、可回滚。

## 限速与并发规则
provider 必须无请求间共享可变状态；批量评测有界并发并声明资源上限。

## 输出目录
代码和 contract 进入 canonical 路径；评测证据进入 `infra/runtime/local-state/exports/evaluations/<capability>/`。

## 命名规范
capability ID 使用稳定 snake_case；provider ID `<capability>.<implementation>`；规则 ID `<capability>.<domain>.<rule>`。

## 质量验收门禁
schema、planned rejection、golden、evidence、API/CLI、provider lifecycle/drift/dependency、package、security、performance 和专业复核。

## 失败处理
任一来源、许可证、确定性、证据或风险门禁失败时维持 planned，不建立 fallback。

## 恢复与重试策略
回退 provider 注册和状态迁移；旧 production provider 在新版本验证完成前保持唯一真相源。

## 安全边界
禁止无免责声明、高风险确定性建议、用户隐私 fixture 和未经许可的数据/代码分发。

## 临时文件清理
删除候选 clone、构建缓存和原始用户数据；保留 manifest、hash 和脱敏门禁摘要。

## 运行记录登记
任务包必须记录 existence check、候选比较、版本/license、状态迁移、门禁和回滚路径。

## 明确禁止事项
- 禁止先写 provider 再补 contract。
- 禁止为单一实现新增无意义接口层。
- 禁止把“能运行”直接升级为 production。
