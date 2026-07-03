# Repo Evidence
- 调试模式: `Optional`

| Evidence | Result |
| --- | --- |
| Current branch | `main`. |
| Current HEAD before 0118 docs | `55741bed0acba44645fd24586e87c6a28605347b` / `55741be feat: add external validation closure gate`. |
| Active prior task | 0117 changed external validation closure profiles and reduced manual triage from 184 to 1 on the 0116 pending list. |
| Main roadmap source | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`. |
| Requirements source | `docs/reference-materials/roadmap/测算基础设施需求文档.md`. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current branch/worktree only | No branch switch, merge, rebase or destructive git operation. |
| Planning task only | No live credential use and no production connection. |
| Single source of truth | Update the existing roadmap instead of creating a competing roadmap. |
| No fake 100% | All external systems without proof remain `外部连通验证待执行`. |
| Dirty 0117 context | Treat 0117 as prerequisite evidence and keep 0118 planning additive. |

# Change Boundary
| In Boundary | Out of Boundary |
| --- | --- |
| 0118 task docs and research report | Production runtime, external accounts, live smoke execution |
| Roadmap post-0117 section | Capability/provider business code |
| Task index entry | Git history rewrite or branch changes |

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Plan becomes broad slogan | Future tasks cannot execute | Use resource domains, concrete next tasks, evidence gates and blockers. |
| External docs become stale | Wrong version claims | Record official URLs and version-sensitive assumptions. |
| 100% overclaim | Audit failure | Keep non-claim and external pending language in every live domain. |
| Parallel truth source | Documentation drift | Append roadmap and point to it from task docs. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| FateCat 100% should be measured as infrastructure maturity, not feature count. | User redefines 100% as only local/offline skill completeness. |
| Closure plan routing is now good enough to drive external workstreams. | Auditors require a non-keyword classifier or workflow tracker integration before handoff. |
| Official infra patterns remain the right analogy. | A production operator rejects resource/control-plane framing and requires a different operating model. |

# Critical Ambiguities
- 外部 live 的真实平台、账号、token、域名、receiver、IdP、SIEM、OTel backend、Vault/KMS 和第三方审计主体仍未提供；这些不能由仓库内计划闭合。
- 100% 基础设施最终是否需要商业 SLA/SOC2/法律审计，当前仍是产品级决策，不在本任务内定稿。

# Debug Evidence Contract
- 本任务为规划任务，不要求 `DEBUG.md`。
- 若后续发现计划与代码事实冲突，必须记录冲突文件、证据命令和修正路径。

# Task Package Context Map
| File | Reason |
| --- | --- |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 100% living plan truth source. |
| `docs/reference-materials/roadmap/测算基础设施需求文档.md` | Requirements baseline. |
| `governance/tasks/0117-measurement-infrastructure-external-validation-closure-profile-expansion/` | Immediate predecessor evidence. |
| `contracts/fate/*` | Resource contract surface. |
| `scripts/*gate*.sh`, `scripts/*gate*.py` | Existing gate implementation surface. |
