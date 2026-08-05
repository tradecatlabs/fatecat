---
id: SOP-EVAL-CORE-HUMAN-REVIEW
type: process
status: current
execution_status: blocked
owner: quality
route_key: intake_core_quality_human_review
route_aliases: ["提交八字紫微专家评审", "录入专业人审证据", "验收外部 benchmark"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 接收核心质量人审证据

## 任务定义
接收外部专家对八字/紫微质量的脱敏评审 bundle，并校验 commit、rubric、artifact hash、no-leak 和接受状态。

## 当前状态
intake gate 和 bundle template 已实现；缺真实专家证据时必须 blocked，仓库不能自动完成。

## 适用场景
专业命理专家复核、外部 benchmark signoff 或 release certification 补证；不用于生成评审结论。

## 输入要求
脱敏 review evidence JSON，包含 reviewer reference、当前 commit、rubric dimensions、artifact hashes、结论和 no-leak attestation。

## 前置条件
生成 template；专家拥有必要权限且独立于实现者；待评 artifact 固定；不得向仓库提供身份密钥。

## 默认工具链
`bash scripts/core-quality-human-review-bundle-template.sh` 和 `bash scripts/core-quality-human-review-gate.sh --require-accepted`。

## 固定路径
Contracts `contracts/fate/evaluations/core-quality-human-review-*.json`；运行输出 `infra/runtime/local-state/exports/core-quality-human-review/`。

## 成熟参数
`--expected-commit` 默认当前 HEAD；最终门禁必须 `--require-accepted`；所有 proof 使用脱敏引用和 sha256。

## 分步执行流程
1. 生成 bundle template 和 rubric checklist。
2. 将待评 artifact hash 与当前 commit 提供给专家。
3. 专家在外部完成评审并返回脱敏 bundle。
4. 执行 intake gate。
5. 通过后把 summary 接入 certification/audit bundle。

## 幂等与增量策略
同一 commit/artifact/reviewer bundle 可重复验证；任一 artifact 或 commit 变化后旧证据 stale。

## 限速与并发规则
按 reviewer 独立收集，可并行评审但不得互相覆盖；最终聚合前逐份验证。

## 输出目录
`infra/runtime/local-state/exports/core-quality-human-review/`；原始专家文件置受控外部存储。

## 命名规范
`core-quality-review-<reviewer-ref>-<short-sha>-<UTC>.json`；不含真实姓名。

## 质量验收门禁
schema、commit/hash 绑定、全部 rubric、accepted、no-leak、时效和签名/身份引用通过。

## 失败处理
缺字段、commit 不匹配、artifact hash 漂移、pending/rejected 或泄露风险均保持 blocked。

## 恢复与重试策略
修正证据包或重新评审；不得编辑专家结论为 accepted；新 commit 必须重新绑定证据。

## 安全边界
不输出 reviewer 私人信息、用户命例、密钥或报告正文；人审不替代医疗法律等专业意见。

## 临时文件清理
删除本地原始 bundle 副本，只保留受控脱敏 summary/hash；失败文件按审计保留策略处理。

## 运行记录登记
登记 reviewer ref、commit、artifact hashes、rubric 状态、gate output hash 和时间。

## 明确禁止事项
- 禁止由自动化伪造专家签字。
- 禁止把 template 当已完成证据。
- 禁止旧 commit 证据复用于新发布。
