---
id: SOP-DIST-SKILL-EXPORT
type: process
status: current
owner: developer-platform
route_key: export_skill_runtime
route_aliases: ["导出 FateCat Skill", "生成 lite skill", "生成 full skill"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 导出 Skill Runtime

## 任务定义
从企业仓库生成可独立安装的 FateCat skill runtime，并验证导出卫生和独立 smoke。

## 当前状态
full/lite 导出和卫生门禁成熟；导出包不等于已发布到外部 skill marketplace。

## 适用场景
本地 skill 分发、安装测试、发布候选或审计导出。

## 输入要求
输出目录或 output parent；模式 `full|lite`；目标目录必须专用且可清理。

## 前置条件
bootstrap/quick gate 通过；worktree 变更明确；无 raw、runtime、secret 或用户报告混入。

## 默认工具链
`bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite`、`check-export-hygiene.sh` 和 strict skill smoke。

## 固定路径
入口 `scripts/export-runtime.sh`；源 `SKILL.md`、contracts、domains、infra 必需文件；输出 `<parent>/fatecat`。

## 成熟参数
默认用户分发使用 `lite`；需要 lifecycle/packs 历史时才用 `full`；禁止输出到仓库根。

## 分步执行流程
1. 清理专用临时 parent。
2. 执行导出。
3. 运行 export hygiene。
4. 在导出目录 bootstrap/strict validate/smoke。
5. 生成文件列表和 aggregate hash。

## 幂等与增量策略
导出为全量重建；同一 commit/mode 应相同；不在旧包上增量覆盖。

## 限速与并发规则
单进程导出；不同 mode 使用不同 parent，可并行但不得共享输出。

## 输出目录
`/tmp/fatecat-export/fatecat` 或 `infra/runtime/local-state/exports/distributions/skill/<mode>/fatecat`。

## 命名规范
归档 `fatecat-skill-<mode>-<short-sha>.tar.gz`；内部根目录固定 `fatecat/`。

## 质量验收门禁
source/export hygiene、strict skill、lite independent smoke、文件 hash、无 raw/vendor runtime leak。

## 失败处理
缺文件、绝对路径、缓存、raw、secret 或 smoke 失败时删除候选并 block。

## 恢复与重试策略
修复源/导出清单后从空目录重建；禁止在失败包上补文件。

## 安全边界
不包含 `.env`、数据库、日志、用户报告、raw 典籍/抓取数据或凭证。

## 临时文件清理
验收后删除解压/venv/cache；保留最终候选和 hash。

## 运行记录登记
记录 commit、mode、文件数、大小、aggregate hash、gate 和输出路径。

## 明确禁止事项
- 禁止直接复制整个 monorepo。
- 禁止增量修补旧导出包。
- 禁止把导出成功写成 marketplace 已发布。
