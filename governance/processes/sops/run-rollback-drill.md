---
id: SOP-REL-ROLLBACK-DRILL
type: process
status: current
owner: sre
route_key: run_rollback_drill
route_aliases: ["执行回滚演练", "生成 rollback evidence", "验证回退路径"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 执行回滚演练

## 任务定义
基于当前 release artifacts、本地 CI 和 public release summary 生成可审计的回滚演练证据。

## 当前状态
本地 dry-run evidence 生成器成熟；不执行真实生产回滚。

## 适用场景
发布前回退路径验证、审计交接或 release proof。

## 输入要求
必填 output JSON；可选 release artifacts dir、local-ci summary、public-release summary。

## 前置条件
候选发布和上一已验证版本明确；部署/数据兼容和恢复步骤已文档化。

## 默认工具链
`bash scripts/rollback-drill.sh --output-json <file> --release-artifacts-dir <dir> ...`。

## 固定路径
`scripts/rollback-drill.py`、release artifacts、deployment docs、current release contracts。

## 成熟参数
脚本内部命令 timeout 15 秒；所有输入可选但最终 release gate 应提供完整证据。

## 分步执行流程
1. 记录当前/回退 commit和 artifact。
2. 生成本地 rollback evidence。
3. 检查 required docs/scripts、artifact/hash 和步骤。
4. 验证回退后 health/smoke 命令可执行。
5. 将证据接入 current/live release gate。

## 幂等与增量策略
同一 current/target/artifact 可重复生成；任一版本或部署变化使旧证据 stale。

## 限速与并发规则
演练单 operator；不与真实部署并发；外部回滚需独立维护窗口。

## 输出目录
`infra/runtime/local-state/exports/releases/<short-sha>/rollback/`。

## 命名规范
`rollback-drill-<current>-to-<target>-<UTC>.json`。

## 质量验收门禁
目标可获得、步骤完整、artifacts/CI/public summary有效、健康验证和数据边界明确。

## 失败处理
目标缺失、迁移不可逆、证据 stale 或验证命令不存在时 block 发布。

## 恢复与重试策略
修正文档/artifact 后重生成；真实回滚失败遵循 incident流程，不重复破坏性动作。

## 安全边界
本地 evidence 不执行生产副作用；真实回滚必须授权、备份和变更窗口。

## 临时文件清理
删除临时 workdir；保留 rollback evidence和目标 artifact。

## 运行记录登记
记录 current/target、operator、artifact hashes、步骤、验证和未演练外部项。

## 明确禁止事项
- 禁止把 dry-run 写成生产回滚已执行。
- 禁止无目标版本/备份发布。
- 禁止使用 `git reset --hard` 代替部署回滚。
