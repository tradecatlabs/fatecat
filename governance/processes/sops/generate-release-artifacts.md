---
id: SOP-REL-ARTIFACTS-GENERATE
type: process
status: current
owner: platform
route_key: generate_release_artifacts
route_aliases: ["生成 SBOM", "生成 provenance", "制作发布证据"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 生成发布制品证据

## 任务定义
为当前 commit 生成并验证 SBOM、provenance、manifest 和发布摘要，作为容器/发布证据的一部分。

## 当前状态
本地 artifact generator/validator 成熟；registry digest 和 GitHub attestation 由真实容器发布流程产生。

## 适用场景
容器发布、current release proof、第三方审计或交付归档。

## 输入要求
输出目录、可选 summary JSON；验证已有 artifact 时使用 `--verify-dir`。

## 前置条件
worktree clean；目标 commit 已通过门禁；输出目录专用；依赖 lock 可读。

## 默认工具链
`bash scripts/release-artifacts.sh --output-dir <dir> --summary-json <file>`。

## 固定路径
`scripts/release-artifacts.py`、requirements locks、container/release contracts、runtime exports。

## 成熟参数
默认输出 `infra/runtime/local-state/release-artifacts`；正式任务使用 commit 专属目录；验证使用同一脚本 `--verify-dir`。

## 分步执行流程
1. 检查 Git clean/HEAD。
2. 在空目录生成 artifacts。
3. 使用 verify-dir 验证自身。
4. 计算目录 hash并绑定 commit。
5. 供 current release/live gate 消费。

## 幂等与增量策略
制品内容绑定 commit和生成时间；同一发布不在原目录覆盖，使用新目录并保留旧证据。

## 限速与并发规则
同一输出目录单进程；可并行生成不同 commit，但最终发布只选一个。

## 输出目录
`infra/runtime/local-state/exports/releases/<short-sha>/artifacts/`。

## 命名规范
保留脚本固定文件名；目录 `<short-sha>-<UTC>`；summary `release-artifacts-summary.json`。

## 质量验收门禁
manifest、SBOM、provenance schema/hash、自验证和 current release proof；外部 digest/attestation 必须另附。

## 失败处理
Git dirty、依赖解析、hash或 schema 失败时删除候选并 block。

## 恢复与重试策略
修复源码/lock 后新目录重建；不得手改 artifact 内容。

## 安全边界
不包含 secret、env、用户数据；生成器不伪造 registry signature或生产部署。

## 临时文件清理
删除失败目录；保留当前 release artifacts 和被审计引用的历史版本。

## 运行记录登记
记录 commit、生成时间、artifact hashes、generator version、verify 和外部缺口。

## 明确禁止事项
- 禁止 dirty worktree 生成最终证据。
- 禁止手工编辑 SBOM/provenance。
- 禁止本地产物冒充 registry attestation。
