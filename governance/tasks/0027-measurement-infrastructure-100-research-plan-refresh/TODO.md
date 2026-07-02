# Execution Checklist
[x] TP-01.01 | P0 | 收集外部官方资料 | Verify: `rg -n "OpenAPI|Stripe|Temporal|Backstage|Kubernetes|Terraform|OpenTelemetry|SRE|SLSA|OWASP|MLflow" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 官方资料覆盖 API、workflow、catalog、controller、provider、observability、SRE、supply chain、security、ML/eval | Parallelizable: No
[x] TP-01.02 | P0 | 提炼基础设施同构能力 | Verify: `rg -n "FateCat 同构要求|测算基础设施" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 外部资料已映射为 FateCat 资源模型、控制面、运行面、provider、评测、观测、安全和发布要求 | Parallelizable: No
[x] TP-02.01 | P0 | 读取当前仓库事实 | Verify: `git status --short --branch && sed -n '1,220p' governance/tasks/INDEX.md && find contracts/fate -maxdepth 3 -type f | sort` | Gate: 当前 worktree、任务索引和 contracts 事实已读取 | Parallelizable: No
[x] TP-02.02 | P0 | 区分完成度 | Verify: `rg -n "仍不是生产 100%|外部连通验证待执行|本地 worktree" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 本地已落地、仍待生产化、外部连通待执行分开表达 | Parallelizable: No
[x] TP-03.01 | P0 | 重写主路线图 | Verify: `git diff -- docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: 复用既有主路线图，不新增平行计划文件 | Parallelizable: No
[x] TP-03.02 | P0 | 写入任务树和验收口径 | Verify: `rg -n "D0 开发者接入面|MI-100 FateCat|下一批推荐任务|100% 总验收清单|不可伪造证据口径" docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | Gate: D0-D10、MI-100、0028+、总验收清单和不可伪造证据口径已写入 | Parallelizable: No
[x] TP-04.01 | P0 | 回填任务包文档 | Verify: `rg -n "\\{\\{[A-Z0-9_]+\\}\\}" governance/tasks/0027-measurement-infrastructure-100-research-plan-refresh docs/reference-materials/roadmap/测算基础设施100%实现计划.md || true` | Gate: 任务包无占位符 | Parallelizable: No
[x] TP-04.02 | P0 | 执行任务文档验证 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && git diff --check` | Gate: validators 和 diff check 通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。

## Deferred
- [ ] `0028`：scoped RBAC baseline。
- [ ] `0029`：OpenAPI / SDK / Sandbox。
- [ ] `0030`：durable job store。
- [ ] `0031`：webhook callback。
- [ ] `0032`：provider lifecycle gates。
- [ ] `0033`：八字/紫微 L4 golden/evidence。
