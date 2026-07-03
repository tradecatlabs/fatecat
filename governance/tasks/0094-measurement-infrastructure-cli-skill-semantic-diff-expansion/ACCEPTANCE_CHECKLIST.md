# Acceptance Checklist

# Global Standards
- [x] API/Web/Bot 标准 Markdown hash equality 保持不变。
- [x] CLI/Skill 进入 `nonMarkdownSurfaceEvidence`，不进入 Markdown hash surfaces。
- [x] CLI evidence 复用 0093 capability CLI smoke。
- [x] Skill evidence 基于 tracked 文档/命令链，不依赖本机绝对 validator。
- [x] 不保存完整报告正文。
- [x] 不声明真实 Bot/HF/API live 已完成。

# Task Package Checklists
## TP-01.01 读取 multi-surface semantic diff 脚本/契约/测试

Verify: `sed -n '1,460p' scripts/multi-surface-semantic-diff.py`、contract、tests。

Gate: 确认 0090 只覆盖 API/Web/Bot Markdown，CLI/Skill 为 `not_in_scope`。

- [x] 现状已复核。

## TP-01.02 读取 CLI capability smoke 与 Skill 命令文档

Verify: `scripts/capability-cli-smoke.py`、`SKILL.md`、`references/commands.md`、`references/io-contract.md`。

Gate: 有可复用 CLI smoke；Skill 文档链可静态校验。

- [x] 可复用材料已复核。

## TP-02.01 在 diff 脚本中新增 CLI capability evidence

Verify: `nonMarkdownSurfaceEvidence.surface.cli`。

Gate: bazi/ziwei/almanac/meihua production capability passed；liuyao planned rejection exit 1。

- [x] CLI evidence 已新增并通过。

## TP-02.02 在 diff 脚本中新增 Skill command chain evidence

Verify: `nonMarkdownSurfaceEvidence.surface.agent_skill`。

Gate: `SKILL.md`、`references/commands.md`、`references/io-contract.md` snippets 全部存在。

- [x] Skill evidence 已新增并通过。

## TP-03.01 更新 semantic diff contract 和 registry

Verify: JSON contract parse and regression tests。

Gate: contract/registry 都包含 `requiredLocalEvidenceSurfaces`。

- [x] Contract 和 registry 已更新。

## TP-03.02 更新 commands/io-contract/AGENTS/roadmap

Verify: 文档包含 capability CLI 和 non-Markdown evidence 口径。

Gate: 不出现 CLI Markdown overclaim。

- [x] 文档已更新。

## TP-03.03 更新 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_multi_surface_semantic_diff.py tests/regression/test_capability_cli_smoke.py`。

Gate: 6 tests passed。

- [x] Regression 已更新并通过。

## TP-04.01 运行 semantic diff gate 和 focused tests

Verify: `bash scripts/multi-surface-semantic-diff.sh --output-json /tmp/fatecat-multi-surface-0094.json` and focused pytest。

Gate: semantic diff passed；CLI/Skill evidence passed。

- [x] Semantic diff gate 和 focused tests 已通过。

## TP-04.02 运行 ruff/format/secret/quick gate

Verify: ruff、secret scan、local-ci quick。

Gate: 全部 exit 0。

- [x] Ruff、secret scan 和 local-ci quick 已通过。

## TP-04.03 回填任务包并提交推送

Verify: task validator、git status、commit、push、gh run check。

Gate: clean worktree、pushed to origin/main；不伪造当前 commit CI。

- [x] 任务包已回填；Git delivery evidence 在提交推送后复核。
