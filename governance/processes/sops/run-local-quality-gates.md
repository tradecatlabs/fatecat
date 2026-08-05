---
id: SOP-DEV-LOCAL-QUALITY-GATES
type: process
status: current
owner: quality
route_key: run_local_quality_gates
route_aliases: ["跑本地 CI", "执行 quick gate", "运行完整 acceptance"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行本地质量门禁

## 任务定义
按变更风险选择 quick、full、container、public-service 或 all profile，生成统一可审计 summary。

## 当前状态
成熟本地 CI 总入口；GitHub Quick/Acceptance 复用相同仓库脚本，但本地通过不等于远端通过。

## 适用场景
开发自检、提交前验收、发布前完整门禁或容器/公开服务专项验收。

## 输入要求
profile、可选 output/image/port/api-url/live-bot；需要 dev gate 时传 `--with-dev`。

## 前置条件
worktree 变更已明确；依赖可安装；Docker/外部凭证只在对应 profile 需要。

## 默认工具链
`bash scripts/local-ci.sh --profile quick --with-dev --output <dir>`；高风险使用 `--profile all`。

## 固定路径
入口 `scripts/local-ci.sh`；完整门禁 `scripts/acceptance.sh`；CI workflows `.github/workflows/{quick,acceptance}.yml`。

## 成熟参数
默认 output `/tmp/fatecat-local-ci-<timestamp>`；执行顺序 quick -> full -> container -> public-service；外部 Bot 仅显式 `--require-live-bot`。

## 分步执行流程
1. 检查 Git 状态和变更范围。
2. 选择最低充分 profile。
3. 执行并等待命令结束。
4. 检查 `summary.json`、`summary.txt`、失败 gate 和 artifact。
5. 修复后只重跑受影响门禁，再跑目标 profile 收口。

## 幂等与增量策略
每次使用新 output 目录；未变化的通过证据可在同一 commit 内引用，但最终交付必须有完整目标 profile。

## 限速与并发规则
同一 worktree 不并发运行多个会写 runtime/export 的 profile；容器端口唯一；外部 live 调用串行。

## 输出目录
默认 `/tmp/fatecat-local-ci-*`；需要审计时复制 summary 到受控 release/audit bundle。

## 命名规范
保留脚本默认时间戳；自定义目录 `fatecat-local-ci-<profile>-<short-sha>-<UTC>`。

## 质量验收门禁
进程 exit 0、summary status passed、required gate 全部通过、无 stale/缺失 artifact。

## 失败处理
以首个失败 gate 为根因，不跳过；区分代码失败、依赖缺失、Docker 缺失和外部凭证缺失。

## 恢复与重试策略
结构性失败修复后重跑该 gate；瞬时下载最多有限重试；最终重新执行完整目标 profile。

## 安全边界
不得把 token 写入 output；外部 live 只在授权环境执行；summary 必须脱敏。

## 临时文件清理
保留当前交付证据；删除过期 `/tmp/fatecat-local-ci-*` 和容器；不得清理仍被审计包引用的目录。

## 运行记录登记
记录 commit、profile、命令、开始结束、summary 路径/hash、通过/失败和环境缺口。

## 明确禁止事项
- 禁止没跑过写“已通过”。
- 禁止用 focused test 代替目标 profile。
- 禁止并行 profile 争用同一输出或端口。
