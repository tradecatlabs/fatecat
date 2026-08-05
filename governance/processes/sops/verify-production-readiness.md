---
id: SOP-OPS-PRODUCTION-READINESS
type: process
status: current
owner: sre
route_key: verify_production_readiness
route_aliases: ["执行生产就绪检查", "验证公网 API", "运行 live release gate"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 验证生产就绪与 Live Release

## 任务定义
聚合本地发布门禁、真实 API/HF/Bot、GitHub run、容器 digest、SBOM、provenance 和回滚证据，判定当前 commit 的 live release 状态。

## 当前状态
静态和证据 gate 已实现；缺任一真实外部证据时必须 pending/blocked，不能在仓库内伪造。

## 适用场景
公开发布、生产变更、HF Space 更新后的最终验收。

## 输入要求
真实 API/HF URL、当前 GitHub run URL/SHA、container digest/evidence、SBOM、provenance、rollback、local-ci summary；可选真实 Bot token。

## 前置条件
worktree clean；Quick/full/container/public gates 通过；外部权限和凭证已授权；所有证据绑定同一 commit。

## 默认工具链
`bash scripts/production-readiness.sh --api-url <url>` 和 `bash scripts/live-release-gate.sh --require-live --require-clean-worktree ...`。

## 固定路径
`contracts/fate/delivery/release-gate.json`、production security policy、release scripts、`infra/runtime/local-state/exports/`。

## 成熟参数
live gate 单请求 timeout 默认 8 秒；Bot 仅显式 `--run-live-bot`；生产 readiness 不传凭证时不会假通过。

## 分步执行流程
1. 运行 local-ci/public-service/container 门禁。
2. 生成 release artifacts 和 rollback evidence。
3. 获取当前 commit 的 GitHub run、registry digest/attestation。
4. 验证真实 API/HF，授权时验证 Bot。
5. 执行 live-release gate并检查每项 evidence。

## 幂等与增量策略
每个证据绑定 commit/hash；任何代码、镜像或部署变化使旧证据 stale，必须只补变化项后重新聚合。

## 限速与并发规则
外部 probe 串行且短超时；同一发布只允许一个 operator；不得并发部署与最终验收。

## 输出目录
`infra/runtime/local-state/exports/live-release/<short-sha>/`。

## 命名规范
`live-release-gate-<short-sha>-<UTC>.json`；proof ref 使用脱敏 HTTPS/artifact handle。

## 质量验收门禁
所有 required evidence passed/current/same commit，worktree clean，无 pending external validation。

## 失败处理
明确区分本地失败、证据缺失、外部不可达、commit 漂移和凭证缺失；任一 required 项失败即 block。

## 恢复与重试策略
外部瞬时失败有限重试；commit/配置失败生成新证据；不得编辑 gate JSON。

## 安全边界
token、DSN、URL secret、报告正文不进证据；真实生产请求必须最小、只读或可回收。

## 临时文件清理
删除 probe 临时响应；保留当前 release evidence；过期 evidence 按 retention 归档。

## 运行记录登记
记录 operator、commit、deployment、URLs（无 secret）、artifact hashes、gate、时间和 rollback target。

## 明确禁止事项
- 禁止本地通过写成生产通过。
- 禁止跨 commit 拼证据。
- 禁止缺外部权限时使用模拟数据解锁。
