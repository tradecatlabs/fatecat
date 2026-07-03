# Task Overview
- Task ID: `0094`
- Slug: `measurement-infrastructure-cli-skill-semantic-diff-expansion`
- Objective: `执行 0093 后的多端同源扩展切片：把 CLI/Skill 从 multi-surface semantic diff 的 not_in_scope 文本提升为本地可复核的 semantic evidence。CLI 必须通过根级 capability CLI 入口复用 CapabilityExecutor，Skill 必须通过仓库标准命令/文档链路证明复用同一 delivery/profile，不允许前端或 skill 自行拼报告，不保存完整报告正文，不声明真实 Bot/HF/API live 已完成。`
- Status: `Done`

## In Scope
- 扩展 `scripts/multi-surface-semantic-diff.py`，保留 API/Web/Bot Markdown hash 相等检查，并新增 CLI/Skill non-Markdown evidence surfaces。
- CLI evidence 复用 `scripts/capability-cli-smoke.py`，验证 bazi/ziwei/almanac/meihua production capability 和 planned liuyao 拒绝。
- Skill evidence 静态验证 `SKILL.md`、`references/commands.md`、`references/io-contract.md` 的标准命令链。
- 更新 `contracts/fate/delivery/multi-surface-semantic-diff.json`、delivery registry、AGENTS、测试和路线图。
- 更新命令参考和 IO 契约，使 Skill 文档可追溯到 capability CLI 与 delivery Markdown 边界。

## Out of Scope
- 不让 CLI 生成标准 Markdown。
- 不把 CLI/Skill 加入 API/Web/Bot Markdown hash 相等集合。
- 不执行真实 Telegram Bot、Hugging Face Space、公网 API、外部 webhook 或生产域名 live 验证。
- 不修改八字、紫微、黄历、梅花计算逻辑。
- 不新增 planned capability 的 production 实现。

## Task Package Tree
```text
TP-01 复核 0090/0093 现状
  TP-01.01 读取 multi-surface semantic diff 脚本/契约/测试
  TP-01.02 读取 CLI capability smoke 与 Skill 命令文档
TP-02 实现 non-Markdown evidence surfaces
  TP-02.01 在 diff 脚本中新增 CLI capability evidence
  TP-02.02 在 diff 脚本中新增 Skill command chain evidence
TP-03 契约、文档和测试接线
  TP-03.01 更新 semantic diff contract 和 registry
  TP-03.02 更新 commands/io-contract/AGENTS/roadmap
  TP-03.03 更新 regression tests
TP-04 验证与 closeout
  TP-04.01 运行 semantic diff gate 和 focused tests
  TP-04.02 运行 ruff/format/secret/quick gate
  TP-04.03 回填任务包并提交推送
```

## Requirement Alignment
- 用户目标：持续推进 100% 测算基础设施任务树，按优先级逐项落地并自检。
- 0092 路线图：0094 是 0093 后的下一项，本地可完成，解决 0090 未覆盖 CLI/Skill 的缺口。
- 0093 基础：已有 `scripts/capability-cli.sh` 和 `capability-cli-smoke`，0094 直接复用，不重复造轮子。
- 正确边界：CLI/Skill 提供同源证据，但不伪装成 Markdown 交付面；外部 live 继续保持 pending。

## Task Package Overview
| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | 复核 multi-surface 现状 | Done | `scripts/multi-surface-semantic-diff.py`、contract、tests |
| TP-01.02 | 复核 CLI/Skill 输入 | Done | `scripts/capability-cli-smoke.py`、`SKILL.md`、`references/*` |
| TP-02.01 | CLI evidence surface | Done | `nonMarkdownSurfaceEvidence.surface.cli` |
| TP-02.02 | Skill evidence surface | Done | `nonMarkdownSurfaceEvidence.surface.agent_skill` |
| TP-03.01 | Contract/registry | Done | `multi-surface-semantic-diff.json`、`registry.json` |
| TP-03.02 | Docs/AGENTS/roadmap | Done | `references/commands.md`、`references/io-contract.md`、AGENTS、roadmap |
| TP-03.03 | Regression tests | Done | `tests/regression/test_multi_surface_semantic_diff.py` |
| TP-04.01 | Semantic diff/focused tests | Done | gate passed；6 tests passed |
| TP-04.02 | Quality gates | Done | ruff passed；secret scan passed；local-ci quick passed |
| TP-04.03 | Closeout/Git | Done | task docs closeout ready; Git delivery handled after docs update |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
