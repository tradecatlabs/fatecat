# Execution Checklist
[x] TP-01.01 | P0 | 盘点 MI-05、bazi/ziwei fixture、executor 和 Markdown gate | Verify: `rg -n "MI-05|bazi-ziwei|snapshotGate|coverage_matrix_cases|rule_depth_cases" docs domains tests scripts` | Gate: L4 baseline 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 bazi/ziwei L4 golden smoke 脚本 | Verify: `bash scripts/bazi-ziwei-l4-golden-smoke.sh --profile quick --output-json /tmp/fatecat-bazi-ziwei-l4.json` | Gate: status passed | Parallelizable: No
[x] TP-02.02 | P0 | 支持 quick/full profile 与脱敏 summary 输出 | Verify: `python3 -m json.tool /tmp/fatecat-bazi-ziwei-l4.json` | Gate: summary 有 profile、availableCaseCount、executedCaseCount 和 privacyBoundary | Parallelizable: No
[x] TP-02.03 | P0 | 接入 quick local-ci | Verify: `rg -n "bazi ziwei L4 golden smoke|test_bazi_ziwei_l4_golden_smoke" scripts/local-ci.sh` | Gate: quick CI 包含脚本和测试 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 L4 golden smoke pytest | Verify: `.venv/bin/python -m pytest -q tests/regression/test_bazi_ziwei_l4_golden_smoke.py` | Gate: focused pytest passes | Parallelizable: No
[x] TP-03.02 | P0 | 运行 focused tests、ruff、format 和 quick CI | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-bazi-ziwei-l4` | Gate: quick CI passes | Parallelizable: No
[x] TP-04.01 | P1 | 同步 API 文档、roadmap、专项基线、AGENTS 和任务索引 | Verify: `rg -n "bazi-ziwei-l4-golden-smoke|MI-05|0034" docs/reference-materials scripts/AGENTS.md governance/tasks/INDEX.md` | Gate: 不夸大专业能力 100% | Parallelizable: No
[x] TP-04.02 | P0 | 生成任务 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0034-bazi-ziwei-l4-golden-evidence --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
