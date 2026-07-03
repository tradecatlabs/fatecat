# Repo Evidence
| Evidence | Value |
| --- | --- |
| Current branch | `main` |
| Base HEAD | `eee30ece7da5fa580eb970db11e3b7e559727a56` / `eee30ec test: add event consumer replay contracts` |
| Worktree state | 0098 retention production cleanup staged gate files and 0099 planning docs are present in current worktree before commit. |
| Existing 100% source of truth | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| Latest completed infra slices | 0096 core corpus/report diff expansion; 0097 event consumer/replay contracts pushed. |
| Current infra slice | 0098 retention production cleanup staged gate local closeout passed; external live evidence remains pending. |
| Contract count signal | `find contracts/fate -maxdepth 2 -type f -name '*.json' | wc -l` -> `46` |
| Script count signal | `find scripts -maxdepth 1 -type f | wc -l` -> `146` |
| Regression file count signal | `find tests/regression -maxdepth 1 -type f -name 'test_*.py' | wc -l` -> `71` |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Current worktree contains 0098 changes | Do not revert or overwrite; distinguish local closeout from external live completion. |
| User asked for planning and research | This task writes plan/docs only; no business code or live production action. |
| External facts may change | Use official/fact-standard sources and mark source URLs in `RESEARCH.md`. |
| External live evidence absent | Mark `外部连通验证待执行`; do not infer production readiness. |
| Existing roadmap is source of truth | Update existing roadmap instead of creating a competing one. |

# Critical Ambiguities
- Whether production credentials will be available soon is unknown; plan must support both local-only and external-live waves.
- Whether 0098/0099 are committed separately or together is a version-control decision; local validation evidence is recorded.
- Third-party legal audit for imported knowledge/vendor assets is not available locally; mark as manual/external review.

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| The right 100% definition is infrastructure maturity, not prediction accuracy. | If user explicitly redefines 100% as business prediction hit rate, this plan must be replaced. |
| Current next local tasks should remain in Wave A. | If production credentials arrive, Wave B live tasks may preempt Wave A. |
| 0098 local closeout passed. | If later remote CI contradicts local evidence, reopen the relevant release-proof task. |

# Change Boundary
- Add and update only planning/task documentation and the main roadmap.
- Do not edit runtime code, scripts, contracts or tests for 0098 in this task.
- Do not commit, push or claim CI/live results unless explicitly executed later.

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Planning drift repeats earlier roadmap content | Medium | Add post-0098 delta and keep one roadmap source. |
| 0098 local closeout is mistaken as external live completion | High | Roadmap wording keeps external live evidence pending. |
| External source list becomes decorative | Medium | Map each infra standard to a concrete FateCat resource/gate. |
| 100% sounds like deterministic fortune accuracy | High | Define 100% as infra maturity; reject prediction-hit-rate claims. |

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix，不需要 `DEBUG.md`。
- 如果文档校验失败，以 validator 输出作为最小修复证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | Official infra standards and fact-standard docs. |
| TP-01.02 | `RESEARCH.md` mapping table. |
| TP-02.01 | Main roadmap, 0095 research plan, 0098 task docs. |
| TP-02.02 | `git status --short --branch`. |
| TP-03.01 | Resource model from `contracts/fate/*` and current registry categories. |
| TP-03.02 | Existing Wave A/B/C/D plus post-0098 deltas. |
| TP-04.01 | Roadmap and 0099 task docs. |
| TP-04.02 | `validate_task_docs.py` and `rg` placeholder checks. |
