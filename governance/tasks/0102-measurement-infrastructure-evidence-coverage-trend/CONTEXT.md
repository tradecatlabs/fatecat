# Repo Evidence
- 当前分支：`main`，0101 已提交并推送；0102 worktree 正在实现 evidence coverage trend gate。
- 直接上游计划：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `Wave A A3`。
- 已有证据面：`contracts/fate/rule_depth_registry.json`、`contracts/fate/classics_rule_index.json`、`CapabilityExecutor` 的 `analysisEvidence`，以及 FastAPI Report envelope 的 `evidenceRefs`。
- 已有能力样板：八字和紫微是当前重点 production capability；本任务只做证据覆盖门禁，不改排盘算法。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 只能分析当前 worktree | 不切分支、不合并、不重写历史。 |
| 不能伪造 100% | `status=passed` 只代表本地 coverage 未回退，不代表预测准确率或基础设施 100%。 |
| 外部系统不可本地证明 | 真实 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/多副本 live 均保留为外部连通验证待执行。 |
| 隐私和安全 | gate summary 只保存计数、ratio、字段名、ruleId 和路径，不复制报告正文、出生地区或 secret。 |
| 胶水原则 | 复用现有 `CapabilityExecutor`、FastAPI TestClient、registry 和 classics index，不重写测算逻辑。 |

# Change Boundary
允许修改：
- `contracts/fate/evidence-coverage-baseline.json`
- `contracts/fate/evidence-coverage-trend-contract.json`
- `scripts/evidence-coverage-trend-gate.py`
- `scripts/evidence-coverage-trend-gate.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_evidence_coverage_trend_gate.py`
- 相关 `AGENTS.md`、API 文档、roadmap 和本任务目录

禁止修改：
- 八字/紫微 provider 计算逻辑
- 真实凭证、`.env`、外部账号配置
- 原始报告正文、真实用户数据或生产日志 payload
- 历史任务目录中的业务证据，除非修复明确的任务索引漂移

# Risk Matrix
| Risk | Impact | Control |
| --- | --- | --- |
| coverage pass 被解释成专业能力 100% | 误导产品与审计判断 | contract、baseline 和文档均写明 production boundary。 |
| 规则引用断链未被发现 | evidence 可追溯性失效 | gate 校验 registry rule id 与 sourceRuleIds 必须存在于 classics index。 |
| Report evidenceRefs 不完整但计数达标 | API 层证据摘要回退 | baseline 包含 `minReportEvidenceRefCompletenessRatio=1.0`。 |
| 保存完整报告或真实用户数据 | 隐私事故 | gate 输出只保存摘要，并检查 forbidden fragments。 |
| gate 成本膨胀 | quick CI 变慢 | 每个 capability 只执行一次 engine 输出，一次 API Report envelope 检查。 |

# Assumptions and Falsification
- 假设：八字/紫微当前 production capability 是 evidence coverage trend 的首批范围。
  - 证伪：新增 production capability 纳入 baseline 前，gate 不应默默声明全系统 coverage。
- 假设：规则来源以 `classics_rule_index.json` 为当前可追溯真相源。
  - 证伪：任何 `rule_depth_registry` 引用未登记规则都必须成为 broken ref。
- 假设：coverage baseline 只记录最低门槛。
  - 证伪：合法能力增强应提升 baseline；能力回退不得降低 baseline 来掩盖。

# Critical Ambiguities
- 预测准确率是否提升：本任务不评价，只评价证据覆盖结构。
- 典籍规则是否足够权威：本任务只验证索引存在和字段完整，不替代命理专家审稿。
- 外部生产连通是否完成：本任务不解决，统一标记外部连通验证待执行。

# Debug Evidence Contract
- 调试模式: Optional
- 当前任务是新增门禁，不是已复现缺陷修复；若 regression、local-ci 或 secret scan 失败，再升级为 Required 并维护 DEBUG.md。

# Task Package Context Map
## TP-01 evidence coverage 需求和 baseline 边界
聚焦 0099 Wave A A3，把 “evidence coverage trend” 限定为本地结构化证据门禁，不直接连外部系统。

### TP-01.01 盘点八字/紫微现有 evidence surface
读取 rule depth registry、classics index、CapabilityExecutor 输出和 API Report envelope，确认可统计字段。

### TP-01.02 定义 tracked baseline、contract 和隐私边界
新增 baseline 和 contract，列出 required evidence items、ratio、forbidden fragments、privacy boundary 和 production boundary。

## TP-02 evidence coverage gate 实现与接线
聚焦最小实现：读取 JSON、执行固定北京测试样本、统计 coverage，不复制完整报告。

### TP-02.01 实现 CLI/wrapper、coverage metrics 和趋势比较
实现 Python CLI 与 shell wrapper；引用断链、字段不完整或 baseline 回退均输出 failed。

### TP-02.02 接入 local-ci summary、AGENTS、API 文档和 roadmap
把 gate 加入 quick local-ci，summary 输出 artifact 路径，并更新目录级架构说明和用户可复核命令。

## TP-03 验证与审查
覆盖正负路径，确保 gate 不泄漏敏感数据、不伪造通过。

### TP-03.01 增加 regression tests
测试 contract、当前 baseline pass、严格 baseline fail、规则引用断链 fail 和 CLI 输出。

### TP-03.02 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan
以真实命令输出作为 closeout 证据。

## TP-04 closeout 与版本控制
把任务状态、索引、验证证据和远端提交状态收口。

### TP-04.01 同步任务文档、INDEX 和验收清单
任务文档必须通过 decompose/closeout validator。

### TP-04.02 提交、推送并记录远端状态
按 auto-github 执行 commit/push，并明确远端 CI 是否覆盖当前 commit。
