# Execution Checklist
[x] TP-01.01 | P0 | 盘点八字/紫微现有 evidence surface | Verify: `rg -n "baziRuleDepth|ziweiRuleDepth|evidenceRefs|classics_rule_index" domains contracts scripts tests` | Gate: 可统计字段和来源明确 | Parallelizable: Yes
[x] TP-01.02 | P0 | 定义 tracked baseline、contract 和隐私边界 | Verify: `cat contracts/fate/evidence-coverage-baseline.json contracts/fate/evidence-coverage-trend-contract.json` | Gate: baseline 与 contract 列出 required checks、forbidden fragments、privacy/production boundary | Parallelizable: Yes
[x] TP-02.01 | P0 | 实现 CLI/wrapper、coverage metrics 和趋势比较 | Verify: `bash scripts/evidence-coverage-trend-gate.sh --output-json /tmp/fatecat-evidence-coverage-trend-0102.json` | Gate: 当前 baseline passed，断链或回退会 failed | Parallelizable: No
[x] TP-02.02 | P0 | 接入 local-ci summary、AGENTS、API 文档和 roadmap | Verify: `rg -n "evidence-coverage-trend|evidenceCoverageTrendGate" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/AGENTS.md tests/AGENTS.md docs/reference-materials` | Gate: quick local-ci 生成 evidence coverage artifact 路径 | Parallelizable: Yes
[x] TP-03.01 | P0 | 增加 regression tests | Verify: `.venv/bin/python -m pytest -q tests/regression/test_evidence_coverage_trend_gate.py` | Gate: pass、strict baseline fail、broken classics refs fail、CLI 输出覆盖 | Parallelizable: Yes
[x] TP-03.02 | P0 | 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0102-final` | Gate: 本地 quick CI 和 secret scan 通过 | Parallelizable: No
[x] TP-04.01 | P0 | 同步任务文档、INDEX 和验收清单 | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0102-measurement-infrastructure-evidence-coverage-trend --phase closeout` | Gate: task docs closeout validator passed | Parallelizable: No
[x] TP-04.02 | P0 | 提交、推送并记录远端状态 | Verify: `git status --short --branch && git ls-remote origin refs/heads/main` | Gate: 本地 HEAD 与 origin/main 匹配或明确说明远端状态 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
