# Repo Evidence
- 调试模式: Optional
- `git status --short --branch`：当前分支 `main...origin/main`，worktree 存在大量未提交修改和未跟踪任务/contract/script/test 文件。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`：本轮刷新主文档。
- `docs/reference-materials/roadmap/测算基础设施需求文档.md`：已有需求基线，定义 FateCat 是面向 Agent 与应用开发者的测算基础设施。
- `governance/tasks/INDEX.md`：`0010` 到 `0026` 已登记多个基础设施切片，包含资源/API/job/provider/report/eval/observability/security/delivery。
- `contracts/fate/`：已有 capability、provider、report、evaluation、observability、security、delivery 等契约目录。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 当前任务只做调研与计划 | 不改业务代码、不实现后续功能 |
| 外部资料必须可复核 | 使用官方文档链接，不把博客结论当事实 |
| 当前 worktree 未提交 | 文档只称“本地 worktree 已落地”，不称远端已验证 |
| 生产能力不能夸大 | 真实域名、Bot、OIDC、SIEM、监控平台统一标注外部连通验证待执行 |
| 后续任务必须可执行 | 给出 `0028+` 推荐任务顺序和验收证据 |

# Change Boundary
- 可改：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`、0027 任务文档。
- 不改：业务源码、测试脚本、contract schema、CI、生产配置、真实 secret。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 计划继续膨胀成空泛愿景 | 后续无法执行 | 每个域给出交付物、证据和下一任务 |
| 把本地 dirty worktree 说成远端完成 | 审计失真 | 明确当前 worktree 未提交、生产外部验证待执行 |
| 误把新增术数功能当基础设施主线 | 默认报告污染 | 计划强调 capability/provider/promotion gate 先于堆功能 |

# Assumptions and Falsification
- 假设：测算基础设施应同构于 API infra、workflow infra、platform engineering、SRE、MLOps 和 supply chain。
- 证伪条件：如果用户把目标收缩为单站点/单报告工具，则 D0-D10 里的开发者平台、SRE、供应链、OIDC/SIEM 可降级。
- 当前未触发证伪：用户明确要求最高层级“测算基础设施”。

# Critical Ambiguities
- 是否要优先生产上线，还是优先补本地工程闭环：本计划按“先本地可证据化，再生产 live”排序。
- OAuth/OIDC 具体供应商未定：后续任务只定义能力，真实接入需用户提供生产身份系统选择。
- 生产监控/SIEM 平台未定：后续任务只要求外部连通证据，不指定厂商。

# Debug Evidence Contract
- 本任务不是 bugfix；无需维护 `DEBUG.md`。
- 若 validator 失败，修复任务文档契约并在 `STATUS.md` 记录验证结果。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 外部官方资料调研，提炼基础设施同构能力。 |
| TP-02 | 当前 worktree、路线图、任务索引和 contracts 事实盘点。 |
| TP-03 | 主路线图重写：D0-D10、MI-100、`0028+`、验收口径。 |
| TP-04 | 任务包回填和 validator 收口。 |

# Blockers
- 无阻塞。本任务不依赖生产凭证、外部服务器或远端 CI。
