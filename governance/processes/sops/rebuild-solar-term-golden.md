---
id: SOP-DATA-SOLAR-TERM-GOLDEN
type: process
status: current
execution_status: blocked
owner: fate-analysis
route_key: rebuild_solar_term_golden
route_aliases: ["更新节气 golden", "重建交节回归", "校验月令边界"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 重建节气 Golden

## 任务定义
验证或受控更新 1900-2030 节气 fixture，锁定节气时刻、月令、立春年界、真太阳时入口和起运边界。

## 当前状态
现有 fixture 与回归为 production gate；当前仓库没有 active canonical 生成器，旧生成器仅在 archive，因此“验证”可执行，“重建”在生成器晋升前 blocked。

## 适用场景
历法依赖升级、外部交节表变更或边界 mismatch 调查；不用于修改生产天文算法本体。

## 输入要求
来源文件必须与 `source_manifest.tsv` 的名称、hash、时区和许可一致；每个新增边界包含 source、expected、tolerance、failureExplanation。

## 前置条件
取得已登记 raw；确认时区/DST 口径；批准数据变更任务；不得从私有 raw 路径直接发布。

## 默认工具链
`bash scripts/run-evaluations.sh --run-id run.solar_terms_golden`、pytest calendar oracle/golden；archive 生成器只作历史参考，不直接执行。

## 固定路径
`domains/fate-analysis/data-products/calendar/solar_terms/source_manifest.tsv`、`golden/solar_terms_1900_2030.json`、`tests/regression/test_solar_terms_golden.py`。

## 成熟参数
现有全量容差为 3660 秒；硬边界样本按各 fixture 声明；EvaluationRun 单命令超时默认 900 秒。

## 分步执行流程
1. 先执行现有 EvaluationRun，记录基线。
2. 校验 raw hash、时区和来源许可。
3. 若需要重建，先将历史生成逻辑迁入 active owner 路径并补生成器测试；未完成时停止。
4. 在独立临时目录生成候选 fixture，比较结构、数量、hash 和边界差异。
5. 人工复核 mismatch 后替换 canonical fixture并跑完整历法门禁。

## 幂等与增量策略
相同 raw/hash/生成器版本必须产生相同 JSON；只增加或修正有证据的边界，不静默重写全表。

## 限速与并发规则
生成单进程执行；oracle 对照可由 pytest 管理，不并行写同一 fixture。

## 输出目录
候选写 `/tmp/fatecat-solar-terms-golden/`；批准后唯一 tracked 输出是 canonical golden JSON。

## 命名规范
fixture 固定 `solar_terms_1900_2030.json`；候选摘要 `solar-terms-diff-<UTC>-<short-sha>.json`。

## 质量验收门禁
solar terms golden、calendar oracle、bazi coverage matrix、data supply-chain 和 Quick CI 全部 PASS；生成器和 raw hash 可复现。

## 失败处理
hash、时区、条目数、容差或 mismatch 解释不一致立即 block，不更新 fixture。

## 恢复与重试策略
保留旧 tracked fixture；修复生成器或来源后从原 raw 重跑，不手改候选 JSON。

## 安全边界
raw 可能受分发限制，不进入 Git/导出包；不得把 oracle 当生产计算依赖。

## 临时文件清理
删除 raw 临时副本和 `/tmp/fatecat-solar-terms-golden/`；保留脱敏 diff/hash。

## 运行记录登记
记录 source hash、生成器 commit、时区、条目数、diff、容差、测试结果和人工复核人。

## 明确禁止事项
- 禁止直接执行 archive 脚本作为生产流程。
- 禁止用 lunar-python 自身生成 expected 再证明自身正确。
- 禁止无来源修改 golden。
