---
id: SOP-REL-RUNTIME-CLEAN
type: process
status: current
owner: engineering
route_key: clean_runtime_artifacts
route_aliases: ["清理运行缓存", "整理仓库卫生", "删除临时导出"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 清理运行态与仓库卫生

## 任务定义
预览并清理缓存、临时导出、编辑器历史和运行态产物，同时验证 tracked source/导出包卫生。

## 当前状态
`clean-runtime.sh`、source/export hygiene 和 ignore 规则成熟；不负责 retention 数据删除。

## 适用场景
交付前仓库整理、构建污染清理、导出包复核或本地环境重建。

## 输入要求
默认 dry-run；可选 `--venv` 做彻底环境重建；明确保留的审计/发布 artifact 列表。

## 前置条件
先运行 `git status --short --branch`；识别用户未提交改动、人工知识资产和仍被引用证据。

## 默认工具链
`bash scripts/clean-runtime.sh --dry-run`，确认后执行；随后 source/export hygiene 和 Git 状态检查。

## 固定路径
`infra/runtime/local-state/`、`/tmp/fatecat-*`、`.gitignore`、source/export hygiene scripts。

## 成熟参数
默认不删除 runtime `.venv`；只有显式 `--venv` 才重建环境；禁止使用 `git clean -fdx`。

## 分步执行流程
1. 记录 Git 状态和受保护资产。
2. 执行 clean dry-run。
3. 逐项确认不会删除 evidence/canonical/用户改动。
4. 执行清理。
5. 运行 source hygiene、export hygiene和 Git 状态复核。

## 幂等与增量策略
重复清理应无额外变化；每次只删除当前工具登记的 runtime，新增路径先更新 contract/test。

## 限速与并发规则
清理期间停止相关服务、构建和测试；不得与 crawler/dataset/CI 并发。

## 输出目录
清理日志写 `/tmp/fatecat-clean-runtime-<UTC>.txt`；不生成新的 tracked 产物。

## 命名规范
临时目录统一 `/tmp/fatecat-*`；runtime 只在 `infra/runtime/local-state/`。

## 质量验收门禁
dry-run 审核、source/export hygiene PASS、Git 无意外删除、canonical/任务/证据 intact。

## 失败处理
发现未提交/受保护文件立即停止；误删风险不使用自动恢复覆盖用户改动。

## 恢复与重试策略
tracked 文件从 Git 恢复需用户明确授权；ignored artifact 从来源重建；不猜测恢复。

## 安全边界
不删除用户数据、canonical、凭证存储、数据库或审计证据，除非对应专用 SOP 和授权。

## 临时文件清理
本任务本身产生的清理日志可在确认后删除；保留异常清单用于复核。

## 运行记录登记
记录 dry-run清单、确认人、删除路径类别、前后 Git 状态和 hygiene结果。

## 明确禁止事项
- 禁止 `git reset --hard`、`git clean -fdx`。
- 禁止清理未识别的用户改动。
- 禁止把 retention 删除混入仓库卫生。
