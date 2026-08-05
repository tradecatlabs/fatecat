---
id: SOP-EVAL-REGISTRY-RUN
type: process
status: current
owner: quality
route_key: run_evaluation_registry
route_aliases: ["运行评测", "执行 EvaluationRun", "更新评测历史"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行统一评测注册表

## 任务定义
从 EvaluationRun registry 选择白名单评测，执行、记录 summary/history 并按 diff policy 判断回归。

## 当前状态
本地 runner、历史留痕、diff 和 nightly workflow 可用；外部 reference repo 评测默认不执行。

## 适用场景
运行单项/全部本地评测、发布前 required 评测或质量趋势留痕。

## 输入要求
一个或多个 `run-id`，或 `--all-local-required`；可选 history/output/timeout；reference repo 需显式授权。

## 前置条件
bootstrap 完成；registry 有效；输出目录可写；预计长任务有足够时间。

## 默认工具链
`bash scripts/run-evaluations.sh`、`bash scripts/compare-evaluations.sh`、evaluation trend gate。

## 固定路径
Registry `contracts/fate/evaluations/registry.json`；默认 summary/history 位于 `infra/runtime/local-state/exports/evaluations/`。

## 成熟参数
单命令 timeout 900 秒；先 `--dry-run`；发布执行 `--all-local-required --record-history`；reference repo 仅显式 `--allow-reference-repo`。

## 分步执行流程
1. `--list` 确认 run ID。
2. `--dry-run` 验证选择和命令白名单。
3. 实际运行并写独立 output JSON。
4. 需要趋势时 `--record-history`。
5. 与 baseline 比较并运行 trend gate。

## 幂等与增量策略
run 结果按 commit/registry/command 绑定；history 追加时间戳记录，`latest.json` 只由成功记录更新。

## 限速与并发规则
runner 按登记顺序执行，禁止自行并行昂贵评测；nightly 由 GitHub concurrency/timeout 管理。

## 输出目录
`infra/runtime/local-state/exports/evaluations/` 或 `/tmp/fatecat-evaluation-*`。

## 命名规范
`evaluation-<run-id>-<UTC>-<short-sha>.json`；history 使用 runner 生成时间戳。

## 质量验收门禁
summary status passed、全部 required command exit 0、无超时、history hash 可读、diff policy 未回归。

## 失败处理
首个失败 run 记录 stdout/stderr tail 和 timeout；不得把 partial success 写成整体通过。

## 恢复与重试策略
只重跑失败 run ID；输入/registry 未变时可复用通过证据，变化后全部相关证据 stale。

## 安全边界
命令必须在 registry 白名单；不得拼接 shell；summary 不保存题目、出生数据或完整报告。

## 临时文件清理
保留正式 history；删除 dry-run 和失败临时目录；不要删除用于当前审计的 summary。

## 运行记录登记
记录 commit、registry hash、run IDs、commands、duration、exit、output hash 和 diff。

## 明确禁止事项
- 禁止绕过命令白名单。
- 禁止把 dry-run 标记为 passed。
- 禁止用本地评测代替外部专家或生产 live。
