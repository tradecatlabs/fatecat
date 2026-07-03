# Task Overview
- Task ID: `0090`
- Slug: `measurement-infrastructure-multi-surface-semantic-diff`
- Objective: `把标准 Markdown 多交付面同源能力从 registry 声明推进为本地可执行语义 diff gate，覆盖 API direct、API job、Web direct、Web job 与 Bot dry-run canonical renderer。`
- Status: `Done`

## In Scope

- 修复 API/Bot 标准 Markdown 八字路径仍默认走 legacy 引擎的问题，统一到 capability 引擎。
- 新增 `contracts/fate/delivery/multi-surface-semantic-diff.json`。
- 新增 `scripts/multi-surface-semantic-diff.py/.sh`，用北京测试样本对八字与紫微报告做 normalized semantic hash 对齐。
- 将 gate 接入 `contracts/fate/delivery/registry.json`、`scripts/local-ci.sh` quick profile 与 focused regression。
- 新增 `tests/regression/test_multi_surface_semantic_diff.py`。
- 更新 scripts/contracts/tests AGENTS、roadmap 和 task index。

## Out of Scope

- 不执行真实 Telegram Bot live smoke。
- 不执行真实 HF Space / 公网 API / 浏览器兼容性 live 验证。
- 不把 CLI JSON 输出改造成标准 Markdown。
- 不保存完整 Markdown 报告正文、真实用户输入、token、secret、DSN 或 webhook URL。

## Future-Optimal Task Contract

| Field | Value |
| --- | --- |
| Target end state | 每个标准 Markdown 交付面都只能通过同一 calculation/report chain 输出；本地 gate 能快速发现 API/Web/Bot dry-run 语义漂移。 |
| Real constraints | Bot live、HF Space、公网 API 和真实浏览器验证依赖外部 token、真实 URL 或外部平台权限；紫微 `asOf` 是运行时字段，跨异步任务存在秒级差异。 |
| Inertia constraints | delivery registry 已有 surface 声明，但缺少可执行语义 diff；API/Bot 历史默认 bazi legacy 引擎。 |
| Wrong concept / wrong boundary | 把“都调用了 generate_full_report”误认为标准 Markdown 完全同源；把 CLI JSON 或 Skill 文档当成 Markdown parity 证据。 |
| Kill list | 前端自拼报告；API/Bot legacy 八字报告；完整 Markdown 正文写入证据 JSON；用 live pending 假装通过。 |
| Proof point | `multi-surface-semantic-diff.sh` 对 bazi/ziwei 输出 `status=passed`，且只保存 hash/长度/行数/归一化策略。 |
| Falsifier | 任一 required surface semantic hash 不一致；Bot 不复用 canonical renderer；证据包含完整报告正文或敏感标记。 |
| Migration slice | 先覆盖本地 API/Web/Bot dry-run 标准 Markdown；后续接真实 Bot live、HF Space live 和浏览器 snapshot。 |
| Rejected short-term patches | 不只在文档里写“同源”；不跳过 Bot；不把紫微秒级 `asOf` 当业务差异。 |
| Future-optimal review owner | `auto-review: future-optimal-drift` |

## Ponytail Task Contract

| Field | Value |
| --- | --- |
| Existence check | 多端输出是测算基础设施的核心信任面；没有可执行 diff，registry 同源声明不可审计。 |
| Selected ladder rung | project-native script + existing TestClient/service functions；自研只做薄编排、hash、归一化和证据输出。 |
| Skipped scope | 真实 Bot live、HF Space live、公网 API live、CLI Markdown 化、浏览器视觉 snapshot。 |
| Ceiling / upgrade path | 后续可增加 Playwright copy snapshot、真实 Bot live diff、HF Space live diff、SDK client diff。 |
| Do-not-simplify | 不保存报告正文；不吞掉 hash mismatch；不把外部 pending 写成 passed。 |
| Minimal runnable check | `bash scripts/multi-surface-semantic-diff.sh --output-json <path>` |
| Complexity review owner | `auto-review: ponytail-complexity` |

## Document-Driven Task Contract

| Field | Value |
| --- | --- |
| Operating model update | not needed：基础设施定位不变。 |
| Toolchain model update | updated：新增 multi-surface semantic diff gate 并接入 `local-ci.sh`。 |
| Process update | updated：标准 Markdown 交付面变更需要语义 diff gate。 |
| Source-of-truth updates | updated：delivery contract、registry、scripts/tests/contracts AGENTS、roadmap、task index。 |
| Local README/AGENTS impact | updated：scripts/tests/contracts AGENTS。 |
| Contract/catalog/schema impact | updated：新增 `contracts/fate/delivery/multi-surface-semantic-diff.json`。 |
| ADR/Gate/module-context impact | not needed：沿用 DeliverySurface registry。 |
| Documentation exemption reason | none。 |
| Validation evidence | focused pytest、ruff、secret scan、quick CI 和 post-push current release proof。 |

## Task Package Tree

```text
TP-01 SPEC: 识别多端标准 Markdown 同源缺口
TP-02 PLAN: 定义 semantic diff gate、volatile normalization 和 no-body evidence
TP-03 BUILD: 实现 engine 收敛、contract、script、registry/local-ci/docs/tests
TP-04 TEST: 运行 focused pytest、ruff、secret scan、quick CI
TP-05 SHIP: commit/push，触发远端 CI，刷新 current proof/audit bundle
```

## Key Deliverables

- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `domains/experience-delivery/services/fatecat-delivery/src/bot.py`
- `contracts/fate/delivery/multi-surface-semantic-diff.json`
- `scripts/multi-surface-semantic-diff.py`
- `scripts/multi-surface-semantic-diff.sh`
- `tests/regression/test_multi_surface_semantic_diff.py`
- `scripts/local-ci.sh`

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
