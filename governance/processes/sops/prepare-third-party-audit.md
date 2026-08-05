---
id: SOP-REL-THIRD-PARTY-AUDIT
type: process
status: current
owner: governance
route_key: prepare_third_party_audit
route_aliases: ["生成审计交接包", "制作 current audit bundle", "第三方审计预演"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 准备第三方审计交接

## 任务定义
从当前 commit 聚合 Git、contracts、任务、local-ci、release、rollback 和 pending external validations，生成交接包并执行审计预演。

## 当前状态
handoff、dry-run、current audit bundle 和 rehearsal 工具成熟；不替代独立审计人员的最终意见。

## 适用场景
第三方工程审计、发布交接、合规复核或接手工程师评估。

## 输入要求
当前 clean worktree、local-ci summary、release proof/artifacts、rollback、可选 GitHub 查询。

## 前置条件
目标 commit 固定；本地门禁完成；外部 pending 如实保留；无敏感值进入 tracked evidence。

## 默认工具链
依次 `audit-handoff.sh`、`audit-handoff-dry-run.sh`、`current-audit-bundle.sh`、`third-party-audit-rehearsal.sh`。

## 固定路径
相关 `scripts/*audit*`、`contracts/fate/audit/`、`governance/tasks/INDEX.md`、runtime exports。

## 成熟参数
handoff 可 `--include-github`；current bundle 最终交付使用 `--require-current-release`；输出目录按 commit 隔离。

## 分步执行流程
1. 固定 HEAD/Git 状态并运行 local gates。
2. 生成 handoff Markdown/JSON。
3. 执行 handoff dry-run verifier。
4. 生成 current audit bundle/evidence index/risk register/pending list。
5. 生成第三方 rehearsal 包并人工检查。

## 幂等与增量策略
包绑定 current commit；代码/任务/证据变化后重新生成，不增量编辑旧 JSON。

## 限速与并发规则
生成器本地串行；GitHub 查询少量、只读；不并发修改任务/证据目录。

## 输出目录
`infra/runtime/local-state/exports/audit/<short-sha>/`。

## 命名规范
使用工具固定 `AUDIT_HANDOFF.md`、JSON、evidence-index、risk-register 和 pending 文件。

## 质量验收门禁
handoff dry-run、current release绑定、敏感赋值防护、pending扫描、risk/non-claim和 rehearsal 全通过。

## 失败处理
Git dirty、commit 漂移、证据缺失、敏感值或过度声明时 block，不删除 pending。

## 恢复与重试策略
补齐真实证据后从 handoff 重新生成；不得手改聚合包让 gate 通过。

## 安全边界
只输出脱敏路径/hash/ref；第三方身份和凭证不进入仓库；external pending 明确保留。

## 临时文件清理
删除中间临时包；保留最终交接包和其输入证据；过期包归档。

## 运行记录登记
记录 commit、generator versions、输入 hashes、GitHub run、gate、pending和交付对象。

## 明确禁止事项
- 禁止把预演当第三方审计。
- 禁止隐瞒 pending external validation。
- 禁止跨 commit 拼接审计证据。
