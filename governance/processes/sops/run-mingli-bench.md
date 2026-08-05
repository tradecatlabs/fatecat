---
id: SOP-EVAL-MINGLI-BENCH
type: process
status: current
owner: quality
route_key: run_mingli_bench
route_aliases: ["运行 MingLi-Bench", "生成命理评测 prompts", "评分 predictions"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行 MingLi-Bench

## 任务定义
以离线统计、prompt 导出或 prediction 评分三种模式运行 MingLi-Bench，并只保留脱敏聚合证据。

## 当前状态
可选本地 benchmark；不是默认生产门禁，reference repo 和数据集许可边界受 registry 控制。

## 适用场景
查看题库统计、导出外部评测输入、评分已有预测；不用于普通 pytest 或专家人审。

## 输入要求
可选 `--year`、`--sample`；prompt 模式需 `--prompt-out`；评分模式需 predictions JSON/JSONL。

## 前置条件
reference repo 完整且 vendor health 通过；确认数据集使用许可；预测文件不含密钥或用户隐私。

## 默认工具链
`bash scripts/run-mingli-bench.sh`、`bash scripts/generate-mingli-predictions.sh`、`bash scripts/mingli-bench-gate.sh`。

## 固定路径
Reference repo `tools/reference-repos/github/MingLi-Bench-main/`；聚合 contract 位于 `contracts/fate/evaluations/`。

## 成熟参数
默认 `--stats` 离线且不调用模型；抽样必须显式 `--sample N`；prediction 字段使用文档允许的 ID/answer aliases。

## 分步执行流程
1. 运行 vendor health 和 `--stats`。
2. 需要外部回答时导出 prompts。
3. 在受控外部环境生成 predictions。
4. 本地用 `--predictions-file ... --output-json ...` 评分。
5. 运行 aggregate gate，只提交聚合证据。

## 幂等与增量策略
固定 dataset/version/year/sample 后 prompt 集稳定；predictions 以 question ID 合并，禁止重复 ID 覆盖。

## 限速与并发规则
本地评分串行；外部模型调用不由本脚本执行，必须另行限速、预算和重试。

## 输出目录
`infra/runtime/local-state/exports/evaluations/mingli-bench/` 或 `/tmp/fatecat-mingli-*`。

## 命名规范
`prompts-<year>-<sample>-<dataset-hash>.jsonl`、`predictions-<provider>-<run>.jsonl`、`report-<run>.json`。

## 质量验收门禁
reference hash/license、ID 唯一、coverage、aggregate gate、no-leak 和 prediction schema 均通过。

## 失败处理
缺题、重复 ID、非法答案、license 不清或 reference repo 漂移时 block，不补默认答案。

## 恢复与重试策略
只补缺失 question ID；保留相同 prompt hash；外部失败不重新抽样。

## 安全边界
不得保存题目、出生信息、标准答案或逐题结果到公开证据；模型 token 不进命令或日志。

## 临时文件清理
审计完成后删除 prompts/predictions 原文；保留 aggregate summary、hash 和 license refs。

## 运行记录登记
记录 dataset/reference hash、year/sample、provider、coverage、accuracy 聚合、gate 和 no-leak。

## 明确禁止事项
- 禁止默认调用外部模型。
- 禁止以单次 benchmark 宣称专业能力 100%。
- 禁止公开受限题库或标准答案。
