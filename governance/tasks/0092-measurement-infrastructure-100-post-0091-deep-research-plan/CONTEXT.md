# Repo Evidence
| Evidence | Result |
| --- | --- |
| `git rev-parse HEAD` | `44cbeddc1d9aaf6dda3fe6b2d306eb27cdd97296` |
| `git log -1 --oneline` | `44cbedd feat: add retention cleanup baseline` |
| `git status --short --branch` | `main...origin/main` plus current 0092 planning docs changes |
| `gh run list --limit 5` | Acceptance `28657479378` success and Container `28657481029` success for `44cbedd` |
| 0091 task | `governance/tasks/0091-measurement-infrastructure-retention-cleanup-baseline/STATUS.md` records local validation and external pending boundaries |
| Current audit contract | `contracts/fate/audit/current-bundle.json` |
| Audit handoff contract | `contracts/fate/audit/handoff.json` |
| Main roadmap | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |

# Constraints Matrix
| Constraint | Meaning |
| --- | --- |
| Planning-only | 本任务只落盘调研和计划，不改业务实现。 |
| No fake live evidence | 没有真实 token、endpoint、外部账号或平台权限时，必须写 `外部连通验证待执行`。 |
| Current branch only | 只分析当前 `main` worktree，不切换分支、不改写历史。 |
| Source-of-truth reuse | 复用现有 roadmap、contracts 和 governance/tasks，不创建平行计划体系。 |
| Capability-first | 新术数能力必须先进入 capability/provider/evidence/evaluation/security/release/audit 协议，不混入默认综合八字报告。 |

# Change Boundary
Allowed:
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0092-measurement-infrastructure-100-post-0091-deep-research-plan/`
- `governance/tasks/INDEX.md`

Not allowed:
- 业务源码、API 行为、provider 算法、数据库 schema、CI workflow 和部署脚本。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把本地 baseline 写成生产完成 | 审计失真，100% 口径不可用 | 所有外部项显式标记 `外部连通验证待执行`。 |
| 计划和当前 0091 后事实不一致 | 后续任务优先级错误 | 使用 `git`、`gh`、contracts 和 task index 复核。 |
| 平行路线图漂移 | 文档真相源分裂 | 只追加主路线图 Post-0091 章节。 |
| 功能堆叠压过基础设施闭环 | 架构退化为工具集合 | 计划按资源域和证据闭环排序，不按术数模块数量排序。 |

# Assumptions and Falsification
- Assumption: 0091 后当前 release proof 和 audit bundle baseline 已可作为本地/远端当前提交证据入口。
- Falsifier: 若后续验证发现 `44cbedd` 的远端 Acceptance/Container 不是 success，Post-0091 计划中的当前事实必须回滚修正。
- Assumption: 100% 基础设施不是预测准确率 100%，而是基础设施成熟度和证据闭环 100%。
- Falsifier: 若计划中出现“预测命中率 100%”“外部 live 已完成但无证据”等表述，任务不得 close。

# Critical Ambiguities
- 是否优先执行真实外部 live 项取决于用户是否提供真实 token、域名、Postgres DSN、IdP/SIEM/OTel/Vault 权限。
- 若没有外部权限，后续只能继续执行本地可验证切片，例如 CLI capability command、CLI/Skill semantic diff、core corpus 扩容、Postgres cleanup gate。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务是 planning-only，不处理已复现 bug。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | Git 状态、0091、远端 CI、audit/release contracts |
| TP-02 | 外部一手资料 source matrix |
| TP-03 | Post-0091 资源域、任务队列、外部阻断项 |
| TP-04 | Roadmap、任务文档、validator |
