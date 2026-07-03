# Repo Evidence
- 当前分支：`main`，0102 已提交并推送，HEAD 为 `d64140d` 起的后续工作。
- 直接上游计划：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `Wave A A4`。
- 已有 current audit bundle：`scripts/current-audit-bundle.py` 可聚合 audit handoff、dry-run、release proof、release artifacts、rollback drill 和 pending external validations。
- 新增缺口：0102 已产生 `evidence-coverage-trend-gate.json`，但 current audit bundle evidence index 尚未显式展开这类 local-ci gate artifact。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 当前 worktree | 不切分支、不合并、不重写历史。 |
| 不伪造审计 | local mode 可生成 blocked bundle；`auditGate=passed` 仍只允许 required evidence 全部通过时出现。 |
| 外部系统不可本地证明 | 真实 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/多副本 live 均保留为外部连通验证待执行。 |
| 隐私和安全 | bundle 只保存 gate 摘要、计数、路径、digest 和 pending 列表，不复制报告正文或凭证。 |
| 胶水原则 | 复用现有 current-audit-bundle、local-ci、evidence coverage gate，不新增审计系统。 |

# Change Boundary
允许修改：
- `scripts/current-audit-bundle.py`
- `scripts/local-ci.sh`
- `tests/regression/test_current_audit_bundle.py`
- `contracts/fate/audit/current-bundle.json`
- 相关 `AGENTS.md`、roadmap 和本任务目录

禁止修改：
- 八字/紫微 provider 计算逻辑
- release/audit/rollback 既有 gate 通过语义
- 真实凭证、`.env`、外部账号配置
- 运行态 audit bundle 输出进入 Git

# Risk Matrix
| Risk | Impact | Control |
| --- | --- | --- |
| 把 local-ci artifact 当成外部 live | 误导审计结论 | evidence item type 为 `quality_gate`，non-claim 保持外部 live pending。 |
| local-ci output dir 缺 artifact | 审计包遗漏关键证据 | local-ci 调用传入 output dir；缺文件时该 evidence item fail。 |
| 审计包输出敏感信息 | 安全事故 | 继续复用 forbidden marker scanner，只输出 gate summary。 |
| 任务只刷新文档不刷新证据 | A4 目标不成立 | regression 必须断言 evidence index 出现 `evidence.evidence_coverage_trend_gate`。 |

# Debug Evidence Contract
- 调试模式: Optional
- 当前任务是审计包增强，不是已复现缺陷修复；若 current bundle 或 tests 失败，再升级为 Required 并维护 DEBUG.md。

# Assumptions and Falsification
- 假设：local-ci output dir 是 current audit bundle 展开 gate artifact 的唯一新增输入。
  - 证伪：若某 gate artifact 不在该目录，current bundle 必须输出 missing/fail，而不是脑补。
- 假设：0102 evidence coverage trend gate 是 A4 首个必须展开的 local-ci gate artifact。
  - 证伪：如果新增 production quality gate 需要审计复核，应后续扩展 artifact list，不在本任务塞完整 local-ci summary。
- 假设：current audit bundle local mode 可以 blocked。
  - 证伪：只有 required 模式且所有当前发布证据真实通过时，才允许 `auditGate=passed`。

# Critical Ambiguities
- 第三方审计是否完成：未完成；本任务只生成更可复核的审计包。
- 外部 live 是否完成：未完成；仍由 Wave B 任务提供独立证据。
- 所有 local-ci gate 是否都要展开：本任务先展开 evidence coverage trend，后续可按审计价值逐个纳入。

# Task Package Context Map
## TP-01 current audit bundle 需求和证据边界
确认 current audit bundle 当前输入和 A4 的新增证据边界。

### TP-01.01 盘点当前 bundle 输入和 0102 evidence artifact 缺口
读取 current bundle、local-ci 和 0102 evidence coverage artifact 接线，确认 evidence index 缺口。

### TP-01.02 定义 local-ci gate artifact 纳入策略和 non-claim
只纳入摘要、路径和 digest，不纳入报告正文或外部 live 声明。

## TP-02 current audit bundle 刷新实现与接线
实现 `--local-ci-output-dir`，并让 local-ci 调用 current bundle 时传入 output dir。

### TP-02.01 实现 local-ci output dir artifact evidence
把 evidence coverage trend gate summary 变成 `EvidenceItem`。

### TP-02.02 接入 local-ci、contract、AGENTS、tests 和 roadmap
同步 contract、目录说明、测试和任务索引。

## TP-03 验证与审查
验证 current bundle 可生成、evidence index 可追踪、原 required/local 语义不回退。

### TP-03.01 增加/更新 regression tests
覆盖 evidence index 包含 `evidence.evidence_coverage_trend_gate`。

### TP-03.02 执行 focused tests、bundle generation、ruff、secret scan 和必要 local-ci
以真实命令输出作为 closeout 证据。

## TP-04 closeout 与版本控制
收口任务状态、验证证据、commit/push 和远端状态。

### TP-04.01 同步任务文档、INDEX 和验收清单
任务文档必须通过 closeout validator。

### TP-04.02 提交、推送并记录远端状态
按 auto-github 执行 commit/push，并明确远端 CI 是否覆盖当前 commit。
