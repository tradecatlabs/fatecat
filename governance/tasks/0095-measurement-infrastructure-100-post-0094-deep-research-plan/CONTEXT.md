# Repo Evidence
- `git status --short --branch`：任务开始前为 `## main...origin/main`，创建 0095 后仅任务文档与 `INDEX.md` 变更。
- `git rev-parse HEAD`：`e34418ca01dbae2f01a81a0c9bf3fc32e5615ef5`。
- `git log -1 --oneline`：`e34418c feat: add CLI skill semantic evidence gate`。
- `governance/tasks/0093-measurement-infrastructure-cli-capability-command-baseline/STATUS.md`：0093 已完成 CLI capability command baseline。
- `governance/tasks/0094-measurement-infrastructure-cli-skill-semantic-diff-expansion/STATUS.md`：0094 已完成 CLI/Skill semantic evidence baseline。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`：主路线图真相源，本任务只追加 post-0094 计划。
- `contracts/fate/evaluations/core-quality-corpus.json`、`report-diff-policy.json`、`mingli-bench-gate.json`：核心质量下一阶段复用对象。

# Constraints Matrix
| 约束 | 决策 |
| --- | --- |
| 当前任务是计划刷新 | 不修改业务代码、不新增 runtime 行为。 |
| 文档驱动 | 主路线图是长期真相源，任务目录保存本次调研证据。 |
| 不伪造外部证据 | 所有真实 Bot/API/OIDC/SIEM/OTel/Vault/KMS/multi-replica 项继续标注外部连通验证待执行。 |
| 隐私治理 | 计划不引入真实用户样本、非北京示例地区或完整报告正文。 |

# Change Boundary
- 更新 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 新增并回填 `governance/tasks/0095-measurement-infrastructure-100-post-0094-deep-research-plan/`。
- 更新 `governance/tasks/INDEX.md` 中 0095 状态。
- 不改 `domains/`、`scripts/`、`contracts/` 的生产行为。

# Risk Matrix
| 风险 | 缓解 |
| --- | --- |
| 与 0092 计划重复 | 只追加 post-0094 最新段落，不创建平行路线图。 |
| 把计划写成完成 | 每个外部项明确 pending/live 证据要求。 |
| 任务编号漂移 | 0095 只作为计划刷新任务，下一步实现任务按下一个可用 ID 创建。 |
| 计划过大不可执行 | 拆为 Wave A/B/C/D，先做本地可执行核心质量切片。 |

# Assumptions and Falsification
- 假设：0093/0094 是当前已完成事实；若后续 `git log` 或任务状态被更改，本计划需刷新。
- 假设：主路线图继续作为 100% living plan；若 governance 决定迁移真相源，本任务需重新落点。
- 证伪条件：若当前 release 已具备真实 Bot/OIDC/SIEM/OTel/Vault/KMS/multi-replica live 证据但未登记，本计划的 pending 清单需调整。

# Critical Ambiguities
- 外部生产环境何时可用未知；本计划把外部 live 项拆到 Wave B。
- SDK/package 采用 PyPI、npm、container image 还是 examples-only 仍需后续任务确定。
- 第三方审计方的具体格式要求未知；当前只保证仓库内可复核审计包。

# Debug Evidence Contract
- 调试模式: Optional
- Not required：本任务不是 bugfix/regression 修复。
- 如任务文档校验失败，按 `auto-tasks` 文档契约修复占位符和任务树。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | `git status`、`git rev-parse`、主路线图、0093/0094 状态。 |
| TP-01.02 | OpenAPI、AsyncAPI、CloudEvents、Kubernetes、Backstage、Terraform、Temporal、OpenTelemetry、Google SRE、DORA、OWASP、NIST、SLSA、CycloneDX、GitHub attestation、Stripe 文档。 |
| TP-02.01 | `RESEARCH.md` 资源成熟度矩阵。 |
| TP-02.02 | `RESEARCH.md` Wave A/B/C/D 与不可伪造标准。 |
| TP-03.01 | 主路线图 post-0094 追加段。 |
| TP-03.02 | 0095 任务文档全量回填。 |
| TP-04.01 | `validate_task_docs.py`、`rg` 引用检查。 |
