# Acceptance Checklist

# Global Standards
- [x] 不残留模板占位符。
- [x] 任务包包含 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 生命周期门禁。
- [x] `CONTEXT.md` 声明 `调试模式: Optional`。
- [x] Gate 不连接真实外部系统，不读取真实 `.env`、token、secret 或 DSN。
- [x] `passed` 不能被解释为预测准确率、专业能力 100% 或外部 live 完成。
- [x] final quick local-ci、secret scan 和 closeout validator 通过。
- [x] 版本控制状态与远端状态收口。

# Task Package Checklists
## TP-01.01
Verify: `rg -n "baziRuleDepth|ziweiRuleDepth|evidenceRefs|classics_rule_index" domains contracts scripts tests`

Gate: evidence 来源已确认。

- [x] rule depth registry 已确认。
- [x] classics rule index 已确认。
- [x] analysisEvidence 和 Report evidenceRefs 已确认。

## TP-01.02
Verify: `cat contracts/fate/evidence-coverage-baseline.json contracts/fate/evidence-coverage-trend-contract.json`

Gate: contract 能指导 gate 和审计人员复核。

- [x] capability minimums 已列出。
- [x] forbidden report fragments、privacy boundary 和 production boundary 已列出。
- [x] Report evidenceRefs completeRatio 已纳入 baseline。

## TP-02.01
Verify: `bash scripts/evidence-coverage-trend-gate.sh --output-json /tmp/fatecat-evidence-coverage-trend-0102.json`

Gate: baseline pass 与负向失败路径可验证。

- [x] CLI/wrapper 可执行。
- [x] broken refs 会形成 finding。
- [x] baseline 回退会形成 finding。

## TP-02.02
Verify: `rg -n "evidence-coverage-trend|evidenceCoverageTrendGate" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/AGENTS.md tests/AGENTS.md docs/reference-materials`

Gate: local-ci 和架构说明已同步。

- [x] local-ci 生成 evidence coverage artifact。
- [x] local-ci summary 输出 evidence coverage artifact 路径。
- [x] `AGENTS.md` 和人类文档记录入口。

## TP-03.01
Verify: `.venv/bin/python -m pytest -q tests/regression/test_evidence_coverage_trend_gate.py`

Gate: 关键路径有 regression 覆盖。

- [x] current baseline passed 覆盖。
- [x] strict baseline fail 覆盖。
- [x] broken classics refs fail 覆盖。
- [x] CLI summary 写出覆盖。

## TP-03.02
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0102-final`

Gate: 本地发布前门禁通过。

- [x] evidence coverage smoke passed。
- [x] focused pytest passed。
- [x] ruff check/format passed。
- [x] quick local-ci passed。
- [x] secret scan passed。
- [x] diff whitespace check passed。

## TP-04.01
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0102-measurement-infrastructure-evidence-coverage-trend --phase closeout`

Gate: 任务文档 closeout 契约通过。

- [x] `README.md`、`CONTEXT.md`、`PLAN.md`、`TODO.md`、`STATUS.md`、`ACCEPTANCE.md`、`ACCEPTANCE_CHECKLIST.md` 已同步。
- [x] `governance/tasks/INDEX.md` 中 0102 状态正确。
- [x] closeout validator passed。

## TP-04.02
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 版本控制收口，不伪造远端 CI。

- [x] scoped files staged and committed。
- [x] push to `origin/main` completed。
- [x] 本地 HEAD 与 origin/main 匹配。
- [x] GitHub Actions 对当前 commit 的状态如实记录。
