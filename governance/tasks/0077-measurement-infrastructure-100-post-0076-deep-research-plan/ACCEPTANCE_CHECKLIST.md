# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：planning-only，不实现业务代码。
- [x] 证据来源明确：仓库事实、任务索引、主路线图、外部一手资料。
- [x] 外部验证项明确标记，不伪造完成。
- [x] 0076 public webhook live smoke gate 未被夸大为 live passed、production ready 或 exactly-once。
- [x] 后续任务能按执行队列逐个创建和验证。
- [x] 任务文档无模板占位符。

# Task Package Checklists

## TP-01 复核仓库事实和任务现状

Verify: Git/worktree、0076 任务状态和主路线图已读取。

Gate: 0076 不被写成 live passed 或 production ready。

- [x] TP-01.01 Git/worktree 与 0076 closeout 事实已记录。
- [x] TP-01.02 既有 roadmap、requirements、runtime backend contract 已复核。

## TP-01.01 Git/worktree 与 0076 事实复核

Verify: `git status --short --branch` 和 0076 `STATUS.md` 已读取。

Gate: 当前事实边界写清，且不回滚或覆盖用户/历史改动。

- [x] 当前 worktree 状态已记录。
- [x] 0076 仅作为 public webhook live smoke gate 记录。

## TP-01.02 既有计划和契约复核

Verify: 主路线图和 `contracts/fate/delivery/runtime-backends.json` 已读取。

Gate: 0.10 是追加最新章节，不删除历史证据。

- [x] 既有 0.9、runtime backend production 缺口已复核。
- [x] 0078+ 后续任务不与已有任务冲突。

## TP-02 外部基础设施同构调研

Verify: `RESEARCH.md` source matrix。

Gate: 来源是一手资料或官方资料链接。

- [x] TP-02.01 API、event、workflow、control plane、observability、security、supply chain、platform engineering 资料已列出。
- [x] TP-02.02 外部范式到 FateCat 的同构映射已写入。

## TP-02.01 外部一手资料调研

Verify: `RESEARCH.md` Source Matrix 包含官方资料链接。

Gate: 不使用二手总结替代关键技术依据。

- [x] API、事件、控制面、持久工作流、可观测、安全、供应链、平台工程资料已列出。

## TP-02.02 FateCat 同构能力抽象

Verify: `RESEARCH.md` Synthesis。

Gate: 每个成熟领域都映射到 FateCat 资源域、gate 或后续任务。

- [x] Capability、Provider、Job、Event、Evaluation、Security、Release、Audit 等资源域已归纳。

## TP-03 形成完整实现计划

Verify: 主路线图 `0.10`。

Gate: 任务树、执行顺序、外部阻断项和失败判定完整。

- [x] TP-03.01 100% 完成门禁和失败判定已落盘。
- [x] TP-03.02 MI-100 后续任务树和执行顺序已落盘。
- [x] TP-03.03 本地可执行任务和外部连通验证待执行任务已区分。

## TP-03.01 100% 完成门禁和失败判定

Verify: 主路线图 `0.10.5` 与 `0.10.6`。

Gate: 不能把 dry-run、local smoke、allow-missing 或 contract 写成 live passed。

- [x] 完成门禁已写明。
- [x] 失败判定已写明。

## TP-03.02 MI-100 任务树和执行顺序

Verify: 主路线图 `0.10.3`。

Gate: 下一步能直接创建 0078+ 任务。

- [x] 0078-0087 建议队列已写明。
- [x] 外部凭证可插队的条件已写明。

## TP-03.03 外部阻断项分层

Verify: `RESEARCH.md` External Validation Pending。

Gate: 所有真实外部平台都标记 `外部连通验证待执行`。

- [x] Bot live、public webhook、Vault/KMS、OIDC、SIEM、OTel、长期多副本、exactly-once 边界已列出。

## TP-04 落盘和校验

Verify: 主路线图、0077 文档和 validator。

Gate: 文档无占位符且任务节点可识别。

- [x] TP-04.01 主路线图已追加 0.10 最新计划。
- [x] TP-04.02 0077 任务文档和 `RESEARCH.md` 已回填。
- [x] TP-04.03 validator 和占位符检查已通过。

## TP-04.01 主路线图更新

Verify: `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 包含 `0.10`。

Gate: 不创建第二份 roadmap。

- [x] 0.10 最新执行计划已追加。

## TP-04.02 任务文档和 RESEARCH 回填

Verify: `rg "\\{\\{" governance/tasks/0077-measurement-infrastructure-100-post-0076-deep-research-plan` 无结果。

Gate: README/CONTEXT/PLAN/ACCEPTANCE/CHECKLIST/TODO/STATUS/RESEARCH 均可读。

- [x] 任务文档已回填。
- [x] `RESEARCH.md` 已新增。

## TP-04.03 文档校验

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0077-measurement-infrastructure-100-post-0076-deep-research-plan --phase decompose`。

Gate: validator exit 0。

- [x] 单任务文档校验通过。
